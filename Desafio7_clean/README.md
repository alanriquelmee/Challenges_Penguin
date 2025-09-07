# 🧩 Challenge 7 – Distributed Logging System

This project implements a **distributed logging system** using Python, Flask, and SQLite.  
It simulates multiple services generating logs and a central server that authenticates, stores, and serves those logs with query filters.

---

## 🚀 Features

- **Multiple simulated services** (`billing`, `users`, `payments`) with unique tokens.
- **Log submission formats**:
  - Single JSON object
  - Array of JSON objects
  - `{"logs": [ ... ]}` batch
- **Database persistence** using SQLite with indexes for efficient queries.
- **Filters** on `service`, `severity`, `timestamp`, `received_at`, plus pagination.
- **Authentication**: only valid tokens can send logs.
- **Clear JSON responses** for all requests.

---

## ⚙️ Setup

### 1. Clone this repository
```bash
git clone https://github.com/alanriquelmee/Challenges_Penguin.git
cd Challenges_Penguin/Desafio7
