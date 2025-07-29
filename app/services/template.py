from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.vulnerability import ScanTemplate
from app.schemas.vulnerability import ScanTemplateCreate


def create_template(db: Session, template: ScanTemplateCreate, created_by: str) -> ScanTemplate:
    db_template = ScanTemplate(
        name=template.name,
        source=template.source,
        column_mapping=template.column_mapping,
        severity_map=template.severity_map,
        created_by=created_by
    )
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template


def get_template(db: Session, template_id: int) -> Optional[ScanTemplate]:
    return db.query(ScanTemplate).filter(ScanTemplate.id == template_id).first()


def list_templates(db: Session, skip: int = 0, limit: int = 100) -> List[ScanTemplate]:
    return db.query(ScanTemplate).offset(skip).limit(limit).all()


def update_template(db: Session, template_id: int, template: ScanTemplateCreate) -> Optional[ScanTemplate]:
    db_template = db.query(ScanTemplate).filter(ScanTemplate.id == template_id).first()
    if db_template:
        db_template.name = template.name
        db_template.source = template.source
        db_template.column_mapping = template.column_mapping
        db_template.severity_map = template.severity_map
        db.commit()
        db.refresh(db_template)
    return db_template


def delete_template(db: Session, template_id: int) -> bool:
    db_template = db.query(ScanTemplate).filter(ScanTemplate.id == template_id).first()
    if db_template:
        db.delete(db_template)
        db.commit()
        return True
    return False 