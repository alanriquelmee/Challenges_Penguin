# Challenge 6 - Web Scraping & SQL Database

This project is part of the Penguin Academy bootcamp challenge series.  
The main goal was to **scrape data from a book website**, store it in a **relational SQL database**, and practice **SQL queries** (basic, intermediate, and advanced).

---

## 📌 Objectives
1. Scrape all categories and books from the website (no skipping allowed).
2. Design and implement a **relational database** with:
   - Categories  
   - Books  
   - Authors  
   - Many-to-many relationships (Books ↔ Authors)  
3. Generate an **ER diagram (UML)** to visualize the structure.
4. Insert the scraped data into the database.
5. Run **SQL queries** for data exploration:
   - Basic queries: `SELECT`, `WHERE`, `JOIN`, `GROUP BY`.
   - Advanced queries: subqueries, window functions, ranking.
6. Demonstrate the impact of **indexing**:
   - Show at least one query that is slow without an index.
   - Add an index and compare performance.

---

## 🛠️ Tech Stack
- **Python** (requests, BeautifulSoup, pandas, sqlite3)
- **SQLite** (relational database)
- **SQL** (DDL, DML, queries)
- **Jupyter Notebook** (analysis, experiments, and documentation)

---

## 📊 Database Schema
The final schema includes:

- **CATEGORIES**
  - `id_categoria` (PK)
  - `nombre_categoria`

- **BOOKS**
  - `id_libro` (PK)
  - `titulo`
  - `precio`
  - `disponibilidad`
  - `rating`
  - `id_categoria` (FK)

- **AUTHORS**
  - `id_autor` (PK)
  - `nombre_autor`

- **BOOK_AUTHOR**
  - `id_libro` (FK)
  - `id_autor` (FK)

> Relations:  
> - Categories ↔ Books (1-to-many)  
> - Books ↔ Authors (many-to-many)  

---

## 🔍 Example Queries

- **Basic JOIN:**
```sql
SELECT l.id_libro, l.titulo, c.nombre_categoria
FROM LIBROS l
JOIN CATEGORIAS c ON l.id_categoria = c.id_categoria
ORDER BY c.nombre_categoria, l.titulo;
