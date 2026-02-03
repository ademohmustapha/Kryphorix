from core.report import generate_pdf, export_json
from plugins.plugin_loader import load_plugins
import argparse, sys

from modules.web import web_scan
from modules.api import api_scan
from modules.ad import ad_scan
from modules.ports import port_scan
from modules.tls import tls_check
from modules.wireless import wireless_scan

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TimeRemainingColumn, TextColumn
from rich.live import Live

console = Console()

# =========================
# Banner
# =========================
def banner():
    """
    Displays the banner for the Kryphorix Cyber Defense Suite.
    This function prints the welcome message to the user.
    """
    console.print("\n🛡 [bold cyan]KRYPhorix Cyber Defense Suite[/bold cyan]", justify="center")
    console.print("[bold white]Advanced Security Assessment Framework[/bold white]\n", justify="center")

# =========================
# Tag findings with module
# =========================
def tag_module(findings, module_name):
    """
    Tags each finding with the module name.
    
    Args:
        findings (list): List of findings to tag.
        module_name (str): The name of the module.

    Returns:
        list: Tagged findings.
    """
    for f in findings:
        f.module = module_name
    return findings

# =========================
# Display summary table
# =========================
def display_summary(findings):
    """
    Displays a summary table of the scan findings.
    
    Args:
        findings (list): The list of findings to display.
    """
    if not findings:
        console.print("[bold green]No vulnerabilities found![/bold green]\n")
        return

    severity_order = {"Critical": 5, "High": 4, "Medium": 3, "Low": 2, "Info": 1}
    findings_sorted = sorted(findings, key=lambda f: severity_order.get(f.severity, 0), reverse=True)

    table = Table(title="Scan Summary", show_lines=True)
    table.add_column("Module", style="bold")
    table.add_column("Title", style="bold")
    table.add_column("Severity")
    table.add_column("Description")
    table.add_column("Fix / Recommendation")

    severity_colors = {
        "Info": "blue",
        "Low": "green",
        "Medium": "yellow",
        "High": "red",
        "Critical": "dark_red"
    }

    for f in findings_sorted:
        table.add_row(
            getattr(f, "module", "Unknown"),
            f.title,
            f"[{severity_colors.get(f.severity, 'white')}]${f.severity}[/{severity_colors.get(f.severity, 'white')}]",
            f.desc,
            f.fix
        )

    console.print(table)

# =========================
# Run a module on multiple targets
# =========================
def run_module(module_name, func, targets):
    """
    Runs a module on multiple targets.
    
    Args:
        module_name (str): The name of the scan module.
        func (function): The scanning function.
        targets (list): List of targets to scan.
    
    Returns:
        list: Results from the scan.
    """
    results = []
    for t in targets:
        try:
            res = func(t)
            results += tag_module(res, module_name)
        except Exception as e:
            console.print(f"[red]Error scanning {t}: {e}[/red]")
    return results

# =========================
# Parse comma-separated targets
# =========================
def parse_targets(value):
    """
    Parses a comma-separated list of targets into a list.
    
    Args:
        value (str): The comma-separated targets string.
    
    Returns:
        list: List of individual targets.
    """
    return [v.strip() for v in value.split(",") if v.strip()]

# =========================
# CLI Mode
# =========================
def cli_mode(args):
    """
    Executes the scan modules based on the command-line arguments.
    
    Args:
        args: The parsed command-line arguments.
    """
    findings = []

    if args.web:
        findings += run_module("Web", web_scan, parse_targets(args.web))
    if args.api:
        findings += run_module("API", api_scan, parse_targets(args.api))
    if args.ad:
        findings += run_module("AD", ad_scan, parse_targets(args.ad))
    if args.ports:
        findings += run_module("Ports", port_scan, parse_targets(args.ports))
    if args.tls:
        findings += run_module("TLS", tls_check, parse_targets(args.tls))
    if args.wifi:
        findings += run_module("Wireless", wireless_scan, ["local"])

    # Run plugins
    for plugin in load_plugins():
        plugin_results = plugin()
        findings += tag_module(plugin_results, "Plugin")

    # Display summary & generate reports
    display_summary(findings)
    if findings:
        generate_pdf(findings)
        export_json(findings)

# =========================
# Argument Parser
# =========================
def parse_args():
    """
    Parses the command-line arguments.
    
    Returns:
        Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="KryPhorix Security Framework")
    parser.add_argument("--web", help="Scan web URLs (comma-separated)")
    parser.add_argument("--api", help="Scan API endpoints (comma-separated)")
    parser.add_argument("--ad", help="Scan Active Directory hosts (comma-separated)")
    parser.add_argument("--ports", help="Scan open ports (comma-separated)")
    parser.add_argument("--tls", help="Check TLS/SSL hosts (comma-separated)")
    parser.add_argument("--wifi", action="store_true", help="Scan available Wi-Fi networks")
    return parser.parse_args()

# =========================
# Menu Mode
# =========================
def menu_mode():
    """
    Provides an interactive menu for the user to select which module to scan.
    """
    banner()
    console.print(Panel(
        "[bold]Menu Mode[/bold]\n"
        "Select a module to scan:\n"
        "1. Web\n"
        "2. API\n"
        "3. Active Directory\n"
        "4. Ports\n"
        "5. TLS/SSL\n"
        "6. Wireless\n"
        "0. Exit"
    ))

    choice = input("Enter your choice (0-6): ")

    if choice == "1":
        url = input("Enter web URL to scan: ")
        findings = run_module("Web", web_scan, [url])
        display_summary(findings)
    elif choice == "2":
        api_url = input("Enter API URL to scan: ")
        findings = run_module("API", api_scan, [api_url])
        display_summary(findings)
    elif choice == "3":
        ad_host = input("Enter Active Directory host to scan: ")
        findings = run_module("AD", ad_scan, [ad_host])
        display_summary(findings)
    elif choice == "4":
        ports = input("Enter IP addresses or ranges to scan (comma-separated): ")
        findings = run_module("Ports", port_scan, parse_targets(ports))
        display_summary(findings)
    elif choice == "5":
        tls_host = input("Enter host to check TLS/SSL: ")
        findings = run_module("TLS", tls_check, [tls_host])
        display_summary(findings)
    elif choice == "6":
        findings = run_module("Wireless", wireless_scan, ["local"])
        display_summary(findings)
    elif choice == "0":
        console.print("[bold green]Exiting...[/bold green]")
        exit()
    else:
        console.print("[bold red]Invalid choice! Please enter a valid number from 0 to 6.[/bold red]")

# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    args = parse_args()
    banner()
    if len(sys.argv) == 1:
        menu_mode()
    else:
        cli_mode(args)

