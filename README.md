# Digimon Animations & Profiles

Every Digimon's idle, walking, attack and faint animations as ready-to-play
frames, plus a bilingual profile of each Digimon (English and 中文). Help us
fill in the profiles and choose which animations to add next!

> The Digimon artwork belongs to Bandai Namco. This is a non-commercial fan
> project; the sprites are shared for fan use only.

## What's here

```
baked/<digimon>/<animation>/f_NNN.png    every animation as ready-to-play frames
digimon.json                            every Digimon's name, stage, attribute, type,
                                        evolutions and description
sprites/<digimon>/<digimon>_<n>.png     the original sprite sheets, cut into single frames
corrections.json                        fixes for frames in sprites/
```

## The baked frames

The frames in `baked/` are rendered from the game's own animations, so every
pose, jump and effect is already in the right order. Each Digimon has four
animations:

| folder | animation |
|---|---|
| `idle` | standing still, breathing |
| `walking` | walking (or flying) on the spot |
| `attack` | the attack move |
| `faint` | falling down when beaten |

Play `f_000.png`, `f_001.png`, … in order, each for **62.5 ms** (16 frames a
second); the number of files is the length of the animation. `idle`,
`walking` and `attack` loop; `faint` plays once and stays on its last frame.
All frames of one Digimon are the same size and share one origin, so stack
them without moving them.

Some Digimon come in more than one look, named `<digimon>_<version>`:
`agumon_adventure` is Agumon from Digimon Adventure, `gekkomon_runevent_fever`
a Gekkomon from an event.

## `digimon.json`

One profile per Digimon, in the wording of the official Digimon Encyclopedia
at [digimon.net](https://digimon.net/reference_en/). Its `folder` is the
folder name in `baked/`; a version like `agumon_adventure` uses the profile of
`agumon`. Agumon's profile, shortened:

```json
{
  "folder": "agumon",
  "name": { "en": "Agumon", "zh": "亞古獸" },
  "stage": { "en": "Rookie", "zh": "成長期" },
  "attribute": { "en": "Vaccine", "zh": "疫苗種" },
  "type": { "en": "Reptile", "zh": "爬蟲類型" },
  "evolves_from": ["koromon"],
  "evolves_to": ["greymon", "numemon[mistake]", "wargreymon[warp]"],
  "description": { "en": "...", "zh": "..." },
  "source": "https://digimon.net/reference_en/detail.php?directory_name=agumon"
}
```

| key | values |
|---|---|
| name, attribute, type, description | `en` English, `zh` Traditional Chinese; add `zh_hans` for Simplified if you like |
| stage | `Baby I` 幼年期Ⅰ, `Baby II` 幼年期Ⅱ, `Rookie` 成長期, `Champion` 成熟期, `Ultimate` 完全體, `Mega` 究極體, `Mega+` 究極體 or `Armor` 裝甲體 |
| attribute | `Vaccine`, `Data`, `Virus`, `Free` or `Unknown`; empty for Baby I and II |
| evolves_from, evolves_to | other Digimon by `folder`, each of which needs its own profile |
| source | the Digimon's page on digimon.net |

An evolution can carry a tag saying how it happens: `[dark]`, `[mistake]`
(care mistake), `[warp]`, `[armor]` or `[mode]` (mode change). A fusion (DNA
digivolution) is `exveemon+stingmon` in `evolves_from`, and
`paildramon(+stingmon)` in `evolves_to`.

## How to help

1. **Write a missing profile.** Some Digimon in `baked/` have none yet.
2. **Fill in or fix a profile:** an empty field, a wrong stage, a missing
   evolution, a better translation, Simplified Chinese names.
3. **Ask for more animations** (see below).
4. **Fix a sprite** in `sprites/` that's sideways or cut wrong (see below).

To see what's missing right now, run this in the repo folder (Python 3):

```bash
python .github/scripts/profiles.py todo
```

Before sending a profile change, check it (GitHub runs the same check on your
pull request):

```bash
python .github/scripts/profiles.py check
```

When you add a profile, add the evolution on both ends, for example `veemon`'s
`evolves_to` and `magnamon`'s `evolves_from`.

## More animations

The game has more animations than the four in `baked/`:

| animation | which Digimon |
|---|---|
| stun (hit, staggering) | every Digimon |
| evolve (the evolution glow) | 90 Digimon |
| jump, fall, slide | the Gekkomon event versions |
| run_fever (fast run) | `gekkomon`, `gekkomon_runevent_shadow` |

Want one of them, or does a baked animation look wrong (a missing part, an
effect cut off)? Open an issue with the **More animations** form and say which
Digimon, which animation, and what you'd use it for. The most requested ones
get added to `baked/`.

## Fixing a sprite (rotate, flip, crop)

Some frames are stored sideways, upside down, facing the wrong way, or with
extra bits around them. Don't edit the picture yourself. Add it to the
`"pending"` list in `corrections.json` instead:

```json
{
  "pending": [
    { "file": "agumon/agumon_26.png", "rotate": 180, "note": "upside down", "by": "your-github-name" },
    { "file": "gabumon/gabumon_25.png", "rotate": 90, "flip": "horizontal" },
    { "file": "palmon/palmon_31.png", "crop": [0, 0, 12, 0], "note": "bit of another frame on the right" }
  ],
  "applied": []
}
```

| key | values |
|---|---|
| file | the sprite, inside `sprites/` |
| rotate | `90`, `180` or `270`, turning clockwise |
| flip | `"horizontal"` (mirror left-right) or `"vertical"` (upside down) |
| crop | `[left, top, right, bottom]`: pixels to cut off each side |
| note, by | optional: what's wrong, and who found it |

Use any of rotate, flip and crop together. They happen in that order, so
count crop pixels on the picture after it has been turned.

When you open a pull request, GitHub checks your entries and tells you if one
is wrong (a file that doesn't exist, a rotate of 45...). Once it is merged into `dev`,
GitHub fixes the sprites by itself in a follow-up pull request and moves
your entries to `"applied"`, so
everyone can see what was changed.

## Branches and sending changes

| branch | what it is |
|---|---|
| `main` | the released version: what you see on the repo's front page. Use it if you just want the frames and profiles. |
| `dev` | where new work goes. Start your changes from here. |

To contribute, fork the repo (untick **Copy the `main` branch only**, so your
fork gets `dev` too), then work from `dev`:

```bash
git clone https://github.com/<your-github-name>/digimon-up-sprites.git
cd digimon-up-sprites
git switch dev
git switch -c my-change
```

Open your pull request against **`dev`**, not `main`: GitHub picks `main`
by default, so change the base branch to `dev` when you create it. The owner
reviews every change, and `dev` is merged into `main` from time to time.
