from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import pandas as pd

from app import schemas
from app.services import template as template_service, auth as auth_service

router = APIRouter(dependencies=[Depends(auth_service.get_current_user)])


@router.post("/", response_model=schemas.ScanTemplate)
def create_template(
    template: schemas.ScanTemplateCreate,
    db: Session = Depends(auth_service.get_db),
    current_user = Depends(auth_service.get_current_user)
):
    """Criar template de importação"""
    return template_service.create_template(db, template, current_user.username)


@router.get("/", response_model=List[schemas.ScanTemplate])
def list_templates(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(auth_service.get_db)
):
    """Listar templates existentes"""
    return template_service.list_templates(db, skip=skip, limit=limit)


@router.get("/{template_id}", response_model=schemas.ScanTemplate)
def get_template(
    template_id: int,
    db: Session = Depends(auth_service.get_db)
):
    """Detalhar um template específico"""
    template = template_service.get_template(db, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.put("/{template_id}", response_model=schemas.ScanTemplate)
def update_template(
    template_id: int,
    template: schemas.ScanTemplateCreate,
    db: Session = Depends(auth_service.get_db)
):
    """Editar template"""
    updated_template = template_service.update_template(db, template_id, template)
    if not updated_template:
        raise HTTPException(status_code=404, detail="Template not found")
    return updated_template


@router.delete("/{template_id}")
def delete_template(
    template_id: int,
    db: Session = Depends(auth_service.get_db)
):
    """Excluir template"""
    success = template_service.delete_template(db, template_id)
    if not success:
        raise HTTPException(status_code=404, detail="Template not found")
    return {"message": "Template deleted successfully"}


@router.post("/auto-create")
def auto_create_template(
    file: UploadFile = File(...),
    name: str = Form(...),
    source: str = Form(...),
    db: Session = Depends(auth_service.get_db),
    current_user = Depends(auth_service.get_current_user)
):
    """Cria template automaticamente baseado no CSV"""
    try:
        # Lê CSV
        df = pd.read_csv(file.file)
        csv_columns = list(df.columns)

        # Mapeamento automático baseado em nomes de colunas
        auto_mapping = {}
        severity_map = {}

        # Mapeamento inteligente de colunas
        column_patterns = {
            'ip': ['ip', 'host_ip', 'target_ip', 'address'],
            'hostname': ['hostname', 'host_name', 'host', 'server', 'target'],
            'nvt_name': ['nvt_name', 'vulnerability_name', 'vuln_name', 'name', 'title'],
            'severity': ['severity', 'risk', 'level', 'priority'],
            'cvss': ['cvss', 'cvss_score', 'score'],
            'cves': ['cves', 'cve', 'cve_id', 'cve_ids']
        }

        for db_col, patterns in column_patterns.items():
            for csv_col in csv_columns:
                if any(pattern.lower() in csv_col.lower() for pattern in patterns):
                    auto_mapping[csv_col] = db_col
                    break

        # Mapeamento de severidade automático
        if 'severity' in auto_mapping:
            severity_col = auto_mapping['severity']
            if severity_col in df.columns:
                unique_severities = df[severity_col].dropna().unique()
                for sev in unique_severities:
                    sev_str = str(sev).lower()
                    if 'critical' in sev_str or 'crit' in sev_str:
                        severity_map[sev] = 'critical'
                    elif 'high' in sev_str:
                        severity_map[sev] = 'high'
                    elif 'medium' in sev_str or 'med' in sev_str:
                        severity_map[sev] = 'medium'
                    elif 'low' in sev_str:
                        severity_map[sev] = 'low'
                    else:
                        severity_map[sev] = 'medium'  # default

        # Verifica se tem mapeamentos essenciais
        required_mappings = ['ip', 'nvt_name']
        missing_required = [req for req in required_mappings if req not in auto_mapping.values()]

        if missing_required:
            return {
                "success": False,
                "error": f"Não foi possível mapear automaticamente: {missing_required}",
                "suggestions": {
                    "csv_columns": csv_columns,
                    "auto_mapping": auto_mapping,
                    "missing_required": missing_required
                }
            }

        # Cria template
        template_data = {
            "name": name,
            "source": source,
            "column_mapping": auto_mapping,
            "severity_map": severity_map
        }

        template = template_service.create_template(db, template_data, current_user.username)

        return {
            "success": True,
            "template": {
                "id": template.id,
                "name": template.name,
                "source": template.source,
                "column_mapping": template.column_mapping,
                "severity_map": template.severity_map
            },
            "analysis": {
                "csv_columns": csv_columns,
                "mapped_columns": list(auto_mapping.keys()),
                "unmapped_columns": [col for col in csv_columns if col not in auto_mapping],
                "severity_mappings": len(severity_map)
            }
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar template: {str(e)}") 