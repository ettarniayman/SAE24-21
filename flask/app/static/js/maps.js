/* RT Voyage — maps.js : Google Maps + Street View */
'use strict';

/* Called by Google Maps API callback */
window.initDestMap = function () {
  const mapEl = document.getElementById('destMap');
  const svEl = document.getElementById('destStreetView');
  if (!mapEl) return;

  const lat = parseFloat(mapEl.dataset.lat || '0');
  const lng = parseFloat(mapEl.dataset.lng || '0');
  const title = mapEl.dataset.title || 'Destination';

  const mapStyles = [
    { elementType: 'geometry', stylers: [{ color: '#0a0d1a' }] },
    { elementType: 'labels.text.fill', stylers: [{ color: '#c9a96e' }] },
    { elementType: 'labels.text.stroke', stylers: [{ color: '#050810' }] },
    { featureType: 'administrative', elementType: 'geometry', stylers: [{ color: '#1a1f3a' }] },
    { featureType: 'poi', stylers: [{ visibility: 'off' }] },
    { featureType: 'road', elementType: 'geometry', stylers: [{ color: '#1e2444' }] },
    { featureType: 'road.arterial', elementType: 'geometry', stylers: [{ color: '#262d52' }] },
    { featureType: 'road.highway', elementType: 'geometry', stylers: [{ color: '#304068' }] },
    { featureType: 'transit', stylers: [{ visibility: 'off' }] },
    { featureType: 'water', elementType: 'geometry', stylers: [{ color: '#050810' }] }
  ];

  const map = new google.maps.Map(mapEl, {
    center: { lat, lng },
    zoom: 13,
    styles: mapStyles,
    mapTypeControl: false,
    streetViewControl: false,
    fullscreenControl: true,
    zoomControl: true
  });

  /* Main marker */
  const marker = new google.maps.Marker({
    position: { lat, lng },
    map,
    title,
    icon: {
      path: google.maps.SymbolPath.CIRCLE,
      scale: 10,
      fillColor: '#c9a96e',
      fillOpacity: 1,
      strokeColor: '#e8c99a',
      strokeWeight: 2
    }
  });

  const infoWindow = new google.maps.InfoWindow({
    content: `<div style="font-family:'Montserrat',sans-serif;padding:6px;background:#0f1325;color:#c9a96e;border-radius:4px;"><strong>${title}</strong></div>`
  });
  marker.addListener('click', () => infoWindow.open(map, marker));

  /* Hotel markers from data attribute */
  try {
    const hotels = JSON.parse(mapEl.dataset.hotels || '[]');
    hotels.forEach(h => {
      if (!h.lat || !h.lng) return;
      new google.maps.Marker({
        position: { lat: h.lat, lng: h.lng },
        map,
        title: h.name,
        icon: {
          path: google.maps.SymbolPath.BACKWARD_CLOSED_ARROW,
          scale: 6,
          fillColor: '#e8c99a',
          fillOpacity: 0.9,
          strokeColor: '#c9a96e',
          strokeWeight: 1
        }
      });
    });
  } catch (_) {}

  /* Street View, avec recherche de panorama le plus proche et fallback si aucun disponible
     (frequent en zone desertique/isolee, ex: Merzouga) */
  if (svEl) {
    const svLat = parseFloat(svEl.dataset.lat || lat);
    const svLng = parseFloat(svEl.dataset.lng || lng);
    const captionEl = document.getElementById('streetViewCaption');
    const streetViewService = new google.maps.StreetViewService();

    streetViewService.getPanorama(
      { location: { lat: svLat, lng: svLng }, radius: 50000, source: google.maps.StreetViewSource.OUTDOOR },
      (data, status) => {
        if (status === google.maps.StreetViewStatus.OK) {
          new google.maps.StreetViewPanorama(svEl, {
            position: data.location.latLng,
            pov: { heading: 0, pitch: 0 },
            zoom: 1,
            addressControl: false,
            fullscreenControl: false
          });
        } else {
          svEl.innerHTML = `
            <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;gap:10px;color:var(--text-sub);background:var(--bg-card2);">
              <i class="fa fa-image" style="font-size:1.8rem;opacity:0.4;"></i>
              <span style="font-size:0.8rem;">Aucune image Street View disponible à proximité</span>
            </div>`;
          if (captionEl) captionEl.style.display = 'none';
        }
      }
    );
  }
};

/* Lazy-load Maps API when map container enters viewport */
(function () {
  const mapEl = document.getElementById('destMap');
  if (!mapEl) return;
  const apiKey = mapEl.dataset.apikey;
  if (!apiKey) return;

  let loaded = false;
  const io = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting && !loaded) {
      loaded = true;
      const s = document.createElement('script');
      s.src = `https://maps.googleapis.com/maps/api/js?key=${encodeURIComponent(apiKey)}&callback=initDestMap`;
      s.async = true;
      s.defer = true;
      document.head.appendChild(s);
      io.disconnect();
    }
  }, { threshold: 0.1 });
  io.observe(mapEl);
})();
