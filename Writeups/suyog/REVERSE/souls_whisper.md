# Soul's Whisper (Reverse Engineering, Easy)

**Author:** Suyog Jadhav  
**Category:** Reverse Engineering  
**Difficulty:** Easy  

## Challenge Description

> The Soul Stone has locked away a secret, but the stone only recognizes the right soul.  
>  
> Analyze the given executable, uncover how it validates the input, and retrieve the hidden flag.  
>  
> **Flag Format:** `OWASP{...}`

**Attachment:** [`soul_whisper`](https://drive.google.com/file/d/1dOeJLCXdjvs0wnRP5aekUo4L27BPlo_a/view?usp=sharing)

## Summary

The challenge provides an unstripped 64-bit ELF executable (`soul_whisper`). Running dynamic tracing (`ltrace`) or static string inspection reveals a direct `strcmp` comparison against the passphrase `"soul"`. Supplying `"soul"` triggers the `soul_stone()` function, which constructs and prints the flag from an array of encoded byte constants.

## Flag

```
OWASP{th3_s0ul_st0n3_wh1sp3r}
```

---

## Step 1 — Binary Reconnaissance & File Inspection

We begin by assessing the file format and binary hardening properties using `file` and `checksec`:

```bash
file soul_whisper
checksec --file=soul_whisper
```

![Binary inspection and checksec properties](resources/whisper_recon.png)

The binary is a standard 64-bit ELF executable compiled with symbols intact (`not stripped`), making static and dynamic analysis straightforward.

---

## Step 2 — String Extraction & Dynamic Tracing

Running `strings` or tracing library calls via `ltrace` exposes the authentication workflow:

```bash
strings soul_whisper | grep -E "stone|soul|phrase"
ltrace ./soul_whisper
```

![String extraction and dynamic library call tracing](resources/whisper_strings.png)

The decompiled logic of `main` verifies user input using standard string comparison:

```c
scanf("%63s", input);
char expected[] = "soul";

if (strcmp(input, expected) == 0) {
    soul_stone();
} else {
    printf("\n[-] The stone rejects your soul.\n");
}
```

When the user enters `"soul"`, the program executes the `soul_stone()` function.

---

## Step 3 — Executing the Binary & Flag Recovery

We execute `./soul_whisper` and provide the passphrase `"soul"`:

```bash
./soul_whisper
```

![Program execution and flag retrieval](resources/whisper_execution.png)

The `soul_stone()` function decodes the byte array:

```c
unsigned char encoded[] = {
    0x4f, 0x57, 0x41, 0x53, 0x50, 0x7b, 0x74, 0x68,
    0x33, 0x5f, 0x73, 0x30, 0x75, 0x6c, 0x5f, 0x73,
    0x74, 0x30, 0x6e, 0x33, 0x5f, 0x77, 0x68, 0x31,
    0x73, 0x70, 0x33, 0x72, 0x7d
};
```

Converting these hex bytes directly to ASCII yields:

```text
OWASP{th3_s0ul_st0n3_wh1sp3r}
```

---

## Step 4 — Automated Solver Script (`solve.py`)

The automated Python solver interacts with the binary dynamically or extracts the encoded byte table statically:

```python
#!/usr/bin/env python3
"""
Soul's Whisper - Automated Solver
Author: Suyog Jadhav
Category: Reverse Engineering (Easy)
"""

import sys
import subprocess
from pwn import *

def solve_dynamic(binary_path="./soul_whisper"):
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
    if os.path.exists("./soul_whisper"):
        dynamic_flag = solve_dynamic("./soul_whisper")
        if dynamic_flag:
            print(f"[+] Dynamically Recovered Flag: {dynamic_flag}")

if __name__ == "__main__":
    main()
```

---

## Solution Summary

| Field | Value |
|---|---|
| **Challenge** | Soul's Whisper |
| **Category** | Reverse Engineering |
| **Difficulty** | Easy |
| **Passphrase** | `soul` |
| **Validation Method** | Direct `strcmp(input, "soul")` |
| **Flag** | `OWASP{th3_s0ul_st0n3_wh1sp3r}` |

---

## Reverse Engineering Methodology

1. **Unstripped Symbol Analysis:**  
   Because symbols and function names are preserved, tools like Ghidra, IDA, or `objdump` immediately reveal high-value targets like `soul_stone()` and `main()`.
2. **Dynamic Call Interception:**  
   Standard C library functions (like `strcmp` and `printf`) can be intercepted using `ltrace` to inspect inputs and target comparison values at runtime without setting up a full debugger.

---

## Tools Used

- **`file` / `checksec`:** Identifying binary architecture and security mitigations.
- **`strings`:** Initial reconnaissance for embedded ASCII strings.
- **`ltrace`:** Dynamic interception of library calls.

---

## Timeline

| Step | Action | Result |
|:---:|---|---|
| 1 | Inspected binary headers | Confirmed 64-bit ELF with PIE enabled and unstripped symbols |
| 2 | Ran `ltrace` on execution | Identified plaintext `strcmp` check against `"soul"` |
| 3 | Provided expected passphrase | Retrieved flag: `OWASP{th3_s0ul_st0n3_wh1sp3r}` |
