import subprocess
from typing import IO, List, cast


def call(command: str, *args) -> str:
    """
    call command with arguments and return stdout or raise exception
    """

    p = subprocess.Popen(
        args=[command] + [a for a in args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    p.wait()

    def read(stream: IO[bytes]) -> str:
        def read_one():
            data = stream.readline()
            if not data:
                return ""
            return data.decode("utf-8")

        return "".join([line for line in iter(read_one, "")])

    out: str
    err: str

    if p.stdout:
        out = read(p.stdout)
        p.stdout.close()

    if p.stderr:
        err = read(p.stderr)
        p.stderr.close()

    if p.returncode != 0:
        if err:
            raise Exception(err)
        else:
            cmd = " ".join(cast(List[str], p.args))
            raise Exception(f"'{cmd}'\n failed with exit code: {p.returncode}")

    return out
