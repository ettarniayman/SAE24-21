#!/usr/bin/env python3
"""
reconnaissance_camera_v3.py — Version Créative Complète
---------------------------------------------------------
Reconnaissance faciale avancée — Projet Pépinière SAE21/SAE24

FONCTIONNALITÉS :
  ✅ Reconnaissance faciale multi-personnes
  ✅ Détection de mouvement (économie CPU)
  ✅ Alerte INTRUS avec photo horodatée sauvegardée
  ✅ Notification Telegram instantanée en cas d'intrus
  ✅ Support multi-caméras simultané (threads)
  ✅ Dashboard présence en temps réel
  ✅ Rapport HTML auto-généré
  ✅ Carte de chaleur des heures de passage
  ✅ CSV enrichi (caméra, type, durée)
  ✅ QR Code badge en complément de la reconnaissance faciale

Usage :
    python3 reconnaissance_camera_v3.py --enroll "Nom Prénom" photo.jpg
    python3 reconnaissance_camera_v3.py --watch --source 0
    python3 reconnaissance_camera_v3.py --watch --source "rtsp://admin:admin@192.168.165.2:554/live.sdp"
    python3 reconnaissance_camera_v3.py --multi --sources "rtsp://cam1" "rtsp://cam2"
    python3 reconnaissance_camera_v3.py --presence
    python3 reconnaissance_camera_v3.py --report
    python3 reconnaissance_camera_v3.py --heatmap
"""

import sys
import os
import csv
import json
import argparse
import threading
import requests
from datetime import datetime, timedelta
from collections import defaultdict

try:
    import cv2
    import face_recognition
except ImportError:
    print("Installe : pip install opencv-python face_recognition")
    sys.exit(1)

# ──────────────────────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────────────────────
KNOWN_FACES_DIR    = "visages_connus"
LOG_FILE           = "journal_entrees_sorties.csv"
INTRUS_DIR         = "alertes_intrus"
REPORT_FILE        = "rapport_camera.html"
PRESENCE_FILE      = "presence_actuelle.json"
HEATMAP_FILE       = "heatmap_presences.json"

TELEGRAM_TOKEN     = "TON_TOKEN_BOT_TELEGRAM"
TELEGRAM_CHAT_ID   = "TON_CHAT_ID"
PROXY_URL          = "http://cache-etu.univ-artois.fr:3128"

DELAI_MIN_LOG      = timedelta(seconds=30)
SEUIL_INTRUS       = 5        # Détections consécutives avant alerte
TIMEOUT_PRESENCE   = 120      # secondes sans détection = personne partie
SEUIL_MOUVEMENT    = 1500     # pixels changés pour déclencher la reconnaissance


# ══════════════════════════════════════════════════════════════
# UTILITAIRES
# ══════════════════════════════════════════════════════════════

def ensure_dirs():
    for d in [KNOWN_FACES_DIR, INTRUS_DIR]:
        os.makedirs(d, exist_ok=True)
    if not os.path.isfile(LOG_FILE):
        with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["date", "heure", "nom_prenom", "camera", "type"])


def log_entry(name: str, camera: str, entry_type: str, last_logged: dict):
    now = datetime.now()
    key = f"{name}_{camera}"
    if key in last_logged and (now - last_logged[key]) < DELAI_MIN_LOG:
        return
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            name, camera, entry_type
        ])
    last_logged[key] = now
    icon = "✅" if entry_type == "reconnu" else "🚨 INTRUS"
    print(f"[{now.strftime('%H:%M:%S')}] {icon} {name} — {camera}")
    update_heatmap(now.hour)


def update_heatmap(hour: int):
    """Met à jour la carte de chaleur des heures de passage."""
    data = {}
    if os.path.exists(HEATMAP_FILE):
        with open(HEATMAP_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    data[str(hour)] = data.get(str(hour), 0) + 1
    with open(HEATMAP_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)


def update_presence(name: str, camera: str):
    presence = {}
    if os.path.exists(PRESENCE_FILE):
        with open(PRESENCE_FILE, "r", encoding="utf-8") as f:
            presence = json.load(f)
    presence[name] = {
        "derniere_vue": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "camera": camera
    }
    with open(PRESENCE_FILE, "w", encoding="utf-8") as f:
        json.dump(presence, f, ensure_ascii=False, indent=2)


def get_presence():
    if not os.path.exists(PRESENCE_FILE):
        return {}
    with open(PRESENCE_FILE, "r", encoding="utf-8") as f:
        presence = json.load(f)
    now = datetime.now()
    return {
        name: data for name, data in presence.items()
        if (now - datetime.strptime(data["derniere_vue"], "%Y-%m-%d %H:%M:%S")).total_seconds() < TIMEOUT_PRESENCE
    }


# ══════════════════════════════════════════════════════════════
# NOTIFICATIONS
# ══════════════════════════════════════════════════════════════

def send_telegram(message: str, photo_path: str = None):
    """Envoie une notification Telegram, avec photo si disponible."""
    try:
        proxies = {"https": PROXY_URL}
        if photo_path and os.path.isfile(photo_path):
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
            with open(photo_path, "rb") as photo:
                requests.post(url, data={
                    "chat_id": TELEGRAM_CHAT_ID,
                    "caption": message
                }, files={"photo": photo}, proxies=proxies, timeout=10)
        else:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            requests.post(url, json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "Markdown"
            }, proxies=proxies, timeout=10)
        print("📲 Notification Telegram envoyée.")
    except Exception as e:
        print(f"[WARN] Telegram : {e}")


# ══════════════════════════════════════════════════════════════
# DÉTECTION DE MOUVEMENT
# ══════════════════════════════════════════════════════════════

def detect_motion(prev_frame, current_frame) -> bool:
    """Retourne True si du mouvement est détecté entre deux frames."""
    if prev_frame is None:
        return True
    diff = cv2.absdiff(prev_frame, current_frame)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
    return cv2.countNonZero(thresh) > SEUIL_MOUVEMENT


# ══════════════════════════════════════════════════════════════
# SCAN QR CODE
# ══════════════════════════════════════════════════════════════

def scan_qr_code(frame):
    """Scanne un QR code dans la frame. Retourne le texte décodé ou None."""
    try:
        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(frame)
        return data if data else None
    except Exception:
        return None


# ══════════════════════════════════════════════════════════════
# CHARGEMENT DES VISAGES
# ══════════════════════════════════════════════════════════════

def load_known_faces():
    encodings, names = [], []
    if not os.path.isdir(KNOWN_FACES_DIR):
        return encodings, names
    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            img = face_recognition.load_image_file(os.path.join(KNOWN_FACES_DIR, filename))
            enc = face_recognition.face_encodings(img)
            if enc:
                encodings.append(enc[0])
                names.append(os.path.splitext(filename)[0].replace("_", " "))
    print(f"✅ {len(names)} personne(s) chargée(s) : {', '.join(names) or 'aucune'}")
    return encodings, names


# ══════════════════════════════════════════════════════════════
# ENRÔLEMENT
# ══════════════════════════════════════════════════════════════

def enroll_person(name: str, photo_path: str):
    if not os.path.isfile(photo_path):
        print(f"Photo introuvable : {photo_path}")
        return
    img = face_recognition.load_image_file(photo_path)
    if not face_recognition.face_encodings(img):
        print("Aucun visage détecté dans cette photo. Essaie une photo plus nette, de face.")
        return
    dest = os.path.join(KNOWN_FACES_DIR, f"{name.replace(' ', '_')}.jpg")
    cv2.imwrite(dest, cv2.imread(photo_path))
    print(f"✅ {name} enrôlé(e) → {dest}")


# ══════════════════════════════════════════════════════════════
# SURVEILLANCE (une caméra)
# ══════════════════════════════════════════════════════════════

def watch_stream(source, known_encodings, known_names,
                 camera_name="CAM1", display=True):
    video = cv2.VideoCapture(source)
    if not video.isOpened():
        print(f"❌ Impossible d'ouvrir le flux : {source}")
        return

    print(f"🎥 Surveillance démarrée — {camera_name}")
    last_logged  = {}
    intrus_count = defaultdict(int)
    prev_frame   = None
    frame_count  = 0
    FRAME_SKIP   = 5

    while True:
        ret, frame = video.read()
        if not ret:
            print(f"Flux interrompu : {camera_name}")
            break

        frame_count += 1

        # 1. QR Code badge — vérifié à chaque frame (rapide)
        qr_data = scan_qr_code(frame)
        if qr_data:
            log_entry(f"Badge:{qr_data}", camera_name, "badge", last_logged)
            update_presence(f"Badge:{qr_data}", camera_name)

        # 2. Détection de mouvement — filtre pour économiser le CPU
        if frame_count % FRAME_SKIP != 0:
            prev_frame = frame.copy()
            if display:
                cv2.imshow(f"Surveillance — {camera_name}", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            continue

        # 3. Reconnaissance faciale (uniquement si mouvement détecté)
        if not detect_motion(prev_frame, frame):
            prev_frame = frame.copy()
            continue

        prev_frame = frame.copy()
        small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb   = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

        locations = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, locations)

        for (top, right, bottom, left), enc in zip(locations, encodings):
            matches = face_recognition.compare_faces(known_encodings, enc, tolerance=0.5)
            name = "Inconnu"
            entry_type = "intrus"

            if True in matches:
                name = known_names[matches.index(True)]
                entry_type = "reconnu"
                intrus_count[camera_name] = 0
                update_presence(name, camera_name)
            else:
                intrus_count[camera_name] += 1
                if intrus_count[camera_name] >= SEUIL_INTRUS:
                    # Sauvegarde photo de l'intrus
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    alert_path = os.path.join(INTRUS_DIR, f"intrus_{camera_name}_{ts}.jpg")
                    cv2.imwrite(alert_path, frame)
                    print(f"🚨 ALERTE INTRUS ! Photo : {alert_path}")
                    # Notification Telegram avec photo
                    send_telegram(
                        f"🚨 *ALERTE INTRUS* — Caméra {camera_name}\n"
                        f"Visage inconnu détecté à {datetime.now().strftime('%H:%M:%S')}",
                        photo_path=alert_path
                    )
                    intrus_count[camera_name] = 0

            log_entry(name, camera_name, entry_type, last_logged)

            # Affichage
            if display:
                t, r, b, l = top*4, right*4, bottom*4, left*4
                color = (0, 255, 0) if name != "Inconnu" else (0, 0, 255)
                cv2.rectangle(frame, (l, t), (r, b), color, 2)
                cv2.rectangle(frame, (l, b-35), (r, b), color, cv2.FILLED)
                cv2.putText(frame, name, (l+6, b-6),
                            cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

        if display:
            # Affiche le nb de personnes présentes en overlay
            presence = get_presence()
            cv2.putText(frame, f"Presents: {len(presence)}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 215, 255), 2)
            cv2.imshow(f"Surveillance — {camera_name}", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    video.release()
    if display:
        cv2.destroyAllWindows()


# ══════════════════════════════════════════════════════════════
# MULTI-CAMÉRAS
# ══════════════════════════════════════════════════════════════

def watch_multi(sources: list, known_encodings, known_names):
    threads = []
    for i, source in enumerate(sources):
        src = 0 if source == "0" else source
        cam = f"CAM{i+1}"
        t = threading.Thread(
            target=watch_stream,
            args=(src, known_encodings, known_names, cam, False),
            daemon=True
        )
        t.start()
        threads.append(t)
        print(f"🎥 Thread démarré : {cam}")

    print(f"\n{len(threads)} caméra(s) en surveillance. Ctrl+C pour arrêter.")
    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("Surveillance arrêtée.")


# ══════════════════════════════════════════════════════════════
# PRÉSENCE & HEATMAP
# ══════════════════════════════════════════════════════════════

def show_presence():
    presence = get_presence()
    print("\n" + "═"*50)
    print("  PERSONNES ACTUELLEMENT DANS LES LOCAUX")
    print("═"*50)
    if not presence:
        print("  Aucune personne détectée.")
    for name, data in presence.items():
        print(f"  ✅ {name} — {data['camera']} — {data['derniere_vue']}")
    print("═"*50)


def show_heatmap():
    """Affiche la carte de chaleur ASCII des heures de passage."""
    if not os.path.exists(HEATMAP_FILE):
        print("Aucune donnée de passage disponible.")
        return
    with open(HEATMAP_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    max_val = max(data.values()) if data else 1
    print("\n  CARTE DE CHALEUR — Heures de passage")
    print("  " + "─"*52)
    for h in range(24):
        count = data.get(str(h), 0)
        bar = "█" * int((count / max_val) * 30)
        print(f"  {h:02d}h  [{bar:<30}] {count}")
    print("  " + "─"*52)


# ══════════════════════════════════════════════════════════════
# RAPPORT HTML
# ══════════════════════════════════════════════════════════════

def generate_report():
    entries = []
    if os.path.isfile(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            entries = list(csv.DictReader(f))[-50:]

    rows = ""
    for e in reversed(entries):
        color = "#28a745" if e.get("type") == "reconnu" else "#dc3545"
        rows += f"""
        <tr>
            <td>{e.get('date','')} {e.get('heure','')}</td>
            <td>{e.get('nom_prenom','')}</td>
            <td>{e.get('camera','')}</td>
            <td style="color:{color};font-weight:bold">{e.get('type','').upper()}</td>
        </tr>"""

    intrus = sorted(os.listdir(INTRUS_DIR))[-5:] if os.path.isdir(INTRUS_DIR) else []
    intrus_html = "".join(f"<li>📸 {f}</li>" for f in intrus) or "<li>Aucune alerte intrus.</li>"

    presence = get_presence()
    presence_html = "".join(
        f"<li>✅ <strong>{n}</strong> — {d['camera']} — {d['derniere_vue']}</li>"
        for n, d in presence.items()
    ) or "<li>Aucune personne présente actuellement.</li>"

    # Heatmap en HTML
    heatmap_html = ""
    if os.path.exists(HEATMAP_FILE):
        with open(HEATMAP_FILE, "r", encoding="utf-8") as f:
            hdata = json.load(f)
        max_v = max(hdata.values()) if hdata else 1
        for h in range(24):
            count = hdata.get(str(h), 0)
            pct = int((count / max_v) * 100) if max_v > 0 else 0
            heatmap_html += f"""
            <div style="display:flex;align-items:center;margin:3px 0">
                <span style="width:35px;font-size:12px">{h:02d}h</span>
                <div style="background:#B8860B;height:18px;width:{pct}%;border-radius:3px;min-width:2px"></div>
                <span style="margin-left:8px;font-size:12px">{count}</span>
            </div>"""

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="30">
    <title>Rapport Caméra — RTVoyage</title>
    <style>
        body {{ font-family:'Segoe UI',Arial,sans-serif; background:#0f0f1a; color:#e0e0e0; margin:0; padding:30px; }}
        h1 {{ color:#B8860B; border-bottom:3px solid #B8860B; padding-bottom:12px; margin-bottom:25px; }}
        h2 {{ color:#9CA3AF; margin:25px 0 12px; }}
        table {{ width:100%; border-collapse:collapse; margin-bottom:30px; }}
        th {{ background:#1F2937; padding:14px; text-align:left; color:#B8860B; font-size:13px; text-transform:uppercase; }}
        td {{ padding:12px; border-bottom:1px solid #1F2937; }}
        tr:hover td {{ background:#1F2937; }}
        ul {{ background:#1F2937; padding:15px 15px 15px 35px; border-radius:8px; }}
        li {{ margin:6px 0; }}
        .heatmap {{ background:#1F2937; padding:20px; border-radius:8px; }}
        footer {{ color:#4B5563; font-size:12px; margin-top:30px; text-align:center; }}
    </style>
</head>
<body>
    <h1>📹 Rapport Surveillance Caméra — RTVoyage</h1>
    <p style="color:#6B7280;font-size:13px">Mis à jour : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} — Rafraîchissement auto 30s</p>

    <h2>👥 Présences actuelles</h2>
    <ul>{presence_html}</ul>

    <h2>🚨 Dernières alertes intrus</h2>
    <ul>{intrus_html}</ul>

    <h2>📊 Carte de chaleur des passages (par heure)</h2>
    <div class="heatmap">{heatmap_html or '<p style="color:#6B7280">Aucune donnée encore.</p>'}</div>

    <h2>📋 Journal des 50 derniers événements</h2>
    <table>
        <thead><tr><th>Date/Heure</th><th>Personne</th><th>Caméra</th><th>Type</th></tr></thead>
        <tbody>{rows}</tbody>
    </table>

    <footer>Projet SAE21/SAE24 — IUT de Béthune — BUT Réseaux & Télécommunications</footer>
</body>
</html>"""

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Rapport HTML généré : {REPORT_FILE}")
    print(f"   Copie dans Flask : cp {REPORT_FILE} ~/SAE24-21_/flask/app/static/")


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Reconnaissance Caméra v3 — Pépinière RTVoyage")
    parser.add_argument("--enroll", metavar="NOM", help="Enrôler une personne")
    parser.add_argument("photo", nargs="?", help="Photo pour l'enrôlement")
    parser.add_argument("--watch",    action="store_true")
    parser.add_argument("--multi",    action="store_true")
    parser.add_argument("--source",   default="0")
    parser.add_argument("--sources",  nargs="+")
    parser.add_argument("--no-display", action="store_true")
    parser.add_argument("--presence", action="store_true")
    parser.add_argument("--report",   action="store_true")
    parser.add_argument("--heatmap",  action="store_true")
    args = parser.parse_args()

    ensure_dirs()

    if args.enroll:
        if not args.photo:
            print("Usage : --enroll \"Nom Prénom\" photo.jpg")
            sys.exit(1)
        enroll_person(args.enroll, args.photo)

    elif args.presence:
        show_presence()

    elif args.heatmap:
        show_heatmap()

    elif args.report:
        generate_report()

    elif args.multi:
        sources = args.sources or ["0"]
        enc, names = load_known_faces()
        if not enc:
            print("⚠️ Aucune personne enrôlée.")
            sys.exit(1)
        watch_multi(sources, enc, names)

    elif args.watch:
        enc, names = load_known_faces()
        if not enc:
            print("⚠️ Aucune personne enrôlée. Utilise --enroll d'abord.")
            sys.exit(1)
        source = 0 if args.source == "0" else args.source
        watch_stream(source, enc, names, display=not args.no_display)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()