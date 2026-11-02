# Digimon Sprites & Animation Sequences

Sprites of the Digimon, cut into single frames, plus a table of which frames
make up each animation. Help us find the right order for every Digimon!

> The Digimon artwork belongs to Bandai Namco. This is a non-commercial fan
> project; the sprites are shared for fan use only.

## What's here

```
sprites/<digimon>/<digimon>_<n>.png     the frames of one Digimon
sprites/<digimon>_2/<digimon>_2_<n>.png  an extra sheet of the same Digimon
sequences.csv                           the animation table
digimon.json                            every Digimon's name, stage, attribute, type,
                                        evolutions and description (English and 中文)
```

`digimon.json` uses the wording of the official Digimon Encyclopedia at
[digimon.net](https://digimon.net/reference_en/); each entry links to its page
in `source`.

## How to read `sequences.csv`

| column | meaning |
|---|---|
| digimon name | the folder name in `sprites/` |
| stage | Baby, In-Training, Rookie, Champion, Ultimate or Mega |
| idle | standing still, breathing |
| walking | walking (or flying) on the spot |
| attack | the attack move |
| faint/knock down | falling down when beaten |

Each animation is a list of frame numbers in play order, separated by spaces.

- `13` means `sprites/agumon/agumon_13.png`
- `2:16` means frame 16 of the extra sheet: `sprites/garudamon_2/garudamon_2_16.png`

Every frame is shown for about 0.13 seconds, then the list loops.

An empty cell means nobody has worked it out yet.

## How to help

1. Watch the Digimon in the game's encyclopedia (or a recording of it).
2. Open the Digimon's folder in `sprites/` and find the frames that match each pose.
3. Fix or fill in the row in `sequences.csv`.
4. Send your change (pull request or issue), and say which Digimon and animation you checked.

Wanted most:

- **faint/knock down** for every Digimon (all empty)
- the rows for Digimon that aren't in the table yet
- double-checking: Tentomon walking, MegaKabuterimon walking, Phoenixmon idle
  and attack, HerculesKabuterimon walking and attack, Kabuterimon attack

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

When you open a pull request to the `dev` branch, GitHub checks your entries and tells you if one
is wrong (a file that doesn't exist, a rotate of 45...). Once it is merged,
GitHub fixes the sprites by itself in a follow-up pull request and moves
your entries to `"applied"`, so
everyone can see what was changed.

## Sending changes

Open your pull request against the **`dev`** branch. The owner reviews every
change, and `dev` is merged into `main` from time to time.
