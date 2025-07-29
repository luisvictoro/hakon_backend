#!/usr/bin/env python3
"""
Script simples para criar usuário admin via API HTTP
"""

import requests
import json

# URL do backend
BASE_URL = "https://hakon-56ae06ddc8d1.herokuapp.com"

def create_admin_user():
    """Criar usuário admin via API"""
    
    # Dados do usuário admin
    admin_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    print("=== Criando Usuário Admin ===")
    print(f"URL: {BASE_URL}/api/auth/register")
    print(f"Dados: {json.dumps(admin_data, indent=2)}")
    
    try:
        # Tentar criar o usuário admin
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json=admin_data,
            timeout=10
        )
        
        print(f"\nStatus: {response.status_code}")
        print(f"Resposta: {response.text}")
        
        if response.status_code == 200:
            print("\n✅ Usuário admin criado com sucesso!")
            print(f"Username: {admin_data['username']}")
            print(f"Password: {admin_data['password']}")
            return True
        elif response.status_code == 400:
            print("\n⚠️  Usuário admin já existe!")
            return True
        else:
            print(f"\n❌ Erro ao criar usuário admin: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Erro de conexão: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        return False

def test_admin_login():
    """Testar login do usuário admin"""
    
    admin_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    print("\n=== Testando Login do Admin ===")
    print(f"URL: {BASE_URL}/api/auth/login")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=admin_data,
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.text}")
        
        if response.status_code == 200:
            print("\n✅ Login do admin funcionando!")
            token_data = response.json()
            if "access_token" in token_data:
                print(f"Token: {token_data['access_token'][:20]}...")
            return True
        else:
            print(f"\n❌ Login do admin falhou: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"\n❌ Erro no teste de login: {e}")
        return False

if __name__ == "__main__":
    # Criar usuário admin
    success = create_admin_user()
    
    if success:
        # Testar login
        test_admin_login()
    
    print("\n=== Resumo ===")
    print("Credenciais do Admin:")
    print("Username: admin")
    print("Password: admin123")
    print(f"URL de Login: {BASE_URL}/api/auth/login") 