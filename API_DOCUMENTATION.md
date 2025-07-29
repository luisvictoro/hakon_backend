# 📚 Documentação da API - Hakon Backend

## 🔐 Autenticação

Todas as rotas (exceto login) requerem autenticação JWT via header `Authorization: Bearer <token>`.

### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Resposta:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

---

## 📋 Templates de Scan

### Criar Template
```http
POST /api/templates
Authorization: Bearer <token>
Content-Type: application/json

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
    "low": "Low",
    "info": "Info"
  }
}
```

**Resposta:**
```json
{
  "id": 1,
  "name": "Nessus Template",
  "source": "Nessus",
  "column_mapping": {...},
  "severity_map": {...},
  "created_by": "admin",
  "created_at": "2025-01-15T10:30:00Z"
}
```

### Listar Templates
```http
GET /api/templates?skip=0&limit=100
Authorization: Bearer <token>
```

### Buscar Template Específico
```http
GET /api/templates/{id}
Authorization: Bearer <token>
```

### Atualizar Template
```http
PUT /api/templates/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Nessus Template Updated",
  "source": "Nessus",
  "column_mapping": {...},
  "severity_map": {...}
}
```

### Deletar Template
```http
DELETE /api/templates/{id}
Authorization: Bearer <token>
```

---

## 📤 Upload e Vulnerabilidades

### Upload CSV
```http
POST /api/vulnerability/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

Form Data:
- month: "2025-01"
- template_id: 1
- file: <arquivo_csv>
```

**Resposta:**
```json
{
  "message": "Upload successful"
}
```

### Listar Meses Disponíveis
```http
GET /api/vulnerability/months
Authorization: Bearer <token>
```

**Resposta:**
```json
["2025-01", "2025-02", "2025-03"]
```

### Listar Todas as Vulnerabilidades
```http
GET /api/vulnerability/uploads
Authorization: Bearer <token>
```

### Listar Vulnerabilidades com Paginação
```http
GET /api/vulnerability/list?skip=0&limit=100
Authorization: Bearer <token>
```

**Resposta:**
```json
[
  {
    "id": 1,
    "ip": "192.168.1.1",
    "hostname": "server01",
    "nvt_name": "SQL Injection",
    "severity": "High",
    "cvss": 8.5,
    "cves": "CVE-2021-1234",
    "reference_month": "2025-01",
    "created_at": "2025-01-15T10:30:00Z",
    "vuln_hash": "abc123...",
    "status": "new"
  }
]
```

### Obter Campos Esperados
```http
GET /api/vulnerability/expected-fields
Authorization: Bearer <token>
```

**Resposta:**
```json
{
  "required_fields": [
    {
      "name": "ip",
      "required": true,
      "description": "Endereço IP do host vulnerável",
      "example": "192.168.1.1",
      "data_type": "string"
    },
    {
      "name": "nvt_name",
      "required": true,
      "description": "Nome da vulnerabilidade/NVT",
      "example": "SQL Injection",
      "data_type": "string"
    },
    {
      "name": "severity",
      "required": true,
      "description": "Nível de severidade da vulnerabilidade",
      "example": "High",
      "data_type": "string"
    }
  ],
  "optional_fields": [
    {
      "name": "hostname",
      "required": false,
      "description": "Nome do host vulnerável",
      "example": "server01.example.com",
      "data_type": "string"
    },
    {
      "name": "cvss",
      "required": false,
      "description": "Score CVSS da vulnerabilidade",
      "example": "8.5",
      "data_type": "float"
    },
    {
      "name": "cves",
      "required": false,
      "description": "Lista de CVEs separados por vírgula",
      "example": "CVE-2021-1234,CVE-2021-5678",
      "data_type": "string"
    }
  ],
  "severity_levels": [
    "Critical",
    "High",
    "Medium",
    "Low",
    "Info"
  ],
  "example_mapping": {
    "Host": "ip",
    "Name": "nvt_name",
    "Risk": "severity",
    "CVSS": "cvss",
    "CVE": "cves",
    "Hostname": "hostname"
  }
}
```

### Histórico de Vulnerabilidade
```http
GET /api/vulnerability/history/{vuln_hash}
Authorization: Bearer <token>
```

**Resposta:**
```json
[
  {
    "id": 1,
    "vuln_hash": "abc123...",
    "month": "2025-01",
    "status": "new",
    "created_at": "2025-01-15T10:30:00Z"
  },
  {
    "id": 2,
    "vuln_hash": "abc123...",
    "month": "2025-02",
    "status": "ongoing",
    "created_at": "2025-02-15T10:30:00Z"
  }
]
```

### Deletar por Mês
```http
DELETE /api/vulnerability/uploads/{month}
Authorization: Bearer <token>
```

### Deletar Tudo
```http
DELETE /api/vulnerability/uploads/all
Authorization: Bearer <token>
```

---

## 🔧 Alterações Manuais

### Alterar Severidade
```http
PUT /api/vulnerability/{vulnerability_id}/severity
Authorization: Bearer <token>
Content-Type: application/json

{
  "field_changed": "severity",
  "new_value": "Critical",
  "reason": "Vulnerabilidade identificada como crítica após análise manual"
}
```

**Resposta:**
```json
{
  "message": "Severity updated successfully",
  "vulnerability": {
    "id": 1,
    "ip": "192.168.1.1",
    "severity": "Critical",
    "original_severity": "High",
    "severity_manually_changed": true,
    "status": "new",
    "original_status": "new",
    "status_manually_changed": false
  },
  "change": {
    "field_changed": "severity",
    "old_value": "High",
    "new_value": "Critical",
    "changed_by": "admin",
    "manually_changed": true
  }
}
```

### Alterar Status
```http
PUT /api/vulnerability/{vulnerability_id}/status
Authorization: Bearer <token>
Content-Type: application/json

{
  "field_changed": "status",
  "new_value": "closed",
  "reason": "Vulnerabilidade corrigida e validada"
}
```

**Resposta:**
```json
{
  "message": "Status updated successfully",
  "vulnerability": {
    "id": 1,
    "ip": "192.168.1.1",
    "severity": "High",
    "original_severity": "High",
    "severity_manually_changed": false,
    "status": "closed",
    "original_status": "new",
    "status_manually_changed": true
  },
  "change": {
    "field_changed": "status",
    "old_value": "new",
    "new_value": "closed",
    "changed_by": "admin",
    "manually_changed": true
  }
}
```

### Histórico de Alterações Manuais
```http
GET /api/vulnerability/{vulnerability_id}/manual-changes
Authorization: Bearer <token>
```

**Resposta:**
```json
[
  {
    "id": 1,
    "vulnerability_id": 1,
    "vuln_hash": "abc123...",
    "field_changed": "severity",
    "old_value": "High",
    "new_value": "Critical",
    "changed_by": "admin",
    "changed_at": "2025-01-15T10:30:00Z",
    "reason": "Vulnerabilidade identificada como crítica após análise manual"
  },
  {
    "id": 2,
    "vulnerability_id": 1,
    "vuln_hash": "abc123...",
    "field_changed": "status",
    "old_value": "new",
    "new_value": "closed",
    "changed_by": "admin",
    "changed_at": "2025-01-15T11:00:00Z",
    "reason": "Vulnerabilidade corrigida e validada"
  }
]
```

### Todas as Alterações Manuais
```http
GET /api/vulnerability/manual-changes/all?skip=0&limit=100
Authorization: Bearer <token>
```

**Resposta:**
```json
[
  {
    "id": 1,
    "vulnerability_id": 1,
    "vuln_hash": "abc123...",
    "field_changed": "severity",
    "old_value": "High",
    "new_value": "Critical",
    "changed_by": "admin",
    "changed_at": "2025-01-15T10:30:00Z",
    "reason": "Vulnerabilidade identificada como crítica após análise manual"
  }
]
```

---

## 🗄️ Estrutura de Dados

### Vulnerability
```typescript
interface Vulnerability {
  id: number;
  ip: string;
  hostname: string | null;
  nvt_name: string;
  severity: string;
  cvss: number | null;
  cves: string | null;
  reference_month: string;
  created_at: string;
  vuln_hash: string;
  status: 'new' | 'ongoing' | 'reopened' | 'closed';
}
```

### ScanTemplate
```typescript
interface ScanTemplate {
  id: number;
  name: string;
  source: string;
  column_mapping: Record<string, string>;
  severity_map: Record<string, string>;
  created_by: string;
  created_at: string;
}
```

### VulnerabilityStatusHistory
```typescript
interface VulnerabilityStatusHistory {
  id: number;
  vuln_hash: string;
  month: string;
  status: 'new' | 'ongoing' | 'reopened' | 'closed';
  created_at: string;
}
```

---

## 🔄 Regras de Status

### Status de Vulnerabilidades
- **new**: Aparece pela primeira vez no mês corrente
- **ongoing**: Já existia no mês anterior e continua presente
- **reopened**: Existia anteriormente, sumiu em um ou mais meses, e voltou a aparecer
- **closed**: Estava presente no mês anterior, mas não reaparece no mês atual

### Geração do Hash
O `vuln_hash` é gerado usando:
```javascript
SHA256(ip + hostname + nvt_name + sorted(cves))
```

---

## 📝 Exemplos de Uso

### Fluxo Completo de Upload

1. **Criar Template**
```javascript
const template = await fetch('/api/templates', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'Nessus Template',
    source: 'Nessus',
    column_mapping: {
      'Host': 'ip',
      'Name': 'nvt_name',
      'Risk': 'severity',
      'CVSS': 'cvss',
      'CVE': 'cves'
    },
    severity_map: {
      'critical': 'Critical',
      'high': 'High',
      'medium': 'Medium',
      'low': 'Low'
    }
  })
});
```

2. **Upload CSV**
```javascript
const formData = new FormData();
formData.append('month', '2025-01');
formData.append('template_id', template.id);
formData.append('file', csvFile);

const upload = await fetch('/api/vulnerability/upload', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`
  },
  body: formData
});
```

3. **Listar Vulnerabilidades**
```javascript
const vulnerabilities = await fetch('/api/vulnerability/list', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

### Análise de Status

```javascript
// Agrupar vulnerabilidades por status
const statusCount = vulnerabilities.reduce((acc, vuln) => {
  acc[vuln.status] = (acc[vuln.status] || 0) + 1;
  return acc;
}, {});

// Histórico de uma vulnerabilidade específica
const history = await fetch(`/api/vulnerability/history/${vulnHash}`, {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

---

## ⚠️ Considerações Importantes

1. **Autenticação**: Sempre incluir o token JWT no header `Authorization`
2. **Templates**: Criar templates antes de fazer upload de CSVs
3. **Meses**: Usar formato "YYYY-MM" para referência de mês
4. **Hash**: O hash é determinístico, então a mesma vulnerabilidade terá o mesmo hash
5. **Status**: O status é calculado automaticamente baseado no histórico
6. **Histórico**: Cada upload gera registros de histórico automaticamente

---

## 🚀 Endpoints Resumidos

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/auth/login` | Login |
| POST | `/api/templates` | Criar template |
| GET | `/api/templates` | Listar templates |
| GET | `/api/templates/{id}` | Buscar template |
| PUT | `/api/templates/{id}` | Atualizar template |
| DELETE | `/api/templates/{id}` | Deletar template |
| POST | `/api/vulnerability/upload` | Upload CSV |
| GET | `/api/vulnerability/months` | Listar meses |
| GET | `/api/vulnerability/uploads` | Listar todas vulnerabilidades |
| GET | `/api/vulnerability/list` | Listar com paginação |
| GET | `/api/vulnerability/expected-fields` | Obter campos esperados |
| GET | `/api/vulnerability/history/{hash}` | Histórico de vulnerabilidade |
| PUT | `/api/vulnerability/{id}/severity` | Alterar severidade manualmente |
| PUT | `/api/vulnerability/{id}/status` | Alterar status manualmente |
| GET | `/api/vulnerability/{id}/manual-changes` | Histórico de alterações manuais |
| GET | `/api/vulnerability/manual-changes/all` | Todas as alterações manuais |
| DELETE | `/api/vulnerability/uploads/{month}` | Deletar por mês |
| DELETE | `/api/vulnerability/uploads/all` | Deletar tudo | 