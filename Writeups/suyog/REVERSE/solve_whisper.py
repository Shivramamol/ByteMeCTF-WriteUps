#!/usr/bin/env python3
"""
Soul's Whisper - Automated Solver
Author: Suyog Jadhav
Category: Reverse Engineering (Easy)
"""

import os
import sys
import subprocess
from pwn import *

def solve_dynamic(binary_path="./rev/soul/soul_whisper"):
    """Solves the challenge by interacting with the binary process."""
    try:
        p = process(binary_path)
        p.recvuntil(b"Enter the whisper: ")
        p.sendline(b"soul")
        output = p.recvall(timeout=2).decode(errors="ignore")
        for line in output.splitlines():
            if "OWASP{" in line:
                return line.strip()
    except Exception as e:
        print(f"[-] Dynamic execution error: {e}")
    return None

def solve_static():
    """Extracts and decodes the byte array embedded in soul_stone()."""
    encoded_bytes = [
        0x4F, 0x57, 0x41, 0x53, 0x50, 0x7B, 0x74, 0x68,
        0x33, 0x5F, 0x73, 0x30, 0x75, 0x6C, 0x5F, 0x73,
        0x74, 0x30, 0x6E, 0x33, 0x5F, 0x77, 0x68, 0x31,
        0x73, 0x70, 0x33, 0x72, 0x7D
    ]
    return "".join(chr(b) for b in encoded_bytes)

def main():
    print("[*] Soul's Whisper Solver")
    
    # Static recovery
    static_flag = solve_static()
    print(f"[+] Statically Decoded Flag: {static_flag}")
    
    # Dynamic verification if binary exists
    target = "./rev/soul/soul_whisper"
    if os.path.exists(target):
        dynamic_flag = solve_dynamic(target)
        if dynamic_flag:
            print(f"[+] Dynamically Recovered Flag: {dynamic_flag}")

if __name__ == "__main__":
    main()
