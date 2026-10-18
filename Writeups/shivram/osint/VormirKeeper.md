# Souled Stone — Writeup

**Category:** OSINT
**Difficulty:** Hard
**Flag:** `OWASP{preikestolen_7734_sacrifice}`

---

## Overview

A collector known only as **VormirKeeper** has left a trail across a few
corners of the internet. The challenge starts with a single profile page
and requires chaining three separate OSINT techniques to reach the flag.

---

## Layer 1 — The Profile

**Start:** `profile.html`

The profile shows a bio and a single posted photo of a faceted gem.

**Technique:** EXIF metadata extraction

Download the image and inspect its metadata:
\`\`\`
exiftool stone_final.jpg
\`\`\`

This reveals embedded GPS coordinates:
\`\`\`
GPSLatitude: 58 deg 59' 11.86" N
GPSLongitude: 6 deg 11' 24.93" E
\`\`\`

Plugging these into Google Maps identifies the location as
**Preikestolen**, a well-known cliff in Norway.

**Layer 1 output:** `preikestolen`

**In-fiction pointer to next layer:**
> "Find me where the keepers gather, same name, no numbers this time."

This hints that the same persona exists elsewhere under the handle
**VormirKeeper** (without the "92").

---

## Layer 2 — The Blog

**Found via:** searching the handle "VormirKeeper"

The blog ("the ledger") contains a reflective post about the cost of
collecting, including the line:

> "entry — three years since Preikestolen"

This date reference becomes important in Layer 3.

**Technique:** Viewing page source

The visible text hints: *"It's never in what you read — it's in what's
written underneath."* This nudges solvers to check the HTML source
(Ctrl+U / Inspect Element), where an HTML comment is hidden:

\`\`\`html
<!-- ledger entry, do not share: 7734 -->
\`\`\`

**Layer 2 output:** `7734`

---

## Layer 3 — The Forum Post

**Found via:** the same handle search, second result

A forum thread ("Collectors' Circle") contains a post from VormirKeeper
with a block of ciphertext:

\`\`\`
VDFULILFH
\`\`\`

**Technique:** Caesar cipher decryption

The key isn't given directly — it's the number "three" from Layer 2's
blog post ("three years since Preikestolen"). Using a Caesar cipher
shift of 3:

\`\`\`
V -> S
D -> A
F -> C
U -> R
L -> I
I -> F
L -> I
F -> C
H -> E
\`\`\`

Decoded: **SACRIFICE**

**Layer 3 output:** `sacrifice`

*(Note: a second forum reply from "rustyOSINT" is a red herring with no
puzzle value — it's there to add noise/realism.)*

---

## Final Step — Assembling the Flag

Combine all three outputs using the published flag format
`OWASP{location_pin_word}`:

\`\`\`
OWASP{preikestolen_7734_sacrifice}
\`\`\`

---

## Key Takeaways

- Image metadata (EXIF) can reveal exact locations even from
  seemingly unrelated photos.
- Viewing page source is a basic but often-overlooked OSINT step —
  information doesn't have to be visible on the rendered page to be
  present in the file.
- Details dropped earlier in an investigation (like a casual date
  reference) can become keys needed later — good OSINT work involves
  keeping track of every detail, not just the obvious ones.
