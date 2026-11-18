# SoloMeter

Blizzard's built-in damage meter for WoW Forever, showing only you.

- Teammates' rows are hidden. Your row sits at the top, without a rank number, and its bar is always full.
- The window shrinks to its header plus your row (Edit Mode's Frame Height won't go below 120).
- Enemy Damage Taken and the Edit Mode preview are left as Blizzard draws them.
- Clicking your row still opens your spell breakdown.

It only changes what's drawn, never Blizzard's data, so the meter keeps working in combat.

**Tip:** with Numbers set to "Complete", your row still shows your % of the group's total. Pick Minimal or Compact in Edit Mode to hide it.

## Install

Use [Forever Addon Manager](https://github.com/Pwizzlard/FAM-releases), or unzip the latest [release](https://github.com/Pwizzlard/SoloMeter/releases) into `World of Warcraft\_forever_\Interface\AddOns`, so you get `Interface\AddOns\SoloMeter\SoloMeter.toc`. Turn the damage meter on in Edit Mode if it isn't already.

## Develop

- `python test_solometer.py` runs the self-check (needs `pip install lupa`).
- `python release.py "notes"` packages the version in the TOC and publishes a GitHub release.
