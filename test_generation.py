"""
Script de test pour la génération Terraform.

Ce script démontre comment utiliser le générateur Terraform :
1. Parse un fichier spec.json
2. Génère la configuration Terraform
3. Affiche les fichiers générés

Pour exécuter :
    python test_generation.py
"""

import sys
from pathlib import Path

# Ajouter src au path Python
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Imports
from validators.parser import SpecParser
from infrastructure.generators import generate_terraform_config


def main():
    """
    Fonction principale qui teste la génération Terraform.
    """
    print("=" * 60)
    print("Test de génération Terraform")
    print("=" * 60)
    
    # Chemin vers un fichier spec.json de test
    # Vous pouvez créer un fichier spec.json simple pour tester
    spec_file = Path("spec.json")
    
    if not spec_file.exists():
        print(f"\n❌ Fichier {spec_file} non trouvé.")
        print("\nCréez un fichier spec.json avec la structure suivante :")
        print("""
{
  "aws": {
    "access_key": "YOUR_KEY",
    "secret_key": "YOUR_SECRET",
    "region": "us-east-1"
  },
  "infrastructure": {
    "scalability": "MED",
    "machine_size": "M",
    "key_pair": "my-keypair"
  },
  "application": {
    "services": [
      {
        "name": "backend",
        "image": "nginx:latest",
        "ports": [8080],
        "type": "EC2"
      }
    ]
  }
}
        """)
        return
    
    try:
        # Étape 1 : Parser et valider le spec.json
        print(f"\n📄 Étape 1 : Parsing de {spec_file}")
        parser = SpecParser(spec_file)
        spec = parser.parse()
        
        # Étape 2 : Générer la configuration Terraform
        print(f"\n🔧 Étape 2 : Génération de la configuration Terraform")
        output_dir = generate_terraform_config(spec, output_dir="terraform_output")
        
        # Étape 3 : Afficher les fichiers générés
        print(f"\n📁 Étape 3 : Fichiers générés dans {output_dir}")
        print("\nFichiers créés :")
        for file in sorted(output_dir.glob("*.tf")):
            print(f"  - {file.name}")
        
        print(f"\n✅ Test réussi ! Vous pouvez maintenant aller dans {output_dir}")
        print("   et exécuter : terraform init && terraform plan")
        
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

