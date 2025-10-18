"""
Semantic validation layer - validates logical consistency.
Runs AFTER syntactic validation (Pydantic models).
"""
from typing import List, Dict, Set
from models import DeploymentSpec, Service, ServiceType


class ValidationError(Exception):
    """Custom validation error"""
    pass


class SemanticValidator:
    """
    Validates logical consistency of deployment specification.
    """
    
    # Valid AWS regions (as of 2024)
    VALID_AWS_REGIONS = {
        'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2',
        'eu-west-1', 'eu-west-2', 'eu-west-3', 'eu-central-1', 'eu-north-1',
        'ap-south-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-northeast-3',
        'ap-southeast-1', 'ap-southeast-2', 'ap-east-1',
        'ca-central-1', 'sa-east-1', 'me-south-1', 'af-south-1'
    }
    
    # Services that can be database backends
    DATABASE_SERVICES = {'RDS'}
    
    # Services that can run application code
    COMPUTE_SERVICES = {'EC2', 'ECS'}
    
    def __init__(self, spec: DeploymentSpec):
        self.spec = spec
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate(self) -> tuple[bool, List[str], List[str]]:
        """
        Run all semantic validations.
        Returns: (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []
        
        # Run all validation checks
        self._validate_aws_region()
        self._validate_service_types()
        self._validate_service_dependencies()
        self._validate_port_conflicts()
        self._validate_environment_references()
        self._validate_scaling_for_type()
        self._validate_rds_specific()
        self._validate_security_concerns()
        
        return len(self.errors) == 0, self.errors, self.warnings
    
    def _validate_aws_region(self):
        """Validate AWS region is valid"""
        region = self.spec.aws.region
        if region not in self.VALID_AWS_REGIONS:
            self.errors.append(
                f"Invalid AWS region '{region}'. Must be one of: {', '.join(sorted(self.VALID_AWS_REGIONS))}"
            )
    
    def _validate_service_types(self):
        """Validate service types have appropriate configurations"""
        for service in self.spec.application.services:
            # RDS services shouldn't have Dockerfile
            if service.type == ServiceType.RDS and service.dockerfile_path:
                self.errors.append(
                    f"Service '{service.name}' is type RDS but has dockerfile_path. "
                    f"RDS services must use pre-built images."
                )
            
            # EC2/ECS services need either Dockerfile or image
            if service.type in self.COMPUTE_SERVICES:
                if not service.dockerfile_path and not service.image:
                    self.errors.append(
                        f"Service '{service.name}' is type {service.type} but has no dockerfile_path or image."
                    )
    
    def _validate_service_dependencies(self):
        """Validate service dependency graph"""
        service_names = {s.name for s in self.spec.application.services}
        
        for service in self.spec.application.services:
            # Check all dependencies exist
            for dep in service.depends_on:
                if dep not in service_names:
                    self.errors.append(
                        f"Service '{service.name}' depends on '{dep}' which doesn't exist."
                    )
        
        # Check for circular dependencies
        if self._has_circular_dependencies():
            self.errors.append(
                "Circular dependency detected in service dependencies. "
                "Services cannot depend on each other in a cycle."
            )
    
    def _has_circular_dependencies(self) -> bool:
        """Detect circular dependencies using DFS"""
        # Build adjacency list
        graph: Dict[str, List[str]] = {}
        for service in self.spec.application.services:
            graph[service.name] = service.depends_on
        
        visited: Set[str] = set()
        rec_stack: Set[str] = set()
        
        def has_cycle(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        for service_name in graph:
            if service_name not in visited:
                if has_cycle(service_name):
                    return True
        
        return False
    
    def _validate_port_conflicts(self):
        """Check for port conflicts between services"""
        port_map: Dict[int, List[str]] = {}
        
        for service in self.spec.application.services:
            for port in service.ports:
                if port not in port_map:
                    port_map[port] = []
                port_map[port].append(service.name)
        
        for port, services in port_map.items():
            if len(services) > 1:
                self.warnings.append(
                    f"Port {port} is used by multiple services: {', '.join(services)}. "
                    f"This is okay if they run on different machines, but may cause conflicts."
                )
    
    def _validate_environment_references(self):
        """Validate environment variable references to other services"""
        service_names = {s.name for s in self.spec.application.services}
        
        for service in self.spec.application.services:
            for key, value in service.environment.items():
                # Check if value references another service (simple heuristic)
                # Common patterns: DB_HOST=database, REDIS_HOST=redis, etc.
                if any(svc_name in value for svc_name in service_names):
                    referenced = [svc for svc in service_names if svc in value]
                    for ref in referenced:
                        if ref not in service.depends_on:
                            self.warnings.append(
                                f"Service '{service.name}' references '{ref}' in environment variable '{key}' "
                                f"but doesn't list it in depends_on. Consider adding dependency."
                            )
    
    def _validate_scaling_for_type(self):
        """Validate scaling configuration is appropriate for service type"""
        for service in self.spec.application.services:
            # RDS doesn't support horizontal scaling the same way
            if service.type == ServiceType.RDS and service.scaling:
                if service.scaling.max > 1:
                    self.warnings.append(
                        f"Service '{service.name}' is type RDS with scaling.max > 1. "
                        f"RDS doesn't support horizontal scaling like EC2. This will be ignored."
                    )
    
    def _validate_rds_specific(self):
        """RDS-specific validation"""
        for service in self.spec.application.services:
            if service.type == ServiceType.RDS:
                # RDS should have database environment variables
                db_env_keys = {'MYSQL_ROOT_PASSWORD', 'POSTGRES_PASSWORD', 'MYSQL_PASSWORD'}
                has_db_password = any(key in service.environment for key in db_env_keys)
                
                if not has_db_password:
                    self.warnings.append(
                        f"RDS service '{service.name}' doesn't have database password set. "
                        f"Expected one of: {', '.join(db_env_keys)}"
                    )
                
                # RDS typically uses standard ports
                expected_ports = {3306, 5432, 1433}  # MySQL, PostgreSQL, SQL Server
                if service.ports and not any(p in expected_ports for p in service.ports):
                    self.warnings.append(
                        f"RDS service '{service.name}' uses non-standard ports: {service.ports}. "
                        f"Standard database ports are: {expected_ports}"
                    )
    
    def _validate_security_concerns(self):
        """Check for common security issues"""
        # Check for hardcoded passwords
        for service in self.spec.application.services:
            for key, value in service.environment.items():
                if 'password' in key.lower() or 'secret' in key.lower():
                    if len(value) < 8:
                        self.warnings.append(
                            f"Service '{service.name}' has weak password in '{key}'. "
                            f"Passwords should be at least 8 characters."
                        )
                    
                    # Check for common weak passwords
                    weak_passwords = {'password', '123456', 'admin', 'root'}
                    if value.lower() in weak_passwords:
                        self.errors.append(
                            f"Service '{service.name}' uses weak password '{value}' in '{key}'. "
                            f"This is a critical security issue."
                        )
        
        # Warn about exposed ports
        for service in self.spec.application.services:
            if service.type == ServiceType.RDS and service.ports:
                self.warnings.append(
                    f"RDS service '{service.name}' exposes ports {service.ports}. "
                    f"Ensure RDS is not publicly accessible in production."
                )


def validate_spec_semantics(spec: DeploymentSpec) -> tuple[bool, List[str], List[str]]:
    """
    Convenience function to run semantic validation.
    Returns: (is_valid, errors, warnings)
    """
    validator = SemanticValidator(spec)
    return validator.validate()