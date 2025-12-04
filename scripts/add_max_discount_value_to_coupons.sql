-- Add max_discount_value column to coupons table
-- This column stores the maximum discount limit in the currency value
-- For example: 10% discount limited to R$ 70 maximum

ALTER TABLE coupons ADD COLUMN max_discount_value NUMERIC(10, 2);

-- Optional: Add comment explaining the field
-- max_discount_value: Maximum discount amount in currency (e.g., 70 for R$ 70 max)
-- When discount_type is 'percentage', this limits the calculated discount
-- When discount_type is 'fixed', this field is not used

-- Example usage:
-- Coupon: 10% discount, max R$ 70
-- - Product R$ 500 → 10% = R$ 50 discount → Final: R$ 450
-- - Product R$ 1000 → 10% = R$ 100, but max is R$ 70 → Final: R$ 930

