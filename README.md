# Rock Art Database

Rock art recording database with Django, REST, and GraphQL APIs plus a tabbed web UI for data entry.

## Quick start

```bash
poetry install --with dev
poetry run python rockartdb/manage.py migrate
poetry run python rockartdb/manage.py runserver
```

Open the UI at `http://localhost:8000/` and add/select a site using the header dropdown.

## APIs

- REST: `http://localhost:8000/api/` (browse endpoints)
- Swagger UI: `http://localhost:8000/api/docs/`
- GraphQL (GraphiQL): `http://localhost:8000/graphql`
- GraphQL via REST: `POST http://localhost:8000/api/graphql/` with JSON body `{"query": "...", "variables": {}}`

## Tests

```bash
poetry run python rockartdb/manage.py test rockart -v 2
```
