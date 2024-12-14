#!/bin/bash

# Configurações
ECR_REPO="my-app"
GITHUB_OWNER="owner"
GITHUB_REPO="repo"
GITHUB_TOKEN="your-github-token"

# Função para listar branches ativas no GitHub
list_active_branches() {
  curl -s -H "Authorization: token $GITHUB_TOKEN" \
    "https://api.github.com/repos/$GITHUB_OWNER/$GITHUB_REPO/branches" | jq -r '.[].name'
}

# Função para listar imagens no ECR
list_ecr_images() {
  aws ecr list-images --repository-name $ECR_REPO --query 'imageIds[*].imageTag' --output text
}

# Função para deletar imagem no ECR
delete_ecr_image() {
  local tag=$1
  echo "Deletando imagem: $tag"
  aws ecr batch-delete-image --repository-name $ECR_REPO --image-ids imageTag=$tag
}

# Passo 1: Obter branches ativas e imagens no ECR
active_branches=$(list_active_branches)
ecr_images=$(list_ecr_images)

# Passo 2: Identificar imagens "orfãs"
for image in $ecr_images; do
  if [[ ! "$active_branches" =~ $image ]] && [[ "$image" != "latest" ]] && [[ "$image" != "desenv" ]]; then
    delete_ecr_image $image
  fi
done
