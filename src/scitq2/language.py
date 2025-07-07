from typing import Optional, Tuple

class Language:
    """Abstract base class for workflow step languages (Shell, Raw, etc)."""
    def compile_command(self, command: str) -> str:
        raise NotImplementedError("Must be implemented by subclasses.")
    def executable(self) -> Optional[str]:
        return None
        

class Raw(Language):
    """Default language: run the command as-is without shell injection or helpers."""
    def compile_command(self, command: str) -> str:
        return command


class Shell(Language):
    VALID_SHELLS = {"bash", "sh", "dash", "zsh"}

    ERREXIT = "errexit"
    PIPEFAIL = "pipefail"
    HELPERS = "helpers"

    def __init__(self, shell: str = "bash", options: Optional[Tuple[str, ...]] = None):
        if shell not in self.VALID_SHELLS:
            raise ValueError(f"Unsupported shell: '{shell}'")

        self.shell = shell
        self.options = set(options or ())

        if self.shell != "bash" and self.PIPEFAIL in self.options:
            raise ValueError("PIPEFAIL is only supported in 'bash'")

    def executable(self):
        return self.shell

    def include_helpers(self) -> bool:
        return self.HELPERS in self.options

    def export_flags(self) -> str:
        flags = []
        if self.ERREXIT in self.options:
            flags.append("-e")
        if self.PIPEFAIL in self.options:
            flags.append("-o pipefail")
        return " ".join(flags)

    def prelude(self) -> str:
        parts = []
        flags = self.export_flags()
        if flags:
            parts.append(f"set {flags}")
        if self.include_helpers():
            parts.append(SHELL_HELPERS)
        return "\n".join(parts)

    def compile_command(self, command: str) -> str:
        pre = self.prelude()
        final = f"{pre}\n{command}" if pre else command
        return final


SHELL_HELPERS = r"""
_para() {
  _scitq_tab=$(echo -e "\t")
  _scitq_nl=$(echo -e "\n")
  _scitq_cmd=$(echo "$*"|sed -e 's/ /🧬/g' -e "s/$_scitq_tab/🦀/g" -e "s/$_scitq_nl/💥/g")
  "$@" &
  _scitq_pid=$!
  _SCITQ_CMDS="${_SCITQ_CMDS} ${_scitq_cmd}🔥$_scitq_pid"
}

_wait() {
  _scitq_tmp_cmds=$_SCITQ_CMDS
  _scitq_running_cmds=""
  unset _SCITQ_CMDS
  for _scitq_cmdpid in $(echo $_scitq_tmp_cmds); do
    _scitq_pid=$(echo $_scitq_cmdpid|sed 's/.*🔥//')
    if kill -0 $_scitq_pid 2>/dev/null; then
      _scitq_running_cmds="$_scitq_running_cmds $_scitq_cmdpid"
    else
      wait $_scitq_pid
      _scitq_code=$?
      if [ "$_scitq_code" -ne 0 ]; then
        _scitq_cmd=$(echo $_scitq_cmdpid|sed -e 's/🔥.*//' -e "s/💥/$_scitq_nl/g" -e "s/🦀/$_scitq_tab/g" -e 's/🧬/ /g')
        echo "Command failed (PID $_scitq_pid): $_scitq_cmd" >&2
        return "$_scitq_code"
      fi
    fi
  done
  for _scitq_cmdpid in $(echo $_scitq_running_cmds); do
    _scitq_pid=$(echo $_scitq_cmdpid|sed 's/.*🔥//')
    wait $_scitq_pid
    _scitq_code=$?
    if [ "$_scitq_code" -ne 0 ]; then
      _scitq_cmd=$(echo $_scitq_cmdpid|sed -e 's/🔥.*//' -e "s/💥/$_scitq_nl/g" -e "s/🦀/$_scitq_tab/g" -e 's/🧬/ /g')
      echo "Command failed (PID $_scitq_pid): $_scitq_cmd" >&2
      return "$_scitq_code"
    fi
  done
  return 0
}

_retry() {
  _max="$1"
  _delay="$2"
  case "$_max" in
    ''|*[!0-9]*) _max=5; _delay=1 ;;
    *)
      case "$_delay" in
        ''|*[!0-9]*) _delay=1; shift 1 ;;
        *) shift 2 ;;
      esac
      ;;
  esac
  _n=0
  until "$@"; do
    _n=$(( _n + 1 ))
    if [ "$_n" -ge "$_max" ]; then
      echo "❌ Retry failed after $_n attempts: $*" >&2
      return 1
    fi
    sleep "$_delay"
  done
}
""".strip()
