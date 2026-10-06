# 🎵 Ultimate Matrix Player (UMP)

**English** | [Français](README.fr.md)

![Ultimate Matrix Player](logo.jpg)

**Ultimate Matrix Player** is a very light **MOD, S3M, XM and IT** module player written in
Python, for demoscene, chiptune and Amiga music fans. It combines a retro "Matrix" interface
with a roulette mode that downloads modules from [The Mod Archive](https://modarchive.org).

**Current version: V1.6** (script `UMPV16.pyw`). What's new is in the [changelog](#changelog).

---

## Contents

1. [Features](#features)
2. [Screenshots](#screenshots)
3. [Installing and running](#installing-and-running)
4. [Usage](#usage)
5. [The `config.ini` file](#the-configini-file)
6. [Building a Windows executable (.exe)](#building-a-windows-executable-exe)
7. [Repository layout](#repository-layout)
8. [Known limitations](#known-limitations)
9. [Changelog](#changelog)
10. [Credits and licence](#credits-and-licence)

---

## Features

- **Module name display**: the title stored inside the file (the name the musician gave the
  song on the Amiga or PC) is shown in yellow under the control bar, in the window title bar
  and in the playlist. If the module has no title, the file name is shown.
- **Formats**: MOD (Amiga, 4 to 32 channels, including old 15-instrument MODs), S3M, XM and IT.
- **Roulette mode [R]**: downloads a random module and plays it right away. The download runs
  in the background, so the interface does not freeze.
- **Three interface sizes**, cycled with the button on the right:
  - **Full** (large): logo, module name, 8 "Matrix" channel columns, VU meters and playlist;
  - **Mini** (medium): module name, VU meters and playlist;
  - **Nano**: just the control bar. The module name stays in the window title bar.
- **Playlist**: add your local files with **ADD**, then double-click a line to play it.
- **Settings saved** in `config.ini`: interface size, playlist visibility, chosen source and
  category.

## Screenshots

| Full | Mini | Nano |
|---|---|---|
| ![Full mode](Exemple_grand.png) | ![Mini mode](Exemple_medium.png) | ![Nano mode](Exemple_nano.png) |

*(These screenshots were taken with V1.5, before the module name line was added.)*

## Installing and running

You need **Python 3** and two libraries:

```bash
pip install pygame pillow
```

Then run the script:

```bash
python UMPV16.pyw
```

On Windows, double-clicking `UMPV16.pyw` is enough (the `.pyw` extension avoids opening a
console window).

> Pillow is only used to show the logo: the player still works without it.
> On Linux, pygame needs `libmodplug` to play modules (`sudo apt install libmodplug1` on
> Debian/Ubuntu).

## Usage

| Button | Action |
|---|---|
| **PLAY** / `>` | Plays the current track, resumes after a pause, or opens the file picker if the playlist is empty |
| **PAUSE** / `\|\|` | Pauses |
| **STOP** / `■` | Stops playback |
| **NEXT** / `>>` | Skips to the next track |
| **ROULETTE [R]** | Downloads and plays a random module (source and category from the drop-down menus) |
| **LIST** | Shows or hides the playlist |
| **ADD** | Adds local files to the playlist |
| `-` / `--` / `+` | Changes the interface size (Full → Mini → Nano) |

Double-click a playlist line to play that track. Playback moves on to the next track
automatically and loops back to the start at the end of the list.

## The `config.ini` file

It is created next to the script (or the executable) on first launch:

```ini
[SOURCES]
ModArchive = All, Chiptune, Demo
Modules.pl = S3M, IT, XM
Modland = Exotic
Amiga Collection = All

[SETTINGS]
mode = full
show_list = True
delay = 80
source = ModArchive
category = All
```

| Setting | Meaning |
|---|---|
| `mode` | Interface size: `full`, `mini` or `nano` |
| `show_list` | Shows the playlist (`True` / `False`) |
| `delay` | Animation refresh, in milliseconds (minimum 20) |
| `source`, `category` | Last chosen source and category |

The `[SOURCES]` section is rewritten on every launch. The `[SETTINGS]` values are saved when
the window is closed.

Modules downloaded by the roulette are stored in the **`WebMods/`** folder. It is not emptied
automatically, but the files are small.

## Building a Windows executable (.exe)

With [PyInstaller](https://pyinstaller.org), to get a standalone `.exe` with the logo and the
icon built in:

```bash
pip install pyinstaller
python -m PyInstaller --noconsole --onefile --add-data "logo.jpg;." --icon="Matrix.ico" UMPV16.pyw
```

The executable is then in the `dist/` folder. It creates its `config.ini` and `WebMods/` folder
next to itself.

## Repository layout

```
.
├── UMPV16.pyw          player source code
├── logo.jpg            banner shown in Full mode (built into the .exe)
├── Matrix.ico          executable icon
├── Exemple_*.png       screenshots of the three modes
├── README.md           this file
└── README.fr.md        French documentation
```

Created at run time (not in the repository): `config.ini` and the `WebMods/` folder.

## Known limitations

- **Roulette sources**: only **ModArchive** does a real search by category (All, Chiptune,
  Demo). The **Modules.pl**, **Modland** and **Amiga Collection** entries currently pick a
  random module from The Mod Archive's catalogue: they do not query those sites yet.
- **"Matrix" animation**: the scrolling notes and the VU meters are decorative. They do not
  reflect what the module is actually playing.
- **Time display**: it counts from the start of the track, with no total length (pygame does
  not provide it for modules).
- Downloads use HTTPS **without certificate verification**, to avoid certificate errors on some
  Windows installations.

## Changelog

### V1.6
- The **module name** (title stored in the MOD, S3M, XM or IT file) is shown under the control
  bar, in the window title bar and in the playlist.
- Fix: the ModArchive category search never ran. `config.ini` turned the source names into
  lower case (`modarchive`), so the check for `ModArchive` never matched.
- Fix: a downloaded module's type is detected from its contents. An XM is no longer saved as
  `.mod`, and an error page is no longer saved as a module.
- Fix: a playlist where no file can be played no longer crashes the program (endless
  recursion).
- The roulette downloads in the background, so the interface no longer freezes. On the
  "random" sources it makes up to 5 attempts if the picked ID does not exist.
- Double-click a playlist line to play it. The current track is highlighted.
- The chosen source and category are remembered. The `delay` setting in `config.ini` is now
  used.
- The file picker filters modules (`*.mod`, `*.s3m`, `*.xm`, `*.it`, and the Amiga `mod.*`
  naming).
- STOP resets the counter to `00:00`.

### V1.5
- First published version: three display modes, roulette, playlist and `config.ini`.

## Credits and licence

Free to use for all tracker music fans.

Enjoy the music! Popov (but not Russian), 2026.

Thanks to [Gemini](https://gemini.google.com) for its valuable help, and to
[The Mod Archive](https://modarchive.org) for its catalogue.
