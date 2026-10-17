# Traveller-5 : Two Shapes on the Horizon (OSINT, Hard)

**Author:** Sarthak Warale  
**Category:** OSINT  
**Difficulty:** Hard  
**Points:** 150  

## Challenge Description

> **Mission: The Traveller's Trail**  
> Identify the two forts in the summit photograph.  
>  
> **Flag format:** `OWASP{FORT1_FORT2}`

## Summary

From the summit of Tikona Fort, two prominent sister forts are visible on the horizon. Comparing the line of sight and topological features in the photograph confirms the two forts are **Lohagad** and **Visapur** (in that order).

## Flag

```
OWASP{LOHGAD_VISAPUR}
```

---

## Step 1 — Analyze the Summit Photograph

The traveller notes:

> *"From the top we could see two other forts. I got some nice photos of them and marked them 1 and 2 because I didn't know their names."*

We are provided with both the original photograph and a copy with the two landmarks numbered 1 and 2:

![Original Summit Photograph](resources/photo-summit-forts-original.jpg)

![Summit Photograph with Landmarks Marked](resources/photo-summit-forts-marked.jpg)

## Step 2 — Line of Sight and Terrain Comparison

Looking northwest from Tikona Fort summit across the Maval landscape:
- **Landmark 1:** The distinctive long ridge and *Vinchukata* (scorpion's tail) spur of **Lohagad Fort**.
- **Landmark 2:** The broad, flat-topped plateau of **Visapur Fort** immediately adjacent to Lohagad.

![Regional Map showing nearby landmarks](resources/evidence-stage-5-region-map.png)

Combining the two fort names in order yields the flag:

```
OWASP{LOHGAD_VISAPUR}
```
