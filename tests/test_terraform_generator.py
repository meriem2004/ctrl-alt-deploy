"""
Tests d'intégration pour le générateur Terraform.

Ces tests vérifient que :
- La génération Terraform fonctionne correctement
- Les fichiers sont créés avec le bon contenu
- Les templates sont valides
"""

import sys
import json
import tempfile
from pathlib import Path
from shutil import rmtree

# Ajouter src au path Python
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

import pytest
from models.models import (
    DeploymentSpec, AWSConfig, InfrastructureConfig, 
    ApplicationConfig, Service, ServiceType, MachineSize, Scalability
)
from infrastructure.generators import TerraformGenerator, generate_terraform_config


class TestTerraformGenerator:
    """Tests pour le générateur Terraform"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        # Créer un répertoire temporaire pour les tests
        self.test_output_dir = Path(tempfile.mkdtemp())
    
    def teardown_method(self):
        """Cleanup après chaque test"""
        # Supprimer le répertoire temporaire
        if self.test_output_dir.exists():
            rmtree(self.test_output_dir)
    
    def create_minimal_spec(self) -> DeploymentSpec:
        """Crée un DeploymentSpec minimal pour les tests"""
        return DeploymentSpec(
            aws=AWSConfig(
                access_key="AKIAIOSFODNN7EXAMPLE",
                secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
                region="us-east-1"
            ),
            infrastructure=InfrastructureConfig(
                scalability=Scalability.MED,
                machine_size=MachineSize.M,
                key_pair="test-keypair"
            ),
            application=ApplicationConfig(
                services=[
                    Service(
                        name="test-service",
                        image="nginx:latest",
                        ports=[8080],
                        type=ServiceType.EC2
                    )
                ]
            )
        )
    
    def test_generator_initialization(self):
        """Test que le générateur s'initialise correctement"""
        generator = TerraformGenerator(str(self.test_output_dir))
        assert generator.output_dir == self.test_output_dir
        assert generator.jinja_env is not None
    
    def test_generate_main_tf(self):
        """Test génération de main.tf"""
        spec = self.create_minimal_spec()
        generator = TerraformGenerator(str(self.test_output_dir))
        generator._generate_main_tf(spec)
        
        main_tf = self.test_output_dir / "main.tf"
        assert main_tf.exists()
        
        content = main_tf.read_text()
        assert "provider \"aws\"" in content
        assert "us-east-1" in content
    
    def test_generate_variables_tf(self):
        """Test génération de variables.tf"""
        spec = self.create_minimal_spec()
        generator = TerraformGenerator(str(self.test_output_dir))
        generator._generate_variables_tf(spec)
        
        variables_tf = self.test_output_dir / "variables.tf"
        assert variables_tf.exists()
        
        content = variables_tf.read_text()
        assert "variable \"aws_region\"" in content
        assert "variable \"key_pair_name\"" in content
    
    def test_generate_ec2_instance_tf(self):
        """Test génération d'un fichier EC2"""
        spec = self.create_minimal_spec()
        generator = TerraformGenerator(str(self.test_output_dir))
        service = spec.application.services[0]
        generator._generate_ec2_instance_tf(service, spec)
        
        instance_tf = self.test_output_dir / "test-service_instance.tf"
        assert instance_tf.exists()
        
        content = instance_tf.read_text()
        assert "resource \"aws_instance\"" in content
        assert "test-service" in content
        assert "t3.medium" in content  # MachineSize.M → t3.medium
    
    def test_generate_vpc_tf(self):
        """Test génération de vpc.tf quand vpc_id est null"""
        spec = self.create_minimal_spec()
        generator = TerraformGenerator(str(self.test_output_dir))
        generator._generate_vpc_tf(spec)
        
        vpc_tf = self.test_output_dir / "vpc.tf"
        assert vpc_tf.exists()
        
        content = vpc_tf.read_text()
        assert "resource \"aws_vpc\"" in content
        assert "resource \"aws_subnet\"" in content
        assert "resource \"aws_internet_gateway\"" in content
    
    def test_generate_complete_ec2(self):
        """Test génération complète pour EC2"""
        spec = self.create_minimal_spec()
        output_dir = generate_terraform_config(spec, str(self.test_output_dir))
        
        assert output_dir == self.test_output_dir
        assert (output_dir / "main.tf").exists()
        assert (output_dir / "variables.tf").exists()
        assert (output_dir / "vpc.tf").exists()  # VPC créé automatiquement
        assert (output_dir / "test-service_instance.tf").exists()
    
    def test_generate_with_rds(self):
        """Test génération avec RDS"""
        spec = DeploymentSpec(
            aws=AWSConfig(
                access_key="AKIAIOSFODNN7EXAMPLE",
                secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
                region="us-east-1"
            ),
            infrastructure=InfrastructureConfig(
                scalability=Scalability.MED,
                machine_size=MachineSize.M,
                key_pair="test-keypair"
            ),
            application=ApplicationConfig(
                services=[
                    Service(
                        name="database",
                        image="mysql:8",
                        ports=[3306],
                        environment={
                            "MYSQL_ROOT_PASSWORD": "testpass",
                            "MYSQL_DATABASE": "testdb"
                        },
                        type=ServiceType.RDS
                    )
                ]
            )
        )
        
        output_dir = generate_terraform_config(spec, str(self.test_output_dir))
        
        assert (output_dir / "database_instance.tf").exists()
        
        content = (output_dir / "database_instance.tf").read_text()
        assert "resource \"aws_db_instance\"" in content
        assert "mysql" in content
        assert "db.t3.medium" in content  # MachineSize.M → db.t3.medium
    
    def test_generate_with_existing_vpc(self):
        """Test génération avec VPC existant (pas de création de VPC)"""
        spec = DeploymentSpec(
            aws=AWSConfig(
                access_key="AKIAIOSFODNN7EXAMPLE",
                secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
                region="us-east-1"
            ),
            infrastructure=InfrastructureConfig(
                scalability=Scalability.MED,
                machine_size=MachineSize.M,
                key_pair="test-keypair",
                vpc_id="vpc-12345678"  # VPC existant
            ),
            application=ApplicationConfig(
                services=[
                    Service(
                        name="test-service",
                        image="nginx:latest",
                        ports=[8080],
                        type=ServiceType.EC2
                    )
                ]
            )
        )
        
        output_dir = generate_terraform_config(spec, str(self.test_output_dir))
        
        # VPC ne devrait PAS être créé si vpc_id est spécifié
        vpc_tf = output_dir / "vpc.tf"
        assert not vpc_tf.exists()

