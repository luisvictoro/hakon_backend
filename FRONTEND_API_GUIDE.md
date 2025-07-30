# Guia de APIs Simplificadas para Frontend

## 🎯 Problema Resolvido

O erro 422 (Unprocessable Entity) que estava ocorrendo foi resolvido com a criação de APIs simplificadas que usam IDs numéricos em vez de strings para severidade e status.

## 📋 APIs Disponíveis

### 1. Obter Opções de Severidade
```http
GET /api/vulnerability/severity-options
Authorization: Bearer {token}
```

**Resposta:**
```json
{
  "severity_options": [
    {"id": 1, "name": "Critical", "value": "Critical"},
    {"id": 2, "name": "High", "value": "High"},
    {"id": 3, "name": "Medium", "value": "Medium"},
    {"id": 4, "name": "Low", "value": "Low"},
    {"id": 5, "name": "Info", "value": "Info"}
  ]
}
```

### 2. Obter Opções de Status
```http
GET /api/vulnerability/status-options
Authorization: Bearer {token}
```

**Resposta:**
```json
{
  "status_options": [
    {"id": 1, "name": "New", "value": "new"},
    {"id": 2, "name": "Ongoing", "value": "ongoing"},
    {"id": 3, "name": "Reopened", "value": "reopened"},
    {"id": 4, "name": "Closed", "value": "closed"}
  ]
}
```

### 3. Alterar Severidade (Usando ID)
```http
PUT /api/vulnerability/{vulnerability_id}/severity-simple?severity_id={1-5}
Authorization: Bearer {token}
```

**Exemplo:**
```http
PUT /api/vulnerability/409/severity-simple?severity_id=1
```

**Resposta:**
```json
{
  "message": "Severity updated successfully",
  "vulnerability_id": 409,
  "severity_id": 1,
  "severity_name": "Critical"
}
```

### 4. Alterar Status (Usando ID)
```http
PUT /api/vulnerability/{vulnerability_id}/status-simple?status_id={1-4}
Authorization: Bearer {token}
```

**Exemplo:**
```http
PUT /api/vulnerability/409/status-simple?status_id=2
```

**Resposta:**
```json
{
  "message": "Status updated successfully",
  "vulnerability_id": 409,
  "status_id": 2,
  "status_name": "ongoing"
}
```

## 🔧 Mapeamento de IDs

### Severidade
- **1** = Critical
- **2** = High
- **3** = Medium
- **4** = Low
- **5** = Info

### Status
- **1** = new
- **2** = ongoing
- **3** = reopened
- **4** = closed

## 💡 Como Usar no Frontend

### 1. Carregar Opções no Início
```javascript
// Carregar opções de severidade
const severityResponse = await fetch('/api/vulnerability/severity-options', {
  headers: { 'Authorization': `Bearer ${token}` }
});
const severityOptions = await severityResponse.json();

// Carregar opções de status
const statusResponse = await fetch('/api/vulnerability/status-options', {
  headers: { 'Authorization': `Bearer ${token}` }
});
const statusOptions = await statusResponse.json();
```

### 2. Criar Dropdowns/Selects
```javascript
// Para severidade
const severitySelect = severityOptions.severity_options.map(option => 
  `<option value="${option.id}">${option.name}</option>`
).join('');

// Para status
const statusSelect = statusOptions.status_options.map(option => 
  `<option value="${option.id}">${option.name}</option>`
).join('');
```

### 3. Alterar Severidade
```javascript
async function changeSeverity(vulnerabilityId, severityId) {
  const response = await fetch(`/api/vulnerability/${vulnerabilityId}/severity-simple?severity_id=${severityId}`, {
    method: 'PUT',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  if (response.ok) {
    const result = await response.json();
    console.log('Severidade alterada:', result.severity_name);
  }
}

// Exemplo de uso
changeSeverity(409, 1); // Mudar para Critical
```

### 4. Alterar Status
```javascript
async function changeStatus(vulnerabilityId, statusId) {
  const response = await fetch(`/api/vulnerability/${vulnerabilityId}/status-simple?status_id=${statusId}`, {
    method: 'PUT',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  if (response.ok) {
    const result = await response.json();
    console.log('Status alterado:', result.status_name);
  }
}

// Exemplo de uso
changeStatus(409, 2); // Mudar para ongoing
```

## 🚫 APIs Antigas (Não Recomendadas)

As seguintes APIs ainda funcionam, mas não são recomendadas para o frontend:

- `PUT /api/vulnerability/{id}/severity` (usa JSON com string)
- `PUT /api/vulnerability/{id}/status` (usa JSON com string)
- `PUT /api/vulnerability/hash/{hash}/severity` (usa hash)

## ✅ Vantagens das Novas APIs

1. **Simplicidade**: Usa IDs numéricos em vez de strings
2. **Validação**: Validação automática dos IDs
3. **Performance**: Menos dados trafegados
4. **Consistência**: Respostas padronizadas
5. **Flexibilidade**: Fácil de usar em dropdowns/selects

## 🔍 Exemplo Completo

```javascript
// 1. Carregar opções
const [severityOptions, setSeverityOptions] = useState([]);
const [statusOptions, setStatusOptions] = useState([]);

useEffect(() => {
  // Carregar opções de severidade
  fetch('/api/vulnerability/severity-options', {
    headers: { 'Authorization': `Bearer ${token}` }
  })
  .then(res => res.json())
  .then(data => setSeverityOptions(data.severity_options));
  
  // Carregar opções de status
  fetch('/api/vulnerability/status-options', {
    headers: { 'Authorization': `Bearer ${token}` }
  })
  .then(res => res.json())
  .then(data => setStatusOptions(data.status_options));
}, []);

// 2. Função para alterar severidade
const handleSeverityChange = async (vulnId, severityId) => {
  try {
    const response = await fetch(`/api/vulnerability/${vulnId}/severity-simple?severity_id=${severityId}`, {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${token}` }
    });
    
    if (response.ok) {
      const result = await response.json();
      alert(`Severidade alterada para: ${result.severity_name}`);
    }
  } catch (error) {
    console.error('Erro ao alterar severidade:', error);
  }
};

// 3. Renderizar selects
return (
  <div>
    <select onChange={(e) => handleSeverityChange(vulnerabilityId, e.target.value)}>
      {severityOptions.map(option => (
        <option key={option.id} value={option.id}>
          {option.name}
        </option>
      ))}
    </select>
  </div>
);
```

## 🎉 Resultado

Com essas novas APIs, o frontend pode:
- ✅ Evitar erros 422
- ✅ Usar IDs numéricos simples
- ✅ Ter validação automática
- ✅ Ter respostas consistentes
- ✅ Ser mais performático 