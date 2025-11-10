import asyncio
import time
import sys


from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table
from rich import box
from rich.style import Style as RichStyle
from colorama import Fore, Back, Style as ColoramaStyle


from config import PROXY_SOURCES, OUTPUT_FILE, CONCURRENT_CHECKS, TIMEOUT
from fetcher import fetch_all_sources
from patterns import extract_proxies
from checker import check_proxy
from storage import save_proxies

console = Console()


def print_banner() -> None:
    art = Fore.CYAN + r"""8888888b.  8888888b.   .d88888b.  Y88b   d88P Y88b   d88P  88888888888  .d88888b.   .d88888b.  888      
888   Y88b 888   Y88b d88P' 'Y88b  Y88b d88P   Y88b d88P       888     d88P' 'Y88b d88P' 'Y88b 888      
888    888 888    888 888     888   Y88o88P     Y88o88P        888     888     888 888     888 888      
888   d88P 888   d88P 888     888    Y888P       Y888P         888     888     888 888     888 888      
8888888P'  8888888P'  888     888    d888b        888          888     888     888 888     888 888      
888        888 T88b   888     888   d88888b       888          888     888     888 888     888 888      
888        888  T88b  Y88b. .d88P  d88P Y88b      888          888     Y88b. .d88P Y88b. .d88P 888      
888        888   T88b  'Y88888P'  d88P   Y88b     888          888      'Y88888P'   'Y88888P'  88888888 
                                                                                                        
                                                                                                        
                                                                                                        """
    print(art)


def create_stats_table(total: int, checked: int, alive: int, elapsed: float) -> Table:
    table = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
    table.add_column(style="cyan bold", width=16)
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


async def check_proxies_with_progress(proxies: set[str]) -> list[str]:
    semaphore = asyncio.Semaphore(CONCURRENT_CHECKS)
    tasks = [check_proxy(proxy, semaphore) for proxy in proxies]

    results: list[str] = []
    total = len(tasks)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("•"),
        TextColumn("[cyan]{task.completed}/{task.total}"),
        TextColumn("•"),
        TextColumn("[green]✓ {task.fields[alive]} alive"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        task_id = progress.add_task(
            "[cyan]Checking proxies...",
            total=total,
            alive=0,
        )

        for coro in asyncio.as_completed(tasks):
            try:
                proxy, is_alive = await coro
                if is_alive:
                    results.append(proxy)
                    progress.update(task_id, advance=1, alive=len(results))
                else:
                    progress.update(task_id, advance=1)
            except Exception as e:
                error_msg = f"[red]Error checking proxy: {e}"
                console.log(error_msg)
                progress.update(task_id, advance=1)

    return results


async def main() -> None:
    print_banner()

    if not PROXY_SOURCES:
        console.print(
            Panel.fit(
                "[red]✗ No proxy sources configured in config.PROXY_SOURCES",
                border_style="red",
                title="❌ Configuration Error",
            )
        )
        return

    console.print(
        Panel.fit(
            f"[yellow]Sources:[/yellow] {len(PROXY_SOURCES)} • "
            f"[yellow]Concurrency:[/yellow] {CONCURRENT_CHECKS} • "
            f"[yellow]Timeout:[/yellow] {TIMEOUT}s • "
            f"[yellow]Output:[/yellow] {OUTPUT_FILE}",
            border_style="blue",
            title="⚙️ Configuration",
            padding=(0, 1),
        )
    )
    console.print()

    start_time = time.time()


    with console.status("[bold blue]Fetching proxy sources...", spinner="aesthetic"):
        try:
            raw_text = await fetch_all_sources(PROXY_SOURCES)
        except Exception as e:
            console.print(
                Panel(
                    f"[red]✗ Fetch failed: {e}",
                    border_style="red",
                    title="❌ Fetch Error",
                )
            )
            return

    console.print("[green]✓[/green] Fetched proxy sources")


    with console.status("[bold blue]Parsing proxies...", spinner="dots"):
        proxies = extract_proxies(raw_text)

    console.print(f"[green]✓[/green] Parsed [yellow]{len(proxies):,}[/yellow] unique valid proxies")
    console.print()

    if not proxies:
        console.print(
            Panel(
                "[red]✗ No proxies found. Exiting.[/red]",
                border_style="red",
                title="❌ No Proxies",
            )
        )
        return


    live_proxies = await check_proxies_with_progress(proxies)


    elapsed = time.time() - start_time


    console.print()
    stats_table = create_stats_table(
        total=len(proxies),
        checked=len(proxies),
        alive=len(live_proxies),
        elapsed=elapsed,
    )
    console.print(
        Panel(
            stats_table,
            border_style="green",
            title="📊 Results",
            padding=(1, 2),
        )
    )


    console.print()
    with console.status(f"[bold blue]Saving to {OUTPUT_FILE}...", spinner="dots"):
        try:
            save_proxies(live_proxies, OUTPUT_FILE)
        except Exception as e:
            console.print(
                Panel(
                    f"[red]✗ Save failed: {e}",
                    border_style="red",
                    title="❌ Save Error",
                )
            )
            return


    console.print(
        Panel.fit(
            f"[green]✓[/green] Saved [bold green]{len(live_proxies):,}[/bold green] live proxies to [cyan]{OUTPUT_FILE}[/cyan]",
            border_style="green",
            title="✅ Success",
            padding=(1, 2),
        )
    )

    console.print(
        Panel.fit(
            "[bold green]✨ Process completed successfully![/bold green]\n"
            "[dim]Press Ctrl+C to exit[/dim]",
            border_style="green",
            padding=(1, 2),
        )
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Interrupted by user. Exiting...[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(Panel(f"[red]_fatal error:[/red] {e}", title="💥 Crash", border_style="red"))
        sys.exit(1)
