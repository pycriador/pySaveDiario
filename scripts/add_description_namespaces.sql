-- Add product description namespaces
-- These namespaces convert HTML from the editor to formatted text for social networks

INSERT INTO namespaces (name, label, description, scope, created_at, updated_at)
SELECT 'product_description', 'Descrição do Produto', 'Descrição completa do produto (converte HTML para texto formatado)', 'OFFER', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM namespaces WHERE name = 'product_description');

INSERT INTO namespaces (name, label, description, scope, created_at, updated_at)
SELECT 'description', 'Descrição', 'Descrição do produto (atalho)', 'OFFER', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM namespaces WHERE name = 'description');

INSERT INTO namespaces (name, label, description, scope, created_at, updated_at)
SELECT 'descricao', 'Descrição (PT)', 'Descrição do produto em português', 'OFFER', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM namespaces WHERE name = 'descricao');

