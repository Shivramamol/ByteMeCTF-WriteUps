# Traveller-2 : Seven Stops (OSINT, Easy)

**Author:** Sarthak Warale  
**Category:** OSINT  
**Difficulty:** Easy  
**Points:** 75  

## Challenge Description

> **Mission: The Traveller's Trail**  
> Which station did the traveller get off at?  
>  
> **Flag format:** `OWASP{...}`

## Summary

The traveller took a local train from Akurdi Railway Station and travelled to the 7th station (after 6 intermediate stops). Following the Pune–Lonavala local train route outwards from Akurdi, counting 6 intermediate stops arrives at **Kamshet Railway Station**.

## Flag

```
OWASP{KAMSHET}
```

---

## Step 1 — Check the Note for Station Clues

The traveller's note describes the train journey:

> *"After 6 stops our destination was on the 7th station. Got off there."*

From Challenge 1, we know the starting point is **Akurdi Railway Station**.

## Step 2 — Trace the Pune–Lonavala Suburban Train Route

Akurdi lies on the Pune Junction – Lonavala suburban railway route. Looking up the sequence of stations traveling towards the Lonavala/trek direction:

1. Starting point: **Akurdi**
2. Stop 1: Dehu Road
3. Stop 2: Begdewadi
4. Stop 3: Ghorawadi
5. Stop 4: Talegaon
6. Stop 5: Vadgaon
7. Stop 6: Kanhe
8. **7th Station (Destination): Kamshet**

![Evidence for Stage 2: Station Sequence](resources/evidence-stage-2-station-sequence.png)

Counting 6 stops after Akurdi leads to **Kamshet Railway Station**.

```
OWASP{KAMSHET}
```
