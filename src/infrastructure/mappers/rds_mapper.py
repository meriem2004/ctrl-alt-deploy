"""
Mapper pour convertir les abstractions (S, M, L, XL) en types d'instances RDS AWS.

Ce module fait le mapping entre :
- Les tailles de machines abstraites (S, M, L, XL) → Types d'instances RDS AWS
- Les images Docker (mysql:8, postgres:14, etc.) → Moteurs RDS AWS

Pourquoi ce mapping est nécessaire ?
- L'utilisateur spécifie des abstractions simples (S, M, L, XL) et une image Docker
- AWS RDS nécessite des types d'instances précis (db.t3.micro, db.t3.medium, etc.)
- Ce mapper fait la traduction automatique
"""

from typing import Dict, Optional
from models.models import MachineSize, Scalability


# Mapping des tailles de machines vers les types d'instances RDS
# Format : {MachineSize: "rds_instance_type"}
# Ces types sont optimisés pour les bases de données
MACHINE_SIZE_TO_RDS_INSTANCE_TYPE: Dict[MachineSize, str] = {
    MachineSize.S: "db.t3.micro",      # Petit : 2 vCPU, 1 GB RAM - Idéal pour dev/test
    MachineSize.M: "db.t3.medium",     # Moyen : 2 vCPU, 4 GB RAM - Idéal pour apps standard
    MachineSize.L: "db.t3.large",      # Grand : 2 vCPU, 8 GB RAM - Idéal pour apps avec charge
    MachineSize.XL: "db.t3.xlarge",    # Très grand : 4 vCPU, 16 GB RAM - Idéal pour apps intensives
}

# Mapping des niveaux de scalabilité vers les types d'instances RDS
SCALABILITY_TO_RDS_INSTANCE_TYPE: Dict[Scalability, str] = {
    Scalability.LOW: "db.t3.micro",
    Scalability.MED: "db.t3.medium",
    Scalability.HIGH: "db.t3.large",
}

# Mapping des images Docker vers les moteurs RDS AWS
# Format : {"image_name": "rds_engine"}
# Exemple : "mysql:8" → "mysql", "postgres:14" → "postgres"
DOCKER_IMAGE_TO_RDS_ENGINE: Dict[str, str] = {
    # MySQL
    "mysql": "mysql",
    "mysql:8": "mysql",
    "mysql:8.0": "mysql",
    "mysql:5.7": "mysql",
    "mariadb": "mariadb",
    "mariadb:10": "mariadb",
    
    # PostgreSQL
    "postgres": "postgres",
    "postgres:14": "postgres",
    "postgres:15": "postgres",
    "postgres:16": "postgres",
    "postgresql": "postgres",
    
    # Autres (à étendre si nécessaire)
    "mssql": "sqlserver",
    "sqlserver": "sqlserver",
}


def map_machine_size_to_rds_instance_type(machine_size: MachineSize) -> str:
    """
    Convertit une taille de machine abstraite (S, M, L, XL) en type d'instance RDS AWS.
    
    Args:
        machine_size: La taille de machine (MachineSize.S, M, L, ou XL)
        
    Returns:
        Le type d'instance RDS correspondant (ex: "db.t3.medium")
        
    Example:
        >>> map_machine_size_to_rds_instance_type(MachineSize.M)
        'db.t3.medium'
    """
    if machine_size not in MACHINE_SIZE_TO_RDS_INSTANCE_TYPE:
        raise ValueError(f"Taille de machine non supportée pour RDS: {machine_size}")
    
    return MACHINE_SIZE_TO_RDS_INSTANCE_TYPE[machine_size]


def map_scalability_to_rds_instance_type(scalability: Scalability) -> str:
    """
    Convertit un niveau de scalabilité (LOW, MED, HIGH) en type d'instance RDS AWS.
    
    Args:
        scalability: Le niveau de scalabilité (Scalability.LOW, MED, ou HIGH)
        
    Returns:
        Le type d'instance RDS correspondant (ex: "db.t3.medium")
    """
    if scalability not in SCALABILITY_TO_RDS_INSTANCE_TYPE:
        raise ValueError(f"Niveau de scalabilité non supporté pour RDS: {scalability}")
    
    return SCALABILITY_TO_RDS_INSTANCE_TYPE[scalability]


def map_docker_image_to_rds_engine(image: str) -> str:
    """
    Convertit une image Docker en moteur RDS AWS.
    
    Args:
        image: L'image Docker (ex: "mysql:8", "postgres:14")
        
    Returns:
        Le moteur RDS correspondant (ex: "mysql", "postgres")
        
    Example:
        >>> map_docker_image_to_rds_engine("mysql:8")
        'mysql'
        >>> map_docker_image_to_rds_engine("postgres:14")
        'postgres'
    """
    # Normaliser l'image (enlever les tags, mettre en minuscule)
    image_lower = image.lower().split(':')[0]  # "mysql:8" → "mysql"
    
    # Chercher dans le mapping
    for docker_image, engine in DOCKER_IMAGE_TO_RDS_ENGINE.items():
        if image_lower == docker_image.split(':')[0]:
            return engine
    
    # Si pas trouvé, essayer directement
    if image_lower in DOCKER_IMAGE_TO_RDS_ENGINE:
        return DOCKER_IMAGE_TO_RDS_ENGINE[image_lower]
    
    # Par défaut, essayer de deviner depuis le nom
    if 'mysql' in image_lower or 'mariadb' in image_lower:
        return 'mysql'
    elif 'postgres' in image_lower:
        return 'postgres'
    elif 'mssql' in image_lower or 'sqlserver' in image_lower:
        return 'sqlserver'
    
    # Si on ne trouve pas, on lève une erreur
    raise ValueError(
        f"Image Docker '{image}' non supportée pour RDS. "
        f"Images supportées: {', '.join(set(DOCKER_IMAGE_TO_RDS_ENGINE.values()))}"
    )


def get_rds_engine_version(image: str) -> str:
    """
    Extrait la version du moteur depuis l'image Docker.
    
    Args:
        image: L'image Docker (ex: "mysql:8.0", "postgres:14")
        
    Returns:
        La version du moteur (ex: "8.0", "14")
        
    Example:
        >>> get_rds_engine_version("mysql:8.0")
        '8.0'
        >>> get_rds_engine_version("postgres:14")
        '14'
    """
    # Si l'image contient un tag de version
    if ':' in image:
        version = image.split(':')[1]
        # Nettoyer la version (enlever les préfixes comme "v")
        version = version.lstrip('v')
        return version
    
    # Versions par défaut selon le moteur
    image_lower = image.lower()
    if 'mysql' in image_lower or 'mariadb' in image_lower:
        return '8.0'  # MySQL 8.0 par défaut
    elif 'postgres' in image_lower:
        return '14'  # PostgreSQL 14 par défaut
    
    return 'latest'


def get_rds_instance_type_for_service(
    machine_size: MachineSize,
    scalability: Scalability
) -> str:
    """
    Détermine le type d'instance RDS pour un service en combinant machine_size et scalability.
    
    Args:
        machine_size: La taille de machine spécifiée (S, M, L, XL)
        scalability: Le niveau de scalabilité (LOW, MED, HIGH)
        
    Returns:
        Le type d'instance RDS final (ex: "db.t3.medium")
    """
    # Si la scalabilité est HIGH, on utilise le mapping de scalabilité
    if scalability == Scalability.HIGH:
        return map_scalability_to_rds_instance_type(scalability)
    
    # Sinon, on utilise la taille de machine comme référence principale
    return map_machine_size_to_rds_instance_type(machine_size)

