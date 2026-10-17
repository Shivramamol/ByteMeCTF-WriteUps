# The Keeper's Legacy

**Category:** OSINT | **Flag format:** `OWASP{Name_of_the_Place}` | **Author:** Somay Rathod

## Challenge Premise

> The Keeper is gone. He left behind seven places, seven fragments of a trail, for the one who would come after him. Find each place. Mark the ground exactly where each fragment was born. Seven points will become something older than the trail itself — a pattern that has watched the world turn through countless generations. Let the pattern be your guide. Follow where it points, beyond the turning of the wheel, to where the Keeper's trail comes to an end. Go there. Find what remains.

Solvers are given seven photographs and nothing else — the riddle only tells them that *locating* the seven places is step one, and that a second step ("follow where it points") still has to happen afterward.

## Step 1 - Geolocate each of the seven photos

Standard GEOINT technique: cross-reference each photo's architecture, signage/script, vegetation, and visible background structures against satellite imagery (Google Earth / Maps) to pin an exact coordinate, not just a neighborhood. Three of the confirmed points in this build are real, independently verifiable Varanasi landmarks — Shri Kashi Vishwanath Temple, a Rajkiya Ayurved Mahavidyalaya building, and Mahalaxmi Temple — with the remaining points filled in from the other four photos.

## Step 2 - Mark exact points, not approximate areas

The riddle's line *"mark the ground exactly where each fragment was born"* is doing real work: the pattern in Step 3 only resolves if each point is placed precisely. A pin dropped on the wrong side of a building or a block away is close enough to pass a casual check but will visibly distort the shape once plotted.

## Step 3 - Recognize the pattern

![Pattern](<resources/solution.png>)

With all seven points placed, connecting them traces the outline of the Big Dipper. The riddle's *"a pattern that has watched the world turn through countless generations"* is a direct nod to the Big Dipper - it never sets, and it has been used as a celestial reference point for millennia, which is also why cultures worldwide (including the Saptarishi Mandal naming in Indian tradition) recognize the same seven-star shape independently.

## Step 4 - Use the pattern as a direction, not just a shape

*"Let the pattern be your guide, follow where it points"* borrows the real astronomy of the Big Dipper's two outermost *"bowl"* stars (Dubhe and Merak), which line up to point toward Polaris - but only the direction, not the usual distance. The line those two points define isn't extended out across the map; the destination sits right at, or immediately beyond, one of the two pointer points themselves. So once the pattern is recognized, the search space for *"where it points"* collapses to a small area around one specific point already on the map, not a long bearing off into empty space.

## Step 5 - Confirm the endpoint with the riddle's own language

With the search narrowed to one of the two pointer points, the riddle's final lines do the confirming rather than a separate GEOINT step: *"beyond the turning of the wheel, to where the Keeper's trail comes to an end... find what remains."* *"The turning of the wheel"* doubles as the wheel of sansara - the cycle of death and rebirth - which points straight at a cremation site, and *"find what remains"* plays on both cremation remains and the end of the trail. Read against the pointer point's real-world location, those lines identify it as Manikarnika Ghat, one of Varanasi's most significant cremation ghats on the Ganges.

## Step 6 - Avoid the decoy

A differently-located ghat sharing the name "Manikarnika Ghat" exists near Uttarkashi, hundreds of kilometers away. A solver who skips the geometry and just searches the flag format's place name directly risks locking onto the wrong landmark. The intended path reaches the answer by construction first, and only confirms it by name afterward - not the reverse.

## Flag

```
OWASP{Manikarnika_Ghat}
```

## Design Notes

- **Why seven points:** enough to form a globally-recognizable asterism without so many points that the shape degenerates into noise - most solvers will recognize the Big Dipper's outline unprompted once plotted correctly.
- **Burying the pointer-star method in verse:** *"let the pattern be your guide / follow where it points"* rewards solvers who either know, or quickly research, how the Big Dipper is used to find Polaris — this adds a celestial-navigation layer on top of pure photo geolocation rather than ending the challenge at "shape identified."
- **The same-name decoy is deliberate:** it punishes shortcutting the geometric construction in favor of guessing the destination from the flag format alone.
- **Dual-meaning language** ("turning of the wheel," "find what remains") ties the astronomy and the ghat's funerary significance together thematically, reinforcing the answer rather than just describing a location.

## Tools Used

- Reverse image search / manual OSINT (signage, architecture, satellite cross-referencing)
- Google Earth / Google My Maps — plotting points and measuring/extending the bearing
- Basic celestial-navigation knowledge (Big Dipper pointer-star method)

## Summary

Each photo geolocates to a real site in Varanasi. Plotting all seven points on a map traces the outline of the **Saptarishi Mandal** - the seven stars of Ursa Major, known in the West as the Big Dipper. Applying the classic "pointer star" trick used to find Polaris - extending the line through the two outer stars of the dipper's bowl - gives a bearing that terminates at a real landmark: **Manikarnika Ghat**, one of Varanasi's oldest cremation ghats on the Ganges.