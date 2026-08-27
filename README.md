# recipe-app-api
Recipe API Project
# Recipe App API

A Django REST Framework API for managing personal recipes, tags, ingredients, and recipe images. Each user's recipes and recipe attributes are isolated from other users.

## Features

- Custom email-based user model
- User registration, token authentication, and profile management
- Recipe create, read, update, and delete operations
- Nested tags and ingredients when creating or updating recipes
- Tag and ingredient listing, renaming, and deletion
- Recipe filtering by tag and ingredient IDs
- Recipe image uploads
- OpenAPI schema and Swagger UI
- PostgreSQL development environment managed with Docker Compose
- Automated tests for models, APIs, admin configuration, and management commands

## Technology

- Python 3.9+
- Django 3.2
- Django REST Framework
- PostgreSQL
- Pillow for image handling
- drf-spectacular for API documentation
- Docker Compose for local development

## Getting Started

### Prerequisites

Install:

- Docker Engine
- Docker Compose v2

The recommended development workflow runs the API and PostgreSQL database in containers, so a local Python installation is not required.

### Start the application

From the project root, run:

```bash
docker compose up --build
```

The application waits for PostgreSQL, applies migrations, and starts Django's development server at:

```text
http://localhost:8000
```

To run the services in the background:

```bash
docker compose up -d --build
```

Stop the services with:

```bash
docker compose down
```

Database and uploaded media are stored in Docker volumes. Use `docker compose down -v` only when you intentionally want to remove the local database and uploaded media volumes.

## Configuration

The Compose setup supplies the following database settings to the application:

| Variable | Purpose |
| --- | --- |
| `DB_HOST` | PostgreSQL service hostname |
| `DB_NAME` | Database name |
| `DB_USER` | Database user |
| `DB_PASS` | Database password |

For production, replace development settings such as the secret key, debug mode, allowed hosts, database credentials, and media storage configuration with environment-based values.

## API Documentation

Once the application is running:

- Swagger UI: `http://localhost:8000/api/docs/`
- OpenAPI schema: `http://localhost:8000/api/schema/`

The Swagger UI provides an interactive view of the available endpoints and request formats.

## Authentication

Protected endpoints use token authentication. Create a user, obtain a token, and send it with subsequent requests:

```http
Authorization: Token <token>
```

### Create a user

```bash
curl -X POST http://localhost:8000/api/user/create/ \
	-H "Content-Type: application/json" \
	-d '{
		"email": "cook@example.com",
		"password": "strong-password",
		"name": "Home Cook"
	}'
```

Passwords must contain at least five characters. The API stores passwords using Django's password hashing rather than as plain text.

### Obtain a token

```bash
curl -X POST http://localhost:8000/api/user/token/ \
	-H "Content-Type: application/json" \
	-d '{
		"email": "cook@example.com",
		"password": "strong-password"
	}'
```

The response contains a token:

```json
{
	"token": "your-token"
}
```

### Check or update the current user

```bash
curl http://localhost:8000/api/user/me/ \
	-H "Authorization: Token <token>"
```

The same endpoint accepts `PATCH` requests for updating the user's name or password.

## Endpoint Reference

All endpoints below, except user registration and token creation, require authentication unless stated otherwise.

### Users

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/user/create/` | Register a user |
| `POST` | `/api/user/token/` | Obtain an authentication token |
| `GET` | `/api/user/me/` | Retrieve the authenticated user |
| `PATCH` | `/api/user/me/` | Update the authenticated user |

### Recipes

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/recipe/recipes/` | List the authenticated user's recipes |
| `POST` | `/api/recipe/recipes/` | Create a recipe |
| `GET` | `/api/recipe/recipes/{id}/` | Retrieve one recipe |
| `PATCH` | `/api/recipe/recipes/{id}/` | Partially update a recipe |
| `PUT` | `/api/recipe/recipes/{id}/` | Replace a recipe |
| `DELETE` | `/api/recipe/recipes/{id}/` | Delete a recipe |
| `POST` | `/api/recipe/recipes/{id}/upload-image/` | Upload or replace a recipe image |

Recipe fields:

```json
{
	"title": "Vegetable curry",
	"time_minutes": 35,
	"description": "A quick weeknight curry.",
	"price": "12.50",
	"link": "https://example.com/vegetable-curry",
	"tags": [
		{"name": "Weeknight"}
	],
	"ingredients": [
		{"name": "Chickpeas"},
		{"name": "Tomatoes"}
	]
}
```

`title`, `time_minutes`, and `price` are required when creating a recipe. Tags and ingredients can be supplied as nested objects. Existing items with the same name for the authenticated user are reused; otherwise they are created automatically.

Filter recipes with comma-separated tag or ingredient IDs:

```text
/api/recipe/recipes/?tags=1,3
/api/recipe/recipes/?ingredients=2,4
/api/recipe/recipes/?tags=1&ingredients=2,4
```

Upload an image as multipart form data:

```bash
curl -X POST http://localhost:8000/api/recipe/recipes/1/upload-image/ \
	-H "Authorization: Token <token>" \
	-F "image=@/path/to/recipe.jpg"
```

### Tags and ingredients

Tags and ingredients share the same behavior:

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/recipe/tags/` | List the user's tags |
| `PATCH` | `/api/recipe/tags/{id}/` | Rename a tag |
| `DELETE` | `/api/recipe/tags/{id}/` | Delete a tag |
| `GET` | `/api/recipe/ingredients/` | List the user's ingredients |
| `PATCH` | `/api/recipe/ingredients/{id}/` | Rename an ingredient |
| `DELETE` | `/api/recipe/ingredients/{id}/` | Delete an ingredient |

Use `assigned_only=1` to return only attributes assigned to at least one recipe:

```text
/api/recipe/tags/?assigned_only=1
/api/recipe/ingredients/?assigned_only=1
```

New tags and ingredients are created automatically when they are included in a recipe create or update request. Standalone tag and ingredient endpoints are used for listing, renaming, and deleting existing items.

## Running Tests

Run the complete test suite inside the application container:

```bash
docker compose run --rm app python manage.py test
```

Run a specific application test module:

```bash
docker compose run --rm app python manage.py test recipe.tests.test_recipe_api
```

Run Django system checks:

```bash
docker compose run --rm app python manage.py check
```

Development linting dependencies are listed in `requirements.dev.txt`.

## Project Structure

```text
.
├── app/
│   ├── manage.py
│   ├── app/       # Django project settings and root URLs
│   ├── core/      # User, recipe, tag, and ingredient models
│   ├── recipe/    # Recipe API, serializers, URLs, and tests
│   └── user/      # User API, serializers, URLs, and tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── requirements.dev.txt
```

## Development Notes

- Run management commands from the `app` directory inside the container, or use `docker compose run --rm app ...` from the project root.
- Migrations are applied automatically by the development Compose command.
- Uploaded files are served from the development media configuration when `DEBUG` is enabled.
- API querysets are restricted to the authenticated user, so users cannot list or modify another user's recipes, tags, or ingredients through these endpoints.

## License

See [LICENSE](LICENSE) for license information.
