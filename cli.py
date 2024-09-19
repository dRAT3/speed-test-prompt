from typing import Optional, Annotated
import os

import asyncio
import typer

from tests.testrunner import BenchRunner

app = typer.Typer()

ascii_art = """\
O       O
O      OOO
O O    O O O
 O O O    O
     /        \\_____/free/prompt/log/god\\__/ng\\  11O1100001    OOO   O
    /      \\    |        \\  O   OOO   OOO```

"""

@app.command()
def run(
        runs: Annotated[int, typer.Option("--runs", "-r", help="Number of runs.")] = 1
    ):
    print(ascii_art)    
    print(11*"*")
    if runs:
        print("Amount of runs: {runs}")
    
@app.command()
def bench(
        runs: Annotated[int, typer.Option("--runs", "-r", help="Number of runs.")] = 1,
        file:  Annotated[str, typer.Option("--file", "-f", help="File to scan for tests")] = "-1",
        rpm: Annotated[int, typer.Option("--rpm", "-i", help="Rate Limit per Minute, set to -1 for max speed")] = 30

    ):
    print(ascii_art)    
    print(11*"*")

    if runs:
        print(f"Amount of runs: {runs}")


    if file and not file == "-1":
        suts = BenchRunner.scan_file(file)
    if file and file == "-1":
        suts = os.path.realpath(__file__) + "/tests/tests.py" 

    suts = ['_bench_check_malicious', '_bench_score_malicious']

    runner = BenchRunner(suts, rpm, runs)


    asyncio.run(runner.arun_tests())

if __name__ == "__main__":
    app()
