#!/bin/bash

# Script para fazer deploy das correções do backend

echo "=== Deploy das Correções do Backend - Hakon ==="
echo ""

# Verificar se estamos no diretório correto
if [ ! -f "app/main.py" ]; then
    echo "❌ Erro: Não estamos no diretório correto do projeto"
    echo "Execute este script no diretório raiz do projeto"
    exit 1
fi

# Verificar se o git está configurado
if ! git status > /dev/null 2>&1; then
    echo "❌ Erro: Git não está configurado neste diretório"
    exit 1
fi

echo "1. Verificando status do git..."
git status

echo ""
echo "2. Adicionando arquivos modificados..."
git add .

echo ""
echo "3. Fazendo commit das correções..."
git commit -m "fix: corrigir problema de login - aceitar JSON e form data

- Modificar endpoint /api/auth/login para aceitar JSON e form data
- Adicionar logging detalhado para debug
- Melhorar tratamento de erros
- Adicionar middleware de logging de requisições
- Configurar CORS adequadamente
- Criar scripts de teste para validação"

echo ""
echo "4. Fazendo push para o repositório..."
git push

echo ""
echo "5. Aguardando deploy no Heroku..."
echo "   O deploy pode levar alguns minutos..."
echo "   Você pode acompanhar o progresso em:"
echo "   https://dashboard.heroku.com/apps/hakon-56ae06ddc8d1/activity"

echo ""
echo "6. Testando endpoints após deploy..."
echo "   Aguarde alguns minutos e execute:"
echo "   python3 test_backend_fix.py"

echo ""
echo "✅ Deploy iniciado com sucesso!"
echo ""
echo "📋 Resumo das correções:"
echo "   - Endpoint /api/auth/login agora aceita JSON e form data"
echo "   - Logging detalhado adicionado"
echo "   - Tratamento de erros melhorado"
echo "   - CORS configurado adequadamente"
echo "   - Scripts de teste criados"
echo ""
echo "🔍 Para monitorar logs:"
echo "   heroku logs --tail -a hakon-56ae06ddc8d1"