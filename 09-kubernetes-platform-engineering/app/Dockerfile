# 09-kubernetes-platform-engineering/app/Dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN pip install boto3
COPY security_audit.py .
CMD ["sh", "-c", "while true; do python3 security_audit.py; sleep 300; done"]