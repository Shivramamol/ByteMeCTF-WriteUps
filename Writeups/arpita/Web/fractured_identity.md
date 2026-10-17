\# FRACTURED IDENTITY (Web Exploitation, Medium)



\*\*Author:\*\* Arpita Nikam  

\*\*Category:\*\* Web Exploitation  

\*\*Difficulty:\*\* Medium  

\*\*Theme:\*\* Soul Stone / Soul Registry  

\*\*Challenge Type:\*\* IDOR / Broken Object-Level Authorization (BOLA)



> Every identity has a record. The question is whether the Registry checks who is allowed to read it.



\---



\## Challenge Description



The Soul Registry appears to be a normal application for viewing soul records. However, different parts of the application refer to different identities, and not every record is meant to be accessible to every user.



The objective is to investigate the application's requests, identify a suspicious record reference, and determine whether the server correctly enforces authorization when a user requests another soul record.



Can you uncover the hidden flag?



\---



\## Summary



The challenge demonstrates \*\*Insecure Direct Object Reference (IDOR)\*\*, also known as a form of \*\*Broken Object-Level Authorization (BOLA)\*\*.



The application provides an authenticated endpoint for retrieving individual soul records. The vulnerability occurs when the server accepts a record ID without verifying that the logged-in user is authorized to access that specific record.



By inspecting the response for the user's own record and following a reference to another record, the hidden record can be accessed.



\---



\## Reconnaissance



\### Step 1 — Open the Soul Registry



Open the deployed challenge:



`https://soul-registry-ctf.onrender.com`



Log in using the credentials provided for the challenge.



After logging in, explore the dashboard and observe how the application loads the user's soul record.



\### Step 2 — Inspect Browser Requests



Open the browser's Developer Tools:



1\. Press `F12`.

2\. Select the \*\*Network\*\* tab.

3\. Choose \*\*Fetch/XHR\*\* to filter API requests.

4\. Reload the dashboard or navigate through the application.

5\. Inspect the requests and their responses.



The Network tab helps reveal the API endpoints used by the frontend and the data returned by the server.



\### Step 3 — Inspect Your Own Soul Record



Locate the request for your own record:



`GET /api/souls/101`



Inspect its response and examine the record details and audit information.



The response contains a reference to another Soul ID: `777`. This is a clue that another record may be relevant to the investigation.



\---



\## Exploitation



\### Step 4 — Investigate the Referenced Record



The application uses the record ID in the API endpoint to retrieve a soul record.



The endpoint pattern is:



```text

GET /api/souls/:id

```



The suspicious record reference suggests trying to retrieve Soul ID `777` while logged in.



\### Step 5 — Test Object-Level Authorization



While maintaining the authenticated session, inspect the following request:



```text

GET /api/souls/777

```



This can be tested through the browser's Network tools or by opening the endpoint in the same authenticated browser session.



Observe the server's response. The application returns the restricted record even though the logged-in user does not own it.



This confirms the authorization weakness: authentication is required, but ownership of the requested record is not properly enforced.



\### Step 6 — Recover the Flag



Inspect the response body for the restricted Soul Record. The hidden flag is stored in the record's `soulFragment` field.



Copy the exact flag returned by the deployed challenge.



\---



\## Flag



```text

OWASP{soul\_registry\_test\_flag}

```



Replace the placeholder above with the actual flag before submitting this write-up.



\---



\## Full Exploitation Chain



```text

Open Soul Registry

&#x20;       |

&#x20;       v

Log in to the application

&#x20;       |

&#x20;       v

Inspect browser Network requests

&#x20;       |

&#x20;       v

Retrieve own record (Soul ID 101)

&#x20;       |

&#x20;       v

Discover reference to Soul ID 777

&#x20;       |

&#x20;       v

Request /api/souls/777

&#x20;       |

&#x20;       v

Authorization check fails to restrict access

&#x20;       |

&#x20;       v

Read the restricted record

&#x20;       |

&#x20;       v

Recover the flag from soulFragment

```



\---



\## Vulnerability Analysis



\### 1. Insecure Direct Object Reference (IDOR)



The application uses a user-supplied record ID to retrieve a specific object. If the server does not verify whether the current user is authorized to access that object, changing the ID can expose another user's data.



\### 2. Broken Object-Level Authorization (BOLA)



The API authenticates the user but does not adequately enforce authorization at the individual record level.



Authentication answers, "Who are you?"



Authorization answers, "Are you allowed to access this particular record?"



The challenge demonstrates why both checks are necessary.



\### 3. Impact



In a real application, this vulnerability could expose private records belonging to other users. Depending on the data and available operations, the impact could include unauthorized disclosure or access to sensitive information.



\### 4. Remediation



Recommended security improvements include:



1\. \*\*Verify record ownership:\*\* Check that the authenticated user is authorized to access the requested record.

2\. \*\*Enforce authorization on the server:\*\* Never rely on hidden buttons or frontend restrictions as security controls.

3\. \*\*Use scoped database queries:\*\* Retrieve records through the current user's authorized dataset wherever appropriate.

4\. \*\*Return appropriate errors:\*\* Deny unauthorized access without revealing protected record contents.

5\. \*\*Test every object-level endpoint:\*\* Include authorization tests for different users and record IDs.



\---



\## Tools Used



\- Web browser

\- Browser Developer Tools

\- Network tab (Fetch/XHR)

\- HTTP request and response inspection



\---



\## Timeline



| Step | Action | Result |

|---|---|---|

| 1 | Open the Soul Registry | Application interface discovered |

| 2 | Log in | Authenticated session established |

| 3 | Inspect API requests | Soul record endpoint identified |

| 4 | Inspect Soul ID 101 | Reference to Soul ID 777 discovered |

| 5 | Request Soul ID 777 | Unauthorized record access observed |

| 6 | Inspect the response | Flag recovered from `soulFragment` |



\---



\## Conclusion



FRACTURED IDENTITY demonstrates that a valid login does not automatically grant permission to access every object in an application. By inspecting API requests and testing record-level authorization, the IDOR/BOLA vulnerability can be identified.



The key lesson is that every request for a protected object must be authorized on the server, regardless of whether the user is already authenticated.



\---



\## Disclaimer



This write-up documents a deliberately vulnerable CTF challenge for educational purposes. Test these techniques only on systems you own or have explicit permission to assess.



\*\*Challenge:\*\* FRACTURED IDENTITY  

\*\*Project:\*\* Soul Registry

