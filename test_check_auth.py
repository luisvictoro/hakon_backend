#!/usr/bin/env python3
"""
Script para testar o endpoint check-auth
"""

import requests
import json

# URL do backend
BASE_URL = "https://hakon-56ae06ddc8d1.herokuapp.com"

def test_login_and_check_auth():
    """Testar login e depois check-auth"""
    
    print("=== Testando Login e Check-Auth ===")
    print(f"Base URL: {BASE_URL}")
    print()
    
    # 1. Fazer login
    print("1. Fazendo login...")
    login_data = {
        "username": "admin",
        "password": "admin"
    }
    
    try:
        login_response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data,
            timeout=10
        )
        
        print(f"   Status: {login_response.status_code}")
        print(f"   Resposta: {login_response.text}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            token = token_data.get("access_token")
            print(f"   ✅ Token obtido: {token[:20] if token else 'Nenhum'}...")
        else:
            print("   ❌ Login falhou")
            return
            
    except Exception as e:
        print(f"   ❌ Erro no login: {e}")
        return
    
    print()
    
    # 2. Testar check-auth sem token
    print("2. Testando check-auth SEM token...")
    try:
        response = requests.get(f"{BASE_URL}/api/auth/check-auth", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Resposta: {response.text}")
        
        if response.status_code == 401:
            print("   ⚠️  Requer autenticação (esperado)")
        else:
            print("   ❌ Deveria retornar 401")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    print()
    
    # 3. Testar check-auth COM token
    print("3. Testando check-auth COM token...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/api/auth/check-auth", headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Resposta: {response.text}")
        
        if response.status_code == 200:
            user_data = response.json()
            print("   ✅ Check-auth funcionou!")
            print(f"   📊 Usuário: {json.dumps(user_data, indent=2)}")
        else:
            print(f"   ❌ Erro: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    print()
    
    # 4. Testar com token inválido
    print("4. Testando check-auth com token inválido...")
    invalid_headers = {
        "Authorization": "Bearer invalid_token_123",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/api/auth/check-auth", headers=invalid_headers, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Resposta: {response.text}")
        
        if response.status_code == 401:
            print("   ⚠️  Token inválido rejeitado (esperado)")
        else:
            print("   ❌ Deveria rejeitar token inválido")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    print()
    print("=== Resumo ===")
    print("Para usar check-auth no frontend:")
    print("1. Fazer login para obter token")
    print("2. Incluir token no header: Authorization: Bearer <token>")
    print("3. Fazer GET para /api/auth/check-auth")

if __name__ == "__main__":
    test_login_and_check_auth() 