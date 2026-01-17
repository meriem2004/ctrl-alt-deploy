"""
Générateur Terraform - Génère les fichiers de configuration Terraform à partir d'un DeploymentSpec.

Ce module est responsable de :
1. Prendre un DeploymentSpec validé
2. Utiliser les mappers pour convertir les abstractions en valeurs AWS
3. Utiliser les templates Jinja2 pour générer les fichiers .tf
4. Écrire les fichiers dans un répertoire de sortie

Workflow :
DeploymentSpec → Mappers → Templates Jinja2 → Fichiers .tf → Terraform peut les utiliser
"""

import os
from pathlib import Path
from typing import Dict, Any, List
from jinja2 import Environment, FileSystemLoader, Template

# Import des modèles pour typer les données
# Utilisation d'imports relatifs depuis src/
import sys
from pathlib import Path

# Ajouter le répertoire src au path Python pour les imports
src_path = Path(__file__).parent.parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from models.models import DeploymentSpec, Service, ServiceType, Scalability

# Import des mappers pour convertir les abstractions
from infrastructure.mappers.instance_mapper import get_instance_type_for_service
from infrastructure.mappers.rds_mapper import (
    get_rds_instance_type_for_service,
    map_docker_image_to_rds_engine,
    get_rds_engine_version
)


class TerraformGenerator:
    """
    Générateur de configuration Terraform à partir d'un DeploymentSpec.
    
    Cette classe orchestre la génération complète :
    - Charge les templates Jinja2
    - Utilise les mappers pour convertir les données
    - Génère les fichiers .tf
    - Organise les fichiers dans un répertoire
    """
    
    def __init__(self, output_dir: str = "terraform_output"):
        """
        Initialise le générateur Terraform.
        
        Args:
            output_dir: Répertoire où écrire les fichiers Terraform générés
        """
        # Chemin du répertoire où on va écrire les fichiers Terraform
        self.output_dir = Path(output_dir)
        
        # Créer le répertoire s'il n'existe pas
        # parents=True : crée aussi les répertoires parents si nécessaire
        # exist_ok=True : ne lève pas d'erreur si le répertoire existe déjà
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Chemin vers le dossier des templates Jinja2
        # __file__ est le chemin de ce fichier Python
        # Ce fichier est dans: src/infrastructure/generators/terraform_generator.py
        # .parent = src/infrastructure/generators
        # .parent.parent = src/infrastructure
        # Donc templates_dir = src/infrastructure/templates
        templates_dir = Path(__file__).parent.parent / "templates"
        
        # Créer l'environnement Jinja2 pour charger les templates
        # FileSystemLoader charge les templates depuis le système de fichiers
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            trim_blocks=True,      # Supprime les espaces en début/fin de bloc
            lstrip_blocks=True,   # Supprime les espaces à gauche des blocs
            keep_trailing_newline=True  # Garde les sauts de ligne finaux
        )
    
    def generate(self, spec: DeploymentSpec) -> Path:
        """
        Méthode principale : génère tous les fichiers Terraform à partir d'un DeploymentSpec.
        
        Args:
            spec: Le DeploymentSpec validé (contient toutes les données de configuration)
            
        Returns:
            Le chemin du répertoire où les fichiers ont été générés
            
        Processus :
        1. Génère main.tf (configuration provider AWS)
        2. Génère variables.tf (définition des variables)
        3. Génère un fichier .tf pour chaque service EC2
        4. Retourne le chemin du répertoire
        """
        print(f"🔧 Génération de la configuration Terraform dans {self.output_dir}")
        
        # Étape 1 : Générer le fichier main.tf (configuration du provider AWS)
        self._generate_main_tf(spec)
        print("✓ main.tf généré")
        
        # Étape 2 : Générer le fichier variables.tf (définition des variables)
        self._generate_variables_tf(spec)
        print("✓ variables.tf généré")
        
        # Étape 2.5 : Générer le VPC si nécessaire (si vpc_id n'est pas spécifié)
        if not spec.infrastructure.vpc_id:
            self._generate_vpc_tf(spec)
            print("✓ vpc.tf généré (VPC automatique)")
        
        # Étape 3 : Générer un fichier .tf pour chaque service EC2
        ec2_services = [s for s in spec.application.services if s.type == ServiceType.EC2]
        
        for service in ec2_services:
            # Génère un fichier spécifique pour chaque service EC2
            self._generate_ec2_instance_tf(service, spec)
            print(f"✓ {service.name}_instance.tf généré")
        
        # Étape 4 : Générer un fichier .tf pour chaque service RDS
        rds_services = [s for s in spec.application.services if s.type == ServiceType.RDS]
        
        for service in rds_services:
            # Génère un fichier spécifique pour chaque service RDS
            self._generate_rds_instance_tf(service, spec)
            print(f"✓ {service.name}_instance.tf généré")
        
        print(f"\n✅ Configuration Terraform générée avec succès dans {self.output_dir}")
        return self.output_dir
    
    def _generate_main_tf(self, spec: DeploymentSpec) -> None:
        """
        Génère le fichier main.tf qui configure le provider AWS.
        
        Args:
            spec: Le DeploymentSpec contenant la configuration AWS
        """
        # Charge le template main.tf.j2
        template = self.jinja_env.get_template("main.tf.j2")
        
        # Prépare les données à passer au template
        # Ces données seront accessibles dans le template via {{ variable }}
        context = {
            "region": spec.aws.region,              # Région AWS
            "access_key": spec.aws.access_key,      # Clé d'accès AWS
            "secret_key": spec.aws.secret_key,      # Clé secrète AWS
            "environment": "production"             # Environnement (pourrait venir du spec)
        }
        
        # Rend le template avec les données (remplace {{ variable }} par les valeurs)
        rendered = template.render(**context)
        
        # Écrit le résultat dans le fichier main.tf
        output_file = self.output_dir / "main.tf"
        output_file.write_text(rendered, encoding="utf-8")
    
    def _generate_variables_tf(self, spec: DeploymentSpec) -> None:
        """
        Génère le fichier variables.tf qui définit les variables Terraform.
        
        Args:
            spec: Le DeploymentSpec contenant la configuration
        """
        # Charge le template variables.tf.j2
        template = self.jinja_env.get_template("variables.tf.j2")
        
        # Prépare les données pour le template
        context = {
            "region": spec.aws.region,
            "key_pair_name": spec.infrastructure.key_pair,
            "vpc_id": spec.infrastructure.vpc_id,   # Peut être None
            "access_key": spec.aws.access_key,
            "secret_key": spec.aws.secret_key,
            # AMI ID par défaut (Ubuntu 22.04 LTS pour us-east-1)
            # En production, on devrait mapper par région
            "ami_id": self._get_ami_id_for_region(spec.aws.region)
        }
        
        # Rend le template
        rendered = template.render(**context)
        
        # Écrit le fichier variables.tf
        output_file = self.output_dir / "variables.tf"
        output_file.write_text(rendered, encoding="utf-8")
    
    def _generate_ec2_instance_tf(self, service: Service, spec: DeploymentSpec) -> None:
        """
        Génère un fichier Terraform pour une instance EC2 spécifique.
        
        Args:
            service: Le service EC2 à déployer (contient name, ports, etc.)
            spec: Le DeploymentSpec complet (pour accéder à infrastructure, aws, etc.)
        """
        # Charge le template ec2_instance.tf.j2
        template = self.jinja_env.get_template("ec2_instance.tf.j2")
        
        # Utilise le mapper pour convertir machine_size + scalability en type d'instance AWS
        instance_type = get_instance_type_for_service(
            machine_size=spec.infrastructure.machine_size,
            scalability=spec.infrastructure.scalability
        )
        
        # Prépare les données pour le template
        context = {
            "service_name": service.name,           # Nom du service (ex: "backend")
            "instance_type": instance_type,          # Type d'instance (ex: "t3.medium")
            "key_pair_name": spec.infrastructure.key_pair,
            "region": spec.aws.region,
            "ports": service.ports,                 # Liste des ports (ex: [8080, 3000])
            "vpc_id": spec.infrastructure.vpc_id,    # Peut être None
            "docker_image": service.image,          # Image Docker si spécifiée (peut être None)
            "ami_id": self._get_ami_id_for_region(spec.aws.region),
            "tags": {}                              # Tags personnalisés (vide pour l'instant)
        }
        
        # Rend le template
        rendered = template.render(**context)
        
        # Écrit le fichier avec le nom du service
        # Ex: backend_instance.tf
        output_file = self.output_dir / f"{service.name}_instance.tf"
        output_file.write_text(rendered, encoding="utf-8")
    
    def _generate_rds_instance_tf(self, service: Service, spec: DeploymentSpec) -> None:
        """
        Génère un fichier Terraform pour une instance RDS spécifique.
        
        Args:
            service: Le service RDS à déployer (contient name, image, ports, environment, etc.)
            spec: Le DeploymentSpec complet (pour accéder à infrastructure, aws, etc.)
        """
        # Charge le template rds_instance.tf.j2
        template = self.jinja_env.get_template("rds_instance.tf.j2")
        
        # Utilise le mapper pour convertir machine_size + scalability en type d'instance RDS
        rds_instance_type = get_rds_instance_type_for_service(
            machine_size=spec.infrastructure.machine_size,
            scalability=spec.infrastructure.scalability
        )
        
        # Convertit l'image Docker en moteur RDS
        rds_engine = map_docker_image_to_rds_engine(service.image or "mysql:8")
        rds_engine_version = get_rds_engine_version(service.image or "mysql:8")
        
        # Extrait les informations de la base de données depuis l'environnement
        # Les variables d'environnement peuvent contenir : MYSQL_ROOT_PASSWORD, POSTGRES_PASSWORD, etc.
        db_password = service.environment.get(
            "MYSQL_ROOT_PASSWORD",
            service.environment.get("POSTGRES_PASSWORD", "changeme123!")
        )
        db_name = service.environment.get("MYSQL_DATABASE", service.environment.get("POSTGRES_DB", service.name))
        db_username = service.environment.get("MYSQL_USER", service.environment.get("POSTGRES_USER", "admin"))
        
        # Prépare les données pour le template
        context = {
            "service_name": service.name,
            "instance_type": rds_instance_type,
            "engine": rds_engine,
            "engine_version": rds_engine_version,
            "ports": service.ports if service.ports else [3306 if rds_engine == "mysql" else 5432],
            "db_name": db_name,
            "db_username": db_username,
            "db_password": db_password,
            "allocated_storage": 20,  # 20 GB par défaut
            "max_allocated_storage": 100,  # 100 GB max
            "multi_az": spec.infrastructure.scalability == Scalability.HIGH,  # Multi-AZ pour haute disponibilité
            "vpc_id": spec.infrastructure.vpc_id,  # Peut être None
        }
        
        # Rend le template
        rendered = template.render(**context)
        
        # Écrit le fichier avec le nom du service
        # Ex: database_instance.tf
        output_file = self.output_dir / f"{service.name}_instance.tf"
        output_file.write_text(rendered, encoding="utf-8")
    
    def _get_ami_id_for_region(self, region: str) -> str:
        """
        Retourne l'AMI ID (Amazon Machine Image) pour une région donnée.
        
        Une AMI est une image de système d'exploitation préconfigurée.
        Chaque région AWS a ses propres AMIs.
        
        Args:
            region: La région AWS (ex: "us-east-1")
            
        Returns:
            L'ID de l'AMI Ubuntu 22.04 LTS pour cette région
            
        Note: 
            En production, on devrait avoir un mapping complet par région.
            Ici, on retourne une valeur par défaut pour us-east-1.
        """
        # Mapping simplifié : AMI Ubuntu 22.04 LTS par région
        # Format: ami-XXXXXXXXXXXXX
        ami_mapping = {
            "us-east-1": "ami-0c55b159cbfafe1f0",      # N. Virginia
            "us-west-2": "ami-0c65adc9a5c1b5d7a",      # Oregon
            "eu-west-1": "ami-0c94855ba95b798c7",      # Ireland
            "eu-central-1": "ami-0d527b8c289b4af7f",   # Frankfurt
        }
        
        # Retourne l'AMI pour la région, ou une valeur par défaut
        return ami_mapping.get(region, "ami-0c55b159cbfafe1f0")  # Par défaut: us-east-1
    
    def _generate_vpc_tf(self, spec: DeploymentSpec) -> None:
        """
        Génère un fichier Terraform pour créer un VPC complet si vpc_id n'est pas spécifié.
        
        Args:
            spec: Le DeploymentSpec contenant la configuration
        """
        # Charge le template vpc.tf.j2
        template = self.jinja_env.get_template("vpc.tf.j2")
        
        # Prépare les données pour le template
        context = {
            "vpc_cidr": "10.0.0.0/16",  # CIDR par défaut pour le VPC
            "dns_enabled": spec.infrastructure.dns_enabled,
            "availability_zones_count": 2,  # 2 AZs par défaut pour haute disponibilité
        }
        
        # Rend le template
        rendered = template.render(**context)
        
        # Écrit le fichier vpc.tf
        output_file = self.output_dir / "vpc.tf"
        output_file.write_text(rendered, encoding="utf-8")


def generate_terraform_config(spec: DeploymentSpec, output_dir: str = "terraform_output") -> Path:
    """
    Fonction utilitaire pour générer la configuration Terraform.
    
    Cette fonction est un raccourci pour créer un TerraformGenerator et générer les fichiers.
    
    Args:
        spec: Le DeploymentSpec validé
        output_dir: Répertoire où écrire les fichiers
        
    Returns:
        Le chemin du répertoire où les fichiers ont été générés
        
    Example:
        >>> spec = parse_deployment_spec("spec.json")
        >>> generate_terraform_config(spec)
        Path('terraform_output')
    """
    generator = TerraformGenerator(output_dir)
    return generator.generate(spec)

