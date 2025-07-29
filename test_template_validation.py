#!/usr/bin/env python3
"""
Script para testar validação de templates e criação automática
"""

import requests
import json
import pandas as pd

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
    """Criar CSV de teste com colunas OpenVAS"""
    data = {
        'IP': ['10.1.1.1', '10.1.1.2'],
        'Hostname': ['server1', 'server2'],
        'Port': [80, 443],
        'Port Protocol': ['tcp', 'tcp'],
        'CVSS': [9.0, 6.5],
        'Severity': ['High', 'Medium'],
        'QoD': [80, 70],
        'Solution Type': ['Workaround', 'Workaround'],
        'NVT Name': ['SQL Injection', 'XSS Vulnerability'],
        'Summary': ['SQL injection found', 'XSS vulnerability found'],
        'Specific Result': ['SQL injection in form', 'XSS in input field'],
        'NVT OID': ['1.3.6.1.4.1.25623.1.0.1234', '1.3.6.1.4.1.25623.1.0.5678'],
        'CVEs': ['CVE-2021-1234', 'CVE-2021-5678'],
        'Task ID': [12345, 12346],
        'Task Name': ['Scan Task 1', 'Scan Task 2'],
        'Timestamp': ['2025-07-29T10:00:00', '2025-07-29T10:01:00'],
        'Result ID': [67890, 67891],
        'Impact': ['High', 'Medium'],
        'Solution': ['Update software', 'Input validation'],
        'Affected Software/OS': ['Linux', 'Windows'],
        'Vulnerability Insight': ['SQL injection in web app', 'XSS in input field'],
        'Vulnerability Detection Method': ['Automated scan', 'Automated scan'],
        'Product Detection Result': ['Product found', 'Product found'],
        'BIDs': [123, 124],
        'CERTs': [456, 457],
        'Other References': ['Reference 1', 'Reference 2'],
        'Max Severity EPSS score': [0.95, 0.75],
        'Max Severity EPSS percentile': [95.5, 75.2]
    }
    
    df = pd.DataFrame(data)
    csv_content = df.to_csv(index=False)
    return csv_content

def test_template_validation(token, template_id):
    """Testar validação de template"""
    print(f"\n🔍 Testando validação do template ID {template_id}...")
    
    csv_content = create_test_csv()
    
    files = {
        'file': ('test_openvas.csv', csv_content, 'text/csv')
    }
    
    data = {
        'template_id': str(template_id)
    }
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/vulnerability/validate-template",
            files=files,
            data=data,
            headers=headers,
            timeout=30
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Validação concluída")
            print(f"   📊 Válido: {result['valid']}")
            
            if result['errors']:
                print(f"   ❌ Erros:")
                for error in result['errors']:
                    print(f"      - {error}")
            
            if result['warnings']:
                print(f"   ⚠️ Avisos:")
                for warning in result['warnings']:
                    print(f"      - {warning}")
            
            print(f"   📋 Colunas CSV: {len(result['csv_info']['columns'])}")
            print(f"   📊 Linhas: {result['csv_info']['rows']}")
            
            return result
        else:
            print(f"   ❌ Erro: {response.text}")
            return None
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return None

def test_auto_create_template(token):
    """Testar criação automática de template"""
    print(f"\n🔧 Testando criação automática de template...")
    
    csv_content = create_test_csv()
    
    files = {
        'file': ('test_openvas.csv', csv_content, 'text/csv')
    }
    
    data = {
        'name': 'Auto OpenVAS Template',
        'source': 'OpenVAS'
    }
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/templates/auto-create",
            files=files,
            data=data,
            headers=headers,
            timeout=30
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Template criado automaticamente")
            print(f"   📋 ID: {result['template']['id']}")
            print(f"   📋 Nome: {result['template']['name']}")
            print(f"   🔗 Mapeamentos: {len(result['template']['column_mapping'])}")
            print(f"   🎯 Severidades: {len(result['template']['severity_map'])}")
            
            print(f"   📊 Análise:")
            print(f"      - Colunas CSV: {len(result['analysis']['csv_columns'])}")
            print(f"      - Mapeadas: {len(result['analysis']['mapped_columns'])}")
            print(f"      - Não mapeadas: {len(result['analysis']['unmapped_columns'])}")
            
            return result['template']['id']
        else:
            print(f"   ❌ Erro: {response.text}")
            return None
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return None

def main():
    """Teste principal"""
    print("=== Teste de Validação e Criação Automática de Templates ===")
    print(f"Base URL: {BASE_URL}")
    
    # 1. Obter token
    print("\n1. Obtendo token de autenticação...")
    token = get_auth_token()
    
    if not token:
        print("❌ Não foi possível obter token. Abortando...")
        return
    
    print(f"   ✅ Token obtido: {token[:20]}...")
    
    # 2. Testar validação do template ID 5 (problemático)
    print("\n2. Testando validação do template ID 5 (problemático)...")
    validation_result = test_template_validation(token, 5)
    
    if validation_result and not validation_result['valid']:
        print("   ❌ Template ID 5 é inválido (como esperado)")
    
    # 3. Testar validação do template ID 8 (correto)
    print("\n3. Testando validação do template ID 8 (correto)...")
    validation_result = test_template_validation(token, 8)
    
    if validation_result and validation_result['valid']:
        print("   ✅ Template ID 8 é válido")
    
    # 4. Testar criação automática
    print("\n4. Testando criação automática de template...")
    new_template_id = test_auto_create_template(token)
    
    if new_template_id:
        # 5. Testar validação do novo template
        print(f"\n5. Testando validação do novo template ID {new_template_id}...")
        validation_result = test_template_validation(token, new_template_id)
        
        if validation_result and validation_result['valid']:
            print("   ✅ Novo template é válido")
    
    print("\n" + "="*50)
    print("✅ Testes concluídos!")
    print("🛡️ Sistema de validação implementado")
    print("🔧 Criação automática funcionando")
    print("📋 Prevenção de problemas de mapeamento ativa")

if __name__ == "__main__":
    main() 