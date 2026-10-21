# variables.tf

variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance size for the self-healing ASG"
  type        = string
  default     = "t2.micro"
}

variable "snow_instance" {
  description = "ServiceNow instance URL, e.g. https://devXXXXXX.service-now.com"
  type        = string
}

variable "snow_username" {
  description = "ServiceNow username"
  type        = string
}

variable "snow_password" {
  description = "ServiceNow password"
  type        = string
  sensitive   = true
}