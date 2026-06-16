-- RT Voyage - Seed Data (CORRIGÉ - colonnes alignées avec le schéma réel)
SET client_encoding = 'UTF8';

-- ─── Nettoyage complet avant injection ────────────────────────────────────────
TRUNCATE TABLE
  destination_activities, program_destinations, program_days,
  testimonials, bookings, post_tags, blog_posts, blog_tags, blog_categories,
  shop_orders, shop_products, shop_categories,
  flight_promotions, promotions, rss_items,
  faq_items, faq_categories,
  newsletter_subscribers, contact_messages,
  medias, hotels, activities, activity_categories,
  travel_programs, destinations, countries, airlines, users
RESTART IDENTITY CASCADE;

-- ─── Countries ────────────────────────────────────────────────────────────────
INSERT INTO countries (name_fr,name_en,code,continent,capital,currency,currency_code,language,flag_emoji) VALUES
('Maroc','Morocco','MA','Afrique','Rabat','Dirham marocain','MAD','Arabe / Français','🇲🇦'),
('France','France','FR','Europe','Paris','Euro','EUR','Français','🇫🇷'),
('Espagne','Spain','ES','Europe','Madrid','Euro','EUR','Espagnol','🇪🇸'),
('Portugal','Portugal','PT','Europe','Lisbonne','Euro','EUR','Portugais','🇵🇹'),
('Italie','Italy','IT','Europe','Rome','Euro','EUR','Italien','🇮🇹'),
('Turquie','Turkey','TR','Eurasie','Ankara','Livre turque','TRY','Turc','🇹🇷'),
('Grèce','Greece','GR','Europe','Athènes','Euro','EUR','Grec','🇬🇷'),
('Émirats arabes unis','UAE','AE','Asie','Abu Dhabi','Dirham émirati','AED','Arabe','🇦🇪'),
('Thaïlande','Thailand','TH','Asie','Bangkok','Baht','THB','Thaï','🇹🇭'),
('Japon','Japan','JP','Asie','Tokyo','Yen','JPY','Japonais','🇯🇵'),
('Indonésie','Indonesia','ID','Asie','Jakarta','Roupie indonésienne','IDR','Indonésien','🇮🇩'),
('Vietnam','Vietnam','VN','Asie','Hanoï','Dong','VND','Vietnamien','🇻🇳'),
('Brésil','Brazil','BR','Amérique du Sud','Brasília','Real brésilien','BRL','Portugais','🇧🇷'),
('Mexique','Mexico','MX','Amérique du Nord','Mexico','Peso mexicain','MXN','Espagnol','🇲🇽'),
('États-Unis','USA','US','Amérique du Nord','Washington D.C.','Dollar américain','USD','Anglais','🇺🇸'),
('Canada','Canada','CA','Amérique du Nord','Ottawa','Dollar canadien','CAD','Français / Anglais','🇨🇦'),
('Jordanie','Jordan','JO','Asie','Amman','Dinar jordanien','JOD','Arabe','🇯🇴'),
('Maldives','Maldives','MV','Asie','Malé','Rufiyaa','MVR','Maldivien','🇲🇻'),
('Sénégal','Senegal','SN','Afrique','Dakar','Franc CFA','XOF','Français','🇸🇳'),
('Tanzanie','Tanzania','TZ','Afrique','Dodoma','Shilling tanzanien','TZS','Swahili','🇹🇿'),
('Pérou','Peru','PE','Amérique du Sud','Lima','Sol','PEN','Espagnol','🇵🇪'),
('Islande','Iceland','IS','Europe','Reykjavik','Couronne islandaise','ISK','Islandais','🇮🇸'),
('Australie','Australia','AU','Océanie','Canberra','Dollar australien','AUD','Anglais','🇦🇺');

-- ─── Destinations - Maroc (villes) ────────────────────────────────────────────
INSERT INTO destinations (slug,name_fr,name_en,short_desc_fr,short_desc_en,country_id,destination_type,latitude,longitude,is_featured,is_active,average_budget_eur,safety_level,best_period_fr) VALUES
('marrakech','Marrakech','Marrakech','La Ville Rouge, capitale du tourisme marocain aux mille couleurs.','The Red City, Morocco''s tourism capital with a thousand colors.',(SELECT id FROM countries WHERE code='MA'),'city',31.6295,-7.9811,TRUE,TRUE,2800,'high','Mars-Juin, Sept-Nov'),
('casablanca','Casablanca','Casablanca','La métropole économique du Maroc, entre modernité et traditions.','Morocco''s economic metropolis, between modernity and tradition.',(SELECT id FROM countries WHERE code='MA'),'city',33.5731,-7.5898,TRUE,TRUE,2200,'high','Toute l''année'),
('rabat','Rabat','Rabat','Capitale du Royaume, ville royale au charme discret et raffiné.','Capital of the Kingdom, a royal city with discreet and refined charm.',(SELECT id FROM countries WHERE code='MA'),'city',34.0209,-6.8416,FALSE,TRUE,1800,'high','Toute l''année'),
('fes','Fès','Fes','Capitale spirituelle du Maroc, la médina la plus authentique du monde.','Morocco''s spiritual capital, the world''s most authentic medina.',(SELECT id FROM countries WHERE code='MA'),'city',34.0181,-5.0078,TRUE,TRUE,2500,'high','Mars-Mai, Sept-Nov'),
('meknes','Meknès','Meknes','La ville des sultans, joyau impérial à l''architecture somptueuse.','The city of sultans, an imperial jewel with sumptuous architecture.',(SELECT id FROM countries WHERE code='MA'),'city',33.8935,-5.5473,FALSE,TRUE,1600,'high','Avril-Oct'),
('tanger','Tanger','Tangier','La porte de l''Afrique, carrefour de cultures au détroit de Gibraltar.','The gateway to Africa, a crossroads of cultures at the Strait of Gibraltar.',(SELECT id FROM countries WHERE code='MA'),'city',35.7595,-5.8340,FALSE,TRUE,2000,'high','Avr-Oct'),
('chefchaouen','Chefchaouen','Chefchaouen','La perle bleue du Rif, un village de rêve tout en nuances d''azur.','The blue pearl of the Rif, a dreamy village in shades of azure.',(SELECT id FROM countries WHERE code='MA'),'city',35.1688,-5.2636,TRUE,TRUE,1800,'high','Avr-Jun, Sept-Oct'),
('agadir','Agadir','Agadir','Ville balnéaire ensoleillée avec 300 jours de soleil par an.','Sunny seaside city with 300 days of sunshine per year.',(SELECT id FROM countries WHERE code='MA'),'beach',30.4278,-9.5981,TRUE,TRUE,3200,'high','Toute l''année'),
('essaouira','Essaouira','Essaouira','La ville des vents, cité d''art et de culture sur l''Atlantique.','The city of winds, an art and culture city on the Atlantic.',(SELECT id FROM countries WHERE code='MA'),'city',31.5085,-9.7595,FALSE,TRUE,1600,'high','Avr-Juin, Oct-Nov'),
('ouarzazate','Ouarzazate','Ouarzazate','La porte du désert et capitale mondiale du cinéma africain.','The gateway to the desert and world capital of African cinema.',(SELECT id FROM countries WHERE code='MA'),'city',30.9335,-6.8936,TRUE,TRUE,2200,'high','Oct-Avr'),
('merzouga','Merzouga','Merzouga','Les majestueuses dunes de l''Erg Chebbi, porte du Sahara.','The majestic dunes of Erg Chebbi, gateway to the Sahara.',(SELECT id FROM countries WHERE code='MA'),'desert',31.0996,-3.9785,TRUE,TRUE,3500,'high','Oct-Avr'),
('dakhla','Dakhla','Dakhla','Lagon paradisiaque et capitale mondiale du kitesurf.','Paradise lagoon and world capital of kitesurfing.',(SELECT id FROM countries WHERE code='MA'),'beach',23.7141,-15.9355,FALSE,TRUE,4500,'medium','Toute l''année'),
('ifrane','Ifrane','Ifrane','La petite Suisse du Maroc, station de montagne enneigée.','Morocco''s little Switzerland, a snow-covered mountain resort.',(SELECT id FROM countries WHERE code='MA'),'mountain',33.5228,-5.1058,FALSE,TRUE,2000,'high','Dec-Fév (ski), Été'),
('al-hoceima','Al Hoceima','Al Hoceima','Perle de la Méditerranée marocaine aux eaux cristallines.','Pearl of the Moroccan Mediterranean with crystal-clear waters.',(SELECT id FROM countries WHERE code='MA'),'beach',35.2517,-3.9372,FALSE,TRUE,2200,'high','Juin-Sept'),
('sale','Salé','Sale','Ville jumelle de Rabat, patrimoine andalou et traditions vivantes.','Rabat''s twin city, Andalusian heritage and living traditions.',(SELECT id FROM countries WHERE code='MA'),'city',34.0365,-6.8131,FALSE,TRUE,1400,'high','Avr-Oct');

-- ─── Destinations - Maroc (nature) ─────────────────────────────────────────────
INSERT INTO destinations (slug,name_fr,name_en,short_desc_fr,short_desc_en,country_id,destination_type,latitude,longitude,is_featured,is_active,average_budget_eur,safety_level,best_period_fr) VALUES
('sahara-erg-chebbi','Sahara - Erg Chebbi','Sahara - Erg Chebbi','Les plus belles dunes du Sahara marocain, un coucher de soleil inoubliable.','The most beautiful dunes of the Moroccan Sahara, an unforgettable sunset.',(SELECT id FROM countries WHERE code='MA'),'desert',31.1300,-4.0100,TRUE,TRUE,4000,'high','Oct-Avr'),
('haut-atlas','Haut Atlas','High Atlas','Les sommets enneigés du Toubkal dominant le paysage berbère.','Toubkal''s snow-capped peaks dominating the Berber landscape.',(SELECT id FROM countries WHERE code='MA'),'mountain',31.0594,-7.9139,TRUE,TRUE,3000,'high','Avr-Juin, Sept-Nov'),
('vallee-ziz','Vallée du Ziz','Ziz Valley','Une oasis de palmeraies serpentant dans un canyon rouge.','A palm grove oasis winding through a red canyon.',(SELECT id FROM countries WHERE code='MA'),'city',31.5665,-4.3555,FALSE,TRUE,2000,'high','Oct-Avr'),
('gorges-todra','Gorges du Todra','Todra Gorges','Falaises vertigineuses de 300 m, paradis des grimpeurs.','Vertigo-inducing 300m cliffs, a climber''s paradise.',(SELECT id FROM countries WHERE code='MA'),'city',31.5950,-5.5850,FALSE,TRUE,1800,'high','Mars-Nov'),
('gorges-dades','Gorges du Dadès','Dades Gorges','Le spectaculaire canyon aux courbes sinueuses et villages en pisé.','The spectacular canyon with winding curves and mud-brick villages.',(SELECT id FROM countries WHERE code='MA'),'city',31.4856,-6.0147,FALSE,TRUE,1800,'high','Avr-Oct'),
('vallee-ourika','Vallée de l''Ourika','Ourika Valley','Cascade, ruisseaux et verdure à 30 km de Marrakech.','Waterfalls, streams and greenery 30 km from Marrakech.',(SELECT id FROM countries WHERE code='MA'),'city',31.2931,-7.6456,FALSE,TRUE,1200,'high','Avr-Oct'),
('moyen-atlas','Moyen Atlas','Middle Atlas','Forêts de cèdres millénaires et lacs aux eaux turquoise.','Millennial cedar forests and turquoise lakes.',(SELECT id FROM countries WHERE code='MA'),'mountain',33.3500,-5.0000,FALSE,TRUE,1500,'high','Avr-Oct'),
('vallee-draa','Vallée du Drâa','Draa Valley','La plus longue oasis d''Afrique, des palmeraies à perte de vue.','Africa''s longest oasis, palm groves as far as the eye can see.',(SELECT id FROM countries WHERE code='MA'),'city',30.2000,-5.9000,FALSE,TRUE,2200,'high','Oct-Avr');

-- ─── Destinations - Europe ─────────────────────────────────────────────────────
INSERT INTO destinations (slug,name_fr,name_en,short_desc_fr,short_desc_en,country_id,destination_type,latitude,longitude,is_featured,is_active,average_budget_eur,safety_level,best_period_fr) VALUES
('paris','Paris','Paris','La Ville Lumière, capitale mondiale de l''art, de la mode et de la gastronomie.','The City of Light, world capital of art, fashion and gastronomy.',(SELECT id FROM countries WHERE code='FR'),'city',48.8566,2.3522,TRUE,TRUE,8000,'high','Avr-Jun, Sept-Oct'),
('nice','Nice','Nice','Perle de la Côte d''Azur, baie des Anges et vieille ville colorée.','Pearl of the Côte d''Azur, Bay of Angels and colorful old town.',(SELECT id FROM countries WHERE code='FR'),'beach',43.7102,7.2620,FALSE,TRUE,7000,'high','Juin-Sept'),
('barcelone','Barcelone','Barcelona','Gaudí, plages et gastronomie dans la capitale catalane.','Gaudí, beaches and gastronomy in the Catalan capital.',(SELECT id FROM countries WHERE code='ES'),'city',41.3851,2.1734,TRUE,TRUE,7500,'high','Avr-Jun, Sept-Oct'),
('madrid','Madrid','Madrid','Capitale ibérique, musées de classe mondiale et vie nocturne légendaire.','Iberian capital, world-class museums and legendary nightlife.',(SELECT id FROM countries WHERE code='ES'),'city',40.4168,-3.7038,FALSE,TRUE,6500,'high','Avr-Jun, Sept-Oct'),
('seville','Séville','Seville','Flamenco, orangers en fleurs et l''Alcázar andalou.','Flamenco, orange blossoms and the Andalusian Alcázar.',(SELECT id FROM countries WHERE code='ES'),'city',37.3886,-5.9823,FALSE,TRUE,5800,'high','Mars-Mai, Oct'),
('lisbonne','Lisbonne','Lisbon','Tram 28, pastéis de nata et fado dans les ruelles d''Alfama.','Tram 28, pastéis de nata and fado in the Alfama alleys.',(SELECT id FROM countries WHERE code='PT'),'city',38.7223,-9.1393,TRUE,TRUE,6000,'high','Avr-Jun, Sept-Oct'),
('porto','Porto','Porto','Vins de Porto, azulejos et la Ribeira au fil du Douro.','Port wines, azulejos and the Ribeira along the Douro.',(SELECT id FROM countries WHERE code='PT'),'city',41.1579,-8.6291,FALSE,TRUE,5500,'high','Avr-Oct'),
('rome','Rome','Rome','La Ville Éternelle, Colisée, Vatican et dolce vita.','The Eternal City, Colosseum, Vatican and dolce vita.',(SELECT id FROM countries WHERE code='IT'),'city',41.9028,12.4964,TRUE,TRUE,8000,'high','Avr-Jun, Sept-Oct'),
('venise','Venise','Venice','La cité des Doges, gondoles et palais sur la lagune.','The city of the Doges, gondolas and palaces on the lagoon.',(SELECT id FROM countries WHERE code='IT'),'city',45.4408,12.3155,TRUE,TRUE,9000,'high','Avr-Jun, Sept-Oct'),
('florence','Florence','Florence','Berceau de la Renaissance, Uffizi et David de Michel-Ange.','Cradle of the Renaissance, Uffizi and Michelangelo''s David.',(SELECT id FROM countries WHERE code='IT'),'city',43.7696,11.2558,FALSE,TRUE,7000,'high','Avr-Jun, Sept-Oct'),
('amsterdam','Amsterdam','Amsterdam','Canaux, vélos, musées et la maison d''Anne Frank.','Canals, bikes, museums and Anne Frank''s house.',(SELECT id FROM countries WHERE code='FR'),'city',52.3676,4.9041,FALSE,TRUE,9000,'high','Avr-Sept'),
('prague','Prague','Prague','La ville aux cent clochers, joyau gothique et baroque.','The city of a hundred spires, a Gothic and Baroque gem.',(SELECT id FROM countries WHERE code='FR'),'city',50.0755,14.4378,FALSE,TRUE,5500,'high','Avr-Jun, Sept-Oct'),
('santorini','Santorin','Santorini','Falaises blanches et dômes bleus suspendus sur la mer Égée.','White cliffs and blue domes suspended above the Aegean Sea.',(SELECT id FROM countries WHERE code='GR'),'beach',36.3932,25.4615,TRUE,TRUE,11000,'high','Juin-Sept'),
('athenes','Athènes','Athens','Le berceau de la démocratie, Parthénon et Acropole.','The cradle of democracy, Parthenon and Acropolis.',(SELECT id FROM countries WHERE code='GR'),'city',37.9838,23.7275,FALSE,TRUE,6500,'high','Avr-Jun, Sept-Oct'),
('istanbul','Istanbul','Istanbul','Le carrefour de deux continents, minarets et bosphore.','The crossroads of two continents, minarets and the Bosphorus.',(SELECT id FROM countries WHERE code='TR'),'city',41.0082,28.9784,TRUE,TRUE,6000,'high','Avr-Jun, Sept-Oct'),
('cappadoce','Cappadoce','Cappadocia','Cheminées de fées et montgolfières au lever du soleil.','Fairy chimneys and hot air balloons at sunrise.',(SELECT id FROM countries WHERE code='TR'),'city',38.6431,34.8289,TRUE,TRUE,7500,'high','Avr-Jun, Sept-Nov'),
('reykjavik','Reykjavik','Reykjavik','Aurores boréales, geysers et sources chaudes en Islande.','Northern lights, geysers and hot springs in Iceland.',(SELECT id FROM countries WHERE code='IS'),'city',64.1355,-21.8954,FALSE,TRUE,18000,'high','Déc-Mars (aurores), Juin-Août');

-- ─── Destinations - Moyen-Orient & Golfe ──────────────────────────────────────
INSERT INTO destinations (slug,name_fr,name_en,short_desc_fr,short_desc_en,country_id,destination_type,latitude,longitude,is_featured,is_active,average_budget_eur,safety_level,best_period_fr) VALUES
('dubai','Dubaï','Dubai','Gratte-ciel vertigineux, désert doré et luxe absolu.','Vertiginous skyscrapers, golden desert and absolute luxury.',(SELECT id FROM countries WHERE code='AE'),'city',25.2048,55.2708,TRUE,TRUE,15000,'high','Nov-Mars'),
('abu-dhabi','Abu Dhabi','Abu Dhabi','Mosquée Sheikh Zayed et Louvre Abu Dhabi dans la capitale des Émirats.','Sheikh Zayed Mosque and Louvre Abu Dhabi in the Emirates capital.',(SELECT id FROM countries WHERE code='AE'),'city',24.4539,54.3773,FALSE,TRUE,13000,'high','Nov-Mars'),
('petra','Petra','Petra','La cité rose taillée dans la roche, huitième merveille du monde.','The rose-red city carved in rock, eighth wonder of the world.',(SELECT id FROM countries WHERE code='JO'),'historical',30.3285,35.4444,TRUE,TRUE,9000,'medium','Mars-Avr, Oct-Nov');

-- ─── Destinations - Asie ──────────────────────────────────────────────────────
INSERT INTO destinations (slug,name_fr,name_en,short_desc_fr,short_desc_en,country_id,destination_type,latitude,longitude,is_featured,is_active,average_budget_eur,safety_level,best_period_fr) VALUES
('bangkok','Bangkok','Bangkok','Temples bouddhistes, marchés flottants et street food légendaire.','Buddhist temples, floating markets and legendary street food.',(SELECT id FROM countries WHERE code='TH'),'city',13.7563,100.5018,TRUE,TRUE,7000,'medium','Nov-Fév'),
('phuket','Phuket','Phuket','Plages de sable blanc, mer d''émeraude et vie nocturne animée.','White sand beaches, emerald sea and vibrant nightlife.',(SELECT id FROM countries WHERE code='TH'),'beach',7.8804,98.3923,FALSE,TRUE,6500,'medium','Nov-Avr'),
('chiang-mai','Chiang Mai','Chiang Mai','La rose du Nord, temples dorés et sanctuaires d''éléphants.','The Rose of the North, golden temples and elephant sanctuaries.',(SELECT id FROM countries WHERE code='TH'),'city',18.7883,98.9853,FALSE,TRUE,5500,'medium','Nov-Fév'),
('tokyo','Tokyo','Tokyo','Néons, sushis, temples shintoïstes et cerisiers en fleurs.','Neon lights, sushi, Shinto temples and cherry blossoms.',(SELECT id FROM countries WHERE code='JP'),'city',35.6762,139.6503,TRUE,TRUE,18000,'high','Mars-Mai, Oct-Nov'),
('kyoto','Kyoto','Kyoto','Géishas, temples Zen et jardins millénaires dans l''ancienne capitale.','Geishas, Zen temples and ancient gardens in the former capital.',(SELECT id FROM countries WHERE code='JP'),'city',35.0116,135.7681,TRUE,TRUE,16000,'high','Mars-Mai, Oct-Nov'),
('osaka','Osaka','Osaka','Château historique, Dotonbori illuminé et gastronomie fusion.','Historic castle, illuminated Dotonbori and fusion gastronomy.',(SELECT id FROM countries WHERE code='JP'),'city',34.6937,135.5023,FALSE,TRUE,14000,'high','Avr-Jun, Oct-Nov'),
('bali','Bali','Bali','Île des dieux, rizières en terrasse, temples et surf.','Island of the gods, terraced rice fields, temples and surfing.',(SELECT id FROM countries WHERE code='ID'),'beach',-8.3405,115.0920,TRUE,TRUE,7000,'medium','Mai-Oct'),
('ubud','Ubud','Ubud','Cœur spirituel de Bali, yoga, jungle et arts traditionnels.','Bali''s spiritual heart, yoga, jungle and traditional arts.',(SELECT id FROM countries WHERE code='ID'),'city',-8.5069,115.2625,FALSE,TRUE,6000,'medium','Mai-Oct'),
('hanoi','Hanoï','Hanoi','Vieille ville coloniale, lacs mythiques et phở authentique.','Colonial old town, mythical lakes and authentic phở.',(SELECT id FROM countries WHERE code='VN'),'city',21.0285,105.8542,TRUE,TRUE,5500,'medium','Oct-Avr'),
('ho-chi-minh','Hô Chi Minh-Ville','Ho Chi Minh City','L''énergie de Saigon, histoire et modernité en fusion.','The energy of Saigon, history and modernity in fusion.',(SELECT id FROM countries WHERE code='VN'),'city',10.8231,106.6297,FALSE,TRUE,5000,'medium','Nov-Avr'),
('halong-bay','Baie d''Halong','Ha Long Bay','Karsts calcaires et jonques traditionnelles sur une mer d''émeraude.','Limestone karsts and traditional junks on an emerald sea.',(SELECT id FROM countries WHERE code='VN'),'city',20.9101,107.1839,TRUE,TRUE,7500,'medium','Oct-Avr'),
('maldives','Maldives','Maldives','Overwater bungalows, récifs de corail et lagons turquoise infinis.','Overwater bungalows, coral reefs and infinite turquoise lagoons.',(SELECT id FROM countries WHERE code='MV'),'beach',3.2028,73.2207,TRUE,TRUE,35000,'high','Nov-Avr');

-- ─── Destinations - Amériques ─────────────────────────────────────────────────
INSERT INTO destinations (slug,name_fr,name_en,short_desc_fr,short_desc_en,country_id,destination_type,latitude,longitude,is_featured,is_active,average_budget_eur,safety_level,best_period_fr) VALUES
('new-york','New York','New York','La ville qui ne dort jamais, Broadway et la skyline mythique.','The city that never sleeps, Broadway and the iconic skyline.',(SELECT id FROM countries WHERE code='US'),'city',40.7128,-74.0060,TRUE,TRUE,20000,'medium','Avr-Jun, Sept-Nov'),
('miami','Miami','Miami','Plages de South Beach, Art Deco et vie nocturne latine.','South Beach beaches, Art Deco and Latin nightlife.',(SELECT id FROM countries WHERE code='US'),'beach',25.7617,-80.1918,FALSE,TRUE,16000,'medium','Nov-Avr'),
('san-francisco','San Francisco','San Francisco','Golden Gate, Alcatraz et la culture hippie de la Californie.','Golden Gate, Alcatraz and California''s hippie culture.',(SELECT id FROM countries WHERE code='US'),'city',37.7749,-122.4194,FALSE,TRUE,18000,'medium','Sept-Nov'),
('montreal','Montréal','Montreal','Ville francophone, jazz et bagels au cœur du Québec.','Francophone city, jazz and bagels in the heart of Quebec.',(SELECT id FROM countries WHERE code='CA'),'city',45.5017,-73.5673,FALSE,TRUE,14000,'high','Juin-Oct'),
('cancun','Cancún','Cancun','Plages de sable blanc et sites mayas sur la Riviera Maya.','White sand beaches and Mayan sites on the Riviera Maya.',(SELECT id FROM countries WHERE code='MX'),'beach',21.1619,-86.8515,TRUE,TRUE,12000,'medium','Nov-Avr'),
('rio','Rio de Janeiro','Rio de Janeiro','Carnaval, Christ Rédempteur et Copacabana au pied du Sugarloaf.','Carnival, Christ the Redeemer and Copacabana at Sugar Loaf''s foot.',(SELECT id FROM countries WHERE code='BR'),'city',-22.9068,-43.1729,TRUE,TRUE,13000,'low','Déc-Mars'),
('buenos-aires','Buenos Aires','Buenos Aires','Tango, bœuf argentin et quartiers européens en Amérique du Sud.','Tango, Argentine beef and European neighborhoods in South America.',(SELECT id FROM countries WHERE code='BR'),'city',-34.6118,-58.4173,FALSE,TRUE,11000,'medium','Oct-Avr'),
('cuzco','Cusco','Cusco','Ancienne capitale inca et porte du Machu Picchu.','Ancient Inca capital and gateway to Machu Picchu.',(SELECT id FROM countries WHERE code='PE'),'historical',-13.5319,-71.9675,TRUE,TRUE,14000,'medium','Avr-Oct'),
('machu-picchu','Machu Picchu','Machu Picchu','La cité perdue des Incas suspendue dans les nuages andins.','The lost city of the Incas suspended in the Andean clouds.',(SELECT id FROM countries WHERE code='PE'),'historical',-13.1631,-72.5450,TRUE,TRUE,16000,'medium','Avr-Oct');

-- ─── Destinations - Afrique ───────────────────────────────────────────────────
INSERT INTO destinations (slug,name_fr,name_en,short_desc_fr,short_desc_en,country_id,destination_type,latitude,longitude,is_featured,is_active,average_budget_eur,safety_level,best_period_fr) VALUES
('dakar','Dakar','Dakar','Île de Gorée, musique djembé et hospitalité teranga du Sénégal.','Gorée Island, djembe music and Senegal''s teranga hospitality.',(SELECT id FROM countries WHERE code='SN'),'city',14.7167,-17.4677,FALSE,TRUE,9000,'medium','Nov-Mai'),
('serengeti','Serengeti','Serengeti','La grande migration, lions, éléphants et savane infinie.','The great migration, lions, elephants and endless savanna.',(SELECT id FROM countries WHERE code='TZ'),'city',-2.3333,34.8333,TRUE,TRUE,28000,'medium','Juin-Oct'),
('zanzibar','Zanzibar','Zanzibar','Île aux épices, plages de corail blanc et architecture arabe.','Spice island, white coral beaches and Arab architecture.',(SELECT id FROM countries WHERE code='TZ'),'beach',-6.1659,39.2026,FALSE,TRUE,18000,'medium','Juin-Oct'),
('sydney','Sydney','Sydney','Opéra, Bondi Beach et le Grand Récif de Corail à portée.','Opera House, Bondi Beach and the Great Barrier Reef within reach.',(SELECT id FROM countries WHERE code='AU'),'city',-33.8688,151.2093,FALSE,TRUE,22000,'high','Oct-Avr');

-- ─── Activity categories ───────────────────────────────────────────────────────
INSERT INTO activity_categories (slug,name_fr,name_en,icon) VALUES
('culture-histoire','Culture & Histoire','Culture & History','fa-landmark'),
('sport-aventure','Sport & Aventure','Sport & Adventure','fa-mountain'),
('gastronomie','Gastronomie','Gastronomy','fa-utensils'),
('bien-etre','Bien-être & Spa','Wellness & Spa','fa-spa'),
('nature','Nature & Faune','Nature & Wildlife','fa-leaf'),
('sport-football','Football Experience','Football Experience','fa-futbol'),
('nautique','Sports Nautiques','Water Sports','fa-water'),
('famille','Famille','Family','fa-child');

-- ─── Sample Activities (duration_hours et price_per_person) ───────────────────
INSERT INTO activities (slug,name_fr,name_en,description_fr,category_id,activity_type,duration_hours,price_per_person) VALUES
('djemaa-el-fna','Place Jemaa El-Fna','Jemaa El-Fna Square','La place mythique au cœur de Marrakech, spectacles de rue et souks.',(SELECT id FROM activity_categories WHERE slug='culture-histoire'),'medina',2,0),
('medina-fes','Médina de Fès','Fes Medina','La plus grande médina médiévale du monde, inscrite à l''UNESCO.',(SELECT id FROM activity_categories WHERE slug='culture-histoire'),'medina',4,0),
('trekking-toubkal','Ascension du Toubkal','Toubkal Trek','4167 m, le plus haut sommet d''Afrique du Nord.',(SELECT id FROM activity_categories WHERE slug='sport-aventure'),'hike',48,800),
('surf-taghazout','Surf à Taghazout','Surf Taghazout','Spot de surf légendaire près d''Agadir.',(SELECT id FROM activity_categories WHERE slug='nautique'),'surf',3,350),
('quad-sahara','Quad dans les dunes','Quad in the dunes','Aventure en quad à travers les dunes de l''Erg Chebbi.',(SELECT id FROM activity_categories WHERE slug='sport-aventure'),'desert',2,400),
('bivouac-desert','Bivouac sous les étoiles','Desert Bivouac','Nuit en camp berbère au milieu du Sahara.',(SELECT id FROM activity_categories WHERE slug='nature'),'desert',12,600),
('visite-bernabeu','Tour du Bernabéu','Bernabéu Tour','Visite officielle du stade du Real Madrid.',(SELECT id FROM activity_categories WHERE slug='sport-football'),'stadium',2,350),
('visite-camp-nou','Tour du Camp Nou','Camp Nou Tour','Visite du plus grand stade d''Europe, musée FC Barcelona.',(SELECT id FROM activity_categories WHERE slug='sport-football'),'stadium',2,300),
('cours-cuisine-marrakech','Cours de cuisine marocaine','Moroccan Cooking Class','Apprenez à préparer le tajine et le couscous traditionnels.',(SELECT id FROM activity_categories WHERE slug='gastronomie'),'cultural',3,450),
('hammam-traditionnel','Hammam traditionnel','Traditional Hammam','Soin authentique dans un hammam marocain historique.',(SELECT id FROM activity_categories WHERE slug='bien-etre'),'luxury',2,200),
('montgolfiere-cappadoce','Montgolfière en Cappadoce','Hot Air Balloon Cappadocia','Vol au lever du soleil au-dessus des cheminées de fées.',(SELECT id FROM activity_categories WHERE slug='sport-aventure'),'excursion',2,900),
('safari-serengeti','Safari en 4×4','4WD Safari','Safari guidé au lever du soleil dans la savane du Serengeti.',(SELECT id FROM activity_categories WHERE slug='nature'),'excursion',8,3500),
('plongee-maldives','Plongée aux Maldives','Maldives Diving','Exploration des récifs coralliens et requins baleines.',(SELECT id FROM activity_categories WHERE slug='nautique'),'nautical',4,800),
('colisee-rome','Visite du Colisée','Colosseum Visit','Visite guidée du Colisée et du Forum Romain.',(SELECT id FROM activity_categories WHERE slug='culture-histoire'),'monument',3,450),
('tour-eiffel','Tour Eiffel','Eiffel Tower','Montée au sommet de la dame de fer, vue panoramique sur Paris.',(SELECT id FROM activity_categories WHERE slug='culture-histoire'),'monument',2,280);

-- Link activities to destinations (sans sort_order)
INSERT INTO destination_activities (destination_id, activity_id)
SELECT d.id, a.id FROM destinations d, activities a WHERE d.slug='marrakech' AND a.slug='djemaa-el-fna';
INSERT INTO destination_activities (destination_id, activity_id)
SELECT d.id, a.id FROM destinations d, activities a WHERE d.slug='marrakech' AND a.slug='cours-cuisine-marrakech';
INSERT INTO destination_activities (destination_id, activity_id)
SELECT d.id, a.id FROM destinations d, activities a WHERE d.slug='marrakech' AND a.slug='hammam-traditionnel';
INSERT INTO destination_activities (destination_id, activity_id)
SELECT d.id, a.id FROM destinations d, activities a WHERE d.slug='fes' AND a.slug='medina-fes';
INSERT INTO destination_activities (destination_id, activity_id)
SELECT d.id, a.id FROM destinations d, activities a WHERE d.slug='merzouga' AND a.slug='bivouac-desert';
INSERT INTO destination_activities (destination_id, activity_id)
SELECT d.id, a.id FROM destinations d, activities a WHERE d.slug='merzouga' AND a.slug='quad-sahara';
INSERT INTO destination_activities (destination_id, activity_id)
SELECT d.id, a.id FROM destinations d, activities a WHERE d.slug='haut-atlas' AND a.slug='trekking-toubkal';
INSERT INTO destination_activities (destination_id, activity_id)
SELECT d.id, a.id FROM destinations d, activities a WHERE d.slug='agadir' AND a.slug='surf-taghazout';
INSERT INTO destination_activities (destination_id, activity_id)
SELECT d.id, a.id FROM destinations d, activities a WHERE d.slug='madrid' AND a.slug='visite-bernabeu';
INSERT INTO destination_activities (destination_id, activity_id)
SELECT d.id, a.id FROM destinations d, activities a WHERE d.slug='barcelone' AND a.slug='visite-camp-nou';
INSERT INTO destination_activities (destination_id, activity_id)
SELECT d.id, a.id FROM destinations d, activities a WHERE d.slug='cappadoce' AND a.slug='montgolfiere-cappadoce';
INSERT INTO destination_activities (destination_id, activity_id)
SELECT d.id, a.id FROM destinations d, activities a WHERE d.slug='serengeti' AND a.slug='safari-serengeti';
INSERT INTO destination_activities (destination_id, activity_id)
SELECT d.id, a.id FROM destinations d, activities a WHERE d.slug='maldives' AND a.slug='plongee-maldives';
INSERT INTO destination_activities (destination_id, activity_id)
SELECT d.id, a.id FROM destinations d, activities a WHERE d.slug='rome' AND a.slug='colisee-rome';
INSERT INTO destination_activities (destination_id, activity_id)
SELECT d.id, a.id FROM destinations d, activities a WHERE d.slug='paris' AND a.slug='tour-eiffel';

-- ─── Airlines ─────────────────────────────────────────────────────────────────
INSERT INTO airlines (slug,name,iata_code,website,alliance,baggage_cabin_kg,baggage_hold_kg,has_business_class,has_first_class,is_partner) VALUES
('royal-air-maroc','Royal Air Maroc','AT','https://royalairmaroc.com',NULL,8,23,TRUE,FALSE,TRUE),
('air-france','Air France','AF','https://airfrance.fr','SkyTeam',12,23,TRUE,TRUE,TRUE),
('emirates','Emirates','EK','https://emirates.com',NULL,7,30,TRUE,TRUE,FALSE),
('qatar-airways','Qatar Airways','QR','https://qatarairways.com','OneWorld',7,30,TRUE,TRUE,FALSE),
('turkish-airlines','Turkish Airlines','TK','https://turkishairlines.com','Star Alliance',8,23,TRUE,FALSE,FALSE),
('ryanair','Ryanair','FR','https://ryanair.com',NULL,10,20,FALSE,FALSE,FALSE),
('easyjet','easyJet','U2','https://easyjet.com',NULL,15,23,FALSE,FALSE,FALSE),
('transavia','Transavia','TO','https://transavia.com',NULL,10,20,FALSE,FALSE,TRUE);

INSERT INTO flight_promotions (airline_id,title_fr,title_en,origin_iata,destination_iata,price_from,currency,valid_from,valid_until,is_active) VALUES
((SELECT id FROM airlines WHERE iata_code='AT'),'Casablanca → Paris dès 1299 MAD','Casablanca → Paris from 1299 MAD','CMN','CDG',1299,'MAD','2026-07-01','2026-09-30',TRUE),
((SELECT id FROM airlines WHERE iata_code='AT'),'Casablanca → Barcelone dès 990 MAD','Casablanca → Barcelona from 990 MAD','CMN','BCN',990,'MAD','2026-06-01','2026-08-31',TRUE),
((SELECT id FROM airlines WHERE iata_code='TO'),'Casablanca → Paris dès 799 MAD','Casablanca → Paris from 799 MAD','CMN','ORY',799,'MAD','2026-07-01','2026-10-31',TRUE),
((SELECT id FROM airlines WHERE iata_code='AF'),'Casablanca → Paris dès 1450 MAD','Casablanca → Paris from 1450 MAD','CMN','CDG',1450,'MAD','2026-07-01','2026-09-30',TRUE),
((SELECT id FROM airlines WHERE iata_code='FR'),'Marrakech → Bristol dès 390 MAD','Marrakech → Bristol from 390 MAD','RAK','BRS',390,'MAD','2026-08-01','2026-10-31',TRUE);

-- ─── Hotels (description_fr et price_min) ─────────────────────────────────────
INSERT INTO hotels (slug,name,hotel_type,stars,destination_id,description_fr,price_min,has_pool,has_spa,has_restaurant,has_wifi,is_partner,is_featured,is_active) VALUES
('la-mamounia-marrakech','La Mamounia','hotel',5,(SELECT id FROM destinations WHERE slug='marrakech'),'Palais légendaire classé parmi les meilleurs hôtels du monde.',3500,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE),
('royal-mansour-marrakech','Royal Mansour','riad',5,(SELECT id FROM destinations WHERE slug='marrakech'),'Riad palais signé par le Roi Mohammed VI, l''ultime luxe.',9000,TRUE,TRUE,TRUE,TRUE,FALSE,TRUE,TRUE),
('sofitel-casablanca','Sofitel Casablanca Tour Blanche','hotel',5,(SELECT id FROM destinations WHERE slug='casablanca'),'Vue panoramique sur la ville et l''Atlantique.',2800,TRUE,TRUE,TRUE,TRUE,TRUE,FALSE,TRUE),
('hotel-palais-fes','Palais Faraj Fès','riad',5,(SELECT id FROM destinations WHERE slug='fes'),'Vue époustouflante sur la médina de Fès depuis la terrasse.',2200,FALSE,TRUE,TRUE,TRUE,FALSE,FALSE,TRUE),
('riad-chefchaouen','Riad Assilah','riad',4,(SELECT id FROM destinations WHERE slug='chefchaouen'),'Riad authentique dans les ruelles bleues de Chefchaouen.',800,FALSE,FALSE,TRUE,TRUE,FALSE,FALSE,TRUE),
('kasbah-tamadot-atlas','Kasbah Tamadot','villa',5,(SELECT id FROM destinations WHERE slug='haut-atlas'),'Propriété de Virgin Galactic de Richard Branson dans l''Atlas.',5500,TRUE,TRUE,TRUE,TRUE,FALSE,TRUE,TRUE),
('le-meridien-dubai','Le Méridien Dubaï','hotel',5,(SELECT id FROM destinations WHERE slug='dubai'),'Hôtel de luxe avec vue sur la marina de Dubaï.',4500,TRUE,TRUE,TRUE,TRUE,FALSE,FALSE,TRUE),
('four-seasons-bali','Four Seasons Bali','resort',5,(SELECT id FROM destinations WHERE slug='bali'),'Resort en terrasse de riz avec villas à piscine privée.',7000,TRUE,TRUE,TRUE,TRUE,FALSE,TRUE,TRUE),
('hotel-particulier-paris','Hôtel du Particulier','hotel',5,(SELECT id FROM destinations WHERE slug='paris'),'Boutique-hôtel discret au cœur de Montmartre.',6500,FALSE,FALSE,TRUE,TRUE,FALSE,FALSE,TRUE),
('grand-hotel-maldives','Grand Park Kodhipparu','resort',5,(SELECT id FROM destinations WHERE slug='maldives'),'Villas sur pilotis au-dessus du lagon, plongée au pied du lit.',18000,TRUE,TRUE,TRUE,TRUE,FALSE,TRUE,TRUE);

-- ─── Travel Programs (tagline_fr/en et price_per_person_discounted) ───────────
INSERT INTO travel_programs (slug,name_fr,name_en,tagline_fr,tagline_en,theme,duration_days,duration_nights,group_min,group_max,price_per_person,price_per_person_discounted,departure_city,is_featured,is_active) VALUES
('circuit-imperial-maroc','Circuit des Villes Impériales','Imperial Cities Circuit','Marrakech, Fès, Meknès et Rabat en 8 jours, un voyage dans le temps.','Marrakech, Fes, Meknes and Rabat in 8 days, a journey through time.','culture',8,7,2,20,8500,7200,'Casablanca',TRUE,TRUE),
('sahara-aventure','Sahara Aventure','Sahara Adventure','Des gorges du Dadès aux dunes de Merzouga, l''aventure du Grand Sud.','From Dades Gorges to Merzouga dunes, the Great South adventure.','adventure',5,4,2,12,5500,4800,'Marrakech',TRUE,TRUE),
('football-espagne','Football Experience - Espagne','Football Experience Spain','Bernabéu + Camp Nou + matches, le rêve de tout fan de football.','Bernabéu + Camp Nou + matches, every football fan''s dream.','football',7,6,2,16,14500,12900,'Casablanca',TRUE,TRUE),
('bali-spirituel','Bali Spirituelle','Spiritual Bali','Yoga, temples et rizières pour un voyage de ressourcement profond.','Yoga, temples and rice fields for a deep rejuvenating journey.','nature',10,9,1,10,22000,19500,'Casablanca',TRUE,TRUE),
('tokyo-kyoto-culture','Japon - Tokyo & Kyoto','Japan - Tokyo & Kyoto','Tradition et modernité dans l''archipel nippon, 12 jours de pur émerveillement.','Tradition and modernity in the Japanese archipelago, 12 days of wonder.','culture',12,11,2,14,32000,28500,'Paris',TRUE,TRUE),
('maldives-luxe','Maldives Lune de Miel','Maldives Honeymoon','Villas sur pilotis, plongée et couchers de soleil de rêve.','Overwater villas, diving and dream sunsets.','luxury',7,6,2,2,55000,48000,'Casablanca',FALSE,TRUE),
('cappadoce-istanbul','Turquie - Istanbul & Cappadoce','Turkey - Istanbul & Cappadocia','Minarets, marchés aux épices et montgolfières en 8 jours.','Minarets, spice markets and hot air balloons in 8 days.','culture',8,7,2,18,11500,9800,'Casablanca',FALSE,TRUE),
('aventure-atlas','Trek Toubkal - Haut Atlas','Toubkal Trek - High Atlas','Ascension du plus haut sommet d''Afrique du Nord (4167 m).','Summit of North Africa''s highest peak (4167 m).','adventure',5,4,4,12,4500,3900,'Marrakech',FALSE,TRUE),
('safari-tanzanie','Safari Tanzanie - Serengeti & Zanzibar','Tanzania Safari - Serengeti & Zanzibar','Grande migration + farniente sur les plages corallines de Zanzibar.','Great migration + relaxation on Zanzibar''s coral beaches.','adventure',12,11,2,10,42000,38000,'Casablanca',FALSE,TRUE),
('gastronomie-italie','Gastronomie - Italie','Gastronomy Italy','Rome, Florence, Venise : arts, pâtes et chianti.','Rome, Florence, Venice: arts, pasta and Chianti.','gastronomy',9,8,2,16,14000,12500,'Casablanca',FALSE,TRUE);

-- Link programs to destinations (sans sort_order)
INSERT INTO program_destinations (program_id, destination_id)
SELECT p.id, d.id FROM travel_programs p, destinations d WHERE p.slug='circuit-imperial-maroc' AND d.slug='marrakech';
INSERT INTO program_destinations (program_id, destination_id)
SELECT p.id, d.id FROM travel_programs p, destinations d WHERE p.slug='circuit-imperial-maroc' AND d.slug='meknes';
INSERT INTO program_destinations (program_id, destination_id)
SELECT p.id, d.id FROM travel_programs p, destinations d WHERE p.slug='circuit-imperial-maroc' AND d.slug='fes';
INSERT INTO program_destinations (program_id, destination_id)
SELECT p.id, d.id FROM travel_programs p, destinations d WHERE p.slug='circuit-imperial-maroc' AND d.slug='rabat';
INSERT INTO program_destinations (program_id, destination_id)
SELECT p.id, d.id FROM travel_programs p, destinations d WHERE p.slug='sahara-aventure' AND d.slug='ouarzazate';
INSERT INTO program_destinations (program_id, destination_id)
SELECT p.id, d.id FROM travel_programs p, destinations d WHERE p.slug='sahara-aventure' AND d.slug='gorges-dades';
INSERT INTO program_destinations (program_id, destination_id)
SELECT p.id, d.id FROM travel_programs p, destinations d WHERE p.slug='sahara-aventure' AND d.slug='merzouga';
INSERT INTO program_destinations (program_id, destination_id)
SELECT p.id, d.id FROM travel_programs p, destinations d WHERE p.slug='football-espagne' AND d.slug='madrid';
INSERT INTO program_destinations (program_id, destination_id)
SELECT p.id, d.id FROM travel_programs p, destinations d WHERE p.slug='football-espagne' AND d.slug='barcelone';
INSERT INTO program_destinations (program_id, destination_id)
SELECT p.id, d.id FROM travel_programs p, destinations d WHERE p.slug='tokyo-kyoto-culture' AND d.slug='tokyo';
INSERT INTO program_destinations (program_id, destination_id)
SELECT p.id, d.id FROM travel_programs p, destinations d WHERE p.slug='tokyo-kyoto-culture' AND d.slug='kyoto';
INSERT INTO program_destinations (program_id, destination_id)
SELECT p.id, d.id FROM travel_programs p, destinations d WHERE p.slug='tokyo-kyoto-culture' AND d.slug='osaka';
INSERT INTO program_destinations (program_id, destination_id)
SELECT p.id, d.id FROM travel_programs p, destinations d WHERE p.slug='gastronomie-italie' AND d.slug='rome';
INSERT INTO program_destinations (program_id, destination_id)
SELECT p.id, d.id FROM travel_programs p, destinations d WHERE p.slug='gastronomie-italie' AND d.slug='florence';
INSERT INTO program_destinations (program_id, destination_id)
SELECT p.id, d.id FROM travel_programs p, destinations d WHERE p.slug='gastronomie-italie' AND d.slug='venise';

-- Program days (Circuit Impérial)
INSERT INTO program_days (program_id,day_number,title_fr,morning_fr,afternoon_fr,evening_fr,accommodation,meals_included) VALUES
((SELECT id FROM travel_programs WHERE slug='circuit-imperial-maroc'),1,'Casablanca → Marrakech','Accueil à l''aéroport Mohammed V, transfert en minibus','Visite de la Mosquée Hassan II, la 3ème plus grande du monde','Dîner de bienvenue au restaurant panoramique de l''hôtel','La Mamounia Marrakech','LD'),
((SELECT id FROM travel_programs WHERE slug='circuit-imperial-maroc'),2,'Marrakech','Visite de la Médina : souks, Ben Youssef, Mouassine','Palais Bahia, Mellah et Jemaa El-Fna','Spectacle de danse et dîner marocain traditionnel','La Mamounia Marrakech','BLD'),
((SELECT id FROM travel_programs WHERE slug='circuit-imperial-maroc'),3,'Marrakech → Fès via Meknès','Route panoramique via Aïn Leuh, pause déjeuner à Meknès','Visite de Meknès : Bab Mansour, Mausolée Moulay Ismaïl','Arrivée à Fès, dîner en riad','Palais Faraj Fès','BLD'),
((SELECT id FROM travel_programs WHERE slug='circuit-imperial-maroc'),4,'Fès','Médina UNESCO : Tanneries Chouara, Medersa Bou Inania','Quartier Al-Andalus, fondouk des marchands, épices','Dîner gastronomique fassi : pastilla, harira','Palais Faraj Fès','BLD'),
((SELECT id FROM travel_programs WHERE slug='circuit-imperial-maroc'),5,'Fès → Rabat','Départ pour Rabat via Meknès','Visite de Rabat : Tour Hassan, Mausolée Mohammed V, Kasbah Oudayas','Soirée libre à Rabat','Hôtel Sofitel Rabat','BLD');

-- Program days (Sahara Aventure)
INSERT INTO program_days (program_id,day_number,title_fr,morning_fr,afternoon_fr,evening_fr,accommodation,meals_included) VALUES
((SELECT id FROM travel_programs WHERE slug='sahara-aventure'),1,'Marrakech → Ouarzazate','Départ de Marrakech, traversée du col de Tichka (2260 m)','Arrivée à Ouarzazate, visite des studios de cinéma Atlas','Dîner et nuit au riad','Riad Salam Ouarzazate','LD'),
((SELECT id FROM travel_programs WHERE slug='sahara-aventure'),2,'Ouarzazate → Gorges du Dadès','Route des Kasbahs : Aït Benhaddou (UNESCO)','Gorges du Dadès, balcon de la rose, vallée des roses','Nuit dans un gîte de montagne','Gîte Gorges du Dadès','BLD'),
((SELECT id FROM travel_programs WHERE slug='sahara-aventure'),3,'Dadès → Todra → Merzouga','Gorges du Todra, escalade libre pour les aventuriers','Route du désert vers Merzouga via Erfoud et fossiles','Arrivée à Merzouga, montée à dos de chameau','Camp berbère Erg Chebbi','BLD'),
((SELECT id FROM travel_programs WHERE slug='sahara-aventure'),4,'Sahara','Lever de soleil depuis la crête des dunes','Quad dans les dunes, visite d''un village nomade','Nuit sous les étoiles, astronomie, musique touareg','Camp berbère Erg Chebbi','BLD'),
((SELECT id FROM travel_programs WHERE slug='sahara-aventure'),5,'Merzouga → Casablanca','Petit-déjeuner au camp, retour en 4×4','Vol de retour ou route Casablanca','-','-','B');

-- ─── Testimonials ─────────────────────────────────────────────────────────────
INSERT INTO testimonials (destination_id,client_name,client_country,rating,comment,travel_date,is_approved,is_featured) VALUES
((SELECT id FROM destinations WHERE slug='marrakech'),'Sophie Martin','France',5,'Un voyage magique ! Les souks, les riads, la gastronomie… Marrakech nous a envoûtés. L''équipe RT Voyage a tout organisé à la perfection.','2025-03-15',TRUE,TRUE),
((SELECT id FROM destinations WHERE slug='merzouga'),'Carlos García','Espagne',5,'Le bivouac sous les étoiles du Sahara est une expérience unique. Je n''aurais jamais imaginé vivre ça un jour. MERCI RT Voyage !','2025-02-20',TRUE,TRUE),
((SELECT id FROM destinations WHERE slug='chefchaouen'),'Emma Wilson','Royaume-Uni',5,'Chefchaouen est une ville de rêve. Chaque ruelle est une photo. Organisation impeccable, guide fantastique.','2025-04-10',TRUE,TRUE),
((SELECT id FROM destinations WHERE slug='bali'),'Yuki Tanaka','Japon',5,'Bali était tout simplement parfaite. Les temples, les rizières d''Ubud, le spa du Four Seasons… un paradis.','2025-01-25',TRUE,TRUE),
((SELECT id FROM destinations WHERE slug='tokyo'),'Julie Dupont','France',5,'Tokyo m''a laissée sans voix. L''organisation de RT Voyage était parfaite, avec des guides locaux passionnants.','2024-11-08',TRUE,TRUE),
((SELECT id FROM destinations WHERE slug='dubai'),'Ahmed Al-Rashid','Émirats arabes unis',4,'Fantastique séjour à Dubaï. Le Burj Khalifa, le désert, les souks dorés. Je recommande vivement.','2025-03-01',TRUE,TRUE),
((SELECT id FROM destinations WHERE slug='paris'),'Maria Santos','Brésil',5,'Paris a dépassé toutes mes attentes ! La gastronomie, le Louvre, Montmartre… RT Voyage a pensé à tout.','2025-05-12',TRUE,TRUE),
((SELECT id FROM destinations WHERE slug='santorini'),'Lars Andersen','Danemark',5,'Santorin au coucher du soleil depuis Oia… aucun mot ne peut décrire cette beauté. Voyage parfait !','2025-06-05',TRUE,FALSE),
((SELECT id FROM destinations WHERE slug='maldives'),'Priya Sharma','Inde',5,'Notre lune de miel aux Maldives était absolument magique. La villa sur l''eau, le lagon turquoise… inoubliable.','2025-04-28',TRUE,TRUE),
((SELECT id FROM destinations WHERE slug='marrakech'),'Oliver Schmidt','Allemagne',4,'Très bon circuit, guide très compétent. La Mamounia est somptueuse. Je reviendrai au Maroc !','2025-05-02',TRUE,FALSE);

-- ─── Blog Categories & Posts ───────────────────────────────────────────────────
INSERT INTO blog_categories (slug,name_fr,name_en,icon) VALUES
('voyage','Voyage','Travel','fa-suitcase'),
('conseils','Conseils','Tips','fa-lightbulb'),
('culture','Culture','Culture','fa-theater-masks'),
('gastronomie','Gastronomie','Gastronomy','fa-utensils'),
('actualites','Actualités','News','fa-newspaper'),
('promotions','Promotions','Deals','fa-tag');

INSERT INTO blog_tags (name,slug) VALUES
('Maroc','maroc'),('Sahara','sahara'),('Riad','riad'),('Médina','medina'),
('Europe','europe'),('Asie','asie'),('Luxury','luxury'),('Adventure','adventure'),
('Family','family'),('Budget','budget'),('Football','football'),('Gastronomie','gastronomie');

INSERT INTO blog_posts (slug,title_fr,title_en,excerpt_fr,excerpt_en,content_fr,category_id,is_published,is_featured,view_count,published_at) VALUES
('top-10-medinas-maroc','Top 10 des médinas à visiter au Maroc','Top 10 medinas to visit in Morocco',
'De Marrakech à Fès en passant par Chefchaouen, découvrez les médinas les plus fascinantes du Maroc.','From Marrakech to Fes via Chefchaouen, discover Morocco''s most fascinating medinas.',
'<p>Le Maroc possède certaines des médinas les plus authentiques et préservées du monde entier.</p>',
(SELECT id FROM blog_categories WHERE slug='voyage'),TRUE,TRUE,1247,'2025-05-15'),

('guide-sahara-marocain','Guide complet : voyager dans le Sahara marocain','Complete guide: travelling in the Moroccan Sahara',
'Tout ce qu''il faut savoir pour préparer votre aventure dans le désert marocain.','Everything you need to know to prepare your Moroccan desert adventure.',
'<p>Le Sahara marocain est l''une des expériences les plus inoubliables qu''un voyageur puisse vivre.</p>',
(SELECT id FROM blog_categories WHERE slug='conseils'),TRUE,FALSE,834,'2025-04-22'),

('experience-football-espagne','Football Experience : Bernabéu et Camp Nou en 7 jours','Football Experience: Bernabéu and Camp Nou in 7 days',
'Notre programme Football Experience Espagne vous emmène dans les temples du football mondial.','Our Football Experience Spain program takes you to the world''s football temples.',
'<p>Pour tout fan de football, visiter le Bernabéu et le Camp Nou est un rêve absolu.</p>',
(SELECT id FROM blog_categories WHERE slug='voyage'),TRUE,TRUE,2156,'2025-06-01'),

('gastronomie-marocaine-secrets','Les secrets de la gastronomie marocaine','The secrets of Moroccan gastronomy',
'Tajine, couscous, pastilla, harira… plongez au cœur des saveurs et épices marocaines.','Tagine, couscous, pastilla, harira... dive into the flavors and spices of Moroccan cuisine.',
'<p>La cuisine marocaine est l''une des plus riches et complexes du monde.</p>',
(SELECT id FROM blog_categories WHERE slug='gastronomie'),TRUE,FALSE,567,'2025-05-28');

-- ─── FAQ ──────────────────────────────────────────────────────────────────────
INSERT INTO faq_categories (slug,name_fr,name_en,"order") VALUES
('reservation','Réservation & Paiement','Booking & Payment',1),
('voyage','Voyages & Programmes','Travel & Programs',2),
('pratique','Informations Pratiques','Practical Information',3),
('annulation','Annulation & Remboursement','Cancellation & Refunds',4);

INSERT INTO faq_items (category_id,question_fr,question_en,answer_fr,answer_en,"order",is_active) VALUES
((SELECT id FROM faq_categories WHERE slug='reservation'),'Comment réserver un voyage avec RT Voyage ?','How do I book a trip with RT Voyage?','Vous pouvez réserver directement sur notre site ou nous contacter par téléphone au +212 5 22 XX XX XX. Un acompte de 30% est demandé à la réservation.','You can book directly on our website or contact us by phone. A 30% deposit is required at booking.',1,TRUE),
((SELECT id FROM faq_categories WHERE slug='reservation'),'Quels modes de paiement acceptez-vous ?','What payment methods do you accept?','Nous acceptons les virements bancaires, les cartes bancaires (Visa, Mastercard) et les espèces en agence.','We accept bank transfers, credit cards (Visa, Mastercard) and cash at our agency.',2,TRUE),
((SELECT id FROM faq_categories WHERE slug='voyage'),'Les programmes incluent-ils les vols ?','Do the programs include flights?','Nos prix affichés n''incluent généralement pas les vols internationaux. Nous proposons cependant les meilleures offres de nos compagnies partenaires.','Our displayed prices generally do not include international flights. We can offer the best deals from our partner airlines.',1,TRUE),
((SELECT id FROM faq_categories WHERE slug='pratique'),'Ai-je besoin d''un visa pour voyager au Maroc ?','Do I need a visa to travel to Morocco?','Les ressortissants de nombreux pays (France, Espagne, Canada, USA, UE...) peuvent entrer au Maroc sans visa pour moins de 90 jours.','Citizens of many countries (France, Spain, Canada, USA, EU...) can enter Morocco without a visa for under 90 days.',1,TRUE),
((SELECT id FROM faq_categories WHERE slug='annulation'),'Quelle est votre politique d''annulation ?','What is your cancellation policy?','Annulation plus de 60 jours avant : remboursement moins 10%. Entre 30 et 60 jours : 50% retenu. Moins de 30 jours : aucun remboursement.','Cancellation more than 60 days before: refund minus 10%. 30-60 days: 50% retained. Less than 30 days: no refund.',1,TRUE),
((SELECT id FROM faq_categories WHERE slug='pratique'),'Proposez-vous des voyages sur mesure ?','Do you offer tailor-made trips?','Absolument ! Notre équipe conçoit des voyages entièrement personnalisés selon vos envies, budget et disponibilités.','Absolutely! Our team designs fully customized trips based on your wishes, budget and availability.',2,TRUE);

-- ─── Promotions ───────────────────────────────────────────────────────────────
INSERT INTO promotions (slug,title_fr,title_en,description_fr,promo_type,destination_id,promo_price,original_price,discount_percent,valid_from,valid_until,is_active) VALUES
('promo-marrakech-ete-2026','Offre Été Marrakech 2026','Summer Marrakech 2026','3 nuits à Marrakech en riad 4★ + petit-déjeuner + visite guidée médina.','hotel',(SELECT id FROM destinations WHERE slug='marrakech'),2200,3100,29,'2026-06-01','2026-08-31',TRUE),
('promo-sahara-octobre','Sahara en Octobre - Prix Spécial','Sahara October Special','Circuit 5 jours Marrakech-Sahara-Marrakech, tout inclus.','package',(SELECT id FROM destinations WHERE slug='merzouga'),4800,5500,13,'2026-09-15','2026-10-31',TRUE),
('promo-dubai-hiver','Dubaï Hiver 2026 - Vol + Hôtel','Dubai Winter 2026 - Flight + Hotel','7 nuits à Dubaï en hôtel 5★ + vols RAM depuis Casablanca.','package',(SELECT id FROM destinations WHERE slug='dubai'),13500,18000,25,'2026-11-01','2027-01-31',TRUE);

-- ─── RSS Items ────────────────────────────────────────────────────────────────
INSERT INTO rss_items (title,link,description,category,published_at) VALUES
('Nouvelle destination : Dakhla, capital du kitesurf','/destinations/dakhla','RT Voyage lance un programme exclusif à Dakhla, le paradis des sports nautiques.','destination','2026-06-10 09:00:00'),
('Promo Été : -29% sur les séjours Marrakech','/promotions','Profitez de notre offre exclusive pour l''été 2026 à Marrakech.','promotion','2026-06-08 08:00:00'),
('Football Experience Espagne - Bernabéu + Camp Nou','/programmes/football-espagne','Notre programme football en Espagne est disponible pour la saison 2025-2026.','article','2026-06-05 10:00:00'),
('Nouveau partenariat : Royal Air Maroc Premium','/airlines/royal-air-maroc','RT Voyage renforce son partenariat avec RAM pour des tarifs préférentiels.','partner','2026-06-01 11:00:00'),
('Guide pratique : voyager au Maroc en été','/blog/guide-sahara-marocain','Conseils, bons plans et astuces pour profiter du Maroc même en période estivale.','article','2026-05-28 09:30:00'),
('Ouverture des réservations Sahara hiver 2026','/programmes/sahara-aventure','Les réservations pour le circuit Sahara Aventure sont ouvertes pour la haute saison.','news','2026-05-20 08:00:00');

-- ─── Admin user (mot de passe : Admin@2025!) ──────────────────────────────────
INSERT INTO users (username,email,password_hash,first_name,last_name,role,is_active) VALUES
('admin','admin@rtvoyage.ma','scrypt:32768:8:1$8EqfVf6GJIfLbzlJ$b42796145775f562dd91608312094e00f32df9942141d51a6851cbb11229e3933b5e7d4f75f789dbd593599c478a2cd0519e4f9a5a670759440d08be612b73eb','Rachid','Tanostrong','super_admin',TRUE);

-- ─── Shop ─────────────────────────────────────────────────────────────────────
INSERT INTO shop_categories (slug,name_fr,name_en,icon) VALUES
('bagages','Bagages & Valises','Luggage & Bags','fa-suitcase'),
('accessoires','Accessoires Voyage','Travel Accessories','fa-plug'),
('guides','Guides & Livres','Guides & Books','fa-book'),
('trekking','Équipement Trekking','Trekking Equipment','fa-mountain'),
('souvenirs','Souvenirs Maroc','Morocco Souvenirs','fa-gift');

INSERT INTO shop_products (slug,name_fr,name_en,description_fr,category_id,price,price_discounted,stock,is_affiliate,is_active) VALUES
('valise-cabine-premium','Valise Cabine Premium 55cm','Premium Cabin Suitcase 55cm','Valise cabine polycarbonate légère (2.5 kg), TSA, 4 roues 360°.',(SELECT id FROM shop_categories WHERE slug='bagages'),890,720,-1,TRUE,TRUE),
('sac-dos-trek-45l','Sac à dos Trek 45L','Trekking Backpack 45L','Sac de randonnée imperméable avec structure dorsale ventilée.',(SELECT id FROM shop_categories WHERE slug='trekking'),650,NULL,50,FALSE,TRUE),
('guide-maroc-lonely-planet','Guide du Maroc - Lonely Planet','Morocco Guide - Lonely Planet','Édition 2025, toutes les destinations, cartes détaillées.',(SELECT id FROM shop_categories WHERE slug='guides'),180,150,100,FALSE,TRUE),
('tajine-decoratif','Tajine décoratif peint','Decorative Painted Tagine','Tajine en céramique peinte à la main, artisanat marocain authentique.',(SELECT id FROM shop_categories WHERE slug='souvenirs'),350,NULL,30,FALSE,TRUE),
('adaptateur-universel','Adaptateur universel de voyage','Universal Travel Adapter','Compatible 150+ pays, 4 ports USB + 1 USB-C, compact.',(SELECT id FROM shop_categories WHERE slug='accessoires'),280,220,-1,TRUE,TRUE);

ANALYZE;
