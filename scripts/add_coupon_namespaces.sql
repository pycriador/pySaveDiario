-- Add coupon-specific namespaces

INSERT OR IGNORE INTO namespaces (name, label, description, scope) VALUES
('coupon_code', 'Código do Cupom', 'Código do cupom de desconto (ex: PRIMEIRACOMPRA)', 'coupon'),
('code', 'Código (Alias)', 'Código do cupom - forma abreviada (ex: FRETE10)', 'coupon'),
('seller', 'Vendedor', 'Nome do vendedor/loja do cupom (ex: Mercado Livre)', 'coupon'),
('seller_name', 'Nome do Vendedor', 'Nome do vendedor - forma longa (ex: Magazine Luiza)', 'coupon'),
('coupon_expires', 'Validade do Cupom', 'Data de expiração do cupom (ex: 31/12/2025)', 'coupon');

-- Display results
SELECT 'Coupon namespaces added successfully!' AS status;
SELECT id, name, label, scope FROM namespaces WHERE scope = 'coupon';

