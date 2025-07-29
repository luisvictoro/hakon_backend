# 🚀 Novas Funcionalidades - Hakon Backend

## 📋 Resumo das Implementações

Este documento descreve as novas funcionalidades implementadas no backend Hakon para suportar:

- ✅ **Templates de Scan**: Mapeamento flexível de colunas CSV
- ✅ **Hash Determinístico**: Identificação única de vulnerabilidades
- ✅ **Controle de Status**: Rastreamento de ciclo de vida das vulnerabilidades
- ✅ **Histórico Completo**: Registro de mudanças de status ao longo do tempo

---

## 🗄️ Novas Tabelas do Banco de Dados

### 1. `scan_templates`
Armazena templates para mapeamento de CSVs de diferentes ferramentas.

```sql
CREATE TABLE scan_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    source VARCHAR(100) NOT NULL,
    column_mapping JSONB NOT NULL,
    severity_map JSONB NOT NULL,
    created_by VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 2. `vulnerability_status_history`
Registra o histórico de status de cada vulnerabilidade.

```sql
CREATE TABLE vulnerability_status_history (
    id SERIAL PRIMARY KEY,
    vuln_hash VARCHAR(64) NOT NULL,
    month VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 3. `vulnerability_change_history`
Armazena alterações manuais de status e severidade.

```sql
CREATE TABLE vulnerability_change_history (
    id SERIAL PRIMARY KEY,
    vulnerability_id INTEGER NOT NULL,
    field VARCHAR(20) NOT NULL,
    old_value VARCHAR(50) NOT NULL,
    new_value VARCHAR(50) NOT NULL,
    changed_by VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```
### 4. `vulnerabilities` (Atualizada)
Adicionados campos `vuln_hash` e `status`.

```sql
ALTER TABLE vulnerabilities 
ADD COLUMN vuln_hash VARCHAR(64) NOT NULL,
ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'new';
```

---

## 🔄 Lógica de Status de Vulnerabilidades

### Regras de Status
1. **new**: Primeira aparição da vulnerabilidade
2. **ongoing**: Continua presente desde o mês anterior
3. **reopened**: Reapareceu após ter sido fechada
4. **closed**: Não aparece mais no mês atual

### Geração do Hash
```python
def generate_vuln_hash(ip, hostname, nvt_name, cves):
    # Normaliza e ordena CVEs
    cve_list = sorted([cve.strip() for cve in cves.split(',')])
    cves = ','.join(cve_list)
    
    # Cria string para hash
    hash_string = f"{ip}|{hostname}|{nvt_name}|{cves}"
    return hashlib.sha256(hash_string.encode()).hexdigest()
```

---

## 📤 Fluxo de Upload Melhorado

### 1. Criação de Template
```json
{
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
    "low": "Low"
  }
}
```

### 2. Upload com Template
```http
POST /api/vulnerability/upload
Content-Type: multipart/form-data

Form Data:
- month: "2025-01"
- template_id: 1
- file: <arquivo_csv>
```

### 3. Processamento Automático
1. Aplica mapeamento de colunas do template
2. Normaliza severidades
3. Gera hash único para cada vulnerabilidade
4. Determina status baseado no histórico
5. Registra no histórico de status

---

## 🆕 Novas APIs

### Templates
- `POST /api/templates` - Criar template
- `GET /api/templates` - Listar templates
- `GET /api/templates/{id}` - Buscar template
- `PUT /api/templates/{id}` - Atualizar template
- `DELETE /api/templates/{id}` - Deletar template

### Vulnerabilidades (Atualizadas)
- `POST /api/vulnerability/upload` - Upload com template_id
- `GET /api/vulnerability/history/{hash}` - Histórico de vulnerabilidade
- `PUT /api/vulnerability/{id}/severity` - Alterar severidade
- `PUT /api/vulnerability/{id}/status` - Alterar status
- `GET /api/vulnerability/changes/{id}` - Histórico de alterações

---

## 🧪 Como Testar

### 1. Iniciar o Backend
```bash
cd hakon-backend
python3 -m uvicorn app.main:app --reload
```

### 2. Executar Testes
```bash
python3 test_new_features.py
```

### 3. Teste Manual via curl
```bash
# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Criar template
curl -X POST http://localhost:8000/api/templates \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Template",
    "source": "Test",
    "column_mapping": {"Host": "ip", "Name": "nvt_name"},
    "severity_map": {"high": "High", "medium": "Medium"}
  }'
```

---

## 📊 Benefícios das Novas Funcionalidades

### 1. **Flexibilidade**
- Suporte a diferentes formatos de CSV
- Mapeamento customizável de colunas
- Normalização de severidades

### 2. **Rastreabilidade**
- Hash único para cada vulnerabilidade
- Histórico completo de mudanças
- Identificação de vulnerabilidades recorrentes

### 3. **Análise Temporal**
- Status automático baseado no tempo
- Relatórios de recorrência
- Visão do ciclo de vida das vulnerabilidades

### 4. **Prevenção de Duplicatas**
- Hash determinístico evita duplicatas
- Mesma vulnerabilidade identificada entre scans
- Consistência de dados

---

## 🔧 Arquivos Modificados/Criados

### Novos Arquivos
- `app/services/template.py` - Serviços para templates
- `app/routes/template.py` - Rotas para templates
- `test_new_features.py` - Testes das novas funcionalidades
- `API_DOCUMENTATION.md` - Documentação completa

### Arquivos Modificados
- `app/models/vulnerability.py` - Novos modelos
- `app/schemas/vulnerability.py` - Novos schemas
- `app/services/vulnerability.py` - Lógica de hash e status
- `app/routes/vulnerability.py` - Upload com template
- `app/main.py` - Inclusão das novas rotas

---

## 🚀 Próximos Passos

1. **Testar em Produção**: Validar todas as funcionalidades
2. **Frontend**: Implementar interface para templates
3. **Relatórios**: Criar dashboards de análise temporal
4. **Performance**: Otimizar queries para grandes volumes
5. **Validação**: Adicionar validações de dados

---

## 📞 Suporte

Para dúvidas ou problemas com as novas funcionalidades:

1. Verificar logs do backend
2. Executar testes automatizados
3. Consultar documentação da API
4. Verificar estrutura do banco de dados 