# Template pour générer une ressource EC2 Terraform
# Variables: service_name, instance_type, ports, docker_image, max_instances

resource "aws_instance" "landing-page" {
  instance_type               = "t3.micro"
  ami                         = data.aws_ami.ubuntu.id
  associate_public_ip_address = true

  # Utiliser le VPC créé automatiquement
  subnet_id = aws_subnet.public[0].id

  tags = {
    Name      = "landing-page"
    Service   = "landing-page"
    ManagedBy = "ctrl-alt-deploy"
  }

  vpc_security_group_ids = [aws_security_group.landing-page_sg.id]

  user_data = <<-EOF
#!/bin/bash
# Add 2GB swap to prevent OOM on small instances
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab

apt-get update
apt-get install -y docker.io
systemctl start docker
systemctl enable docker
apt-get install -y docker-compose
docker pull omarbdoc/ctrl-alt-deploy:latest
docker run -d -p 3000:3000 omarbdoc/ctrl-alt-deploy:latest
EOF

  lifecycle {
    create_before_destroy = true
  }
}

# Security Group pour l'instance EC2
resource "aws_security_group" "landing-page_sg" {
  name        = "landing-page-sg"
  description = "Security group for landing-page service"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "Allow all inbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name      = "landing-page-sg"
    Service   = "landing-page"
    ManagedBy = "ctrl-alt-deploy"
  }
}

# Outputs - Valeurs retournées après le déploiement
output "landing-page_instance_id" {
  description = "ID de l'instance EC2 pour landing-page"
  value       = aws_instance.landing-page.id
}

output "landing-page_public_ip" {
  description = "IP publique de l'instance EC2 pour landing-page"
  value       = aws_instance.landing-page.public_ip
}

output "landing-page_public_dns" {
  description = "DNS publique de l'instance EC2 pour landing-page"
  value       = aws_instance.landing-page.public_dns
}

