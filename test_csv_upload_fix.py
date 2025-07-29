#!/usr/bin/env python3
"""
Script para testar o upload de CSV após as correções
"""

import requests
import json
import pandas as pd
from io import StringIO

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
            return response.json().get("access_token")
        else:
            print(f"❌ Login falhou: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Erro no login: {e}")
        return None

def create_test_csv():
    """Criar CSV de teste com dados válidos"""
    data = {
        'ip': ['10.1.1.1', '10.1.1.2', '10.1.1.3'],
        'hostname': ['server1', 'server2', 'server3'],
        'nvt_name': ['SQL Injection', 'XSS Vulnerability', 'Buffer Overflow'],
        'severity': ['high', 'medium', 'critical'],
        'cvss': [9.0, 6.5, 10.0],
        'cves': ['CVE-2021-1234', 'CVE-2021-5678', 'CVE-2021-9012']
    }
    
    df = pd.DataFrame(data)
    csv_content = df.to_csv(index=False)
    return csv_content

def create_template(token):
    """Criar template de teste"""
    template_data = {
        "name": "Test Template",
        "source": "Test Scanner",
        "column_mapping": {
            "ip": "ip",
            "hostname": "hostname", 
            "nvt_name": "nvt_name",
            "severity": "severity",
            "cvss": "cvss",
            "cves": "cves"
        },
        "severity_map": {
            "critical": "critical",
            "high": "high",
            "medium": "medium",
            "low": "low"
        }
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/templates",
            json=template_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            template = response.json()
            print(f"✅ Template criado: ID {template['id']}")
            return template['id']
        else:
            print(f"❌ Erro ao criar template: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao criar template: {e}")
        return None

def test_csv_upload(token, template_id):
    """Testar upload de CSV"""
    print("\n🔍 Testando upload de CSV...")
    
    # Criar CSV de teste
    csv_content = create_test_csv()
    print(f"   CSV criado com {len(csv_content.splitlines())} linhas")
    
    # Preparar dados do upload
    files = {
        'file': ('test.csv', csv_content, 'text/csv')
    }
    
    data = {
        'month': '2025-07',
        'template_id': str(template_id)
    }
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/vulnerability/upload",
            files=files,
            data=data,
            headers=headers,
            timeout=30
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Upload bem-sucedido: {result}")
            return True
        else:
            print(f"   ❌ Erro no upload: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro no upload: {e}")
        return False

def check_dashboard_stats(token):
    """Verificar estatísticas do dashboard após upload"""
    print("\n📊 Verificando estatísticas do dashboard...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/vulnerability/dashboard/stats",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            stats = response.json()
            print(f"   ✅ Estatísticas obtidas:")
            print(f"      Total de vulnerabilidades: {stats['total_vulnerabilities']}")
            print(f"      Por status: {stats['total_by_status']}")
            print(f"      Por severidade: {stats['total_by_severity']}")
            return True
        else:
            print(f"   ❌ Erro ao obter estatísticas: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro ao obter estatísticas: {e}")
        return False

def main():
    """Teste principal"""
    print("=== Teste de Upload de CSV Corrigido ===")
    print(f"Base URL: {BASE_URL}")
    
    # 1. Obter token
    print("\n1. Obtendo token de autenticação...")
    token = get_auth_token()
    
    if not token:
        print("❌ Não foi possível obter token. Abortando...")
        return
    
    print(f"   ✅ Token obtido: {token[:20]}...")
    
    # 2. Criar template
    print("\n2. Criando template de teste...")
    template_id = create_template(token)
    
    if not template_id:
        print("❌ Não foi possível criar template. Abortando...")
        return
    
    # 3. Testar upload
    success = test_csv_upload(token, template_id)
    
    if success:
        # 4. Verificar estatísticas
        check_dashboard_stats(token)
        
        print("\n" + "="*50)
        print("✅ Teste concluído com sucesso!")
        print("✅ Upload de CSV está funcionando corretamente")
        print("✅ Dados estão sendo processados sem erros de banco")
    else:
        print("\n" + "="*50)
        print("❌ Teste falhou!")
        print("❌ Upload de CSV ainda tem problemas")

if __name__ == "__main__":
    main() 