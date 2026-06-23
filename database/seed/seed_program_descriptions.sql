-- Descriptions, inclus/non-inclus pour les 10 programmes de voyage (travel_programs)
-- A executer apres seed.sql

UPDATE travel_programs SET
  description_fr = 'Embarquez pour un circuit de 8 jours à travers les quatre villes impériales du Maroc : Marrakech la rouge, Fès la spirituelle, Meknès l''historique et Rabat la capitale. Ce voyage culturel vous plonge dans les médinas classées à l''UNESCO, les palais royaux et les souks ancestraux, accompagné d''un guide francophone tout au long du parcours.',
  includes_fr = E'Transport climatisé avec chauffeur\nGuide francophone certifié\nHébergement en riads et hôtels 4*\nPetits-déjeuners quotidiens\nVisites guidées des médinas\nEntrées aux monuments historiques',
  excludes_fr = E'Vols internationaux\nDéjeuners et dîners (sauf mention)\nPourboires et dépenses personnelles\nAssurance voyage'
WHERE slug='circuit-imperial-maroc';

UPDATE travel_programs SET
  description_fr = 'Cinq jours intenses entre les gorges spectaculaires du Dadès et les dunes dorées de Merzouga. Bivouac sous les étoiles dans le désert du Sahara, balade à dos de dromadaire au coucher du soleil, et rencontre avec les nomades berbères. Une immersion totale dans le Grand Sud marocain, pensée pour les amateurs de grands espaces et d''aventure authentique.',
  includes_fr = E'4x4 avec chauffeur-guide\nNuit en bivouac désert (tentes berbères)\nNuits en hôtels et kasbahs\nPension complète pendant le trek\nBalade à dos de dromadaire\nMusique et soirée traditionnelle berbère',
  excludes_fr = E'Vols internationaux\nBoissons alcoolisées\nPourboires\nAssurance annulation'
WHERE slug='sahara-aventure';

UPDATE travel_programs SET
  description_fr = 'Le rêve de tout passionné de football : 7 jours en Espagne avec accès aux stades mythiques du Santiago Bernabéu et du Camp Nou, billets pour des matchs de Liga selon le calendrier, et visite des musées des clubs. Entre Madrid et Barcelone, ce programme combine ferveur sportive et découverte des deux plus grandes villes du pays.',
  includes_fr = E'Vols internes Madrid-Barcelone\nHébergement en hôtels 4*\nBillets de match selon calendrier\nVisite guidée Bernabéu et Camp Nou\nTransferts aéroport et stades\nPetits-déjeuners inclus',
  excludes_fr = E'Vols internationaux\nRepas hors petit-déjeuner\nMerchandising et souvenirs\nAssurance voyage'
WHERE slug='football-espagne';

UPDATE travel_programs SET
  description_fr = 'Dix jours pour se reconnecter à l''essentiel : séances de yoga matinales face aux rizières en terrasses d''Ubud, visites de temples balinais millénaires, et moments de pur ressourcement entre nature luxuriante et spiritualité hindouiste. Un voyage pensé pour ralentir, respirer et se retrouver, loin de l''agitation du quotidien.',
  includes_fr = E'Hébergement en villas et éco-lodges\nCours de yoga quotidiens\nGuide spirituel local\nVisites de temples (Tirta Empul, Besakih)\nRepas végétariens inclus\nSéance de méditation guidée',
  excludes_fr = E'Vols internationaux\nSoins spa optionnels\nBoissons hors repas\nPourboires'
WHERE slug='bali-spirituel';

UPDATE travel_programs SET
  description_fr = 'Douze jours de pur émerveillement entre tradition et modernité au cœur de l''archipel nippon. De la frénésie électrique de Tokyo aux temples zen de Kyoto en passant par le Mont Fuji, ce circuit culturel offre un contraste saisissant entre gratte-ciels futuristes, sanctuaires shintoïstes et jardins japonais séculaires.',
  includes_fr = E'Trajets en train à grande vitesse (Shinkansen)\nGuide francophone\nHébergement en ryokans et hôtels\nVisites de temples et sanctuaires\nExpérience cérémonie du thé\nPetits-déjeuners quotidiens',
  excludes_fr = E'Vols internationaux\nDéjeuners et dîners\nPass transport urbain\nAssurance voyage'
WHERE slug='tokyo-kyoto-culture';

UPDATE travel_programs SET
  description_fr = 'Sept jours d''exception dans un cadre paradisiaque pour célébrer votre lune de miel : villa privée sur pilotis avec accès direct au lagon turquoise, séances de plongée parmi les récifs coralliens, et couchers de soleil inoubliables. Le programme idéal pour un séjour romantique tout compris dans l''archipel des Maldives.',
  includes_fr = E'Villa sur pilotis avec piscine privée\nPension complète\nUne sortie snorkeling/plongée incluse\nTransfert en hydravion\nDîner romantique sur la plage\nSpa : un soin de bienvenue',
  excludes_fr = E'Vols internationaux\nActivités nautiques additionnelles\nBoissons premium\nPourboires'
WHERE slug='maldives-luxe';

UPDATE travel_programs SET
  description_fr = 'Huit jours entre les minarets d''Istanbul et les cheminées de fées de Cappadoce. Flânez dans le Grand Bazar, admirez Sainte-Sophie et la Mosquée Bleue, puis envolez-vous au lever du soleil à bord d''une montgolfière au-dessus des paysages lunaires de Cappadoce. Un circuit culturel riche en contrastes entre Orient et modernité.',
  includes_fr = E'Vol intérieur Istanbul-Cappadoce\nGuide francophone\nHébergement en hôtels-troglodytes et hôtels 4*\nVol en montgolfière au lever du soleil\nVisites guidées (Sainte-Sophie, Topkapi)\nPetits-déjeuners quotidiens',
  excludes_fr = E'Vols internationaux\nDéjeuners et dîners\nPourboires guides et chauffeurs\nAssurance voyage'
WHERE slug='cappadoce-istanbul';

UPDATE travel_programs SET
  description_fr = 'Cinq jours pour gravir le Toubkal, point culminant de l''Afrique du Nord à 4167 mètres d''altitude. Ce trek encadré par des guides berbères expérimentés traverse les villages authentiques du Haut Atlas, avec nuits en refuge de montagne. Une aventure exigeante mais accessible, récompensée par un panorama à couper le souffle au sommet.',
  includes_fr = E'Guide de montagne berbère certifié\nMulet pour le portage des bagages\nNuits en refuges et gîtes\nPension complète durant le trek\nÉquipement de sécurité (crampons en hiver)\nTransferts depuis Marrakech',
  excludes_fr = E'Vols internationaux\nÉquipement personnel de trek\nPourboires guides et muletiers\nAssurance montagne'
WHERE slug='aventure-atlas';

UPDATE travel_programs SET
  description_fr = 'Douze jours entre safari et farniente : observez la Grande Migration des gnous dans le Serengeti au cœur de 4x4 ouverts avec un ranger expérimenté, puis détendez-vous sur les plages coralliennes de Zanzibar. Un programme complet qui combine la magie de la savane tanzanienne et la douceur de vivre de l''océan Indien.',
  includes_fr = E'4x4 de safari avec ranger guide\nHébergement en lodges et hôtels balnéaires\nPension complète durant le safari\nEntrées parcs nationaux\nVol intérieur Serengeti-Zanzibar\nUne excursion île de Prison Island',
  excludes_fr = E'Vols internationaux\nBoissons alcoolisées\nActivités nautiques optionnelles à Zanzibar\nPourboires'
WHERE slug='safari-tanzanie';

UPDATE travel_programs SET
  description_fr = 'Neuf jours pour les amateurs de gastronomie et d''art à travers Rome, Florence et Venise. Dégustez les meilleures pâtes fraîches, visitez les vignobles du Chianti, et laissez-vous porter par les chefs-d''œuvre de la Renaissance. Ateliers de cuisine avec des chefs locaux et dégustations de vins ponctuent ce voyage culturel et culinaire en Italie.',
  includes_fr = E'Trains à grande vitesse entre les villes\nGuide francophone\nHébergement en hôtels 4*\nDeux ateliers de cuisine italienne\nDégustation de vins au Chianti\nPetits-déjeuners et 3 dîners typiques',
  excludes_fr = E'Vols internationaux\nDéjeuners (sauf ateliers)\nEntrées musées non mentionnées\nPourboires'
WHERE slug='gastronomie-italie';
