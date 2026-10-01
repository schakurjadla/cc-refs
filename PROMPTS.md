# Turkish Time: Script + Workflows (v3, 01.10.2026)

Source: `Downloads/BRIEFING-CLAUDE (1).md`. Changes in v2 (Schakur's feedback):
1. **Motif:** a big **nazar (evil eye) surrounded by İznik tulips and carnations** instead of the wolf/tea glass. It's the best-known Turkish symbol and carries no political reading.
2. **Shirt look like the original:** the original is a large, finely drawn Chinese dragon with white serif text underneath, on black or red ([Etsy](https://www.etsy.com/listing/4573265875/you-met-me-at-a-very-chinese-time-in-my), [TeePublic](https://www.teepublic.com/t-shirts/you-met-me-at-a-very-chinese-time)). We copy that: detailed illustration, not PS2.
3. **Tools:** Higgsfield API (pay per generation) + Higgs chat for the tutorial on camera. **Seedance 2.5 = one prompt, 19 s, all references** (model allows 4–30 s, image + video + audio references).
4. **Print:** motif via GPT Image 2.5 with a transparent background → set the text in Figma → mockup via image-to-image.

**v3: sweater instead of hoodie.** The product is a crewneck sweater (no hood, no pocket), like the Swiss one. In every image/video prompt it's called a **"crewneck sweatshirt"**, because "sweater" alone makes image models draw a knitted jumper. On camera you just say "sweater".

Fixed nouns: **the host** = the Turkish man. **The visitor** = the German man. Captions, prices and the shirt line never go into an image or video prompt.

---

## A. Workflow: video (for the tutorial)

| # | Step | Tool | Setting | Output |
|---|---|---|---|---|
| 1 | Host character sheet | Higgs chat / API `gpt_image_2_5` | 2k, 16:9 | `host_sheet` |
| 2 | Visitor character sheet | same | 2k, 16:9 | `visitor_sheet` |
| 3 | 3 locations | same | 2k, 4:3 | `loc_lokanta`, `loc_road`, `loc_terrace` |
| 4 | 15-panel storyboard (check before video) | same, references 1–3 | 2k, 16:9 | `storyboard` |
| 5 | Two voices | ElevenLabs Voice Design | see C | `voice_host`, `voice_visitor` |
| 6 | Dialogue as **one** 19 s track | ElevenLabs Text to Dialogue (Eleven v4) | see B | `dialogue.mp3` |
| 7 | Video test | `seedance_2_5`, `omni_reference` | 19 s, 9:16, **`draft: true`** (480p, cheap) | Draft job |
| 8 | Video final | `seedance_2_5` | `draft_job_id` = winning draft → 1080p | `final.mp4` |
| 9 | Captions + end card | After Effects | Captions hand-set, end card = mockup from D | Reel |

Cost tip: always preflight with `get_cost: true` before a generation. For example, GPT Image 2.5 at 2k/high/transparent = **2.75 credits** (preflight 01.10.), at 1k/low = 0.25. The draft→finalize route in Seedance saves 1080p renders on failed takes.

## B. Script: 6 beats (19 s)

The Swiss reference is inverted: there the bill was endlessly long, here **the receipt is tiny**. The visitor turns it over looking for the rest.

| Beat | Time | Image | Caption (hand-set) | Spoken |
|---|---|---|---|---|
| 1 | 0:00–0:03.5 | Lokanta, two-shot, **the table full of plates** (kebab, mezze, bread, salad, tea). The host leans back at ease, the visitor sits upright, stuffed | My friend came to Turkey for the first time. | — (spoons, TV) |
| 2 | 0:03.5–0:06.5 | Close-up of the visitor with the tiny receipt, turns it over | He saw the prices and asked if there was a mistake. | **The visitor:** "Sorry — is this the whole bill? I think there's a mistake." |
| 3 | 0:06.5–0:10.5 | The host crosses his arms, deadpan, then pours tea without looking. The visitor keeps staring at the receipt | my friend, that's just Turkey. You'll get used to it. | **The host:** "Kardeşim. That's just Turkey. You'll get used to it." |
| 4 | 0:10.5–0:13 | Sedan on a coastal road at dusk, red sleeve out of the window | — | — (engine, wind) |
| 5 | 0:13–0:16 | Terrace at sunset. The host looks into the camera, the visitor in the background with tea at the sea | — | **The visitor** sighs |
| 6 | 0:16–0:19 | Push-in on the host, deadpan | You met me at a very Turkish time in my life. | **The host:** "You met me at a very Turkish time in my life." |

### Eleven v4: Text to Dialogue (Speaker 1 = visitor, Speaker 2 = host)

```
Speaker 1: [rushed] [whispering] Sorry — is this… the whole bill? [pause] I think there's a mistake.
Speaker 2: [sighs] [dry] Kardeşim. [pause] That's just Turkey. [slightly annoyed] You'll get used to it.
Speaker 1: [quietly] …okay.
Speaker 1: [long sigh]
Speaker 2: [dry] [slow] You met me at a very Turkish time in my life.
```

Generate 3–4 takes per line. Then cut **one** track in the beat timing above (pauses included) and export it as `dialogue.mp3`. That becomes the audio reference for Seedance.

## C. Voice Design (ElevenLabs)

### The host
```
Young man, early twenties, mid-to-high tenor, bright and slightly nasal tone. A cartoon voice, not naturalistic: theatrical delivery with big pitch bends up and down inside a single phrase, vocal fry at the ends of lines, audible tired sighs between sentences. Native English speaker with a Turkish accent underneath; Turkish slang such as "abi", "kardeşim", "hadi" and "yavaş yavaş" is pronounced fully Turkish. Slow, unbothered pace, three to four words per second. Recording quality: 2004 video game disc audio, heavily compressed, narrow band, no high frequencies, like a game cutscene played through a small TV speaker.
```
Preview text: `Kardeşim, listen to me. You sit, you drink your tea, nobody is in a hurry. Hadi, yavaş yavaş. This is how it works here, abi.`

(Briefing contradiction: the body is mid-30s and stocky, the voice is "early twenties". Written as briefed. If it should match the body: `Man in his mid-thirties, low warm baritone with a rough edge,`.)

### The visitor
```
Man, late twenties, light baritone, clipped and careful. A cartoon voice, not naturalistic: polite and tense, slightly breathless when surprised, pitch jumps up on questions, a short nervous laugh. Native German speaking English with a clear German accent: hard consonants, "th" becoming "s" or "z", "w" sounding close to "v". Quick, precise pace, four to five words per second when nervous. Recording quality: 2004 video game disc audio, heavily compressed, narrow band, no high frequencies, like a game cutscene played through a small TV speaker.
```
Preview text: `Excuse me, sorry, I think there is a small mistake here. This cannot be the whole bill. In Germany this would be maybe three times more, at least.`

---

## D. Workflow: sweater print + shop

| # | Step | Tool | Setting |
|---|---|---|---|
| 1 | Choose the POD blank **first**, then lock the colour (see D1a) | Printful or Printify | **Comfort Colors 1566** garment-dyed crewneck, colour **Crimson** (fallback: Terracotta) |
| 2 | Generate the motif, no text | `gpt_image_2_5` | 2k, 1:1, quality high, **`background: transparent`** |
| 3 | Set the print file | Figma (I'll build it) | Frame 3600 × 4200 px (= 30 × 35 cm at 300 dpi), motif on top, text below |
| 4 | Export | Figma | PNG, transparent, 300 dpi |
| 5 | Mockup via image-to-image | `gpt_image_2_5`, references: blank sweater photo + print PNG | 2k, 4:5 |
| 6 | Upload to the shop + order a sample | Printify | Sample = real photo for the video ending |

### D1a: the blank (decided)

**Pick: Comfort Colors 1566, colour Crimson.** It's the garment-dyed crewneck most POD shops carry, and garment-dyed means it already looks washed and faded, like the original. Crimson is its closest colour to the faded Turkish red. "Brick" (the old note) is out: it's more of a wine red, and it's usually not offered for the 1566 by POD shops.

Check before you generate anything (2 minutes, in the shop dashboard):
1. Printful (first choice, has its own production in Spain and Latvia) → catalog → search "Comfort Colors 1566". Is **Crimson** there? Then look at the shipping/production location for Germany.
2. If Printful doesn't have it, or only ships it from the US: Printify → search "1566" → pick a provider that has Crimson and ships to Germany.
3. If Crimson is nowhere: **Terracotta** (more orange-red, also works with the turquoise of the nazar).
4. If no 1566 at all: any **plain red crewneck** the shop produces in Europe (often Stanley/Stella). It won't be garment-dyed, so the worn look comes only from the print texture.

**Colour lock:** open the chosen colour in the shop, take the hex from the swatch (or the colour picker on the product photo), and replace `#B23A2E` with it **everywhere in this file** (find & replace, 7 places) before you generate the blank, the mockup or the host. That way the AI sweater, the character's sweater and the real sweater are the same red. When the sample arrives, compare it to the mockup; if it's off, regenerate D4/D5 with the hex taken from a photo of the sample.

### D1b: request to Claude (on camera in the video)

```
Write me an image prompt for GPT Image 2.5 for a print on a crewneck sweatshirt. Motif: a large Turkish nazar (the blue evil-eye bead) surrounded by İznik tulips and carnations, drawn as detailed as the dragon on the "You met me at a very Chinese time in my life" shirt. Underneath, in serif type: "you met me at a very Turkish time in my life". Rules: no words like premium, stunning, cinematic, high quality, elegant. Describe concrete objects instead of adjectives. All colours as hex codes, two dominant colours far apart on the colour wheel. Flat screenprint look with wear, transparent background, nothing political.
```

### D2: motif prompt (nazar + İznik flowers + text)
Higgsfield: GPT Image 2.5 · quality max · 4k · background transparent · 1:1 · 4 variants. Check the text letter by letter; if it's wrong, regenerate, otherwise fix it in Figma.

```
Print artwork for the chest of a crewneck sweatshirt, one centred illustration with one line of type underneath, on a transparent background, nothing else. No other text, no numbers, no signature, no frame.

The motif: a large Turkish nazar — the blue glass evil-eye bead — seen straight on, as the centre of the design: a deep navy #1B2A4A outer ring, a white ring, a turquoise #2E8B8B ring, and a dark navy pupil with one small curved highlight showing it is made of glass, tiny air bubbles and a slight uneven edge from hand-blown glass. Around the nazar, wrapping it on both sides and below, a dense arrangement of İznik-style flowers drawn like a 16th-century Ottoman tile design: four tall tulips with long pointed petals, three open carnations with serrated edges, curling saz leaves with sharp serrated tips, small rosettes and buds filling the gaps. The flowers in cream #EFE6D5 and Ottoman gold #C9A227 with thin charcoal #23201D linework, a few turquoise #2E8B8B petals echoing the bead.

Drawing style: fine detailed ink illustration with confident even line weight and cross-hatched shading, like the dragon on a vintage souvenir shirt — dense, symmetrical, readable from three metres away. Flat spot colours, no gradients, no glow, no 3D rendering.

Print treatment: five flat spot colours only, hard edges. A light even wear texture over all colours — small specks and hairline gaps of missing ink, like a screenprint washed thirty times. The overall shape is roughly a wide upright oval.

Type: underneath the illustration, centred, two lines set in a classic old-style serif like Garamond, regular weight, lowercase except the T, cream #EFE6D5, with the same light wear texture as the illustration:
line 1: "you met me at a very"
line 2: "Turkish time in my life"
Spell it exactly like this, letter by letter. The type block is about as wide as the illustration, tight line spacing, generous letter spacing.
```

### D3: typography in Figma (never generated)

1. Text, verbatim: `you met me at a very Turkish time in my life`.
2. Typeface: **EB Garamond** regular (Google Fonts, OFL, commercial use OK), like the white serif on the original.
3. Two centred lines: `you met me at a very` / `Turkish time in my life`. Width ≈ 85% of the motif, line spacing 1.05, tracking +20.
4. Colour cream `#EFE6D5` (on the red sweater it reads like the white of the original, just not as harsh).
5. Wear: mask the text with the same speckle texture as the motif. Otherwise it looks pasted on.
6. On DTG/DTF, set the underbase to about 85% so the red shows through and the print looks faded.

### D4: blank sweater photo (mockup base)

```
Photograph of one heavyweight crewneck sweatshirt lying flat on a slightly rough pale concrete floor #CFCAC2, shot from directly above. 400 gsm brushed-back cotton fleece, garment-dyed and washed, faded Anatolian red #B23A2E with uneven tone: lighter on the raised folds and along the seams, darker inside the creases. Round ribbed crew neckline lying flat, sleeves bent loosely inward, the left cuff turned up once to show the soft fleece inside. Ribbed collar, cuffs and hem slightly wavy from washing, flatlock seams, dropped shoulders, one soft diagonal fold across the front body. No hood, no pocket, no zip. Matte cotton surface with visible knit texture and a few loose fibres, no sheen. Completely blank: no print, no logo, no neck label, no text anywhere. Soft overcast daylight from a window on the left, a gentle shadow along the right edge of the garment. 50mm lens, f/8, sharp across the whole garment.
```

### D5: mockup image-to-image (references: D4 photo + print PNG from Figma)

```
Use the first image as the base photo and keep everything in it unchanged: the sweatshirt, its colour, the folds, the concrete floor, the light. Place the artwork from the second image onto the chest of the sweatshirt, centred, about 30 cm wide, top edge 8 cm below the collar. The print must sit in the fabric, not on top of it: it bends over every fold, darkens inside the creases, breaks slightly where the fleece texture shows through, and has the same matte surface as the cotton — screenprinted ink washed many times, no shine, no flat sticker look. Copy the artwork's shapes, colours and the line of type exactly; do not redraw or respell anything.
```
Check the text letter by letter. If it's wrong: place the print in Photoshop instead (Displace + Multiply). Never publish wrong text.

---

## E. Character sheets + locations (GPT Image 2.5, 2k)

PS2 style stays for the characters (briefing). The "original look" only applies to the shirt.

### E1: the host (16:9)
v4: give the mockup from D5 in as a reference image and replace "completely plain — no print, no graphic, no label" in the prompt with "wearing exactly the printed crewneck sweatshirt from the reference image, the nazar print on the chest".
```
Character turnaround sheet: three full-body views of the same man standing side by side on a flat mid-grey #8A8580 background — front view, left side profile, back view. Even spacing, feet on one shared ground line, arms relaxed at his sides, neutral standing pose. No text, no labels, no numbers, no logos anywhere on the sheet.

The man: Turkish, mid-thirties, broad stocky build, wide shoulders, thick forearms, weathered mature face with sun creases at the corners of the eyes, full dark beard with a heavy moustache covering the upper lip, short cropped dark hair, deep-set dark eyes under thick eyebrows. Calm deadpan expression, mouth closed, no smile.

Clothing: heavyweight 400 gsm cotton fleece crewneck sweatshirt, no hood, garment-washed, faded Anatolian red #B23A2E, completely plain — no print, no graphic, no label. The red is lighter along the seams and cuff edges where the dye has washed out, round ribbed collar sitting close at the base of the neck, ribbed cuffs pushed a little up the forearms. Dark tobacco-brown #4A3524 work trousers, straight cut, slight wear at the knees. Worn brown leather boots with scuffed toes. A thin gold chain #C9A227 at the neck holding one small glass nazar bead (deep navy #1B2A4A outer ring, white ring, turquoise #2E8B8B centre), the size of a fingernail.

Palette: the red #B23A2E and the navy/turquoise of the nazar are the only strong colours; skin, trousers, boots and background stay desaturated.

PS2-era real-time game render: low-poly geometry with visible hard polygon edges, faceted flat-shaded surfaces, 64-256px low-resolution textures, dithered color gradients, harsh vertex lighting with no rim light, subtle aliasing, 4:3 framing, muted saturated palette.
```

### E2: the visitor (16:9)
```
Character turnaround sheet: three full-body views of the same man standing side by side on a flat mid-grey #8A8580 background — front view, left side profile, back view. Even spacing, feet on one shared ground line, arms close to the body, slightly stiff posture. No text, no labels, no numbers, no logos anywhere on the sheet.

The man: German, late twenties, tall and thin, narrow sloping shoulders, long neck, pale skin with a pink sunburn on the nose, forehead and back of the neck. Short ash-blond hair with a neat side part, clean-shaven, thin rectangular metal glasses. Polite tense expression: eyebrows slightly raised, lips pressed together.

Clothing: short-sleeved button-up shirt in pale washed blue #A9B8C6 with a faint grey check, tucked in, one pen clipped in the chest pocket. Beige cotton chino shorts #C8B99A to just above the knee, brown braided belt. White sports socks pulled up to mid-calf inside brown leather sandals. An old silver compact digital camera hanging on a black nylon strap around his neck, resting on his chest. Thin black digital wristwatch.

Palette: pale blue and beige, desaturated; the only saturated accents are the pink sunburn and the silver camera. He must read as the cool, washed-out counterpart to a man in faded red.

PS2-era real-time game render: low-poly geometry with visible hard polygon edges, faceted flat-shaded surfaces, 64-256px low-resolution textures, dithered color gradients, harsh vertex lighting with no rim light, subtle aliasing, 4:3 framing, muted saturated palette.
```

The sheets are 16:9: set the format in the tool. It overrides "4:3 framing" in the style line.

### E3: lokanta, evening (4:3)
```
Interior of a small Turkish lokanta in the evening, completely empty, no people. Camera at seated eye height, looking across one small square table toward the back wall.

Foreground: the table, covered with a turquoise-and-white checked oilcloth, two simple wooden chairs facing each other across it. On the table: two empty tulip-shaped tea glasses on small saucers, a steel napkin holder, a white plate of lemon wedges, a red plastic basket of sliced white bread, a glass salt shaker.

Back wall: lower half white square tiles with one band of turquoise #2E8B8B patterned tiles, upper half painted pale cream. A steam-table counter along the wall: stainless steel trays of beans in tomato sauce, rice, stewed aubergine, a stack of white plates, a large double-stacked steel teapot on a burner. A small wall-mounted TV high in the corner showing a blurry green football pitch. A window on the right shows a dark street with one orange street lamp.

Light: warm tungsten bulbs in plain glass shades hanging over the tables, a cooler white strip light above the counter. All signs, menus and price boards are blank or unreadable — no text anywhere.

Palette: turquoise #2E8B8B and warm tungsten amber dominate; everything else desaturated cream, steel and wood.

PS2-era real-time game render: low-poly geometry with visible hard polygon edges, faceted flat-shaded surfaces, 64-256px low-resolution textures, dithered color gradients, harsh vertex lighting with no rim light, subtle aliasing, 4:3 framing, muted saturated palette.
```

### E4: coastal road at dusk (4:3)
```
A two-lane asphalt coastal road at dusk, completely empty, no cars, no people. Camera high on the hillside above the road, looking down and across. The road curves along a steep slope; a white-and-red metal guardrail on the sea side, dry grass and three gnarled olive trees on the hill side, a low stone retaining wall.

Below the road: dark calm sea. Across the bay, on the far shore: a city glowing with thousands of small warm lights stacked up the hills, their reflections stretched into lines on the water.

Sky: deep navy #1B2A4A overhead fading to one thin band of burnt orange at the horizon behind the city. Two orange sodium street lamps on the road just switched on.

No text, no road signs with writing, no billboards.

Palette: navy #1B2A4A and warm orange city light dominate; road, hill and trees desaturated grey-green.

PS2-era real-time game render: low-poly geometry with visible hard polygon edges, faceted flat-shaded surfaces, 64-256px low-resolution textures, dithered color gradients, harsh vertex lighting with no rim light, subtle aliasing, 4:3 framing, muted saturated palette.
```

### E5: stone terrace at sunset (4:3)
```
A stone terrace of an old hillside house above the sea at sunset, completely empty, no people. Camera at standing eye height at the back of the terrace, looking out toward the sea.

Floor of large uneven honey-coloured limestone slabs with dry moss in the joints. A low stone wall along the edge, waist high. Overhead, a wooden pergola with a grapevine, its leaves throwing a pattern of small shadows on the floor. On the left: a small round metal table with a double-stacked steel teapot, two tulip-shaped tea glasses on saucers, a bowl of green olives; two low wooden stools with woven straw seats beside it. A terracotta pot of red geraniums on the wall.

Beyond the wall: terraced hills dropping to the sea, a few white houses, the sun low and large just above the hills on the right, the sea turning gold-orange near the horizon, turquoise #2E8B8B close to the shore.

No text anywhere.

Palette: warm sunset gold #C9A227 and turquoise #2E8B8B dominate; stone and wood desaturated.

PS2-era real-time game render: low-poly geometry with visible hard polygon edges, faceted flat-shaded surfaces, 64-256px low-resolution textures, dithered color gradients, harsh vertex lighting with no rim light, subtle aliasing, 4:3 framing, muted saturated palette.
```

---

## F. Seedance 2.5: ONE prompt for all 19 s

**Settings:** `seedance_2_5` · `mode: omni_reference` · `duration: 19` · `aspect_ratio: 9:16` · `generate_audio: true` · test with `draft: true`, final via `draft_job_id` at 1080p.

**References (`image_references` / `audio_references`):**
`@host` = E1 · `@visitor` = E2 · `@lokanta` = E3 · `@road` = E4 · `@terrace` = E5 · `@dialogue` = dialogue.mp3 (19 s). Optional `@storyboard` = 15-panel sheet as a shot guide.

```
A 19-second vertical short film in six shots with hard cuts, PS2-era real-time game cutscene look: low-poly geometry with visible hard polygon edges, faceted flat-shaded surfaces, 64-256px low-resolution textures, dithered color gradients, harsh vertex lighting with no rim light, subtle aliasing, slightly stiff game-engine animation, muted saturated palette.

Characters, fixed for the whole film:
The host (@host) — broad stocky Turkish man, mid-thirties, full dark beard and heavy moustache, plain faded red #B23A2E crewneck sweatshirt with no print, thin gold chain with a small nazar bead. He never smiles.
The visitor (@visitor) — tall thin German man, late twenties, thin rectangular glasses, sunburnt nose, pale blue short-sleeved shirt, silver compact camera on a strap around his neck.
Voices and timing follow @dialogue.

SHOT 1 — 0.0–3.5s — lokanta (@lokanta), evening. Static wide two-shot at seated eye height, very slow push-in. The host sits on the left, leaning back, one arm hooked over the back of his chair, completely at ease. The visitor sits upright on the right, hands flat on the table, turning his head to look at the steel food trays on the counter and back. Between them the table is covered with plates: kebab, mezze, flatbread, salad, half-empty tea glasses — far more food than two people can eat. Sound: spoons clinking in tea glasses, a TV murmuring.

HARD CUT. SHOT 2 — 3.5–6.5s — same lokanta. Close-up of the visitor from the chest up. He holds a tiny paper receipt, no bigger than a business card, with both hands close to his glasses, eyes widening; he turns it over to look at the blank back, then looks up. The visitor says, whispering and rushed: "Sorry — is this the whole bill? I think there's a mistake."

HARD CUT. SHOT 3 — 6.5–10.5s — same lokanta. Medium two-shot. The host crosses his arms, face completely flat, sighs. Without looking, he lifts a steel teapot and pours dark amber tea into the visitor's glass; steam rises. The visitor keeps staring at the tiny receipt. The host says, dry and slow: "Kardeşim. That's just Turkey. You'll get used to it."

HARD CUT. SHOT 4 — 10.5–13.0s — coastal road (@road) at dusk. High side angle from the hillside, slow pan following a dark boxy 1990s sedan with no badges driving left to right along the curve. The driver's window is down; the host's forearm in the faded red sweatshirt sleeve rests on the window frame. City lights glow across the bay and reflect on the water. Sound: engine hum, wind.

HARD CUT. SHOT 5 — 13.0–16.0s — stone terrace (@terrace) at sunset. Slow lateral dolly left to right. The host stands in the foreground on the left, waist-up, still, looking straight into the camera. Behind him, small and in soft focus, the visitor stands at the low stone wall with his back half turned, holding a tea glass with both hands, looking at the sea and the low sun; his shoulders drop with one long sigh.

HARD CUT. SHOT 6 — 16.0–19.0s — same terrace. Slow push-in from medium shot to close-up on the host's face. Golden sun from the right on one side of his face, turquoise sea out of focus behind him. He holds eye contact with the camera and says, dry and slow: "You met me at a very Turkish time in my life." On the last word one eyebrow lifts very slightly.

Palette for the whole film: faded red #B23A2E and turquoise #2E8B8B dominant; navy #1B2A4A in the dusk shot, gold #C9A227 in the sunset shots; everything else desaturated.

Keep fixed across all shots: both faces, the beard, glasses, sunburn, both outfits, the gold chain and nazar bead, the sweatshirt stays plain red with no print, the receipt stays tiny, no other main characters.

No on-screen text, no subtitles, no captions, no logos, no watermark. Any writing on paper, signs or screens is blurred and unreadable.
```

**Sweater in the video:** the host wears the plain red sweater (Seedance distorts print text). The product shows up after shot 6 as an end card: sample photo or D5 mockup.

### F2: 15-panel storyboard (GPT Image 2.5, 2k, 16:9) · refs: @host @visitor @lokanta @road @terrace

```
Storyboard sheet of 15 panels in a grid of 5 columns and 3 rows, thin black gutters, all panels the same size, vertical 9:16 panels. No text, no numbers, no captions, no speech bubbles anywhere. The same two characters in every panel: the host (@host) — broad bearded Turkish man in a plain faded red #B23A2E crewneck sweatshirt with a gold chain and small nazar bead; the visitor (@visitor) — thin German man with glasses, pale blue short-sleeved shirt and a silver camera on a strap.

Row 1:
1. Wide two-shot in the lokanta (@lokanta) at night: the host leans back relaxed, the visitor sits upright, two empty tea glasses between them.
2. The visitor turns to look at the steam-table counter with steel trays of food.
3. Close-up of a hand placing a tiny paper receipt, the size of a business card, on the checked oilcloth.
4. Close-up of the visitor holding the tiny receipt near his glasses, eyes wide.
5. Insert: the visitor's fingers turning the tiny receipt over, the back is blank.

Row 2:
6. Medium two-shot: the host leans back, arms crossed, face flat; the visitor stares at the receipt.
7. The host pours tea from a steel teapot into the visitor's glass without looking at it.
8. The visitor still staring at the receipt, a full steaming tea glass beside his hand.
9. High side view of a dark boxy 1990s sedan on the coastal road (@road) at dusk, city lights across the bay.
10. Close-up of a red sweatshirt sleeve resting on the open driver's window, the sea blurred behind.

Row 3:
11. Wide shot of the stone terrace (@terrace) at sunset: the host in the foreground left, the visitor small at the wall in the background.
12. The visitor from behind, holding a tea glass with both hands, facing the sea and the low sun.
13. The host waist-up, looking straight into the lens, flat face.
14. Medium close-up of the host, deadpan, golden light on one side of his face.
15. Tight close-up of the host, one eyebrow slightly raised.

Palette across the sheet: faded red #B23A2E and turquoise #2E8B8B dominant, navy #1B2A4A in the night panels, gold #C9A227 in the sunset panels, everything else desaturated.

PS2-era real-time game render: low-poly geometry with visible hard polygon edges, faceted flat-shaded surfaces, 64-256px low-resolution textures, dithered color gradients, harsh vertex lighting with no rim light, subtle aliasing, muted saturated palette.
```

---

## G. Three hooks for the first TikTok post

| | A: Format 1:1 | B: The tiny receipt | C: Line first |
|---|---|---|---|
| **First 2 s** | Shot 1, caption "My friend came to Turkey for the first time." from frame 1 | Shot 2 (receipt gets turned over) + caption "He saw the prices…", then shot 1 → rest | Shot 6 with the line, hard cut to shot 1, the line returns at the end |
| **Post caption** | `you met me at a very turkish time in my life 🇹🇷` | `he asked for the rest of the bill 🧾🇹🇷` | `my friend, that's just Turkey.` |
| **Trigger** | Trend recognition: anyone who knows the Swiss/Chinese version waits for the line; Turkish Germans tag friends | Price debate ("how much?!", "not cheap for us"). Risk: inflation is a sore subject | Identity line + loop, watched twice |

**Bet: A.** It copies the structure that made 2.4M, and on a new account recognition works better than a reshuffled order. Post B and C on days 2–3.
**Expectation:** 300–2,000 views, estimate ~800. Above 10k = the format carries. What decides the bet are shop clicks, not views. Turn on TikTok's "AI-generated content" label (EU AI Act).
