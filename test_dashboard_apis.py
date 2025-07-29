#!/usr/bin/env python3
"""
Script para testar as novas APIs de dashboard
"""

import requests
import json
from datetime import datetime

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

def test_dashboard_endpoint(endpoint: str, token: str, description: str):
    """Testar endpoint específico"""
    print(f"\n🔍 Testando {description}...")
    print(f"   Endpoint: {endpoint}")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Sucesso!")
            
            # Mostrar estrutura dos dados
            if isinstance(data, dict):
                print(f"   📊 Estrutura: {list(data.keys())}")
                if 'total_vulnerabilities' in data:
                    print(f"   📈 Total de vulnerabilidades: {data['total_vulnerabilities']}")
            elif isinstance(data, list):
                print(f"   📊 Total de itens: {len(data)}")
                if data:
                    print(f"   📋 Exemplo: {data[0] if len(data) > 0 else 'N/A'}")
            
        else:
            print(f"   ❌ Erro: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")

def main():
    """Testar todas as APIs de dashboard"""
    
    print("=== Testando APIs de Dashboard ===")
    print(f"Base URL: {BASE_URL}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Obter token de autenticação
    print("\n1. Obtendo token de autenticação...")
    token = get_auth_token()
    
    if not token:
        print("❌ Não foi possível obter token. Abortando...")
        return
    
    print(f"   ✅ Token obtido: {token[:20]}...")
    
    # Lista de endpoints para testar
    dashboard_endpoints = [
        ("/api/vulnerability/dashboard/stats", "Estatísticas Completas do Dashboard"),
        ("/api/vulnerability/dashboard/status-counts", "Contagem por Status"),
        ("/api/vulnerability/dashboard/severity-counts", "Contagem por Severidade"),
        ("/api/vulnerability/dashboard/month-counts", "Contagem por Mês"),
        ("/api/vulnerability/dashboard/top-vulnerabilities", "Top Vulnerabilidades"),
        ("/api/vulnerability/dashboard/top-vulnerabilities?limit=5", "Top 5 Vulnerabilidades"),
        ("/api/vulnerability/dashboard/recent-activity", "Atividade Recente (6 meses)"),
        ("/api/vulnerability/dashboard/recent-activity?months=3", "Atividade Recente (3 meses)")
    ]
    
    # Testar cada endpoint
    for endpoint, description in dashboard_endpoints:
        test_dashboard_endpoint(endpoint, token, description)
    
    print("\n" + "="*50)
    print("=== Resumo das APIs de Dashboard ===")
    print("✅ /api/vulnerability/dashboard/stats - Estatísticas completas")
    print("✅ /api/vulnerability/dashboard/status-counts - Contagem por status")
    print("✅ /api/vulnerability/dashboard/severity-counts - Contagem por severidade")
    print("✅ /api/vulnerability/dashboard/month-counts - Contagem por mês")
    print("✅ /api/vulnerability/dashboard/top-vulnerabilities - Top vulnerabilidades")
    print("✅ /api/vulnerability/dashboard/recent-activity - Atividade recente")
    print()
    print("🚀 Benefícios:")
    print("   • Resposta rápida (dados otimizados)")
    print("   • Menos tráfego de rede")
    print("   • Processamento no servidor")
    print("   • Ideal para dashboards em tempo real")
    print()
    print("📊 Uso no Frontend:")
    print("   • Uma única chamada para dashboard completo")
    print("   • Chamadas específicas para componentes individuais")
    print("   • Atualização automática com polling")

if __name__ == "__main__":
    main() 