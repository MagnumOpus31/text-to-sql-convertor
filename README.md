**# Natural Language to SQL Converter**

A full-stack **Text-to-SQL application** that converts natural language questions into SQL queries using an LLM, validates the generated SQL, detects ambiguity, and executes the query against a SQLite database.

The application supports **local development using Ollama and Qwen 2.5 3B** and **public deployment using the Groq API with Qwen**.

**## Live Demo**

The application is deployed on Render:

https://english-to-sql-converter.onrender.com/

**## Features**

* **Natural Language → SQL** — Converts user questions into SQL queries.

* **Clarification Engine** — Detects ambiguous questions and asks the user for clarification before generating SQL.

* **Local Typo Correction** — Corrects common spelling mistakes before processing the question.

* **Intent Detection** — Identifies the requested operation:

  * `READ`

  * `CREATE_TABLE`

  * `INSERT`

  * `UPDATE`

  * `DELETE`

* **Dynamic Schema Detection** — Retrieves the current database schema instead of relying only on a hardcoded schema.

* **SQL Validation** — Checks whether generated SQL follows the expected syntax and operation rules.

* **Semantic Validation** — Checks whether the generated query is compatible with the available database schema.

* **SQL Correction** — Attempts to correct invalid generated SQL before execution.

* **Complex SQL Generation** — Supports multi-table queries using `JOIN`, `GROUP BY`, `ORDER BY`, `LIMIT`, and aggregate functions such as `SUM`, `COUNT`, `AVG`, `MAX`, and `MIN`.

* **CRUD Operations** — Supports reading, inserting, updating, and deleting database records.

* **Schema Creation** — Can generate and execute `CREATE TABLE` statements.

* **Operation Safety** — Protects against dangerous `UPDATE` and `DELETE` operations.

* **Confirmation System** — Requires confirmation before executing database-changing operations.

* **Evaluation Framework** — Includes test cases for evaluating SQL generation and the clarification engine.

* **Automated Tests** — Individual components have dedicated test files.

* **FastAPI Backend** — Provides an API layer between the frontend and the Text-to-SQL processing pipeline.

* **Streamlit Frontend** — Provides a simple web interface for interacting with the application.

* **Docker Support** — Includes Docker and Docker Compose configuration for local development.

* **Cloud Deployment** — The application is deployed using Docker on Render.

**## System Workflow**

```text
User Question

      ↓

Streamlit Frontend

      ↓

FastAPI Backend

      ↓

Local Typo Correction

      ↓

Clarification / Ambiguity Detection

      ↓

Resolved Question

      ↓

Intent Detection

      ↓

┌─────────────────────────────────────┐
│ READ                                │
│ CREATE TABLE                        │
│ INSERT                              │
│ UPDATE                              │
│ DELETE                              │
└─────────────────────────────────────┘

      ↓

Schema Detection

      ↓

SQL Generation

      ↓

SQL Validation

      ↓

Semantic Validation

      ↓

Safety Check

      ↓

User Confirmation (write operations)

      ↓

Database Execution

      ↓

Result

## Example

### Simple Query

User:

Show me all customers from Mumbai

Generated SQL:

SELECT *
FROM customers
WHERE city = 'Mumbai';

### Ambiguous Query

User:

Show me the top customers

The clarification engine identifies the ambiguity and asks:

What metric should be used to rank the top customers?

If the user answers:

Total spending

The question is resolved to:

Show me the top customers ranked by total spending.

The system can then generate the appropriate SQL query.

### JOIN Query

User:

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

### Complex Aggregation Query

User:

Show me the top 3 customers by total spending

Generated SQL:

SELECT
    c.name,
    SUM(o.total_amount) AS total_spending
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spending DESC
LIMIT 3;

This query demonstrates:

JOIN
SUM
GROUP BY
ORDER BY
LIMIT

### INSERT

User:

Add a customer named Amit from Mumbai

The system generates an INSERT statement and asks for confirmation before execution.

### UPDATE

User:

Update Rahul's city to Pune

The system generates an UPDATE statement and checks that it contains a sufficiently specific WHERE clause before execution.

### DELETE

User:

Delete the customer with customer ID 1

The system generates:

DELETE FROM customers
WHERE customer_id = 1;

The operation is checked for safety and requires confirmation.

## Safety Mechanisms

Database-changing operations are treated differently from read-only queries.

The system blocks or warns about potentially dangerous operations such as:

DELETE FROM customers;

and:

UPDATE customers
SET city = 'Mumbai';

It also detects conditions such as:

WHERE 1=1

and potentially broad modification conditions.

This helps prevent accidental modification or deletion of large portions of the database.

## Database Schema

The demonstration SQLite database contains the following tables:

### customers

customer_id
name
city

### orders

order_id
customer_id
order_date
total_amount

### products

product_id
product_name
category
price

### order_items

order_id
product_id
quantity
unit_price

The relationships allow the system to generate multi-table queries such as:

customers → orders → order_items → products

## Project Structure

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
│   └── component test files
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

Note: The project contains dedicated test files for individual components. The current repository structure may evolve as the project is further cleaned up.

## Technologies Used

Python
FastAPI
Streamlit
SQLite
Qwen 2.5 3B
Ollama
Groq API
Pydantic
Requests
Docker
Docker Compose
Render

## LLM Providers

### Local Development

The local development setup uses:

Ollama
    ↓
Qwen 2.5 3B

This allows the application to run locally without requiring an external LLM API key.

### Deployment

The deployed application uses:

Groq API
    ↓
Qwen

The LLM provider and model are configurable through environment variables.

## Engineering Decisions

Major architecture and technology decisions are documented in:

decision.md

The document contains the reasoning and trade-offs behind the project's design choices.

## Installation

Clone the repository:

git clone <your-repository-url>

cd english-to-sql-converter

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install the dependencies:

pip install -r requirements.txt

For local development, Ollama is used to run the Qwen 2.5 3B language model.

Make sure Ollama is installed and running:

ollama serve

Make sure the required model is available:

ollama pull qwen2.5:3b

## Running the Application

The local application consists of a FastAPI backend and a Streamlit frontend.

Start the FastAPI backend:

uvicorn api.main:app --reload

In another terminal, start the Streamlit frontend:

streamlit run app.py

The Streamlit interface can then be opened in the browser.

## Running with Docker

The project also includes Docker configuration for local development.

Build and start the application:

docker compose up --build

The Docker setup runs:

FastAPI Backend
        +
Streamlit Frontend
        +
Ollama running on the host

## Deployment

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

The deployment uses:

Dockerfile.deploy

The application is available at:

https://english-to-sql-converter.onrender.com/

The deployed application uses environment variables such as:

LLM_PROVIDER
GROQ_MODEL
GROQ_API_KEY
API_URL

API credentials are stored as environment variables and are not committed to the repository.

## Running Tests

Individual component tests can be run with:

python test_clarification.py

python test_intent_detector.py

python test_local_typo_corrector.py

python test_operation_safety.py

Additional tests are available for:

SQL generation
SQL validation
Semantic validation
Schema handling
INSERT operations
UPDATE operations
DELETE operations
Clarification
Operation safety

## Evaluation

The project includes an evaluation framework for comparing SQL generation with and without the clarification engine.

Example evaluation categories include:

Basic database queries
Location-based filtering
Aggregation
Ambiguous questions
Clarification and question resolution
SQL generation

The evaluation framework helps identify cases where clarification improves the interpretation of natural language queries.

## Security

API credentials are stored using environment variables and are not included in the repository.

Sensitive files and local database files are excluded through .gitignore:

.env
data/*.db
__pycache__/
*.pyc
venv/

## Future Improvements

Possible future improvements include:

Supporting additional SQL dialects
Improving natural-language clarification
Adding more comprehensive evaluation datasets
Improving query-generation accuracy
Supporting additional database systems
Supporting more complex database relationships
Adding more advanced query verification

## Author

Jinay Shah

B.Tech Electronics and Telecommunication Engineering

Interested in Data Science, Machine Learning, Artificial Intelligence, and Software Engineering.