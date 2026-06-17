# The Last Train Never Came — Ren'Py edition

This is the same story as the single-file HTML game (`../the-last-train.html`),
ported to **Ren'Py** so it can be built into a real, installable app.

You are **Kali**. You explore a ruined transit station overnight with **Emy**,
examining objects and unlocking dialogue. Every so often the game slips into a
cold-blue *flash* of Emy's unspoken thoughts. Your choices lead to one of five
endings (radiant, hopeful, bittersweet, distant, severed).

## Run it (about 5 minutes of setup)

1. Download **Ren'Py 8** (free, Windows/Mac/Linux) from <https://www.renpy.org/>
   and install it. Launch the Ren'Py launcher. (Use version 8 — the rain,
   mist, blur and color-grade effects rely on its modern renderer.)
2. In the launcher, click **Create New Project**, give it a name, and finish
   the wizard. Ren'Py makes a project folder containing a `game/` subfolder.
3. Copy **`game/script.rpy`** from here over the `game/script.rpy` in your new
   project (replace the file).
4. Select the project in the launcher and press **Launch Project**. It runs.

## Turn it into an app

In the launcher, with the project selected:

- **Build Distributions** → tick Windows / Mac / Linux → **Build**.
  You get double-clickable apps (e.g. a Windows `.exe`, a Mac `.app`).
- **Build Web** makes a browser version you can host or share via a link.
- Android/iOS are supported too (a bit more setup — see the Ren'Py docs).

## What the graphics already do

This version leans on Ren'Py's GPU rendering, so it ships with real atmosphere
and **no image files needed**:

- **Particle rain** (two depth layers) via Ren'Py's `SnowBlossom`.
- **Blurred drifting mist** along the floor.
- **Random distant lightning** flashes.
- A **blurred twilight gradient** background and a unifying cool color grade
  (`matrixcolor`), plus a blurred cold wash during Emy's flashes.
- Characters composited from parts (Emy: brown hair + mossy coat; Kali: short
  black hair, glasses, dusk-violet coat).

All of this is defined in the art block near the top of `script.rpy`.

## Making it prettier (optional, later)

- **Real portraits / backgrounds:** replace the `image bg station = ...` and
  `image emy_fig = ...` / `image kali_fig = ...` lines with PNGs, e.g.
  `image kali_fig = "kali.png"`. Drop the PNGs into the `game/` folder. The
  rain/mist/lightning overlay keeps working over real art automatically.
  - Emy: medium brown hair, scrappy/mossy layers.
  - Kali: short black hair, clear-framed round glasses.
- **Music:** the music is already wired up. Drop a looping track at
  `game/audio/theme.ogg` and it plays automatically on startup (3s fade-in),
  with a corner ♪ button to mute/unmute. No file = silence, no crash. See
  `game/audio/PUT_MUSIC_HERE.txt` for free sources. (Ren'Py can't synthesize
  audio like the HTML version — it needs an actual sound file.)

## Editing the story

All dialogue is plain text inside `game/script.rpy`. Each object is its own
`label obj_*`, each decision is a `menu:`, and the five endings are the
`label ending_*` blocks. Edit the strings freely.
