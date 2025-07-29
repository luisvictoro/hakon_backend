# 🎯 Exemplo de Integração Frontend - API de Campos Esperados

## 📋 Visão Geral

Esta API fornece informações sobre os campos esperados para upload de vulnerabilidades, permitindo que o frontend:

- Valide arquivos CSV antes do upload
- Crie interfaces dinâmicas de mapeamento
- Forneça feedback em tempo real ao usuário
- Implemente validação client-side

## 🔗 Endpoint

```http
GET /api/vulnerability/expected-fields
Authorization: Bearer <token>
```

## 📊 Estrutura da Resposta

```typescript
interface ExpectedFieldsResponse {
  required_fields: ExpectedField[];
  optional_fields: ExpectedField[];
  severity_levels: string[];
  example_mapping: Record<string, string>;
}

interface ExpectedField {
  name: string;
  required: boolean;
  description: string;
  example: string | null;
  data_type: string;
}
```

## 🚀 Exemplos de Uso

### 1. Validação de CSV Antes do Upload

```javascript
// Função para validar CSV usando a API
async function validateCSV(csvFile) {
  try {
    // 1. Obter campos esperados da API
    const response = await fetch('/api/vulnerability/expected-fields', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    const expectedFields = await response.json();
    
    // 2. Ler CSV
    const csvData = await readCSV(csvFile);
    const csvColumns = Object.keys(csvData[0] || {});
    
    // 3. Validar campos obrigatórios
    const requiredFields = expectedFields.required_fields.map(f => f.name);
    const missingFields = [];
    
    for (const field of requiredFields) {
      const hasMapping = Object.values(expectedFields.example_mapping).includes(field);
      if (!hasMapping) {
        missingFields.push(field);
      }
    }
    
    // 4. Retornar resultado da validação
    return {
      isValid: missingFields.length === 0,
      missingFields,
      suggestions: expectedFields.example_mapping,
      severityLevels: expectedFields.severity_levels
    };
    
  } catch (error) {
    console.error('Erro na validação:', error);
    return { isValid: false, error: error.message };
  }
}
```

### 2. Interface de Mapeamento Dinâmico

```jsx
import React, { useState, useEffect } from 'react';

function CSVMappingInterface({ csvColumns, onMappingComplete }) {
  const [expectedFields, setExpectedFields] = useState(null);
  const [mapping, setMapping] = useState({});
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    // Carregar campos esperados da API
    fetchExpectedFields();
  }, []);
  
  const fetchExpectedFields = async () => {
    try {
      const response = await fetch('/api/vulnerability/expected-fields', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      setExpectedFields(data);
      setLoading(false);
    } catch (error) {
      console.error('Erro ao carregar campos:', error);
      setLoading(false);
    }
  };
  
  const handleMappingChange = (csvColumn, dbField) => {
    setMapping(prev => ({
      ...prev,
      [csvColumn]: dbField
    }));
  };
  
  const validateMapping = () => {
    if (!expectedFields) return false;
    
    const requiredFields = expectedFields.required_fields.map(f => f.name);
    const mappedFields = Object.values(mapping);
    
    return requiredFields.every(field => mappedFields.includes(field));
  };
  
  if (loading) return <div>Carregando campos esperados...</div>;
  
  return (
    <div className="mapping-interface">
      <h3>Mapeamento de Colunas</h3>
      
      {/* Campos Obrigatórios */}
      <div className="required-fields">
        <h4>Campos Obrigatórios</h4>
        {expectedFields.required_fields.map(field => (
          <div key={field.name} className="field-item required">
            <label>{field.name}</label>
            <p>{field.description}</p>
            <select 
              value={mapping[field.name] || ''}
              onChange={(e) => handleMappingChange(field.name, e.target.value)}
            >
              <option value="">Selecione uma coluna CSV</option>
              {csvColumns.map(col => (
                <option key={col} value={col}>{col}</option>
              ))}
            </select>
            {field.example && (
              <small>Exemplo: {field.example}</small>
            )}
          </div>
        ))}
      </div>
      
      {/* Campos Opcionais */}
      <div className="optional-fields">
        <h4>Campos Opcionais</h4>
        {expectedFields.optional_fields.map(field => (
          <div key={field.name} className="field-item optional">
            <label>{field.name}</label>
            <p>{field.description}</p>
            <select 
              value={mapping[field.name] || ''}
              onChange={(e) => handleMappingChange(field.name, e.target.value)}
            >
              <option value="">Selecione uma coluna CSV</option>
              {csvColumns.map(col => (
                <option key={col} value={col}>{col}</option>
              ))}
            </select>
            {field.example && (
              <small>Exemplo: {field.example}</small>
            )}
          </div>
        ))}
      </div>
      
      {/* Validação */}
      <div className="validation">
        {validateMapping() ? (
          <button onClick={() => onMappingComplete(mapping)}>
            Mapeamento Válido - Continuar
          </button>
        ) : (
          <div className="error">
            ⚠️ Mapeie todos os campos obrigatórios
          </div>
        )}
      </div>
    </div>
  );
}
```

### 3. Validação de Severidade

```javascript
// Função para validar níveis de severidade
function validateSeverity(severity, expectedLevels) {
  return expectedLevels.includes(severity);
}

// Exemplo de uso
const severityLevels = ['Critical', 'High', 'Medium', 'Low', 'Info'];
const isValid = validateSeverity('High', severityLevels); // true
const isInvalid = validateSeverity('Unknown', severityLevels); // false
```

### 4. Preview de Dados

```javascript
// Função para mostrar preview dos dados mapeados
function showDataPreview(csvData, mapping, expectedFields) {
  const preview = csvData.slice(0, 5).map(row => {
    const mappedRow = {};
    
    // Mapear dados conforme o mapping
    Object.entries(mapping).forEach(([csvCol, dbField]) => {
      mappedRow[dbField] = row[csvCol];
    });
    
    // Validar campos obrigatórios
    const missingFields = expectedFields.required_fields
      .filter(field => !mappedRow[field.name])
      .map(field => field.name);
    
    return {
      ...mappedRow,
      _missingFields: missingFields,
      _isValid: missingFields.length === 0
    };
  });
  
  return preview;
}
```

### 5. Sugestões Automáticas de Mapeamento

```javascript
// Função para sugerir mapeamentos automáticos
function suggestMapping(csvColumns, expectedFields) {
  const suggestions = {};
  
  csvColumns.forEach(csvCol => {
    // Tentar encontrar correspondência exata
    const exactMatch = expectedFields.example_mapping[csvCol];
    if (exactMatch) {
      suggestions[csvCol] = exactMatch;
      return;
    }
    
    // Tentar correspondência por similaridade
    const similarMatch = findSimilarField(csvCol, expectedFields);
    if (similarMatch) {
      suggestions[csvCol] = similarMatch;
    }
  });
  
  return suggestions;
}

function findSimilarField(csvColumn, expectedFields) {
  const allFields = [
    ...expectedFields.required_fields,
    ...expectedFields.optional_fields
  ];
  
  // Buscar por similaridade (exemplo simples)
  const normalizedColumn = csvColumn.toLowerCase().replace(/[^a-z]/g, '');
  
  for (const field of allFields) {
    const normalizedField = field.name.toLowerCase();
    if (normalizedColumn.includes(normalizedField) || 
        normalizedField.includes(normalizedColumn)) {
      return field.name;
    }
  }
  
  return null;
}
```

## 🎨 CSS para Interface

```css
.mapping-interface {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.field-item {
  margin-bottom: 20px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.field-item.required {
  border-left: 4px solid #e74c3c;
  background-color: #fdf2f2;
}

.field-item.optional {
  border-left: 4px solid #3498db;
  background-color: #f0f8ff;
}

.field-item label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}

.field-item p {
  color: #666;
  margin-bottom: 10px;
  font-size: 14px;
}

.field-item select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.field-item small {
  color: #888;
  font-style: italic;
}

.validation {
  margin-top: 20px;
  padding: 15px;
  border-radius: 8px;
}

.validation button {
  background-color: #27ae60;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.validation .error {
  color: #e74c3c;
  font-weight: bold;
}
```

## 🔧 Integração Completa

```javascript
// Exemplo de integração completa
class CSVUploadManager {
  constructor() {
    this.expectedFields = null;
    this.token = null;
  }
  
  async initialize(token) {
    this.token = token;
    await this.loadExpectedFields();
  }
  
  async loadExpectedFields() {
    const response = await fetch('/api/vulnerability/expected-fields', {
      headers: { 'Authorization': `Bearer ${this.token}` }
    });
    this.expectedFields = await response.json();
  }
  
  async processCSV(file) {
    const csvData = await this.readCSV(file);
    const validation = this.validateCSV(csvData);
    
    if (!validation.isValid) {
      throw new Error(`CSV inválido: ${validation.errors.join(', ')}`);
    }
    
    return {
      data: csvData,
      mapping: validation.suggestedMapping,
      preview: this.createPreview(csvData, validation.suggestedMapping)
    };
  }
  
  // ... outros métodos
}
```

## 📝 Benefícios

1. **Validação Antecipada**: Evita uploads de arquivos inválidos
2. **UX Melhorada**: Interface intuitiva de mapeamento
3. **Flexibilidade**: Suporte a diferentes formatos de CSV
4. **Feedback Imediato**: Validação em tempo real
5. **Manutenibilidade**: Centralização das regras de validação 