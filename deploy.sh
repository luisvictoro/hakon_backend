#!/bin/bash

# Script de Deploy - Hakon Backend
# Este script facilita o processo de deploy das novas funcionalidades

echo "🚀 Iniciando deploy do Hakon Backend..."

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Instale o Python 3.8+ primeiro."
    exit 1
fi

# Verificar se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não encontrado. Instale o pip primeiro."
    exit 1
fi

echo "✅ Python e pip encontrados"

# Verificar se o arquivo .env existe
if [ ! -f ".env" ]; then
    echo "❌ Arquivo .env não encontrado. Crie o arquivo .env com as configurações do banco."
    exit 1
fi

echo "✅ Arquivo .env encontrado"

# Instalar dependências
echo "📦 Instalando dependências..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências"
    exit 1
fi

echo "✅ Dependências instaladas"

# Executar migração do banco
echo "🗄️ Executando migração do banco de dados..."
python3 migrate_database.py

if [ $? -ne 0 ]; then
    echo "❌ Erro na migração do banco"
    exit 1
fi

echo "✅ Migração concluída"

# Criar usuário admin se necessário
echo "👤 Verificando usuário admin..."
python3 create_admin_user.py

if [ $? -ne 0 ]; then
    echo "❌ Erro ao criar usuário admin"
    exit 1
fi

echo "✅ Usuário admin verificado"

# Testar importação do app
echo "🧪 Testando importação do app..."
python3 -c "from app.main import app; print('✅ App importado com sucesso')"

if [ $? -ne 0 ]; then
    echo "❌ Erro ao importar app"
    exit 1
fi

echo "✅ App importado com sucesso"

# Executar testes
echo "🧪 Executando testes..."
python3 test_new_features.py

if [ $? -ne 0 ]; then
    echo "❌ Erro nos testes"
    exit 1
fi

echo "✅ Testes passaram"

# Verificar se há processos rodando na porta 8000
echo "🔍 Verificando porta 8000..."
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️ Porta 8000 já está em uso. Parando processo anterior..."
    pkill -f uvicorn
    sleep 2
fi

# Iniciar servidor
echo "🚀 Iniciando servidor..."
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Aguardar servidor inicializar
sleep 5

# Testar se o servidor está respondendo
echo "🔍 Testando servidor..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)

if [ "$response" = "200" ]; then
    echo "✅ Servidor iniciado com sucesso!"
    echo ""
    echo "🎉 DEPLOY CONCLUÍDO COM SUCESSO!"
    echo ""
    echo "📋 Informações do deploy:"
    echo "   🌐 Servidor: http://localhost:8000"
    echo "   📚 Documentação: http://localhost:8000/docs"
    echo "   🔍 Health Check: http://localhost:8000/health"
    echo ""
    echo "🔐 Credenciais de acesso:"
    echo "   👤 Usuário: admin"
    echo "   🔑 Senha: admin"
    echo ""
    echo "📁 Arquivos de documentação criados:"
    echo "   📄 API_DOCUMENTATION.md - Documentação técnica"
    echo "   📄 FRONTEND_INTEGRATION_GUIDE.md - Guia de integração"
    echo "   📄 README_NEW_FEATURES.md - Resumo das funcionalidades"
    echo "   📄 IMPLEMENTATION_SUMMARY.md - Resumo final"
    echo ""
    echo "🚀 O backend está pronto para uso!"
else
    echo "❌ Erro ao iniciar servidor"
    exit 1
fi 