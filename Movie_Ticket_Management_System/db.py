import mysql.connector


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="movie_ticket_booking"
)

print("Database connected!")

cursor = conn.cursor()