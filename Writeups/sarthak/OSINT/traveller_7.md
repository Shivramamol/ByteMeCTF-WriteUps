# Traveller-7 : The Digital Footprint (OSINT, Hard)

**Author:** Sarthak Warale  
**Category:** OSINT  
**Difficulty:** Hard  
**Points:** 200  

## Challenge Description

> **Mission: The Traveller's Trail**  
> Find the small trace the traveller left at the destination.  
>  
> **Flag format:** `OWASP{...}`

## Summary

The traveller's note mentioned leaving a review after the trip. Searching recent Google Maps reviews for Tikona Fort / nearby locations reveals a planted review under the username `glitchseeker` containing a Base64-encoded string. Decoding the string produces the flag.

## Flag

```
OWASP{you_found_the_trace_7Kx92}
```

---

## Step 1 — Locate the Planted Review

The traveller's note concluded with:

> *"The trip was worth it. I will give it great review later."*

Checking Google Maps reviews for Tikona Fort uncovers a review posted by a user with the handle **glitchseeker**:

![Planted Google Maps Review](resources/evidence-stage-7-google-maps-review.jpg)

The review text includes the following Base64 payload:

```
T1dBU1B7eW91X2ZvdW5kX3RoZV90cmFjZV83S3g5Mn0=
```

## Step 2 — Decode the Payload

Decoding the Base64 string:

```bash
echo "T1dBU1B7eW91X2ZvdW5kX3RoZV90cmFjZV83S3g5Mn0=" | base64 -d
```

Output:
```
OWASP{you_found_the_trace_7Kx92}
```
