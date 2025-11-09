import asyncio
import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich import box

from config import PROXY_SOURCES, OUTPUT_FILE, CONCURRENT_CHECKS, TIMEOUT
from fetcher import fetch_all_sources
from patterns import extract_proxies
from checker import check_proxy
from storage import save_proxies

console = Console()

BANNER = """
[cyan]╔═════════════════════════════════════════════════════╗
║                                                           ║
║   ███████╗ ██████╗  ██████╗██╗  ██╗███████╗███████╗       ║
║   ██╔════╝██╔═══██╗██╔════╝██║ ██╔╝██╔════╝██╔════╝       ║
║   ███████╗██║   ██║██║     █████╔╝ ███████╗███████╗       ║
║   ╚════██║██║   ██║██║     ██╔═██╗ ╚════██║╚════██║       ║
║   ███████║╚██████╔╝╚██████╗██║  ██╗███████║███████║       ║
║   ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝       ║
║                                                           ║
║         [bold yellow]Proxy Parser & Checker[/bold yellow] ║
║              [dim]High-Performance Async Tool[/dim]       ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝[/cyan]
"""

def print_banner():
    console.print(BANNER)
    console.print()


def create_stats_table(total: int, checked: int, alive: int, elapsed: float) -> Table:
    table = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
    table.add_column(style="cyan bold")
    table.add_column(style="white")
    
    table.add_row("📊 Total Proxies", f"{total:,}")
    table.add_row("✅ Checked", f"{checked:,}")
    table.add_row("🟢 Alive", f"[green]{alive:,}[/green]")
    table.add_row("⏱️  Elapsed Time", f"{elapsed:.1f}s")
    
    if checked > 0:
        success_rate = (alive / checked) * 100
        speed = checked / elapsed if elapsed > 0 else 0
        table.add_row("📈 Success Rate", f"[yellow]{success_rate:.2f}%[/yellow]")
        table.add_row("⚡ Speed", f"[magenta]{speed:.0f} checks/s[/magenta]")
    
    return table


async def check_proxies_with_progress(proxies: set) -> list:
    semaphore = asyncio.Semaphore(CONCURRENT_CHECKS)
    tasks = [check_proxy(proxy, semaphore) for proxy in proxies]
    
    results = []
    total = len(tasks)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("•"),
        TextColumn("[cyan]{task.completed}/{task.total}"),
        TextColumn("•"),
        TextColumn("[green]✓ {task.fields[alive]}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        
        task = progress.add_task(
            "[cyan]Checking proxies...",
            total=total,
            alive=0
        )
        
        for coro in asyncio.as_completed(tasks):
            proxy, is_alive = await coro
            
            if is_alive:
                results.append(proxy)
                progress.update(task, advance=1, alive=len(results))
            else:
                progress.update(task, advance=1)
    
    return results


async def main():
    print_banner()
    
    console.print(Panel.fit(
        f"[yellow]Sources:[/yellow] {len(PROXY_SOURCES)} | "
        f"[yellow]Concurrent:[/yellow] {CONCURRENT_CHECKS} | "
        f"[yellow]Timeout:[/yellow] {TIMEOUT}s",
        border_style="cyan",
        title="⚙️  Configuration"
    ))
    console.print()
    
    start_time = time.time()
    
    with console.status("[bold cyan]Fetching proxies from sources...", spinner="dots"):
        raw_text = await fetch_all_sources(PROXY_SOURCES)
    
    console.print("[green]✓[/green] Fetched proxy sources")
    
    with console.status("[bold cyan]Parsing proxies...", spinner="dots"):
        proxies = extract_proxies(raw_text)
    
    console.print(f"[green]✓[/green] Parsed [yellow]{len(proxies):,}[/yellow] unique valid proxies")
    console.print()
    
    if not proxies:
        console.print("[red]✗ No proxies found. Exiting.[/red]")
        return
    
    live_proxies = await check_proxies_with_progress(proxies)
    
    console.print()
    elapsed = time.time() - start_time
    
    stats_table = create_stats_table(len(proxies), len(proxies), len(live_proxies), elapsed)
    console.print(Panel(stats_table, border_style="green", title="📊 Results"))
    
    console.print()
    with console.status(f"[bold cyan]Saving to {OUTPUT_FILE}...", spinner="dots"):
        save_proxies(live_proxies, OUTPUT_FILE)
    
    console.print(f"[green]✓[/green] Saved [yellow]{len(live_proxies):,}[/yellow] live proxies to [cyan]{OUTPUT_FILE}[/cyan]")
    console.print()
    console.print(Panel.fit(
        "[bold green]✨ Process completed successfully![/bold green]",
        border_style="green"
    ))


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Process interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]✗ Error: {e}[/red]")
  
