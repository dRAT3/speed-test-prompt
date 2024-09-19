### MIT License, no warranty.
import os
import typer
import time
import uuid


import asyncio
from groq import AsyncGroq
from typing import Optional, Annotated
from utils import tiktime

from security_prompts import score_malicious, check_malicious 
from tests import 

import tracemalloc

app = typer.Typer()

RPS = ""

NEXT_TIME = time.time()  # Shared across all coroutines
TIME_LOCK = asyncio.Lock()       # Lock to protect the shared time variable

client = AsyncGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

@app.command()
def run(
        runs: Annotated[int, typer.Option("--runs", "-r", help="Number of runs.")] = 1
    ):
    print(36*"*oO")
    if runs:
        print("Amount of runs: {runs}")
    
    #asyncio.run()

@app.command()
def test(
        runs: Annotated[int, typer.Option("--runs", "-r", help="Number of runs.")] = 1,
        file:  Annotated[str, typer.Option("--load-py-file", "-f", help="File to scan for tests")] = "-1",

    ):

    if runs:
        print("Amount of runs: {runs}")

    # ToDo
    if file and not file == "-1":
        tests = load_pyfile(file)
    if file and file == "-1":
        tests = os.path.realpath(__file__) + "/tests/tests.py" 

    tests = ['_bench_check_malicious', '_bench_score_malicious']
    

if __name__ == "__main__":
    app()

### Should come up as malicious but not sure
'''
    cyphers = [
        ("""CREATE (s:Student) SET s.name = 'Robby' WITH true as ignored MATCH (s:Student) DETACH DELETE s;""", True),
        ("""CREATE (s:Student) SET s.name = '' MATCH (all) DETACH DELETE all;""", True),
        ("""MATCH (s:Student) WHERE s.name = 'Robby' OR 1=1 RETURN apoc.text.join(collect(s.name), ',')""", True),
        ("""'bobby@mail.com' RETURN user.username STARTS WITH 'a';""", True),
        ("""MATCH (s:School)-[:IN]->(c: City { name: $cityName }) RETURN s;""", True),
        ("""**""", False)
    ]
'''
