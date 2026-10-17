#!/usr/bin/env python3
"""
Sanity Check - Automated Solver
Author: Suyog Jadhav
Category: Misc / OSINT (Easy)
"""

import base64

def solve():
    payload_b64 = "RV1LWVpxfTlmSTpnOVV+OlVIc345RzlVSX5sVThlODx3"
    
    print("[*] Decoding Base64 payload...")
    raw_bytes = base64.b64decode(payload_b64)
    
    print("[*] Applying XOR decryption with key 0x0A...")
    xor_key = 0x0A
    flag = bytes([b ^ xor_key for b in raw_bytes]).decode("utf-8", errors="ignore")
    
    print(f"[+] Recovered Flag: {flag}")
    return flag

if __name__ == "__main__":
    solve()
