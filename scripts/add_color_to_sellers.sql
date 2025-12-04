-- Add color column to sellers table
-- This script adds a color field for visual identification of sellers

ALTER TABLE sellers ADD COLUMN color VARCHAR(255) DEFAULT '#6b7280';

-- Update default colors for known sellers
UPDATE sellers SET color = '#FFE600' WHERE LOWER(name) = 'mercado livre';
UPDATE sellers SET color = '#EE4D2D' WHERE LOWER(name) = 'shopee';
UPDATE sellers SET color = '#FF9900' WHERE LOWER(name) = 'amazon';
UPDATE sellers SET color = '#DC143C' WHERE LOWER(name) = 'magazine luiza';
UPDATE sellers SET color = '#E62129' WHERE LOWER(name) = 'aliexpress';
UPDATE sellers SET color = '#003DA5' WHERE LOWER(name) = 'kabum';
UPDATE sellers SET color = '#0070C0' WHERE LOWER(name) = 'casas bahia';
UPDATE sellers SET color = '#00A859' WHERE LOWER(name) = 'extra';

