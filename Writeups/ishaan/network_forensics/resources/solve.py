#!/usr/bin/env python3
"""
ByteMe CTF 2026 - Official Verification / Solver Script
Challenge Name: The Soul Stone Intercept
Category: Network Forensics / File Forensics / Steganography
"""

import io
import tarfile
from PIL import Image
from scapy.all import rdpcap, TCP, UDP, Raw

PCAP_FILE = "soul_stone_intercept.pcap"

def solve():
    print(f"[*] Loading '{PCAP_FILE}'...")
    packets = rdpcap(PCAP_FILE)
    print(f"[*] Loaded {len(packets)} packets.")

    # -------------------------------------------------------------------------
    # STAGE 1: Reconstruct HTTP Stream & Extract 'vormir_vault.tar.gz'
    # -------------------------------------------------------------------------
    print("\n[+] Stage 1: Inspecting TCP streams on port 8080...")
    http_data = bytearray()
    for pkt in packets:
        if pkt.haslayer(TCP) and pkt.haslayer(Raw):
            if pkt[TCP].sport == 8080:
                http_data.extend(pkt[Raw].load)

    header_end = http_data.find(b"\r\n\r\n")
    if header_end == -1:
        raise ValueError("Could not find HTTP header delimiter in stream.")

    headers = http_data[:header_end].decode("utf-8", errors="ignore")
    archive_raw = bytes(http_data[header_end + 4:])
    print("[*] HTTP Response Headers recovered:")
    for line in headers.splitlines():
        if "X-Vormir" in line or "Content-Disposition" in line or "Content-Length" in line:
            print(f"    | {line}")

    if archive_raw[:2] != b"\x1f\x8b":
        raise ValueError("Extracted payload is not a valid gzip archive.")
    print(f"[+] Successfully carved 'vormir_vault.tar.gz' ({len(archive_raw)} bytes).")

    # -------------------------------------------------------------------------
    # STAGE 2: Extract 'soul_stone_sigil.png' & Perform Steganography
    # -------------------------------------------------------------------------
    print("\n[+] Stage 2: Extracting artifact from 'vormir_vault.tar.gz'...")
    sigil_bytes = None
    with tarfile.open(fileobj=io.BytesIO(archive_raw), mode="r:gz") as tar:
        for member in tar.getmembers():
            print(f"    - Extracted: {member.name} ({member.size} bytes)")
            if member.name == "soul_stone_sigil.png":
                sigil_bytes = tar.extractfile(member).read()

    if not sigil_bytes:
        raise FileNotFoundError("Could not find 'soul_stone_sigil.png' inside archive.")

    sigil_img = Image.open(io.BytesIO(sigil_bytes))
    w, h = sigil_img.size
    print(f"[*] Sigil dimensions: {w}x{h}, Mode: {sigil_img.mode}")

    # LSB Extraction (Green Channel)
    g_pix = sigil_img.load()
    extracted_bits = []
    for y in range(h):
        for x in range(w):
            extracted_bits.append(g_pix[x, y][1] & 1)

    extracted_bytes = bytearray()
    for i in range(0, len(extracted_bits) - 7, 8):
        byte_val = 0
        for bit_i in range(8):
            byte_val = (byte_val << 1) | extracted_bits[i + bit_i]
        if byte_val == 0:
            break
        extracted_bytes.append(byte_val)

    steg_text = extracted_bytes.decode("utf-8", errors="ignore")
    print("\n[+] Steganographic Message Recovered from Sigil:")
    print("------------------------------------------------------------------------")
    print(steg_text.strip())
    print("------------------------------------------------------------------------")

    # -------------------------------------------------------------------------
    # STAGE 2.5: MCU Lore Riddle Deduction
    # -------------------------------------------------------------------------
    daughter = "Gamora"
    reversed_name = daughter[::-1]   # "aromaG"
    adopted_order = "1"              # Gamora = 1st daughter
    port_hex = "1337"                # Port 1337
    derived_key = f"{reversed_name}{adopted_order}{port_hex}"
    
    print(f"\n[!] DERIVED XOR KEY: {derived_key}")

    # -------------------------------------------------------------------------
    # STAGE 3: Extract Covert UDP Stream (Dst Port: 1337) & Decrypt
    # -------------------------------------------------------------------------
    print("\n[+] Stage 3: Filtering UDP stream (Destination Port: 1337)...")
    udp_packets = []
    for pkt in packets:
        if pkt.haslayer(UDP) and pkt.haslayer(Raw):
            if pkt[UDP].dport == 1337:
                udp_packets.append(pkt)

    # Sort chronologically by packet timestamp
    udp_packets.sort(key=lambda p: float(p.time))
    print(f"[*] Found {len(udp_packets)} covert UDP packets.")

    encrypted_stream = bytearray()
    for pkt in udp_packets:
        encrypted_stream.extend(pkt[Raw].load)

    key = derived_key.encode("utf-8")
    decrypted_stream = bytes([b ^ key[i % len(key)] for i, b in enumerate(encrypted_stream)])
    decrypted_text = decrypted_stream.decode("utf-8")

    print("\n[+] Decrypted Soul Stone Message:")
    print("========================================================================")
    print(decrypted_text.strip())
    print("========================================================================")

    for line in decrypted_text.splitlines():
        if "TRUE_FLAG:" in line:
            true_flag = line.split("TRUE_FLAG:")[1].strip()
            print(f"\n[FLAG] TRUE SOUL STONE FLAG: {true_flag}")
            return true_flag

if __name__ == "__main__":
    solve()