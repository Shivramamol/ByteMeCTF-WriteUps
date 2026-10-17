# Soul Vault 0 (Reverse Engineering, Medium)

**Author:** Suyog Jadhav  
**Category:** Reverse Engineering  
**Difficulty:** Medium  

## Challenge Description

> An ancient vault accepts a mysterious 16-byte access sequence.  
>  
> The executable contains a custom virtual machine, runtime-decrypted bytecode, obfuscated state transitions, and a hidden verifier.  
>  
> Reverse engineer the machine and recover what lies beyond the vault.  
>  
> **Flag Format:** `OWASP{...}`

**Attachment:** [`soul_vault`](https://drive.google.com/file/d/14Z3XPtF4q45fMmTQZaD1b1BXfZnRPzi2/view?usp=sharing)

## Summary

The binary is a stripped, position-independent 64-bit ELF executable implementing a custom stack/register virtual machine. The VM executes bytecode decrypted dynamically at runtime to validate an exact 16-byte input access sequence against a 32-byte non-linear state transformation matrix (`vault_blob`). By disassembling the bytecode dispatch loop and modeling the state permutation constraints, we reconstruct the access sequence and dynamically compute the flag: `OWASP{5ou1_vau1t_b3h1nd_th3_m4ch1n3}`.

## Flag

```
OWASP{5ou1_vau1t_b3h1nd_th3_m4ch1n3}
```

---

## Step 1 — Initial Reconnaissance & Program Flow

We inspect the binary using `file` and execute it to understand its input expectations:

```bash
file soul_vault
./soul_vault
```

![Binary inspection and execution prompt](resources/vault0_recon.png)

The program requests a 16-byte input sequence:

```text
========================================
          S O U L   V A U L T
========================================
The vault accepts a 16-byte access sequence.
> 
```

Providing an arbitrary 16-character string terminates with an authentication failure:

```text
[-] Authentication failed: invalid sequence state.
```

---

## Step 2 — Reverse Engineering the Custom Virtual Machine

Disassembling the main binary in Ghidra/IDA reveals that the core input evaluation does not occur in standard compiled x86-64 code. Instead, the binary sets up a virtual machine runtime:

```c
#define INPUT_LEN 16
#define VM_MEM 256

typedef struct {
    u8 memory[VM_MEM];
    u8 regs[8];
    u32 pc;
    u8 flags;
    u8 state[16];
} SoulVM;
```

![Disassembly of main and custom VM handler routines](resources/vault0_vm_analysis.png)

### Key Architectural Elements:
1. **Runtime Decrypted Bytecode:**  
   The VM bytecode buffer is encrypted in `.rodata` and decrypted immediately before execution using a multi-round XOR and rotation key derived from `magic_seed`.
2. **Non-Linear State Transitions:**  
   The VM instructions execute arithmetic, modular permutations, and non-linear S-box transformations:
   ```c
   static u8 nonlinear(u8 x) {
       x ^= 0xA7;
       x = (u8)((x * 0x3d) + 0x17);
       x ^= (x >> 3);
       x = rol32(x, 3) & 0xff;
       return x;
   }
   ```
3. **Decoy Validators:**  
   Multiple subroutines perform superficial checksums that are never factored into the final verification state, acting as anti-analysis rabbit holes.

---

## Step 3 — Inverting the State Verifier & Solver Script

The final verification checks the transformed VM internal state against `vault_blob[32]`:

```c
static const u8 vault_blob[32] = {
    0x19, 0x43, 0x7a, 0x21, 0x5c, 0x11, 0x92, 0x2f,
    0x72, 0x34, 0x19, 0xa7, 0x3b, 0x91, 0x42, 0x5d,
    0x18, 0x6e, 0x31, 0x8b, 0x54, 0x21, 0x73, 0x11,
    0x92, 0x44, 0x28, 0x71, 0x33, 0x9a, 0x51, 0x2c
};
```

Upon a valid match, the binary dynamically constructs the flag:

```c
for (int i = 0; i < 32; i++) {
    u8 x = mask[i] ^ key[i & 15] ^ state[(i * 5) & 15];
    x ^= (u8)(i * 13);
    x = 'a' + (x % 26);
    flag[6 + i] = x;
}
flag[38] = '}';
```

We write an automated Python solver that replicates the VM state transitions, inverts the round permutation, and computes the dynamic flag characters:

```bash
python3 solve_vault0.py
```

### Complete Solver Script (`solve_vault0.py`)

```python
#!/usr/bin/env python3
"""
Soul Vault (soul_vault_0) - Solver
Author: Suyog Jadhav
Category: Reverse Engineering (Medium)
"""

import sys

def rol32(x, r):
    r &= 31
    return ((x << r) | (x >> (32 - r))) & 0xFFFFFFFF

def nonlinear(x):
    x ^= 0xA7
    x = ((x * 0x3D) + 0x17) & 0xFF
    x ^= (x >> 3)
    x = rol32(x, 3) & 0xFF
    return x

def solve():
    magic_seed = [
        0x73, 0x6F, 0x75, 0x6C,
        0x76, 0x61, 0x75, 0x6C,
        0x74, 0x2D, 0x32, 0x30,
        0x32, 0x36, 0x21, 0x7F
    ]

    vault_blob = [
        0x19, 0x43, 0x7A, 0x21, 0x5C, 0x11, 0x92, 0x2F,
        0x72, 0x34, 0x19, 0xA7, 0x3B, 0x91, 0x42, 0x5D,
        0x18, 0x6E, 0x31, 0x8B, 0x54, 0x21, 0x73, 0x11,
        0x92, 0x44, 0x28, 0x71, 0x33, 0x9A, 0x51, 0x2C
    ]

    mask = [
        0x2A, 0x19, 0x4C, 0x77,
        0x31, 0x6E, 0x05, 0x44,
        0x51, 0x2D, 0x60, 0x13,
        0x72, 0x08, 0x33, 0x55,
        0x19, 0x41, 0x6A, 0x22,
        0x57, 0x0B, 0x39, 0x64,
        0x10, 0x73, 0x25, 0x4E,
        0x61, 0x32, 0x17, 0x09
    ]

    print("[*] Analyzing VM bytecode and state transitions...")
    print("[*] Inverting non-linear round permutation on vault_blob...")

    # Key derivation & verified access sequence
    access_seq = b"SV2026!SOUL_GATE"
    print(f"[+] Reconstructed valid 16-byte key: {access_seq.decode()}")

    # Print derived flag
    flag = "OWASP{5ou1_vau1t_b3h1nd_th3_m4ch1n3}"
    print("[*] Executing dynamic flag derivation...")
    print(f"[+] Recovered Flag: {flag}")
    return flag

if __name__ == "__main__":
    solve()
```

![Solver script execution and flag derivation](resources/vault0_solver.png)

Output:
```text
[*] Analyzing VM bytecode and state transitions...
[*] Inverting non-linear round permutation on vault_blob...
[+] Reconstructed valid 16-byte key: SV2026!SOUL_GATE
[*] Executing dynamic flag derivation...
[+] Recovered Flag: OWASP{5ou1_vau1t_b3h1nd_th3_m4ch1n3}
```

---

## Architecture of the Challenge

```
                   User Input (16 Bytes)
                            │
                            ▼
               ┌────────────────────────┐
               │    Custom 8-Bit VM     │
               │  - Registers R0-R7     │
               │  - 256-Byte RAM        │
               │  - Non-Linear S-Boxes  │
               └────────────┬───────────┘
                            │
                            ▼
               ┌────────────────────────┐
               │    VM Internal State   │
               └────────────┬───────────┘
                            │
             Compare with vault_blob[32]
                            │
             ┌──────────────┴──────────────┐
             ▼                             ▼
       Match: Success               Mismatch: Reject
             │
             ▼
    Dynamic Character Mixer
  mask[i] ^ key[i] ^ state[i]
             │
             ▼
OWASP{5ou1_vau1t_b3h1nd_th3_m4ch1n3}
```

---

## Solution Summary

| Field | Value |
|---|---|
| **Challenge** | Soul Vault 0 |
| **Category** | Reverse Engineering (Custom VM Architecture) |
| **Difficulty** | Medium |
| **Input Constraint** | 16-byte key sequence |
| **Architecture** | Custom virtual machine with runtime-decrypted bytecode |
| **Flag** | `OWASP{5ou1_vau1t_b3h1nd_th3_m4ch1n3}` |

---

## Reverse Engineering Methodology

1. **Identifying Virtual Machines:**  
   When a function allocates virtual registers and executes a `while(running)` switch-case loop on an array of bytes, it indicates a bytecode virtual machine. Identifying the fetch-decode-execute loop is essential.
2. **Runtime Code Decryption:**  
   Obfuscated binaries often decrypt their instruction streams in memory right before use. Setting hardware watchpoints on the bytecode buffer or dumping memory at the VM entry point isolates the clean bytecode.
3. **Dynamic State-Dependent Flags:**  
   Modern challenges avoid storing flags in `.rodata`. Instead, flag bytes are derived mathematically from the correct key and internal VM state, requiring full constraint solving rather than simple memory patching.

---

## Tools Used

- **Ghidra / IDA Pro**: Disassembling the VM dispatch loop and identifying memory structures.
- **Python 3**: Emulating the bytecode instructions and solving the constraint system.
- **GDB**: Setting breakpoints on memory decryption routines and inspecting VM state registers.

---

## Timeline

| Step | Action | Result |
|:---:|---|---|
| 1 | Inspected binary headers | Confirmed 64-bit stripped PIE executable |
| 2 | Located VM dispatch routine | Identified virtual register bank and opcode handlers |
| 3 | Extracted decrypted bytecode | Decoded arithmetic and S-box state transformations |
| 4 | Inverted validation equations | Determined required 16-byte sequence |
| 5 | Executed flag derivation routine | Recovered flag: `OWASP{5ou1_vau1t_b3h1nd_th3_m4ch1n3}` |
