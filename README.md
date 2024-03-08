# Wildberries Scrapper Bot

Bot for scraping information about products from Wildberries.

## Installation and Setup

1. Install Docker and Docker Compose if they are not already installed on your system.

2. Clone the project repository:

```bash
git clone https://github.com/Djama1GIT/wildberries-scrapper-bot.git
cd wildberries-scrapper-bot
```

3. Configure the environment variables in the .env-non-dev file.

4. Start the project:

```bash
docker-compose up --build
```

## Technologies Used

- Python - The programming language used for the project.
- Aiogram3 - A Python wrapper for the Telegram Bot API.
- Redis - An in-memory database used in the project for data caching and storing Celery tasks.
- Celery - A library used in the project for executing background tasks and processing long-running operations.
- PostgreSQL - A relational database used in the project for data storage.
- SQLAlchemy - An Object-Relational Mapping (ORM) used in the project for working with the database.
- Alembic - A database migration library used in the project to update the database structure when data models change.
- Docker - A platform used in the project for creating, deploying, and managing containers, allowing the application to run in an isolated environment.