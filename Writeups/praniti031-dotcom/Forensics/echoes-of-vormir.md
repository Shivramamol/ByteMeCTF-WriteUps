\# Echoes of Vormir (Forensics, Easy)



\*\*Author:\*\* Your Name  

\*\*Category:\*\* Forensics  

\*\*Difficulty:\*\* Easy



\---



\## Challenge Description



> Four echoes remain from the journey to Vormir. Each image contains a piece of the story, but the pieces are scattered.

>

> The objective is to investigate the four files, understand the clues they contain, and reconstruct the final message.



\## Summary



This challenge involves analyzing four PNG images to uncover hidden metadata, hexadecimal clues, and Base64-encoded flag fragments. By examining the files, decoding the clues, and combining the fragments in the intended order, the final flag can be recovered.



\## Flag



```text

OWASP{echoes\_are\_hard\_to\_bury}

```



\---



\## Step 1 — Identify the File Types



First, identify the formats of the four provided files using the `file` command.



```bash

file soul\_01.png soul\_02.png soul\_03.png soul\_04.png

```



All four files were identified as PNG images. However, the visible image content does not reveal the complete message, so further investigation is required.



\---



\## Step 2 — Inspect the Image Metadata



Use ExifTool to inspect the metadata of all four images.



```bash

exiftool soul\_01.png

exiftool soul\_02.png

exiftool soul\_03.png

exiftool soul\_04.png

```



The fourth image contains the following comment:



```text

Comment : The beginning comes first.

```



This clue suggests that the order of the images is important when reconstructing the final message.



\---



\## Step 3 — Decode the Hexadecimal Clue



The third image contains the following hexadecimal string:



```text

4445434f44453a424153453634

```



Decode the hexadecimal string using `xxd`:



```bash

echo "4445434f44453a424153453634" | xxd -r -p

```



\*\*Output:\*\*



```text

DECODE:BASE64

```



This reveals that Base64 decoding is required to recover the final message.



\---



\## Step 4 — Search for Hidden Data



Next, use the `strings` command to search for readable data in the first two image files.



```bash

strings soul\_01.png | tail

strings soul\_02.png | tail

```



The following encoded fragments were discovered.



\*\*Fragment from `soul\_01.png`:\*\*



```text

T1dBU1B7ZWNob2VzX2FyZV9oYXJk

```



\*\*Fragment from `soul\_02.png`:\*\*



```text

X3RvX2J1cnl9

```



These strings are Base64-encoded fragments of the final flag.



\---



\## Step 5 — Determine the Order and Reconstruct the Message



Based on the story clue, the intended order of the echoes is:



```text

soul\_04 → soul\_03 → soul\_01 → soul\_02

```



The encoded flag fragments are found in `soul\_01.png` and `soul\_02.png`.



Combining the fragments in the intended order produces the following Base64 string:



```text

T1dBU1B7ZWNob2VzX2FyZV9oYXJkX3RvX2J1cnl9

```



\---



\## Step 6 — Decode the Final Flag



Decode the combined Base64 string using the `base64` command.



```bash

echo 'T1dBU1B7ZWNob2VzX2FyZV9oYXJkX3RvX2J1cnl9' | base64 -d

```



\*\*Output:\*\*



```text

OWASP{echoes\_are\_hard\_to\_bury}

```



The final flag has been successfully recovered.



\---



\## Solution Summary



| Field | Value |

|---|---|

| Challenge Name | Echoes of Vormir |

| Category | Forensics |

| Difficulty | Easy |

| Input Files | Four PNG images |

| Metadata Analysis | ExifTool |

| Hexadecimal Decoding | `xxd` |

| Hidden Data Extraction | `strings` |

| Encoding Technique | Base64 |

| Final Flag | `OWASP{echoes\_are\_hard\_to\_bury}` |



\---



\## Root Cause / Forensics Methodology



This challenge demonstrates how files can contain information beyond their visible content. Metadata, appended strings, and encoded data can all provide clues during a forensic investigation.



1\. \*\*Metadata Analysis\*\* — ExifTool reveals a comment that provides a clue about the ordering of the images.



2\. \*\*Hexadecimal Decoding\*\* — Converting the hexadecimal string into readable text reveals the instruction `DECODE:BASE64`.



3\. \*\*Hidden Data Extraction\*\* — The `strings` command reveals Base64-encoded fragments appended to the PNG files.



4\. \*\*Message Reconstruction\*\* — The fragments are combined according to the intended order to reconstruct the complete encoded message.



5\. \*\*Base64 Decoding\*\* — Decoding the reconstructed string reveals the final flag.



\### Key Takeaway



In CTF forensics challenges, do not rely only on the visible contents of a file. Inspect metadata, search for appended data, investigate encoding clues, and correlate the evidence to uncover hidden information.



\---



\## Tools Used



| Tool | Purpose |

|---|---|

| `file` | Identifies the file formats |

| `exiftool` | Inspects image metadata |

| `xxd` | Converts hexadecimal data into readable text |

| `strings` | Searches for readable strings within files |

| `base64` | Decodes the final message |



\---



\## Timeline



| Step | Action | Result |

|---|---|---|

| 1 | Identified the four files | Confirmed all files were PNG images |

| 2 | Inspected image metadata | Discovered the ordering clue |

| 3 | Decoded the hexadecimal string | Obtained `DECODE:BASE64` |

| 4 | Searched for hidden strings | Found two encoded flag fragments |

| 5 | Combined the fragments | Reconstructed the Base64 string |

| 6 | Decoded the final message | Recovered the flag |



\---



\## Conclusion



The \*\*Echoes of Vormir\*\* challenge was solved by combining basic digital forensics techniques with hexadecimal and Base64 decoding. The challenge highlights the importance of carefully inspecting files and following clues to reconstruct hidden information.



\*\*Final Flag:\*\*



```text

OWASP{echoes\_are\_hard\_to\_bury}

```

