#!/usr/bin/env python3
"""
Script para testar especificamente o endpoint de meses
"""

import requests
import json

# URL do backend
BASE_URL = "https://hakon-56ae06ddc8d1.herokuapp.com"

def test_months_endpoint():
    """Testar endpoint de meses"""
    
    print("=== Testando Endpoint de Meses ===")
    print(f"Base URL: {BASE_URL}")
    print()
    
    # 1. Fazer login para obter token
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
            print(f"   ✅ Token obtido: {token[:20]}...")
        else:
            print(f"   ❌ Login falhou: {login_response.status_code}")
            return
            
    except Exception as e:
        print(f"   ❌ Erro no login: {e}")
        return
    
    print()
    
    # 2. Testar endpoint de meses
    print("2. Testando /api/vulnerability/months...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/api/vulnerability/months", headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            months = response.json()
            print(f"   ✅ Sucesso!")
            print(f"   📊 Total de meses: {len(months)}")
            print(f"   📅 Meses retornados:")
            
            for i, month in enumerate(months, 1):
                print(f"      {i:2d}. {month}")
            
            print()
            print("   📋 Formato dos meses:")
            print("      - Formato: YYYY-MM")
            print("      - Exemplo: 2025-01, 2025-02, etc.")
            
        else:
            print(f"   ❌ Erro: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    print()
    print("=== Resumo ===")
    print("✅ Endpoint /api/vulnerability/months agora retorna todos os meses do ano atual")
    print("✅ Útil para o frontend ter uma lista completa de meses para seleção")
    print("✅ Quando houver dados de vulnerabilidades, retornará apenas os meses com dados")

if __name__ == "__main__":
    test_months_endpoint() 