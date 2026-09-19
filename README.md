# Natural Language to SQL Converter

A full-stack Text-to-SQL application that converts natural language questions into SQL queries using an LLM, validates the generated SQL, detects ambiguity, and executes the query against a SQLite database.

The project supports both local development with Ollama/Qwen and public deployment using the Groq API.

## Live Demo

The application is deployed on Render:

https://english-to-sql-converter.onrender.com/

## Overview

The goal of this project is to allow users to interact with a relational database using natural language instead of manually writing SQL.

For example:

```text
Show me the top 3 customers by total spending

can be converted into:

SELECT
    c.name,
    SUM(o.total_amount) AS total_spending
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spending DESC
LIMIT 3;

The system then validates and executes the generated SQL and displays the results.

Key Features
Natural Language → SQL

Converts natural language questions into SQL queries.

Ambiguity Detection and Clarification

Detects questions where the user's intended meaning is unclear.

For example:

Show me the top customers

The system asks for clarification instead of making an arbitrary assumption:

What metric should be used to rank the top customers?

The user can then specify:

Total spending

and the system can generate the appropriate SQL query.

Local Typo Correction

Corrects common spelling mistakes before processing the question.

Intent Detection

Identifies the requested database operation:

READ
CREATE_TABLE
INSERT
UPDATE
DELETE
Dynamic Schema Detection

Retrieves the current database schema so that SQL generation can be based on the available tables and columns.

SQL Validation

Validates generated SQL against the expected operation and SQL rules.

Semantic Validation

Checks whether the generated SQL is compatible with the available database schema and expected query structure.

SQL Correction

Attempts to correct invalid generated SQL before execution.

Complex SQL Generation

The system can generate queries involving:

JOIN
Multiple-table relationships
GROUP BY
ORDER BY
LIMIT
Aggregations such as SUM, COUNT, AVG, MAX, and MIN
Filtering with WHERE
Multi-step relational queries

Example:

Show me the top 3 customers by total spending

can result in a query using:

JOIN + SUM + GROUP BY + ORDER BY + LIMIT
CRUD Operations

Supports:

Reading data
Creating tables
Inserting records
Updating records
Deleting records
Operation Safety

Database-changing operations are checked before execution.

The system is designed to prevent dangerous operations such as unrestricted:

DELETE FROM customers;

or:

UPDATE customers
SET city = 'Mumbai';
Confirmation System

Database-changing operations require confirmation before execution.

Evaluation Framework

The project contains an evaluation framework for testing SQL generation and comparing behavior with and without clarification.

Automated Tests

Individual components have dedicated test files for functionality such as clarification, intent detection, typo correction, validation, and operation safety.

System Architecture
                         User
                           |
                           v
                 Streamlit Frontend
                           |
                           v
                    FastAPI Backend
                           |
                           v
                  Local Typo Correction
                           |
                           v
               Clarification / Ambiguity
                           |
                           v
                    Intent Detection
                           |
                           v
                   Schema Detection
                           |
                           v
                    SQL Generation
                           |
                           v
                   SQL Validation
                           |
                           v
                Semantic Validation
                           |
                           v
                    Safety Checks
                           |
                           v
              User Confirmation
               (write operations)
                           |
                           v
                  SQLite Database
                           |
                           v
                       Results
Example Queries
1. Simple Query
User
Show me all customers from Mumbai
Generated SQL
SELECT *
FROM customers
WHERE city = 'Mumbai';
2. Ambiguous Query
User
Show me the top customers

The system detects that "top" is ambiguous and asks:

What metric should be used to rank the top customers?

The user can respond:

Total spending

The system can then generate an appropriate aggregation query.

3. JOIN Query
User
Show me the names of customers who bought laptops

The system can identify the relationship between:

customers
    ↓
orders
    ↓
order_items
    ↓
products

and generate a multi-table JOIN query.

4. Complex Aggregation Query
User
Show me the top 3 customers by total spending
Generated SQL
SELECT
    c.name,
    SUM(o.total_amount) AS total_spending
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spending DESC
LIMIT 3;

This demonstrates:

JOIN
SUM
GROUP BY
ORDER BY
LIMIT
5. INSERT

Example:

Add a customer named Amit from Mumbai

The system can generate an INSERT statement and request confirmation before execution.

6. UPDATE

Example:

Update Rahul's city to Pune

The generated UPDATE statement is checked for a sufficiently specific condition before execution.

7. DELETE

Example:

Delete the customer with customer ID 1

The system generates a targeted DELETE statement and requires confirmation before execution.

Safety Mechanisms

Read-only queries and database-changing operations are handled differently.

Potentially dangerous queries such as:

DELETE FROM customers;

or:

UPDATE customers
SET city = 'Mumbai';

are checked before execution.

The system also checks for potentially unsafe conditions such as:

WHERE 1=1

and unrestricted or overly broad modification operations.

This reduces the risk of accidental large-scale database modifications.

Database Schema

The demonstration SQLite database contains the following tables.

customers
customer_id
name
city
orders
order_id
customer_id
order_date
total_amount
products
product_id
product_name
category
price
order_items
order_id
product_id
quantity
unit_price

The relationships allow the system to generate multi-table queries such as:

customers → orders → order_items → products
Project Structure
english-to-sql-converter/
│
├── api/
│   └── main.py
│
├── src/
│   ├── clarification.py
│   ├── database.py
│   ├── delete_generator.py
│   ├── delete_validator.py
│   ├── insert_generator.py
│   ├── insert_validator.py
│   ├── intent_detector.py
│   ├── local_typo_corrector.py
│   ├── operation_safety.py
│   ├── schema.py
│   ├── schema_generator.py
│   ├── schema_validator.py
│   ├── sql_corrector.py
│   ├── sql_generator.py
│   ├── sql_semantic_validator.py
│   ├── sql_validator.py
│   ├── update_generator.py
│   └── update_validator.py
│
├── evaluation/
│   ├── evaluate.py
│   ├── evaluate_with_clarification.py
│   ├── test_cases.py
│   ├── results.json
│   ├── clarification_results.json
│   └── with_clarification.json
│
├── tests/
│
├── data/
│   └── database.db
│
├── app.py
├── requirements.txt
├── Dockerfile
├── Dockerfile.deploy
├── docker-compose.yml
├── start.sh
├── .dockerignore
├── .gitignore
└── README.md
Technologies Used
Python
FastAPI
Streamlit
SQLite
Pydantic
Requests
Docker
Docker Compose
Ollama
Qwen
Groq API
Render
LLM Providers
Local Development

The application can use:

Ollama
    ↓
Qwen 2.5 3B

This allows local development without requiring an external LLM API.

Deployment

The deployed version uses:

Groq API
    ↓
Qwen model

The provider and model are configurable through environment variables.

Local Installation

Clone the repository:

git clone <your-repository-url>

cd english-to-sql-converter

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt
Running Locally

For local development with Ollama, install Ollama and make sure the required model is available.

Start Ollama:

ollama serve

The application can then be started using the local configuration.

The Streamlit frontend communicates with the FastAPI backend.

Running with Docker

The project includes Docker configuration for running the application locally.

Build and start the containers:

docker compose up --build

The services include:

FastAPI Backend
        +
Streamlit Frontend
        +
Ollama running on the host
Deployment

The application is deployed using:

GitHub
   ↓
Render
   ↓
Docker
   ↓
FastAPI + Streamlit
   ↓
Groq API

The deployment uses a separate deployment Dockerfile:

Dockerfile.deploy

The deployed application is available at:

https://english-to-sql-converter.onrender.com/

Environment variables are used for deployment configuration and API credentials.

Testing

Individual component tests can be executed using commands such as:

python test_clarification.py
python test_intent_detector.py
python test_local_typo_corrector.py
python test_operation_safety.py

Additional tests are available for:

SQL generation
SQL validation
Semantic validation
Schema handling
INSERT
UPDATE
DELETE
Clarification
Operation safety
Evaluation

The project includes an evaluation framework for comparing SQL generation with and without the clarification engine.

Evaluation categories include:

Basic database queries
Location-based filtering
Aggregation
Ambiguous questions
Clarification
Question resolution
SQL generation

The evaluation framework helps identify cases where clarification improves the interpretation of natural language queries.

Engineering Decisions

Major architecture and technology decisions are documented in:

decision.md

The document contains the reasoning and trade-offs behind the project's design choices.

Security and Configuration

API credentials are stored using environment variables and are not included in the repository.

For example:

GROQ_API_KEY
LLM_PROVIDER
GROQ_MODEL
API_URL

Sensitive local files are excluded through .gitignore.

Example:

.env
data/*.db
__pycache__/
*.pyc
venv/
Future Improvements

Possible future improvements include:

Supporting additional SQL dialects
Improving natural-language clarification
Expanding evaluation datasets
Improving SQL generation accuracy
Supporting additional database systems
Improving handling of complex database relationships
Adding more advanced query verification
Author

Jinay Shah

B.Tech Electronics and Telecommunication Engineering

Interested in Data Science, Machine Learning, Artificial Intelligence, and Software Engineering.