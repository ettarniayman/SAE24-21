#!/usr/bin/env python3
"""
extract_voip_call.py
-----------------------
Extrait et reconstitue une conversation téléphonique VoIP (RTP/G.711)
à partir d'un fichier de capture réseau (.pcap), dans le cadre du
projet pépinière SAE21/SAE24.

⚠️ USAGE STRICTEMENT PÉDAGOGIQUE, SUR TON PROPRE RÉSEAU UNIQUEMENT.
   Intercepter des communications sans autorisation est un délit
   (article 226-15 du code pénal) en dehors d'un cadre pédagogique
   autorisé comme celui-ci.

PRINCIPE :
Une conversation VoIP se déroule en 2 étapes visibles dans la capture :
  1. SIP (Session Initiation Protocol) : négocie l'appel (qui appelle qui,
     quel codec audio utiliser, sur quel port UDP envoyer le son).
  2. RTP (Real-time Transport Protocol) : transporte le son lui-même,
     paquet par paquet, sur les ports négociés par SIP.
Ce script :
  1. Parcourt le fichier pcap pour trouver les paquets RTP.
  2. Regroupe les paquets par flux (un flux = une direction de la
     conversation, identifié par IP source/destination + port).
  3. Extrait l'audio brut (généralement encodé en G.711 µ-law ou A-law).
  4. Convertit en fichier .wav écoutable avec un lecteur audio normal.

PRÉREQUIS :
    pip install scapy --break-system-packages
    sudo apt install sox -y   (pour la conversion finale en wav, plus fiable)

USAGE :
    python3 extract_voip_call.py capture_telephonie.pcap
"""

import sys
import os
import struct
import wave
from collections import defaultdict

try:
    from scapy.all import rdpcap, UDP, IP
except ImportError:
    print("Le module scapy n'est pas installé.")
    print("Installe-le avec : pip install scapy --break-system-packages")
    sys.exit(1)


# ──────────────────────────────────────────────────────────────
# Table de conversion G.711 µ-law (codec audio téléphonique standard)
# vers PCM 16 bits (format brut utilisable dans un .wav)
# ──────────────────────────────────────────────────────────────

def ulaw2linear(ulaw_byte: int) -> int:
    """Convertit un octet G.711 µ-law en échantillon PCM 16 bits signé."""
    ulaw_byte = ~ulaw_byte & 0xFF
    sign = ulaw_byte & 0x80
    exponent = (ulaw_byte >> 4) & 0x07
    mantissa = ulaw_byte & 0x0F
    sample = (mantissa << 3) + 0x84
    sample <<= exponent
    sample -= 0x84
    if sign != 0:
        sample = -sample
    return sample


def extract_rtp_streams(pcap_path: str):
    """
    Parcourt le pcap et regroupe les paquets RTP par flux
    (identifié par le couple IP:port source -> IP:port destination).
    Retourne un dict {flux_id: [bytes_audio, ...]}
    """
    print(f"Lecture de {pcap_path} ...")
    packets = rdpcap(pcap_path)
    print(f"{len(packets)} paquets chargés.")

    streams = defaultdict(list)
    rtp_count = 0

    for pkt in packets:
        if UDP in pkt and IP in pkt:
            payload = bytes(pkt[UDP].payload)
            # Un en-tête RTP fait au moins 12 octets, et le 1er octet
            # commence typiquement par la version RTP (2) en bits de poids fort
            if len(payload) > 12:
                version = (payload[0] >> 6) & 0x03
                payload_type = payload[1] & 0x7F
                # payload_type 0 = PCMU (G.711 µ-law), le plus courant en téléphonie
                if version == 2 and payload_type == 0:
                    flux_id = (
                        pkt[IP].src, pkt[UDP].sport,
                        pkt[IP].dst, pkt[UDP].dport
                    )
                    audio_payload = payload[12:]  # on saute l'en-tête RTP (12 octets)
                    streams[flux_id].append(audio_payload)
                    rtp_count += 1

    print(f"{rtp_count} paquets RTP (G.711 PCMU) détectés sur {len(streams)} flux distincts.")
    return streams


def save_stream_as_wav(audio_chunks: list, output_path: str, sample_rate: int = 8000):
    """Convertit les octets µ-law accumulés en fichier .wav PCM 16 bits."""
    raw_ulaw = b"".join(audio_chunks)

    pcm_samples = bytearray()
    for byte in raw_ulaw:
        sample = ulaw2linear(byte)
        pcm_samples += struct.pack("<h", sample)  # little-endian, 16 bits signé

    with wave.open(output_path, "wb") as wav_file:
        wav_file.setnchannels(1)        # mono (un flux = une direction)
        wav_file.setsampwidth(2)        # 16 bits = 2 octets
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(bytes(pcm_samples))

    duration_sec = len(raw_ulaw) / sample_rate
    print(f"  ✓ {output_path} créé ({duration_sec:.1f} secondes)")


def main():
    if len(sys.argv) < 2:
        print("Usage : python3 extract_voip_call.py <fichier.pcap>")
        sys.exit(1)

    pcap_path = sys.argv[1]
    if not os.path.isfile(pcap_path):
        print(f"Fichier introuvable : {pcap_path}")
        sys.exit(1)

    streams = extract_rtp_streams(pcap_path)

    if not streams:
        print("\nAucun flux RTP (G.711 PCMU) trouvé dans cette capture.")
        print("Vérifie que :")
        print("  - la capture a bien été faite pendant un appel actif")
        print("  - le codec utilisé est bien G.711 (le plus courant), pas G.729/Opus")
        print("  - tu captures au bon endroit du réseau (le trafic RTP doit transiter par là)")
        return

    output_dir = "appels_extraits"
    os.makedirs(output_dir, exist_ok=True)

    print(f"\nExtraction de {len(streams)} flux audio vers '{output_dir}/' ...")
    for i, (flux_id, chunks) in enumerate(streams.items(), start=1):
        src_ip, src_port, dst_ip, dst_port = flux_id
        filename = f"appel_{i}_{src_ip}-{src_port}_vers_{dst_ip}-{dst_port}.wav"
        output_path = os.path.join(output_dir, filename)
        save_stream_as_wav(chunks, output_path)

    print(f"\nTerminé. Écoute les fichiers .wav dans '{output_dir}/' avec n'importe quel lecteur audio.")
    print("Astuce : les deux sens d'une même conversation sont 2 fichiers séparés")
    print("(un pour chaque direction) — c'est normal, RTP fonctionne en 2 flux distincts.")


if __name__ == "__main__":
    main()
