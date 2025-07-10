#  Network & Port Scanner

##  Description rapide

Script Python pour :

- Trouver votre IP locale
- Scanner un réseau local pour détecter les hôtes actifs
- Scanner les ports ouverts sur un hôte choisi avec détection de bannière


Choix de conception :

✅ 1. socket pour l’IP locale
Utilisé pour déterminer l’IP privée réelle de la machine sur le réseau, plus fiable que gethostname.

✅ 2. subprocess + ping système
Permet de vérifier la présence des hôtes sans librairie externe, compatible Windows et Linux.

✅ 3. Multithreading (threading + Queue)
Accélère le scan de ports (I/O bound) en testant plusieurs ports en parallèle.

✅ 4. Tentative de bannière (grab_banner)
Pour identifier le service qui tourne sur un port ouvert (ex : SSH, HTTP).

✅ 5. Timeout des sockets
Empêche le script de se bloquer trop longtemps sur un port non réactif.

✅ 6. colorama pour affichage coloré
Améliore la lisibilité des résultats en console.


---

## ️ Prérequis



###  Installation des modules nécessaires

```bash
pip install colorama

```

## ️ Utilisation

```bash
python3 scan.py

```

