-- Add price_with_coupon namespace

INSERT OR IGNORE INTO namespaces (name, label, description, scope, created_at, updated_at)
VALUES ('price_with_coupon', 'Preço com Cupom', 'Preço do produto com o desconto do cupom aplicado (ex: R$ 90.00)', 'OFFER', datetime('now'), datetime('now'));

