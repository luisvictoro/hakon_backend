#!/usr/bin/env python3
"""
Script para verificar e corrigir problemas no banco de dados
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

def check_tables():
    """Verifica se as tabelas necessárias existem"""
    
    db = SessionLocal()
    
    try:
        logger.info("🔍 Verificando tabelas do banco de dados...")
        
        # Verifica tabela vulnerabilities
        result = db.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = 'vulnerabilities'
        """))
        
        if result.fetchone():
            logger.info("✅ Tabela vulnerabilities existe")
        else:
            logger.error("❌ Tabela vulnerabilities não existe!")
            return False
        
        # Verifica tabela vulnerability_manual_change_history
        result = db.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = 'vulnerability_manual_change_history'
        """))
        
        if result.fetchone():
            logger.info("✅ Tabela vulnerability_manual_change_history existe")
        else:
            logger.warning("⚠️ Tabela vulnerability_manual_change_history não existe")
            return False
        
        # Verifica campos na tabela vulnerabilities
        result = db.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'vulnerabilities' 
            AND column_name IN ('original_severity', 'severity_manually_changed', 'original_status', 'status_manually_changed')
        """))
        
        existing_columns = [row[0] for row in result.fetchall()]
        logger.info(f"📋 Campos existentes na tabela vulnerabilities: {existing_columns}")
        
        required_columns = ['original_severity', 'severity_manually_changed', 'original_status', 'status_manually_changed']
        missing_columns = [col for col in required_columns if col not in existing_columns]
        
        if missing_columns:
            logger.warning(f"⚠️ Campos faltando: {missing_columns}")
            return False
        
        logger.info("✅ Todas as tabelas e campos necessários existem")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao verificar tabelas: {e}")
        return False
    finally:
        db.close()

def run_migrations():
    """Executa as migrações necessárias"""
    
    logger.info("🚀 Executando migrações...")
    
    try:
        # Importa e executa o script de migração
        from migrate_manual_changes import main as run_migration
        run_migration()
        return True
    except Exception as e:
        logger.error(f"❌ Erro ao executar migrações: {e}")
        return False

def test_simple_query():
    """Testa uma query simples para verificar se o banco está funcionando"""
    
    db = SessionLocal()
    
    try:
        logger.info("🧪 Testando query simples...")
        
        # Testa buscar uma vulnerabilidade
        result = db.execute(text("SELECT COUNT(*) FROM vulnerabilities"))
        count = result.fetchone()[0]
        
        logger.info(f"✅ Query funcionou! Encontradas {count} vulnerabilidades")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro na query: {e}")
        return False
    finally:
        db.close()

def main():
    """Função principal"""
    logger.info("🔧 Verificação e correção do banco de dados")
    logger.info("=" * 50)
    
    # Testa query simples primeiro
    if not test_simple_query():
        logger.error("❌ Banco de dados não está acessível")
        return
    
    # Verifica tabelas
    if not check_tables():
        logger.warning("⚠️ Problemas encontrados no banco. Executando migrações...")
        
        if run_migrations():
            logger.info("✅ Migrações executadas com sucesso")
            
            # Verifica novamente
            if check_tables():
                logger.info("🎉 Banco de dados corrigido com sucesso!")
            else:
                logger.error("❌ Problemas persistem após migrações")
        else:
            logger.error("❌ Falha ao executar migrações")
    else:
        logger.info("🎉 Banco de dados está OK!")

if __name__ == "__main__":
    main() 