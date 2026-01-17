#!/usr/bin/env python3
"""
Script pour exécuter tous les tests du projet.

Usage:
    python run_tests.py              # Exécute tous les tests
    python run_tests.py --unit       # Seulement les tests unitaires
    python run_tests.py --integration # Seulement les tests d'intégration
    python run_tests.py --e2e        # Seulement les tests end-to-end
    python run_tests.py --coverage   # Avec rapport de couverture
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Exécute les tests selon les arguments"""
    # Ajouter src au path
    src_path = Path(__file__).parent / "src"
    sys.path.insert(0, str(src_path))
    
    # Arguments de ligne de commande
    args = sys.argv[1:]
    
    # Construire la commande pytest
    cmd = ["python", "-m", "pytest"]
    
    if "--unit" in args:
        cmd.extend(["-m", "unit"])
    elif "--integration" in args:
        cmd.extend(["-m", "integration"])
    elif "--e2e" in args:
        cmd.extend(["-m", "e2e"])
    
    if "--coverage" in args:
        cmd.extend(["--cov=src", "--cov-report=html", "--cov-report=term"])
    
    # Ajouter verbose si pas déjà
    if "-v" not in cmd:
        cmd.append("-v")
    
    # Exécuter les tests
    print("=" * 60)
    print("Exécution des tests")
    print("=" * 60)
    print(f"Commande: {' '.join(cmd)}")
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n✅ Tous les tests sont passés !")
    else:
        print("\n❌ Certains tests ont échoué")
        sys.exit(1)

if __name__ == "__main__":
    main()

