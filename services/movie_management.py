import mysql.connector

from db import conn, cursor
from models.movie import Movie

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()


# ==========================================================
# ADD MOVIE
# ==========================================================

def add_movie():

    console.print(
        Panel(
            "[bold cyan]🎬 ADD MOVIE[/bold cyan]",
            border_style="cyan",
            box=box.DOUBLE
        )
    )

    try:

        movie_name = console.input(
            "[bold green]Movie Name : [/bold green]"
        ).strip()

        genre = console.input(
            "[bold green]Genre : [/bold green]"
        ).strip()

        language = console.input(
            "[bold green]Language : [/bold green]"
        ).strip()

        duration = int(
            console.input(
                "[bold green]Duration (minutes) : [/bold green]"
            )
        )

        release_date = console.input(
            "[bold green]Release Date (YYYY-MM-DD) : [/bold green]"
        ).strip()

        if not movie_name or not genre or not language:
            console.print(
                Panel(
                    "[bold red]❌ All fields are required.[/bold red]",
                    border_style="red"
                )
            )
            return

        cursor.execute(
            """
            INSERT INTO movies
            (
                movie_name,
                genre,
                language,
                duration,
                release_date
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                movie_name,
                genre,
                language,
                duration,
                release_date
            )
        )

        conn.commit()

        console.print(
            Panel(
                "[bold green]✅ Movie added successfully![/bold green]\n\n"
                f"[green]Movie : {movie_name}[/green]",
                border_style="green",
                box=box.DOUBLE
            )
        )

    except ValueError:

        console.print(
            Panel(
                "[bold red]❌ Duration must be a number.[/bold red]",
                border_style="red"
            )
        )

    except mysql.connector.Error as e:

        conn.rollback()

        console.print(
            Panel(
                f"[bold red]❌ Database Error[/bold red]\n\n"
                f"[yellow]{e}[/yellow]",
                border_style="red"
            )
        )

    except KeyboardInterrupt:

        conn.rollback()

        console.print(
            "\n[yellow]⚠️ Add movie cancelled.[/yellow]"
        )

    except Exception as e:

        conn.rollback()

        console.print(
            Panel(
                f"[bold red]❌ Error[/bold red]\n\n"
                f"[yellow]{e}[/yellow]",
                border_style="red"
            )
        )


# ==========================================================
# VIEW MOVIES
# ==========================================================

def view_movies():

    console.print(
        Panel(
            "[bold cyan]📋 VIEW MOVIES[/bold cyan]",
            border_style="cyan",
            box=box.DOUBLE
        )
    )

    try:

        cursor.execute(
            """
            SELECT
                movie_id,
                movie_name,
                genre,
                language,
                duration,
                release_date
            FROM movies
            ORDER BY movie_id
            """
        )

        movies = cursor.fetchall()

        if not movies:

            console.print(
                Panel(
                    "[yellow]⚠️ No movies found.[/yellow]",
                    border_style="yellow"
                )
            )

            return

        table = Table(
            title="🎬 MOVIE LIST",
            box=box.ROUNDED,
            border_style="cyan",
            show_lines=True
        )

        table.add_column(
            "Movie ID",
            justify="center",
            style="bold yellow"
        )

        table.add_column("Movie Name")
        table.add_column("Genre")
        table.add_column("Language")
        table.add_column(
            "Duration",
            justify="center"
        )

        table.add_column(
            "Release Date",
            justify="center"
        )

        for row in movies:

            movie = Movie(
                movie_id=row[0],
                movie_name=row[1],
                genre=row[2],
                language=row[3],
                duration=row[4],
                release_date=row[5]
            )

            table.add_row(
                str(movie.movie_id),
                str(movie.movie_name),
                str(movie.genre),
                str(movie.language),
                f"{movie.duration} min",
                str(movie.release_date)
            )

        console.print(table)

    except mysql.connector.Error as e:

        console.print(
            Panel(
                f"[bold red]❌ Database Error[/bold red]\n\n"
                f"[yellow]{e}[/yellow]",
                border_style="red"
            )
        )

    except Exception as e:

        console.print(
            Panel(
                f"[bold red]❌ Error[/bold red]\n\n"
                f"[yellow]{e}[/yellow]",
                border_style="red"
            )
        )


# ==========================================================
# SEARCH MOVIE
# ID / NAME / GENRE / LANGUAGE / RELEASE DATE
# ==========================================================

def search_movie():

    console.print(
        Panel(
            "[bold cyan]🔍 SEARCH MOVIE[/bold cyan]",
            border_style="cyan",
            box=box.DOUBLE
        )
    )

    try:

        # --------------------------------------------------
        # SEARCH OPTIONS
        # --------------------------------------------------

        table = Table(
            title="SEARCH BY",
            box=box.ROUNDED,
            border_style="blue"
        )

        table.add_column(
            "Option",
            justify="center",
            style="bold yellow"
        )

        table.add_column(
            "Search Type",
            style="bold white"
        )

        table.add_row("1", "🆔 Movie ID")
        table.add_row("2", "🎬 Movie Name")
        table.add_row("3", "🎭 Genre")
        table.add_row("4", "🌐 Language")
        table.add_row("5", "📅 Release Date")
        table.add_row("6", "🔎 Search All Fields")

        console.print(table)

        choice = console.input(
            "\n[bold green]Enter Search Choice : [/bold green]"
        ).strip()

        # --------------------------------------------------
        # MOVIE ID
        # --------------------------------------------------

        if choice == "1":

            movie_id = int(
                console.input(
                    "[bold green]Enter Movie ID : [/bold green]"
                )
            )

            query = """
                SELECT
                    movie_id,
                    movie_name,
                    genre,
                    language,
                    duration,
                    release_date
                FROM movies
                WHERE movie_id = %s
            """

            cursor.execute(
                query,
                (movie_id,)
            )

        # --------------------------------------------------
        # MOVIE NAME
        # --------------------------------------------------

        elif choice == "2":

            movie_name = console.input(
                "[bold green]Enter Movie Name : [/bold green]"
            ).strip()

            query = """
                SELECT
                    movie_id,
                    movie_name,
                    genre,
                    language,
                    duration,
                    release_date
                FROM movies
                WHERE movie_name LIKE %s
                ORDER BY movie_id
            """

            cursor.execute(
                query,
                (f"%{movie_name}%",)
            )

        # --------------------------------------------------
        # GENRE
        # --------------------------------------------------

        elif choice == "3":

            genre = console.input(
                "[bold green]Enter Genre : [/bold green]"
            ).strip()

            query = """
                SELECT
                    movie_id,
                    movie_name,
                    genre,
                    language,
                    duration,
                    release_date
                FROM movies
                WHERE genre LIKE %s
                ORDER BY movie_id
            """

            cursor.execute(
                query,
                (f"%{genre}%",)
            )

        # --------------------------------------------------
        # LANGUAGE
        # --------------------------------------------------

        elif choice == "4":

            language = console.input(
                "[bold green]Enter Language : [/bold green]"
            ).strip()

            query = """
                SELECT
                    movie_id,
                    movie_name,
                    genre,
                    language,
                    duration,
                    release_date
                FROM movies
                WHERE language LIKE %s
                ORDER BY movie_id
            """

            cursor.execute(
                query,
                (f"%{language}%",)
            )

        # --------------------------------------------------
        # RELEASE DATE
        # --------------------------------------------------

        elif choice == "5":

            release_date = console.input(
                "[bold green]Enter Release Date (YYYY-MM-DD) : [/bold green]"
            ).strip()

            query = """
                SELECT
                    movie_id,
                    movie_name,
                    genre,
                    language,
                    duration,
                    release_date
                FROM movies
                WHERE release_date = %s
            """

            cursor.execute(
                query,
                (release_date,)
            )

        # --------------------------------------------------
        # SEARCH ALL
        # --------------------------------------------------

        elif choice == "6":

            keyword = console.input(
                "[bold green]Enter Search Keyword : [/bold green]"
            ).strip()

            query = """
                SELECT
                    movie_id,
                    movie_name,
                    genre,
                    language,
                    duration,
                    release_date
                FROM movies
                WHERE
                    CAST(movie_id AS CHAR) LIKE %s
                    OR movie_name LIKE %s
                    OR genre LIKE %s
                    OR language LIKE %s
                    OR CAST(duration AS CHAR) LIKE %s
                    OR CAST(release_date AS CHAR) LIKE %s
                ORDER BY movie_id
            """

            value = f"%{keyword}%"

            cursor.execute(
                query,
                (
                    value,
                    value,
                    value,
                    value,
                    value,
                    value
                )
            )

        else:

            console.print(
                Panel(
                    "[bold red]❌ Invalid Search Choice![/bold red]",
                    border_style="red"
                )
            )

            return

        # --------------------------------------------------
        # GET RESULTS
        # --------------------------------------------------

        movies = cursor.fetchall()

        if not movies:

            console.print(
                Panel(
                    "[bold red]❌ No movie found.[/bold red]",
                    border_style="red"
                )
            )

            return

        # --------------------------------------------------
        # DISPLAY RESULTS
        # --------------------------------------------------

        result_table = Table(
            title="🔎 SEARCH RESULTS",
            box=box.ROUNDED,
            border_style="green",
            show_lines=True
        )

        result_table.add_column(
            "Movie ID",
            justify="center",
            style="bold yellow"
        )

        result_table.add_column("Movie Name")
        result_table.add_column("Genre")
        result_table.add_column("Language")

        result_table.add_column(
            "Duration",
            justify="center"
        )

        result_table.add_column(
            "Release Date",
            justify="center"
        )

        for row in movies:

            result_table.add_row(
                str(row[0]),
                str(row[1]),
                str(row[2]),
                str(row[3]),
                f"{row[4]} min",
                str(row[5])
            )

        console.print(result_table)

    except ValueError:

        console.print(
            Panel(
                "[bold red]❌ Movie ID must be a number.[/bold red]",
                border_style="red"
            )
        )

    except mysql.connector.Error as e:

        console.print(
            Panel(
                f"[bold red]❌ Database Error[/bold red]\n\n"
                f"[yellow]{e}[/yellow]",
                border_style="red"
            )
        )

    except KeyboardInterrupt:

        console.print(
            "\n[yellow]⚠️ Search cancelled.[/yellow]"
        )

    except Exception as e:

        console.print(
            Panel(
                f"[bold red]❌ Error[/bold red]\n\n"
                f"[yellow]{e}[/yellow]",
                border_style="red"
            )
        )


# ==========================================================
# UPDATE MOVIE
# ==========================================================

def update_movie():

    console.print(
        Panel(
            "[bold cyan]✏️ UPDATE MOVIE[/bold cyan]",
            border_style="cyan",
            box=box.DOUBLE
        )
    )

    try:

        movie_id = int(
            console.input(
                "[bold green]Enter Movie ID : [/bold green]"
            )
        )

        cursor.execute(
            """
            SELECT
                movie_id,
                movie_name,
                genre,
                language,
                duration,
                release_date
            FROM movies
            WHERE movie_id = %s
            """,
            (movie_id,)
        )

        movie = cursor.fetchone()

        if not movie:

            console.print(
                Panel(
                    "[bold red]❌ Movie not found.[/bold red]",
                    border_style="red"
                )
            )

            return

        console.print(
            Panel(
                f"[cyan]Current Movie : {movie[1]}[/cyan]",
                border_style="cyan"
            )
        )

        movie_name = console.input(
            f"[bold green]New Movie Name [{movie[1]}] : [/bold green]"
        ).strip()

        genre = console.input(
            f"[bold green]New Genre [{movie[2]}] : [/bold green]"
        ).strip()

        language = console.input(
            f"[bold green]New Language [{movie[3]}] : [/bold green]"
        ).strip()

        duration_input = console.input(
            f"[bold green]New Duration [{movie[4]}] : [/bold green]"
        ).strip()

        release_date = console.input(
            f"[bold green]New Release Date [{movie[5]}] : [/bold green]"
        ).strip()

        if not movie_name:
            movie_name = movie[1]

        if not genre:
            genre = movie[2]

        if not language:
            language = movie[3]

        if not duration_input:
            duration = movie[4]
        else:
            duration = int(duration_input)

        if not release_date:
            release_date = movie[5]

        cursor.execute(
            """
            UPDATE movies
            SET
                movie_name = %s,
                genre = %s,
                language = %s,
                duration = %s,
                release_date = %s
            WHERE movie_id = %s
            """,
            (
                movie_name,
                genre,
                language,
                duration,
                release_date,
                movie_id
            )
        )

        conn.commit()

        console.print(
            Panel(
                "[bold green]✅ Movie updated successfully.[/bold green]",
                border_style="green",
                box=box.DOUBLE
            )
        )

    except ValueError:

        console.print(
            Panel(
                "[bold red]❌ Duration/Movie ID must be a number.[/bold red]",
                border_style="red"
            )
        )

    except mysql.connector.Error as e:

        conn.rollback()

        console.print(
            Panel(
                f"[bold red]❌ Database Error[/bold red]\n\n"
                f"[yellow]{e}[/yellow]",
                border_style="red"
            )
        )

    except KeyboardInterrupt:

        conn.rollback()

        console.print(
            "\n[yellow]⚠️ Update movie cancelled.[/yellow]"
        )

    except Exception as e:

        conn.rollback()

        console.print(
            Panel(
                f"[bold red]❌ Error[/bold red]\n\n"
                f"[yellow]{e}[/yellow]",
                border_style="red"
            )
        )


# ==========================================================
# DELETE MOVIE
# ==========================================================

# ==========================================================
# DELETE MOVIE
# ==========================================================

def delete_movie():

    try:

        movie_id = int(
            console.input(
                "[bold green]Enter Movie ID : [/bold green]"
            )
        )

        # Delete related shows first
        cursor.execute(
            """
            DELETE FROM shows
            WHERE movie_id = %s
            """,
            (movie_id,)
        )

        # Delete movie
        cursor.execute(
            """
            DELETE FROM movies
            WHERE movie_id = %s
            """,
            (movie_id,)
        )

        conn.commit()

        console.print(
            Panel(
                "[bold green]✅ Movie deleted successfully.[/bold green]",
                border_style="green"
            )
        )

    except ValueError:

        console.print(
            Panel(
                "[bold red]❌ Movie ID must be a number.[/bold red]",
                border_style="red"
            )
        )

    except mysql.connector.Error as e:

        conn.rollback()

        console.print(
            Panel(
                f"[bold red]❌ Database Error[/bold red]\n\n"
                f"[yellow]{e}[/yellow]",
                border_style="red"
            )
        )

    except Exception as e:

        conn.rollback()

        console.print(
            Panel(
                f"[bold red]❌ Error[/bold red]\n\n"
                f"[yellow]{e}[/yellow]",
                border_style="red"
            )
        )