import subprocess
import typer
import sys

from subprocess import CompletedProcess


app = typer.Typer()


def _stop_on_failure(process: CompletedProcess):
    if process.returncode != 0:
        print(f"[{' '.join(process.args)}] Process returned non zero return code")
        print(f"[{' '.join(process.args)}] Captured output:\n\n")
        print(process.stdout)
        sys,exit(1)


def _run(cmd: str, /, *args: str, capture_std=True):
    if capture_std:
        _stop_on_failure(subprocess.run([cmd, *args], capture_output=True, text=True))
    else:
        subprocess.run([cmd, *args], capture_output=capture_std)


@app.command()
def check(*, black: bool = True, flake: bool = True, mypy: bool = True, strict: bool = True):
    if strict:
        black = flake = mypy = True
    _check(black, flake, mypy)


def _check(black: bool, flake: bool, mypy: bool):
    if black:
        _run("black", "src")
    if flake:
        _run("flake8", "src")
    if mypy:
        _run("mypy", "src")


@app.command()
def build(*, black: bool = True, flake: bool = True, mypy: bool = False):
    _check(black, flake, mypy)
    _run("poetry", "build", capture_std=False)


@app.command()
def update():
    _run("poetry", "update", capture_std=False)


def main():
    app()


if __name__ == "__main__":
    main
