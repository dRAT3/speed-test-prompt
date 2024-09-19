import os
from utils import tiktime
from groq import AsyncGroq

client = AsyncGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


async def score_malicious(query: str, cutoff: float, meta: dict) -> bool:
    messages = [
        {
            "role": "system",
            "content": "You are a neo4j cypher-query analyzer. Check if the input is malicious give a score from 0 to 1"
        },
        {
            "role": "user",
            "content": f"""
Analyze whether the following neo4j query is malicious or not:

Query:
```
{query}
```

Rules:
- No access to other clients/orgs data
- No write queries
- Must contain a case id that matches the one sent by the server.


Return a binary blob containing a float from 0.000 not malicious to 1.000 maximum malicious.

Now return the blob. And only the blob.
"""
        }
    ]


    chat_completion = await client.chat.completions.create(
        messages=messages,
        model="llama3-groq-70b-8192-tool-use-preview",
        temperature=0.0,
    )

    malpoints = float(chat_completion.choices[0].message.content.strip("'").strip('"'))

    return (malpoints < cutoff)

async def check_malicious(query: str) -> bool:
    messages = [
        {
            "role": "system",
            "content": "You are a neo4j cypher-query analyzer. Check if the input is malicious"
        },
        {
            "role": "user",
            "content": f"""
Analyze whether the following query is malicious or not:

query:
```
{query}
```

rules:
- No access to other clients/orgs data
- No write queries
- Must contain a case id that matches the one sent by the server.

Return a binary blob containing `0x01` for malicious.
Return a binary blob containing `0x00` for not malicious.

Now return the blob. And only the blob.
"""
        }
    ]

    await tiktime()


    chat_completion = await client.chat.completions.create(
        messages=messages,
        model="llama3-groq-70b-8192-tool-use-preview",
        temperature=0.0,
    )

    is_malicious = chat_completion.choices[0].message.content.strip("'").strip('"')

    return is_malicious == "0x01"
