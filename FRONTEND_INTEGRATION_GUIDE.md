# 🎯 Guia de Integração Frontend - Hakon Backend

## 📋 Resumo das Funcionalidades Implementadas

O backend Hakon foi completamente atualizado com as seguintes funcionalidades:

### ✅ **Templates de Scan**
- Criação e gerenciamento de templates para diferentes ferramentas
- Mapeamento flexível de colunas CSV
- Normalização de severidades

### ✅ **Hash Determinístico**
- Identificação única de vulnerabilidades
- Prevenção de duplicatas
- Rastreamento consistente entre scans

### ✅ **Controle de Status**
- Status automático: `new`, `ongoing`, `reopened`, `closed`
- Histórico completo de mudanças
- Análise temporal de vulnerabilidades

### ✅ **Histórico Completo**
- Registro de todas as mudanças de status
- Rastreamento do ciclo de vida das vulnerabilidades
- Relatórios de recorrência

---

## 🔐 Autenticação

### Login
```typescript
interface LoginRequest {
  username: string;
  password: string;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
}

// Exemplo de uso
const login = async (credentials: LoginRequest): Promise<LoginResponse> => {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials)
  });
  return response.json();
};
```

### Interceptor para Token
```typescript
// Adicionar token em todas as requisições
const apiClient = {
  get: async (url: string) => {
    const token = localStorage.getItem('token');
    return fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
  },
  
  post: async (url: string, data: any) => {
    const token = localStorage.getItem('token');
    return fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
  }
};
```

---

## 📋 Templates de Scan

### Estruturas de Dados
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

interface ScanTemplateCreate {
  name: string;
  source: string;
  column_mapping: Record<string, string>;
  severity_map: Record<string, string>;
}
```

### APIs de Templates
```typescript
// Criar template
const createTemplate = async (template: ScanTemplateCreate): Promise<ScanTemplate> => {
  const response = await apiClient.post('/api/templates', template);
  return response.json();
};

// Listar templates
const listTemplates = async (): Promise<ScanTemplate[]> => {
  const response = await apiClient.get('/api/templates');
  return response.json();
};

// Buscar template específico
const getTemplate = async (id: number): Promise<ScanTemplate> => {
  const response = await apiClient.get(`/api/templates/${id}`);
  return response.json();
};

// Atualizar template
const updateTemplate = async (id: number, template: ScanTemplateCreate): Promise<ScanTemplate> => {
  const response = await fetch(`/api/templates/${id}`, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(template)
  });
  return response.json();
};

// Deletar template
const deleteTemplate = async (id: number): Promise<void> => {
  await fetch(`/api/templates/${id}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
  });
};
```

### Exemplo de Template
```typescript
const nessusTemplate: ScanTemplateCreate = {
  name: "Nessus Template",
  source: "Nessus",
  column_mapping: {
    "Host": "ip",
    "Name": "nvt_name",
    "Risk": "severity",
    "CVSS": "cvss",
    "CVE": "cves"
  },
  severity_map: {
    "critical": "Critical",
    "high": "High",
    "medium": "Medium",
    "low": "Low",
    "info": "Info"
  }
};
```

---

## 📤 Upload e Vulnerabilidades

### Estruturas de Dados
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

interface VulnerabilityStatusHistory {
  id: number;
  vuln_hash: string;
  month: string;
  status: 'new' | 'ongoing' | 'reopened' | 'closed';
  created_at: string;
}
```

### Upload de CSV
```typescript
const uploadCSV = async (
  file: File, 
  month: string, 
  templateId: number
): Promise<{ message: string }> => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('month', month);
  formData.append('template_id', templateId.toString());

  const response = await fetch('/api/vulnerability/upload', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    },
    body: formData
  });
  
  return response.json();
};
```

### APIs de Vulnerabilidades
```typescript
// Listar meses disponíveis
const getMonths = async (): Promise<string[]> => {
  const response = await apiClient.get('/api/vulnerability/months');
  return response.json();
};

// Listar vulnerabilidades com paginação
const listVulnerabilities = async (
  skip: number = 0, 
  limit: number = 100
): Promise<Vulnerability[]> => {
  const response = await apiClient.get(`/api/vulnerability/list?skip=${skip}&limit=${limit}`);
  return response.json();
};

// Histórico de vulnerabilidade
const getVulnerabilityHistory = async (vulnHash: string): Promise<VulnerabilityStatusHistory[]> => {
  const response = await apiClient.get(`/api/vulnerability/history/${vulnHash}`);
  return response.json();
};

// Deletar por mês
const deleteByMonth = async (month: string): Promise<void> => {
  await fetch(`/api/vulnerability/uploads/${month}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
  });
};

// Deletar tudo
const deleteAll = async (): Promise<void> => {
  await fetch('/api/vulnerability/uploads/all', {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
  });
};
```

---

## 🎨 Componentes Frontend Sugeridos

### 1. Template Manager
```typescript
interface TemplateManagerProps {
  onTemplateSelect: (template: ScanTemplate) => void;
}

const TemplateManager: React.FC<TemplateManagerProps> = ({ onTemplateSelect }) => {
  const [templates, setTemplates] = useState<ScanTemplate[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadTemplates = async () => {
      try {
        const data = await listTemplates();
        setTemplates(data);
      } catch (error) {
        console.error('Erro ao carregar templates:', error);
      } finally {
        setLoading(false);
      }
    };
    loadTemplates();
  }, []);

  return (
    <div>
      <h3>Templates de Scan</h3>
      {loading ? (
        <p>Carregando...</p>
      ) : (
        <div>
          {templates.map(template => (
            <div key={template.id} onClick={() => onTemplateSelect(template)}>
              <h4>{template.name}</h4>
              <p>Fonte: {template.source}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
```

### 2. CSV Upload
```typescript
interface CSVUploadProps {
  selectedTemplate: ScanTemplate | null;
  onUploadSuccess: () => void;
}

const CSVUpload: React.FC<CSVUploadProps> = ({ selectedTemplate, onUploadSuccess }) => {
  const [file, setFile] = useState<File | null>(null);
  const [month, setMonth] = useState('');
  const [uploading, setUploading] = useState(false);

  const handleUpload = async () => {
    if (!file || !selectedTemplate || !month) return;

    setUploading(true);
    try {
      await uploadCSV(file, month, selectedTemplate.id);
      onUploadSuccess();
    } catch (error) {
      console.error('Erro no upload:', error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <h3>Upload de CSV</h3>
      <input 
        type="file" 
        accept=".csv" 
        onChange={(e) => setFile(e.target.files?.[0] || null)} 
      />
      <input 
        type="month" 
        value={month} 
        onChange={(e) => setMonth(e.target.value)} 
      />
      <button 
        onClick={handleUpload} 
        disabled={!file || !selectedTemplate || !month || uploading}
      >
        {uploading ? 'Enviando...' : 'Upload'}
      </button>
    </div>
  );
};
```

### 3. Vulnerability List
```typescript
interface VulnerabilityListProps {
  vulnerabilities: Vulnerability[];
  onVulnerabilityClick: (vulnerability: Vulnerability) => void;
}

const VulnerabilityList: React.FC<VulnerabilityListProps> = ({ 
  vulnerabilities, 
  onVulnerabilityClick 
}) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'new': return 'green';
      case 'ongoing': return 'orange';
      case 'reopened': return 'red';
      case 'closed': return 'gray';
      default: return 'black';
    }
  };

  return (
    <div>
      <h3>Vulnerabilidades</h3>
      <table>
        <thead>
          <tr>
            <th>IP</th>
            <th>Vulnerabilidade</th>
            <th>Severidade</th>
            <th>Status</th>
            <th>Mês</th>
          </tr>
        </thead>
        <tbody>
          {vulnerabilities.map(vuln => (
            <tr key={vuln.id} onClick={() => onVulnerabilityClick(vuln)}>
              <td>{vuln.ip}</td>
              <td>{vuln.nvt_name}</td>
              <td>{vuln.severity}</td>
              <td style={{ color: getStatusColor(vuln.status) }}>
                {vuln.status}
              </td>
              <td>{vuln.reference_month}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
```

### 4. Vulnerability History
```typescript
interface VulnerabilityHistoryProps {
  vulnHash: string;
}

const VulnerabilityHistory: React.FC<VulnerabilityHistoryProps> = ({ vulnHash }) => {
  const [history, setHistory] = useState<VulnerabilityStatusHistory[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const data = await getVulnerabilityHistory(vulnHash);
        setHistory(data);
      } catch (error) {
        console.error('Erro ao carregar histórico:', error);
      } finally {
        setLoading(false);
      }
    };
    loadHistory();
  }, [vulnHash]);

  return (
    <div>
      <h3>Histórico da Vulnerabilidade</h3>
      {loading ? (
        <p>Carregando...</p>
      ) : (
        <div>
          {history.map(record => (
            <div key={record.id}>
              <span>{record.month}</span>
              <span style={{ color: getStatusColor(record.status) }}>
                {record.status}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
```

---

## 📊 Dashboards e Relatórios

### 1. Status Distribution
```typescript
const StatusDistribution: React.FC = () => {
  const [vulnerabilities, setVulnerabilities] = useState<Vulnerability[]>([]);

  const statusCount = vulnerabilities.reduce((acc, vuln) => {
    acc[vuln.status] = (acc[vuln.status] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  return (
    <div>
      <h3>Distribuição por Status</h3>
      <div>
        {Object.entries(statusCount).map(([status, count]) => (
          <div key={status}>
            <span>{status}: {count}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
```

### 2. Monthly Trends
```typescript
const MonthlyTrends: React.FC = () => {
  const [months, setMonths] = useState<string[]>([]);
  const [vulnerabilities, setVulnerabilities] = useState<Vulnerability[]>([]);

  const monthlyData = months.map(month => {
    const monthVulns = vulnerabilities.filter(v => v.reference_month === month);
    return {
      month,
      total: monthVulns.length,
      new: monthVulns.filter(v => v.status === 'new').length,
      ongoing: monthVulns.filter(v => v.status === 'ongoing').length,
      reopened: monthVulns.filter(v => v.status === 'reopened').length,
      closed: monthVulns.filter(v => v.status === 'closed').length
    };
  });

  return (
    <div>
      <h3>Tendências Mensais</h3>
      {/* Implementar gráfico com biblioteca como Chart.js ou Recharts */}
    </div>
  );
};
```

---

## 🚀 Fluxo Completo de Integração

### 1. Setup Inicial
```typescript
// Configurar interceptor de autenticação
const setupAuth = () => {
  // Verificar token no localStorage
  const token = localStorage.getItem('token');
  if (!token) {
    // Redirecionar para login
    window.location.href = '/login';
  }
};
```

### 2. Fluxo de Upload
```typescript
const uploadFlow = async () => {
  // 1. Selecionar template
  const template = await selectTemplate();
  
  // 2. Fazer upload
  await uploadCSV(file, month, template.id);
  
  // 3. Recarregar lista de vulnerabilidades
  await loadVulnerabilities();
  
  // 4. Mostrar relatórios atualizados
  await updateReports();
};
```

### 3. Gerenciamento de Estado
```typescript
// Usar Context API ou Redux para gerenciar estado global
interface AppState {
  templates: ScanTemplate[];
  vulnerabilities: Vulnerability[];
  selectedTemplate: ScanTemplate | null;
  loading: boolean;
  error: string | null;
}
```

---

## ⚠️ Considerações Importantes

1. **Autenticação**: Sempre incluir token JWT em todas as requisições
2. **Tratamento de Erros**: Implementar tratamento robusto de erros
3. **Loading States**: Mostrar indicadores de carregamento
4. **Validação**: Validar dados antes de enviar para o backend
5. **Cache**: Considerar cache para templates e dados estáticos
6. **Pagination**: Implementar paginação para grandes volumes de dados

---

## 📞 Suporte

Para dúvidas sobre integração:

1. Consultar `API_DOCUMENTATION.md` para detalhes técnicos
2. Verificar `README_NEW_FEATURES.md` para funcionalidades
3. Executar `test_new_features.py` para testes
4. Usar `migrate_database.py` para migração do banco

---

## 🎯 Próximos Passos

1. **Implementar Interface**: Criar componentes React/Vue/Angular
2. **Testes Frontend**: Implementar testes unitários e E2E
3. **Validação**: Adicionar validações de formulário
4. **UX/UI**: Melhorar experiência do usuário
5. **Performance**: Otimizar carregamento de dados 