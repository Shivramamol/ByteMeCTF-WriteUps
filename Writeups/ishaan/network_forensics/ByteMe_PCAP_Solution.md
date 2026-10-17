# ByteMe CTF 2026 — The Soul Stone Intercept (Network & File Forensics / Steganography, Medium-Hard)

**Author:** Ishaan Jog
**Category:** Network Forensics / File Forensics / Steganography
**Difficulty:** Medium

---

## Challenge Description

Long-range scanners aboard Thanos's flagship, Sanctuary II, intercepted an anomalous network stream exchanged between an operative terminal and the mystical Altar of Vormir. The cursed guardian, Johann Schmidt (Red Skull), guards the relic and enforces the cosmic rule: "I guide others to a treasure I cannot possess. A soul for a soul."

Following Gamora's sacrifice, an extraction attempt was initiated, but the altar sealed into dormancy before the coordinates could be confirmed. Analyze the captured transmission (`soul_stone_intercept.pcap`), bypass the illusions of Vormir, and claim the true Soul Stone flag.

**Challenge File:** `soul_stone_intercept.pcap`
**Flag Format:** `OWASP{...}`

## Flag

```
OWASP{v0rm1r_s0ul_sacr1f1c3_849201}
```

---

## Summary

The challenge requires participants to analyze a network packet capture containing mixed HTTP, ICMP, DNS, UDP, and TLS traffic. Contestants must extract a compressed archive (`vormir_vault.tar.gz`) transferred over an unencrypted HTTP POST session on port 8080.

Decompressing the archive yields a visual artifact (`soul_stone_sigil.png`). Contestants must apply Least Significant Bit (LSB) steganography analysis (using StegSolve, Aphotens, or Python) to uncover a hidden inscription embedded in the image's color planes.

The hidden inscription reveals a decoy flag (`OWASP{n0t_th3_tru3_s0ul_839210}`) marked as rejected, along with an MCU Vormir Lore Riddle:

> "The key to the void is the name of the daughter who fell, written backwards, concatenated with her adopted order among Thanos's children, and salted with the Covert UDP Port in decimal."

Deducing the riddle (Gamora reversed = `aromaG` + 1st daughter = `1` + UDP Port = `1337`) yields the repeating XOR key `aromaG11337`. Finally, contestants extract the application payload from sequential covert UDP packets (`udp.dport == 1337`) and decrypt the stream to claim the true flag: `OWASP{v0rm1r_s0ul_sacr1f1c3_849201}`.

---

## Recon

Opening `soul_stone_intercept.pcap` in Wireshark or running protocol hierarchy statistics:

```bash
tshark -r soul_stone_intercept.pcap -q -z io,phs
```

reveals the protocol breakdown:

- **DNS (UDP 53):** Queries resolving `gateway.vormir.sanctuary.internal` to `198.51.100.108` and `telemetry.titan-fleet.mil` to `203.0.113.50`.
- **TCP (Port 8080):** Full 3-way handshake and subsequent HTTP transfer between Thanos's terminal (`10.42.13.37`) and the Vormir Altar (`198.51.100.108`).
- **UDP (Port 1337):** Covert traffic stream between `10.42.13.37` and `198.51.100.108`.
- **ICMP:** Benign gateway pings to `8.8.8.8`.
- **TLS (Port 443):** Background encrypted telemetry sessions to external servers (`203.0.113.50`).

The unencrypted HTTP transfer on port 8080 immediately indicates an application layer transfer.

---

## Step 1 — Inspect the HTTP Exchange on Port 8080

Filtering for `http` or `tcp.port == 8080` in Wireshark reveals:

**Client POST Request:**

```http
POST /vormir/altar/v1/extract HTTP/1.1
Host: gateway.vormir.sanctuary.internal:8080
User-Agent: Sanctuary-Vanguard/3.14 (Titan-OS; ARM64)
Authorization: Bearer SACRIFICE_VERIFIED_GAMORA_ZEN_WHOBERI
Content-Length: 72
Connection: close

{"request": "soul_stone_vault_manifest", "bearer": "thanos_vanguard"}
```

**Server Response:**

```http
HTTP/1.1 200 OK
Server: Vormir-Altar-Daemon/1.0 (Spectral-OS)
Content-Type: application/x-tar-gz
Content-Disposition: attachment; filename="vormir_vault.tar.gz"
X-Vormir-Inscription: "A soul for a soul. The Stone demands sacrifice."
Content-Length: 71156
Connection: close
```

The response delivers a gzip-compressed archive named `vormir_vault.tar.gz`.

---

## Step 2 — Carve the Archive from the Packet Capture

**Method A — Wireshark GUI:**

1. Navigate to: **File -> Export Objects -> HTTP...**
2. Select the object `vormir_vault.tar.gz`.
3. Click **Save** to write the file locally.

**Method B — Linux CLI (tshark):**

```bash
tshark -r soul_stone_intercept.pcap --export-objects "http,carved_vault"
cd carved_vault
file %5cvormir%5caltar%5cv1%5cextract
mv %5cvormir%5caltar%5cv1%5cextract vormir_vault.tar.gz
```

Verify archive integrity:

```bash
file vormir_vault.tar.gz
```

---

## Step 3 — Extract and Inspect the Artifact (`soul_stone_sigil.png`)

Decompressing `vormir_vault.tar.gz`:

```bash
tar -xzvf vormir_vault.tar.gz
```

Output:

```text
soul_stone_sigil.png
```

Unlike classic CTF challenges with plain-text manifest logs, the archive contains a single visual artifact: `soul_stone_sigil.png`.

Opening the image shows a cosmic obsidian altar surrounded by amber Soul Stone glyphs and the inscribed quote:

> "I guide others to a treasure I cannot possess. A soul for a soul."

Running `strings` or `exiftool` on the file reveals no hidden strings or metadata anomalies—indicating steganographic concealment inside the pixel data.

---

## Step 4 — Steganography Analysis: Inspecting Color Planes (LSB)

Because PNG uses lossless compression, the Least Significant Bit (LSB) of RGB pixel channels can encode hidden data.

**Method A — StegSolve GUI:**

1. Open `soul_stone_sigil.png` in StegSolve.
2. Click the bottom `<` or `>` arrow buttons to cycle through the color bit planes.
3. Advance to **Red Plane 0**.

The visual bitplane displays a sharp, high-contrast monochrome inscription:

```text
================== [ALTAR OF VORMIR : SPECTRAL SIGIL] ==================
PROVISIONAL TOKEN: OWASP{n0t_th3_tru3_s0ul_839210}  [STATUS: REJECTED BY THE STONE]
VERDICT: A phantom token. The true coordinates are sealed in the void.
RIDDLE OF THE VOID:
"The key to the void is the name of the daughter who fell,
written backwards, concatenated with her adopted order
among Thanos's children, and salted with the Covert UDP Port in decimal."
RESONANCE STREAM: Covert UDP Traffic (Destination Port: 1337)
```

**Method B — Python LSB Extraction Script:**

Contestants can extract either the visual plane or the sequential Green LSB data stream:

```python
from PIL import Image

img = Image.open("soul_stone_sigil.png")

# 1. Visual Red Plane 0
red_0 = img.getchannel("R").point(lambda p: (p & 1) * 255)
red_0.save("red_plane_0.png")

# 2. Sequential Green LSB Stream
w, h = img.size
pix = img.load()
bits = [pix[x, y][1] & 1 for y in range(h) for x in range(w)]
raw_bytes = bytearray()
for i in range(0, len(bits) - 7, 8):
    byte = 0
    for b in range(8):
        byte = (byte << 1) | bits[i + b]
    if byte == 0:
        break
    raw_bytes.append(byte)
print(raw_bytes.decode("utf-8", errors="ignore"))
```

---

## Step 5 — Decipher the MCU Vormir Lore Riddle

The steganographic inscription provides:

**The Decoy Flag:** `OWASP{n0t_th3_tru3_s0ul_839210}`.

**The Riddle:**

> "The key to the void is the name of the daughter who fell, written backwards, concatenated with her adopted order among Thanos's children, and salted with the Covert UDP Port in decimal."

**Semantic Deduction:**

- Daughter who fell on Vormir: Gamora
- Written backwards: `aromaG`
- Adopted order among Thanos's children: Gamora was the first adopted child (eldest daughter = 1; Nebula was second).
- Covert UDP Port in decimal: `1337`.
- Combined Key: `aromaG` + `1` + `1337` = `aromaG11337`

The repeating XOR decryption key is:

```text
aromaG11337
```

---

## Step 6 — Extract Covert UDP Stream & Decrypt the True Flag

**Method A — CyberChef (Easiest GUI Method):**

1. In Wireshark, filter for `udp.dport == 1337`.
2. Right-click any packet -> **Follow** -> **UDP Stream**.
3. Switch "Show data as" to **Hex Dump** (or Raw).
4. Copy the payload bytes and paste into CyberChef.
5. Apply operations:
   - `From Hex`
   - `XOR` (Key: `aromaG11337`, Scheme: UTF-8)

**Method B — CLI (tshark + Python):**

Extract raw stream bytes:

```bash
tshark -r soul_stone_intercept.pcap -Y "udp.dport == 1337" -T fields -e udp.payload | tr -d '\n' > encrypted_stream.hex
```

Decrypt using Python:

```python
import binascii

with open("encrypted_stream.hex", "r") as f:
    enc_data = binascii.unhexlify(f.read().strip())

key = b"aromaG11337"
decrypted = bytes([b ^ key[i % len(key)] for i, b in enumerate(enc_data)])
print(decrypted.decode("utf-8"))
```

**Decrypted Output:**

```text
[ALTAR OF VORMIR - SOUL STONE RESONANCE HARMONIZED]
Red Skull: "I guide others to a treasure I cannot possess. A soul for a soul.
Take the stone and weep for what it cost."
COSMIC_SECTOR: VORMIR_CLIFF_APEX_616
TRUE_FLAG: OWASP{v0rm1r_s0ul_sacr1f1c3_849201}
```

---

## Flag

```text
OWASP{v0rm1r_s0ul_sacr1f1c3_849201}
```

---

## Forensic Mechanics & Root Cause

- **Cleartext Data Exfiltration:** HTTP port 8080 transmitted the initial asset unencrypted, enabling trivial HTTP object carving.
- **Visual Bitplane Steganography:** The payload hid critical telemetry inside the Least Significant Bit (LSB) of PNG pixel channels, evading basic ASCII and raw-byte string scanners.
- **Covert UDP Tunneling:** Normal network monitors inspect standard ports but ignore arbitrary high-numbered UDP payloads. The rogue terminal hijacked destination UDP port 1337 to tunnel encrypted coordinates.
- **Semantic Lore Derivation:** The challenge enforces multi-modal human reasoning (network forensics -> file carving -> visual steganography -> narrative riddle deduction -> XOR stream decryption) that resists automated LLM scraping.