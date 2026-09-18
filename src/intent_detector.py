
import json
from src.ollama_client import generate_ollama_response



def detect_intent(question):

    prompt = f"""
You are an intent detection system for a Text-to-SQL application.

Determine what the user wants to do.

Possible intents:

READ
CREATE_TABLE
INSERT
UPDATE
DELETE

Definitions:

READ:
The user wants to retrieve, search, count, filter, sort,
or analyze existing data.

CREATE_TABLE:
The user wants to create a new database table.

INSERT:
The user wants to add new records/data into an existing table.

UPDATE:
The user wants to modify existing records/data in an existing table.


DELETE:
The user wants to remove existing records/data from an existing table.

Examples:

User:
Show me all customers
Intent:
READ

User:
How many products are there?
Intent:
READ

User:
Which customer spent the most?
Intent:
READ

User:
Show me employees from Engineering
Intent:
READ

User:
Create a table called employees
Intent:
CREATE_TABLE

User:
Create an employees table with id, name and salary
Intent:
CREATE_TABLE

User:
Add Rahul to employees with employee_id 1 and salary 75000
Intent:
INSERT

User:
Insert a new employee named Priya into employees
Intent:
INSERT

User:
Add a product called Laptop with price 60000
Intent:
INSERT

User:
Update Rahul's salary to 80000
Intent:
UPDATE

User:
Change employee 1 department to HR
Intent:
UPDATE

User:
Update the price of the Laptop to 65000
Intent:
UPDATE

User:
Delete employee 1
Intent:
DELETE

User:
Remove Rahul from employees
Intent:
DELETE

User:
Delete all products in the Electronics category
Intent:
DELETE

User:
Change Mumbai customers' city to Pune
Intent:
UPDATE

Important distinction:

INSERT means adding a NEW record.

UPDATE means modifying an EXISTING record.

For example:

"Add Rahul to employees"
=> INSERT

"Change Rahul's salary"
=> UPDATE

Return ONLY valid JSON in this exact format:

{{
    "intent": "READ"
}}

or:

{{
    "intent": "CREATE_TABLE"
}}

or:

{{
    "intent": "INSERT"
}}

or:

{{
    "intent": "UPDATE"
}}

or:

{{
    "intent": "DELETE"
}}

User question:
{question}
"""

    result = generate_ollama_response(
        prompt,
    ).strip()

    if result.startswith("```json"):
        result = result[7:]

    if result.startswith("```"):
        result = result[3:]

    if result.endswith("```"):
        result = result[:-3]

    return json.loads(result.strip())