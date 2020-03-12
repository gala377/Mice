import subprocess
import typer

from subprocess import CompletedProcess


app = typer.Typer()


def _stop_on_failure(process: CompletedProcess):
    if process.returncode != 0:
        print("Process returned non zero return code")
        print("Captured output:\n\n")
        print(process.stdout)
        raise RuntimeError("Build returned some errors")


def _run(cmd: str, /, *args: str, capture_std=True):
    if capture_std:
        _stop_on_failure(subprocess.run([cmd, *args], capture_output=True, text=True))
    else:
        subprocess.run([cmd, *args], capture_output=capture_std)


@app.command()
def check():
    _check()


def _check():
    _run("black", "src")
    _run("flake8", "src")
    _run("mypy", "src")


@app.command()
def build():
    _check()
    _run("poetry", "build", capture_std=False)


@app.command()
def update():
    _run("poetry", "update", capture_std=False)


def main():
    app()


if __name__ == "__main__":
    main
