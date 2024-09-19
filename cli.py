from typing import Optional, Annotated
import os

import asyncio
import typer
import yaml

from bencher.benchrunner import BenchRunner

app = typer.Typer()

@app.command()
def bench(
        file:  Optional[Annotated[str, typer.Option("--file", "-f", help="File to scan for tests")]] = None,
        runs: Annotated[int, typer.Option("--runs", "-r", help="Number of runs.")] = 1,
        rpm: Annotated[int, typer.Option("--rpm", "-i", help="Rate Limit per Minute")] = 30,

    ):
    print(33*"*")
    print(f"Amount of runs: {runs}")

    if file:
        suts = BenchRunner.scan_file(file)

    suts = ['_bench_check_malicious', '_bench_score_malicious' ]

    runner = BenchRunner(suts, rpm, runs)


    asyncio.run(runner.arun_tests())

if __name__ == "__main__":
    app()
