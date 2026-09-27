"""Module d'affichage de console et export des résultats """

import json
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
    
def export_to_json(
    results: list[dict],
    metadata: dict,
    filepath: str,
) -> None:
    payload = {
        "scan": metadata,
        "summary": {
            "total_ports": metadata.get("total_ports", 0),
            "open_ports": len(results),
        },
        "results": results,
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"\n[+] Résultats exportés dans : {filepath}")