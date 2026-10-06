# 🎵 Ultimate Matrix Player (UMP)

**English** | [Français](README.fr.md)

![Ultimate Matrix Player](logo.jpg)

**Ultimate Matrix Player** is a very light **MOD, S3M, XM and IT** module player written in
Python, for demoscene, chiptune and Amiga music fans. It combines a retro "Matrix" interface
with a roulette mode that downloads random modules from four online archives:
[The Mod Archive](https://modarchive.org), [Modules.pl](https://www.modules.pl),
[Modland](https://ftp.modland.com/pub/modules/) and [AMP](https://amp.dascene.net).

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
  in the background, so the interface does not freeze. Each source picks from its own site:

  | Source | Site | Categories |
  |---|---|---|
  | ModArchive | [modarchive.org](https://modarchive.org) | All (random module), Chiptune, Demo (the site's "Demo Style" genre) |
  | Modules.pl | [modules.pl](https://www.modules.pl) | S3M, IT, XM (the site's format filter) |
  | Modland | [ftp.modland.com](https://ftp.modland.com/pub/modules/) | Protracker (MOD), Fasttracker 2 (XM), Screamtracker 3 (S3M), Impulsetracker (IT) |
  | Amiga Collection | [AMP – Amiga Music Preservation](https://amp.dascene.net) | All (MOD, XM, S3M or IT), MOD, XM |

  The module is always downloaded from the chosen source's own site: a file that would come
  from another address is refused. Archives are unpacked automatically (zip on Modules.pl,
  gzip on AMP). The file is saved as **`Artist - Title.ext`** with the names given by the site
  (just `Title.ext` when the artist is unknown), and its extension comes from its actual
  contents.
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
Modland = Protracker, Fasttracker 2, Screamtracker 3, Impulsetracker
Amiga Collection = All, MOD, XM

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

Modules downloaded by the roulette are stored in the **`WebMods/`** folder, named
`Artist - Title.ext` (for example `Purple Motion - Aquaphobia.s3m`). If a different module
already has that name, ` (2)`, ` (3)`… is added. The folder is not emptied automatically, but the
files are small. The folder also holds `modland_allmods.zip`, Modland's list of files (about
6 MB), downloaded the first time Modland is used and refreshed once a week.

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

- **Roulette sources**: the player reads the sites' web pages (ModArchive, Modules.pl) or
  their download links (Modland, AMP). If a site changes its layout, its source can stop
  working until the player is updated; the roulette then shows "No module downloaded".
- **Amiga Collection (AMP)**: the module is drawn from a fixed range of numbers (1 to 185,000,
  about 182,500 in October 2026). Modules added beyond that are not drawn. Most of AMP is in
  Amiga formats the player cannot read: only MOD, XM, S3M and IT files are kept.
- **Modland**: the first use downloads the list of files (about 6 MB), so the first draw takes
  a few seconds longer.
- The roulette makes up to 6 draws if a link is dead or the module is in an unsupported
  format. It gives up at once if the network is down.
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
- **Real roulette sources**: Modules.pl, Modland and Amiga Collection (AMP) now pick a module
  on their own site instead of The Mod Archive's catalogue. Modland's categories are now
  Protracker, Fasttracker 2, Screamtracker 3 and Impulsetracker (instead of "Exotic"), and
  Amiga Collection offers All, MOD and XM.
- Fix: ModArchive's search by category no longer worked: the API address it used
  (`xml-search.php`) now answers "404 Not Found". The player now uses the site's genre pages and
  its "random module" page. Also, `config.ini` turned the source names into lower case
  (`modarchive`), so the check for `ModArchive` never matched.
- zip (Modules.pl) and gzip (AMP) archives are unpacked. Files packed with an Amiga packer
  (PowerPacker…) are no longer taken for a MOD.
- Downloaded modules are named `Artist - Title.ext` from the site's information, and each
  source only accepts a file coming from its own site.
- Fix: a downloaded module's type is detected from its contents. An XM is no longer saved as
  `.mod`, and an error page is no longer saved as a module.
- Fix: a playlist where no file can be played no longer crashes the program (endless
  recursion).
- The roulette downloads in the background, so the interface no longer freezes. It makes up
  to 6 draws if a link is dead or the module cannot be played.
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
[The Mod Archive](https://modarchive.org), [Modules.pl](https://www.modules.pl),
[Modland](https://ftp.modland.com) and [AMP](https://amp.dascene.net) for their collections.
