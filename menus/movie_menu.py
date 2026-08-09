from services.movie_management import (
    add_movie,
    view_movies,
    search_movie,
    update_movie,
    delete_movie
)

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box


console = Console()


# ==========================================================
# MOVIE MANAGEMENT MENU
# ==========================================================

def movie_menu():

    while True:

        try:

            console.clear()

            # --------------------------------------------------
            # HEADER
            # --------------------------------------------------

            console.print(
                Panel(
                    "[bold cyan]🎬 MOVIE MANAGEMENT[/bold cyan]",
                    border_style="cyan",
                    box=box.DOUBLE
                )
            )

            # --------------------------------------------------
            # MENU TABLE
            # --------------------------------------------------

            table = Table(
                title="MOVIE MENU",
                box=box.ROUNDED,
                border_style="blue",
                show_lines=True
            )

            table.add_column(
                "Option",
                justify="center",
                style="bold yellow"
            )

            table.add_column(
                "Operation",
                style="bold white"
            )

            table.add_row(
                "1",
                "➕ Add Movie"
            )

            table.add_row(
                "2",
                "📋 View Movies"
            )

            table.add_row(
                "3",
                "🔍 Search Movie"
            )

            table.add_row(
                "4",
                "✏️ Update Movie"
            )

            table.add_row(
                "5",
                "🗑️ Delete Movie"
            )

            table.add_row(
                "6",
                "⬅️ Back"
            )

            console.print(table)

            # --------------------------------------------------
            # USER INPUT
            # --------------------------------------------------

            choice = console.input(
                "\n[bold green]Enter Choice : [/bold green]"
            ).strip()

            # --------------------------------------------------
            # ADD MOVIE
            # --------------------------------------------------

            if choice == "1":

                try:

                    add_movie()

                except Exception as e:

                    console.print(
                        Panel(
                            f"[bold red]❌ Add Movie Error[/bold red]\n\n"
                            f"[yellow]{e}[/yellow]",
                            border_style="red"
                        )
                    )

                console.input(
                    "\n[cyan]Press Enter to continue...[/cyan]"
                )

            # --------------------------------------------------
            # VIEW MOVIES
            # --------------------------------------------------

            elif choice == "2":

                try:

                    view_movies()

                except Exception as e:

                    console.print(
                        Panel(
                            f"[bold red]❌ View Movies Error[/bold red]\n\n"
                            f"[yellow]{e}[/yellow]",
                            border_style="red"
                        )
                    )

                console.input(
                    "\n[cyan]Press Enter to continue...[/cyan]"
                )

            # --------------------------------------------------
            # SEARCH MOVIE
            # --------------------------------------------------

            elif choice == "3":

                try:

                    search_movie()

                except Exception as e:

                    console.print(
                        Panel(
                            f"[bold red]❌ Search Movie Error[/bold red]\n\n"
                            f"[yellow]{e}[/yellow]",
                            border_style="red"
                        )
                    )

                console.input(
                    "\n[cyan]Press Enter to continue...[/cyan]"
                )

            # --------------------------------------------------
            # UPDATE MOVIE
            # --------------------------------------------------

            elif choice == "4":

                try:

                    update_movie()

                except Exception as e:

                    console.print(
                        Panel(
                            f"[bold red]❌ Update Movie Error[/bold red]\n\n"
                            f"[yellow]{e}[/yellow]",
                            border_style="red"
                        )
                    )

                console.input(
                    "\n[cyan]Press Enter to continue...[/cyan]"
                )

            # --------------------------------------------------
            # DELETE MOVIE
            # --------------------------------------------------

            elif choice == "5":

                try:

                    delete_movie()

                except Exception as e:

                    console.print(
                        Panel(
                            f"[bold red]❌ Delete Movie Error[/bold red]\n\n"
                            f"[yellow]{e}[/yellow]",
                            border_style="red"
                        )
                    )

                console.input(
                    "\n[cyan]Press Enter to continue...[/cyan]"
                )

            # --------------------------------------------------
            # BACK
            # --------------------------------------------------

            elif choice == "6":

                console.print(
                    "[bold yellow]⬅️ Returning to Main Menu...[/bold yellow]"
                )

                break

            # --------------------------------------------------
            # INVALID CHOICE
            # --------------------------------------------------

            else:

                console.print(
                    Panel(
                        "[bold red]❌ Invalid Choice![/bold red]\n\n"
                        "[yellow]Please enter a number from 1 to 6.[/yellow]",
                        border_style="red"
                    )
                )

                console.input(
                    "\n[cyan]Press Enter to continue...[/cyan]"
                )

        # ======================================================
        # KEYBOARD INTERRUPT
        # ======================================================

        except KeyboardInterrupt:

            console.print(
                Panel(
                    "[bold yellow]⚠️ Movie Management interrupted.[/bold yellow]\n\n"
                    "[yellow]Returning to Main Menu...[/yellow]",
                    border_style="yellow"
                )
            )

            break

        # ======================================================
        # UNEXPECTED ERROR
        # ======================================================

        except Exception as e:

            console.print(
                Panel(
                    f"[bold red]❌ Unexpected Error[/bold red]\n\n"
                    f"[yellow]{e}[/yellow]",
                    border_style="red"
                )
            )

            console.input(
                "\n[cyan]Press Enter to continue...[/cyan]"
            )