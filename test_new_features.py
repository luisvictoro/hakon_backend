#!/usr/bin/env python3
"""
Script para testar as novas funcionalidades do backend:
- Templates de scan
- Upload com template
- Histórico de vulnerabilidades
- Status de vulnerabilidades
"""

import requests
import json
import pandas as pd
from io import StringIO

# Configuração
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/api/auth/login"
TEMPLATES_URL = f"{BASE_URL}/api/templates"
VULN_URL = f"{BASE_URL}/api/vulnerability"

def login():
    """Faz login e retorna o token"""
    login_data = {
        "username": "admin",
        "password": "admin"
    }
    
    response = requests.post(LOGIN_URL, json=login_data)
    if response.status_code == 200:
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    else:
        print(f"Erro no login: {response.status_code} - {response.text}")
        return None

def test_templates(headers):
    """Testa as operações de templates"""
    print("\n=== Testando Templates ===")
    
    # Criar template
    template_data = {
        "name": "Nessus Template",
        "source": "Nessus",
        "column_mapping": {
            "Host": "ip",
            "Name": "nvt_name",
            "Risk": "severity",
            "CVSS": "cvss",
            "CVE": "cves"
        },
        "severity_map": {
            "critical": "Critical",
            "high": "High",
            "medium": "Medium",
            "low": "Low",
            "info": "Info"
        }
    }
    
    response = requests.post(TEMPLATES_URL, json=template_data, headers=headers)
    if response.status_code == 200:
        template = response.json()
        print(f"✅ Template criado: {template['name']} (ID: {template['id']})")
        template_id = template['id']
    else:
        print(f"❌ Erro ao criar template: {response.status_code} - {response.text}")
        return None
    
    # Listar templates
    response = requests.get(TEMPLATES_URL, headers=headers)
    if response.status_code == 200:
        templates = response.json()
        print(f"✅ Templates listados: {len(templates)} encontrados")
    else:
        print(f"❌ Erro ao listar templates: {response.status_code}")
    
    # Buscar template específico
    response = requests.get(f"{TEMPLATES_URL}/{template_id}", headers=headers)
    if response.status_code == 200:
        template = response.json()
        print(f"✅ Template encontrado: {template['name']}")
    else:
        print(f"❌ Erro ao buscar template: {response.status_code}")
    
    return template_id

def create_test_csv():
    """Cria um CSV de teste"""
    data = {
        'Host': ['192.168.1.1', '192.168.1.2', '192.168.1.1'],
        'Name': ['SQL Injection', 'XSS Vulnerability', 'SQL Injection'],
        'Risk': ['high', 'medium', 'high'],
        'CVSS': [8.5, 6.1, 8.5],
        'CVE': ['CVE-2021-1234', 'CVE-2021-5678', 'CVE-2021-1234']
    }
    
    df = pd.DataFrame(data)
    csv_content = df.to_csv(index=False)
    return csv_content

def test_upload(headers, template_id):
    """Testa o upload de CSV com template"""
    print("\n=== Testando Upload com Template ===")
    
    csv_content = create_test_csv()
    
    files = {'file': ('test.csv', csv_content, 'text/csv')}
    data = {'month': '2025-01', 'template_id': template_id}
    
    response = requests.post(f"{VULN_URL}/upload", files=files, data=data, headers=headers)
    if response.status_code == 200:
        print("✅ Upload realizado com sucesso")
    else:
        print(f"❌ Erro no upload: {response.status_code} - {response.text}")

def test_vulnerabilities(headers):
    """Testa as operações de vulnerabilidades"""
    print("\n=== Testando Vulnerabilidades ===")
    
    # Listar vulnerabilidades
    response = requests.get(f"{VULN_URL}/list", headers=headers)
    if response.status_code == 200:
        vulns = response.json()
        print(f"✅ Vulnerabilidades listadas: {len(vulns)} encontradas")
        
        if vulns:
            # Mostrar primeira vulnerabilidade
            vuln = vulns[0]
            print(f"   Exemplo: {vuln['ip']} - {vuln['nvt_name']} - Status: {vuln['status']}")
            
            # Testar histórico
            vuln_hash = vuln['vuln_hash']
            response = requests.get(f"{VULN_URL}/history/{vuln_hash}", headers=headers)
            if response.status_code == 200:
                history = response.json()
                print(f"✅ Histórico da vulnerabilidade: {len(history)} registros")
                for h in history:
                    print(f"   {h['month']}: {h['status']}")
            else:
                print(f"❌ Erro ao buscar histórico: {response.status_code}")
    else:
        print(f"❌ Erro ao listar vulnerabilidades: {response.status_code}")
    
    # Listar meses
    response = requests.get(f"{VULN_URL}/months", headers=headers)
    if response.status_code == 200:
        months = response.json()
        print(f"✅ Meses disponíveis: {months}")
    else:
        print(f"❌ Erro ao listar meses: {response.status_code}")

def test_second_upload(headers, template_id):
    """Testa upload de segundo mês para verificar status"""
    print("\n=== Testando Upload do Segundo Mês ===")
    
    # Criar CSV com algumas vulnerabilidades iguais e algumas diferentes
    data = {
        'Host': ['192.168.1.1', '192.168.1.3', '192.168.1.4'],
        'Name': ['SQL Injection', 'New Vulnerability', 'Another Issue'],
        'Risk': ['high', 'critical', 'medium'],
        'CVSS': [8.5, 9.0, 5.5],
        'CVE': ['CVE-2021-1234', 'CVE-2021-9999', 'CVE-2021-8888']
    }
    
    df = pd.DataFrame(data)
    csv_content = df.to_csv(index=False)
    
    files = {'file': ('test2.csv', csv_content, 'text/csv')}
    data = {'month': '2025-02', 'template_id': template_id}
    
    response = requests.post(f"{VULN_URL}/upload", files=files, data=data, headers=headers)
    if response.status_code == 200:
        print("✅ Upload do segundo mês realizado com sucesso")
        
        # Verificar status das vulnerabilidades
        response = requests.get(f"{VULN_URL}/list", headers=headers)
        if response.status_code == 200:
            vulns = response.json()
            print(f"✅ Total de vulnerabilidades: {len(vulns)}")
            
            # Agrupar por status
            status_count = {}
            for vuln in vulns:
                status = vuln['status']
                status_count[status] = status_count.get(status, 0) + 1
            
            print("📊 Distribuição por status:")
            for status, count in status_count.items():
                print(f"   {status}: {count}")
    else:
        print(f"❌ Erro no upload do segundo mês: {response.status_code} - {response.text}")

def main():
    """Função principal"""
    print("🚀 Iniciando testes das novas funcionalidades...")
    
    # Login
    headers = login()
    if not headers:
        print("❌ Falha no login. Abortando testes.")
        return
    
    print("✅ Login realizado com sucesso")
    
    # Testar templates
    template_id = test_templates(headers)
    if not template_id:
        print("❌ Falha nos testes de template. Abortando.")
        return
    
    # Testar upload
    test_upload(headers, template_id)
    
    # Testar vulnerabilidades
    test_vulnerabilities(headers)
    
    # Testar segundo upload
    test_second_upload(headers, template_id)
    
    print("\n🎉 Testes concluídos!")

if __name__ == "__main__":
    main() 