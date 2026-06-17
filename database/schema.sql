-- RT Voyage — PostgreSQL Schema
-- Encoding: UTF-8

-- ─── Extensions ───────────────────────────────────────────────────────────────
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ─── Enum types ───────────────────────────────────────────────────────────────
CREATE TYPE user_role      AS ENUM ('super_admin','admin','agent','client');
CREATE TYPE dest_type      AS ENUM ('city','nature','desert','mountain','beach','historical');
CREATE TYPE hotel_type     AS ENUM ('hotel','riad','villa','resort','hostel','apartment');
CREATE TYPE activity_type  AS ENUM ('monument','stadium','museum','medina','desert','mountain','hike','beach','surf','nautical','family','sport','cultural','luxury','excursion');
CREATE TYPE program_theme  AS ENUM ('culture','adventure','nature','luxury','sport','gastronomy','family','football');
CREATE TYPE booking_status AS ENUM ('pending','confirmed','cancelled','completed');
CREATE TYPE payment_status AS ENUM ('pending','paid','refunded','failed');
CREATE TYPE promo_type     AS ENUM ('general','flight','hotel','package','activity');
CREATE TYPE media_category AS ENUM ('main','gallery','drone','immersive','ai_generated','document');
CREATE TYPE rss_category   AS ENUM ('news','destination','promotion','article','partner');

-- ─── Countries ────────────────────────────────────────────────────────────────
CREATE TABLE countries (
  id            SERIAL PRIMARY KEY,
  name_fr       VARCHAR(100) NOT NULL,
  name_en       VARCHAR(100) NOT NULL,
  code          CHAR(2) NOT NULL UNIQUE,
  continent     VARCHAR(50),
  capital       VARCHAR(100),
  currency      VARCHAR(60),
  currency_code CHAR(3),
  language      VARCHAR(100),
  flag_emoji    VARCHAR(10),
  description   TEXT,
  image         VARCHAR(500),
  is_active     BOOLEAN NOT NULL DEFAULT TRUE,
  created_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_countries_code ON countries(code);

-- ─── Users ────────────────────────────────────────────────────────────────────
CREATE TABLE users (
  id             SERIAL PRIMARY KEY,
  username       VARCHAR(80) NOT NULL UNIQUE,
  email          VARCHAR(120) NOT NULL UNIQUE,
  password_hash  VARCHAR(256) NOT NULL,
  first_name     VARCHAR(80),
  last_name      VARCHAR(80),
  phone          VARCHAR(30),
  role           user_role NOT NULL DEFAULT 'client',
  is_active      BOOLEAN NOT NULL DEFAULT TRUE,
  avatar         VARCHAR(500),
  preferred_lang CHAR(2) DEFAULT 'fr',
  created_at     TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  last_login     TIMESTAMP WITH TIME ZONE
);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role  ON users(role);

-- ─── Destinations ─────────────────────────────────────────────────────────────
CREATE TABLE destinations (
  id                SERIAL PRIMARY KEY,
  slug              VARCHAR(150) NOT NULL UNIQUE,
  name_fr           VARCHAR(150) NOT NULL,
  name_en           VARCHAR(150),
  region            VARCHAR(100),
  short_desc_fr     TEXT,
  short_desc_en     TEXT,
  long_desc_fr      TEXT,
  long_desc_en      TEXT,
  history_fr        TEXT,
  history_en        TEXT,
  culture_fr        TEXT,
  culture_en        TEXT,
  gastronomy_fr     TEXT,
  gastronomy_en     TEXT,
  country_id        INTEGER REFERENCES countries(id) ON DELETE SET NULL,
  destination_type  dest_type DEFAULT 'city',
  latitude          NUMERIC(10,7),
  longitude         NUMERIC(10,7),
  timezone_name     VARCHAR(50),
  altitude_m        INTEGER,
  image_main        VARCHAR(500),
  image_thumb       VARCHAR(500),
  video_url         VARCHAR(500),
  video_drone_url   VARCHAR(500),
  youtube_id        VARCHAR(20),
  vimeo_id          VARCHAR(20),
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
  icon     VARCHAR(80)
);

CREATE TABLE activities (
  id            SERIAL PRIMARY KEY,
  slug          VARCHAR(150) NOT NULL UNIQUE,
  name_fr       VARCHAR(150) NOT NULL,
  name_en       VARCHAR(150),
  description_fr TEXT,
  description_en TEXT,
  category_id   INTEGER REFERENCES activity_categories(id),
  activity_type activity_type,
  image         VARCHAR(500),
  duration_h    NUMERIC(4,1),
  price_from    NUMERIC(10,2),
  is_active     BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE destination_activities (
  destination_id INTEGER NOT NULL REFERENCES destinations(id) ON DELETE CASCADE,
  activity_id    INTEGER NOT NULL REFERENCES activities(id)   ON DELETE CASCADE,
  sort_order     SMALLINT DEFAULT 0,
  PRIMARY KEY (destination_id, activity_id)
);

-- ─── Hotels ───────────────────────────────────────────────────────────────────
CREATE TABLE hotels (
  id                SERIAL PRIMARY KEY,
  slug              VARCHAR(150) NOT NULL UNIQUE,
  name              VARCHAR(150) NOT NULL,
  hotel_type        hotel_type DEFAULT 'hotel',
  stars             SMALLINT CHECK (stars BETWEEN 1 AND 5),
  destination_id    INTEGER REFERENCES destinations(id) ON DELETE SET NULL,
  address           VARCHAR(300),
  latitude          NUMERIC(10,7),
  longitude         NUMERIC(10,7),
  short_desc_fr     TEXT,
  short_desc_en     TEXT,
  long_desc_fr      TEXT,
  long_desc_en      TEXT,
  image_main        VARCHAR(500),
  amenities         TEXT,
  has_pool          BOOLEAN DEFAULT FALSE,
  has_spa           BOOLEAN DEFAULT FALSE,
  has_restaurant    BOOLEAN DEFAULT FALSE,
  has_wifi          BOOLEAN DEFAULT TRUE,
  has_parking       BOOLEAN DEFAULT FALSE,
  has_gym           BOOLEAN DEFAULT FALSE,
  has_bar           BOOLEAN DEFAULT FALSE,
  has_beach_access  BOOLEAN DEFAULT FALSE,
  price_from        NUMERIC(10,2),
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
  short_desc_fr   TEXT,
  short_desc_en   TEXT,
  long_desc_fr    TEXT,
  long_desc_en    TEXT,
  image_main      VARCHAR(500),
  theme           program_theme DEFAULT 'culture',
  duration_days   SMALLINT,
  duration_nights SMALLINT,
  group_min       SMALLINT DEFAULT 1,
  group_max       SMALLINT DEFAULT 20,
  price_per_person     NUMERIC(10,2),
  price_discounted     NUMERIC(10,2),
  departure_city  VARCHAR(100),
  includes_fr     TEXT,
  includes_en     TEXT,
  excludes_fr     TEXT,
  excludes_en     TEXT,
  meta_title      VARCHAR(200),
  meta_description VARCHAR(320),
  is_featured     BOOLEAN DEFAULT FALSE,
  is_active       BOOLEAN NOT NULL DEFAULT TRUE,
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
  morning_fr     TEXT,
  morning_en     TEXT,
  afternoon_fr   TEXT,
  afternoon_en   TEXT,
  evening_fr     TEXT,
  evening_en     TEXT,
  accommodation  VARCHAR(200),
  meals_included VARCHAR(3),
  UNIQUE (program_id, day_number)
);

-- ─── Airlines & Flight Promotions ─────────────────────────────────────────────
CREATE TABLE airlines (
  id                SERIAL PRIMARY KEY,
  slug              VARCHAR(100) NOT NULL UNIQUE,
  name              VARCHAR(150) NOT NULL,
  iata_code         CHAR(2) NOT NULL UNIQUE,
  logo              VARCHAR(500),
  website           VARCHAR(300),
  alliance          VARCHAR(80),
  baggage_cabin_kg  NUMERIC(4,1),
  baggage_hold_kg   NUMERIC(4,1),
  has_business_class BOOLEAN DEFAULT FALSE,
  has_first_class   BOOLEAN DEFAULT FALSE,
  is_partner        BOOLEAN DEFAULT FALSE,
  is_active         BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE flight_promotions (
  id           SERIAL PRIMARY KEY,
  airline_id   INTEGER NOT NULL REFERENCES airlines(id) ON DELETE CASCADE,
  origin       CHAR(3) NOT NULL,
  destination  CHAR(3) NOT NULL,
  price_from   NUMERIC(10,2) NOT NULL,
  currency     CHAR(3) DEFAULT 'MAD',
  valid_from   DATE,
  valid_until  DATE,
  booking_url  VARCHAR(500),
  is_active    BOOLEAN NOT NULL DEFAULT TRUE
);

-- ─── Blog ─────────────────────────────────────────────────────────────────────
CREATE TABLE blog_categories (
  id       SERIAL PRIMARY KEY,
  slug     VARCHAR(80) NOT NULL UNIQUE,
  name_fr  VARCHAR(100) NOT NULL,
  name_en  VARCHAR(100),
  icon     VARCHAR(80)
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
  image           VARCHAR(500),
  category_id     INTEGER REFERENCES blog_categories(id) ON DELETE SET NULL,
  author_id       INTEGER REFERENCES users(id) ON DELETE SET NULL,
  meta_title      VARCHAR(200),
  meta_description VARCHAR(320),
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
  client_name     VARCHAR(120) NOT NULL,
  client_country  VARCHAR(80),
  client_photo    VARCHAR(500),
  rating          SMALLINT NOT NULL DEFAULT 5 CHECK (rating BETWEEN 1 AND 5),
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
  email                VARCHAR(120) NOT NULL,
  phone                VARCHAR(30),
  destination_interest VARCHAR(120),
  subject              VARCHAR(80) NOT NULL,
  message              TEXT NOT NULL,
  ip_address           VARCHAR(45),
  is_read              BOOLEAN NOT NULL DEFAULT FALSE,
  is_replied           BOOLEAN NOT NULL DEFAULT FALSE,
  created_at           TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_contact_read ON contact_messages(is_read) WHERE is_read = FALSE;

-- ─── Newsletter ───────────────────────────────────────────────────────────────
CREATE TABLE newsletter_subscribers (
  id                  SERIAL PRIMARY KEY,
  email               VARCHAR(120) NOT NULL UNIQUE,
  first_name          VARCHAR(80),
  lang                CHAR(2) DEFAULT 'fr',
  confirmation_token  VARCHAR(64),
  is_confirmed        BOOLEAN NOT NULL DEFAULT FALSE,
  unsubscribe_token   VARCHAR(64) NOT NULL,
  subscribed_at       TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  confirmed_at        TIMESTAMP WITH TIME ZONE
);
CREATE INDEX idx_newsletter_email ON newsletter_subscribers(email);

-- ─── FAQ ──────────────────────────────────────────────────────────────────────
CREATE TABLE faq_categories (
  id       SERIAL PRIMARY KEY,
  slug     VARCHAR(80) NOT NULL UNIQUE,
  name_fr  VARCHAR(120) NOT NULL,
  name_en  VARCHAR(120),
  sort_order SMALLINT DEFAULT 0
);

CREATE TABLE faq_items (
  id           SERIAL PRIMARY KEY,
  category_id  INTEGER NOT NULL REFERENCES faq_categories(id) ON DELETE CASCADE,
  question_fr  TEXT NOT NULL,
  question_en  TEXT,
  answer_fr    TEXT NOT NULL,
  answer_en    TEXT,
  sort_order   SMALLINT DEFAULT 0,
  is_active    BOOLEAN NOT NULL DEFAULT TRUE
);

-- ─── Promotions ───────────────────────────────────────────────────────────────
CREATE TABLE promotions (
  id              SERIAL PRIMARY KEY,
  slug            VARCHAR(150) NOT NULL UNIQUE,
  title_fr        VARCHAR(200) NOT NULL,
  title_en        VARCHAR(200),
  description_fr  TEXT,
  description_en  TEXT,
  image           VARCHAR(500),
  promo_type      promo_type DEFAULT 'general',
  destination_id  INTEGER REFERENCES destinations(id) ON DELETE SET NULL,
  program_id      INTEGER REFERENCES travel_programs(id) ON DELETE SET NULL,
  original_price  NUMERIC(10,2),
  promo_price     NUMERIC(10,2),
  discount_percent NUMERIC(5,2),
  promo_code      VARCHAR(30),
  valid_from      DATE,
  valid_until     DATE,
  is_active       BOOLEAN NOT NULL DEFAULT TRUE,
  created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ─── Media ────────────────────────────────────────────────────────────────────
CREATE TABLE medias (
  id               SERIAL PRIMARY KEY,
  destination_id   INTEGER REFERENCES destinations(id) ON DELETE SET NULL,
  hotel_id         INTEGER REFERENCES hotels(id)       ON DELETE SET NULL,
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
CREATE INDEX idx_media_dest  ON medias(destination_id);
CREATE INDEX idx_media_hotel ON medias(hotel_id);

-- ─── Shop ─────────────────────────────────────────────────────────────────────
CREATE TABLE shop_categories (
  id       SERIAL PRIMARY KEY,
  slug     VARCHAR(80) NOT NULL UNIQUE,
  name_fr  VARCHAR(100) NOT NULL,
  name_en  VARCHAR(100),
  icon     VARCHAR(80)
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
  stock            INTEGER DEFAULT -1,
  affiliate_url    VARCHAR(500),
  is_affiliate     BOOLEAN DEFAULT FALSE,
  is_active        BOOLEAN NOT NULL DEFAULT TRUE,
  created_at       TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ─── Bookings ─────────────────────────────────────────────────────────────────
CREATE TABLE bookings (
  id              SERIAL PRIMARY KEY,
  reference       VARCHAR(20) NOT NULL UNIQUE,
  user_id         INTEGER REFERENCES users(id) ON DELETE SET NULL,
  program_id      INTEGER REFERENCES travel_programs(id) ON DELETE SET NULL,
  first_name      VARCHAR(80) NOT NULL,
  last_name       VARCHAR(80) NOT NULL,
  email           VARCHAR(120) NOT NULL,
  phone           VARCHAR(30),
  nationality     VARCHAR(80),
  participants    SMALLINT NOT NULL DEFAULT 1,
  departure_date  DATE,
  return_date     DATE,
  special_requests TEXT,
  total_price     NUMERIC(12,2),
  currency        CHAR(3) DEFAULT 'MAD',
  status          booking_status NOT NULL DEFAULT 'pending',
  payment_status  payment_status NOT NULL DEFAULT 'pending',
  created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX idx_bookings_user   ON bookings(user_id);
CREATE INDEX idx_bookings_status ON bookings(status);

-- ─── RSS Items ────────────────────────────────────────────────────────────────
CREATE TABLE rss_items (
  id           SERIAL PRIMARY KEY,
  title        VARCHAR(300) NOT NULL,
  link         VARCHAR(500),
  description  TEXT,
  category     rss_category DEFAULT 'news',
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

CREATE TRIGGER trg_programs_upd BEFORE UPDATE ON travel_programs
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_bookings_upd BEFORE UPDATE ON bookings
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_posts_upd BEFORE UPDATE ON blog_posts
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();
