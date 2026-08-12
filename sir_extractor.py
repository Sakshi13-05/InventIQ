import os
import json

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def extract_sir(invention_text):

    system_prompt = """
You are the SIR decomposition engine for an intellectual
property analysis system called InventIQ.

Your task is to analyze an inventor's natural-language
description and decompose the invention into three
functional components:

SUBJECT:
The main technological entity, device, mechanism,
component, or system involved.

ACTION:
The primary function or operation performed by the
subject. Focus on what the invention actually does.

BOUNDARY:
The application domain, environment, use case,
operating condition, or context in which the action
takes place.

IMPORTANT RULES:

1. Understand the meaning of the invention rather than
   simply copying words.

2. Do not treat grammatical words such as "that",
   "which", "it", etc. as the subject.

3. The Subject should describe the actual technological
   concept.

4. The Action should describe the core functionality.

5. The Boundary should describe where, why, or in what
   context the invention is used.

6. Keep each component concise but meaningful.

7. Return ONLY valid JSON.

Return exactly this structure:

{
    "subject": "...",
    "action": "...",
    "boundary": "..."
}

Example:

Input:
"A device for farmers that uses ultrasonic waves to keep
bugs away from stored rice."

Output:
{
    "subject": "high-frequency acoustic pest deterrent",
    "action": "repelling insects using ultrasonic sound",
    "boundary": "agricultural grain storage"
}

Example:

Input:
"A wrist-watch that never needs a battery because it
runs on sunlight."

Output:
{
    "subject": "photovoltaic-powered wearable timepiece",
    "action": "converting solar energy into usable power",
    "boundary": "personal wearable timekeeping"
}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": invention_text
            }
        ],
        temperature=0,
        response_format={
            "type": "json_object"
        }
    )

    content = response.choices[0].message.content

    return json.loads(content)