from datetime import datetime, timedelta
import mysql.connector

from db import conn, cursor
from models.shows import Show

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()


# ==========================================================
# ADD SHOW
# ==========================================================

def add_show():

    console.print(
        Panel(
            "[bold cyan]🎭 ADD SHOW[/bold cyan]",
            border_style="cyan",
            box=box.DOUBLE
        )
    )

    try:

        movie_id = int(
            console.input(
                "[bold green]Movie ID : [/bold green]"
            )
        )

        theater_id = int(
            console.input(
                "[bold green]Theater ID : [/bold green]"
            )
        )

        show_date = console.input(
            "[bold green]Show Date (YYYY-MM-DD) : [/bold green]"
        ).strip()

        show_time = console.input(
            "[bold green]Show Time (HH:MM:SS) : [/bold green]"
        ).strip()

        new_start = datetime.strptime(
            show_date + " " + show_time,
            "%Y-%m-%d %H:%M:%S"
        )

        # --------------------------------------------------
        # CHECK MOVIE
        # --------------------------------------------------

        cursor.execute(
            """
            SELECT movie_name, duration
            FROM movies
            WHERE movie_id = %s
            """,
            (movie_id,)
        )

        movie = cursor.fetchone()

        if not movie:

            console.print(
                Panel(
                    "[bold red]❌ Movie ID not found.[/bold red]",
                    border_style="red"
                )
            )

            return

        movie_name = movie[0]
        duration = movie[1]

        # --------------------------------------------------
        # CHECK THEATER
        # --------------------------------------------------

        cursor.execute(
            """
            SELECT theater_name
            FROM theaters
            WHERE theater_id = %s
            """,
            (theater_id,)
        )

        theater = cursor.fetchone()

        if not theater:

            console.print(
                Panel(
                    "[bold red]❌ Theater ID not found.[/bold red]",
                    border_style="red"
                )
            )

            return

        # --------------------------------------------------
        # CALCULATE END TIME
        # --------------------------------------------------

        new_end = new_start + timedelta(
            minutes=duration
        )

        # --------------------------------------------------
        # CHECK EXISTING SHOWS
        # --------------------------------------------------

        cursor.execute(
            """
            SELECT
                s.show_id,
                s.show_time,
                m.movie_name,
                m.duration
            FROM shows s
            JOIN movies m
                ON s.movie_id = m.movie_id
            WHERE s.theater_id = %s
            AND s.show_date = %s
            """,
            (theater_id, show_date)
        )

        existing_shows = cursor.fetchall()

        # --------------------------------------------------
        # CHECK TIMING CONFLICT
        # --------------------------------------------------

        for show in existing_shows:

            existing_show_id = show[0]
            existing_time = str(show[1])
            existing_movie_name = show[2]
            existing_duration = show[3]

            existing_time = existing_time.split(".")[0]

            existing_start = datetime.strptime(
                show_date + " " + existing_time,
                "%Y-%m-%d %H:%M:%S"
            )

            existing_end = (
                existing_start
                + timedelta(minutes=existing_duration)
            )

            if (
                new_start < existing_end
                and new_end > existing_start
            ):

                console.print(
                    Panel(
                        "[bold red]❌ SHOW TIMING CONFLICT![/bold red]\n\n"
                        f"[yellow]Existing Show ID : {existing_show_id}[/yellow]\n"
                        f"[yellow]Existing Movie : {existing_movie_name}[/yellow]\n"
                        f"[yellow]Existing Start : "
                        f"{existing_start.strftime('%H:%M:%S')}[/yellow]\n"
                        f"[yellow]Existing End : "
                        f"{existing_end.strftime('%H:%M:%S')}[/yellow]",
                        border_style="red"
                    )
                )

                return

        # --------------------------------------------------
        # INSERT SHOW
        # --------------------------------------------------

        cursor.execute(
            """
            INSERT INTO shows
            (
                movie_id,
                theater_id,
                show_date,
                show_time
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                movie_id,
                theater_id,
                show_date,
                show_time
            )
        )

        conn.commit()

        console.print(
            Panel(
                "[bold green]✅ Show added successfully.[/bold green]\n\n"
                f"[green]Movie : {movie_name}[/green]\n"
                f"[green]Start : "
                f"{new_start.strftime('%H:%M:%S')}[/green]\n"
                f"[green]End : "
                f"{new_end.strftime('%H:%M:%S')}[/green]",
                border_style="green"
            )
        )

    except ValueError:

        console.print(
            Panel(
                "[bold red]❌ Invalid date/time.[/bold red]\n\n"
                "[yellow]Date : YYYY-MM-DD[/yellow]\n"
                "[yellow]Time : HH:MM:SS[/yellow]",
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
            "\n[yellow]⚠️ Add show cancelled.[/yellow]"
        )

    except Exception as e:

        conn.rollback()

        console.print(
            Panel(
                f"[bold red]❌ Unexpected Error[/bold red]\n\n"
                f"[yellow]{e}[/yellow]",
                border_style="red"
            )
        )


# ==========================================================
# VIEW SHOWS
# ==========================================================

def view_shows():

    console.print(
        Panel(
            "[bold cyan]📋 SHOW LIST[/bold cyan]",
            border_style="cyan",
            box=box.DOUBLE
        )
    )

    try:

        cursor.execute(
            """
            SELECT
                s.show_id,
                m.movie_name,
                t.theater_name,
                s.show_date,
                s.show_time
            FROM shows s
            JOIN movies m
                ON s.movie_id = m.movie_id
            JOIN theaters t
                ON s.theater_id = t.theater_id
            ORDER BY s.show_date, s.show_time
            """
        )

        records = cursor.fetchall()

        if not records:

            console.print(
                Panel(
                    "[yellow]⚠️ No shows found.[/yellow]",
                    border_style="yellow"
                )
            )

            return

        table = Table(
            title="🎭 SHOWS",
            box=box.ROUNDED,
            border_style="cyan",
            show_lines=True
        )

        table.add_column("Show ID", justify="center")
        table.add_column("Movie")
        table.add_column("Theater")
        table.add_column("Date")
        table.add_column("Time")

        for row in records:

            table.add_row(
                str(row[0]),
                str(row[1]),
                str(row[2]),
                str(row[3]),
                str(row[4])
            )

        console.print(table)

    except mysql.connector.Error as e:

        console.print(
            Panel(
                f"[bold red]❌ Database Error[/bold red]\n\n{e}",
                border_style="red"
            )
        )

    except Exception as e:

        console.print(
            Panel(
                f"[bold red]❌ Error[/bold red]\n\n{e}",
                border_style="red"
            )
        )


# ==========================================================
# SEARCH SHOW
# ==========================================================

def search_show():

    console.print(
        Panel(
            "[bold cyan]🔍 SEARCH SHOW[/bold cyan]",
            border_style="cyan",
            box=box.DOUBLE
        )
    )

    try:

        show_id = int(
            console.input(
                "[bold green]Enter Show ID : [/bold green]"
            )
        )

        cursor.execute(
            """
            SELECT
                s.show_id,
                m.movie_name,
                t.theater_name,
                s.show_date,
                s.show_time
            FROM shows s
            JOIN movies m
                ON s.movie_id = m.movie_id
            JOIN theaters t
                ON s.theater_id = t.theater_id
            WHERE s.show_id = %s
            """,
            (show_id,)
        )

        row = cursor.fetchone()

        if not row:

            console.print(
                Panel(
                    "[bold red]❌ Show not found.[/bold red]",
                    border_style="red"
                )
            )

            return

        table = Table(
            title="🎭 SHOW DETAILS",
            box=box.ROUNDED,
            border_style="green"
        )

        table.add_column("Field", style="bold cyan")
        table.add_column("Value", style="bold white")

        table.add_row("Show ID", str(row[0]))
        table.add_row("Movie", str(row[1]))
        table.add_row("Theater", str(row[2]))
        table.add_row("Date", str(row[3]))
        table.add_row("Time", str(row[4]))

        console.print(table)

    except ValueError:

        console.print(
            Panel(
                "[bold red]❌ Show ID must be a number.[/bold red]",
                border_style="red"
            )
        )

    except mysql.connector.Error as e:

        console.print(
            Panel(
                f"[bold red]❌ Database Error[/bold red]\n\n{e}",
                border_style="red"
            )
        )

    except Exception as e:

        console.print(
            Panel(
                f"[bold red]❌ Error[/bold red]\n\n{e}",
                border_style="red"
            )
        )


# ==========================================================
# UPDATE SHOW
# ==========================================================

def update_show():

    console.print(
        Panel(
            "[bold cyan]✏️ UPDATE SHOW[/bold cyan]",
            border_style="cyan",
            box=box.DOUBLE
        )
    )

    try:

        show_id = int(
            console.input(
                "[bold green]Show ID : [/bold green]"
            )
        )

        cursor.execute(
            """
            SELECT show_id
            FROM shows
            WHERE show_id = %s
            """,
            (show_id,)
        )

        show = cursor.fetchone()

        if not show:

            console.print(
                Panel(
                    "[bold red]❌ Show not found.[/bold red]",
                    border_style="red"
                )
            )

            return

        movie_id = int(
            console.input(
                "[bold green]New Movie ID : [/bold green]"
            )
        )

        theater_id = int(
            console.input(
                "[bold green]New Theater ID : [/bold green]"
            )
        )

        show_date = console.input(
            "[bold green]New Date (YYYY-MM-DD) : [/bold green]"
        ).strip()

        show_time = console.input(
            "[bold green]New Time (HH:MM:SS) : [/bold green]"
        ).strip()

        new_start = datetime.strptime(
            show_date + " " + show_time,
            "%Y-%m-%d %H:%M:%S"
        )

        # CHECK MOVIE

        cursor.execute(
            """
            SELECT movie_name, duration
            FROM movies
            WHERE movie_id = %s
            """,
            (movie_id,)
        )

        movie = cursor.fetchone()

        if not movie:

            console.print(
                Panel(
                    "[bold red]❌ Movie ID not found.[/bold red]",
                    border_style="red"
                )
            )

            return

        duration = movie[1]

        new_end = new_start + timedelta(
            minutes=duration
        )

        # CHECK THEATER

        cursor.execute(
            """
            SELECT theater_id
            FROM theaters
            WHERE theater_id = %s
            """,
            (theater_id,)
        )

        theater = cursor.fetchone()

        if not theater:

            console.print(
                Panel(
                    "[bold red]❌ Theater ID not found.[/bold red]",
                    border_style="red"
                )
            )

            return

        # CHECK CONFLICT

        cursor.execute(
            """
            SELECT
                s.show_id,
                s.show_time,
                m.movie_name,
                m.duration
            FROM shows s
            JOIN movies m
                ON s.movie_id = m.movie_id
            WHERE s.theater_id = %s
            AND s.show_date = %s
            AND s.show_id != %s
            """,
            (
                theater_id,
                show_date,
                show_id
            )
        )

        existing_shows = cursor.fetchall()

        for existing in existing_shows:

            existing_time = str(existing[1]).split(".")[0]

            existing_start = datetime.strptime(
                show_date + " " + existing_time,
                "%Y-%m-%d %H:%M:%S"
            )

            existing_end = (
                existing_start
                + timedelta(minutes=existing[3])
            )

            if (
                new_start < existing_end
                and new_end > existing_start
            ):

                console.print(
                    Panel(
                        "[bold red]❌ SHOW TIMING CONFLICT![/bold red]\n\n"
                        f"Existing Movie : {existing[2]}\n"
                        f"Existing Start : "
                        f"{existing_start.strftime('%H:%M:%S')}\n"
                        f"Existing End : "
                        f"{existing_end.strftime('%H:%M:%S')}",
                        border_style="red"
                    )
                )

                return

        # UPDATE

        cursor.execute(
            """
            UPDATE shows
            SET
                movie_id = %s,
                theater_id = %s,
                show_date = %s,
                show_time = %s
            WHERE show_id = %s
            """,
            (
                movie_id,
                theater_id,
                show_date,
                show_time,
                show_id
            )
        )

        conn.commit()

        console.print(
            Panel(
                "[bold green]✅ Show updated successfully.[/bold green]",
                border_style="green"
            )
        )

    except ValueError:

        console.print(
            Panel(
                "[bold red]❌ Invalid input.[/bold red]",
                border_style="red"
            )
        )

    except mysql.connector.Error as e:

        conn.rollback()

        console.print(
            Panel(
                f"[bold red]❌ Database Error[/bold red]\n\n{e}",
                border_style="red"
            )
        )

    except KeyboardInterrupt:

        conn.rollback()

        console.print(
            "\n[yellow]⚠️ Update show cancelled.[/yellow]"
        )

    except Exception as e:

        conn.rollback()

        console.print(
            Panel(
                f"[bold red]❌ Error[/bold red]\n\n{e}",
                border_style="red"
            )
        )


# ==========================================================
# DELETE SHOW
# ==========================================================

def delete_show():

    console.print(
        Panel(
            "[bold red]🗑️ DELETE SHOW[/bold red]",
            border_style="red",
            box=box.DOUBLE
        )
    )

    try:

        show_id = int(
            console.input(
                "[bold green]Enter Show ID : [/bold green]"
            )
        )

        # --------------------------------------------------
        # CHECK SHOW
        # --------------------------------------------------

        cursor.execute(
            """
            SELECT
                s.show_id,
                m.movie_name,
                t.theater_name,
                s.show_date,
                s.show_time
            FROM shows s
            JOIN movies m
                ON s.movie_id = m.movie_id
            JOIN theaters t
                ON s.theater_id = t.theater_id
            WHERE s.show_id = %s
            """,
            (show_id,)
        )

        show = cursor.fetchone()

        if not show:

            console.print(
                Panel(
                    "[bold red]❌ Show not found.[/bold red]",
                    border_style="red"
                )
            )

            return

        # --------------------------------------------------
        # SHOW DETAILS
        # --------------------------------------------------

        table = Table(
            title="🎭 SHOW DETAILS",
            box=box.ROUNDED,
            border_style="yellow"
        )

        table.add_column("Field", style="bold cyan")
        table.add_column("Value", style="bold white")

        table.add_row("Show ID", str(show[0]))
        table.add_row("Movie", str(show[1]))
        table.add_row("Theater", str(show[2]))
        table.add_row("Date", str(show[3]))
        table.add_row("Time", str(show[4]))

        console.print(table)

        # --------------------------------------------------
        # CHECK TICKETS
        # --------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM tickets
            WHERE show_id = %s
            """,
            (show_id,)
        )

        ticket_count = cursor.fetchone()[0]

        if ticket_count > 0:

            console.print(
                Panel(
                    f"[bold yellow]⚠️ {ticket_count} ticket(s) "
                    "are associated with this show.[/bold yellow]\n\n"
                    "[yellow]These tickets will also be deleted "
                    "automatically.[/yellow]",
                    border_style="yellow"
                )
            )

        # --------------------------------------------------
        # CONFIRM
        # --------------------------------------------------

        confirm = console.input(
            "\n[bold red]Are you sure you want to delete "
            "this show? (Y/N) : [/bold red]"
        ).strip().lower()

        if confirm != "y":

            console.print(
                Panel(
                    "[yellow]❌ Show deletion cancelled.[/yellow]",
                    border_style="yellow"
                )
            )

            return

        # --------------------------------------------------
        # DELETE SHOW
        # --------------------------------------------------

        cursor.execute(
            """
            DELETE FROM shows
            WHERE show_id = %s
            """,
            (show_id,)
        )

        conn.commit()

        console.print(
            Panel(
                "[bold green]✅ Show deleted successfully.[/bold green]\n\n"
                "[green]Related tickets were also deleted automatically.[/green]",
                border_style="green",
                box=box.DOUBLE
            )
        )

    except ValueError:

        console.print(
            Panel(
                "[bold red]❌ Invalid Show ID[/bold red]\n\n"
                "[yellow]Show ID must be a number.[/yellow]",
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
            "\n[yellow]⚠️ Show deletion interrupted.[/yellow]"
        )

    except Exception as e:

        conn.rollback()

        console.print(
            Panel(
                f"[bold red]❌ Unexpected Error[/bold red]\n\n"
                f"[yellow]{e}[/yellow]",
                border_style="red"
            )
        )