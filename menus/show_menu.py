from services.show_management import (
    add_show,
    view_shows,
    search_show,
    update_show,
    delete_show
)

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box


console = Console()


# ==========================================================
# SHOW MANAGEMENT MENU
# ==========================================================

def show_menu():

    while True:

        try:

            console.clear()

            # --------------------------------------------------
            # HEADER
            # --------------------------------------------------

            console.print(
                Panel(
                    "[bold cyan]🎭 SHOW MANAGEMENT[/bold cyan]",
                    border_style="cyan",
                    box=box.DOUBLE
                )
            )

            # --------------------------------------------------
            # MENU TABLE
            # --------------------------------------------------

            table = Table(
                title="SHOW MENU",
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
                "➕ Add Show"
            )

            table.add_row(
                "2",
                "📋 View Shows"
            )

            table.add_row(
                "3",
                "🔍 Search Show"
            )

            table.add_row(
                "4",
                "✏️ Update Show"
            )

            table.add_row(
                "5",
                "🗑️ Delete Show"
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
            # ADD SHOW
            # --------------------------------------------------

            if choice == "1":

                try:

                    add_show()

                except Exception as e:

                    console.print(
                        Panel(
                            f"[bold red]❌ Add Show Error[/bold red]\n\n"
                            f"[yellow]{e}[/yellow]",
                            border_style="red"
                        )
                    )

                console.input(
                    "\n[cyan]Press Enter to continue...[/cyan]"
                )

            # --------------------------------------------------
            # VIEW SHOWS
            # --------------------------------------------------

            elif choice == "2":

                try:

                    view_shows()

                except Exception as e:

                    console.print(
                        Panel(
                            f"[bold red]❌ View Shows Error[/bold red]\n\n"
                            f"[yellow]{e}[/yellow]",
                            border_style="red"
                        )
                    )

                console.input(
                    "\n[cyan]Press Enter to continue...[/cyan]"
                )

            # --------------------------------------------------
            # SEARCH SHOW
            # --------------------------------------------------

            elif choice == "3":

                try:

                    search_show()

                except Exception as e:

                    console.print(
                        Panel(
                            f"[bold red]❌ Search Show Error[/bold red]\n\n"
                            f"[yellow]{e}[/yellow]",
                            border_style="red"
                        )
                    )

                console.input(
                    "\n[cyan]Press Enter to continue...[/cyan]"
                )

            # --------------------------------------------------
            # UPDATE SHOW
            # --------------------------------------------------

            elif choice == "4":

                try:

                    update_show()

                except Exception as e:

                    console.print(
                        Panel(
                            f"[bold red]❌ Update Show Error[/bold red]\n\n"
                            f"[yellow]{e}[/yellow]",
                            border_style="red"
                        )
                    )

                console.input(
                    "\n[cyan]Press Enter to continue...[/cyan]"
                )

            # --------------------------------------------------
            # DELETE SHOW
            # --------------------------------------------------

            elif choice == "5":

                try:

                    delete_show()

                except Exception as e:

                    console.print(
                        Panel(
                            f"[bold red]❌ Delete Show Error[/bold red]\n\n"
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
                    Panel(
                        "[bold yellow]⬅️ Returning to Main Menu...[/bold yellow]",
                        border_style="yellow"
                    )
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
                    "[bold yellow]⚠️ Show Management interrupted.[/bold yellow]\n\n"
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