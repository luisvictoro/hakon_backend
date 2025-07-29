#!/usr/bin/env python3
"""
Script para debugar validação de token JWT
"""

import requests
import json
import jwt
from datetime import datetime

# URL do backend
BASE_URL = "https://hakon-56ae06ddc8d1.herokuapp.com"

def decode_token(token):
    """Decodificar token JWT (sem verificar assinatura)"""
    try:
        # Decodificar sem verificar para ver o conteúdo
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload
    except Exception as e:
        return f"Erro ao decodificar: {e}"

def test_token_validation():
    """Testar validação de token"""
    
    print("=== Debug Token JWT ===")
    print(f"Base URL: {BASE_URL}")
    print()
    
    # 1. Fazer login e obter token
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
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            token = token_data.get("access_token")
            print(f"   ✅ Token obtido: {token[:50]}...")
            
            # Decodificar token para ver conteúdo
            payload = decode_token(token)
            print(f"   📊 Payload do token: {json.dumps(payload, indent=2)}")
            
            # Verificar expiração
            if 'exp' in payload:
                exp_timestamp = payload['exp']
                exp_date = datetime.fromtimestamp(exp_timestamp)
                now = datetime.now()
                print(f"   ⏰ Expira em: {exp_date}")
                print(f"   ⏰ Agora: {now}")
                print(f"   ⏰ Válido: {exp_date > now}")
            
        else:
            print(f"   ❌ Login falhou: {login_response.status_code}")
            return
            
    except Exception as e:
        print(f"   ❌ Erro no login: {e}")
        return
    
    print()
    
    # 2. Testar token com diferentes endpoints
    print("2. Testando token com diferentes endpoints...")
    
    endpoints = [
        "/api/auth/check-auth",
        "/api/vulnerability/months",
        "/api/vulnerability/uploads"
    ]
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    for endpoint in endpoints:
        print(f"\n   Testando {endpoint}...")
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
            print(f"      Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"      ✅ Sucesso - {len(data)} itens")
                else:
                    print(f"      ✅ Sucesso - {json.dumps(data, indent=6)}")
            else:
                print(f"      ❌ Erro: {response.text}")
                
        except Exception as e:
            print(f"      ❌ Erro: {e}")
    
    print()
    
    # 3. Testar token expirado (simular)
    print("3. Testando comportamento com token expirado...")
    
    # Criar um token que expira em 1 segundo
    import time
    expired_payload = {
        "sub": "admin",
        "exp": int(time.time()) + 1  # Expira em 1 segundo
    }
    
    # Nota: Não podemos criar um token válido sem a chave secreta
    # Mas podemos testar o comportamento com token inválido
    expired_headers = {
        "Authorization": "Bearer expired_token_123",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/api/auth/check-auth", headers=expired_headers, timeout=10)
        print(f"   Status com token inválido: {response.status_code}")
        print(f"   Resposta: {response.text}")
        
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    print()
    print("=== Resumo ===")
    print("Se o token está sendo rejeitado no frontend, verifique:")
    print("1. Se o token está sendo enviado corretamente no header")
    print("2. Se não há problemas de CORS")
    print("3. Se o token não expirou")
    print("4. Se há diferenças de timezone")

if __name__ == "__main__":
    test_token_validation() 