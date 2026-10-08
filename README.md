# TP Sécurité – Application volontairement vulnérable

## But du projet
Mini API FastAPI + SQLite servant de **cible de scan** pour un TP DevSecOps :
- **SAST** avec [Bandit](https://bandit.readthedocs.io/)
- **SCA** avec [pip-audit](https://pypi.org/project/pip-audit/) / OWASP Dependency-Check

Les rapports « avant » sont dans `reports/before/`, les rapports « après » corrections dans `reports/after/`.

## ⚠️ Avertissement
**Ce code est VOLONTAIREMENT VULNÉRABLE. Ne JAMAIS le déployer ni l'exposer sur un réseau.**
Il est uniquement destiné à être scanné puis corrigé.

## Failles attendues

| ID Bandit | Fichier | Faille | Correction attendue |
|-----------|---------|--------|---------------------|
| B105 | main.py | `SECRET_KEY` en dur | Lire depuis une variable d'environnement |
| B608 | main.py (`/user`) | Injection SQL (f-string) | Requête paramétrée `?` |
| B602 | main.py (`/ping`) | Injection de commande (`shell=True`) | Liste d'arguments, `shell=False`, validation de `host` |
| B324 | main.py (`/register`) | Hachage MD5 | bcrypt / argon2 / PBKDF2 avec sel |
| B506 | main.py (`/config`) | `yaml.load` avec `yaml.Loader` | `yaml.safe_load` |
| B501 | main.py (`/fetch`) | `verify=False` | Retirer `verify=False` (vérif. TLS activée) |
| – (SCA) | requirements.txt | Dépendances anciennes avec CVE | Mettre à jour vers des versions corrigées |

## Commandes

```bash
# Build et lancement Docker
docker build -t tp-securite .
docker run --rm -p 8000:8000 tp-securite

# Tests
pip install -r requirements.txt pytest httpx requests
pytest

# SAST : Bandit
pip install bandit
bandit -r . -x ./tests,./.venv -f txt -o reports/before/bandit.txt
bandit -r . -x ./tests,./.venv -f json -o reports/before/bandit.json

# SCA : pip-audit
pip install pip-audit
pip-audit -r requirements.txt
```
