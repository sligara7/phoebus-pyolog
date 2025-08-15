"""Nox sessions for phoebus-pyolog development."""

import nox

nox.options.sessions = ["lint", "tests"]


@nox.session
def lint(session: nox.Session) -> None:
    """Run linting tools."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")


@nox.session(python=["3.9", "3.10", "3.11", "3.12", "3.13"])
def tests(session: nox.Session) -> None:
    """Run the test suite."""
    session.install("-e", ".[test]")
    session.run(
        "pytest",
        *session.posargs,
        env={"COVERAGE_FILE": f".coverage.{session.python}"},
    )


@nox.session
def coverage(session: nox.Session) -> None:
    """Combine coverage data and create report."""
    session.install("coverage[toml]")
    session.run("coverage", "combine")
    session.run("coverage", "report")


@nox.session
def docs(session: nox.Session) -> None:
    """Build the documentation."""
    session.install("-e", ".[docs]")
    session.cd("docs")
    session.run("sphinx-build", "-b", "html", ".", "_build/html")


@nox.session
def build(session: nox.Session) -> None:
    """Build the package."""
    session.install("build")
    session.run("python", "-m", "build")
