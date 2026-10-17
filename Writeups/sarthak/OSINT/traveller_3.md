# Traveller-3 : The Road Ends Here (OSINT, Medium)

**Author:** Sarthak Warale  
**Category:** OSINT  
**Difficulty:** Medium  
**Points:** 100  

## Challenge Description

> **Mission: The Traveller's Trail**  
> Which village did the traveller get off the bus at?  
>  
> **Flag format:** `OWASP{...}`

## Summary

From Kamshet Railway Station, the traveller traveled approximately 20–22 km by bus towards the base of a fort, followed by a final 1–2 km walk. Cross-referencing forts roughly 20 km from Kamshet with local bus routes identifies **Tikona Peth**, the base village for Tikona Fort.

## Flag

```
OWASP{TIKONA_PETH}
```

---

## Step 1 — Analyze the Route Clues

The traveller's note mentions:

> *"The fort wasn't exactly near the station — Maps showed something around 20–22 km away.*  
> *From there we took a bus and got down somewhere near the base. Had to walk another 1–2 km after that."*

Key parameters:
- Starting point: **Kamshet**
- Distance from station: **~20–22 km**
- Public transit: Bus to a village near the base
- Walking distance: 1–2 km to the fort base

## Step 2 — Map Out Potential Destinations from Kamshet

Measuring a 20–22 km radius from Kamshet Railway Station toward the popular trekking regions around Pawna Lake points directly to the road leading to Tikona Fort. 

The bus drops passengers at the base village of **Tikona Peth** (also known as Tikonapeth), from where a ~1.5 km walking trail leads directly to the fort trailhead.

![Evidence for Stage 3: Route to Tikona Peth](resources/evidence-stage-3-route-to-tikona-peth.png)

```
OWASP{TIKONA_PETH}
```
