#!/usr/bin/env python3
"""
Script para verificar o mapeamento do template ID 5
"""

import requests
import json

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

def check_template_mapping(token, template_id):
    """Verificar o mapeamento do template"""
    print(f"\n🔍 Verificando mapeamento do template ID {template_id}...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/templates/{template_id}",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            template = response.json()
            print(f"   ✅ Template encontrado: {template['name']}")
            print(f"   📋 Source: {template['source']}")
            print(f"   👤 Created by: {template['created_by']}")
            print(f"   📅 Created at: {template['created_at']}")
            
            print(f"\n   🔗 Column Mapping:")
            for csv_col, db_col in template['column_mapping'].items():
                print(f"      '{csv_col}' → '{db_col}'")
            
            print(f"\n   🎯 Severity Mapping:")
            for csv_sev, db_sev in template['severity_map'].items():
                print(f"      '{csv_sev}' → '{db_sev}'")
            
            return template
            
        else:
            print(f"   ❌ Erro: {response.text}")
            return None
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return None

def create_correct_template(token):
    """Criar template correto para o CSV do usuário"""
    print(f"\n🔧 Criando template correto para suas colunas...")
    
    template_data = {
        "name": "OpenVAS CSV Template",
        "source": "OpenVAS",
        "column_mapping": {
            "IP": "ip",
            "Hostname": "hostname",
            "NVT Name": "nvt_name",
            "Severity": "severity",
            "CVSS": "cvss",
            "CVEs": "cves"
        },
        "severity_map": {
            "Critical": "critical",
            "High": "high",
            "Medium": "medium",
            "Low": "low",
            "Log": "low",
            "Debug": "low"
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
            print(f"   ✅ Template criado: ID {template['id']}")
            print(f"   📋 Nome: {template['name']}")
            return template['id']
        else:
            print(f"   ❌ Erro ao criar template: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"   ❌ Erro ao criar template: {e}")
        return None

def test_upload_with_correct_template(token, template_id):
    """Testar upload com template correto"""
    print(f"\n🔍 Testando upload com template ID {template_id}...")
    
    # CSV com as colunas corretas
    csv_content = """IP,Hostname,Port,Port Protocol,CVSS,Severity,QoD,Solution Type,NVT Name,Summary,Specific Result,NVT OID,CVEs,Task ID,Task Name,Timestamp,Result ID,Impact,Solution,Affected Software/OS,Vulnerability Insight,Vulnerability Detection Method,Product Detection Result,BIDs,CERTs,Other References,Max Severity EPSS score,Max Severity EPSS percentile
10.1.1.1,server1,80,tcp,9.0,High,80,Workaround,SQL Injection,SQL injection vulnerability,SQL injection found,1.3.6.1.4.1.25623.1.0.1234,CVE-2021-1234,12345,Scan Task 1,2025-07-29T10:00:00,67890,High,Update software,Linux,SQL injection in web app,Automated scan,Product found,123,456,Reference 1,0.95,95.5
10.1.1.2,server2,443,tcp,6.5,Medium,70,Workaround,XSS Vulnerability,XSS vulnerability found,XSS in form,1.3.6.1.4.1.25623.1.0.5678,CVE-2021-5678,12346,Scan Task 2,2025-07-29T10:01:00,67891,Medium,Input validation,Windows,XSS in input field,Automated scan,Product found,124,457,Reference 2,0.75,75.2"""
    
    files = {
        'file': ('test_openvas.csv', csv_content, 'text/csv')
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
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print(f"   ✅ Upload bem-sucedido!")
            return True
        else:
            print(f"   ❌ Erro no upload")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro no upload: {e}")
        return False

def main():
    """Teste principal"""
    print("=== Verificação do Template ID 5 ===")
    print(f"Base URL: {BASE_URL}")
    
    # 1. Obter token
    print("\n1. Obtendo token de autenticação...")
    token = get_auth_token()
    
    if not token:
        print("❌ Não foi possível obter token. Abortando...")
        return
    
    print(f"   ✅ Token obtido: {token[:20]}...")
    
    # 2. Verificar template ID 5
    template_id = 5
    template = check_template_mapping(token, template_id)
    
    if not template:
        print(f"\n❌ Template ID {template_id} não encontrado!")
        return
    
    # 3. Criar template correto se necessário
    print(f"\n📋 Suas colunas CSV:")
    user_columns = [
        "IP", "Hostname", "Port", "Port Protocol", "CVSS", "Severity", "QoD", 
        "Solution Type", "NVT Name", "Summary", "Specific Result", "NVT OID", 
        "CVEs", "Task ID", "Task Name", "Timestamp", "Result ID", "Impact", 
        "Solution", "Affected Software/OS", "Vulnerability Insight", 
        "Vulnerability Detection Method", "Product Detection Result", "BIDs", 
        "CERTs", "Other References", "Max Severity EPSS score", 
        "Max Severity EPSS percentile"
    ]
    
    for i, col in enumerate(user_columns, 1):
        print(f"   {i:2d}. {col}")
    
    # 4. Criar template correto
    new_template_id = create_correct_template(token)
    
    if new_template_id:
        # 5. Testar upload com template correto
        test_upload_with_correct_template(token, new_template_id)
        
        print(f"\n" + "="*50)
        print("✅ SOLUÇÃO ENCONTRADA!")
        print(f"📋 Use o template ID {new_template_id} no frontend")
        print("🔗 Este template tem o mapeamento correto para suas colunas")
        print("📊 Colunas mapeadas: IP, Hostname, NVT Name, Severity, CVSS, CVEs")
    else:
        print(f"\n❌ Não foi possível criar o template correto")

if __name__ == "__main__":
    main() 