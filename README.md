# SpotOn: The Efficient Event Booking Solution

Simplify event ticketing and boost registrations with SpotOn — an efficient event booking solution for organizers.

---

## Requirements

- Python 3.12
- Node.js 18
- npm 9+
- PostgreSQL 16 (production) or SQLite (local dev)

---

## Local Development

### 1. Clone the repository

```bash
git clone https://github.com/mnovosel29/spot_on.git
cd spot_on
```

### 2. Create and activate a virtual environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and fill in the required values. Leave `DATABASE_URI` empty to use SQLite locally.

### 5. Install Node.js dependencies and build CSS

```bash
npm install
npm run build
```

For live CSS reloading during development:

```bash
npm run watch
```

### 6. Run database migrations

```bash
flask db upgrade
```

### 7. Seed the admin user

```bash
python seed.py
```

Credentials are read from `.env` (`ADMIN_EMAIL`, `ADMIN_PASSWORD`). The script is idempotent — safe to run multiple times.

### 8. Start the development server

```bash
flask run
```

App will be available at `http://localhost:5000`.

---

## Production (Docker)

### 1. Clone the repository

```bash
git clone https://github.com/mnovosel29/spot_on.git
cd spot_on
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and set all required values — `SECRET_KEY`, `SECURITY_PASSWORD_SALT`, mail settings, and admin credentials. `DATABASE_URI` is overridden by `docker-compose.yml` to point at the Postgres service, so it can be left empty.

### 3. Build and start all services

```bash
docker compose up --build
```

This will:
1. Start the Postgres database and wait until it is healthy
2. Build the Tailwind CSS via the `npm` service
3. Run `flask db upgrade` and seed the admin user
4. Start the Flask application on port `5023`

App will be available at `http://localhost:5023`.

### 4. Stop all services

```bash
docker compose down
```

To also remove the database volume:

```bash
docker compose down -v
```

---

## Adding Translations

### 1. Register the new language

In `.env`, add the language code to `LANGUAGES` (comma-separated) and optionally set it as `DEFAULT_LANGUAGE`:

```
LANGUAGES="en,hr,es"
DEFAULT_LANGUAGE="hr"
```

### 2. Extract translatable strings

```bash
pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .
```

### 3. Initialize the new language

```bash
pybabel init -i messages.pot -d app/translations -l <language-code>
```

### 4. Translate strings

Open `app/translations/<language-code>/LC_MESSAGES/messages.po` and fill in translations for each `msgstr`.

### 5. Compile translations

```bash
pybabel compile -d app/translations
```

For Flask-Security strings:

```bash
pybabel compile -d app/translations/ -i app/translations/<language-code>/LC_MESSAGES/flask_security.po -l <language-code> -D flask_security
```

### 6. Restart the application

Translations take effect after a restart.
