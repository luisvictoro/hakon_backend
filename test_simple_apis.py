#!/usr/bin/env python3
"""
Test script for the new simplified APIs using IDs
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

def test_severity_options(token):
    """Test severity options API"""
    print("🔧 Testando API de opções de severidade...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{VULN_URL}/severity-options", headers=headers)
        response.raise_for_status()
        
        data = response.json()
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200:
            print("✅ API de opções de severidade funcionou!")
            return data.get("severity_options", [])
        else:
            print("❌ Erro na API de opções de severidade")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
        return []

def test_status_options(token):
    """Test status options API"""
    print("🔧 Testando API de opções de status...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{VULN_URL}/status-options", headers=headers)
        response.raise_for_status()
        
        data = response.json()
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200:
            print("✅ API de opções de status funcionou!")
            return data.get("status_options", [])
        else:
            print("❌ Erro na API de opções de status")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
        return []

def get_vulnerability_for_test(token):
    """Get a vulnerability for testing"""
    print("📋 Buscando vulnerabilidade para teste...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{VULN_URL}/list", headers=headers)
        response.raise_for_status()
        
        vulns = response.json()
        if not vulns:
            print("❌ Nenhuma vulnerabilidade encontrada")
            return None
            
        vuln = vulns[0]
        print(f"✅ Vulnerabilidade encontrada: ID {vuln.get('id')}")
        return vuln
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao buscar vulnerabilidades: {e}")
        return None

def test_severity_change_simple(token, vuln_id):
    """Test simple severity change using ID"""
    print(f"🔧 Testando mudança de severidade simples (ID: {vuln_id})...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test with severity_id = 1 (Critical)
    try:
        response = requests.put(
            f"{VULN_URL}/{vuln_id}/severity-simple?severity_id=1",
            headers=headers
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Mudança de severidade simples funcionou!")
            return True
        else:
            print("❌ Erro na mudança de severidade simples")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
        return False

def test_status_change_simple(token, vuln_id):
    """Test simple status change using ID"""
    print(f"🔧 Testando mudança de status simples (ID: {vuln_id})...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test with status_id = 2 (ongoing)
    try:
        response = requests.put(
            f"{VULN_URL}/{vuln_id}/status-simple?status_id=2",
            headers=headers
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Mudança de status simples funcionou!")
            return True
        else:
            print("❌ Erro na mudança de status simples")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testando APIs simplificadas com IDs")
    print("=" * 50)
    
    # Login
    token = login()
    if not token:
        print("❌ Falha no login. Abortando testes.")
        return
    
    print()
    
    # Test options APIs
    print("📋 TESTANDO APIS DE OPÇÕES")
    print("-" * 30)
    
    severity_options = test_severity_options(token)
    print()
    
    status_options = test_status_options(token)
    print()
    
    # Get vulnerability for testing
    vuln = get_vulnerability_for_test(token)
    if not vuln:
        print("❌ Nenhuma vulnerabilidade encontrada. Abortando testes.")
        return
    
    vuln_id = vuln.get("id")
    print()
    
    # Test simple change APIs
    print("🔧 TESTANDO APIS DE MUDANÇA SIMPLES")
    print("-" * 30)
    
    severity_success = test_severity_change_simple(token, vuln_id)
    print()
    
    status_success = test_status_change_simple(token, vuln_id)
    print()
    
    # Summary
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    print(f"✅ API de opções de severidade: {'PASSOU' if severity_options else 'FALHOU'}")
    print(f"✅ API de opções de status: {'PASSOU' if status_options else 'FALHOU'}")
    print(f"✅ Mudança de severidade simples: {'PASSOU' if severity_success else 'FALHOU'}")
    print(f"✅ Mudança de status simples: {'PASSOU' if status_success else 'FALHOU'}")
    print()
    
    if severity_options and status_options and severity_success and status_success:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ As APIs simplificadas estão funcionando corretamente")
    else:
        print("❌ ALGUNS TESTES FALHARAM")
        print("🔍 Verifique os logs acima para mais detalhes")
    
    print()
    print("📋 URLs das novas APIs:")
    print(f"   GET {VULN_URL}/severity-options")
    print(f"   GET {VULN_URL}/status-options")
    print(f"   PUT {VULN_URL}/{{vulnerability_id}}/severity-simple?severity_id={{1-5}}")
    print(f"   PUT {VULN_URL}/{{vulnerability_id}}/status-simple?status_id={{1-4}}")
    print()
    print("📋 Mapeamento de IDs:")
    print("   Severidade: 1=Critical, 2=High, 3=Medium, 4=Low, 5=Info")
    print("   Status: 1=new, 2=ongoing, 3=reopened, 4=closed")

if __name__ == "__main__":
    main() 