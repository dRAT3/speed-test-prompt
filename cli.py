from typing import Optional, Annotated
import os

import asyncio
import typer

from bencher.benchrunner import BenchRunner
from utils import bucket_instance, 

app = typer.Typer()

from termcolor import colored

ascii_art = """
     O       O
     O      OOO
   O O    O O O
    O O O    O

       /        \\________
      /            \\     \\______/free/prompt/log/god\\__   
     /              \\        |              |    /ng\\
   1101100001     OOO       OOO      OOO
"""

# Define colored sections
colored_art = (
    colored("     O       O", 'cyan') + "\n" +
    colored("     O      OOO", 'cyan') + "\n" +
    colored("   O O    O O O", 'yellow') + "\n" +
    colored("    O O O    O", 'yellow') + "\n\n" +
    colored("       /        \\________", 'green') + "\n" +
    colored("      /            \\     \\______/free/prompt/log/god\\__", 'magenta') + "\n" +
    colored("     /              \\        |              |    /ng\\", 'magenta') + "\n" +
    colored("   1101100001     OOO       OOO      OOO", 'red')
)

colored_art_2 = (
    colored("     O       O", 'cyan') + "\n" +
    colored("    O O     O O", 'cyan') + "\n" +
    colored("   O O O   O O O", 'yellow') + "\n" +
    colored("   O   O   O   O", 'yellow') + "\n" +
    colored("      O     O", 'yellow') + "\n" +
    colored("        / \\        \\________", 'green') + "\n" +
    colored("       /   \\        \\     \\______/free/prompt/log/god\\__", 'magenta') + "\n" +
    colored("      /     \\        \\        |              |    /ng\\", 'magenta') + "\n" +
    colored("  1101100001    OOO     OOO      OOO", 'red') + "\n" +
    colored("       //\\\\", 'yellow') + "\n" +
    colored("      //  \\\\", 'yellow')
)


@app.command()
def run(
        runs: Annotated[int, typer.Option("--runs", "-r", help="Number of runs.")] = 1
    ):
    # Print the colored ASCII art
    print(colored_art)
    print(colored_art_2)

    print(11*"*")
    if runs:
        print("Amount of runs: {runs}")
    
@app.command()
def bench(
        runs: Annotated[int, typer.Option("--runs", "-r", help="Number of runs.")] = 1,
        file:  Annotated[str, typer.Option("--file", "-f", help="File to scan for tests")] = "-1",
        rpm: Annotated[int, typer.Option("--rpm", "-i", help="Rate Limit per Minute, set to -1 for max speed")] = 30

    ):
    print(colored_art)    
    print(colored_art_2)
    print(11*"*")

    if runs:
        print(f"Amount of runs: {runs}")


    if file and not file == "-1":
        suts = BenchRunner.scan_file(file)
    if file and file == "-1":
        suts = os.path.realpath(__file__) + "/tests/tests.py" 

    #suts = ['_bench_check_malicious', '_bench_score_malicious']
    suts = ['_test_tiktimer_rate_limit_30_rpm']

    runner = BenchRunner(suts, rpm, runs)


    asyncio.run(runner.arun_tests())

if __name__ == "__main__":
    app()
