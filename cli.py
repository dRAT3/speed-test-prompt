from typing import Optional, Annotated
import os
from utils.ascii_art import animate_art, print_art
from colorama import init

import asyncio
import typer
import time
import yaml
import threading

from bencher.benchrunner import BenchRunner

app = typer.Typer()

init(autoreset=True)
stop_animation = False  # Global flag to stop the animation
logs = []  # List to store log messages


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

@app.command()
def run(
        runs: Annotated[int, typer.Option("--runs", "-r", help="Number of runs.")] = 1
    ):
    # Print the colored ASCII art
    print(11*"*")
    if runs:
        print("Amount of runs: {runs}")
    
@app.command()
def bench(
        runs: Annotated[int, typer.Option("--runs", "-r", help="Number of runs.")] = 1,
        file:  Annotated[str, typer.Option("--file", "-f", help="File to scan for tests")] = "-1",
        rpm: Annotated[int, typer.Option("--rlmb", "-i", help="Rate Limit per Minute, set to -1 for max speed")] = 30

    ):
    print(11*"*")

    if runs:
        print(f"Amount of runs: {runs}")


    if file and not file == "-1":
        suts = BenchRunner.scan_file(file)
    if file and file == "-1":
        suts = os.path.realpath(__file__) + "/tests/tests.py" 

    suts = ['_bench_check_malicious', '_bench_score_malicious', '_test_bucket_rate_limit_30']
    #suts = ['_test_tiktimer_rate_limit_30_rpm']

    runner = BenchRunner(suts, rpm, runs)


    asyncio.run(runner.arun_tests())

@app.command()
def run_loading_animation(speed: float = 0.1):
    """
    Runs the loading animation and prints logs simultaneously.

    Parameters:
    speed: The delay between frames (in seconds).
    """
    global stop_animation
    stop_animation = False
    
    # Initial clear screen
    clear_screen()

    # Print the first frame of animation
    print_art(0, True)
    
    # Start the animation in a separate thread
    animation_thread = threading.Thread(target=animate_art, args=(True, speed))
    animation_thread.start()

    # Simulate log printing while the animation runs
    global logs
    for i in range(10):  # Simulating 10 log entries
        time.sleep(1)  # Delay to simulate work being done
        log_message = f"Log message {i+1}: Something is processing..."
        logs.append(log_message)
        print_logs()  # Print logs below the animation

    # Stop the animation after logs are printed
    stop_animation = True
    animation_thread.join()  # Wait for the animation thread to finish

    # Final message
    print("Loading complete. All processes finished!")

def print_logs():
    """Prints all accumulated logs without clearing them."""
    global logs
    print("\n".join(logs))  # Print all logs

if __name__ == "__main__":
    app()
