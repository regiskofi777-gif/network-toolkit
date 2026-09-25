"""Module de scan TCP et UDP."""
import socket

def get_banner(sock: socket.socket) -> str:
    try:
        sock.send(b"\r\n")
        banner = sock.recv(1024)
        return banner.decode("utf-8", errors="ignore").strip()
    except Exception:
        return "Pas de bannière visible"

def scan_tcp_port(target: str, port: int) -> dict | None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1.0)
        if sock.connect_ex((target, port)) == 0:
            banner = get_banner(sock)
            return {"port": port, "protocol": "TCP", "state": "open", "bannière": banner}
    return None

def scan_udp_port(target: str, port: int) -> dict:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(2.0)
        try:
            sock.sendto(b"", (target, port))
            sock.recvfrom(1024)
            return {"port": port, "protocol": "UDP", "state": "open", "banner": ""}
        except socket.timeout:
            return {"port": port, "protocol": "UDP", "state": "open|filtered", "banner": ""}
        except socket.error:
            return {"port": port, "protocol": "UDP", "state": "closed", "banner": ""}