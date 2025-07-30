#!/usr/bin/env python3
"""
Simple test to change severity without manual change history
"""

import requests
import json

# Configuration
BASE_URL = "https://hakon-56ae06ddc8d1.herokuapp.com"
LOGIN_URL = f"{BASE_URL}/api/auth/login"
VULN_URL = f"{BASE_URL}/api/vulnerability"

def login():
    """Login to get access token"""
    print("🔐 Fazendo login...")
    
    login_data = {
        "username": "admin",
        "password": "admin"
    }
    
    try:
        response = requests.post(LOGIN_URL, json=login_data)
        response.raise_for_status()
        
        token = response.json().get("access_token")
        if not token:
            print("❌ Token não encontrado na resposta")
            return None
            
        print("✅ Login realizado com sucesso")
        return token
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro no login: {e}")
        return None

def test_simple_severity_change(token):
    """Test a simple severity change without manual change history"""
    print("🔧 Testando mudança simples de severidade...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Get a vulnerability first
    try:
        response = requests.get(f"{VULN_URL}/list", headers=headers)
        response.raise_for_status()
        
        vulns = response.json()
        if not vulns:
            print("❌ Nenhuma vulnerabilidade encontrada")
            return False
            
        vuln = vulns[0]
        vuln_id = vuln.get("id")
        vuln_hash = vuln.get("vuln_hash")
        
        print(f"📋 Testando com vulnerabilidade ID: {vuln_id}, Hash: {vuln_hash[:16]}...")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao buscar vulnerabilidades: {e}")
        return False
    
    # Test the original ID-based route
    change_data = {
        "severity": "High",
        "reason": "Teste simples"
    }
    
    try:
        response = requests.put(
            f"{VULN_URL}/{vuln_id}/severity",
            headers=headers,
            json=change_data
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Mudança de severidade funcionou!")
            return True
        else:
            print("❌ Erro na mudança de severidade")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Teste simples de mudança de severidade")
    print("=" * 50)
    
    # Login
    token = login()
    if not token:
        print("❌ Falha no login. Abortando testes.")
        return
    
    # Test simple severity change
    success = test_simple_severity_change(token)
    
    print()
    if success:
        print("🎉 Teste passou!")
    else:
        print("❌ Teste falhou")

if __name__ == "__main__":
    main() 