#!/usr/bin/env python3
"""
Script para testar diferentes senhas do usuário admin
"""

import requests
import json

# URL do backend
BASE_URL = "https://hakon-56ae06ddc8d1.herokuapp.com"

def test_admin_login(password):
    """Testar login do admin com uma senha específica"""
    
    admin_data = {
        "username": "admin",
        "password": password
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=admin_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"✅ SENHA ENCONTRADA: '{password}'")
            token_data = response.json()
            if "access_token" in token_data:
                print(f"   Token: {token_data['access_token'][:20]}...")
            return True
        else:
            print(f"❌ Senha '{password}' - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro testando senha '{password}': {e}")
        return False

def main():
    """Testar várias senhas comuns"""
    
    print("=== Testando Senhas do Admin ===")
    print(f"Username: admin")
    print(f"URL: {BASE_URL}/api/auth/login")
    print()
    
    # Lista de senhas para testar
    passwords = [
        "admin",
        "admin123", 
        "password",
        "123456",
        "Hk18133329@",  # Senha que apareceu nos logs
        "hakon",
        "hakon123",
        "test",
        "test123"
    ]
    
    found = False
    
    for password in passwords:
        if test_admin_login(password):
            found = True
            break
    
    if not found:
        print("\n❌ Nenhuma senha funcionou!")
        print("Você pode tentar criar um novo usuário admin com:")
        print("python3 create_admin_simple.py")
    
    print("\n=== Resumo ===")
    print("Se encontrou a senha, use essas credenciais no frontend:")
    print("Username: admin")
    print("Password: [senha encontrada acima]")

if __name__ == "__main__":
    main() 