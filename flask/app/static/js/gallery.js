/* RT Voyage — gallery.js : lightbox pur JS */
'use strict';

(function () {
  /* Build lightbox DOM once */
  const lb = document.createElement('div');
  lb.id = 'rtLightbox';
  lb.innerHTML = `
    <div class="lb-overlay"></div>
    <div class="lb-container">
      <button class="lb-close" aria-label="Fermer">&#x2715;</button>
      <button class="lb-prev" aria-label="Précédent">&#x2039;</button>
      <button class="lb-next" aria-label="Suivant">&#x203A;</button>
      <div class="lb-media"></div>
      <div class="lb-caption"></div>
      <div class="lb-counter"></div>
    </div>`;
  document.body.appendChild(lb);

  const style = document.createElement('style');
  style.textContent = `
    #rtLightbox{position:fixed;inset:0;z-index:9999;display:none;align-items:center;justify-content:center;}
    #rtLightbox.active{display:flex;}
    .lb-overlay{position:absolute;inset:0;background:rgba(5,8,16,0.96);cursor:pointer;}
    .lb-container{position:relative;z-index:1;max-width:90vw;max-height:90vh;display:flex;flex-direction:column;align-items:center;}
    .lb-media img,.lb-media video{max-width:88vw;max-height:78vh;border-radius:4px;box-shadow:0 8px 40px rgba(0,0,0,0.7);object-fit:contain;}
    .lb-media iframe{width:80vw;height:45vw;max-height:75vh;border:none;border-radius:4px;box-shadow:0 8px 40px rgba(0,0,0,0.7);}
    .lb-close{position:fixed;top:20px;right:24px;background:none;border:none;color:#fff;font-size:1.6rem;cursor:pointer;opacity:0.7;transition:opacity 0.2s;}
    .lb-close:hover{opacity:1;}
    .lb-prev,.lb-next{position:fixed;top:50%;transform:translateY(-50%);background:rgba(201,169,110,0.15);border:1px solid rgba(201,169,110,0.3);color:var(--gold,#c9a96e);font-size:2.5rem;cursor:pointer;padding:4px 16px;border-radius:4px;transition:background 0.2s;}
    .lb-prev{left:16px;}.lb-next{right:16px;}
    .lb-prev:hover,.lb-next:hover{background:rgba(201,169,110,0.3);}
    .lb-caption{margin-top:12px;font-size:0.84rem;color:rgba(255,255,255,0.6);text-align:center;}
    .lb-counter{font-size:0.72rem;color:rgba(255,255,255,0.35);margin-top:6px;}
  `;
  document.head.appendChild(style);

  let items = [];
  let current = 0;

  function extractYouTubeId(url) {
    const m = url.match(/(?:youtube\.com\/(?:watch\?v=|embed\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})/);
    return m ? m[1] : null;
  }

  function extractVimeoId(url) {
    const m = url.match(/vimeo\.com\/(\d+)/);
    return m ? m[1] : null;
  }

  function detectType(href) {
    if (/\.(mp4|webm|ogg)$/i.test(href)) return 'video';
    if (/youtube\.com|youtu\.be/.test(href)) return 'youtube';
    if (/vimeo\.com/.test(href)) return 'vimeo';
    return 'image';
  }

  function open(list, idx) {
    items = list;
    current = idx;
    render();
    lb.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function close() {
    lb.classList.remove('active');
    document.body.style.overflow = '';
    lb.querySelector('.lb-media').innerHTML = '';
  }

  function render() {
    const item = items[current];
    const media = lb.querySelector('.lb-media');
    media.innerHTML = '';

    if (item.type === 'video') {
      const v = document.createElement('video');
      v.src = item.src;
      v.controls = true;
      v.autoplay = true;
      media.appendChild(v);

    } else if (item.type === 'youtube') {
      const id = extractYouTubeId(item.src);
      if (id) {
        const iframe = document.createElement('iframe');
        iframe.src = `https://www.youtube.com/embed/${id}?autoplay=1&rel=0`;
        iframe.allow = 'autoplay; fullscreen; picture-in-picture';
        iframe.allowFullscreen = true;
        media.appendChild(iframe);
      }

    } else if (item.type === 'vimeo') {
      const id = extractVimeoId(item.src);
      if (id) {
        const iframe = document.createElement('iframe');
        iframe.src = `https://player.vimeo.com/video/${id}?autoplay=1`;
        iframe.allow = 'autoplay; fullscreen';
        iframe.allowFullscreen = true;
        media.appendChild(iframe);
      }

    } else {
      const img = new Image();
      img.src = item.src;
      img.alt = item.caption || '';
      media.appendChild(img);
    }

    lb.querySelector('.lb-caption').textContent = item.caption || '';
    lb.querySelector('.lb-counter').textContent = `${current + 1} / ${items.length}`;
  }

  function prev() { current = (current - 1 + items.length) % items.length; render(); }
  function next() { current = (current + 1) % items.length; render(); }

  lb.querySelector('.lb-overlay').addEventListener('click', close);
  lb.querySelector('.lb-close').addEventListener('click', close);
  lb.querySelector('.lb-prev').addEventListener('click', prev);
  lb.querySelector('.lb-next').addEventListener('click', next);

  document.addEventListener('keydown', (e) => {
    if (!lb.classList.contains('active')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') prev();
    if (e.key === 'ArrowRight') next();
  });

  /* Touch swipe */
  let touchStartX = 0;
  lb.addEventListener('touchstart', (e) => { touchStartX = e.changedTouches[0].clientX; }, { passive: true });
  lb.addEventListener('touchend', (e) => {
    const dx = e.changedTouches[0].clientX - touchStartX;
    if (Math.abs(dx) > 50) dx < 0 ? next() : prev();
  });

  /* Auto-wire gallery items */
  function wireGallery(galleryEl) {
    const anchors = galleryEl.querySelectorAll('a.gallery-item');
    const list = Array.from(anchors).map(a => ({
      src: a.href,
      caption: a.dataset.caption || a.querySelector('img')?.alt || '',
      type: detectType(a.href),
    }));
    anchors.forEach((a, i) => {
      a.addEventListener('click', (e) => {
        e.preventDefault();
        open(list, i);
      });
    });
  }

  document.querySelectorAll('.gallery-grid, #destGallery, #hotelGallery').forEach(wireGallery);

  /* Expose for dynamic galleries */
  window.RTGallery = { open, close, wire: wireGallery };
})();
