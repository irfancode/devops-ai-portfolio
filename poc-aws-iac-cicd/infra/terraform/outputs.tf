output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  description = "Private subnet IDs"
  value       = module.vpc.private_subnet_ids
}

output "api_public_ip" {
  description = "API server public IP"
  value       = module.ec2.public_ip
}

output "api_instance_id" {
  description = "API server instance ID"
  value       = module.ec2.instance_id
}

output "rds_endpoint" {
  description = "RDS endpoint"
  value       = module.rds.endpoint
  sensitive   = true
}

output "log_bucket_name" {
  description = "S3 log bucket name"
  value       = module.s3.bucket_name
}
