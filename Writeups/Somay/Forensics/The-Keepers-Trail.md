# The Keeper's Trail

**Category:** Crypto / Forensics | **Difficulty:** Medium | **Flag format:** `OWASP{...}` | **Author:** Somay Rathod

## Challenge Premise

Solvers receive a single aged-parchment image styled as a letter from Vormir, signed off by the number **3061**, and closing with the line *"Perhaps you are the one."* Nothing in the letter explicitly says there's more to find - the challenge rewards close reading and curiosity.


## Step 1 - Read the letter carefully

The external letter is the only thing given up front. Its Vormir flavor text carries two pieces of real data disguised as flourish:

- The sign-off, **"regards, 3061"**, is **prime #1**.
- The repeated reference to **Vormir** as the location/theme is the secret word later needed as a decryption key - nothing marks it as a password, it just has to be recognized as significant.

```
$ file letter.png
letter.png: PNG image data, ...
```

## Step 2 - Check the image for a plain-sight clue

Running basic string/metadata extraction on the image surfaces a `tEXt` chunk the viewer won't see:

```
$ exiftool -tEXt:all letter.png
# or
$ strings letter.png | less
```

The embedded text congratulates the solver for looking closely, hints to "peel back the layers" (pointing at LSB steganography), reminds them the key came from the letter, and separately flags that a locked PDF exists and will need whatever is found beneath those layers.

## Step 3 - Extract the hidden layer (LSB steganography)

Standard, zsteg-detectable LSB embedding (no custom bit order) pulls out an AES-256-CBC-encrypted blob rather than a usable file directly:

```
$ zsteg -a letter.png
b1,r,lsb,xy  .. text: "<hex-encoded IV+ciphertext>"
```

Decrypting requires recognizing the only "key-shaped" thing given so far - the word from the letter:

```python
import hashlib
from Crypto.Cipher import AES

blob   = bytes.fromhex("<extracted hex>")
iv, ct = blob[:16], blob[16:]
key    = hashlib.sha256(b"Vormir").digest()
pt     = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)   # strip PKCS7 padding
```

The decrypted bytes are a PNG - a QR code.

## Step 4 - Scan the QR code

Scanning the recovered QR image yields a plaintext string:

```
FewerReturns
```

This reads like flavor text on its own (it echoes the letter's "Few do. Fewer return." line) but is actually the password for the PDF found next.


## Step 5 - Open the PDF and read the redirect

With the password from Step 4 open it

The unlocked PDF is signed 3061 again (confirming prime #1 was never a red herring), explicitly tells the solver the three primes must be **multiplied together**, and points back to the original image as the place the flag ultimately lives

## Step 6 - Hunt the EXIF metadata for the remaining primes

The image's EXIF block is built on a realistic Nikon-style template padded with several numeric decoy fields. None of them are labeled — the solver has to test each one for primality to separate signal from noise:

```
$ exiftool letter.png
ISO                     : 200   -> not prime (decoy)
SubjectDistance         : 861   -> not prime (3 * 7 * 41, decoy)
FocalLengthIn35mmFormat : 899   -> not prime (29 * 31, decoy)
GPSAltitude             : 703   -> not prime (19 * 37, decoy)
GPSDOP                  : 517   -> not prime (11 * 47, decoy)
FocalLength             : 787   -> PRIME  (prime #2)
ImageNumber             : 941   -> PRIME  (prime #3)
```

A one-liner with `sympy.isprime` across every numeric EXIF field makes this fast; brute-force trial division works too.

## Step 7 - Multiply the primes

```
3061 * 787 * 941 = 2,266,875,587
```

## Step 8 - Decrypt the final flag

The PDF also carries a hex-encoded AES-256-CBC blob. Its key is derived the same way as the QR layer - SHA-256 of the secret, this time the prime product used as a string:

```python
key = hashlib.sha256(b"2266875587").digest()
iv, ct = blob[:16], blob[16:]
pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)   # strip PKCS7 padding
```

## Flag

```
OWASP{YouAreTheOne}
```

The numeric product is the *key*, not the flag - solvers who stop at "2266875587" and submit that as the answer have only done the math, not finished the story.

## Design Notes

- **Four clues, one carrier file:** the letter, the in-image text clue, the LSB/QR payload, and the PDF all had to click together; no clue is solvable in isolation, which is what pushes this from "easy" to "mid-hard."
- **Kerckhoffs's principle, applied on purpose:** the cipher, mode, and key-derivation method (AES-256-CBC, SHA-256 of a narrative secret, random IV prepended to ciphertext, PKCS7 padding) are disclosed openly in the challenge description. Only the secret word and the two hidden primes are actually hidden - the mechanism never is.
- **Why AES over repeating-key XOR:** an earlier draft used repeating-key XOR for both encrypted layers. Both broke immediately under known-plaintext attacks - the PNG magic bytes crib the QR layer's key, and the public `OWASP{` prefix crib the flag layer's key - without the solver ever needing the actual secrets. Switching to AES-256-CBC with a full SHA-256-derived key and random IV closes that shortcut.
- **Decoys earn their keep:** the EXIF decoys are deliberately composite numbers (861, 899, 703, 517) so a solver who doesn't actually check primality and instead guesses "the biggest number" or "the GPS-looking ones" picks wrong.
- **The flag itself is a twist, not a reward for arithmetic:** resolving the final flag as `OWASP{YouAreTheOne}` (pulled from the letter's closing line) rather than the prime product keeps the last step from being "plug numbers into the flag format," consistent with the Cicada-3301 redirect theme running through the whole challenge.

## Tools Used

- `exiftool` / `strings` - metadata and embedded-text extraction
- `zsteg` - LSB steganography extraction
- QR decoder (phone camera or `zbarimg`)
- Python (`hashlib`, `pycryptodome`) - AES-256-CBC decryption
- `sympy.isprime` (or manual trial division) - separating real primes from EXIF decoys

## Summary

The "letter" image is actually three challenges stacked in one file: a hidden text clue readable with basic string extraction, an AES-encrypted QR code hidden via LSB steganography, and two prime numbers buried among decoy fields in the EXIF metadata. Chasing all three leads to a password-protected PDF, which in turn holds an AES-encrypted flag that can only be decrypted once the solver has multiplied three primes together. The final flag, once decrypted, is a short narrative payoff rather than the numeric product itself - a deliberate anti-climax/twist that punishes solvers who stop at "I found the math answer."
