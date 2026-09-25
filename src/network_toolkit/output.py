"""Module d'affichage de console et export des résultats """

from datetime import datetime

def print_result(result: dict) -> None:
    if result is None:
        return
    port = result["port"]
    proto = result["protocol"]
    state = result["state"]
    banner = result.get("banner", "")
    if banner:
        print(f"Port {proto} {port:5} : [{state}] | Banner: {banner}")
    else:
        print(f"Port {proto} {port:5} : [{state}]")

def print_summary(start: datetime, end: datetime, total: int, open_count: int) -> None:
    duration = end - start
    print(f"\n[+] Scan terminé en {duration}")
    print(f"[+] {open_count} port(s) ouvert(s) sur {total} analysé(s).")
    