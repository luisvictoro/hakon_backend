# 🎯 Exemplo de Implementação Frontend - Alterações Manuais

## 📋 Visão Geral

Este documento mostra como o frontend deve implementar as funcionalidades de alteração manual de severidade e status de vulnerabilidades.

## 🔧 APIs Disponíveis

### 1. Alterar Severidade
```http
PUT /api/vulnerability/{vulnerability_id}/severity
```

### 2. Alterar Status
```http
PUT /api/vulnerability/{vulnerability_id}/status
```

### 3. Histórico de Alterações
```http
GET /api/vulnerability/{vulnerability_id}/manual-changes
```

## 🚀 Implementação Frontend

### 1. Componente de Lista de Vulnerabilidades

```jsx
import React, { useState, useEffect } from 'react';
import { changeVulnerabilitySeverity, changeVulnerabilityStatus } from '../services/vulnerabilityService';

function VulnerabilityList() {
  const [vulnerabilities, setVulnerabilities] = useState([]);
  const [loading, setLoading] = useState(false);

  // Função para alterar severidade
  const handleSeverityChange = async (vulnerabilityId, newSeverity, reason) => {
    try {
      setLoading(true);
      
      const response = await changeVulnerabilitySeverity(vulnerabilityId, newSeverity, reason);
      
      // Atualiza a lista local
      setVulnerabilities(prev => prev.map(vuln => 
        vuln.id === vulnerabilityId 
          ? { ...vuln, ...response.vulnerability }
          : vuln
      ));
      
      // Mostra notificação de sucesso
      showNotification('Severidade alterada com sucesso!', 'success');
      
    } catch (error) {
      console.error('Erro ao alterar severidade:', error);
      showNotification('Erro ao alterar severidade', 'error');
    } finally {
      setLoading(false);
    }
  };

  // Função para alterar status
  const handleStatusChange = async (vulnerabilityId, newStatus, reason) => {
    try {
      setLoading(true);
      
      const response = await changeVulnerabilityStatus(vulnerabilityId, newStatus, reason);
      
      // Atualiza a lista local
      setVulnerabilities(prev => prev.map(vuln => 
        vuln.id === vulnerabilityId 
          ? { ...vuln, ...response.vulnerability }
          : vuln
      ));
      
      showNotification('Status alterado com sucesso!', 'success');
      
    } catch (error) {
      console.error('Erro ao alterar status:', error);
      showNotification('Erro ao alterar status', 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="vulnerability-list">
      <h2>Lista de Vulnerabilidades</h2>
      
      {vulnerabilities.map(vuln => (
        <VulnerabilityCard
          key={vuln.id}
          vulnerability={vuln}
          onSeverityChange={handleSeverityChange}
          onStatusChange={handleStatusChange}
          loading={loading}
        />
      ))}
    </div>
  );
}
```

### 2. Componente de Card de Vulnerabilidade

```jsx
function VulnerabilityCard({ vulnerability, onSeverityChange, onStatusChange, loading }) {
  const [showSeverityModal, setShowSeverityModal] = useState(false);
  const [showStatusModal, setShowStatusModal] = useState(false);
  const [showHistory, setShowHistory] = useState(false);

  const getSeverityColor = (severity) => {
    const colors = {
      'Critical': '#dc3545',
      'High': '#fd7e14',
      'Medium': '#ffc107',
      'Low': '#28a745',
      'Info': '#17a2b8'
    };
    return colors[severity] || '#6c757d';
  };

  const getStatusColor = (status) => {
    const colors = {
      'new': '#007bff',
      'ongoing': '#ffc107',
      'reopened': '#fd7e14',
      'closed': '#28a745'
    };
    return colors[status] || '#6c757d';
  };

  return (
    <div className="vulnerability-card">
      <div className="card-header">
        <h3>{vulnerability.nvt_name}</h3>
        <div className="card-actions">
          <button 
            onClick={() => setShowHistory(true)}
            className="btn btn-sm btn-outline-info"
          >
            📋 Histórico
          </button>
        </div>
      </div>
      
      <div className="card-body">
        <div className="vuln-info">
          <p><strong>IP:</strong> {vulnerability.ip}</p>
          <p><strong>Hostname:</strong> {vulnerability.hostname || 'N/A'}</p>
          <p><strong>CVSS:</strong> {vulnerability.cvss || 'N/A'}</p>
          <p><strong>CVE:</strong> {vulnerability.cves || 'N/A'}</p>
        </div>
        
        <div className="vuln-status">
          {/* Severidade */}
          <div className="severity-section">
            <label>Severidade:</label>
            <div className="severity-display">
              <span 
                className="severity-badge"
                style={{ backgroundColor: getSeverityColor(vulnerability.severity) }}
              >
                {vulnerability.severity}
              </span>
              
              {vulnerability.severity_manually_changed && (
                <span className="manual-indicator" title="Alterado manualmente">
                  ✏️
                </span>
              )}
              
              <button 
                onClick={() => setShowSeverityModal(true)}
                className="btn btn-sm btn-outline-primary"
                disabled={loading}
              >
                Alterar
              </button>
            </div>
          </div>
          
          {/* Status */}
          <div className="status-section">
            <label>Status:</label>
            <div className="status-display">
              <span 
                className="status-badge"
                style={{ backgroundColor: getStatusColor(vulnerability.status) }}
              >
                {vulnerability.status}
              </span>
              
              {vulnerability.status_manually_changed && (
                <span className="manual-indicator" title="Alterado manualmente">
                  ✏️
                </span>
              )}
              
              <button 
                onClick={() => setShowStatusModal(true)}
                className="btn btn-sm btn-outline-primary"
                disabled={loading}
              >
                Alterar
              </button>
            </div>
          </div>
        </div>
      </div>
      
      {/* Modal de Alteração de Severidade */}
      {showSeverityModal && (
        <SeverityChangeModal
          vulnerability={vulnerability}
          onClose={() => setShowSeverityModal(false)}
          onConfirm={(newSeverity, reason) => {
            onSeverityChange(vulnerability.id, newSeverity, reason);
            setShowSeverityModal(false);
          }}
        />
      )}
      
      {/* Modal de Alteração de Status */}
      {showStatusModal && (
        <StatusChangeModal
          vulnerability={vulnerability}
          onClose={() => setShowStatusModal(false)}
          onConfirm={(newStatus, reason) => {
            onStatusChange(vulnerability.id, newStatus, reason);
            setShowStatusModal(false);
          }}
        />
      )}
      
      {/* Modal de Histórico */}
      {showHistory && (
        <ManualChangesHistoryModal
          vulnerabilityId={vulnerability.id}
          onClose={() => setShowHistory(false)}
        />
      )}
    </div>
  );
}
```

### 3. Modal de Alteração de Severidade

```jsx
function SeverityChangeModal({ vulnerability, onClose, onConfirm }) {
  const [newSeverity, setNewSeverity] = useState(vulnerability.severity);
  const [reason, setReason] = useState('');
  const [loading, setLoading] = useState(false);

  const severityOptions = [
    { value: 'Critical', label: 'Critical', color: '#dc3545' },
    { value: 'High', label: 'High', color: '#fd7e14' },
    { value: 'Medium', label: 'Medium', color: '#ffc107' },
    { value: 'Low', label: 'Low', color: '#28a745' },
    { value: 'Info', label: 'Info', color: '#17a2b8' }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (newSeverity === vulnerability.severity) {
      onClose();
      return;
    }
    
    setLoading(true);
    try {
      await onConfirm(newSeverity, reason);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal">
        <div className="modal-header">
          <h3>Alterar Severidade</h3>
          <button onClick={onClose} className="btn-close">&times;</button>
        </div>
        
        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            <div className="form-group">
              <label>Vulnerabilidade:</label>
              <p>{vulnerability.nvt_name}</p>
            </div>
            
            <div className="form-group">
              <label>Severidade Atual:</label>
              <span className="severity-badge" style={{ backgroundColor: getSeverityColor(vulnerability.severity) }}>
                {vulnerability.severity}
              </span>
              {vulnerability.severity_manually_changed && (
                <span className="manual-indicator">(Alterado manualmente)</span>
              )}
            </div>
            
            <div className="form-group">
              <label>Nova Severidade:</label>
              <select 
                value={newSeverity} 
                onChange={(e) => setNewSeverity(e.target.value)}
                className="form-control"
                required
              >
                {severityOptions.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
            
            <div className="form-group">
              <label>Motivo da Alteração:</label>
              <textarea
                value={reason}
                onChange={(e) => setReason(e.target.value)}
                className="form-control"
                rows="3"
                placeholder="Descreva o motivo da alteração..."
              />
            </div>
          </div>
          
          <div className="modal-footer">
            <button type="button" onClick={onClose} className="btn btn-secondary">
              Cancelar
            </button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Alterando...' : 'Confirmar Alteração'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
```

### 4. Modal de Alteração de Status

```jsx
function StatusChangeModal({ vulnerability, onClose, onConfirm }) {
  const [newStatus, setNewStatus] = useState(vulnerability.status);
  const [reason, setReason] = useState('');
  const [loading, setLoading] = useState(false);

  const statusOptions = [
    { value: 'new', label: 'Nova', color: '#007bff' },
    { value: 'ongoing', label: 'Em Andamento', color: '#ffc107' },
    { value: 'reopened', label: 'Reaberta', color: '#fd7e14' },
    { value: 'closed', label: 'Fechada', color: '#28a745' }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (newStatus === vulnerability.status) {
      onClose();
      return;
    }
    
    setLoading(true);
    try {
      await onConfirm(newStatus, reason);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal">
        <div className="modal-header">
          <h3>Alterar Status</h3>
          <button onClick={onClose} className="btn-close">&times;</button>
        </div>
        
        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            <div className="form-group">
              <label>Vulnerabilidade:</label>
              <p>{vulnerability.nvt_name}</p>
            </div>
            
            <div className="form-group">
              <label>Status Atual:</label>
              <span className="status-badge" style={{ backgroundColor: getStatusColor(vulnerability.status) }}>
                {vulnerability.status}
              </span>
              {vulnerability.status_manually_changed && (
                <span className="manual-indicator">(Alterado manualmente)</span>
              )}
            </div>
            
            <div className="form-group">
              <label>Novo Status:</label>
              <select 
                value={newStatus} 
                onChange={(e) => setNewStatus(e.target.value)}
                className="form-control"
                required
              >
                {statusOptions.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
            
            <div className="form-group">
              <label>Motivo da Alteração:</label>
              <textarea
                value={reason}
                onChange={(e) => setReason(e.target.value)}
                className="form-control"
                rows="3"
                placeholder="Descreva o motivo da alteração..."
              />
            </div>
          </div>
          
          <div className="modal-footer">
            <button type="button" onClick={onClose} className="btn btn-secondary">
              Cancelar
            </button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Alterando...' : 'Confirmar Alteração'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
```

### 5. Modal de Histórico de Alterações

```jsx
function ManualChangesHistoryModal({ vulnerabilityId, onClose }) {
  const [changes, setChanges] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchManualChanges();
  }, [vulnerabilityId]);

  const fetchManualChanges = async () => {
    try {
      const response = await fetch(`/api/vulnerability/${vulnerabilityId}/manual-changes`, {
        headers: {
          'Authorization': `Bearer ${getToken()}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setChanges(data);
      }
    } catch (error) {
      console.error('Erro ao buscar histórico:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('pt-BR');
  };

  return (
    <div className="modal-overlay">
      <div className="modal modal-large">
        <div className="modal-header">
          <h3>Histórico de Alterações Manuais</h3>
          <button onClick={onClose} className="btn-close">&times;</button>
        </div>
        
        <div className="modal-body">
          {loading ? (
            <div className="loading">Carregando histórico...</div>
          ) : changes.length === 0 ? (
            <div className="no-changes">
              <p>Nenhuma alteração manual encontrada para esta vulnerabilidade.</p>
            </div>
          ) : (
            <div className="changes-list">
              {changes.map((change, index) => (
                <div key={change.id} className="change-item">
                  <div className="change-header">
                    <span className="change-number">#{index + 1}</span>
                    <span className="change-field">{change.field_changed === 'severity' ? 'Severidade' : 'Status'}</span>
                    <span className="change-date">{formatDate(change.changed_at)}</span>
                  </div>
                  
                  <div className="change-details">
                    <div className="change-values">
                      <span className="old-value">{change.old_value}</span>
                      <span className="arrow">→</span>
                      <span className="new-value">{change.new_value}</span>
                    </div>
                    
                    <div className="change-meta">
                      <span className="changed-by">Alterado por: {change.changed_by}</span>
                      {change.reason && (
                        <div className="change-reason">
                          <strong>Motivo:</strong> {change.reason}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
        
        <div className="modal-footer">
          <button onClick={onClose} className="btn btn-primary">
            Fechar
          </button>
        </div>
      </div>
    </div>
  );
}
```

### 6. Serviço de API

```javascript
// services/vulnerabilityService.js

const API_BASE = '/api/vulnerability';

export const changeVulnerabilitySeverity = async (vulnerabilityId, newSeverity, reason) => {
  const response = await fetch(`${API_BASE}/${vulnerabilityId}/severity`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getToken()}`
    },
    body: JSON.stringify({
      field_changed: 'severity',
      new_value: newSeverity,
      reason: reason
    })
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Erro ao alterar severidade');
  }

  return response.json();
};

export const changeVulnerabilityStatus = async (vulnerabilityId, newStatus, reason) => {
  const response = await fetch(`${API_BASE}/${vulnerabilityId}/status`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getToken()}`
    },
    body: JSON.stringify({
      field_changed: 'status',
      new_value: newStatus,
      reason: reason
    })
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Erro ao alterar status');
  }

  return response.json();
};

export const getManualChanges = async (vulnerabilityId) => {
  const response = await fetch(`${API_BASE}/${vulnerabilityId}/manual-changes`, {
    headers: {
      'Authorization': `Bearer ${getToken()}`
    }
  });

  if (!response.ok) {
    throw new Error('Erro ao buscar histórico de alterações');
  }

  return response.json();
};
```

### 7. CSS para Estilização

```css
/* vulnerability-card.css */

.vulnerability-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 20px;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.card-body {
  padding: 15px;
}

.vuln-status {
  display: flex;
  gap: 20px;
  margin-top: 15px;
}

.severity-section,
.status-section {
  flex: 1;
}

.severity-display,
.status-display {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 5px;
}

.severity-badge,
.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  color: white;
  font-size: 12px;
  font-weight: bold;
}

.manual-indicator {
  color: #007bff;
  font-size: 14px;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-large {
  max-width: 800px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.modal-body {
  padding: 15px;
}

.modal-footer {
  padding: 15px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* Change history styles */
.changes-list {
  max-height: 400px;
  overflow-y: auto;
}

.change-item {
  border: 1px solid #eee;
  border-radius: 4px;
  margin-bottom: 10px;
  padding: 10px;
}

.change-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.change-number {
  background: #007bff;
  color: white;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 12px;
}

.change-field {
  font-weight: bold;
  color: #333;
}

.change-date {
  color: #666;
  font-size: 12px;
}

.change-values {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 5px;
}

.old-value {
  background: #f8f9fa;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 12px;
}

.arrow {
  color: #666;
}

.new-value {
  background: #e7f3ff;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 12px;
  color: #007bff;
}

.change-meta {
  font-size: 12px;
  color: #666;
}

.change-reason {
  margin-top: 5px;
  padding: 5px;
  background: #f8f9fa;
  border-radius: 3px;
}
```

## 🎯 Como o Frontend Deve Fazer as Alterações

### 1. **Alterar Severidade**
```javascript
// Exemplo de uso
const handleSeverityChange = async (vulnerabilityId) => {
  try {
    const response = await changeVulnerabilitySeverity(
      vulnerabilityId, 
      'Critical', 
      'Vulnerabilidade identificada como crítica após análise manual'
    );
    
    console.log('Severidade alterada:', response);
    // Atualizar UI com os novos dados
    
  } catch (error) {
    console.error('Erro:', error);
    // Mostrar erro para o usuário
  }
};
```

### 2. **Alterar Status**
```javascript
// Exemplo de uso
const handleStatusChange = async (vulnerabilityId) => {
  try {
    const response = await changeVulnerabilityStatus(
      vulnerabilityId, 
      'closed', 
      'Vulnerabilidade corrigida e validada'
    );
    
    console.log('Status alterado:', response);
    // Atualizar UI com os novos dados
    
  } catch (error) {
    console.error('Erro:', error);
    // Mostrar erro para o usuário
  }
};
```

### 3. **Verificar se Foi Alterado Manualmente**
```javascript
// No componente de exibição
{vulnerability.severity_manually_changed && (
  <span className="manual-indicator" title="Alterado manualmente">
    ✏️
  </span>
)}

{vulnerability.status_manually_changed && (
  <span className="manual-indicator" title="Alterado manualmente">
    ✏️
  </span>
)}
```

### 4. **Mostrar Valores Originais vs Atuais**
```javascript
// Exemplo de tooltip ou modal
const showOriginalValues = () => {
  return (
    <div className="original-values">
      <p><strong>Severidade Original:</strong> {vulnerability.original_severity}</p>
      <p><strong>Status Original:</strong> {vulnerability.original_status}</p>
      <p><strong>Severidade Atual:</strong> {vulnerability.severity}</p>
      <p><strong>Status Atual:</strong> {vulnerability.status}</p>
    </div>
  );
};
```

## 📝 Benefícios da Implementação

1. **Feedback Visual**: Indicadores claros de alterações manuais
2. **Histórico Completo**: Rastreamento de todas as alterações
3. **Validação**: Prevenção de valores inválidos
4. **UX Intuitiva**: Interface clara e fácil de usar
5. **Auditoria**: Registro completo de quem alterou o quê e quando 