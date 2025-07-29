#!/usr/bin/env python3
"""
Script para testar a API de campos esperados
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
            token_data = response.json()
            return token_data.get("access_token")
        else:
            print(f"❌ Erro no login: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao obter token: {e}")
        return None

def test_expected_fields_api():
    """Testar a API de campos esperados"""
    print("🧪 Testando API de Campos Esperados")
    print("=" * 50)
    
    # Obter token
    token = get_auth_token()
    if not token:
        print("❌ Não foi possível obter token de autenticação")
        return
    
    print(f"✅ Token obtido: {token[:20]}...")
    
    # Testar endpoint
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/vulnerability/expected-fields",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API funcionando corretamente!")
            print()
            
            # Exibir campos obrigatórios
            print("📋 CAMPOS OBRIGATÓRIOS:")
            for field in data["required_fields"]:
                print(f"  • {field['name']} ({field['data_type']})")
                print(f"    Descrição: {field['description']}")
                print(f"    Exemplo: {field['example']}")
                print()
            
            # Exibir campos opcionais
            print("📋 CAMPOS OPCIONAIS:")
            for field in data["optional_fields"]:
                print(f"  • {field['name']} ({field['data_type']})")
                print(f"    Descrição: {field['description']}")
                print(f"    Exemplo: {field['example']}")
                print()
            
            # Exibir níveis de severidade
            print("📋 NÍVEIS DE SEVERIDADE ACEITOS:")
            for severity in data["severity_levels"]:
                print(f"  • {severity}")
            print()
            
            # Exibir exemplo de mapeamento
            print("📋 EXEMPLO DE MAPEAMENTO DE COLUNAS:")
            for csv_col, db_col in data["example_mapping"].items():
                print(f"  • '{csv_col}' → '{db_col}'")
            print()
            
            # Salvar resposta em arquivo JSON
            with open("expected_fields_response.json", "w") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print("💾 Resposta salva em 'expected_fields_response.json'")
            
        else:
            print(f"❌ Erro na API: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro ao testar API: {e}")

def test_without_auth():
    """Testar sem autenticação (deve retornar 401)"""
    print("\n🔒 Testando sem autenticação...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/vulnerability/expected-fields",
            timeout=10
        )
        
        if response.status_code == 401:
            print("✅ Proteção de autenticação funcionando corretamente")
        else:
            print(f"❌ Esperava 401, recebeu {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro no teste sem autenticação: {e}")

if __name__ == "__main__":
    test_expected_fields_api()
    test_without_auth()
    
    print("\n" + "=" * 50)
    print("�� Teste concluído!") 