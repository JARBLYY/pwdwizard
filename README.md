# 🔐 PWDWizard

A self-hosted password manager built with Python, Flask, and MySQL. Store and retrieve encrypted credentials through a clean web UI — no third-party vaults, no cloud dependency, your data stays yours.

---

## How it works

- You enter a **master password** on login
- The app derives an encryption key from it using **PBKDF2-HMAC-SHA256** (100k iterations)
- All passwords are encrypted with **Fernet (AES-128)** before hitting the database
- Your master password and derived key are **never stored** — only held in the server session while you're logged in

---

## Stack

| Layer | Tech |
|---|---|
| Backend | Python 3.10, Flask |
| Encryption | `cryptography` (Fernet + PBKDF2) |
| Database | MySQL 8 |
| Containerization | Docker + Docker Compose |

---

## Running locally

**Prerequisites:** Docker + Docker Compose installed.

```bash
git clone https://github.com/JARBLYY/pwdwizard.git
cd pwdwizard
docker-compose up --build
```

Then open `http://localhost:5000` in your browser.

---

## Project structure

```
backend/
  app.py                  # Flask app + routes
  PWDWizard/
    MasterPassword.py     # PBKDF2 key derivation
    EncryptAndDecrypt.py  # Fernet encrypt/decrypt
    generator.py          # Secure password generation
    MySQL.py              # DB connection + setup
    SavingAndRetrieving.py
  templates/
    login.html
    dashboard.html
    add_password.html
```

---

## ⚠️ Security notes

- The `SECRET_KEY` in `app.py` should be changed to a strong random value before deploying
- MySQL credentials in `docker-compose.yml` are defaults — update them for any non-local deployment
- This project is built for learning/personal use; a production deployment would warrant a full security audit

---

## Roadmap

- [ ] FastAPI REST backend (Round 2)
- [ ] Cloud deployment (Render)
- [ ] Password strength indicator
- [ ] Search / filter vault entries
- [ ] Per-entry tags / categories
