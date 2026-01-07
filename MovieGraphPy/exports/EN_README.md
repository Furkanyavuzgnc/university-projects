# 🎬 MovieGraphPy — Python Application with the Neo4j Movies Dataset

This project is a Python console application that queries **movie–actor–director relationships** from the Neo4j **Movies Dataset** and generates a graphical data output in **graph.json** format for the selected movie.

The goal of the project is to demonstrate graph database structure, Python–Neo4j integration, and visualization of relational movie data in graph model format.

---

## 🧠 Technologies Used

- 🐍 Python  
- 🗄 Neo4j Desktop  
- 🔌 Bolt Protocol  
- 🧾 Cypher Query Language  
- 📦 neo4j Python Driver  

---

## ⚙️ Installation Steps

### 1️⃣ Install Neo4j

✔ Install Neo4j Desktop  
✔ Create a new database  
✔ Start the database (**it must be Running**)  

To load the Movies dataset, run: :play movies


and execute the commands in order.

---

### 2️⃣ Create a Python Virtual Environment

Inside the project folder:python -m venv .venv


Activate it and install the required package:pip install neo4j


---

### 3️⃣ Connection Settings

Application uses the following settings:
    bolt://localhost:7687
    username: neo4j
    password: ********


---

## ▶️ Running the Application

Run:python main.py


You will see the following menu:
    Search Movie
    Show Movie Details
    Create graph.json for Selected Movie
    Exit


---

## 🔍 Features

### ✔ Search Movie
Returns a list of movies matching the search keyword.

### ✔ Show Movie Details
Displays:

- Movie title  
- Release year  
- Tagline  
- Directors  
- Actors  

---

### ✔ Create graph.json
Exports data for the selected movie:
    nodes → Movie and people
    links → Relationships between them


File location:exports/graph.json


The file is **overwritten each time**.

---

## 🧠 About the JSON Structure

Example format:

```json
{
  "nodes": [...],
  "links": [...]
}

✔ nodes → graph nodes (Movie & Person)
✔ links → relationships (ACTED_IN / DIRECTED)

This JSON file can be used in graph visualization tools.

📂 Project Structure
MovieGraphPy
 ├ main.py
 ├ db.py
 ├ services
 │   ├ search_service.py
 │   ├ detail_service.py
 │   ├ graph_service.py
 ├ exports
 │   └ graph.json
 └ README.md


🧾 Code Architecture
The application works with three main services:
| File                | Purpose                         |
| ------------------- | ------------------------------- |
| `search_service.py` | Handles movie search operations |
| `detail_service.py` | Fetches movie details           |
| `graph_service.py`  | Generates JSON graph output     |
| `db.py`             | Tests database connection       |
| `main.py`           | Menu-based console interface    |

🎯 Learning Outcomes
✔ Understand graph database modeling with Neo4j
✔ Build Python–Neo4j integration
✔ Write Cypher queries
✔ Generate JSON-based graph data
✔ Develop a console-based application

📌 Notes
    Database must be running
    Incorrect password will cause connection failure
    graph.json is overwritten each time

✅ License
This project is developed for educational purposes.











