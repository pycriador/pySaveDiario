-- Create social_network_configs table
CREATE TABLE IF NOT EXISTS social_network_configs (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    network VARCHAR(50) NOT NULL UNIQUE,
    prefix_text TEXT,
    suffix_text TEXT,
    active BOOLEAN
);

-- Insert default configurations
INSERT OR IGNORE INTO social_network_configs (network, prefix_text, suffix_text, active) VALUES
('instagram', '', '#ofertas #descontos #promoção', 1),
('facebook', '🔥 OFERTA IMPERDÍVEL!

', '

👍 Curta nossa página para não perder promoções!', 1),
('whatsapp', '💰 *PROMOÇÃO*

', '

_Compartilhe com quem precisa!_', 1),
('telegram', '📢 NOVA OFERTA!

', '

🔔 Ative as notificações do canal!', 1);

-- Update alembic_version to mark migration as applied
INSERT OR REPLACE INTO alembic_version (version_num) VALUES ('f8c2a9b4e5d7');

-- Display results
SELECT 'Table created and initialized successfully!' AS status;
SELECT * FROM social_network_configs;

