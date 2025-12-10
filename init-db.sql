-- Criação dos bancos de dados para o sistema Freela Facility
-- Este script é executado automaticamente quando o container PostgreSQL é iniciado

-- Cria o banco de dados secundário se não existir
SELECT 'CREATE DATABASE freela_facility_secondary'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'freela_facility_secondary')\gexec

-- Mensagem de confirmação
\echo 'Bancos de dados inicializados com sucesso!'
\echo 'Database principal: freela_facility (criado automaticamente)'
\echo 'Database secundário: freela_facility_secondary'
