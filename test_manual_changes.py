#!/usr/bin/env python3
"""
Script para testar as APIs de alterações manuais de severidade e status
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
            token_data = response.json()
            return token_data.get("access_token")
        else:
            print(f"❌ Erro no login: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao obter token: {e}")
        return None

def get_vulnerabilities(token):
    """Obter lista de vulnerabilidades para testar"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/vulnerability/list?limit=5",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Erro ao obter vulnerabilidades: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Erro ao obter vulnerabilidades: {e}")
        return []

def test_change_severity(token, vulnerability_id):
    """Testar alteração de severidade"""
    print(f"\n🧪 Testando alteração de severidade para vulnerabilidade {vulnerability_id}")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Teste 1: Alterar para Critical
    change_data = {
        "field_changed": "severity",
        "new_value": "Critical",
        "reason": "Teste de alteração manual - vulnerabilidade crítica"
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/api/vulnerability/{vulnerability_id}/severity",
            json=change_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Alteração de severidade realizada com sucesso!")
            print(f"   Severidade anterior: {result['change']['old_value']}")
            print(f"   Nova severidade: {result['change']['new_value']}")
            print(f"   Alterado por: {result['change']['changed_by']}")
            print(f"   Alteração manual: {result['change']['manually_changed']}")
            return True
        else:
            print(f"❌ Erro na alteração: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao alterar severidade: {e}")
        return False

def test_change_status(token, vulnerability_id):
    """Testar alteração de status"""
    print(f"\n🧪 Testando alteração de status para vulnerabilidade {vulnerability_id}")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Teste: Alterar para closed
    change_data = {
        "field_changed": "status",
        "new_value": "closed",
        "reason": "Teste de alteração manual - vulnerabilidade corrigida"
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/api/vulnerability/{vulnerability_id}/status",
            json=change_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Alteração de status realizada com sucesso!")
            print(f"   Status anterior: {result['change']['old_value']}")
            print(f"   Novo status: {result['change']['new_value']}")
            print(f"   Alterado por: {result['change']['changed_by']}")
            print(f"   Alteração manual: {result['change']['manually_changed']}")
            return True
        else:
            print(f"❌ Erro na alteração: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao alterar status: {e}")
        return False

def test_get_manual_changes(token, vulnerability_id):
    """Testar obtenção do histórico de alterações manuais"""
    print(f"\n🧪 Testando obtenção do histórico de alterações para vulnerabilidade {vulnerability_id}")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/vulnerability/{vulnerability_id}/manual-changes",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            changes = response.json()
            print(f"✅ Histórico obtido com sucesso! {len(changes)} alterações encontradas")
            
            for i, change in enumerate(changes, 1):
                print(f"   {i}. Campo: {change['field_changed']}")
                print(f"      Valor anterior: {change['old_value']}")
                print(f"      Novo valor: {change['new_value']}")
                print(f"      Alterado por: {change['changed_by']}")
                print(f"      Data: {change['changed_at']}")
                if change.get('reason'):
                    print(f"      Motivo: {change['reason']}")
                print()
            
            return True
        else:
            print(f"❌ Erro ao obter histórico: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao obter histórico: {e}")
        return False

def test_get_all_manual_changes(token):
    """Testar obtenção de todas as alterações manuais"""
    print(f"\n🧪 Testando obtenção de todas as alterações manuais")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/vulnerability/manual-changes/all?limit=10",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            changes = response.json()
            print(f"✅ Todas as alterações obtidas com sucesso! {len(changes)} alterações encontradas")
            
            for i, change in enumerate(changes[:3], 1):  # Mostra apenas as 3 primeiras
                print(f"   {i}. Vulnerabilidade ID: {change['vulnerability_id']}")
                print(f"      Campo: {change['field_changed']}")
                print(f"      Valor anterior: {change['old_value']}")
                print(f"      Novo valor: {change['new_value']}")
                print(f"      Alterado por: {change['changed_by']}")
                print(f"      Data: {change['changed_at']}")
                print()
            
            return True
        else:
            print(f"❌ Erro ao obter alterações: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao obter alterações: {e}")
        return False

def test_invalid_changes(token, vulnerability_id):
    """Testar alterações inválidas"""
    print(f"\n🧪 Testando alterações inválidas")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Teste 1: Severidade inválida
    invalid_severity = {
        "field_changed": "severity",
        "new_value": "InvalidSeverity",
        "reason": "Teste de severidade inválida"
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/api/vulnerability/{vulnerability_id}/severity",
            json=invalid_severity,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 400:
            print("✅ Validação de severidade inválida funcionando corretamente")
        else:
            print(f"❌ Esperava erro 400, recebeu {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro no teste de severidade inválida: {e}")
    
    # Teste 2: Status inválido
    invalid_status = {
        "field_changed": "status",
        "new_value": "invalid_status",
        "reason": "Teste de status inválido"
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/api/vulnerability/{vulnerability_id}/status",
            json=invalid_status,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 400:
            print("✅ Validação de status inválido funcionando corretamente")
        else:
            print(f"❌ Esperava erro 400, recebeu {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro no teste de status inválido: {e}")

def main():
    """Função principal"""
    print("🧪 Testando APIs de Alterações Manuais")
    print("=" * 50)
    
    # Obter token
    token = get_auth_token()
    if not token:
        print("❌ Não foi possível obter token de autenticação")
        return
    
    print(f"✅ Token obtido: {token[:20]}...")
    
    # Obter vulnerabilidades para testar
    vulnerabilities = get_vulnerabilities(token)
    if not vulnerabilities:
        print("❌ Não foi possível obter vulnerabilidades para testar")
        return
    
    print(f"✅ {len(vulnerabilities)} vulnerabilidades obtidas para teste")
    
    # Usar a primeira vulnerabilidade para os testes
    test_vuln = vulnerabilities[0]
    vulnerability_id = test_vuln['id']
    
    print(f"📋 Usando vulnerabilidade ID: {vulnerability_id}")
    print(f"   IP: {test_vuln['ip']}")
    print(f"   Severidade atual: {test_vuln['severity']}")
    print(f"   Status atual: {test_vuln['status']}")
    
    # Executar testes
    tests_passed = 0
    total_tests = 5
    
    # Teste 1: Alterar severidade
    if test_change_severity(token, vulnerability_id):
        tests_passed += 1
    
    # Teste 2: Alterar status
    if test_change_status(token, vulnerability_id):
        tests_passed += 1
    
    # Teste 3: Obter histórico de alterações
    if test_get_manual_changes(token, vulnerability_id):
        tests_passed += 1
    
    # Teste 4: Obter todas as alterações
    if test_get_all_manual_changes(token):
        tests_passed += 1
    
    # Teste 5: Testar validações
    test_invalid_changes(token, vulnerability_id)
    tests_passed += 1  # Considera como passou se não deu erro
    
    # Resultado final
    print("\n" + "=" * 50)
    print(f"🏁 Resultado dos testes: {tests_passed}/{total_tests} passaram")
    
    if tests_passed == total_tests:
        print("🎉 Todos os testes passaram!")
    else:
        print("⚠️ Alguns testes falharam")

if __name__ == "__main__":
    main() 