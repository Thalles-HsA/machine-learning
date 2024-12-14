#!/bin/bash

# Nome do repositório ECR
ECR_REPO="863518425456.dkr.ecr.us-east-1.amazonaws.com/machine-learning"
ECR_REGION="us-east-1"
DOCKER_COMPOSE_FILE="docker-compose.yml"

# Função para exibir mensagens formatadas
log() {
  echo -e "\e[32m[INFO]\e[0m $1"
}

error() {
  echo -e "\e[31m[ERROR]\e[0m $1"
  exit 1
}

# Verificar se o arquivo docker-compose.yml existe
if [[ ! -f "$DOCKER_COMPOSE_FILE" ]]; then
  error "Arquivo $DOCKER_COMPOSE_FILE não encontrado! Verifique o caminho e tente novamente."
fi

# Verificar se o AWS CLI está instalado
if ! command aws --version &> /dev/null; then
  error "AWS CLI não está instalado. Instale-o antes de rodar este script."
fi

# Verificar se o Docker está instalado
if ! command docker --version &> /dev/null; then
  error "Docker não está instalado. Instale-o antes de rodar este script."
fi

# Verificar se o login no ECR é válido
log "Verificando login no ECR..."
if ! docker pull "$ECR_REPO:latest" > /dev/null 2>&1; then
  log "Token expirado ou ausente. Realizando login no ECR..."
  if aws ecr get-login-password --region "$ECR_REGION" | docker login --username AWS --password-stdin "$ECR_REPO"; then
    log "Login no ECR realizado com sucesso!"
  else
    error "Falha ao fazer login no ECR. Verifique suas credenciais e permissões."
  fi
else
  log "Login no ECR ainda é válido."
fi

# Subir os containers com docker-compose
log "Rodando o docker-compose..."
if docker-compose up "$@"; then
  log "Containers iniciados com sucesso!"
else
  error "Falha ao iniciar os containers."
fi
