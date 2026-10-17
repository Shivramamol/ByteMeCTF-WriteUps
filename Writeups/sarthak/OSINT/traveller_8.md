# Traveller-8 : Who Was the Traveller (OSINT, Expert)

**Author:** Sarthak Warale  
**Category:** OSINT  
**Difficulty:** Expert  
**Points:** 300  

## Challenge Description

> **Mission: The Traveller's Trail**  
> Find the traveller's name and position.  
>  
> **Flag format:** `OWASP{NAME_POSITION}`

## Summary

Searching for the username `glitchseeker` uncovered in Challenge 7 leads to a CTFtime team profile (`k4iz3n`). The profile lists the team's official website as `owasppccoe.in` and a contact email `sarthak.warale24@pccoepune.org`. Cross-referencing the official OWASP PCCOE team page reveals that **Sarthak Warale** holds the position of **Co-Lead**.

## Flag

```
OWASP{SARTHAK_CO_LEAD}
```

---

## Step 1 — Investigate the Handle `glitchseeker`

From Challenge 7, the reviewer's handle was identified as **glitchseeker**. 

Performing an OSINT search on this handle across CTF platforms locates a CTFtime profile associated with the academic CTF team **k4iz3n**:

![Evidence for Stage 8: CTFtime profile](resources/evidence-stage-8-ctftime-profile.png)

Key findings on the CTFtime profile:
- **Member:** `glitchseeker`
- **Website:** `https://www.owasppccoe.in/`
- **Contact Email:** `sarthak.warale24@pccoepune.org`

## Step 2 — Correlate with the OWASP PCCOE Team Page

Navigating to the official OWASP PCCOE chapter website (`https://owasppccoe.in/team`) and inspecting the Core Team roster:

![Evidence for Stage 8: OWASP PCCOE Core Team page](resources/evidence-stage-8-owasp-pccoe-team.png)

The profile confirms:
- **Name:** Sarthak Warale
- **Role / Position:** Co-Lead

Combining the name and position in the required `OWASP{NAME_POSITION}` format:

```
OWASP{SARTHAK_CO_LEAD}
```

