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

# Mapping des niveaux de scalabilité vers les types d'instances EC2
# Format : {Scalability: "instance_type"}
# Plus le niveau est élevé, plus l'instance est puissante
SCALABILITY_TO_INSTANCE_TYPE: Dict[Scalability, str] = {
    Scalability.LOW: "t3.micro",     # Faible scalabilité = instance petite
    Scalability.MED: "t3.medium",    # Scalabilité moyenne = instance moyenne
    Scalability.HIGH: "t3.large",    # Haute scalabilité = instance grande
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


def map_scalability_to_instance_type(scalability: Scalability) -> str:
    """
    Convertit un niveau de scalabilité (LOW, MED, HIGH) en type d'instance EC2 AWS.
    
    Args:
        scalability: Le niveau de scalabilité (Scalability.LOW, MED, ou HIGH)
        
    Returns:
        Le type d'instance EC2 correspondant (ex: "t3.medium")
        
    Example:
        >>> map_scalability_to_instance_type(Scalability.MED)
        't3.medium'
    """
    # On récupère le type d'instance depuis le dictionnaire de mapping
    if scalability not in SCALABILITY_TO_INSTANCE_TYPE:
        raise ValueError(f"Niveau de scalabilité non supporté: {scalability}")
    
    # Retourne le type d'instance correspondant
    return SCALABILITY_TO_INSTANCE_TYPE[scalability]


def get_instance_type_for_service(
    machine_size: MachineSize,
    scalability: Scalability
) -> str:
    """
    Détermine le type d'instance EC2 pour un service en combinant machine_size et scalability.
    
    Logique :
    - Si scalability est HIGH, on priorise la scalabilité (instance plus puissante)
    - Sinon, on utilise machine_size comme référence principale
    
    Args:
        machine_size: La taille de machine spécifiée (S, M, L, XL)
        scalability: Le niveau de scalabilité (LOW, MED, HIGH)
        
    Returns:
        Le type d'instance EC2 final (ex: "t3.large")
        
    Example:
        >>> get_instance_type_for_service(MachineSize.M, Scalability.HIGH)
        't3.large'
    """
    # Si la scalabilité est HIGH, on utilise le mapping de scalabilité
    # car HIGH nécessite une instance plus puissante
    if scalability == Scalability.HIGH:
        return map_scalability_to_instance_type(scalability)
    
    # Sinon, on utilise la taille de machine comme référence principale
    # C'est la taille que l'utilisateur a explicitement choisie
    return map_machine_size_to_instance_type(machine_size)

