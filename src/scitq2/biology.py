import csv
import json
import subprocess
import urllib.request
from typing import Any, Dict, Iterator, List, Optional, Iterable, Mapping, Literal
import re
from .uri import URI, URIObject
import sys

from typing import Optional, List, Dict


# Only fields that exist in ENA (and possibly SRA after remapping)
ALLOWED_FIELDS = {
    "run_accession", "first_public", "last_updated", 
    "experiment_accession", "library_name", "library_strategy", "library_selection",
    "library_source", "library_layout", "instrument_platform", "instrument_model",
    "study_accession", "sample_accession", "scientific_name", "sample_alias", "secondary_sample_accession",
    "insert_size", "tax_id", "read_count", "base_count", "nominal_length", "fastq_bytes", "read_count", "base_count"
}

NUMERIC_FIELDS = {
    "insert_size", "tax_id", "read_count", "base_count", "nominal_length", "fastq_bytes", "read_count", "base_count", 
}


class FieldExpr:
    def __init__(self, field: str, op: str, value: Any):
        self.field = field
        self.op = op
        self.value = value

    def matches(self, record: Dict[str, Any]) -> bool:
        val = record.get(self.field)
        if self.op == "==":
            return val == self.value
        elif self.op == "in":
            return val in self.value
        elif self.op in {">", ">=", "<", "<="}:
            try:
                return eval(f"float(val) {self.op} float(self.value)")
            except Exception:
                return False
        else:
            raise ValueError(f"Unsupported operator: {self.op}")

    def __repr__(self):
        return f"{self.field} {self.op} {self.value}"


class FieldBuilder:
    def __init__(self, field: str):
        self.field = field

    def __eq__(self, value): return FieldExpr(self.field, "==", value)
    def isin(self, values): return FieldExpr(self.field, "in", values)

    def __check_numeric(self):
        if self.field not in NUMERIC_FIELDS:
            raise TypeError(f"Field '{self.field}' does not support numeric comparisons")

    def __ge__(self, value): self.__check_numeric(); return FieldExpr(self.field, ">=", value)
    def __gt__(self, value): self.__check_numeric(); return FieldExpr(self.field, ">", value)
    def __le__(self, value): self.__check_numeric(); return FieldExpr(self.field, "<=", value)
    def __lt__(self, value): self.__check_numeric(); return FieldExpr(self.field, "<", value)


# Static filter interface (S.<field_name>) — EBI field names only
class S:
    """
    Static filter interface for ENA/SRA fields.
    This class provides a set of fields that can be used to filter samples
    based on their attributes such as run_accession, first_public, last_updated,
    read_count, base_count, average_read_length, size_mb, experiment_accession,
    library_name, library_strategy, library_selection, library_source, library_layout,
    insert_size, instrument_platform, instrument_model, study_accession,
    sample_accession, tax_id, scientific_name, sample_alias, and secondary_sample_accession.
    Usage:
    sample_filter = SampleFilter(
        S.library_strategy == "WGS",
        S.read_count >= 1000000,
        S.first_public >= "2020-01-01"
    )
    """
    run_accession = FieldBuilder("run_accession")
    first_public = FieldBuilder("first_public")
    last_updated = FieldBuilder("last_updated")
    read_count = FieldBuilder("read_count")
    base_count = FieldBuilder("base_count")
    average_read_length = FieldBuilder("average_read_length")
    size_mb = FieldBuilder("size_mb")
    experiment_accession = FieldBuilder("experiment_accession")
    library_name = FieldBuilder("library_name")
    library_strategy = FieldBuilder("library_strategy")
    library_selection = FieldBuilder("library_selection")
    library_source = FieldBuilder("library_source")
    library_layout = FieldBuilder("library_layout")
    insert_size = FieldBuilder("insert_size")
    instrument_platform = FieldBuilder("instrument_platform")
    instrument_model = FieldBuilder("instrument_model")
    study_accession = FieldBuilder("study_accession")
    sample_accession = FieldBuilder("sample_accession")
    tax_id = FieldBuilder("tax_id")
    scientific_name = FieldBuilder("scientific_name")
    sample_alias = FieldBuilder("sample_alias")
    secondary_sample_accession = FieldBuilder("secondary_sample_accession")


class SampleFilter:
    def __init__(self, *expressions: FieldExpr):
        self.expressions = expressions

    def matches(self, record: Dict[str, Any]) -> bool:
        return all(expr.matches(record) for expr in self.expressions)


class Sample:
    def __init__(self, tag: str, fields: Dict[str, Any]):
        self.tag = tag
        self.fields = fields

    def __getattr__(self, name):
        return self.fields.get(name)

    def __repr__(self):
        return f"<Sample {self.tag}>"


def _filter_fields(record: Dict[str, Any]) -> Dict[str, Any]:
    return {k: tuple(map(int,v.split(';'))) if k=='fastq_bytes' else 
                (int(v) if k in NUMERIC_FIELDS else
                    v
                )
            for k, v in record.items() if k in ALLOWED_FIELDS}


# Sentinel value for inconsistent fields
Undefined = object()

def with_properties(cls):
    for field in ALLOWED_FIELDS:
        singular = field
        plural = field + "s"

        def make_singular(name=singular):
            return property(lambda self: self._get_singular(name), doc=f"Singular value of '{name}' or Undefined.")

        def make_plural(name=singular):
            return property(lambda self: self._get_plural(name), doc=f"All values of '{name}' as a list.")

        setattr(cls, singular, make_singular())
        setattr(cls, plural, make_plural())

    return cls


@with_properties
class SampleGroup:
    def __init__(self, tag: str, records: List[Dict[str, Any]], download_method: str = '', from_uri: bool = False):
        self.tag = tag
        self._records = records
        if download_method:
            self._uri_option = '@' + download_method
        else:
            self._uri_option = ''
        self.from_uri = from_uri
        self._compute_fields()

    def _compute_fields(self):
        self._fields = {}
        for key in ALLOWED_FIELDS:
            values = {r[key] for r in self._records if key in r}
            values.discard(None)
            self._fields[key] = list(values)

        # Prefer directly provided FASTQ URIs if present (URI-based discovery),
        # otherwise fall back to building from run_accession (ENA/SRA sources).
        if self.from_uri:
            uris: List[str] = []
            for r in self._records:
                uris.extend(r['fastqs'])
            self.fastqs = uris
        else:
            self.fastqs = [
                f"run+fastq{self._uri_option}://{r['run_accession']}" if isinstance(r, dict) else f"run+fastq{self._uri_option}://{getattr(r, 'run_accession')}"
                for r in self._records
                if (isinstance(r, dict) and ('run_accession' in r)) or (not isinstance(r, dict) and hasattr(r, 'run_accession'))
            ]

    def _get_singular(self, name: str):
        values = self._fields.get(name, [])
        if len(values) == 1:
            return values[0]
        return Undefined

    def _get_plural(self, name: str):
        return self._fields.get(name, [])


def _group_samples(data: List[Dict[str, Any]], group_by: str, download_method: str = '') -> Iterator[SampleGroup]:
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for record in data:
        tag = record.get(group_by)
        if tag:
            groups.setdefault(tag, []).append(record)
    return [SampleGroup(tag, records, download_method) for tag, records in groups.items()]

def ENA(identifier: str, group_by: str, filter: Optional[SampleFilter] = None, use_ftp: bool = False, use_aspera: bool = False) -> Iterator[SampleGroup]:
    if group_by not in ALLOWED_FIELDS:
        raise ValueError(f"Invalid group_by field: {group_by}. Must be one of {ALLOWED_FIELDS}")
    url = (
        "https://www.ebi.ac.uk/ena/portal/api/filereport"
        f"?accession={identifier}"
        "&result=read_run"
        "&format=json"
        "&fields="
        "run_accession,first_public,last_updated,read_count,base_count,nominal_length,"
        "fastq_bytes,experiment_accession,library_name,library_strategy,library_selection,"
        "library_source,library_layout,instrument_platform,instrument_model,"
        "study_accession,sample_accession,tax_id,scientific_name,sample_alias,secondary_sample_accession"
    )
    try:
        with urllib.request.urlopen(url) as response:
            raw = json.load(response)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise ValueError(f"Identifier '{identifier}' not found in ENA")
        body = e.read().decode("utf-8", errors="replace").strip()
        print(f"HTTP request {url} failed with status {e.code}: {e.reason}", file=sys.stderr)
        print(f"⇨ Response body:\n{body}", file=sys.stderr)
        raise

    data = [_filter_fields(r) for r in raw]
    if filter:
        data = [r for r in data if filter.matches(r)]
    
    return _group_samples(data, group_by, download_method='ena-aspera' if use_aspera else 'ena-ftp' if use_ftp else '')


def SRA(identifier: str, group_by: str, event_name: str, filter: Optional[SampleFilter] = None) -> Iterator[SampleGroup]:
    cmd = [
        "docker", "run", "--rm", "ncbi/edirect",
        "esearch", "-db", "sra", "-query", identifier,
        "|", "efetch", "-format", "runinfo"
    ]
    joined = " ".join(cmd)
    process = subprocess.run(joined, shell=True, stdout=subprocess.PIPE, check=True)
    text = process.stdout.decode("utf-8")
    lines = list(csv.DictReader(text.splitlines()))

    def normalize_headers(r: Dict[str, str]) -> Dict[str, str]:
        return {
            "run_accession": r.get("Run"),
            "experiment_accession": r.get("Experiment"),
            "sample_accession": r.get("Sample"),
            "study_accession": r.get("SRAStudy"),
            "library_name": r.get("LibraryName"),
            "library_strategy": r.get("LibraryStrategy"),
            "library_source": r.get("LibrarySource"),
            "library_selection": r.get("LibrarySelection"),
            "library_layout": r.get("LibraryLayout"),
            "insert_size": r.get("InsertSize"),
            "instrument_platform": r.get("Platform"),
            "instrument_model": r.get("Model"),
            "scientific_name": r.get("ScientificName"),
            "tax_id": r.get("TaxID"),
            "sample_alias": r.get("SampleName"),
            "secondary_sample_accession": r.get("BioSample"),
            "base_count": r.get("bases"),
            "read_count": r.get("spots"),
            "nominal_length": r.get("avgLength"),
            "fastq_bytes": r.get("size_MB")* 1_000_000,  # Convert MB to bytes
            "first_public": r.get("ReleaseDate"),
            "last_updated": r.get("LoadDate"),
        }

    data = [_filter_fields(normalize_headers(r)) for r in lines]
    if filter:
        data = [r for r in data if filter.matches(r)]

    return _group_samples(data, group_by, download_method='sra-tools')

# -----------------------------
# FASTQ discovery on top of URI
# -----------------------------

_READ_REGEX = re.compile(r".*(1|2)\.f.*q(\.gz)?$", re.IGNORECASE)


def find_sample_parity(fastqs: List[str]) -> Dict[str, Any]:
    """classify a sample as paired/single/unknown based on FASTQ names"""
    r1_list: List[str] = []
    r2_list: List[str] = []
    extras: List[str] = []
    for fq in fastqs:
        m = _READ_REGEX.match(fq)
        if m:
            if m.group(1) == "1":
                r1_list.append(fq)
            elif m.group(1) == "2":
                r2_list.append(fq)
            else:
                extras.append(fq)
        else:
            extras.append(fq)
    nR1, nR2 = len(r1_list), len(r2_list)
    if nR1 == nR2 and nR1 > 0:
        detected = "paired"
    elif (nR1 == 0 and nR2 == 0) or (nR1 > 0 and nR2 == 0) or (nR2 > 0 and nR1 == 0):
        detected = "single"
    else:
        detected = "unknown"  # nR1>0, nR2>0, nR1!=nR2
    return {
        "detected": detected,
        "R1": r1_list,
        "R2": r2_list,
        "extras": extras,
        "nR1": nR1,
        "nR2": nR2,
    }

def FASTQ(
    roots: Iterable[str] | str,
    *,
    group_by: str = "folder",             # "folder", "pattern.<name>", or "none"
    layout: Literal["auto", "paired", "single"] = "auto",
    only_read1: Optional[bool] = None,     # defaults True only when layout=="single"
    strict_pairs: bool = False,
    allow_unknown: bool = True,            # if False, drop unknown when aligning to single
    study_vote: Literal["majority", "all"] = "majority",
    filter: Optional[str] = None,
    pattern: Optional[str] = None,
) -> List[SampleGroup]:
    """
    High-level FASTQ source on top of URI.find().

    Returns a list of sample dicts with keys:
      - sample_accession, project_accession
      - detected_layout: 'paired' | 'single' | 'unknown'
      - study_layout: 'paired' | 'single' (when layout='auto')
      - effective_layout: 'paired' | 'single' (post-alignment)
      - reads: { 'R1': [...], 'R2': [...] } when effective_layout == 'paired'
      - fastqs: list[str] (final selection after enforcement)
      - notes: list[str]
      - any extra fields requested via `fields`
    """

    # Normalize roots to a list for URI.find
    if isinstance(roots, str):
        roots_list = [roots]
    else:
        roots_list = list(roots)

    # Build field_map for URI.find consistent with user's conventions
    field_map: Dict[str, str] = {
        "fastqs": "file.uris",
    }
    # group id resolution
    if group_by == "folder":
        field_map.update({
            "sample_accession": "folder.name",
            "project_accession": "folder.basename",
        })
    elif group_by.startswith("pattern."):
        group_name = group_by.split(".", 1)[1]
        field_map.update({
            "sample_accession": f"file.pattern.{group_name}",
            "project_accession": "folder.basename",  # may be Undefined if not meaningful
        })
    elif group_by == "none":
        field_map.update({
            "sample_accession": "file.basename",
            "project_accession": "folder.basename",
        })
    else:
        raise ValueError("group_by must be 'folder', 'pattern.<name>', or 'none'")

    # Call URI.find once per root and concatenate results
    fastq_uris: List[URIObject] = []
    if filter:
        filter = filter + '.f*q.gz'
    else:
        filter = '*.f*q.gz'
    for root in roots_list:
        part = URI.find(root, group_by=group_by, pattern=pattern, filter=filter, field_map=field_map)
        # Expect `part` to be a list/iter of dicts with keys from fm
        fastq_uris.extend(list(part))

    # First pass: classify per-sample (collect tuples)
    classified_samples: List[Dict[str, any]] = []
    paired_count = 0
    nonpaired_count = 0

    for uri in fastq_uris:
        fastqs = list(uri.fastqs or [])
        sample_fastqs = find_sample_parity(fastqs)
        detected_layout = sample_fastqs["detected"]
        if detected_layout == "paired":
            paired_count += 1
        else:
            nonpaired_count += 1
        sample = {
            "sample_accession": getattr(uri, "sample_accession", None),
            "project_accession": getattr(uri, "project_accession", None),
            "fastqs": fastqs,
            "detected_layout": detected_layout,
            "R1": sample_fastqs["R1"],
            "R2": sample_fastqs["R2"],
            "extras": sample_fastqs["extras"],
        }
        classified_samples.append(sample)

    # Decide study vote if needed
    if layout == "auto":
        if study_vote == "all":
            study_layout = "paired" if (paired_count > 0 and nonpaired_count == 0) else "single"
        else:  # majority
            study_layout = "paired" if paired_count >= nonpaired_count else "single"
    elif layout == "paired":
        study_layout = "paired"
    else:
        study_layout = "single"

    # Alignment & selection
    out: List[SampleGroup] = []
    for sample in classified_samples:
        if layout == "auto":
            if study_layout == "single":
                sample['effective_layout'] = "single"
                final_fastqs = sample['fastqs']  # keep as-is
            else:  # paired study
                if sample['detected_layout'] == "paired":
                    sample['effective_layout'] = "paired"
                    final_fastqs = (sample["R1"] + sample["R2"]) if strict_pairs else \
                        (sample["R1"] + sample["R2"] + sample["extras"])
                    #if strict_pairs and extras:
                    #    notes.append("excluded extras (strict_pairs)")
                else:
                    sample['effective_layout'] = "single"
                    final_fastqs = sample['fastqs']
        elif layout == "paired":
            if sample["detected_layout"] != "paired":
                # one day print or log a warning
                continue
            else:
                sample['effective_layout'] = "paired"
                final_fastqs = (sample["R1"] + sample["R2"]) if strict_pairs else \
                        (sample["R1"] + sample["R2"] + sample["extras"])
                #if strict_pairs and extras:
                #    notes.append("excluded extras (strict_pairs)")
        else:  # layout == "single"
            sample['effective_layout'] = "single"
            if sample["detected_layout"] == "paired":
                if (only_read1 or only_read1 is None)  and sample["R1"]:
                    final_fastqs = sample["R1"]
                else:
                    continue
            elif sample["detected_layout"] == "single" or allow_unknown:
                final_fastqs = sample["fastqs"]

        sample["library_layout"] = study_layout
        sample["fastqs"] = final_fastqs

        out.append(SampleGroup(sample.get("sample_accession",""), [sample], from_uri=True))

    return out
