# Traveller-6 : Across the Water (OSINT, Medium)

**Author:** Sarthak Warale  
**Category:** OSINT  
**Difficulty:** Medium  
**Points:** 150  

## Challenge Description

> **Mission: The Traveller's Trail**  
> Identify the fort visible across the water and the lake.  
>  
> **Flag format:** `OWASP{FORT_LAKE}`

## Summary

On the journey back from Tikona Fort, the traveller paused beside a lake and photographed a conical fort standing across the water. Geolocation of the viewpoint confirms the body of water is **Pawna Lake** (Pavana reservoir) and the conical fort across it is **Tung Fort**.

## Flag

```
OWASP{TUNG_PAWNA}
```

---

## Step 1 — Examine the Return Photograph

The traveller's note states:

> *"On the way back, we stopped beside a lake. From there, another fort was visible across the water. It looked quite different from what we saw from the top."*

![Return photograph showing fort across the lake](resources/photo-return-tung-pawna.jpg)

## Step 2 — Identify the Lake and Fort

1. **The Lake:** Tikona Fort directly overlooks the massive **Pawna Lake** (Pavana Dam reservoir). The road back to Kamshet runs alongside the eastern shores of Pawna Lake.
2. **The Fort Across the Water:** Directly opposite Tikona across Pawna Lake is **Tung Fort** (Khardurg), famous for its steep conical peak rising prominently out of the water.

Combining the fort and the lake according to the required format gives:

```
OWASP{TUNG_PAWNA}
```
