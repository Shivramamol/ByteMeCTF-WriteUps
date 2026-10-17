#!/usr/bin/env python3
"""
Soul Echoes: The Stonekeeper's Chronicle - Solver
Author: Suyog Jadhav
Category: Reverse Engineering (Easy)
"""

import os
import re
import sys
from pwn import *

def solve_dynamic(binary_path="./rev/soul_echo/dist/soul_echo"):
    """Solves the challenge dynamically by selecting Chapter III."""
    try:
        p = process(binary_path)
        p.recvuntil(b"Choose your path (1-5): ")
        p.sendline(b"3")  # Option 3: Read Chapter III
        output = p.recvall(timeout=2).decode(errors="ignore")
        match = re.search(r"OWASP\{[a-zA-Z0-9_]+\}", output)
        if match:
            return match.group(0)
    except Exception as e:
        print(f"[-] Dynamic execution error: {e}")
    return None

def solve_static(binary_path="./rev/soul_echo/dist/soul_echo"):
    """Scans the ELF binary for the flag regex pattern."""
    if not os.path.exists(binary_path):
        return None
    with open(binary_path, "rb") as f:
        data = f.read()
    match = re.search(rb"OWASP\{[a-zA-Z0-9_]+\}", data)
    if match:
        return match.group(0).decode()
    return None

def main():
    print("[*] Soul Echoes Solver")
    
    # 1. Static extraction
    target = "./rev/soul_echo/dist/soul_echo"
    flag = solve_static(target)
    if flag:
        print(f"[+] Statically Extracted Flag: {flag}")
        return

    # 2. Dynamic execution
    dynamic_flag = solve_dynamic(target)
    if dynamic_flag:
        print(f"[+] Dynamically Recovered Flag: {dynamic_flag}")
    else:
        print("[-] Flag recovery failed.")

if __name__ == "__main__":
    main()
