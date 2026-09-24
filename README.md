# network-toolkit
La première version d'un Network Toolkit capable de scanner une plage de ports TCP ATTENTION ! Je rappelle qu’il est formellement interdit de scanner les ports d’un hôte sans sa permission explicite. Pour tester le scanner, faites-le au niveau de votre propre réseau. Vous êtes entièrement responsables de l’usage que vous faites de ce scanner de ports.
# Comment executer le code ?

Il faut ouvrir le terminal et se positionner dans le dossier ou se trouve le fichier scan.py puis executer les commandes selon le besoin

python3 scan.py 127.0.0.1 --ports 20 100 --type tcp

python3 scan.py localhost --ports 1 1024 --type udp
