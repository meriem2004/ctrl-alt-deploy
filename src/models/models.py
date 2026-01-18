"""
Data models for deployment specification.
This handles SYNTACTIC validation (structure, types, required fields).
"""
from typing import Optional, List, Dict, Literal
from pydantic import BaseModel, Field, field_validator, model_validator
from enum import Enum


class MachineSize(str, Enum):
    """Valid machine sizes"""
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"


class Scalability(str, Enum):
    """Valid scalability levels"""
    LOW = "LOW"
    MED = "MED"
    HIGH = "HIGH"


class ServiceType(str, Enum):
    """Valid service types"""
    EC2 = "EC2"
    RDS = "RDS"
    ECS = "ECS"


class AWSConfig(BaseModel):
    """AWS credentials and configuration"""
    access_key: str = Field(..., min_length=16, max_length=128, description="AWS access key")
    secret_key: str = Field(..., min_length=16, description="AWS secret key")
    region: str = Field(..., description="AWS region (e.g., us-east-1)")
    
    @field_validator('region')
    @classmethod
    def validate_region_format(cls, v: str) -> str:
        """Validate region format (will check if valid in semantic validation)"""
        if not v or len(v) < 5:
            raise ValueError("Region must be a valid AWS region string")
        return v


class DockerHubCredentials(BaseModel):
    """Optional Docker Hub credentials"""
    username: Optional[str] = None
    password: Optional[str] = None


class DockerConfig(BaseModel):
    """Docker configuration"""
    hub_credentials: Optional[DockerHubCredentials] = None


class InfrastructureConfig(BaseModel):
    """Infrastructure-level configuration"""
    scalability: Scalability = Field(default=Scalability.MED, description="Overall scalability level")
    machine_size: MachineSize = Field(default=MachineSize.M, description="Default machine size")
    vpc_id: Optional[str] = Field(None, description="Existing VPC ID (optional)")
    key_pair: Optional[str] = Field(None, description="SSH key pair name for EC2 instances (Optional)")
    dns_enabled: bool = Field(default=False, description="Enable DNS configuration")


class ScalingConfig(BaseModel):
    """Scaling configuration for a service"""
    min: int = Field(..., ge=1, le=100, description="Minimum number of instances")
    max: int = Field(..., ge=1, le=100, description="Maximum number of instances")
    
    @model_validator(mode='after')
    def validate_min_max(self):
        """Ensure min <= max"""
        if self.min > self.max:
            raise ValueError(f"Scaling min ({self.min}) cannot be greater than max ({self.max})")
        return self


class Service(BaseModel):
    """Individual service configuration"""
    name: str = Field(..., min_length=1, max_length=64, description="Service name")
    dockerfile_path: Optional[str] = Field(None, description="Path to Dockerfile")
    image: Optional[str] = Field(None, description="Docker image URL")
    ports: List[int] = Field(default_factory=list, description="Exposed ports")
    environment: Dict[str, str] = Field(default_factory=dict, description="Environment variables")
    scaling: Optional[ScalingConfig] = None
    type: ServiceType = Field(default=ServiceType.EC2, description="Service deployment type")
    depends_on: List[str] = Field(default_factory=list, description="Service dependencies")
    
    @field_validator('ports')
    @classmethod
    def validate_ports(cls, v: List[int]) -> List[int]:
        """Validate port numbers"""
        for port in v:
            if not (1 <= port <= 65535):
                raise ValueError(f"Port {port} is invalid. Must be between 1-65535")
        return v
    
    @field_validator('name')
    @classmethod
    def validate_name_format(cls, v: str) -> str:
        """Service name must be alphanumeric with hyphens/underscores"""
        import re
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError(f"Service name '{v}' must contain only alphanumeric characters, hyphens, and underscores")
        return v
    
    @model_validator(mode='after')
    def validate_image_source(self):
        """Must have either dockerfile_path OR image, not both or neither"""
        has_dockerfile = self.dockerfile_path is not None
        has_image = self.image is not None
        
        if not has_dockerfile and not has_image:
            raise ValueError(f"Service '{self.name}' must specify either 'dockerfile_path' or 'image'")
        
        if has_dockerfile and has_image:
            raise ValueError(f"Service '{self.name}' cannot have both 'dockerfile_path' and 'image'. Choose one.")
        
        return self


class ApplicationConfig(BaseModel):
    """Application-level configuration"""
    repository_url: Optional[str] = Field(None, description="Git repository URL")
    services: List[Service] = Field(..., min_length=1, description="List of services to deploy")


class DeploymentSpec(BaseModel):
    """Root deployment specification model"""
    spec_version: str = Field(default="1.0.0", description="Specification version")
    aws: AWSConfig
    docker: Optional[DockerConfig] = None
    infrastructure: InfrastructureConfig
    application: ApplicationConfig
    
    class Config:
        """Pydantic configuration"""
        use_enum_values = True
        validate_assignment = True
        str_strip_whitespace = True