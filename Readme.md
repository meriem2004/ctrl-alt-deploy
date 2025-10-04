Ctrl Alt Deploy
Overview

Ctrl Alt Deploy is an automated deployment system that takes a GitHub repository as input and manages the full deployment pipeline to AWS. The system validates the repository structure, builds and packages the application into a Docker image, provisions the required AWS infrastructure using Terraform, and deploys the application to an EKS cluster with Helm.

If the repository is not structured correctly, the system provides feedback and suggestions for making it deployable.

Features

Repository validation (checks for Dockerfile, Kubernetes manifests, or Helm charts)

Automatic Docker image build and push to AWS ECR

Infrastructure provisioning with Terraform (VPC, IAM roles, security groups, EKS, ALB ingress controller)

Application deployment with Helm to EKS

Error reporting and feedback with actionable suggestions

Workflow

Input: User provides a GitHub repository link.

Validation: The system checks for Dockerfile, Helm chart, and application structure.

Infrastructure provisioning: Terraform provisions AWS resources including VPC, EKS, IAM policies, security groups, and ALB ingress.

Image build: The application is containerized, and the Docker image is pushed to ECR.

Deployment: Helm is used to deploy the application to the EKS cluster.

Feedback: The system returns either a deployment URL or error details with required changes.