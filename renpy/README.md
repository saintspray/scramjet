# The Last Train Never Came — Ren'Py edition

This is the same story as the single-file HTML game (`../the-last-train.html`),
ported to **Ren'Py** so it can be built into a real, installable app.

You are **Kali**. You explore a ruined transit station overnight with **Emy**,
examining objects and unlocking dialogue. Every so often the game slips into a
cold-blue *flash* of Emy's unspoken thoughts. Your choices lead to one of five
endings (radiant, hopeful, bittersweet, distant, severed).

## Run it (about 5 minutes of setup)

1. Download **Ren'Py** (free, Windows/Mac/Linux) from <https://www.renpy.org/>
   and install it. Launch the Ren'Py launcher.
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

## Making it prettier (optional, later)

The art and music are placeholders so it runs with zero extra files:

- **Portraits / backgrounds:** replace the `image bg station = ...` and
  `image fig emy = ...` / `image fig kali = ...` lines near the top of
  `script.rpy` with real PNGs, e.g. `image fig kali = "kali.png"`. Drop the
  PNGs into the `game/` folder.
  - Emy: medium brown hair, scrappy/mossy layers.
  - Kali: short black hair, clear-framed round glasses.
- **Music:** add a track to `game/` and uncomment/add `play music "song.ogg"`
  near `label start`. (Ren'Py can't synthesize audio like the HTML version's
  generated soundtrack — it needs an actual sound file.)

## Editing the story

All dialogue is plain text inside `game/script.rpy`. Each object is its own
`label obj_*`, each decision is a `menu:`, and the five endings are the
`label ending_*` blocks. Edit the strings freely.
