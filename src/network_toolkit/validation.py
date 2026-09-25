"""Vérification des saisies utilisateur"""

import socket
import sys


def resolve_target(hostname: str) -> str:

    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        print(f"[-] Impossible de résoudre '{hostname}'. Vérifiez l'adresse. ")
        sys.exit(1)


def validate_port_range(start: int, end: int) -> None:
    if not (1 <= start <= 65535) or not (1 <= end <= 65535):
        print("[-] Les ports doivent être entre 1 et 65535.")
        sys.exit(1)
    if start > end:
        print("[-] Le port de début doit être inférieur au port de fin.")
        sys.exit(1)