# Traveller-1 : The First Stop (OSINT, Easy)

**Author:** Sarthak Warale  
**Category:** OSINT  
**Difficulty:** Easy  
**Points:** 75  

## Challenge Description

> **Mission: The Traveller's Trail**  
> A traveller left behind a note and a few photographs, but not the names of the places they visited.  
> Reconstruct the journey step by step—from the railway station to the trek, the forts, the lake, and finally the traveller's digital footprint.  
> Follow the trail. Find the flags. Complete the journey.  
>  
> **Challenge:** Determine the railway station from which the traveller started.  
> **File:** [`resources/traveller-note.txt`](resources/traveller-note.txt)  
> **Flag format:** `OWASP{...}`

## Summary

The traveller's note mentions residing in Nigdi, Pradhikaran, and walking to a nearby railway station to catch a local train. Researching the local railway network around Nigdi/Pradhikaran reveals that the closest railway station is **Akurdi Railway Station**.

## Flag

```
OWASP{AKURDI}
```

---

## Step 1 — Analyze the Traveller's Note

The note provided in the challenge files (`resources/traveller-note.txt`) contains the opening clue:

> *"I live in Nigdi, Pradhikaran, so I walked to the station and took a local from there."*

This establishes two critical pieces of information:
1. The starting residential area is **Nigdi, Pradhikaran** (PCMC, Pune).
2. The distance to the railway station is within walking distance.

## Step 2 — Identify the Nearest Railway Station

Looking up railway stations serving the Nigdi and Pradhikaran localities on Google Maps or Indian Railways network maps identifies **Akurdi Railway Station** (`AKRD`), located directly adjacent to Sector 26 / Pradhikaran.

![Evidence for Stage 1: Akurdi Railway Station](resources/evidence-stage-1-akurdi.png)

Wrapping the station name in uppercase in the flag format gives:

```
OWASP{AKURDI}
```
