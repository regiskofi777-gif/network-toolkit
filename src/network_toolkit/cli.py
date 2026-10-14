"""Interface en ligne de commande"""

from network_toolkit.logger import setup_logger 
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
from network_toolkit.output import print_result, print_summary, export_to_json


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
    logger = setup_logger()
    parser = build_parser()
    args = parser.parse_args()
    try:
        target = resolve_target(args.target)
        start, end = parse_port_range(args.ports)
        validate_threads(args.threads)
    except ValidationError as e:
        logger.error("Erreur de validation : %s", e)
        return 1

    port_list = range(start, end + 1)
    scan_function = scan_tcp_port if args.protocol == "tcp" else scan_udp_port

    logger.info("Cible : %s", target)
    logger.info("Protocole : %s", args.protocol.upper())
    logger.info("Ports : %d-%d (%d ports)", start, end, len(port_list))
    logger.info("Workers : %d", args.threads)

    start_time = datetime.now()
    results = []

    try:
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            for result in executor.map(lambda p: scan_function(target, p), port_list):
                if result is not None:
                    results.append(result)
                    print_result(result)
    except KeyboardInterrupt:
        logger.warning("Scan interrompu par l'utilisateur.")
        return 130
    end_time = datetime.now()
    print_summary(start_time, end_time, len(port_list), len(results))

    if args.output:
        metadata = {
            "target": target,
            "protocol": args.protocol,
            "port_range": f"{start}-{end}",
            "threads": args.threads,
            "started_at": start_time.isoformat(),
            "finished_at": end_time.isoformat(),
            "duration_seconds": round((end_time - start_time).total_seconds(), 3),
            "total_ports": len(port_list),
        }
        try:
            export_to_json(results, metadata, args.output)
        except OSError as e:
            logger.error("Impossible d'ecrire dans le fichier : %s", e)
            return 1

    return 0