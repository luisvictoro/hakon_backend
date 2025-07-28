#!/bin/bash

# Script para verificar status do Heroku

echo "=== Verificando Status do Heroku ==="
echo ""

# Verificar se o Heroku CLI está instalado
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI não está instalado"
    echo "Instale com: curl https://cli-assets.heroku.com/install.sh | sh"
    exit 1
fi

echo "1. Verificando status da aplicação..."
heroku ps -a hakon-56ae06ddc8d1

echo ""
echo "2. Verificando logs recentes..."
heroku logs --tail -n 50 -a hakon-56ae06ddc8d1

echo ""
echo "3. Verificando variáveis de ambiente..."
heroku config -a hakon-56ae06ddc8d1

echo ""
echo "4. Verificando build logs..."
heroku builds -a hakon-56ae06ddc8d1

echo ""
echo "✅ Verificação concluída!"