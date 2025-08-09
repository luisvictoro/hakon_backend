#!/usr/bin/env python3
"""
Script de migração para adicionar campos de alterações manuais na tabela vulnerabilities
"""

import os
import sys
from dotenv import load_dotenv

# Adiciona o app directory ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

load_dotenv()

from app.database import engine, SessionLocal
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_vulnerability_table():
    """Adiciona novos campos na tabela vulnerabilities"""
    
    db = SessionLocal()
    
    try:
        logger.info("Iniciando migração da tabela vulnerabilities...")
        
        # Verifica se os campos já existem
        result = db.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'vulnerabilities' 
            AND column_name IN ('original_severity', 'severity_manually_changed', 'original_status', 'status_manually_changed')
        """))
        
        existing_columns = [row[0] for row in result.fetchall()]
        logger.info(f"Colunas existentes: {existing_columns}")
        
        # Adiciona campos se não existirem
        if 'original_severity' not in existing_columns:
            logger.info("Adicionando campo original_severity...")
            db.execute(text("ALTER TABLE vulnerabilities ADD COLUMN original_severity VARCHAR(20) NOT NULL DEFAULT 'Medium'"))
        
        if 'severity_manually_changed' not in existing_columns:
            logger.info("Adicionando campo severity_manually_changed...")
            db.execute(text("ALTER TABLE vulnerabilities ADD COLUMN severity_manually_changed BOOLEAN DEFAULT FALSE"))
        
        if 'original_status' not in existing_columns:
            logger.info("Adicionando campo original_status...")
            db.execute(text("ALTER TABLE vulnerabilities ADD COLUMN original_status VARCHAR(20) NOT NULL DEFAULT 'new'"))
        
        if 'status_manually_changed' not in existing_columns:
            logger.info("Adicionando campo status_manually_changed...")
            db.execute(text("ALTER TABLE vulnerabilities ADD COLUMN status_manually_changed BOOLEAN DEFAULT FALSE"))

        # Adiciona colunas base de parse solicitadas, se não existirem
        parse_columns = [
            ("port", "INTEGER"),
            ("summary", "TEXT"),
            ("impact", "TEXT"),
            ("solution", "TEXT"),
            ("affects", "TEXT"),
            ("parameter", "VARCHAR(255)"),
            ("request", "TEXT"),
            ("raw_text_details", "TEXT")
        ]
        # Coleta todas as colunas existentes
        result_all = db.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'vulnerabilities'
        """))
        existing_all = {row[0] for row in result_all.fetchall()}
        for column_name, column_type in parse_columns:
            if column_name not in existing_all:
                logger.info(f"Adicionando coluna {column_name}...")
                db.execute(text(f"ALTER TABLE vulnerabilities ADD COLUMN {column_name} {column_type}"))
        
        # Atualiza registros existentes
        logger.info("Atualizando registros existentes...")
        db.execute(text("""
            UPDATE vulnerabilities 
            SET 
                original_severity = severity,
                original_status = status
            WHERE original_severity IS NULL OR original_status IS NULL
        """))
        
        db.commit()
        logger.info("✅ Migração concluída com sucesso!")
        
    except Exception as e:
        logger.error(f"❌ Erro na migração: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def create_manual_changes_table():
    """Cria a tabela de histórico de alterações manuais"""
    
    db = SessionLocal()
    
    try:
        logger.info("Criando tabela vulnerability_manual_change_history...")
        
        # Verifica se a tabela já existe
        result = db.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = 'vulnerability_manual_change_history'
        """))
        
        if result.fetchone():
            logger.info("Tabela vulnerability_manual_change_history já existe")
            return
        
        # Cria a tabela
        db.execute(text("""
            CREATE TABLE vulnerability_manual_change_history (
                id SERIAL PRIMARY KEY,
                vulnerability_id INTEGER NOT NULL,
                vuln_hash VARCHAR(64) NOT NULL,
                field_changed VARCHAR(20) NOT NULL,
                old_value VARCHAR(50) NOT NULL,
                new_value VARCHAR(50) NOT NULL,
                changed_by VARCHAR(255) NOT NULL,
                changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                reason TEXT
            )
        """))
        
        # Cria índices
        db.execute(text("CREATE INDEX idx_vuln_manual_changes_vuln_id ON vulnerability_manual_change_history(vulnerability_id)"))
        db.execute(text("CREATE INDEX idx_vuln_manual_changes_hash ON vulnerability_manual_change_history(vuln_hash)"))
        db.execute(text("CREATE INDEX idx_vuln_manual_changes_changed_at ON vulnerability_manual_change_history(changed_at)"))
        
        db.commit()
        logger.info("✅ Tabela vulnerability_manual_change_history criada com sucesso!")
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar tabela: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def main():
    """Função principal"""
    logger.info("🚀 Iniciando migração para alterações manuais...")
    
    try:
        # Migra tabela vulnerabilities
        migrate_vulnerability_table()
        
        # Cria tabela de histórico
        create_manual_changes_table()
        
        logger.info("🎉 Migração concluída com sucesso!")
        logger.info("")
        logger.info("📋 Resumo das alterações:")
        logger.info("  ✅ Adicionados campos na tabela vulnerabilities:")
        logger.info("     - original_severity")
        logger.info("     - severity_manually_changed")
        logger.info("     - original_status")
        logger.info("     - status_manually_changed")
        logger.info("  ✅ Criada tabela vulnerability_manual_change_history")
        logger.info("")
        logger.info("🔧 Próximos passos:")
        logger.info("  1. Reiniciar a aplicação")
        logger.info("  2. Testar as novas APIs de alteração manual")
        
    except Exception as e:
        logger.error(f"❌ Falha na migração: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 