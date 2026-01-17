"""
Mappers - Conversion des abstractions en valeurs AWS concrètes.
"""

from .instance_mapper import (
    map_machine_size_to_instance_type,
    map_scalability_to_instance_type,
    get_instance_type_for_service,
    MACHINE_SIZE_TO_INSTANCE_TYPE,
    SCALABILITY_TO_INSTANCE_TYPE
)

from .rds_mapper import (
    map_machine_size_to_rds_instance_type,
    map_scalability_to_rds_instance_type,
    map_docker_image_to_rds_engine,
    get_rds_engine_version,
    get_rds_instance_type_for_service,
    MACHINE_SIZE_TO_RDS_INSTANCE_TYPE,
    SCALABILITY_TO_RDS_INSTANCE_TYPE,
    DOCKER_IMAGE_TO_RDS_ENGINE
)

__all__ = [
    # EC2 mappers
    'map_machine_size_to_instance_type',
    'map_scalability_to_instance_type',
    'get_instance_type_for_service',
    'MACHINE_SIZE_TO_INSTANCE_TYPE',
    'SCALABILITY_TO_INSTANCE_TYPE',
    # RDS mappers
    'map_machine_size_to_rds_instance_type',
    'map_scalability_to_rds_instance_type',
    'map_docker_image_to_rds_engine',
    'get_rds_engine_version',
    'get_rds_instance_type_for_service',
    'MACHINE_SIZE_TO_RDS_INSTANCE_TYPE',
    'SCALABILITY_TO_RDS_INSTANCE_TYPE',
    'DOCKER_IMAGE_TO_RDS_ENGINE'
]

