# Variables Terraform pour la configuration

variable "aws_region" {
  description = "Région AWS où déployer les ressources"
  type        = string
  default     = "us-east-1"
}



variable "aws_access_key" {
  description = "Clé d'accès AWS"
  type        = string
  sensitive   = true
  default     = "AKIAIOSFODNN7EXAMPLE"
}

variable "aws_secret_key" {
  description = "Clé secrète AWS"
  type        = string
  sensitive   = true
  default     = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
}

