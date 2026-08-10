from services.ticket_cancellation_service import view_tickets, search_ticket, cancel_ticket, view_cancelled_tickets
from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.table import Table

console = Console()

def ticket_menu():
    while True:
        try:
            console.print(Panel("[bold cyan]🎟️ TICKET MANAGEMENT[/bold cyan]", border_style="cyan", box=box.DOUBLE))
            table = Table(title="TICKET MENU", box=box.ROUNDED, border_style="cyan")
            table.add_column("Option", justify="center", style="bold yellow")
            table.add_column("Operation", style="bold white")
            
            table.add_row("1", "📋 View Active Tickets")
            table.add_row("2", "🔍 Search Ticket")
            table.add_row("3", "❌ Cancel Ticket")
            table.add_row("4", "📂 View Cancelled Tickets")
            table.add_row("5", "⬅️ Back")
            console.print(table)
            
            choice = console.input("\n[bold green]Enter Choice : [/bold green]").strip()

            if choice == "1": view_tickets()
            elif choice == "2": search_ticket()
            elif choice == "3": cancel_ticket()
            elif choice == "4": view_cancelled_tickets()
            elif choice == "5": break
            else:
                console.print(Panel("[bold red]❌ Invalid Choice![/bold red]\n\n[yellow]Please enter a number from 1 to 5.[/yellow]", border_style="red"))
        except KeyboardInterrupt:
            console.print("\n[yellow]⚠️ Returning to previous menu...[/yellow]")
            break
        except Exception as e:
            console.print(Panel(f"[bold red]❌ Unexpected Error[/bold red]\n\n[yellow]{e}[/yellow]", border_style="red"))