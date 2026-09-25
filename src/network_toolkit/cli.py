"""Interface en ligne de commande"""
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from network_toolkit.scanner import scan_tcp_port, scan_udp_port
from network_toolkit.validation import resolve_target, validate_port_range
from network_toolkit.output import print_result, print_summary


def ask_target() -> str:
    hostname = input("Entrez votre hostname ou adresse IP :")
    return resolve_target(hostname)

def ask_scan_type() -> str:
    choice = input("Entrez votre choix [1 - TCP] ou [2 - UDP] :")
    if choice not in ("1", "2"):
        print("[-] Choix invalide, Sortir du script.")
        sys.exit(1)
    return choice

def ask_port_range() -> range:
    try:
        start = int(input("Port de debut (ex: 20) : "))
        end = int(input("Port de fin (ex: 100) : "))
    except ValueError:
        Print("[-] Veuillez entrer des nombres entiers.")
        sys.exit(1)
    validate_port_range(start, end)
    return range(start, end + 1)

def run() -> None:
    """Execution du scanner"""
    try:
        target = ask_target()
        scan_type = ask_scan_type()
        port_list = ask_port_range()

        scan_function = scan_tcp_port if scan_type == "1" else scan_udp_port
        start_time = datetime.now()
        results = []

        print("\nAnalyse en cours...")

        with ThreadPoolExecutor(max_workers=100) as executor:
            for result in executor.map(lambda p: scan_function(target, p), port_list):
                if result is not None: 
                    results.append(result)
                    print_result(result)
            
        end_time = datetime.now()
        print_summary(start_time, end_time, len(port_list), len(results))

    except KeyboardInterrupt:
        print("\n[-] Scan interrompu par l'utilisateur.")
        sys.exit(130)
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        sys.exit(1)
