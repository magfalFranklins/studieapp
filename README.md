# studieapp
Franklins studieapp

Utöver de två pythonfilerna behövs filerna

.env #som innehåller

DATABASE_URL=postgres://.......länken till databasen

.flaskenv 

#som innehåller

FLASK_APP=app

FLASK_DEBUG=1

Appen kräver att följande moduler installerats

pip install psycopg2-binary

pip install flask

pip install python-dotenv

Lämpligen i en virtual environment som skapas med

py -3 -m venv .venv

.venv\scripts\activat

eventuellt behövs följande kommando

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process






