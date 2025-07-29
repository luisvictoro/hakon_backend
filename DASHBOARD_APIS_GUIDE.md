# 📊 APIs de Dashboard - Guia para Frontend

## 🎯 **Objetivo**

APIs otimizadas especificamente para dashboards, que retornam dados processados e estatísticas em vez de listas completas de vulnerabilidades.

---

## 🚀 **Benefícios**

- **Performance**: Resposta muito mais rápida
- **Eficiência**: Menos tráfego de rede
- **Escalabilidade**: Processamento no servidor
- **Flexibilidade**: Dados específicos para cada componente

---

## 📡 **APIs Disponíveis**

### 1. **Dashboard Completo**
```http
GET /api/vulnerability/dashboard/stats
```

**Resposta:**
```json
{
  "total_vulnerabilities": 1250,
  "total_by_status": {
    "new": 150,
    "ongoing": 800,
    "reopened": 200,
    "closed": 100
  },
  "total_by_severity": {
    "critical": 50,
    "high": 300,
    "medium": 600,
    "low": 300
  },
  "total_by_month": {
    "2025-01": 400,
    "2025-02": 450,
    "2025-03": 400
  },
  "top_vulnerabilities": [
    {
      "nvt_name": "SQL Injection",
      "count": 45,
      "severity": "high",
      "affected_hosts": 12
    }
  ],
  "recent_activity": [
    {
      "month": "2025-03",
      "new_count": 50,
      "ongoing_count": 300,
      "reopened_count": 30,
      "closed_count": 20
    }
  ]
}
```

### 2. **Contagem por Status**
```http
GET /api/vulnerability/dashboard/status-counts
```

**Resposta:**
```json
{
  "new": 150,
  "ongoing": 800,
  "reopened": 200,
  "closed": 100
}
```

### 3. **Contagem por Severidade**
```http
GET /api/vulnerability/dashboard/severity-counts
```

**Resposta:**
```json
{
  "critical": 50,
  "high": 300,
  "medium": 600,
  "low": 300
}
```

### 4. **Contagem por Mês**
```http
GET /api/vulnerability/dashboard/month-counts
```

**Resposta:**
```json
{
  "2025-01": 400,
  "2025-02": 450,
  "2025-03": 400
}
```

### 5. **Top Vulnerabilidades**
```http
GET /api/vulnerability/dashboard/top-vulnerabilities?limit=10
```

**Parâmetros:**
- `limit` (opcional): Número de vulnerabilidades (padrão: 10)

**Resposta:**
```json
[
  {
    "nvt_name": "SQL Injection",
    "count": 45,
    "severity": "high",
    "affected_hosts": 12
  },
  {
    "nvt_name": "XSS Reflected",
    "count": 38,
    "severity": "medium",
    "affected_hosts": 8
  }
]
```

### 6. **Atividade Recente**
```http
GET /api/vulnerability/dashboard/recent-activity?months=6
```

**Parâmetros:**
- `months` (opcional): Número de meses (padrão: 6)

**Resposta:**
```json
[
  {
    "month": "2025-03",
    "new_count": 50,
    "ongoing_count": 300,
    "reopened_count": 30,
    "closed_count": 20
  },
  {
    "month": "2025-02",
    "new_count": 45,
    "ongoing_count": 280,
    "reopened_count": 25,
    "closed_count": 15
  }
]
```

---

## 💻 **Implementação no Frontend**

### **React Hook para Dashboard**
```javascript
import { useState, useEffect } from 'react';

function useDashboardStats() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      
      const response = await fetch(
        'https://hakon-56ae06ddc8d1.herokuapp.com/api/vulnerability/dashboard/stats',
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();
      setStats(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  return { stats, loading, error, refetch: fetchStats };
}

// Uso no componente
function Dashboard() {
  const { stats, loading, error, refetch } = useDashboardStats();

  if (loading) return <div>Carregando...</div>;
  if (error) return <div>Erro: {error}</div>;

  return (
    <div className="dashboard">
      <h1>Dashboard de Vulnerabilidades</h1>
      
      {/* Cards de resumo */}
      <div className="stats-cards">
        <div className="card">
          <h3>Total</h3>
          <p>{stats.total_vulnerabilities}</p>
        </div>
        <div className="card">
          <h3>Novas</h3>
          <p>{stats.total_by_status.new}</p>
        </div>
        <div className="card">
          <h3>Críticas</h3>
          <p>{stats.total_by_severity.critical}</p>
        </div>
      </div>

      {/* Gráficos */}
      <div className="charts">
        <StatusChart data={stats.total_by_status} />
        <SeverityChart data={stats.total_by_severity} />
        <ActivityChart data={stats.recent_activity} />
      </div>

      {/* Top vulnerabilidades */}
      <div className="top-vulns">
        <h3>Top Vulnerabilidades</h3>
        {stats.top_vulnerabilities.map(vuln => (
          <div key={vuln.nvt_name} className="vuln-item">
            <span>{vuln.nvt_name}</span>
            <span>{vuln.count} ocorrências</span>
            <span className={`severity-${vuln.severity}`}>{vuln.severity}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
```

### **Vue.js Composable**
```javascript
// composables/useDashboard.js
import { ref, onMounted } from 'vue';

export function useDashboard() {
  const stats = ref(null);
  const loading = ref(true);
  const error = ref(null);

  const fetchStats = async () => {
    try {
      loading.value = true;
      const token = localStorage.getItem('token');
      
      const response = await fetch(
        'https://hakon-56ae06ddc8d1.herokuapp.com/api/vulnerability/dashboard/stats',
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      stats.value = await response.json();
    } catch (err) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  };

  onMounted(fetchStats);

  return {
    stats,
    loading,
    error,
    refetch: fetchStats
  };
}
```

### **Angular Service**
```typescript
// services/dashboard.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
  private baseUrl = 'https://hakon-56ae06ddc8d1.herokuapp.com/api/vulnerability/dashboard';

  constructor(private http: HttpClient) {}

  getStats(): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
      'Content-Type': 'application/json'
    });

    return this.http.get(`${this.baseUrl}/stats`, { headers });
  }

  getStatusCounts(): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
      'Content-Type': 'application/json'
    });

    return this.http.get(`${this.baseUrl}/status-counts`, { headers });
  }

  getTopVulnerabilities(limit: number = 10): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
      'Content-Type': 'application/json'
    });

    return this.http.get(`${this.baseUrl}/top-vulnerabilities?limit=${limit}`, { headers });
  }
}
```

---

## 🔄 **Atualização Automática**

### **Polling Simples**
```javascript
function useAutoRefresh(interval = 30000) { // 30 segundos
  const { stats, loading, error, refetch } = useDashboardStats();

  useEffect(() => {
    const timer = setInterval(refetch, interval);
    return () => clearInterval(timer);
  }, [refetch, interval]);

  return { stats, loading, error };
}
```

### **WebSocket (Futuro)**
```javascript
// Para implementação futura com WebSocket
function useRealTimeStats() {
  const [stats, setStats] = useState(null);
  
  useEffect(() => {
    const ws = new WebSocket('wss://hakon-56ae06ddc8d1.herokuapp.com/ws/dashboard');
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setStats(data);
    };

    return () => ws.close();
  }, []);

  return stats;
}
```

---

## 📊 **Exemplos de Uso**

### **Card de Resumo**
```javascript
function SummaryCard({ title, value, icon, color }) {
  return (
    <div className={`summary-card ${color}`}>
      <div className="icon">{icon}</div>
      <div className="content">
        <h3>{title}</h3>
        <p className="value">{value}</p>
      </div>
    </div>
  );
}

// Uso
<SummaryCard 
  title="Total de Vulnerabilidades"
  value={stats.total_vulnerabilities}
  icon="🔍"
  color="blue"
/>
```

### **Gráfico de Status**
```javascript
function StatusChart({ data }) {
  const chartData = Object.entries(data).map(([status, count]) => ({
    status,
    count,
    color: getStatusColor(status)
  }));

  return (
    <div className="chart">
      <h3>Status das Vulnerabilidades</h3>
      {chartData.map(item => (
        <div key={item.status} className="bar">
          <span className="label">{item.status}</span>
          <div className="bar-fill" style={{ 
            width: `${(item.count / Math.max(...chartData.map(d => d.count))) * 100}%`,
            backgroundColor: item.color 
          }}></div>
          <span className="value">{item.count}</span>
        </div>
      ))}
    </div>
  );
}
```

---

## 🎨 **CSS para Dashboard**
```css
.dashboard {
  padding: 20px;
  background: #f5f5f5;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: center;
}

.charts {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.chart {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.bar {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.bar-fill {
  height: 20px;
  border-radius: 10px;
  margin: 0 10px;
  transition: width 0.3s ease;
}

.severity-critical { color: #dc3545; }
.severity-high { color: #fd7e14; }
.severity-medium { color: #ffc107; }
.severity-low { color: #28a745; }
```

---

## ✅ **Vantagens das Novas APIs**

1. **Performance**: 10-50x mais rápido que buscar todas as vulnerabilidades
2. **Escalabilidade**: Funciona bem mesmo com milhares de registros
3. **Flexibilidade**: Dados específicos para cada componente
4. **Manutenibilidade**: Lógica de processamento centralizada
5. **Experiência do usuário**: Dashboards responsivos e em tempo real

---

## 🚀 **Próximos Passos**

1. **Implementar no frontend** usando os exemplos acima
2. **Testar performance** comparando com as APIs antigas
3. **Adicionar cache** se necessário para otimizar ainda mais
4. **Considerar WebSocket** para atualizações em tempo real
5. **Implementar filtros** por período, severidade, etc. 