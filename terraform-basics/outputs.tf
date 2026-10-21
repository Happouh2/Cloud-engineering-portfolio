output "vpc_id" {
  description = "ID of the created VPC"
  value       = aws_vpc.main.id
}
 
output "web_server_public_ip" {
  description = "Public IP of the web server"
  value       = aws_instance.web_server.public_ip
}
 
output "web_server_url" {
  description = "URL to reach the web server"
  value       = "http://${aws_instance.web_server.public_ip}"
}