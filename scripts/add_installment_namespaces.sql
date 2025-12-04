-- Add installment namespaces to offers

-- Installment count
INSERT OR IGNORE INTO namespaces (name, label, description, scope, created_at, updated_at)
VALUES ('installment_count', 'Quantidade de Parcelas', 'Número de parcelas da oferta (ex: 5)', 'OFFER', datetime('now'), datetime('now'));

-- Installment value
INSERT OR IGNORE INTO namespaces (name, label, description, scope, created_at, updated_at)
VALUES ('installment_value', 'Valor da Parcela', 'Valor de cada parcela (ex: 72.00)', 'OFFER', datetime('now'), datetime('now'));

-- Installment interest free
INSERT OR IGNORE INTO namespaces (name, label, description, scope, created_at, updated_at)
VALUES ('installment_interest_free', 'Com/Sem Juros', 'Se o parcelamento tem juros (ex: sem juros)', 'OFFER', datetime('now'), datetime('now'));

-- Full installment text (formatted)
INSERT OR IGNORE INTO namespaces (name, label, description, scope, created_at, updated_at)
VALUES ('installment_full', 'Parcelamento Completo', 'Texto formatado completo do parcelamento (ex: 5x de R$ 72.00 sem juros)', 'OFFER', datetime('now'), datetime('now'));

