"""
Mapper pour convertir les abstractions (S, M, L, XL) en types d'instances AWS réels.

Ce module fait le mapping entre :
- Les tailles de machines abstraites (S, M, L, XL) → Types d'instances EC2 AWS
- Les niveaux de scalabilité (LOW, MED, HIGH) → Types d'instances EC2 AWS

Pourquoi ce mapping est nécessaire ?
- L'utilisateur spécifie des abstractions simples (S, M, L, XL)
- AWS nécessite des types d'instances précis (t2.micro, t3.medium, etc.)
- Ce mapper fait la traduction automatique
"""

from typing import Dict
from models.models import MachineSize, Scalability


# Mapping des tailles de machines vers les types d'instances EC2
# Format : {MachineSize: "instance_type"}
# Ces types sont optimisés pour différents cas d'usage
MACHINE_SIZE_TO_INSTANCE_TYPE: Dict[MachineSize, str] = {
    MachineSize.S: "t3.micro",      # Petit : 2 vCPU, 1 GB RAM - Idéal pour dev/test
    MachineSize.M: "t3.medium",      # Moyen : 2 vCPU, 4 GB RAM - Idéal pour apps standard
    MachineSize.L: "t3.large",       # Grand : 2 vCPU, 8 GB RAM - Idéal pour apps avec charge
    MachineSize.XL: "t3.xlarge",     # Très grand : 4 vCPU, 16 GB RAM - Idéal pour apps intensives
}

# Mapping des niveaux de scalabilité vers le nombre maximum d'instances
# Format : {Scalability: int}
# LOW: 1 (une seule machine), MED: 3 (petit groupe), HIGH: 10 (groupe plus large)
SCALABILITY_TO_MAX_INSTANCES: Dict[Scalability, int] = {
    Scalability.LOW: 1,
    Scalability.MED: 3,
    Scalability.HIGH: 10,
}


def map_machine_size_to_instance_type(machine_size: MachineSize) -> str:
    """
    Convertit une taille de machine abstraite (S, M, L, XL) en type d'instance EC2 AWS.
    
    Args:
        machine_size: La taille de machine (MachineSize.S, M, L, ou XL)
        
    Returns:
        Le type d'instance EC2 correspondant (ex: "t3.medium")
        
    Example:
        >>> map_machine_size_to_instance_type(MachineSize.M)
        't3.medium'
    """
    # On récupère le type d'instance depuis le dictionnaire de mapping
    # Si la clé n'existe pas, on lève une exception
    if machine_size not in MACHINE_SIZE_TO_INSTANCE_TYPE:
        raise ValueError(f"Taille de machine non supportée: {machine_size}")
    
    # Retourne le type d'instance correspondant
    return MACHINE_SIZE_TO_INSTANCE_TYPE[machine_size]


def map_scalability_to_max_instances(scalability: Scalability) -> int:
    """
    Convertit un niveau de scalabilité (LOW, MED, HIGH) en nombre maximum d'instances.
    
    Args:
        scalability: Le niveau de scalabilité (Scalability.LOW, MED, ou HIGH)
        
    Returns:
        Le nombre maximum d'instances (1, 3, ou 10)
    """
    if scalability not in SCALABILITY_TO_MAX_INSTANCES:
        raise ValueError(f"Niveau de scalabilité non supporté: {scalability}")
    
    return SCALABILITY_TO_MAX_INSTANCES[scalability]


def get_instance_type_for_service(
    machine_size: MachineSize,
    scalability: Scalability = None
) -> str:
    """
    Détermine le type d'instance EC2 pour un service en fonction de machine_size.
    
    Note: La scalabilité (LOW, MED, HIGH) n'influence plus le type de machine,
    mais déterminera plus tard le nombre d'instances dans un Auto Scaling Group.
    
    Args:
        machine_size: La taille de machine spécifiée (S, M, L, XL)
        scalability: Optionnel, conservé pour compatibilité de signature.
        
    Returns:
        Le type d'instance EC2 final (ex: "t3.medium")
    """
    # On utilise maintenant uniquement la taille de machine pour le type d'instance
    return map_machine_size_to_instance_type(machine_size)

