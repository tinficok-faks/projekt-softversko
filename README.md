![Tests](https://img.shields.io/badge/tests-17%2F19%20passed-yellow)
[![Coverage](https://img.shields.io/badge/coverage-76%25-yellowgreen)](backend/htmlcov/index.html)

# projekt-softversko

Full-stack web aplikacija razvijena u sklopu kolegija **Softversko programiranje** na Fakultetu primijenjene matematike i informatike Sveučilišta u Osijeku (FPMIZ Osijek).

---

## O projektu

Ovaj projekt je full-stack web aplikacija s Python backendom i JavaScript/CSS frontendom. Razvijen je kao projektni zadatak u timu od tri suradnika.

## Struktura projekta

```
projekt-softversko/
├── backend/       # Python REST API / poslovna logika
├── frontend/      # JSX + CSS web klijent
├── .gitignore
└── README.md
```

## Tehnički stack

| Sloj     | Tehnologija         |
|----------|---------------------|
| Backend  | Python              |
| Frontend | JSX, CSS            |

## Backend paketi

| Paket | Upotreba |
|---|---|
| `fastapi` | Router, Depends, HTTPException, CORSMiddleware, StaticFiles |
| `uvicorn` | Backend server (pokretanje aplikacije) |
| `sqlmodel` | SQLModel, Field, Relationship, Session, create_engine |
| `pydantic` | Kroz pydantic-settings |
| `pydantic-settings` | BaseSettings, SettingsConfigDict (za .env datoteke) |
| `python-jose` | JWT encoding/decoding (jose.jwt) |
| `passlib` | Password hashing context (CryptContext) |
| `bcrypt` | Kroz passlib kao scheme |
| `python-multipart` | File uploads (FastAPI UploadFile) |
| `pytest` | Test framework |


## Pokretanje

### Preduvjeti

- [Python 3.x](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/) (za frontend)

### Pokretanje backenda

```bash
cd backend
pip install -r requirements.txt
python3 init_db.py
uvicorn app.main:app -—reload
```

### Pokretanje frontenda

```bash
cd frontend
npm install
npm run dev
```

## Suradnici

Projekt je razvijen od strane pet studenata u sklopu kolegija Softversko programiranje. Pogledajte [stranicu suradnika](https://github.com/TonyVargek/projekt-softversko/graphs/contributors) za više detalja.

## Kolegij

**Softversko programiranje**
Fakultet primijenjene matematike i informatike (MATHOS), Sveučilište Josipa Jurja Strossmayera u Osijeku
