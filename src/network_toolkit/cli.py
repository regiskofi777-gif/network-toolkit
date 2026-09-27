"""Interface en ligne de commande"""

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from network_toolkit.scanner import scan_tcp_port, scan_udp_port
from network_toolkit.validation import (
    ValidationError,
    parse_port_range,
    resolve_target,
    validate_threads,
)
from network_toolkit.output import print_result, print_summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog = "network_toolkit",
        description = "Scanner de ports TCP/UDP - usage autorisé uniquement.",
    )
    parser.add_argument(
        "-t", "--target",
        required = True,
        help = "Adresse IP ou nom d'hôte à scanner.",
    )
    parser.add_argument(
        "-p", "--ports",
        required = True,
        help = "Plage de ports au format 'début-fin' (ex:20-100)."
    )
    parser.add_argument(
        "-T", "--threads",
        type = int,
        default = 100,
        help = "Nombre de workers (1-500, par défaut:100)."
    )
    parser.add_argument(
        "-o", "--output",
        default = None,
        help = "Fichier JSON de sortie (optionnel).",
    )
    parser.add_argument(
        "--protocol",
        choices = ["tcp", "udp"],
        default = "tcp",
        help = "Protocole à scanner (par défaut : tcp).",
    )
    return parser

def run() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        target = resolve_target(args.target)
        start, end = parse_port_range(args.ports)
        validate_threads(args.threads)
    except ValidationError as e:
        print(f"[-] Erreur de validation : {e}", file=sys.stderr)
        return 1

    port_list = range(start, end + 1)
    scan_function = scan_tcp_port if args.protocol == "tcp" else scan_udp_port

    print(f"[+] Cible : {target}")
    print(f"[+] Protocole : {args.protocol.upper()}")
    print(f"[+] Ports : {start}-{end} ({len(port_list)} ports)")
    print(f"[+] Workers : {args.threads}")
    print("\nAnalyse en cours...\n")

    start_time = datetime.now()
    results = []

    try:
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            for result in executor.map(lambda p: scan_function(target, p), port_list):
                if result is not None:
                    results.append(result)
                    print_result(result)
    except KeyboardInterrupt:
        print("\n[-] Scan interrompu par l'utilisateur.", file=sys.stderr)
        return 130
    end_time = datetime.now()
    print_summary(start_time, end_time, len(port_list), len(results))

    return 0