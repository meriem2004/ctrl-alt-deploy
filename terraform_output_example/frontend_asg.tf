# Launch Template for frontend
resource "aws_launch_template" "frontend_lt" {
  name_prefix   = "frontend-lt-"
  image_id      = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  user_data = base64encode(<<-EOF
#!/bin/bash
set -euo pipefail
exec > /var/log/user-data.log 2>&1
apt-get update -y
apt-get install -y docker.io
systemctl enable --now docker
echo 'optional_pass' | docker login -u 'optional_user' --password-stdin || true
docker pull omarbdoc/ctrl-alt-deploy:latest
docker run -d --restart=always -p 3000:3000 -e NODE_ENV='production' omarbdoc/ctrl-alt-deploy:latest
EOF
  )

  network_interfaces {
    associate_public_ip_address = true
    security_groups             = [aws_security_group.frontend_sg.id]
  }

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "frontend-instance"
    }
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Auto Scaling Group for frontend
resource "aws_autoscaling_group" "frontend_asg" {
  name                = "frontend-asg"
  vpc_zone_identifier = aws_subnet.public[*].id
  target_group_arns   = [aws_lb_target_group.frontend_tg.arn]
  health_check_type   = "ELB"
  health_check_grace_period = 300

  min_size         = 1
  max_size         = 2
  desired_capacity = 1

  launch_template {
    id      = aws_launch_template.frontend_lt.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "frontend"
    propagate_at_launch = true
  }
}

# Security Group for frontend instances
resource "aws_security_group" "frontend_sg" {
  name        = "frontend-sg"
  description = "Security group for frontend instances"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Allow traffic from ALB"
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    security_groups = [aws_security_group.frontend_lb_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "frontend-sg"
  }
}
