# Collectors' Circle — Guestbook — Writeup

*(Collectors' Circle - Guestbook)*

**Category:** Web / Security
**Difficulty:** Medium
**Flag:** `OWASP{dom_never_trusts_the_url}`

---

## Overview

The Collectors' Circle forum has a guestbook page that reflects a
visitor's name back onto the page. The input is filtered, but the
filter only blocks a specific keyword — not the underlying technique.

---

## Step 1 — Explore the Page

Open `guestbook.html`. A hint on the page suggests trying a `?name=`
URL parameter:

guestbook.html?name=Alex


Result: the page displays **"Welcome, Alex!"** — confirming the input
is reflected directly into the page.

---

## Step 2 — Try a Basic Payload

A natural first attempt:

guestbook.html?name=<script>alert(1)</script>


Result: **nothing happens.** No popup appears, indicating some form of
filtering is in place.

---

## Step 3 — Inspect the Filter

Viewing the page source (Ctrl+U) reveals the relevant JavaScript:

```javascript
function basicFilter(input) {
  return input.replace(/script/gi, '');
}
```

This filter only strips the literal word **"script"** (case-insensitive).
It does not block any other HTML tags, attributes, or event handlers.

---

## Step 4 — Bypass the Filter

Since the filter is keyword-based rather than behavior-based, any
payload that triggers JavaScript execution *without* using the word
"script" will succeed. A classic bypass:

guestbook.html?name=<img src=x onerror=alert(1)>


The broken image (`src=x`) fails to load, which fires the `onerror`
event handler — running JavaScript despite the filter.

---

## Step 5 — Locate the Flag-Retrieval Function

Still inspecting the page's JavaScript, a function is already defined:

```javascript
window.collectFlag = function() {
  fetch('/.netlify/functions/get-flag')
    .then(res => res.json())
    .then(data => alert('Flag captured: ' + data.flag));
};
```

This function calls a backend serverless function to retrieve the real
flag — the flag is never present anywhere in the page's HTML or
client-side JavaScript.

---

## Step 6 — Trigger the Flag

Final payload:

guestbook.html?name=<img src=x onerror=window.collectFlag()>


This executes `collectFlag()` via the `onerror` handler, which fetches
the flag from the server and displays it:

Flag captured: owasp{dom_never_trusts_the_url}


---

## Key Takeaways

- **Keyword-based filters are not a substitute for proper output
  encoding.** Blocking the literal word "script" does nothing to stop
  the dozens of other HTML constructs that execute JavaScript (`img`,
  `svg`, `body`, `iframe`, and many event handler attributes).
- **DOM XSS often hides in plain sight** — the vulnerable sink here was
  a single line using `innerHTML` instead of `textContent`.
- **Sensitive data should never live client-side** if it depends on a
  security boundary (like "only reachable via a successful exploit") —
  the real fix here was moving the flag to a server-side function that
  only responds when actually called, rather than hiding it in the
  page's HTML.
