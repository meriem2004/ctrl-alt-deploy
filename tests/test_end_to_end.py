"""
Tests end-to-end pour valider le workflow complet.

Ces tests vérifient que :
- Le parsing fonctionne
- La génération fonctionne
- Les fichiers Terraform sont valides
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
from validators.parser import SpecParser, ParseError
from infrastructure.generators import generate_terraform_config


class TestEndToEnd:
    """Tests end-to-end complets"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.test_output_dir = Path(tempfile.mkdtemp())
    
    def teardown_method(self):
        """Cleanup après chaque test"""
        if self.test_output_dir.exists():
            rmtree(self.test_output_dir)
    
    def test_full_workflow_ec2_only(self):
        """Test workflow complet avec seulement EC2"""
        spec_content = {
            "aws": {
                "access_key": "AKIAIOSFODNN7EXAMPLE",
                "secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
                "region": "us-east-1"
            },
            "infrastructure": {
                "scalability": "MED",
                "machine_size": "M",
                "key_pair": "test-keypair"
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
        
        # Créer un fichier spec temporaire
        spec_file = self.test_output_dir / "test_spec.json"
        spec_file.write_text(json.dumps(spec_content))
        
        # Parser
        parser = SpecParser(spec_file)
        spec = parser.parse()
        
        # Générer Terraform
        output_dir = generate_terraform_config(spec, str(self.test_output_dir / "terraform"))
        
        # Vérifier les fichiers
        assert (output_dir / "main.tf").exists()
        assert (output_dir / "variables.tf").exists()
        assert (output_dir / "vpc.tf").exists()
        assert (output_dir / "backend_instance.tf").exists()
    
    def test_full_workflow_ec2_and_rds(self):
        """Test workflow complet avec EC2 et RDS"""
        spec_content = {
            "aws": {
                "access_key": "AKIAIOSFODNN7EXAMPLE",
                "secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
                "region": "us-east-1"
            },
            "infrastructure": {
                "scalability": "MED",
                "machine_size": "M",
                "key_pair": "test-keypair"
            },
            "application": {
                "services": [
                    {
                        "name": "backend",
                        "image": "nginx:latest",
                        "ports": [8080],
                        "type": "EC2"
                    },
                    {
                        "name": "database",
                        "image": "mysql:8",
                        "ports": [3306],
                        "environment": {
                            "MYSQL_ROOT_PASSWORD": "testpass",
                            "MYSQL_DATABASE": "testdb"
                        },
                        "type": "RDS"
                    }
                ]
            }
        }
        
        spec_file = self.test_output_dir / "test_spec.json"
        spec_file.write_text(json.dumps(spec_content))
        
        # Parser
        parser = SpecParser(spec_file)
        spec = parser.parse()
        
        # Générer Terraform
        output_dir = generate_terraform_config(spec, str(self.test_output_dir / "terraform"))
        
        # Vérifier les fichiers
        assert (output_dir / "main.tf").exists()
        assert (output_dir / "backend_instance.tf").exists()
        assert (output_dir / "database_instance.tf").exists()
        
        # Vérifier le contenu RDS
        rds_content = (output_dir / "database_instance.tf").read_text()
        assert "mysql" in rds_content
        assert "db.t3.medium" in rds_content
    
    def test_invalid_spec_raises_error(self):
        """Test qu'un spec invalide lève une erreur"""
        spec_content = {
            "aws": {
                "access_key": "short",  # Trop court
                "secret_key": "short",
                "region": "us-east-1"
            },
            "infrastructure": {
                "key_pair": "test-keypair"
            },
            "application": {
                "services": []
            }
        }
        
        spec_file = self.test_output_dir / "invalid_spec.json"
        spec_file.write_text(json.dumps(spec_content))
        
        parser = SpecParser(spec_file)
        
        with pytest.raises(ParseError):
            parser.parse()
    
    def test_different_machine_sizes(self):
        """Test avec différentes tailles de machines"""
        sizes = ["S", "M", "L", "XL"]
        
        for size in sizes:
            spec_content = {
                "aws": {
                    "access_key": "AKIAIOSFODNN7EXAMPLE",
                    "secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
                    "region": "us-east-1"
                },
                "infrastructure": {
                    "scalability": "MED",
                    "machine_size": size,
                    "key_pair": "test-keypair"
                },
                "application": {
                    "services": [
                        {
                            "name": f"service-{size.lower()}",
                            "image": "nginx:latest",
                            "ports": [8080],
                            "type": "EC2"
                        }
                    ]
                }
            }
            
            spec_file = self.test_output_dir / f"spec_{size}.json"
            spec_file.write_text(json.dumps(spec_content))
            
            parser = SpecParser(spec_file)
            spec = parser.parse()
            
            output_dir = generate_terraform_config(
                spec, 
                str(self.test_output_dir / f"terraform_{size}")
            )
            
            instance_tf = output_dir / f"service-{size.lower()}_instance.tf"
            assert instance_tf.exists()
            
            # Vérifier que le type d'instance correspond à la taille
            content = instance_tf.read_text()
            if size == "S":
                assert "t3.micro" in content
            elif size == "M":
                assert "t3.medium" in content
            elif size == "L":
                assert "t3.large" in content
            elif size == "XL":
                assert "t3.xlarge" in content

