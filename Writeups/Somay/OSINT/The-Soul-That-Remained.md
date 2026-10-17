# The Soul That Remained

**Category:** OSINT **Flag format:** `OWASP{...}`

## Challenge Premise

The challenge hands solvers a single image and two lines of flavor text:

> A few thoughts, scattered among the things he had written. And if you find the message, you will still need to understand how he wanted it to be read.

Nothing points directly at a tool or technique — the challenge expects solvers to notice that the first sentence is about *finding* something, and the second is a separate warning that *finding* it won't be enough.

## Summary

The image's EXIF metadata hides both a username and an encrypted flag. Reverse-image-searching the picture leads to the same person's GitHub account, where a personal blog repo delivers the cipher type and a riddle about the key, and a second, unrelated-looking repo's README quietly contains the key itself. Combining the two — Vigenère cipher, key "protonmail" — decrypts the flag.

## Step 1 - Pull the image metadata

```
$ exiftool image.png
Creator : nagi1262
Rights  : What is hidden remembers its key
Comment : DNOLD{fammewzbz_fryaqyh}
```

Three findings, three jobs:

- **Creator** reads like a username, not a real name — worth treating as an OSINT lead.
- **Rights** is oddly phrased for an EXIF field; "remembers its key" is a strong hint the flag below is encrypted with something key-based (Vigenère, XOR, etc.), not just encoded.
- **Comment** is the flag — but in its current form it isn't valid `OWASP{}` content, confirming it's ciphertext.

## Step 2 - Reverse username search

Running the username through a reverse search turns up a GitHub account for **nagi1262**, using the same profile picture. The account has three repositories:

1. `Super-Tic-Tac-Toe`
2. `Random-Thoughts`
3. `C-Notes`

## Step 3 - Read the "Random-Thoughts" repo

This is the one the challenge text was pointing at - *"a few thoughts scattered among the things he had written."* It holds five short pieces of writing. The last one, **"when everything is still - II,"** contains the real clues buried in prose:

- *"Even a piece of writing can hide another meaning inside it."* — confirms the flag is encrypted, not just hidden.
- *"Let one alphabet move against another."* — points specifically at a **Vigenère cipher** (one alphabet shifted against another, letter by letter).
- *"That key is not something you rarely invent — it is something that is already given to you."* — the key isn't meant to be guessed or brute-forced; it already exists somewhere in the solver's hands.
- *"A name, place, or address — where the message belongs — can say more than the message itself."* — the key is tied to an **address** of some kind.

`C-Notes` turns out to be a dead end - clean, nothing relevant.

## Step 4 - Find the key in the other repo

`Super-Tic-Tac-Toe` looks unrelated (a C project), and the code itself is clean - but its **README** contains an email address:

```
nagi1262@protonmail.com
```

That's the "address" the Random-Thoughts clue was pointing to. Stripped of the username, the numbers, and the `.com`, the only purely alphabetical piece of that address is:

```
protonmail
```

which matches the earlier clue that the key is something already given, not invented.

## Step 5 — Decrypt with Vigenère

Decrypting the EXIF comment with key `protonmail` (treating `_` as a pass-through character that doesn't advance the key):

```python
def vigenere_decrypt(ciphertext, key):
    result = []
    ki = 0
    for ch in ciphertext:
        if ch.isalpha():
            shift = ord(key[ki % len(key)].lower()) - ord('a')
            base = ord('a')
            result.append(chr((ord(ch) - base - shift) % 26 + base))
            ki += 1
        else:
            result.append(ch)
    return "".join(result)

print(vigenere_decrypt("DNOLD{fammewzbz_fryaqyh}", "protonmail"))
# -> OWASP{something_remains}
```

## Flag

```
OWASP{something_remains}
```

## Design Notes

- **Three independent leads, one answer:** the EXIF metadata, the GitHub OSINT trail, and the blog-post riddle each give one piece (username → cipher type and key-riddle → actual key) — no single clue solves the challenge alone.
- **Decoy repos as a filter:** `C-Notes` is a genuine dead end and `Super-Tic-Tac-Toe`'s code is a red herring on its own — the key is hiding in the one place (a README) a solver might skip while focused on "the writing repo." This rewards solvers who check *everything* the clue mentioned ("things he had written") rather than just the obviously named repo.
- **The key riddle resolves in hindsight, not in advance:** "already given to you" and "a name, place, or address" don't make sense until the solver has already found the email — the clue is there to confirm the key once found, not to derive it cold.

## Tools Used

- `exiftool` — metadata extraction
- GitHub repo browsing
- Python — Vigenère decryption