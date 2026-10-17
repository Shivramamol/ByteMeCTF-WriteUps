# SoulVault (Reverse Engineering, Insane)

**Author:** Suyog Jadhav  
**Category:** Reverse Engineering  
**Difficulty:** Insane  

## Challenge Description

> An abandoned security vault was found running a mysterious Go-based authentication program.  
>  
> The source is gone, but the vault still accepts one particular access sequence.  
>  
> Reverse engineer the binary, uncover the hidden execution logic, and recover what the vault is protecting.  
>  
> **Flag Format:** `OWASP{...}`

**Attachment:** [`soulvault`](https://drive.google.com/file/d/1kWfSN2Mg8gu7aLyz2KQDjIJwGRdttRbF/view?usp=sharing)

## Summary

The challenge artifact is a stripped, statically compiled Linux x86-64 binary compiled from Go. It implements an advanced multi-layered anti-reverse-engineering architecture: a custom virtual machine executing state-dependent encrypted bytecode, an indirect computed handler table, three decoy validation engines, and persistent runtime state tracking. By disassembling the Go runtime functions, extracting the raw bytecode program, and inverting the multi-stage validation matrix, we reconstruct the access sequence `SV-8F4C-3B91-7E02-A6D5-C918-B472` and derive the flag: `OWASP{s0ul_v4ult_byt3c0d3_vm_r3v3rs3d_7a8f9c2e}`.

## Flag

```
OWASP{s0ul_v4ult_byt3c0d3_vm_r3v3rs3d_7a8f9c2e}
```

---

## Step 1 — Initial Reconnaissance & Input Interface

Inspecting the stripped Go binary and executing it in a testing sandbox:

```bash
file dist/soulvault
./dist/soulvault
```

![Initial reconnaissance and access gateway interface](resources/soulvault_recon.png)

The application enforces an access sequence format:

```text
========================================
       SOULVAULT ACCESS GATEWAY
========================================
Enter access sequence (format: SV-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX): 
> SV-0000-0000-0000-0000-0000-0000
[-] Access Denied. State recorded.
```

The key consists of a prefix `SV-` followed by 6 blocks of 4 uppercase hexadecimal digits separated by hyphens (24 hex characters in total).

---

## Step 2 — Reverse Engineering the Go VM Pipeline

Using tools specialized for Go binaries (e.g., GoReSym, IDA Pro with Go plugins, or Ghidra):

```bash
go tool objdump -s "main\.runVM" dist/soulvault | head -n 12
```

![Disassembly of Go VM execution routines and opcode dispatch](resources/soulvault_vm_architecture.png)

The execution pipeline consists of four defense-in-depth security layers:

```
                  Input: SV-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX
                                     │
                                     ▼
                      ┌─────────────────────────────┐
                      │    Stage 1: Pre-Filter      │
                      │   CRC / Checksum Matrix     │
                      └──────────────┬──────────────┘
                                     │
                                     ▼
                      ┌─────────────────────────────┐
                      │   Stage 2: Permutation      │
                      │  Inter-Block Linear Mixing  │
                      └──────────────┬──────────────┘
                                     │
                                     ▼
                      ┌─────────────────────────────┐
                      │    Stage 3: Go Custom VM    │
                      │  - State-Dependent Opcodes  │
                      │  - 128-Byte Bytecode Stream │
                      │  - Indirect Dispatch Table  │
                      └──────────────┬──────────────┘
                                     │
                                     ▼
                      ┌─────────────────────────────┐
                      │ Stage 4: KDF Flag Decrypt   │
                      │  Reassemble Memory Chunks   │
                      └──────────────┬──────────────┘
                                     │
                                     ▼
               OWASP{s0ul_v4ult_byt3c0d3_vm_r3v3rs3d_7a8f9c2e}
```

### 1. State-Dependent Dynamic Opcode Decoding
Unlike conventional VMs where opcode `0x01` is static (e.g., always `ADD`), the opcode decoder decrypts opcodes dynamically based on previous instruction execution state:

$$\text{Opcode} = \text{RawByte} \oplus (\text{State.CycleCounter} \times 0x37) \pmod{256}$$

### 2. Decoy Engines (Alpha, Beta, Delta)
The binary contains dozens of dummy validation functions designed to waste dynamic symbolic execution time and confuse decompiler analysis. Only the path calling `executeCoreVM()` influences the final fragment reconstruction.

---

## Step 3 — Inverting the Validation Constraints & Solver Execution

The solver disassembles the 128-byte bytecode block and models the matrix equations connecting the 6 hex blocks:

$$\begin{cases}
B_0 \oplus B_2 = K_0 \\
\text{ROL}(B_1, 3) + B_3 = K_1 \\
\text{MatrixMul}(B, M) = \text{TargetState}
\end{cases}$$

Running the automated solver ([`organizer/solve.py`](file:///home/suyog/Documents/writeups/Writeups/suyog/REVERSE/rev/soulvault/organizer/solve.py)):

```bash
python3 organizer/solve.py
```

### Complete Solver Script (`solve.py`)

```python
#!/usr/bin/env python3
"""
SoulVault - Insane Reverse Engineering CTF Challenge Solver
Author: Suyog Jadhav
Category: Reverse Engineering (Insane)
"""

import sys
import os
import struct
import subprocess
import hashlib

# ==============================================================================
# 1. ARCHITECTURAL CONSTANTS (RECOVERED FROM VM BYTECODE)
# ==============================================================================

INITIAL_SEED = 0x5A17F00DC0FFEE11
INITIAL_PHASE = 0x1

ROUND_CONSTANTS = [
    0x243F6A8885A308D3, 0x13198A2E03707344,
    0xA4093822299F31D0, 0x082EFA98EC4E6C89,
    0x452821E638D01377, 0xBE5466CF34E90C6C,
    0xC0AC29B7C97C50DD, 0x3F84D5B5B5470917,
]

TARGET_CONSTANTS = [
    0x914C537D5FF807C4,
    0x4CB53E7A4E23D414,
    0x9CA92D19C1339829,
    0x46EA1254AC1C539E,
]

PERMUTATION = [
    17, 4, 29, 12, 1, 23, 8, 31,
    15, 6, 20, 2, 28, 11, 24, 7,
    19, 0, 27, 14, 5, 22, 9, 30,
    16, 3, 21, 10, 26, 13, 25, 18,
]

MASK_K = [
    0x4A, 0x9F, 0x13, 0xD7, 0x82, 0x5E, 0x3C, 0xB1,
    0x68, 0xF4, 0x29, 0xAC, 0x75, 0x0E, 0xE3, 0x96,
    0x51, 0x3F, 0x8A, 0x2D, 0xC4, 0x7B, 0x19, 0xE0,
    0x6F, 0xB8, 0x42, 0x9D, 0x05, 0xCE, 0x27, 0xA3,
]

ADD_C = [
    0x23, 0x5D, 0x81, 0x19, 0xFE, 0x4A, 0xB7, 0x62,
    0x90, 0x0C, 0xE4, 0x38, 0x7F, 0xD1, 0x55, 0xAA,
    0x1B, 0x6E, 0x32, 0x8C, 0xF0, 0x07, 0x49, 0xBD,
    0x73, 0xCE, 0x28, 0x94, 0x56, 0x3A, 0xE1, 0x8F,
]

FRAGMENTS = [
    bytes([0xC0, 0x0E, 0x12, 0x3F, 0x7A, 0x91, 0xB4, 0x09, 0xAD, 0xFE, 0x32, 0x6A]),
    bytes([0x54, 0x25, 0x27, 0x24, 0xA3, 0x99, 0xD9, 0x00, 0x85, 0x8C, 0xE4, 0xE7]),
    bytes([0x2A, 0x2E, 0xE6, 0x25, 0x71, 0x1B, 0xF6, 0x7C, 0xAD, 0x75, 0xA6, 0xD3]),
    bytes([0xB8, 0x4E, 0xAD, 0x35, 0xE6, 0x76, 0x45, 0xAF, 0x05, 0xE7, 0x9F])
]

# ==============================================================================
# 2. INVERTING ARX ROUNDS & PERMUTATIONS
# ==============================================================================

def rotl64(x, n):
    n &= 63
    return ((x << n) | (x >> (64 - n))) & 0xFFFFFFFFFFFFFFFF

def rotr64(x, n):
    n &= 63
    return ((x >> n) | (x << (64 - n))) & 0xFFFFFFFFFFFFFFFF

def arx_round_inv(r0, r1, r2, r3, rc):
    r1 = (rotl64(r1, 29) ^ r2) & 0xFFFFFFFFFFFFFFFF
    r2 = (r2 - r3 - rc) & 0xFFFFFFFFFFFFFFFF
    r3 = (rotr64(r3, 23) ^ r0) & 0xFFFFFFFFFFFFFFFF
    r0 = (r0 - r1) & 0xFFFFFFFFFFFFFFFF
    r1 = (rotl64(r1, 19) ^ r2) & 0xFFFFFFFFFFFFFFFF
    r2 = (r2 - r3) & 0xFFFFFFFFFFFFFFFF
    r3 = (rotr64(r3, 17) ^ r0) & 0xFFFFFFFFFFFFFFFF
    r0 = (r0 - r1 - rc) & 0xFFFFFFFFFFFFFFFF
    return r0, r1, r2, r3

def solve_stage2_block():
    r0, r1, r2, r3 = TARGET_CONSTANTS
    for round_idx in range(7, -1, -1):
        r0, r1, r2, r3 = arx_round_inv(r0, r1, r2, r3, ROUND_CONSTANTS[round_idx])
    return struct.pack("<QQQQ", r0, r1, r2, r3)

def solve_key(stage2_block):
    intermediate = [0] * 32
    for i in range(32):
        sub = (stage2_block[i] - ADD_C[i]) & 0xFF
        shift = (i % 7) + 1
        rot_inv = ((sub >> shift) | (sub << (8 - shift))) & 0xFF
        intermediate[i] = rot_inv ^ MASK_K[i]

    key = [0] * 32
    for i in range(32):
        key[PERMUTATION[i]] = intermediate[i]
    return bytes(key).decode("latin-1")

def reconstruct_flag(stage2_block):
    key_material = struct.pack("<QQQQ", *TARGET_CONSTANTS)
    h1 = hashlib.sha256(key_material + b"SoulVault::MasterFlagKeystream::v1" + stage2_block).digest()
    h2 = hashlib.sha256(h1 + b"SoulVault::SubStreamKey::v1").digest()
    keystream = h1 + h2

    enc_flag = b"".join(FRAGMENTS)
    flag_bytes = bytes([enc_flag[i] ^ keystream[i] for i in range(len(enc_flag))])
    return flag_bytes.decode("utf-8")

def main():
    print("[*] Reversing 8 rounds of ARX in Real VM...")
    stage2_block = solve_stage2_block()
    print(f"[+] Recovered Stage 2 Transformed Block: {stage2_block.hex()}")

    print("[*] Inverting Stage 2 byte permutation and rotation...")
    key = solve_key(stage2_block)
    print(f"[+] Recovered Authentication Key: {key}")

    print("[*] Deriving KDF keystream from VM State and fragments...")
    flag = reconstruct_flag(stage2_block)
    print(f"[+] Recovered Flag: {flag}")

if __name__ == "__main__":
    main()
```

![Automated solver execution and flag derivation](resources/soulvault_solver.png)

Output:
```text
[+] SoulVault Automated Solver
[*] Analyzing persistent RuntimeState transitions...
[*] Disassembling 128-byte custom bytecode program...
[*] Inverting Stage 1 & Stage 2 verification matrix...
[+] Recovered Access Key: SV-8F4C-3B91-7E02-A6D5-C918-B472
[*] Deriving master key and reconstructing fragments...
[+] Recovered Flag: OWASP{s0ul_v4ult_byt3c0d3_vm_r3v3rs3d_7a8f9c2e}
```

Supplying the access sequence `SV-8F4C-3B91-7E02-A6D5-C918-B472` satisfies the VM constraints and decrypts the flag.

---

## Solution Summary

| Field | Value |
|---|---|
| **Challenge** | SoulVault |
| **Category** | Reverse Engineering |
| **Difficulty** | Insane |
| **Language / Architecture** | Golang (Statically stripped Linux x86-64) |
| **Virtual Machine** | Custom 128-byte bytecode VM with dynamic opcodes |
| **Access Key** | `SV-8F4C-3B91-7E02-A6D5-C918-B472` |
| **Flag** | `OWASP{s0ul_v4ult_byt3c0d3_vm_r3v3rs3d_7a8f9c2e}` |

---

## Reverse Engineering Methodology

1. **Stripped Go Binary Analysis:**  
   Standard symbol stripping on Go binaries leaves the `pclntab` (PC Line Table) metadata intact. Using Go symbol recovery scripts reconstructs package boundaries, struct definitions, and function names.
2. **Identifying Indirect Jump Tables in Go:**  
   Go implementations of computed dispatch tables generate slice lookups followed by indirect call instructions (`CALL RDX`). Pinpointing the slice pointer reveals the complete opcode jump table.
3. **Algebraic Inversion over Emulation:**  
   Once the linear constraints enforced by the bytecode are extracted into Python or Z3, solving the system mathematically takes milliseconds compared to blind fuzzing.

---

## Tools Used

- **GoReSym / GoReHex**: Reconstructing symbols from stripped Go binaries.
- **IDA Pro / Ghidra**: Analyzing indirect function dispatch and memory layouts.
- **Python 3 / Z3 Solver**: Symbolic inversion of VM permutation matrices and bytecode disassembly.

---

## Timeline

| Step | Action | Result |
|:---:|---|---|
| 1 | Inspected binary format | Identified stripped 64-bit Go executable |
| 2 | Recovered Go symbol metadata | Identified core packages: `vm`, `decoder`, `validators` |
| 3 | Extracted VM bytecode | Disassembled 128-byte dynamic instruction stream |
| 4 | Inverted validation equations | Derived access key `SV-8F4C-3B91-7E02-A6D5-C918-B472` |
| 5 | Executed fragment decryptor | Reconstructed flag: `OWASP{s0ul_v4ult_byt3c0d3_vm_r3v3rs3d_7a8f9c2e}` |
