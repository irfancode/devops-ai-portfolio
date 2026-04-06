terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "terraform-state-bucket"
    key            = "ai-devops-poc/terraform.tfstate"
    region         = "ap-southeast-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "ai-devops-poc"
      ManagedBy   = "terraform"
      Environment = var.environment
    }
  }
}

module "vpc" {
  source = "./modules/vpc"

  vpc_cidr    = var.vpc_cidr
  environment = var.environment
  az_count    = var.az_count
}

module "ec2" {
  source = "./modules/ec2"

  instance_type      = var.instance_type
  ami_id             = var.api_ami
  subnet_id          = module.vpc.public_subnet_ids[0]
  security_group_ids = [module.vpc.web_sg_id]
  key_name           = var.key_name
  user_data          = file("${path.module}/user_data.sh")
  environment        = var.environment
}

module "s3" {
  source = "./modules/s3"

  bucket_name = "${var.project_name}-${var.environment}-logs"
  environment = var.environment
}

module "rds" {
  source = "./modules/rds"

  db_name           = var.db_name
  db_username       = var.db_username
  db_password       = var.db_password
  subnet_ids        = module.vpc.private_subnet_ids
  security_group_id = module.vpc.db_sg_id
  instance_class    = var.db_instance_class
  allocated_storage = var.db_allocated_storage
  environment       = var.environment
}

module "iam" {
  source = "./modules/iam"

  project_name  = var.project_name
  environment   = var.environment
  ec2_role_name = "api-ec2-role-${var.environment}"
}
