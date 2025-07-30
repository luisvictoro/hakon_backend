#!/usr/bin/env python3
"""
Test the original issue that was causing 422 error
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

def test_original_issue(token):
    """Test the original URL that was failing"""
    print("🔧 Testando o problema original...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # The original failing request
    vuln_hash = "33a2067962fe1d6bb65980fe02558da19faba41a6f495064bbe33ac4e45f916a"
    change_data = {
        "severity": "Critical"
    }
    
    print(f"📋 Testando URL: {VULN_URL}/hash/{vuln_hash}/severity")
    print(f"📋 Dados: {change_data}")
    
    try:
        response = requests.put(
            f"{VULN_URL}/hash/{vuln_hash}/severity",
            headers=headers,
            json=change_data
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Problema original resolvido!")
            return True
        elif response.status_code == 422:
            print("❌ Ainda há erro 422 (Unprocessable Entity)")
            return False
        else:
            print(f"❌ Erro diferente: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testando o problema original (422 error)")
    print("=" * 50)
    
    # Login
    token = login()
    if not token:
        print("❌ Falha no login. Abortando testes.")
        return
    
    # Test original issue
    success = test_original_issue(token)
    
    print()
    if success:
        print("🎉 O problema original foi resolvido!")
    else:
        print("❌ O problema ainda persiste")

if __name__ == "__main__":
    main() 