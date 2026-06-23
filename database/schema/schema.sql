-- RT Voyage — PostgreSQL Schema
-- Encoding: UTF-8

-- ─── Extensions ───────────────────────────────────────────────────────────────
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ─── Countries ────────────────────────────────────────────────────────────────
CREATE TABLE countries (
  id            SERIAL PRIMARY KEY,
  name_fr       VARCHAR(100) NOT NULL,
  name_en       VARCHAR(100) NOT NULL,
  code          VARCHAR(3) NOT NULL UNIQUE,
  continent     VARCHAR(50),
  capital       VARCHAR(100),
  currency      VARCHAR(60),
  currency_code VARCHAR(10),
  language      VARCHAR(100),
  flag_emoji    VARCHAR(10),
  description_fr TEXT,
  description_en TEXT,
  image         VARCHAR(255),
  is_active     BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE INDEX idx_countries_code ON countries(code);

-- ─── Users ────────────────────────────────────────────────────────────────────
CREATE TABLE users (
  id             SERIAL PRIMARY KEY,
  username       VARCHAR(80) NOT NULL UNIQUE,
  email          VARCHAR(255) NOT NULL UNIQUE,
  password_hash  VARCHAR(255) NOT NULL,
  first_name     VARCHAR(100),
  last_name      VARCHAR(100),
  phone          VARCHAR(20),
  role           VARCHAR(20) NOT NULL DEFAULT 'client',
  is_active      BOOLEAN NOT NULL DEFAULT TRUE,
  avatar         VARCHAR(255),
  preferred_lang VARCHAR(5) DEFAULT 'fr',
  created_at     TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  last_login     TIMESTAMP WITH TIME ZONE
);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role  ON users(role);

-- ─── Destinations ─────────────────────────────────────────────────────────────
CREATE TABLE destinations (
  id                SERIAL PRIMARY KEY,
  slug              VARCHAR(120) NOT NULL UNIQUE,
  name_fr           VARCHAR(120) NOT NULL,
  name_en           VARCHAR(120) NOT NULL,
  region            VARCHAR(100),
  short_desc_fr     VARCHAR(500),
  short_desc_en     VARCHAR(500),
  long_desc_fr      TEXT,
  long_desc_en      TEXT,
  history_fr        TEXT,
  history_en        TEXT,
  culture_fr        TEXT,
  culture_en        TEXT,
  gastronomy_fr     TEXT,
  gastronomy_en     TEXT,
  country_id        INTEGER NOT NULL REFERENCES countries(id) ON DELETE SET NULL,
  destination_type  VARCHAR(30) DEFAULT 'city',
  latitude          NUMERIC(10,7),
  longitude         NUMERIC(10,7),
  timezone_name     VARCHAR(50),
  altitude_m        INTEGER,
  image_main        VARCHAR(255),
  image_thumb       VARCHAR(255),
  video_url         VARCHAR(500),
  video_drone_url   VARCHAR(500),
  youtube_id        VARCHAR(50),
  vimeo_id          VARCHAR(50),
  street_view_lat   NUMERIC(10,7),
  street_view_lng   NUMERIC(10,7),
  climate_fr        TEXT,
  climate_en        TEXT,
  best_period_fr    VARCHAR(200),
  best_period_en    VARCHAR(200),
  avg_temp_jan      INTEGER,
  avg_temp_jul      INTEGER,
  average_budget_eur INTEGER,
  budget_low        NUMERIC(10,2),
  budget_high       NUMERIC(10,2),
  currency_local    VARCHAR(30),
  difficulty_level  VARCHAR(20) DEFAULT 'easy',
  safety_level      VARCHAR(20) DEFAULT 'safe',
  visa_required     BOOLEAN DEFAULT FALSE,
  visa_info_fr      TEXT,
  meta_title_fr     VARCHAR(200),
  meta_title_en     VARCHAR(200),
  meta_desc_fr      VARCHAR(300),
  meta_desc_en      VARCHAR(300),
  is_featured       BOOLEAN NOT NULL DEFAULT FALSE,
  is_active         BOOLEAN NOT NULL DEFAULT TRUE,
  view_count        INTEGER NOT NULL DEFAULT 0,
  created_at        TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at        TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_dest_slug    ON destinations(slug);
CREATE INDEX idx_dest_country ON destinations(country_id);
CREATE INDEX idx_dest_featured ON destinations(is_featured) WHERE is_featured = TRUE;
CREATE INDEX idx_dest_type    ON destinations(destination_type);
CREATE INDEX idx_dest_name_trgm ON destinations USING GIN (name_fr gin_trgm_ops);

-- ─── Activity categories & activities ─────────────────────────────────────────
CREATE TABLE activity_categories (
  id       SERIAL PRIMARY KEY,
  slug     VARCHAR(80) NOT NULL UNIQUE,
  name_fr  VARCHAR(100) NOT NULL,
  name_en  VARCHAR(100),
  icon     VARCHAR(80),
  color    VARCHAR(20)
);

CREATE TABLE activities (
  id            SERIAL PRIMARY KEY,
  slug          VARCHAR(150) NOT NULL UNIQUE,
  name_fr       VARCHAR(150) NOT NULL,
  name_en       VARCHAR(150) NOT NULL,
  description_fr TEXT,
  description_en TEXT,
  category_id   INTEGER REFERENCES activity_categories(id),
  duration_hours NUMERIC(5,1),
  difficulty    VARCHAR(20) DEFAULT 'easy',
  min_age       INTEGER,
  max_participants INTEGER,
  price_per_person NUMERIC(10,2),
  currency      VARCHAR(5) DEFAULT 'EUR',
  image         VARCHAR(500),
  video_url     VARCHAR(500),
  location_name VARCHAR(150),
  latitude      NUMERIC(10,7),
  longitude     NUMERIC(10,7),
  includes_fr   TEXT,
  includes_en   TEXT,
  excludes_fr   TEXT,
  excludes_en   TEXT,
  is_featured   BOOLEAN DEFAULT FALSE,
  is_active     BOOLEAN NOT NULL DEFAULT TRUE,
  activity_type VARCHAR(30)
);

CREATE TABLE destination_activities (
  destination_id INTEGER NOT NULL REFERENCES destinations(id) ON DELETE CASCADE,
  activity_id    INTEGER NOT NULL REFERENCES activities(id)   ON DELETE CASCADE,
  sort_order     SMALLINT DEFAULT 0,
  PRIMARY KEY (destination_id, activity_id)
);

CREATE TABLE destination_themes (
  destination_id INTEGER NOT NULL REFERENCES destinations(id) ON DELETE CASCADE,
  theme          VARCHAR(50) NOT NULL,
  PRIMARY KEY (destination_id, theme)
);

-- ─── Hotels ───────────────────────────────────────────────────────────────────
CREATE TABLE hotels (
  id                SERIAL PRIMARY KEY,
  slug              VARCHAR(150) NOT NULL UNIQUE,
  name              VARCHAR(150) NOT NULL,
  hotel_type        VARCHAR(30) DEFAULT 'hotel',
  stars             SMALLINT CHECK (stars BETWEEN 1 AND 5),
  destination_id    INTEGER REFERENCES destinations(id) ON DELETE SET NULL,
  address           VARCHAR(300),
  latitude          NUMERIC(10,7),
  longitude         NUMERIC(10,7),
  phone             VARCHAR(30),
  email             VARCHAR(150),
  website           VARCHAR(255),
  description_fr    TEXT,
  description_en    TEXT,
  image_main        VARCHAR(500),
  amenities         TEXT,
  check_in_time     VARCHAR(10),
  check_out_time    VARCHAR(10),
  has_pool          BOOLEAN DEFAULT FALSE,
  has_spa           BOOLEAN DEFAULT FALSE,
  has_restaurant    BOOLEAN DEFAULT FALSE,
  has_wifi          BOOLEAN DEFAULT TRUE,
  has_parking       BOOLEAN DEFAULT FALSE,
  has_gym           BOOLEAN DEFAULT FALSE,
  has_bar           BOOLEAN DEFAULT FALSE,
  has_beach_access  BOOLEAN DEFAULT FALSE,
  price_min         NUMERIC(10,2),
  price_max         NUMERIC(10,2),
  currency          VARCHAR(5) DEFAULT 'EUR',
  rating            NUMERIC(3,1),
  review_count      INTEGER DEFAULT 0,
  booking_url       VARCHAR(500),
  is_partner        BOOLEAN DEFAULT FALSE,
  is_featured       BOOLEAN DEFAULT FALSE,
  is_active         BOOLEAN NOT NULL DEFAULT TRUE,
  created_at        TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_hotels_dest ON hotels(destination_id);
CREATE INDEX idx_hotels_slug ON hotels(slug);

-- ─── Travel Programs ──────────────────────────────────────────────────────────
CREATE TABLE travel_programs (
  id              SERIAL PRIMARY KEY,
  slug            VARCHAR(150) NOT NULL UNIQUE,
  name_fr         VARCHAR(200) NOT NULL,
  name_en         VARCHAR(200),
  tagline_fr      VARCHAR(300),
  tagline_en      VARCHAR(300),
  description_fr  TEXT,
  description_en  TEXT,
  image_main      VARCHAR(500),
  theme           VARCHAR(50) DEFAULT 'culture',
  duration_days   SMALLINT,
  duration_nights SMALLINT,
  group_min       SMALLINT DEFAULT 1,
  group_max       SMALLINT DEFAULT 20,
  price_per_person             NUMERIC(10,2),
  price_per_person_discounted  NUMERIC(10,2),
  currency        VARCHAR(5) DEFAULT 'EUR',
  departure_city  VARCHAR(100),
  departure_country_code VARCHAR(5),
  includes_fr     TEXT,
  includes_en     TEXT,
  excludes_fr     TEXT,
  excludes_en     TEXT,
  meta_title      VARCHAR(200),
  meta_description VARCHAR(320),
  difficulty      VARCHAR(20) DEFAULT 'easy',
  is_featured     BOOLEAN DEFAULT FALSE,
  is_active       BOOLEAN NOT NULL DEFAULT TRUE,
  view_count      INTEGER NOT NULL DEFAULT 0,
  booking_count   INTEGER NOT NULL DEFAULT 0,
  created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_prog_slug  ON travel_programs(slug);
CREATE INDEX idx_prog_theme ON travel_programs(theme);

CREATE TABLE program_destinations (
  program_id     INTEGER NOT NULL REFERENCES travel_programs(id) ON DELETE CASCADE,
  destination_id INTEGER NOT NULL REFERENCES destinations(id)    ON DELETE CASCADE,
  sort_order     SMALLINT DEFAULT 0,
  PRIMARY KEY (program_id, destination_id)
);

CREATE TABLE program_days (
  id             SERIAL PRIMARY KEY,
  program_id     INTEGER NOT NULL REFERENCES travel_programs(id) ON DELETE CASCADE,
  day_number     SMALLINT NOT NULL,
  title_fr       VARCHAR(200),
  title_en       VARCHAR(200),
  description_fr TEXT,
  description_en TEXT,
  morning_fr     TEXT,
  morning_en     TEXT,
  afternoon_fr   TEXT,
  afternoon_en   TEXT,
  evening_fr     TEXT,
  evening_en     TEXT,
  accommodation  VARCHAR(200),
  meals_included VARCHAR(20),
  image          VARCHAR(500),
  destination_id INTEGER REFERENCES destinations(id) ON DELETE SET NULL,
  UNIQUE (program_id, day_number)
);

-- ─── Airlines & Flight Promotions ─────────────────────────────────────────────
CREATE TABLE airlines (
  id                SERIAL PRIMARY KEY,
  slug              VARCHAR(100) NOT NULL UNIQUE,
  name              VARCHAR(150) NOT NULL,
  iata_code         VARCHAR(5) UNIQUE,
  country_code      VARCHAR(5),
  logo              VARCHAR(500),
  website           VARCHAR(300),
  description_fr    TEXT,
  description_en    TEXT,
  alliance          VARCHAR(80),
  baggage_cabin_kg  INTEGER,
  baggage_hold_kg   INTEGER,
  baggage_policy_fr TEXT,
  has_business_class BOOLEAN DEFAULT FALSE,
  has_first_class   BOOLEAN DEFAULT FALSE,
  is_partner        BOOLEAN DEFAULT FALSE,
  is_active         BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE flight_promotions (
  id           SERIAL PRIMARY KEY,
  airline_id   INTEGER NOT NULL REFERENCES airlines(id) ON DELETE CASCADE,
  title_fr     VARCHAR(200) NOT NULL,
  title_en     VARCHAR(200) NOT NULL,
  description_fr TEXT,
  origin       VARCHAR(100),
  destination  VARCHAR(100),
  origin_iata  VARCHAR(5),
  destination_iata VARCHAR(5),
  price_from   NUMERIC(10,2),
  currency     VARCHAR(5) DEFAULT 'EUR',
  valid_from   DATE,
  valid_until  DATE,
  booking_url  VARCHAR(500),
  image        VARCHAR(500),
  is_active    BOOLEAN NOT NULL DEFAULT TRUE,
  created_at   TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ─── Blog ─────────────────────────────────────────────────────────────────────
CREATE TABLE blog_categories (
  id             SERIAL PRIMARY KEY,
  slug           VARCHAR(80) NOT NULL UNIQUE,
  name_fr        VARCHAR(100) NOT NULL,
  name_en        VARCHAR(100) NOT NULL,
  description_fr TEXT,
  color          VARCHAR(20),
  icon           VARCHAR(80),
  is_active      BOOLEAN DEFAULT TRUE
);

CREATE TABLE blog_tags (
  id   SERIAL PRIMARY KEY,
  name VARCHAR(60) NOT NULL UNIQUE,
  slug VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE blog_posts (
  id              SERIAL PRIMARY KEY,
  slug            VARCHAR(200) NOT NULL UNIQUE,
  title_fr        VARCHAR(250) NOT NULL,
  title_en        VARCHAR(250),
  excerpt_fr      TEXT,
  excerpt_en      TEXT,
  content_fr      TEXT,
  content_en      TEXT,
  image_main      VARCHAR(255),
  image_alt_fr    VARCHAR(200),
  category_id     INTEGER REFERENCES blog_categories(id) ON DELETE SET NULL,
  author_id       INTEGER REFERENCES users(id) ON DELETE SET NULL,
  meta_title_fr   VARCHAR(200),
  meta_desc_fr    VARCHAR(300),
  is_published    BOOLEAN NOT NULL DEFAULT FALSE,
  is_featured     BOOLEAN NOT NULL DEFAULT FALSE,
  view_count      INTEGER NOT NULL DEFAULT 0,
  published_at    TIMESTAMP WITH TIME ZONE,
  created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_post_slug      ON blog_posts(slug);
CREATE INDEX idx_post_published ON blog_posts(is_published, published_at);

CREATE TABLE post_tags (
  post_id INTEGER NOT NULL REFERENCES blog_posts(id) ON DELETE CASCADE,
  tag_id  INTEGER NOT NULL REFERENCES blog_tags(id)  ON DELETE CASCADE,
  PRIMARY KEY (post_id, tag_id)
);

-- ─── Testimonials ─────────────────────────────────────────────────────────────
CREATE TABLE testimonials (
  id              SERIAL PRIMARY KEY,
  destination_id  INTEGER REFERENCES destinations(id) ON DELETE SET NULL,
  program_id      INTEGER REFERENCES travel_programs(id) ON DELETE SET NULL,
  user_id         INTEGER REFERENCES users(id) ON DELETE SET NULL,
  client_name     VARCHAR(120) NOT NULL,
  client_country  VARCHAR(80),
  client_photo    VARCHAR(500),
  rating          SMALLINT NOT NULL DEFAULT 5 CHECK (rating BETWEEN 1 AND 5),
  title           VARCHAR(200),
  comment         TEXT NOT NULL,
  travel_date     DATE,
  is_approved     BOOLEAN NOT NULL DEFAULT FALSE,
  is_featured     BOOLEAN NOT NULL DEFAULT FALSE,
  created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_testi_approved ON testimonials(is_approved) WHERE is_approved = TRUE;

-- ─── Contact Messages ─────────────────────────────────────────────────────────
CREATE TABLE contact_messages (
  id                   SERIAL PRIMARY KEY,
  first_name           VARCHAR(80) NOT NULL,
  last_name            VARCHAR(80) NOT NULL,
  email                VARCHAR(200) NOT NULL,
  phone                VARCHAR(30),
  destination_interest VARCHAR(150),
  subject              VARCHAR(200) NOT NULL,
  message              TEXT NOT NULL,
  lang                 VARCHAR(5) DEFAULT 'fr',
  ip_address           VARCHAR(50),
  is_read              BOOLEAN NOT NULL DEFAULT FALSE,
  is_replied           BOOLEAN NOT NULL DEFAULT FALSE,
  created_at           TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_contact_read ON contact_messages(is_read) WHERE is_read = FALSE;

-- ─── Newsletter ───────────────────────────────────────────────────────────────
CREATE TABLE newsletter_subscribers (
  id                  SERIAL PRIMARY KEY,
  email               VARCHAR(200) NOT NULL UNIQUE,
  first_name          VARCHAR(80),
  lang                VARCHAR(5) DEFAULT 'fr',
  is_active           BOOLEAN DEFAULT TRUE,
  confirmation_token  VARCHAR(100) UNIQUE,
  is_confirmed        BOOLEAN NOT NULL DEFAULT FALSE,
  unsubscribe_token   VARCHAR(100) UNIQUE,
  subscribed_at       TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  unsubscribed_at     TIMESTAMP WITH TIME ZONE
);
CREATE INDEX idx_newsletter_email ON newsletter_subscribers(email);

-- ─── FAQ ──────────────────────────────────────────────────────────────────────
CREATE TABLE faq_categories (
  id       SERIAL PRIMARY KEY,
  slug     VARCHAR(80) NOT NULL UNIQUE,
  name_fr  VARCHAR(120) NOT NULL,
  name_en  VARCHAR(120),
  icon     VARCHAR(50),
  "order"  SMALLINT DEFAULT 0
);

CREATE TABLE faq_items (
  id           SERIAL PRIMARY KEY,
  category_id  INTEGER NOT NULL REFERENCES faq_categories(id) ON DELETE CASCADE,
  question_fr  TEXT NOT NULL,
  question_en  TEXT,
  answer_fr    TEXT NOT NULL,
  answer_en    TEXT,
  "order"      SMALLINT DEFAULT 0,
  is_active    BOOLEAN NOT NULL DEFAULT TRUE,
  view_count   INTEGER DEFAULT 0
);

-- ─── Promotions ───────────────────────────────────────────────────────────────
CREATE TABLE promotions (
  id              SERIAL PRIMARY KEY,
  slug            VARCHAR(150) NOT NULL UNIQUE,
  title_fr        VARCHAR(200) NOT NULL,
  title_en        VARCHAR(200),
  description_fr  TEXT,
  description_en  TEXT,
  image           VARCHAR(255),
  promo_type      VARCHAR(30) DEFAULT 'general',
  destination_id  INTEGER REFERENCES destinations(id) ON DELETE SET NULL,
  original_price  NUMERIC(10,2),
  promo_price     NUMERIC(10,2),
  discount_percent INTEGER,
  currency        VARCHAR(5) DEFAULT 'EUR',
  promo_code      VARCHAR(30),
  valid_from      TIMESTAMP WITH TIME ZONE,
  valid_until     TIMESTAMP WITH TIME ZONE,
  is_active       BOOLEAN NOT NULL DEFAULT TRUE,
  is_featured     BOOLEAN DEFAULT FALSE,
  created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ─── Media ────────────────────────────────────────────────────────────────────
CREATE TABLE medias (
  id               SERIAL PRIMARY KEY,
  destination_id   INTEGER REFERENCES destinations(id) ON DELETE SET NULL,
  hotel_id         INTEGER REFERENCES hotels(id)       ON DELETE SET NULL,
  product_id       INTEGER,  -- FK vers shop_products(id) ajoutee plus bas, table pas encore creee a ce stade
  program_id       INTEGER REFERENCES travel_programs(id) ON DELETE SET NULL,
  post_id          INTEGER REFERENCES blog_posts(id)      ON DELETE SET NULL,
  filename         VARCHAR(255),            -- NULL when video_url is set
  original_name    VARCHAR(255),
  file_path        VARCHAR(500),
  file_type        VARCHAR(20),             -- image, video, pdf
  mime_type        VARCHAR(80),
  file_size        INTEGER,                 -- bytes
  file_size_kb     INTEGER,                 -- kilobytes (display)
  width            INTEGER,
  height           INTEGER,
  title_fr         VARCHAR(200),
  title_en         VARCHAR(200),
  alt_fr           VARCHAR(200),
  alt_text         VARCHAR(200),
  caption_fr       TEXT,
  video_url        VARCHAR(500),            -- external YouTube/Vimeo URL
  duration_seconds INTEGER,
  media_category   VARCHAR(30) DEFAULT 'gallery',
  is_active        BOOLEAN NOT NULL DEFAULT TRUE,
  sort_order       SMALLINT DEFAULT 0,
  uploaded_by      INTEGER REFERENCES users(id) ON DELETE SET NULL,
  created_at       TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  CONSTRAINT chk_media_source CHECK (filename IS NOT NULL OR video_url IS NOT NULL)
);
CREATE INDEX idx_media_dest    ON medias(destination_id);
CREATE INDEX idx_media_hotel   ON medias(hotel_id);
CREATE INDEX idx_media_program ON medias(program_id);
CREATE INDEX idx_media_post    ON medias(post_id);

-- ─── Shop ─────────────────────────────────────────────────────────────────────
CREATE TABLE shop_categories (
  id       SERIAL PRIMARY KEY,
  slug     VARCHAR(80) NOT NULL UNIQUE,
  name_fr  VARCHAR(100) NOT NULL,
  name_en  VARCHAR(100),
  icon     VARCHAR(80),
  image    VARCHAR(255),
  is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE shop_products (
  id               SERIAL PRIMARY KEY,
  slug             VARCHAR(150) NOT NULL UNIQUE,
  name_fr          VARCHAR(200) NOT NULL,
  name_en          VARCHAR(200),
  description_fr   TEXT,
  description_en   TEXT,
  image_main       VARCHAR(500),
  category_id      INTEGER REFERENCES shop_categories(id) ON DELETE SET NULL,
  price            NUMERIC(10,2) NOT NULL,
  price_discounted NUMERIC(10,2),
  currency         VARCHAR(5) DEFAULT 'EUR',
  stock            INTEGER DEFAULT -1,
  sku              VARCHAR(50) UNIQUE,
  brand            VARCHAR(100),
  affiliate_url    VARCHAR(500),
  is_affiliate     BOOLEAN DEFAULT FALSE,
  is_featured      BOOLEAN DEFAULT FALSE,
  is_active        BOOLEAN NOT NULL DEFAULT TRUE,
  rating           NUMERIC(3,1),
  review_count     INTEGER DEFAULT 0,
  created_at       TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

ALTER TABLE medias ADD CONSTRAINT fk_medias_product_id
  FOREIGN KEY (product_id) REFERENCES shop_products(id) ON DELETE SET NULL;
CREATE INDEX idx_media_product ON medias(product_id);

CREATE TABLE shop_orders (
  id           SERIAL PRIMARY KEY,
  user_id      INTEGER REFERENCES users(id) ON DELETE SET NULL,
  product_id   INTEGER REFERENCES shop_products(id) ON DELETE SET NULL,
  quantity     INTEGER DEFAULT 1,
  unit_price   NUMERIC(10,2),
  total_price  NUMERIC(10,2),
  status       VARCHAR(20) DEFAULT 'pending',
  created_at   TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ─── Bookings ─────────────────────────────────────────────────────────────────
CREATE TABLE bookings (
  id              SERIAL PRIMARY KEY,
  reference       VARCHAR(20) NOT NULL UNIQUE,
  user_id         INTEGER REFERENCES users(id) ON DELETE SET NULL,
  program_id      INTEGER REFERENCES travel_programs(id) ON DELETE SET NULL,
  first_name      VARCHAR(80) NOT NULL,
  last_name       VARCHAR(80) NOT NULL,
  email           VARCHAR(200) NOT NULL,
  phone           VARCHAR(30),
  nationality     VARCHAR(80),
  participants    INTEGER DEFAULT 1,
  departure_date  DATE,
  return_date     DATE,
  total_price     NUMERIC(10,2),
  currency        VARCHAR(5) DEFAULT 'EUR',
  special_requests TEXT,
  status          VARCHAR(20) DEFAULT 'pending',
  payment_status  VARCHAR(20) DEFAULT 'unpaid',
  notes           TEXT,
  created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_bookings_user   ON bookings(user_id);
CREATE INDEX idx_bookings_status ON bookings(status);

-- ─── Commandes (panier) ────────────────────────────────────────────────────────
CREATE TABLE orders (
  id              SERIAL PRIMARY KEY,
  reference       VARCHAR(20) NOT NULL UNIQUE,
  user_id         INTEGER REFERENCES users(id) ON DELETE SET NULL,
  first_name      VARCHAR(80) NOT NULL,
  last_name       VARCHAR(80) NOT NULL,
  email           VARCHAR(200) NOT NULL,
  phone           VARCHAR(30),
  billing_address TEXT,
  status          VARCHAR(20) NOT NULL DEFAULT 'pending',
  -- statuses: pending, confirmed, paid, processing, completed, cancelled, refunded
  payment_status  VARCHAR(20) NOT NULL DEFAULT 'pending',
  subtotal        NUMERIC(12,2) NOT NULL DEFAULT 0,
  total           NUMERIC(12,2) NOT NULL DEFAULT 0,
  currency        VARCHAR(3) NOT NULL DEFAULT 'EUR',
  notes           TEXT,
  created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_orders_user   ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);

CREATE TABLE order_items (
  id              SERIAL PRIMARY KEY,
  order_id        INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  item_type       VARCHAR(20) NOT NULL,
  -- item_type: program, product
  program_id      INTEGER REFERENCES travel_programs(id) ON DELETE SET NULL,
  product_id      INTEGER REFERENCES shop_products(id) ON DELETE SET NULL,
  quantity        INTEGER NOT NULL DEFAULT 1,
  unit_price      NUMERIC(12,2) NOT NULL,
  departure_date  DATE,
  participants    INTEGER,
  subtotal        NUMERIC(12,2) NOT NULL,
  CONSTRAINT chk_order_item_type CHECK (
    (item_type = 'program' AND program_id IS NOT NULL AND product_id IS NULL) OR
    (item_type = 'product' AND product_id IS NOT NULL AND program_id IS NULL)
  )
);
CREATE INDEX idx_order_items_order ON order_items(order_id);

-- ─── RSS Items ────────────────────────────────────────────────────────────────
CREATE TABLE rss_items (
  id           SERIAL PRIMARY KEY,
  title        VARCHAR(300) NOT NULL,
  link         VARCHAR(500),
  description  TEXT,
  category     VARCHAR(50) DEFAULT 'news',
  image        VARCHAR(255),
  is_active    BOOLEAN NOT NULL DEFAULT TRUE,
  published_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ─── Views ────────────────────────────────────────────────────────────────────
CREATE OR REPLACE VIEW v_destination_stats AS
SELECT
  d.id,
  d.name_fr,
  d.view_count,
  COUNT(DISTINCT t.id)  AS testimonial_count,
  ROUND(AVG(t.rating), 1) AS avg_rating,
  COUNT(DISTINCT h.id)  AS hotel_count
FROM destinations d
LEFT JOIN testimonials t ON t.destination_id = d.id AND t.is_approved
LEFT JOIN hotels       h ON h.destination_id = d.id AND h.is_active
WHERE d.is_active
GROUP BY d.id;

CREATE OR REPLACE VIEW v_booking_stats AS
SELECT
  DATE_TRUNC('month', created_at) AS month,
  COUNT(*)                          AS total,
  SUM(total_price)                  AS revenue,
  COUNT(*) FILTER (WHERE status = 'confirmed') AS confirmed
FROM bookings
GROUP BY 1
ORDER BY 1;

-- ─── Triggers ────────────────────────────────────────────────────────────────
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END;
$$;

CREATE TRIGGER trg_destinations_upd BEFORE UPDATE ON destinations
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_bookings_upd BEFORE UPDATE ON bookings
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_orders_upd BEFORE UPDATE ON orders
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_posts_upd BEFORE UPDATE ON blog_posts
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();
