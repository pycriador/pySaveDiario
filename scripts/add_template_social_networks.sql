-- Create template_social_networks association table

CREATE TABLE IF NOT EXISTS template_social_networks (
    template_id INTEGER NOT NULL,
    social_network_id INTEGER NOT NULL,
    PRIMARY KEY (template_id, social_network_id),
    FOREIGN KEY (template_id) REFERENCES templates(id) ON DELETE CASCADE,
    FOREIGN KEY (social_network_id) REFERENCES social_network_configs(id) ON DELETE CASCADE
);

-- Display results
SELECT 'Template-Social Networks association table created successfully!' AS status;

