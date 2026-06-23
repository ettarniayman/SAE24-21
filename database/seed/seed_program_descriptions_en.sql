-- English descriptions, includes/excludes for the 10 travel programs
-- Run after seed.sql and seed_program_descriptions.sql

UPDATE travel_programs SET
  description_en = 'Embark on an 8-day journey through Morocco''s four imperial cities: red Marrakech, spiritual Fez, historic Meknes and the capital Rabat. This cultural trip immerses you in UNESCO-listed medinas, royal palaces and age-old souks, accompanied by an English-speaking guide throughout the journey.',
  includes_en = E'Air-conditioned transport with driver\nCertified English-speaking guide\nAccommodation in riads and 4* hotels\nDaily breakfasts\nGuided medina tours\nEntrance fees to historic monuments',
  excludes_en = E'International flights\nLunches and dinners (unless stated)\nTips and personal expenses\nTravel insurance'
WHERE slug='circuit-imperial-maroc';

UPDATE travel_programs SET
  description_en = 'Five intense days between the spectacular Dades Gorges and the golden dunes of Merzouga. Camp under the stars in the Sahara desert, ride camels at sunset, and meet Berber nomads. A total immersion into Morocco''s Deep South, designed for lovers of wide open spaces and authentic adventure.',
  includes_en = E'4x4 with driver-guide\nDesert bivouac night (Berber tents)\nNights in hotels and kasbahs\nFull board during the trek\nCamel ride\nTraditional Berber music evening',
  excludes_en = E'International flights\nAlcoholic beverages\nTips\nCancellation insurance'
WHERE slug='sahara-aventure';

UPDATE travel_programs SET
  description_en = 'The dream of every football fan: 7 days in Spain with access to the legendary Santiago Bernabéu and Camp Nou stadiums, La Liga match tickets subject to the calendar, and visits to both clubs'' museums. Between Madrid and Barcelona, this programme combines footballing passion with discovering the country''s two greatest cities.',
  includes_en = E'Internal Madrid-Barcelona flights\n4* hotel accommodation\nMatch tickets subject to calendar\nGuided tour of Bernabéu and Camp Nou\nAirport and stadium transfers\nBreakfasts included',
  excludes_en = E'International flights\nMeals other than breakfast\nMerchandise and souvenirs\nTravel insurance'
WHERE slug='football-espagne';

UPDATE travel_programs SET
  description_en = 'Ten days to reconnect with the essentials: morning yoga sessions facing Ubud''s terraced rice fields, visits to centuries-old Balinese temples, and moments of deep relaxation amid lush nature and Hindu spirituality. A trip designed to slow down, breathe and reconnect with yourself, far from everyday hustle.',
  includes_en = E'Accommodation in villas and eco-lodges\nDaily yoga classes\nLocal spiritual guide\nTemple visits (Tirta Empul, Besakih)\nVegetarian meals included\nGuided meditation session',
  excludes_en = E'International flights\nOptional spa treatments\nDrinks other than meals\nTips'
WHERE slug='bali-spirituel';

UPDATE travel_programs SET
  description_en = 'Twelve days of pure wonder between tradition and modernity at the heart of the Japanese archipelago. From the electric buzz of Tokyo to the zen temples of Kyoto, via Mount Fuji, this cultural tour offers a striking contrast between futuristic skyscrapers, Shinto shrines and centuries-old Japanese gardens.',
  includes_en = E'Bullet train (Shinkansen) journeys\nEnglish-speaking guide\nAccommodation in ryokans and hotels\nTemple and shrine visits\nTea ceremony experience\nDaily breakfasts',
  excludes_en = E'International flights\nLunches and dinners\nUrban transport pass\nTravel insurance'
WHERE slug='tokyo-kyoto-culture';

UPDATE travel_programs SET
  description_en = 'Seven exceptional days in a paradisiacal setting to celebrate your honeymoon: a private overwater villa with direct access to the turquoise lagoon, diving sessions among coral reefs, and unforgettable sunsets. The ideal all-inclusive romantic getaway in the Maldives archipelago.',
  includes_en = E'Overwater villa with private pool\nFull board\nOne snorkelling/diving outing included\nSeaplane transfer\nRomantic dinner on the beach\nSpa: one welcome treatment',
  excludes_en = E'International flights\nAdditional water activities\nPremium beverages\nTips'
WHERE slug='maldives-luxe';

UPDATE travel_programs SET
  description_en = 'Eight days between the minarets of Istanbul and the fairy chimneys of Cappadocia. Wander through the Grand Bazaar, admire Hagia Sophia and the Blue Mosque, then take off at sunrise aboard a hot air balloon over Cappadocia''s lunar landscapes. A cultural tour rich in contrasts between East and modernity.',
  includes_en = E'Internal Istanbul-Cappadocia flight\nEnglish-speaking guide\nAccommodation in cave hotels and 4* hotels\nSunrise hot air balloon flight\nGuided tours (Hagia Sophia, Topkapi)\nDaily breakfasts',
  excludes_en = E'International flights\nLunches and dinners\nTips for guides and drivers\nTravel insurance'
WHERE slug='cappadoce-istanbul';

UPDATE travel_programs SET
  description_en = 'Five days to climb Mount Toubkal, the highest peak in North Africa at 4,167 metres. This trek, led by experienced Berber mountain guides, crosses authentic villages of the High Atlas, with nights in mountain refuges. A demanding yet accessible adventure, rewarded with breathtaking panoramic views from the summit.',
  includes_en = E'Certified Berber mountain guide\nMule for luggage transport\nNights in refuges and gîtes\nFull board during the trek\nSafety equipment (crampons in winter)\nTransfers from Marrakech',
  excludes_en = E'International flights\nPersonal trekking equipment\nTips for guides and muleteers\nMountain insurance'
WHERE slug='aventure-atlas';

UPDATE travel_programs SET
  description_en = 'Twelve days combining safari and relaxation: observe the wildebeest Great Migration in the Serengeti aboard open-top 4x4 vehicles with an experienced ranger, then unwind on the coral beaches of Zanzibar. A complete programme combining the magic of the Tanzanian savannah with the gentle pace of life on the Indian Ocean.',
  includes_en = E'Safari 4x4 with ranger guide\nAccommodation in lodges and beach hotels\nFull board during the safari\nNational park entrance fees\nInternal Serengeti-Zanzibar flight\nOne excursion to Prison Island',
  excludes_en = E'International flights\nAlcoholic beverages\nOptional water activities in Zanzibar\nTips'
WHERE slug='safari-tanzanie';

UPDATE travel_programs SET
  description_en = 'Nine days for food and art lovers across Rome, Florence and Venice. Taste the finest fresh pasta, visit the vineyards of Chianti, and let yourself be carried away by Renaissance masterpieces. Cooking workshops with local chefs and wine tastings punctuate this cultural and culinary journey through Italy.',
  includes_en = E'High-speed trains between cities\nEnglish-speaking guide\n4* hotel accommodation\nTwo Italian cooking workshops\nWine tasting in Chianti\nBreakfasts and 3 traditional dinners',
  excludes_en = E'International flights\nLunches (except workshops)\nMuseum entries not mentioned\nTips'
WHERE slug='gastronomie-italie';
