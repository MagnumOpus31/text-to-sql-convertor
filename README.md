# Natural Language to SQL Converter

A Python-based Text-to-SQL system that converts natural language questions into SQL queries using a local Qwen 2.5 3B model through Ollama.

## Features

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
* **Semantic Validation** — Checks whether the generated query makes sense for the available database schema.
* **SQL Correction** — Attempts to correct invalid generated SQL.
* **CRUD Operations** — Supports reading, inserting, updating, and deleting database records.
* **Schema Creation** — Can generate and execute `CREATE TABLE` statements.
* **Operation Safety** — Protects against dangerous `UPDATE` and `DELETE` operations.
* **Confirmation System** — Requires confirmation before executing database-changing operations.
* **Evaluation Framework** — Includes test cases for evaluating SQL generation and the clarification engine.
* **Automated Tests** — Individual components have dedicated test files.

## System Workflow

```text
User Question
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
```

## Example

### Simple Query

**User:**

```text
Show me all customers from Mumbai
```

**Generated SQL:**

```sql
SELECT * FROM customers
WHERE city = 'Mumbai';
```

### Ambiguous Query

**User:**

```text
Show me the top customers
```

The clarification engine identifies the ambiguity and asks:

```text
Would you like to rank the customers by total spending or number of orders?
```

If the user answers:

```text
Total spending
```

The question is resolved to:

```text
Show me the top customers ranked by total spending.
```

The system can then generate the appropriate SQL query.

### INSERT

**User:**

```text
Add an employee named Amit to Sales with a salary of 55000
```

**Generated SQL:**

```sql
INSERT INTO employees (employee_id, name, department, salary)
VALUES (3, 'Amit', 'Sales', 55000);
```

The system asks for confirmation before execution.

### UPDATE

**User:**

```text
Increase Rahul's salary to 80000
```

The system generates an `UPDATE` statement and checks that it contains a sufficiently specific `WHERE` clause before execution.

### DELETE

**User:**

```text
Delete the employee with employee ID 1
```

The system generates:

```sql
DELETE FROM employees
WHERE employee_id = 1;
```

The operation is checked for safety and requires confirmation.

## Safety Mechanisms

Database-changing operations are treated differently from read-only queries.

The system blocks or warns about potentially dangerous operations such as:

```sql
DELETE FROM employees;
```

and:

```sql
UPDATE employees
SET salary = 50000;
```

It also detects conditions such as:

```sql
WHERE 1=1
```

and potentially multi-row deletion conditions.

This helps prevent accidental modification or deletion of large portions of the database.

## Database Schema

The demonstration SQLite database contains the following tables:

### customers

```text
customer_id
name
city
```

### orders

```text
order_id
customer_id
order_date
total_amount
```

### products

```text
product_id
product_name
category
price
```

### order_items

```text
order_id
product_id
quantity
unit_price
```

### employees

```text
employee_id
name
department
salary
```

## Project Structure

```text
english-to-sql-converter/
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
│   ├── main.py
│   ├── operation_safety.py
│   ├── schema.py
│   ├── schema_generator.py
│   ├── schema_validator.py
│   ├── sql_corrector.py
│   ├── sql_generator.py
│   ├── sql_semantic_validator.py
│   ├── sql_validator.py
│   ├── typo_corrector.py
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
├── chat.py
├── setup.py
├── .gitignore
└── README.md
```

> Note: Test files are currently located in the project root. They can be moved into a `tests/` directory in a future cleanup.

## Technologies Used

* **Python**
* **SQLite**
* **Qwen 2.5 3B via Ollama**
* **Ollama**
* **Qwen 2.5 3B**
* **Pydantic**
* **python-dotenv**

## Engineering Decisions

Major architecture and technology decisions are documented in
[`decision.md`](decision.md), including the reasoning and trade-offs behind
the project's design choices.

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd english-to-sql-converter
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Ollama is used to run the local Qwen 2.5 3B language model, so no external LLM API key is required.

Make sure Ollama is installed and running:

```bash
ollama serve

## Running the Application

From the project root:

```bash
python chat.py
```

Enter a natural language question when prompted.

## Running Tests

Individual component tests can be run with:

```bash
python test_clarification.py
python test_intent_detector.py
python test_local_typo_corrector.py
python test_operation_safety.py
```

Additional tests are available for SQL generation, validation, schema handling, INSERT, UPDATE, and DELETE operations.

## Evaluation

The project includes an evaluation framework for comparing SQL generation with and without the clarification engine.

Example evaluation categories include:

* Basic database queries
* Location-based filtering
* Aggregation
* Ambiguous questions
* Clarification and question resolution

The project uses a local Qwen 2.5 3B model through Ollama, so LLM requests are not dependent on an external API rate limit.

## Security

No `.env` file or external LLM API key is required. The application communicates with the locally running Ollama server.

Sensitive files and local database files are excluded through `.gitignore`:

```gitignore
.env
data/*.db
__pycache__/
*.pyc
venv/
```

## Future Improvements

Possible future improvements include:

* Supporting additional SQL dialects
* Improving natural-language clarification
* Adding more comprehensive evaluation datasets
* Improving query-generation accuracy
* Adding a graphical user interface
* Supporting more complex database relationships

## Author

**Jinay Shah**

B.Tech Electronics and Telecommunication Engineering

Interested in Data Science, Machine Learning, Artificial Intelligence, and Software Engineering.
