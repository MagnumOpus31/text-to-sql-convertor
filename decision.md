# Engineering Decisions

This document records the major technical and architectural decisions made
during the development of the Text-to-SQL Assistant and the reasoning behind
them.

The goal is to make the system's design choices understandable and
maintainable rather than documenting only the final technology stack.

---

## 1. Use a Local LLM Instead of a Cloud LLM API

### Decision

Use **Qwen 2.5 3B through Ollama** as the local language model.

### Why

The project initially experimented with a cloud-based Gemini API. However,
the free API tier introduced request and quota limitations.

Since the project is intended to be a practical portfolio project, depending
on a paid API or a limited free-tier quota would make development and
demonstration less reliable.

Ollama provides a local inference interface, allowing the application to run
without sending database questions to an external API.

### Benefits

- No API key required during normal operation
- No cloud API request limits
- Works offline after the model is downloaded
- Better privacy for database queries
- Reproducible local development environment
- Demonstrates knowledge of local LLM deployment

### Trade-offs

- Requires local computational resources
- Inference is slower than larger hosted models in many cases
- A 3B model has less reasoning capability than larger models
- Users must install Ollama and download the model

---

## 2. Use Qwen 2.5 3B Instead of a Larger Local Model

### Decision

Use `qwen2.5:3b`.

### Why

The application needs enough language understanding to interpret natural
language database questions, while the development machine has limited RAM.

A larger model could potentially produce better results but would increase
memory usage and inference time.

Qwen 2.5 3B provided a reasonable balance between:

- SQL generation quality
- Natural-language understanding
- Memory usage
- Local inference speed

### Trade-offs

A smaller model can occasionally generate incorrect SQL or misunderstand
complex instructions. Therefore, the application does not trust the model
output directly.

This led to the addition of deterministic validation and safety layers.

---

## 3. Use a Hybrid LLM + Deterministic Architecture

### Decision

Do not rely entirely on the LLM.

Use the LLM for language understanding and SQL generation, while deterministic
Python components handle validation, safety, schema inspection, and other
critical logic.

### Why

LLMs can generate syntactically valid but logically incorrect SQL.

For example, during development Qwen generated:

```sql
UPDATE customers
SET name = 'NewName', city = 'NewCity'
WHERE 1;