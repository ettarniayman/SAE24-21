-- RT Voyage — Additional Views & Triggers
-- Note: Core views and triggers are already defined in schema.sql
-- This file is reserved for future additions.

-- ─── Additional search index ──────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_dest_view_count ON destinations(view_count DESC);
CREATE INDEX IF NOT EXISTS idx_dest_budget     ON destinations(average_budget_eur);
CREATE INDEX IF NOT EXISTS idx_prog_price      ON travel_programs(price_per_person);
CREATE INDEX IF NOT EXISTS idx_hotel_stars     ON hotels(stars DESC);
CREATE INDEX IF NOT EXISTS idx_blog_published  ON blog_posts(published_at DESC) WHERE is_published = TRUE;
CREATE INDEX IF NOT EXISTS idx_promo_valid     ON promotions(valid_until) WHERE is_active = TRUE;
CREATE INDEX IF NOT EXISTS idx_booking_ref     ON bookings(reference);

-- ─── View: active promotions with program/dest info ───────────────────────────
CREATE OR REPLACE VIEW v_active_promotions AS
SELECT
  p.*,
  d.name_fr  AS dest_name_fr,
  d.image_main AS dest_image,
  tp.name_fr AS program_name_fr
FROM promotions p
LEFT JOIN destinations d  ON d.id  = p.destination_id
LEFT JOIN travel_programs tp ON tp.id = p.program_id
WHERE p.is_active = TRUE
  AND (p.valid_until IS NULL OR p.valid_until >= CURRENT_DATE);

-- ─── View: featured blog posts with author info ───────────────────────────────
CREATE OR REPLACE VIEW v_featured_posts AS
SELECT
  bp.*,
  u.first_name || ' ' || u.last_name AS author_name,
  bc.name_fr AS category_name_fr,
  bc.slug    AS category_slug
FROM blog_posts bp
LEFT JOIN users          u  ON u.id  = bp.author_id
LEFT JOIN blog_categories bc ON bc.id = bp.category_id
WHERE bp.is_published = TRUE
ORDER BY bp.is_featured DESC, bp.published_at DESC;

-- ─── Trigger: auto-generate booking reference ─────────────────────────────────
CREATE OR REPLACE FUNCTION generate_booking_reference()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  IF NEW.reference IS NULL OR NEW.reference = '' THEN
    NEW.reference := 'RTV' || UPPER(SUBSTRING(MD5(RANDOM()::TEXT) FROM 1 FOR 8));
  END IF;
  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_booking_reference ON bookings;
CREATE TRIGGER trg_booking_reference
  BEFORE INSERT ON bookings
  FOR EACH ROW EXECUTE FUNCTION generate_booking_reference();

-- ─── Trigger: increment view_count safely ─────────────────────────────────────
CREATE OR REPLACE FUNCTION increment_dest_view()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  UPDATE destinations SET view_count = view_count + 1 WHERE id = NEW.id;
  RETURN NEW;
END;
$$;
