#!/usr/bin/env python3
"""
Script para debugar o problema de upload do frontend
"""

import requests
import json

# URL do backend
BASE_URL = "https://hakon-56ae06ddc8d1.herokuapp.com"

def get_auth_token():
    """Obter token de autenticação"""
    login_data = {
        "username": "admin",
        "password": "admin"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            print(f"❌ Login falhou: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Erro no login: {e}")
        return None

def test_template_exists(token, template_id):
    """Verificar se o template existe"""
    print(f"\n🔍 Verificando se template ID {template_id} existe...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/templates/{template_id}",
            headers=headers,
            timeout=10
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            template = response.json()
            print(f"   ✅ Template encontrado: {template['name']}")
            return True
        elif response.status_code == 404:
            print(f"   ❌ Template ID {template_id} não encontrado")
            return False
        else:
            print(f"   ❌ Erro: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def test_upload_with_binary_file(token, template_id):
    """Testar upload com arquivo binário (simulando frontend)"""
    print(f"\n🔍 Testando upload com arquivo binário...")
    
    # Criar um arquivo binário simples
    binary_content = b"This is a binary file content for testing"
    
    files = {
        'file': ('test.bin', binary_content, 'application/octet-stream')
    }
    
    data = {
        'month': '2025-07',
        'template_id': str(template_id)
    }
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/vulnerability/upload",
            files=files,
            data=data,
            headers=headers,
            timeout=30
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print(f"   ✅ Upload bem-sucedido")
            return True
        else:
            print(f"   ❌ Erro no upload")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro no upload: {e}")
        return False

def test_upload_with_invalid_csv(token, template_id):
    """Testar upload com CSV inválido"""
    print(f"\n🔍 Testando upload com CSV inválido...")
    
    # CSV com dados malformados
    invalid_csv = "ip,hostname,nvt_name,severity,cvss,cves\ninvalid_ip,server1,SQL Injection,high,9.0,CVE-2021-1234"
    
    files = {
        'file': ('test.csv', invalid_csv, 'text/csv')
    }
    
    data = {
        'month': '2025-07',
        'template_id': str(template_id)
    }
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/vulnerability/upload",
            files=files,
            data=data,
            headers=headers,
            timeout=30
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        return response.status_code, response.text
            
    except Exception as e:
        print(f"   ❌ Erro no upload: {e}")
        return None, str(e)

def test_upload_with_missing_fields(token, template_id):
    """Testar upload com campos faltando"""
    print(f"\n🔍 Testando upload com campos faltando...")
    
    # Teste 1: Sem template_id
    print("   Teste 1: Sem template_id")
    files = {
        'file': ('test.csv', 'ip,hostname\n10.1.1.1,server1', 'text/csv')
    }
    
    data = {
        'month': '2025-07'
        # template_id faltando
    }
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/vulnerability/upload",
            files=files,
            data=data,
            headers=headers,
            timeout=30
        )
        
        print(f"      Status: {response.status_code}")
        print(f"      Response: {response.text}")
        
    except Exception as e:
        print(f"      ❌ Erro: {e}")
    
    # Teste 2: Sem month
    print("   Teste 2: Sem month")
    files = {
        'file': ('test.csv', 'ip,hostname\n10.1.1.1,server1', 'text/csv')
    }
    
    data = {
        'template_id': str(template_id)
        # month faltando
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/vulnerability/upload",
            files=files,
            data=data,
            headers=headers,
            timeout=30
        )
        
        print(f"      Status: {response.status_code}")
        print(f"      Response: {response.text}")
        
    except Exception as e:
        print(f"      ❌ Erro: {e}")

def main():
    """Teste principal"""
    print("=== Debug do Upload do Frontend ===")
    print(f"Base URL: {BASE_URL}")
    
    # 1. Obter token
    print("\n1. Obtendo token de autenticação...")
    token = get_auth_token()
    
    if not token:
        print("❌ Não foi possível obter token. Abortando...")
        return
    
    print(f"   ✅ Token obtido: {token[:20]}...")
    
    # 2. Verificar template ID 5
    template_id = 5
    template_exists = test_template_exists(token, template_id)
    
    if not template_exists:
        print(f"\n❌ Template ID {template_id} não existe!")
        print("   Isso pode ser a causa do erro 400.")
        print("   O frontend está tentando usar um template que não existe.")
        return
    
    # 3. Testar upload com arquivo binário
    test_upload_with_binary_file(token, template_id)
    
    # 4. Testar upload com CSV inválido
    status, response = test_upload_with_invalid_csv(token, template_id)
    
    # 5. Testar upload com campos faltando
    test_upload_with_missing_fields(token, template_id)
    
    print("\n" + "="*50)
    print("📋 Possíveis causas do erro 400:")
    print("1. Template ID 5 não existe")
    print("2. Arquivo não é um CSV válido")
    print("3. Campos obrigatórios faltando (month, template_id)")
    print("4. Formato do arquivo incorreto")
    print("5. Dados do CSV não correspondem ao template")

if __name__ == "__main__":
    main() 