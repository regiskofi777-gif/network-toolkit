# Network Toolkit

> ⚠️ **Avertissement légal** — Cet outil est destiné **uniquement** à
> l'analyse de réseaux que vous possédez ou pour lesquels vous disposez
> d'une **autorisation écrite explicite**. Scanner un réseau sans
> autorisation est illégal dans la plupart des juridictions. L'auteur
> décline toute responsabilité en cas d'utilisation abusive.

Outil Python en ligne de commande pour scanner, tester et diagnostiquer
un réseau dans un environnement autorisé.

---

## Description

**Network Toolkit** est un scanner de ports TCP/UDP écrit en Python,
utilisable en ligne de commande. Il permet de détecter les ports ouverts,
de récupérer les bannières de service lorsque celles-ci sont disponibles,
et d'exporter les résultats au format JSON.

Le projet est développé dans le cadre d'un programme d'autoformation
full-stack, et sert de première brique à une suite d'outils réseau et
web.

---

## Fonctionnalités

- **Scan TCP** avec détection des ports ouverts et récupération de bannières
- **Scan UDP** avec distinction ouvert / filtré / fermé
- **Multithreading** configurable via `--threads` (1 à 500 workers)
- **Export JSON** structuré et exploitable
- **Logs structurés** (niveau, timestamp) sur `stderr`, séparés des résultats
- **Validation robuste** des entrées (cible, plage de ports, workers)
- **Résolution DNS** automatique des noms d'hôte
- **Mesure de la durée** du scan
- **Tests unitaires** (31 tests avec pytest)
- **Qualité de code** assurée par ruff (linting + formatting)

---

## Prérequis

- **Python 3.11 ou supérieur**
- **Linux** (testé sur Kali), macOS ou Windows
- Aucune dépendance externe à l'exécution (uniquement la bibliothèque
  standard Python)

---

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/regiskofi777-gif/network-toolkit.git
cd network-toolkit

# Créer et activer un environnement virtuel
python3 -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows

# Installer le paquet en mode éditable
pip install -e .

# (Optionnel) Installer les dépendances de développement
pip install pytest ruff

```
**Note Kali/Debian** : si `pip install` refuse de s'exécuter à cause  
de `externally-managed-environment`, utilisez impérativement un  
environnement virtuel (comme ci-dessus) plutôt que `sudo pip`.
    
## Utilisation

### Syntaxe générale
``` 
python -m network_toolkit --target <CIBLE> --ports <DEBUT-FIN> [OPTIONS]
```

## Options disponibles
| **Option** | **Raccourci** | **Description** | **Défaut** |
| :-: | :-: | :-: | :-: |
| `--target` | `-t` | Adresse IP ou nom d'hôte à scanner | **obligatoire** |
| `--ports` | `-p` | Plage de ports au format `debut-fin` | **obligatoire** |
| `--threads` | `-T` | Nombre de workers (1-500) | `100` |
| `--protocol` |  | `tcp` ou `udp` | `tcp` |
| `--output` | `-o` | Fichier JSON de sortie | aucun |
| `--help` | `-h` | Affiche l'aide |  |

## Exemples

### Scanner les ports 20 à 1000 en TCP :
```bash
python -m network_toolkit --target 127.0.0.1 --ports 20-1000
```
### Scanner un port UDP spécifique :
```bash
python -m network_toolkit --target 192.168.1.1 --ports 53-53 --protocol udp
```
### Limiter les workers et exporter en JSON :
```bash
python -m network_toolkit --target 127.0.0.1 --ports 20-9999 \
  --threads 50 --output result.json
```

### Rediriger les résultats vers un fichier (sans les logs) :
```bash
python -m network_toolkit --target 127.0.0.1 --ports 20-9999 > ports.txt
```
### Exemple de sortie
```text
Sur le terminal (logs d'info + résultats) :
[2026-10-17 15:32:11] [INFO] Cible : 127.0.0.1
[2026-10-17 15:32:11] [INFO] Protocole : TCP
[2026-10-17 15:32:11] [INFO] Ports : 20-9999 (9980 ports)
[2026-10-17 15:32:11] [INFO] Workers : 100

Port TCP    80 : [open] | Banner: Pas de bannière (timeout)
Port TCP   631 : [open] | Banner: Pas de bannière (timeout)
Port TCP  3306 : [open] | Banner: `11.8.8-MariaDB-1 from Debian...
Port TCP  7070 : [open] | Banner: Pas de bannière (timeout)

[+] Scan terminé en 0:00:02.362497
[+] 4 port(s) ouvert(s) sur 9980 analysé(s).
```

### Format JSON exporté ( `--output result.json` ) :
```json
{
  "scan": {
    "target": "127.0.0.1",
    "protocol": "tcp",
    "port_range": "20-9999",
    "threads": 100,
    "started_at": "2026-10-17T15:32:11.234567",
    "finished_at": "2026-10-17T15:32:13.567890",
    "duration_seconds": 2.333,
    "total_ports": 9980
  },
  "summary": {
    "total_ports": 9980,
    "open_ports": 4
  },
  "results": [
    {
      "port": 80,
      "protocol": "TCP",
      "state": "open",
      "banner": "Pas de bannière (timeout)"
    }
  ]
}
```

## Structure du projet

```text
network-toolkit/
├── .gitignore
├── README.md
├── requirements.txt
├── pyproject.toml
├── src/
│   └── network_toolkit/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── logger.py
│       ├── output.py
│       ├── scanner.py
│       └── validation.py
└── tests/
    ├── __init__.py
    ├── test_output.py
    └── test_validation.py
```

| **Fichier** | **Rôle** |
| :-: | :-: |
| `__main__.py` | Point d'entrée (`python -m network_toolkit`) |
| `cli.py` | Interface CLI (argparse, orchestration) |
| `logger.py` | Configuration du logging structuré |
| `scanner.py` | Moteur de scan TCP et UDP |
| `validation.py` | Validation des entrées utilisateur |
| `output.py` | Affichage console et export JSON |
| `tests/` | Tests unitaires (pytest) |



## Développement

### Lancer les tests

bash

```
pytest -v
```

### Vérifier la qualité du code

```bash
ruff check src/ tests/
ruff format src/ tests/
```
# Limitations connues

- Les services à **protocole binaire** (MySQL/MariaDB, Redis, etc.)  
peuvent afficher une bannière contenant des octets non imprimables.  
C'est volontaire : le scanner ne suppose pas qu'un port correspond à  
un service donné, et restitue la réponse brute du service.

- Les services **HTTP** n'envoient pas de bannière sans requête  
préalable — le scanner affiche alors « Pas de bannière (timeout) ».

- Pas encore de **configuration par fichier** (tout passe par les  
arguments CLI).

- Pas encore de **détection de service** (fingerprinting avancé).


## Roadmap

- ☑ 

- **Semaine 1** — Scanner TCP simple, structure du projet

- ☑ 

- **Semaine 2** — Scan UDP, multithreading, bannières, CLI, export JSON

- ☑ 

- **Semaine 3** — Tests unitaires, ruff, logs structurés, tag v1.0.0

- □ 

- **Projet B** — Task Manager Full-Stack (FastAPI + React)

- □ 

- **Projet C** — NetMonitor Full-Stack (WebSocket + Prometheus + Grafana)


## Licence

MIT

## Auteur

Kouadio Koffi Regis — [github.com/regiskofi777-gif](https://github.com/regiskofi777-gif)

