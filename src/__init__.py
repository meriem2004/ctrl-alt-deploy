# Update src/models/__init__.py
cat > src/models/__init__.py << 'EOF'
from .models import (
    DeploymentSpec,
    Service,
    AWSConfig,
    InfrastructureConfig,
    ApplicationConfig,
    MachineSize,
    Scalability,
    ServiceType
)

__all__ = [
    'DeploymentSpec',
    'Service',
    'AWSConfig',
    'InfrastructureConfig',
    'ApplicationConfig',
    'MachineSize',
    'Scalability',
    'ServiceType'
]
EOF

# Update src/validators/__init__.py
cat > src/validators/__init__.py << 'EOF'
from .parser import SpecParser, parse_deployment_spec, ParseError
from .semantic_validator import SemanticValidator, validate_spec_semantics

__all__ = [
    'SpecParser',
    'parse_deployment_spec',
    'ParseError',
    'SemanticValidator',
    'validate_spec_semantics'
]
EOF