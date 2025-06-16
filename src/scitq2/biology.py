import csv
import json
import subprocess
import urllib.request
from typing import Any, Dict, Iterator, List, Optional


# Only fields that exist in ENA (and possibly SRA after remapping)
ALLOWED_FIELDS = {
    "run_accession", "first_public", "last_updated", 
    "experiment_accession", "library_name", "library_strategy", "library_selection",
    "library_source", "library_layout", "instrument_platform", "instrument_model",
    "study_accession", "sample_accession", "tax_id", "scientific_name", "sample_alias", "secondary_sample_accession"
}

NUMERIC_FIELDS = {
    "insert_size", "tax_id", "read_count", "base_count", "average_read_length", "size_mb", "read_count", "base_count", 
    "average_read_length", "size_mb", "insert_size", 
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
    return {k: v for k, v in record.items() if k in ALLOWED_FIELDS}


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
    def __init__(self, tag: str, records: List[Dict[str, Any]], is_sra: bool):
        self.tag = tag
        self._records = records
        self._is_sra = is_sra
        self._compute_fields()

    def _compute_fields(self):
        self._fields = {}
        for key in ALLOWED_FIELDS:
            values = {r.get(key) for r in self._records if key in r}
            values.discard(None)
            self._fields[key] = list(values)

        self.fastqs = [
            f"run+fastq{'@sra' if self._is_sra else ''}://{r['run_accession']}"
            for r in self._records if 'run_accession' in r
        ]

    def _get_singular(self, name: str):
        values = self._fields.get(name, [])
        if len(values) == 1:
            return values[0]
        return Undefined

    def _get_plural(self, name: str):
        return self._fields.get(name, [])


def _group_samples(data: List[Dict[str, Any]], group_by: str, is_sra: bool) -> Dict[str, SampleGroup]:
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for record in data:
        tag = record.get(group_by)
        if tag:
            groups.setdefault(tag, []).append(record)
    return {tag: SampleGroup(tag, records, is_sra) for tag, records in groups.items()}

def ENA(identifier: str, group_by: str, event_name: str, filter: Optional[SampleFilter] = None) -> Iterator[Sample]:
    url = (
        "https://www.ebi.ac.uk/ena/portal/api/filereport"
        f"?accession={identifier}"
        "&result=read_run"
        "&format=json"
        "&fields="
        "run_accession,first_public,last_updated,read_count,base_count,average_read_length,"
        "size_mb,experiment_accession,library_name,library_strategy,library_selection,"
        "library_source,library_layout,insert_size,instrument_platform,instrument_model,"
        "study_accession,sample_accession,tax_id,scientific_name,sample_alias,secondary_sample_accession"
    )
    with urllib.request.urlopen(url) as response:
        raw = json.load(response)

    data = [_filter_fields(r) for r in raw]
    if filter:
        data = [r for r in data if filter.matches(r)]

    return _group_samples(data, group_by, is_sra=False)


def SRA(identifier: str, group_by: str, event_name: str, filter: Optional[SampleFilter] = None) -> Iterator[Sample]:
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
            "average_read_length": r.get("avgLength"),
            "size_mb": r.get("size_MB"),
            "first_public": r.get("ReleaseDate"),
            "last_updated": r.get("LoadDate"),
        }

    data = [_filter_fields(normalize_headers(r)) for r in lines]
    if filter:
        data = [r for r in data if filter.matches(r)]

    return _group_samples(data, group_by, is_sra=True)
