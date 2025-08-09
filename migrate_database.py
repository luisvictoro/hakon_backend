#!/usr/bin/env python3
"""
Script para migrar o banco de dados com as novas funcionalidades:
- Adicionar campos vuln_hash e status na tabela vulnerabilities
- Criar tabela scan_templates
- Criar tabela vulnerability_status_history
"""

import os
import sys
from sqlalchemy import text, create_engine
from sqlalchemy.exc import ProgrammingError

# Adiciona o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, Base
from app.models import vulnerability

def check_table_exists(engine, table_name):
    """Verifica se uma tabela existe"""
    with engine.connect() as conn:
        result = conn.execute(text(f"""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = '{table_name}'
            );
        """))
        return result.scalar()

def check_column_exists(engine, table_name, column_name):
    """Verifica se uma coluna existe em uma tabela"""
    with engine.connect() as conn:
        result = conn.execute(text(f"""
            SELECT EXISTS (
                SELECT FROM information_schema.columns 
                WHERE table_name = '{table_name}' 
                AND column_name = '{column_name}'
            );
        """))
        return result.scalar()

def migrate_vulnerabilities_table():
    """Adiciona os novos campos na tabela vulnerabilities"""
    print("🔧 Migrando tabela vulnerabilities...")
    
    with engine.connect() as conn:
        # Verifica se a tabela vulnerabilities existe
        if not check_table_exists(engine, 'vulnerabilities'):
            print("❌ Tabela vulnerabilities não encontrada. Criando...")
            Base.metadata.create_all(bind=engine, tables=[vulnerability.Vulnerability.__table__])
            print("✅ Tabela vulnerabilities criada")
            return
        
        # Adiciona campo vuln_hash se não existir
        if not check_column_exists(engine, 'vulnerabilities', 'vuln_hash'):
            print("➕ Adicionando campo vuln_hash...")
            try:
                conn.execute(text("""
                    ALTER TABLE vulnerabilities 
                    ADD COLUMN vuln_hash VARCHAR(64);
                """))
                conn.commit()
                print("✅ Campo vuln_hash adicionado")
            except ProgrammingError as e:
                print(f"⚠️ Erro ao adicionar vuln_hash: {e}")
        else:
            print("✅ Campo vuln_hash já existe")
        
        # Adiciona campo status se não existir
        if not check_column_exists(engine, 'vulnerabilities', 'status'):
            print("➕ Adicionando campo status...")
            try:
                conn.execute(text("""
                    ALTER TABLE vulnerabilities 
                    ADD COLUMN status VARCHAR(20) DEFAULT 'new';
                """))
                conn.commit()
                print("✅ Campo status adicionado")
            except ProgrammingError as e:
                print(f"⚠️ Erro ao adicionar status: {e}")
        else:
            print("✅ Campo status já existe")
        
        # Novos campos solicitados para base de parse (não remove existentes)
        new_columns_sql = [
            ("port", "INTEGER"),
            ("summary", "TEXT"),
            ("impact", "TEXT"),
            ("solution", "TEXT"),
            ("affects", "TEXT"),
            ("parameter", "VARCHAR(255)"),
            ("request", "TEXT"),
            ("raw_text_details", "TEXT")
        ]
        for column_name, column_type in new_columns_sql:
            if not check_column_exists(engine, 'vulnerabilities', column_name):
                print(f"➕ Adicionando coluna {column_name}...")
                try:
                    conn.execute(text(f"""
                        ALTER TABLE vulnerabilities 
                        ADD COLUMN {column_name} {column_type};
                    """))
                    conn.commit()
                    print(f"✅ Coluna {column_name} adicionada")
                except ProgrammingError as e:
                    print(f"⚠️ Erro ao adicionar {column_name}: {e}")
            else:
                print(f"✅ Coluna {column_name} já existe")

        # Adiciona índices se não existirem
        try:
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_vulnerabilities_vuln_hash 
                ON vulnerabilities(vuln_hash);
            """))
            conn.commit()
            print("✅ Índice em vuln_hash criado")
        except ProgrammingError as e:
            print(f"⚠️ Erro ao criar índice vuln_hash: {e}")

def migrate_scan_templates_table():
    """Cria a tabela scan_templates"""
    print("\n🔧 Migrando tabela scan_templates...")
    
    if not check_table_exists(engine, 'scan_templates'):
        print("➕ Criando tabela scan_templates...")
        try:
            Base.metadata.create_all(bind=engine, tables=[vulnerability.ScanTemplate.__table__])
            print("✅ Tabela scan_templates criada")
        except Exception as e:
            print(f"❌ Erro ao criar tabela scan_templates: {e}")
    else:
        print("✅ Tabela scan_templates já existe")

def migrate_vulnerability_status_history_table():
    """Cria a tabela vulnerability_status_history"""
    print("\n🔧 Migrando tabela vulnerability_status_history...")
    
    if not check_table_exists(engine, 'vulnerability_status_history'):
        print("➕ Criando tabela vulnerability_status_history...")
        try:
            Base.metadata.create_all(bind=engine, tables=[vulnerability.VulnerabilityStatusHistory.__table__])
            print("✅ Tabela vulnerability_status_history criada")
        except Exception as e:
            print(f"❌ Erro ao criar tabela vulnerability_status_history: {e}")
    else:
        print("✅ Tabela vulnerability_status_history já existe")

def update_existing_vulnerabilities():
    """Atualiza vulnerabilidades existentes com hash e status"""
    print("\n🔄 Atualizando vulnerabilidades existentes...")
    
    with engine.connect() as conn:
        # Verifica se há vulnerabilidades sem hash
        result = conn.execute(text("""
            SELECT COUNT(*) FROM vulnerabilities 
            WHERE vuln_hash IS NULL OR vuln_hash = '';
        """))
        count = result.scalar()
        
        if count > 0:
            print(f"📊 Encontradas {count} vulnerabilidades para atualizar")
            
            # Busca vulnerabilidades sem hash
            result = conn.execute(text("""
                SELECT id, ip, hostname, nvt_name, cves 
                FROM vulnerabilities 
                WHERE vuln_hash IS NULL OR vuln_hash = '';
            """))
            
            updated = 0
            for row in result:
                try:
                    # Gera hash para vulnerabilidade existente
                    import hashlib
                    
                    ip = str(row.ip).strip() if row.ip else ""
                    hostname = str(row.hostname).strip() if row.hostname else ""
                    nvt_name = str(row.nvt_name).strip() if row.nvt_name else ""
                    cves = str(row.cves).strip() if row.cves else ""
                    
                    # Ordena CVEs
                    if cves:
                        cve_list = sorted([cve.strip() for cve in cves.split(',')])
                        cves = ','.join(cve_list)
                    
                    hash_string = f"{ip}|{hostname}|{nvt_name}|{cves}"
                    vuln_hash = hashlib.sha256(hash_string.encode()).hexdigest()
                    
                    # Atualiza a vulnerabilidade
                    conn.execute(text("""
                        UPDATE vulnerabilities 
                        SET vuln_hash = :vuln_hash, status = 'new'
                        WHERE id = :id
                    """), {"vuln_hash": vuln_hash, "id": row.id})
                    
                    updated += 1
                    
                except Exception as e:
                    print(f"⚠️ Erro ao atualizar vulnerabilidade {row.id}: {e}")
            
            conn.commit()
            print(f"✅ {updated} vulnerabilidades atualizadas")
        else:
            print("✅ Todas as vulnerabilidades já possuem hash")

def main():
    """Função principal de migração"""
    print("🚀 Iniciando migração do banco de dados...")
    
    try:
        # Testa conexão com o banco
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Conexão com banco de dados estabelecida")
    except Exception as e:
        print(f"❌ Erro ao conectar com banco de dados: {e}")
        return
    
    # Executa migrações
    migrate_vulnerabilities_table()
    migrate_scan_templates_table()
    migrate_vulnerability_status_history_table()
    update_existing_vulnerabilities()
    
    print("\n🎉 Migração concluída com sucesso!")
    print("\n📋 Resumo das alterações:")
    print("- ✅ Campo vuln_hash adicionado à tabela vulnerabilities")
    print("- ✅ Campo status adicionado à tabela vulnerabilities")
    print("- ✅ Tabela scan_templates criada")
    print("- ✅ Tabela vulnerability_status_history criada")
    print("- ✅ Vulnerabilidades existentes atualizadas")

if __name__ == "__main__":
    main() 