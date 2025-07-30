#!/usr/bin/env python3
"""
Test script for hash-based vulnerability update routes
"""

import requests
import json
import sys

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

def get_vulnerabilities(token):
    """Get list of vulnerabilities to find a hash"""
    print("📋 Buscando vulnerabilidades...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{VULN_URL}/list", headers=headers)
        response.raise_for_status()
        
        vulns = response.json()
        if not vulns:
            print("❌ Nenhuma vulnerabilidade encontrada")
            return None
            
        print(f"✅ Encontradas {len(vulns)} vulnerabilidades")
        return vulns[0]  # Return first vulnerability
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao buscar vulnerabilidades: {e}")
        return None

def test_severity_change_by_hash(token, vuln_hash):
    """Test severity change using hash"""
    print(f"🔧 Testando mudança de severidade por hash: {vuln_hash[:16]}...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test data
    change_data = {
        "severity": "Critical",
        "reason": "Teste via hash"
    }
    
    try:
        response = requests.put(
            f"{VULN_URL}/hash/{vuln_hash}/severity",
            headers=headers,
            json=change_data
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Mudança de severidade por hash funcionou!")
            return True
        else:
            print("❌ Erro na mudança de severidade por hash")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
        return False

def test_status_change_by_hash(token, vuln_hash):
    """Test status change using hash"""
    print(f"🔧 Testando mudança de status por hash: {vuln_hash[:16]}...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test data
    change_data = {
        "status": "ongoing",
        "reason": "Teste via hash"
    }
    
    try:
        response = requests.put(
            f"{VULN_URL}/hash/{vuln_hash}/status",
            headers=headers,
            json=change_data
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Mudança de status por hash funcionou!")
            return True
        else:
            print("❌ Erro na mudança de status por hash")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
        return False

def test_original_routes(token, vuln_id):
    """Test original ID-based routes for comparison"""
    print(f"🔧 Testando rotas originais com ID: {vuln_id}")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test severity change
    change_data = {
        "severity": "High",
        "reason": "Teste via ID"
    }
    
    try:
        response = requests.put(
            f"{VULN_URL}/{vuln_id}/severity",
            headers=headers,
            json=change_data
        )
        
        print(f"📊 Severity Change Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Rota original de severidade funcionou!")
        else:
            print("❌ Erro na rota original de severidade")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição original: {e}")

def main():
    """Main test function"""
    print("🧪 Testando rotas baseadas em hash para vulnerabilidades")
    print("=" * 60)
    
    # Login
    token = login()
    if not token:
        print("❌ Falha no login. Abortando testes.")
        sys.exit(1)
    
    # Get vulnerabilities
    vuln = get_vulnerabilities(token)
    if not vuln:
        print("❌ Nenhuma vulnerabilidade encontrada. Abortando testes.")
        sys.exit(1)
    
    vuln_hash = vuln.get("vuln_hash")
    vuln_id = vuln.get("id")
    
    print(f"📋 Vulnerabilidade de teste:")
    print(f"   ID: {vuln_id}")
    print(f"   Hash: {vuln_hash}")
    print(f"   Severidade atual: {vuln.get('severity')}")
    print(f"   Status atual: {vuln.get('status')}")
    print()
    
    # Test hash-based routes
    print("🔧 TESTANDO ROTAS BASEADAS EM HASH")
    print("-" * 40)
    
    severity_success = test_severity_change_by_hash(token, vuln_hash)
    print()
    
    status_success = test_status_change_by_hash(token, vuln_hash)
    print()
    
    # Test original routes for comparison
    print("🔧 TESTANDO ROTAS ORIGINAIS (COMPARAÇÃO)")
    print("-" * 40)
    test_original_routes(token, vuln_id)
    print()
    
    # Summary
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    print(f"✅ Mudança de severidade por hash: {'PASSOU' if severity_success else 'FALHOU'}")
    print(f"✅ Mudança de status por hash: {'PASSOU' if status_success else 'FALHOU'}")
    print()
    
    if severity_success and status_success:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ As rotas baseadas em hash estão funcionando corretamente")
    else:
        print("❌ ALGUNS TESTES FALHARAM")
        print("🔍 Verifique os logs acima para mais detalhes")
    
    print()
    print("📋 URLs das novas rotas:")
    print(f"   PUT {VULN_URL}/hash/{{vuln_hash}}/severity")
    print(f"   PUT {VULN_URL}/hash/{{vuln_hash}}/status")

if __name__ == "__main__":
    main() 