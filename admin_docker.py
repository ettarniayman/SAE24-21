#!/usr/bin/env python3
"""
admin_docker_v3.py — Version Créative Complète
------------------------------------------------
Script d'administration avancée des conteneurs Docker
Projet Pépinière SAE21/SAE24 — RTVoyage

FONCTIONNALITÉS :
  ✅ Menu interactif complet
  ✅ Surveillance automatique avec auto-relance
  ✅ Alerte email en cas de panne
  ✅ Notification Telegram instantanée
  ✅ Graphique ASCII CPU/RAM
  ✅ Sauvegarde planifiée automatique (minuit)
  ✅ Rapport HTML auto-généré
  ✅ Historique JSON des événements
  ✅ Export logs horodatés
  ✅ Affichage espace disque volumes Docker
  ✅ Bandeau RSS automatique sur incident

Usage :
    python3 admin_docker_v3.py           → menu interactif
    python3 admin_docker_v3.py status    → état rapide
    python3 admin_docker_v3.py watch     → surveillance continue
    python3 admin_docker_v3.py report    → génère rapport HTML
    python3 admin_docker_v3.py backup    → sauvegarde BDD
    python3 admin_docker_v3.py schedule  → sauvegarde planifiée
"""

import sys
import os
import time
import json
import smtplib
import threading
import requests
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    import docker
except ImportError:
    print("Module 'docker' manquant. Installe-le avec : pip install docker")
    sys.exit(1)

# ──────────────────────────────────────────────────────────────
# CONFIGURATION — À adapter selon ton environnement
# ──────────────────────────────────────────────────────────────
SERVICES = {
    "web":     "rtvoyage_flask",
    "db":      "rtvoyage_postgres",
    "apache":  "rtvoyage_apache",
    "pgadmin": "rtvoyage_pgadmin",
    "tftp":    "pepiniere_tftp",
}

# Email (optionnel)
EMAIL_EXPEDITEUR  = "admin@rtvoyage.ma"
EMAIL_DESTINATAIRE = "ton_email@gmail.com"
EMAIL_SMTP        = "smtp.gmail.com"
EMAIL_PORT        = 587
EMAIL_PASSWORD    = "ton_mot_de_passe_app"

# Telegram (optionnel — crée un bot sur @BotFather)
TELEGRAM_TOKEN   = "TON_TOKEN_BOT_TELEGRAM"
TELEGRAM_CHAT_ID = "TON_CHAT_ID"
PROXY_URL        = "http://cache-etu.univ-artois.fr:3128"

# Fichiers de données
LOG_FILE         = "admin_docker.log"
REPORT_FILE      = "rapport_docker.html"
HISTORY_FILE     = "historique_evenements.json"
RSS_FILE         = "rss_incidents.xml"

CHECK_INTERVAL   = 30   # secondes entre chaque vérification en mode watch
DB_USER          = "rtvoyage_user"
DB_NAME          = "rtvoyage"


# ══════════════════════════════════════════════════════════════
# UTILITAIRES DE BASE
# ══════════════════════════════════════════════════════════════

COLORS = {
    "INFO":  "\033[92m",
    "WARN":  "\033[93m",
    "ERROR": "\033[91m",
    "OK":    "\033[94m",
    "RESET": "\033[0m"
}

def log(message: str, level: str = "INFO"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{level}] {message}"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    color = COLORS.get(level, "")
    print(f"{color}{line}{COLORS['RESET']}")


def get_client():
    try:
        return docker.from_env()
    except Exception as e:
        log(f"Impossible de se connecter à Docker : {e}", "ERROR")
        sys.exit(1)


def get_container(client, label: str):
    name = SERVICES.get(label)
    if not name:
        log(f"Service inconnu : '{label}'. Disponibles : {', '.join(SERVICES)}", "WARN")
        return None
    try:
        return client.containers.get(name)
    except docker.errors.NotFound:
        log(f"Conteneur '{name}' introuvable.", "WARN")
        return None


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_history(events: list):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(events[-500:], f, ensure_ascii=False, indent=2)


def add_event(label: str, action: str, status: str):
    events = load_history()
    events.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "service": label,
        "action": action,
        "status": status
    })
    save_history(events)


# ══════════════════════════════════════════════════════════════
# NOTIFICATIONS
# ══════════════════════════════════════════════════════════════

def send_email_alert(subject: str, body: str):
    """Envoie un email d'alerte en cas de panne."""
    try:
        msg = MIMEMultipart()
        msg["From"]    = EMAIL_EXPEDITEUR
        msg["To"]      = EMAIL_DESTINATAIRE
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))
        with smtplib.SMTP(EMAIL_SMTP, EMAIL_PORT) as s:
            s.starttls()
            s.login(EMAIL_EXPEDITEUR, EMAIL_PASSWORD)
            s.send_message(msg)
        log(f"Email d'alerte envoyé : {subject}", "OK")
    except Exception as e:
        log(f"Erreur envoi email : {e}", "WARN")


def send_telegram_alert(message: str):
    """Envoie une notification Telegram instantanée."""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        proxies = {"https": PROXY_URL} if PROXY_URL else None
        requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }, proxies=proxies, timeout=10)
        log("Notification Telegram envoyée.", "OK")
    except Exception as e:
        log(f"Erreur Telegram : {e}", "WARN")


def notify_incident(label: str, action: str):
    """Notifie par email + Telegram en cas d'incident."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"⚠️ [RTVoyage] Service '{label}' — {action} — {ts}"
    send_telegram_alert(msg)
    send_email_alert(
        subject=f"[RTVoyage] Alerte panne — {label}",
        body=f"{msg}\n\nVérifiez l'état des conteneurs sur http://192.168.161.2/admin"
    )
    update_rss(label, action)


# ══════════════════════════════════════════════════════════════
# FLUX RSS AUTOMATIQUE
# ══════════════════════════════════════════════════════════════

def update_rss(service: str, event: str):
    """Ajoute un événement au flux RSS des incidents."""
    ts = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
    item = f"""
    <item>
        <title>[RTVoyage] {event} — {service}</title>
        <description>Le service {service} a subi un événement : {event} le {ts}</description>
        <pubDate>{ts}</pubDate>
        <guid>{ts}-{service}</guid>
    </item>"""

    items = ""
    if os.path.exists(RSS_FILE):
        with open(RSS_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            start = content.find("<item>")
            if start != -1:
                items = content[start:content.rfind("</item>") + 7]

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>RTVoyage — Incidents Infrastructure</title>
    <link>http://192.168.161.2</link>
    <description>Alertes et événements des services Docker RTVoyage</description>
    {item}
    {items}
  </channel>
</rss>"""

    with open(RSS_FILE, "w", encoding="utf-8") as f:
        f.write(rss)
    log(f"Flux RSS mis à jour : {RSS_FILE}", "OK")


# ══════════════════════════════════════════════════════════════
# FONCTIONS PRINCIPALES
# ══════════════════════════════════════════════════════════════

def list_status(client):
    print("\n" + "═" * 72)
    print(f"  {'SERVICE':<12} {'CONTENEUR':<25} {'ÉTAT':<12} {'DÉMARRÉ LE'}")
    print("═" * 72)
    all_ok = True
    for label, name in SERVICES.items():
        try:
            c = client.containers.get(name)
            status = c.status
            started = c.attrs.get("State", {}).get("StartedAt", "")[:16]
            icon = "✅" if status == "running" else "❌"
            if status != "running":
                all_ok = False
            print(f"  {icon} {label:<10} {name:<25} {status:<12} {started}")
        except docker.errors.NotFound:
            print(f"  ❓ {label:<10} {name:<25} {'INTROUVABLE':<12}")
            all_ok = False
    print("═" * 72)
    print(f"  État global : {'✅ TOUT OK' if all_ok else '⚠️  PANNES DÉTECTÉES'}")
    print()
    return all_ok


def restart_service(client, label: str):
    c = get_container(client, label)
    if not c:
        return
    c.restart()
    log(f"Service '{label}' ({c.name}) redémarré.", "OK")
    add_event(label, "RESTART", "success")


def stop_service(client, label: str):
    c = get_container(client, label)
    if not c:
        return
    c.stop()
    log(f"Service '{label}' ({c.name}) arrêté.", "WARN")
    add_event(label, "STOP", "manual")


def start_service(client, label: str):
    c = get_container(client, label)
    if not c:
        return
    c.start()
    log(f"Service '{label}' ({c.name}) démarré.", "OK")
    add_event(label, "START", "success")


def show_logs(client, label: str, lines: int = 30):
    c = get_container(client, label)
    if not c:
        return
    logs = c.logs(tail=lines).decode("utf-8", errors="replace")
    print(f"\n{'═'*60}\n  LOGS — {c.name}\n{'═'*60}")
    print(logs)


def show_stats(client, label: str):
    """Stats CPU/RAM avec graphique ASCII en couleur."""
    c = get_container(client, label)
    if not c:
        return
    stats = c.stats(stream=False)
    cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - \
                stats["precpu_stats"]["cpu_usage"]["total_usage"]
    sys_delta = stats["cpu_stats"]["system_cpu_usage"] - \
                stats["precpu_stats"]["system_cpu_usage"]
    cpu_pct = round((cpu_delta / sys_delta) * 100, 1) if sys_delta > 0 else 0
    mem_mb  = round(stats["memory_stats"]["usage"] / 1024 / 1024, 1)
    mem_lim = round(stats["memory_stats"]["limit"] / 1024 / 1024, 1)
    mem_pct = round((mem_mb / mem_lim) * 100, 1) if mem_lim > 0 else 0

    cpu_bar = "\033[92m" + "█" * int(cpu_pct / 5) + "\033[90m" + "░" * (20 - int(cpu_pct / 5)) + "\033[0m"
    mem_bar = "\033[94m" + "█" * int(mem_pct / 5) + "\033[90m" + "░" * (20 - int(mem_pct / 5)) + "\033[0m"

    print(f"\n  📊 Stats — {c.name}")
    print(f"  CPU  [{cpu_bar}] {cpu_pct}%")
    print(f"  RAM  [{mem_bar}] {mem_mb}Mo / {mem_lim}Mo ({mem_pct}%)")


def show_disk_usage(client):
    """Affiche l'espace disque utilisé par les volumes Docker."""
    print(f"\n{'═'*60}\n  💾 ESPACE DISQUE — Volumes Docker\n{'═'*60}")
    try:
        df = client.df()
        for vol in df.get("Volumes", []):
            name = vol.get("Name", "?")
            size = vol.get("UsageData", {}).get("Size", 0)
            size_mb = round(size / 1024 / 1024, 1) if size > 0 else 0
            print(f"  📦 {name:<40} {size_mb} Mo")
        for img in df.get("Images", [])[:5]:
            tags = img.get("RepoTags", ["<none>"])
            size = round(img.get("Size", 0) / 1024 / 1024, 1)
            print(f"  🐳 {tags[0] if tags else '<none>':<40} {size} Mo")
    except Exception as e:
        log(f"Erreur disk usage : {e}", "WARN")
    print()


def backup_db(client):
    """Sauvegarde PostgreSQL horodatée avec notification."""
    c = get_container(client, "db")
    if not c:
        return
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"backup_{ts}.sql"
    _, output = c.exec_run(f"pg_dump -U {DB_USER} {DB_NAME}", demux=False)
    with open(filename, "wb") as f:
        f.write(output)
    size_kb = round(os.path.getsize(filename) / 1024, 1)
    log(f"Sauvegarde créée : {filename} ({size_kb} Ko)", "OK")
    add_event("db", "BACKUP", filename)
    return filename


def export_logs():
    """Exporte les logs dans un fichier horodaté."""
    if not os.path.exists(LOG_FILE):
        print("Aucun log à exporter.")
        return
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = f"logs_export_{ts}.txt"
    with open(LOG_FILE, "r") as src, open(dest, "w") as dst:
        dst.write(src.read())
    log(f"Logs exportés : {dest}", "OK")


def generate_report(client):
    """Génère un rapport HTML complet, auto-rafraîchi toutes les 30 secondes."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows = ""
    for label, name in SERVICES.items():
        try:
            c = client.containers.get(name)
            status = c.status
            color = "#28a745" if status == "running" else "#dc3545"
            started = c.attrs.get("State", {}).get("StartedAt", "")[:16]
            rows += f"""
            <tr>
                <td>{label}</td><td>{name}</td>
                <td style="color:{color};font-weight:bold">{status.upper()}</td>
                <td>{started}</td>
            </tr>"""
        except docker.errors.NotFound:
            rows += f"""
            <tr>
                <td>{label}</td><td>{name}</td>
                <td style="color:#ffc107;font-weight:bold">INTROUVABLE</td>
                <td>—</td>
            </tr>"""

    events = load_history()[-20:]
    event_rows = ""
    for e in reversed(events):
        color = "#28a745" if e["status"] == "success" else "#dc3545"
        event_rows += f"""
        <tr>
            <td>{e['timestamp']}</td><td>{e['service']}</td>
            <td>{e['action']}</td>
            <td style="color:{color}">{e['status']}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="30">
    <title>Dashboard Docker — RTVoyage</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #0f0f1a; color: #e0e0e0; padding: 30px; }}
        h1 {{ color: #B8860B; border-bottom: 3px solid #B8860B; padding-bottom: 12px; margin-bottom: 25px; font-size: 28px; }}
        h2 {{ color: #9CA3AF; margin: 25px 0 12px; font-size: 18px; }}
        .meta {{ color: #6B7280; font-size: 13px; margin-bottom: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; border-radius: 8px; overflow: hidden; }}
        th {{ background: #1F2937; padding: 14px 16px; text-align: left; color: #B8860B; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px; }}
        td {{ padding: 12px 16px; border-bottom: 1px solid #1F2937; font-size: 14px; }}
        tr:hover td {{ background: #1F2937; }}
        .badge {{ display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: bold; }}
        footer {{ color: #4B5563; font-size: 12px; margin-top: 30px; text-align: center; }}
    </style>
</head>
<body>
    <h1>🐳 Dashboard Infrastructure — RTVoyage Pépinière</h1>
    <p class="meta">Généré le : <strong>{ts}</strong> &nbsp;|&nbsp; Auto-rafraîchissement toutes les 30 secondes</p>

    <h2>📊 État des services</h2>
    <table>
        <thead><tr><th>Service</th><th>Conteneur</th><th>État</th><th>Démarré le</th></tr></thead>
        <tbody>{rows}</tbody>
    </table>

    <h2>📋 Historique des événements (20 derniers)</h2>
    <table>
        <thead><tr><th>Date/Heure</th><th>Service</th><th>Action</th><th>Résultat</th></tr></thead>
        <tbody>{event_rows}</tbody>
    </table>

    <footer>Projet SAE21/SAE24 — IUT de Béthune — BUT Réseaux & Télécommunications</footer>
</body>
</html>"""

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    log(f"Rapport HTML généré : {REPORT_FILE}", "OK")
    print(f"  Ouvre avec : xdg-open {REPORT_FILE}")
    print(f"  Ou copie dans static Flask : cp {REPORT_FILE} ~/SAE24-21_/flask/app/static/")


def watch_mode(client):
    """Surveillance continue avec auto-relance et notifications."""
    log("Mode surveillance démarré. Ctrl+C pour arrêter.", "INFO")
    try:
        while True:
            for label, name in SERVICES.items():
                try:
                    c = client.containers.get(name)
                    if c.status != "running":
                        log(f"⚠️  '{label}' est tombé ! Relance automatique...", "ERROR")
                        print("\a")
                        notify_incident(label, "PANNE DÉTECTÉE — Relance automatique")
                        c.start()
                        log(f"✅ '{label}' relancé.", "OK")
                        add_event(label, "AUTO_RESTART", "success")
                        notify_incident(label, "Service relancé avec succès")
                except docker.errors.NotFound:
                    log(f"'{label}' introuvable.", "WARN")
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        log("Surveillance arrêtée.", "INFO")


def schedule_backup(client):
    """Lance une sauvegarde planifiée toutes les nuits à minuit."""
    log("Sauvegarde planifiée activée (tous les jours à 00:00). Ctrl+C pour arrêter.", "INFO")
    try:
        while True:
            now = datetime.now()
            if now.hour == 0 and now.minute == 0:
                log("Sauvegarde automatique de nuit...", "INFO")
                backup_db(client)
                time.sleep(61)
            time.sleep(30)
    except KeyboardInterrupt:
        log("Planification arrêtée.", "INFO")


# ══════════════════════════════════════════════════════════════
# MENU INTERACTIF
# ══════════════════════════════════════════════════════════════

def print_menu():
    print("""
\033[93m╔══════════════════════════════════════════════════════════════╗
║        ADMINISTRATION DOCKER v3 — Projet Pépinière RTVoyage   ║
╠══════════════════════════════════════════════════════════════╣
║  1.  Afficher l'état de tous les services                     ║
║  2.  Démarrer un service                                      ║
║  3.  Arrêter un service                                       ║
║  4.  Redémarrer un service                                    ║
║  5.  Voir les logs d'un service                               ║
║  6.  Voir les statistiques CPU/RAM (graphique ASCII couleur)  ║
║  7.  Voir l'espace disque des volumes Docker                  ║
║  8.  Sauvegarder la base de données maintenant                ║
║  9.  Activer la sauvegarde planifiée (chaque nuit à minuit)   ║
║  10. Générer le rapport HTML                                  ║
║  11. Exporter les logs                                        ║
║  12. Mode surveillance automatique (auto-relance + alertes)   ║
║  0.  Quitter                                                  ║
╚══════════════════════════════════════════════════════════════╝\033[0m
""")


def interactive_menu():
    client = get_client()
    while True:
        print_menu()
        choice = input("  Choix : ").strip()
        if choice == "0":
            print("Au revoir.")
            break
        elif choice == "1":
            list_status(client)
        elif choice in ("2", "3", "4", "5", "6"):
            print(f"  Services disponibles : {', '.join(SERVICES.keys())}")
            label = input("  Quel service ? : ").strip()
            if   choice == "2": start_service(client, label)
            elif choice == "3": stop_service(client, label)
            elif choice == "4": restart_service(client, label)
            elif choice == "5": show_logs(client, label)
            elif choice == "6": show_stats(client, label)
        elif choice == "7":  show_disk_usage(client)
        elif choice == "8":  backup_db(client)
        elif choice == "9":  threading.Thread(target=schedule_backup, args=(client,), daemon=True).start(); print("Planification activée en arrière-plan.")
        elif choice == "10": generate_report(client)
        elif choice == "11": export_logs()
        elif choice == "12": watch_mode(client)
        else:
            print("  Choix invalide.")
        input("\n  Appuie sur Entrée pour continuer...")


# ══════════════════════════════════════════════════════════════
# POINT D'ENTRÉE
# ══════════════════════════════════════════════════════════════

def main():
    client = get_client()
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        label = sys.argv[2] if len(sys.argv) > 2 else None
        if   cmd == "status":   list_status(client)
        elif cmd == "watch":    watch_mode(client)
        elif cmd == "report":   generate_report(client)
        elif cmd == "backup":   backup_db(client)
        elif cmd == "schedule": schedule_backup(client)
        elif cmd == "disk":     show_disk_usage(client)
        elif cmd == "restart" and label: restart_service(client, label)
        elif cmd == "stop"    and label: stop_service(client, label)
        elif cmd == "start"   and label: start_service(client, label)
        elif cmd == "logs"    and label: show_logs(client, label)
        elif cmd == "stats"   and label: show_stats(client, label)
        else:
            print("Usage : python3 admin_docker_v3.py [status|watch|report|backup|schedule|disk|restart|stop|start|logs|stats] [service]")
        return
    interactive_menu()


if __name__ == "__main__":
    main()