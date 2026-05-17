import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="netflixdb"
)

cursor = db.cursor()