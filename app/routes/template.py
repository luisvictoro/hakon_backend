from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

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