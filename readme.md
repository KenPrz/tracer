# Tracer

**Tracer** is a command-line tool to automate the documentation of a database. It uses a Makefile to simplify execution and a Python script (`main.py`) to generate the documentation.

---

## **Features**

* Generate documentation for any MySQL database.
* Flexible configuration via environment variables or Makefile arguments.
* Easy integration into existing workflows with `make`.

---

## **Requirements**

* Python 3.x
* MySQL client accessible from the machine
* `main.py` script with logic to document the database

---

## **Installation**

1. Clone the repository:

```bash
git clone git@github.com:KenPrz/tracer.git tracer
cd tracer
```

2. Install required Python packages (if any):

```bash
pip install -r requirements.txt
```

---

## **Makefile Usage**

### **Option 1: Pass variables directly**

```bash
make run DB_CONTAINER=my_container DB_USER=my_user DB_PASS=my_pass DB_NAME=my_db
```

### **Option 2: Set environment variables**

```bash
export DB_CONTAINER=my_container
export DB_USER=my_user
export DB_PASS=my_pass
export DB_NAME=my_db

make run
```

---

### **Makefile**

```make
# Makefile for Tracer project

.PHONY: run

run:
	@echo "Executing the database documentation script..."
	python3 main.py --db_container=$(DB_CONTAINER) --db_user=$(DB_USER) --db_pass=$(DB_PASS) --db_name=$(DB_NAME)
```

---

### **Python Script Usage**

The Python script (`main.py`) should accept these arguments:

* `--db_container` – Name of the database container or host
* `--db_user` – Database username
* `--db_pass` – Database password
* `--db_name` – Database name to document

Example:

```bash
python3 main.py --db_container=my_container --db_user=my_user --db_pass=my_pass --db_name=my_db
```

---

### **Notes**

* Ensure all required variables are set before running `make run`.
* The generated documentation can be customized inside `main.py` to output JSON, Markdown, or HTML.

---