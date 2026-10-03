
import socket

class ValidationError(ValueError):
    pass

def resolve_target(hostname: str) -> str:
    if not hostname or not hostname.strip():
        raise ValidationError("La cible ne peut pas être vide")
    try:
        return socket.gethostbyname(hostname.strip())
    except socket.gaierror:
        raise ValidationError(f"Impossible de résoudre '{hostname}'. Vérifiez l'adresse")

def parse_port_range(value: str) -> tuple[int, int]:
    if "-" not in value:
        raise ValidationError(f"Format de plage invalide : '{value}'. Attendu : 'debut-fin'.")
    parts = value.split("-", 1)
    try:
        start = int(parts[0])
        end = int(parts[1])
    except ValueError:
        raise ValidationError(f"Les ports doivent des nombres entiers : '{value}'.")
    validate_port_range(start, end)
    return start, end

def validate_port_range(start: int, end: int) -> None:
    if not (1 <= start <= 65535):
        raise ValidationError(f"Port de début hors bornes : {start} (attendu 1-65535).")
    if not (1 <= end <= 65535):
        raise ValidationError(f"Port de fin hors bornes : {end} (attendu 1-65535).")
    if start > end:
        raise ValidationError(f"Plage inversée : début ({start}) > fin ({end}).")

def validate_threads(n: int) -> None:
    if n < 1:
        raise ValidationError(f"Le nombre de threads doit être >= 1 (reçu : {n}).")
    if n > 500:
        raise ValidationError(f"Le nombre de threads ne doit pas dépasser 500 (reçu : {n}).")
    
