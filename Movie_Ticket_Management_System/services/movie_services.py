from datetime import datetime
import mysql.connector

from db import conn, cursor
from models.movie import Movie


# ---------------- ADD MOVIE ---------------- #

def add_movie():
    try:
        print("\n===== Add Movie =====")

        movie_name = input("Movie Name : ")
        genre = input("Genre : ")
        language = input("Language : ")
        duration = int(input("Duration (minutes) : "))

        date = input("Release Date (DD-MM-YYYY): ")
        release_date = datetime.strptime(date, "%d-%m-%Y").strftime("%Y-%m-%d")

        movie = Movie(movie_name, genre, language, duration, release_date)

        query = """
        INSERT INTO movies
        (movie_name, genre, language, duration, release_date)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            movie.movie_name,
            movie.genre,
            movie.language,
            movie.duration,
            movie.release_date
        )

        cursor.execute(query, values)
        conn.commit()

        print("Movie Added Successfully!")

    except ValueError:
        print("Invalid Input! Duration must be a number and date must be DD-MM-YYYY.")

    except mysql.connector.Error as e:
        print("Database Error :", e)

    except Exception as e:
        print("Error :", e)


# ---------------- VIEW MOVIES ---------------- #

def view_movies():
    try:
        print("\n===== Movie List =====")

        cursor.execute("SELECT * FROM movies")
        movies = cursor.fetchall()

        if not movies:
            print("No Movies Found.")
            return

        print("-" * 80)
        print(f"{'ID':<5}{'Movie Name':<20}{'Genre':<15}{'Language':<15}{'Duration':<10}{'Release Date'}")
        print("-" * 80)

        for movie in movies:
            print(f"{movie[0]:<5}{movie[1]:<20}{movie[2]:<15}{movie[3]:<15}{movie[4]:<10}{movie[5]}")

    except mysql.connector.Error as e:
        print("Database Error :", e)

    except Exception as e:
        print("Error :", e)


# ---------------- SEARCH MOVIE ---------------- #

def search_movie():

    while True:

        try:
            print("\n===== Search Movie =====")
            print("1. Search by Movie ID")
            print("2. Search by Movie Name")
            print("3. Search by Language")
            print("4. Search by Genre")
            print("5. Back")

            choice = input("Enter Choice : ")

            if choice == "1":
                movie_id = int(input("Enter Movie ID : "))
                query = "SELECT * FROM movies WHERE movie_id=%s"
                cursor.execute(query, (movie_id,))
                movies = cursor.fetchall()

            elif choice == "2":
                movie_name = input("Enter Movie Name : ")
                query = "SELECT * FROM movies WHERE movie_name LIKE %s"
                cursor.execute(query, ("%" + movie_name + "%",))
                movies = cursor.fetchall()

            elif choice == "3":
                language = input("Enter Language : ")
                query = "SELECT * FROM movies WHERE language=%s"
                cursor.execute(query, (language,))
                movies = cursor.fetchall()

            elif choice == "4":
                genre = input("Enter Genre : ")
                query = "SELECT * FROM movies WHERE genre=%s"
                cursor.execute(query, (genre,))
                movies = cursor.fetchall()

            elif choice == "5":
                return

            else:
                print("Invalid Choice!")
                continue

            if movies:
                print("\n" + "-" * 80)
                print(f"{'ID':<5}{'Movie Name':<20}{'Genre':<15}{'Language':<15}{'Duration':<10}{'Release Date'}")
                print("-" * 80)

                for movie in movies:
                    print(f"{movie[0]:<5}{movie[1]:<20}{movie[2]:<15}{movie[3]:<15}{movie[4]:<10}{movie[5]}")
            else:
                print("Movie Not Found.")

        except ValueError:
            print("Movie ID must be a number.")

        except mysql.connector.Error as e:
            print("Database Error :", e)

        except Exception as e:
            print("Error :", e)


# ---------------- UPDATE MOVIE ---------------- #

def update_movie():

    try:
        movie_id = int(input("Enter Movie ID : "))

        cursor.execute("SELECT * FROM movies WHERE movie_id=%s", (movie_id,))
        movie = cursor.fetchone()

        if not movie:
            print("Movie Not Found.")
            return

        movie_name = input("New Movie Name : ")
        genre = input("New Genre : ")
        language = input("New Language : ")
        duration = int(input("New Duration (minutes): "))

        date = input("New Release Date (DD-MM-YYYY): ")
        release_date = datetime.strptime(date, "%d-%m-%Y").strftime("%Y-%m-%d")

        query = """
        UPDATE movies
        SET movie_name=%s,
            genre=%s,
            language=%s,
            duration=%s,
            release_date=%s
        WHERE movie_id=%s
        """

        values = (
            movie_name,
            genre,
            language,
            duration,
            release_date,
            movie_id
        )

        cursor.execute(query, values)
        conn.commit()

        print("Movie Updated Successfully!")

    except ValueError:
        print("Invalid Input! Duration must be a number and date must be DD-MM-YYYY.")

    except mysql.connector.Error as e:
        print("Database Error :", e)

    except Exception as e:
        print("Error :", e)


# ---------------- DELETE MOVIE ---------------- #

def delete_movie():

    try:
        movie_id = int(input("Enter Movie ID : "))

        cursor.execute("SELECT * FROM movies WHERE movie_id=%s", (movie_id,))
        movie = cursor.fetchone()

        if not movie:
            print("Movie Not Found.")
            return

        cursor.execute("DELETE FROM movies WHERE movie_id=%s", (movie_id,))
        conn.commit()

        print("Movie Deleted Successfully!")

    except ValueError:
        print("Movie ID must be a number.")

    except mysql.connector.Error as e:
        print("Database Error :", e)

    except Exception as e:
        print("Error :", e)