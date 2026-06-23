import os
import json
import csv
from datetime import datetime

from flask import render_template, current_app
from . import bp, admin_required

HOST_DATA_DIR = "/host_data"

SERVICES = {
    "web":     "rtvoyage_flask",
    "db":      "rtvoyage_postgres",
    "apache":  "rtvoyage_apache",
    "pgadmin": "rtvoyage_pgadmin",
    "tftp":    "pepiniere_tftp",
}


@bp.route("/rapport-docker")
@admin_required
def rapport_docker():
    """Génère dynamiquement l'état des conteneurs via l'API Docker."""
    import docker

    conteneurs = []
    docker_error = None
    try:
        client = docker.from_env()
    except Exception as e:
        client = None
        docker_error = str(e)

    if client:
        for label, name in SERVICES.items():
            try:
                c = client.containers.get(name)
            except docker.errors.NotFound:
                conteneurs.append({
                    "label": label, "name": name,
                    "status": "introuvable", "ok": False,
                    "cpu_pct": 0, "mem_mb": 0, "mem_lim": 0, "started": "—",
                })
                continue

            cpu_pct = mem_mb = mem_lim = 0
            if c.status == "running":
                try:
                    stats = c.stats(stream=False)
                    cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - \
                        stats["precpu_stats"]["cpu_usage"]["total_usage"]
                    sys_delta = stats["cpu_stats"]["system_cpu_usage"] - \
                        stats["precpu_stats"]["system_cpu_usage"]
                    cpu_pct = round((cpu_delta / sys_delta) * 100, 1) if sys_delta > 0 else 0
                    mem_mb = round(stats["memory_stats"]["usage"] / 1024 / 1024, 1)
                    mem_lim = round(stats["memory_stats"]["limit"] / 1024 / 1024, 1)
                except Exception:
                    pass

            conteneurs.append({
                "label": label,
                "name": name,
                "status": c.status,
                "started": c.attrs.get("State", {}).get("StartedAt", "")[:16],
                "cpu_pct": cpu_pct,
                "mem_mb": mem_mb,
                "mem_lim": mem_lim,
                "ok": c.status == "running",
            })

    history = []
    history_path = os.path.join(HOST_DATA_DIR, "historique_evenements.json")
    if os.path.exists(history_path):
        with open(history_path, "r", encoding="utf-8") as f:
            history = json.load(f)[-20:]

    return render_template(
        "admin/rapport_docker.html",
        conteneurs=conteneurs,
        history=list(reversed(history)),
        docker_error=docker_error,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )


@bp.route("/rapport-camera")
@admin_required
def rapport_camera():
    """Génère dynamiquement le rapport de surveillance caméra depuis les fichiers de données."""
    entries = []
    log_path = os.path.join(HOST_DATA_DIR, "journal_entrees_sorties.csv")
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            entries = list(csv.DictReader(f))[-50:]

    presence = {}
    presence_path = os.path.join(HOST_DATA_DIR, "presence_actuelle.json")
    if os.path.exists(presence_path):
        with open(presence_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        now = datetime.now()
        for name, data in raw.items():
            derniere = datetime.strptime(data["derniere_vue"], "%Y-%m-%d %H:%M:%S")
            if (now - derniere).total_seconds() < 120:
                presence[name] = data

    intrus_dir = os.path.join(HOST_DATA_DIR, "alertes_intrus")
    intrus = sorted(os.listdir(intrus_dir))[-10:] if os.path.isdir(intrus_dir) else []

    heatmap = {}
    heatmap_path = os.path.join(HOST_DATA_DIR, "heatmap_presences.json")
    if os.path.exists(heatmap_path):
        with open(heatmap_path, "r", encoding="utf-8") as f:
            heatmap = json.load(f)

    return render_template(
        "admin/rapport_camera.html",
        entries=list(reversed(entries)),
        presence=presence,
        intrus=intrus,
        heatmap=heatmap,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
