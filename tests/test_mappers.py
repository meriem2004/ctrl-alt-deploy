"""
Tests unitaires pour les mappers (EC2 et RDS).

Ces tests vérifient que les mappers convertissent correctement :
- Les abstractions (S, M, L, XL) → Types d'instances AWS
- Les images Docker → Moteurs RDS
"""

import sys
from pathlib import Path

# Ajouter src au path Python
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

import pytest
from models.models import MachineSize, Scalability
from infrastructure.mappers.instance_mapper import (
    map_machine_size_to_instance_type,
    map_scalability_to_instance_type,
    get_instance_type_for_service
)
from infrastructure.mappers.rds_mapper import (
    map_machine_size_to_rds_instance_type,
    map_scalability_to_rds_instance_type,
    map_docker_image_to_rds_engine,
    get_rds_engine_version,
    get_rds_instance_type_for_service
)


class TestEC2Mappers:
    """Tests pour les mappers EC2"""
    
    def test_map_machine_size_s(self):
        """Test mapping MachineSize.S → t3.micro"""
        result = map_machine_size_to_instance_type(MachineSize.S)
        assert result == "t3.micro"
    
    def test_map_machine_size_m(self):
        """Test mapping MachineSize.M → t3.medium"""
        result = map_machine_size_to_instance_type(MachineSize.M)
        assert result == "t3.medium"
    
    def test_map_machine_size_l(self):
        """Test mapping MachineSize.L → t3.large"""
        result = map_machine_size_to_instance_type(MachineSize.L)
        assert result == "t3.large"
    
    def test_map_machine_size_xl(self):
        """Test mapping MachineSize.XL → t3.xlarge"""
        result = map_machine_size_to_instance_type(MachineSize.XL)
        assert result == "t3.xlarge"
    
    def test_map_scalability_low(self):
        """Test mapping Scalability.LOW → t3.micro"""
        result = map_scalability_to_instance_type(Scalability.LOW)
        assert result == "t3.micro"
    
    def test_map_scalability_med(self):
        """Test mapping Scalability.MED → t3.medium"""
        result = map_scalability_to_instance_type(Scalability.MED)
        assert result == "t3.medium"
    
    def test_map_scalability_high(self):
        """Test mapping Scalability.HIGH → t3.large"""
        result = map_scalability_to_instance_type(Scalability.HIGH)
        assert result == "t3.large"
    
    def test_get_instance_type_high_scalability(self):
        """Test que HIGH scalabilité priorise sur machine_size"""
        result = get_instance_type_for_service(MachineSize.M, Scalability.HIGH)
        # HIGH devrait donner t3.large, pas t3.medium
        assert result == "t3.large"
    
    def test_get_instance_type_med_scalability(self):
        """Test que MED scalabilité utilise machine_size"""
        result = get_instance_type_for_service(MachineSize.M, Scalability.MED)
        assert result == "t3.medium"


class TestRDSMappers:
    """Tests pour les mappers RDS"""
    
    def test_map_machine_size_to_rds_s(self):
        """Test mapping MachineSize.S → db.t3.micro"""
        result = map_machine_size_to_rds_instance_type(MachineSize.S)
        assert result == "db.t3.micro"
    
    def test_map_machine_size_to_rds_m(self):
        """Test mapping MachineSize.M → db.t3.medium"""
        result = map_machine_size_to_rds_instance_type(MachineSize.M)
        assert result == "db.t3.medium"
    
    def test_map_docker_image_mysql(self):
        """Test mapping image MySQL → engine mysql"""
        result = map_docker_image_to_rds_engine("mysql:8")
        assert result == "mysql"
    
    def test_map_docker_image_mysql_no_tag(self):
        """Test mapping image MySQL sans tag → engine mysql"""
        result = map_docker_image_to_rds_engine("mysql")
        assert result == "mysql"
    
    def test_map_docker_image_postgres(self):
        """Test mapping image PostgreSQL → engine postgres"""
        result = map_docker_image_to_rds_engine("postgres:14")
        assert result == "postgres"
    
    def test_map_docker_image_postgres_no_tag(self):
        """Test mapping image PostgreSQL sans tag → engine postgres"""
        result = map_docker_image_to_rds_engine("postgres")
        assert result == "postgres"
    
    def test_get_rds_engine_version_mysql(self):
        """Test extraction version depuis image MySQL"""
        result = get_rds_engine_version("mysql:8.0")
        assert result == "8.0"
    
    def test_get_rds_engine_version_postgres(self):
        """Test extraction version depuis image PostgreSQL"""
        result = get_rds_engine_version("postgres:14")
        assert result == "14"
    
    def test_get_rds_engine_version_default(self):
        """Test version par défaut si pas de tag"""
        result = get_rds_engine_version("mysql")
        assert result == "8.0"  # Version par défaut MySQL
    
    def test_get_rds_instance_type_high_scalability(self):
        """Test que HIGH scalabilité priorise pour RDS"""
        result = get_rds_instance_type_for_service(MachineSize.M, Scalability.HIGH)
        assert result == "db.t3.large"
    
    def test_get_rds_instance_type_med_scalability(self):
        """Test que MED scalabilité utilise machine_size pour RDS"""
        result = get_rds_instance_type_for_service(MachineSize.M, Scalability.MED)
        assert result == "db.t3.medium"
    
    def test_map_docker_image_invalid(self):
        """Test que image invalide lève une erreur"""
        with pytest.raises(ValueError):
            map_docker_image_to_rds_engine("invalid-image:1.0")

