# 🎵 Ultimate Matrix Player (UMP)

[English](README.md) | **Français**

![Ultimate Matrix Player](logo.jpg)

**Ultimate Matrix Player** est un lecteur de modules **MOD, S3M, XM et IT** très léger, écrit en
Python, pour les amateurs de demoscene, de chiptune et de musique Amiga. Il associe une
interface rétro façon « Matrix » à un mode roulette qui télécharge des modules au hasard
depuis quatre archives en ligne : [The Mod Archive](https://modarchive.org),
[Modules.pl](https://www.modules.pl), [Modland](https://ftp.modland.com/pub/modules/) et
[AMP](https://amp.dascene.net).

**Version actuelle : V1.6** (script `UMPV16.pyw`). Les nouveautés sont dans le
[journal des versions](#journal-des-versions).

---

## Sommaire

1. [Fonctionnalités](#fonctionnalités)
2. [Captures d'écran](#captures-décran)
3. [Installation et lancement](#installation-et-lancement)
4. [Utilisation](#utilisation)
5. [Fichier `config.ini`](#fichier-configini)
6. [Créer un exécutable Windows (.exe)](#créer-un-exécutable-windows-exe)
7. [Contenu du dépôt](#contenu-du-dépôt)
8. [Limites connues](#limites-connues)
9. [Journal des versions](#journal-des-versions)
10. [Crédits et licence](#crédits-et-licence)

---

## Fonctionnalités

- **Nom du module affiché** : le titre enregistré dans le fichier (le nom que le musicien a
  donné à son morceau sur Amiga ou PC) s'affiche en jaune sous la barre de commandes, dans
  la barre de titre de la fenêtre et dans la playlist. Si le module n'a pas de titre, c'est
  le nom du fichier qui s'affiche.
- **Formats** : MOD (Amiga, de 4 à 32 voies, y compris les vieux MOD à 15 instruments), S3M, XM
  et IT.
- **Mode roulette [R]** : télécharge un module au hasard et le lance aussitôt. Le
  téléchargement se fait en arrière-plan, sans figer l'interface. Chaque source tire dans son
  propre site :

  | Source | Site | Catégories |
  |---|---|---|
  | ModArchive | [modarchive.org](https://modarchive.org) | All (module au hasard), Chiptune, Demo (genre « Demo Style » du site) |
  | Modules.pl | [modules.pl](https://www.modules.pl) | S3M, IT, XM (filtre par format du site) |
  | Modland | [ftp.modland.com](https://ftp.modland.com/pub/modules/) | Protracker (MOD), Fasttracker 2 (XM), Screamtracker 3 (S3M), Impulsetracker (IT) |
  | Amiga Collection | [AMP – Amiga Music Preservation](https://amp.dascene.net) | All (MOD, XM, S3M ou IT), MOD, XM |

  Le module est toujours téléchargé sur le site de la source choisie : un fichier qui
  viendrait d'une autre adresse est refusé. Les archives sont décompressées automatiquement
  (zip sur Modules.pl, gzip sur AMP). Le fichier est enregistré sous le nom
  **`Artiste - Titre.ext`** donné par le site (simplement `Titre.ext` si l'artiste est
  inconnu), et son extension vient de son contenu réel.
- **Trois tailles d'interface**, que le bouton à droite fait défiler :
  - **Full** (grande) : logo, nom du module, 8 colonnes « Matrix », VU-mètres et playlist ;
  - **Mini** (moyenne) : nom du module, VU-mètres et playlist ;
  - **Nano** : simple barre de commandes. Le nom du module reste dans la barre de titre.
- **Playlist** : ajoute tes fichiers locaux avec **ADD**, puis double-clique sur une ligne pour
  la jouer.
- **Réglages mémorisés** dans `config.ini` : taille d'interface, affichage de la liste, source
  et catégorie choisies.

## Captures d'écran

| Full | Mini | Nano |
|---|---|---|
| ![Mode Full](Exemple_grand.png) | ![Mode Mini](Exemple_medium.png) | ![Mode Nano](Exemple_nano.png) |

*(Ces captures datent de la V1.5 : la ligne du nom du module n'y figure pas encore.)*

## Installation et lancement

**Sous Windows, le plus simple** : télécharge l'exe tout prêt dans les
[Releases](https://github.com/Popov2026/UltimateMatrixPlayer/releases) (rien à installer, voir
[Créer un exécutable Windows](#créer-un-exécutable-windows-exe) si Windows le bloque).

Sinon, depuis le code source :

Il te faut **Python 3** et deux bibliothèques :

```bash
pip install pygame pillow
```

Lance ensuite le script :

```bash
python UMPV16.pyw
```

Sous Windows, un double-clic sur `UMPV16.pyw` suffit (l'extension `.pyw` évite l'ouverture
d'une console).

> Pillow ne sert qu'à afficher le logo : sans Pillow, le lecteur fonctionne quand même.
> Sous Linux, pygame a besoin de `libmodplug` pour lire les modules
> (`sudo apt install libmodplug1` sous Debian/Ubuntu).

## Utilisation

| Bouton | Rôle |
|---|---|
| **PLAY** / `>` | Lit le morceau en cours, reprend après une pause ou ouvre le sélecteur de fichiers si la playlist est vide |
| **PAUSE** / `\|\|` | Met en pause |
| **STOP** / `■` | Arrête la lecture |
| **NEXT** / `>>` | Passe au morceau suivant |
| **ROULETTE [R]** | Télécharge et lance un module au hasard (source et catégorie choisies dans les menus) |
| **LIST** | Affiche ou masque la playlist |
| **ADD** | Ajoute des fichiers locaux à la playlist |
| `-` / `--` / `+` | Change la taille de l'interface (Full → Mini → Nano) |

Double-clique sur une ligne de la playlist pour jouer ce morceau. La lecture enchaîne les
morceaux et repart au début à la fin de la liste.

## Fichier `config.ini`

Il est créé à côté du script (ou de l'exécutable) au premier lancement :

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

| Réglage | Rôle |
|---|---|
| `mode` | Taille de l'interface : `full`, `mini` ou `nano` |
| `show_list` | Affiche la playlist (`True` / `False`) |
| `delay` | Rafraîchissement de l'animation, en millisecondes (20 au minimum) |
| `source`, `category` | Dernières source et catégorie choisies |

La section `[SOURCES]` est réécrite à chaque lancement. Les valeurs de `[SETTINGS]` sont
enregistrées à la fermeture de la fenêtre.

Les modules téléchargés par la roulette sont rangés dans le dossier **`WebMods/`**, sous le nom
`Artiste - Titre.ext` (par exemple `Purple Motion - Aquaphobia.s3m`). Si un autre module porte
déjà ce nom, ` (2)`, ` (3)`… est ajouté. Le dossier n'est pas vidé
automatiquement, mais les fichiers sont petits. Le dossier contient aussi
`modland_allmods.zip`, la liste des fichiers de Modland (6 Mo environ), téléchargée à la
première utilisation de Modland puis renouvelée une fois par semaine.

## Créer un exécutable Windows (.exe)

Les exe sont compilés par **GitHub Actions** (`.github/workflows/windows-build.yml`) sur une
machine Windows, directement depuis ce dépôt :

- à chaque pull request et à chaque modification de `main`, l'exe est compilé et testé (lecture
  d'un module par pygame, ouverture de l'interface, démarrage des exe). Le résultat se
  télécharge dans l'onglet *Actions*, rubrique *Artifacts* ;
- pour publier une **release**, au choix :
  - onglet *Actions* → *Windows build* → **Run workflow**, en indiquant la version (par
    exemple `v1.6`) : la release et son tag sont créés ;
  - ou *Releases* → **Draft a new release** sur GitHub : l'exe est ajouté automatiquement à
    la release quelques minutes après sa publication ;
  - ou pousser un tag `vX.Y` (`git tag v1.6 && git push origin v1.6`).

  La release contient :
  - `UltimateMatrixPlayer-vX.Y-windows.zip` (**recommandé**) : un dossier à décompresser,
    qui contient `UltimateMatrixPlayer.exe` ;
  - `UltimateMatrixPlayer-vX.Y-portable.exe` : un seul fichier, qui démarre un peu plus
    lentement ;
  - `SHA256SUMS.txt` : les empreintes des deux fichiers.

L'exe crée son `config.ini` et son dossier `WebMods/` à côté de lui.

### Windows 11 bloque l'exe ?

L'exe n'est pas signé avec un certificat de développeur (payant). SmartScreen ne le connaît
donc pas encore et affiche « Windows a protégé votre ordinateur » : clique sur
**Informations complémentaires** puis **Exécuter quand même**. Si le fichier téléchargé est
bloqué : clic droit → **Propriétés** → coche **Débloquer** (sur le zip, avant de le
décompresser).

Pour limiter les faux positifs des antivirus, la compilation :

- recompile le **bootloader** de PyInstaller au lieu d'utiliser celui fourni, que beaucoup
  d'antivirus signalent parce que des logiciels malveillants l'utilisent aussi ;
- n'utilise **pas UPX** (compression d'exe souvent jugée suspecte) ;
- intègre les **informations de version** (Propriétés → Détails) et l'icône ;
- propose une version en **dossier** (zip), moins souvent signalée que l'exe unique, qui se
  décompresse à chaque lancement.

Si Defender signale quand même l'exe, c'est un faux positif : on peut l'envoyer à Microsoft
pour analyse (https://www.microsoft.com/wdsi/filesubmission). Seule une **signature de code**
fait disparaître l'avertissement SmartScreen ; pour un projet libre, le programme gratuit
[SignPath Foundation](https://signpath.org) ou le service Azure Trusted Signing sont des
pistes.

Pour compiler soi-même sous Windows (sans le bootloader recompilé) :

```bash
pip install pygame pillow pyinstaller
python -m PyInstaller --noconfirm --windowed --noupx --name UltimateMatrixPlayer --icon Matrix.ico --add-data "logo.jpg;." --version-file packaging/version_info.txt UMPV16.pyw
```

Le résultat est dans `dist/UltimateMatrixPlayer/`.

## Contenu du dépôt

```
.
├── UMPV16.pyw          code source du lecteur
├── logo.jpg            bannière affichée en mode Full (intégrée au .exe)
├── Matrix.ico          icône de l'exécutable
├── Exemple_*.png       captures d'écran des trois modes
├── README.md           documentation en anglais
├── README.fr.md        ce fichier
├── packaging/          informations de version de l'exe, notes de release
└── .github/            compilation et tests Windows (GitHub Actions)
```

Créés à l'exécution (non versionnés) : `config.ini` et le dossier `WebMods/`.

## Limites connues

- **Sources de la roulette** : le lecteur lit les pages web des sites (ModArchive, Modules.pl)
  ou leurs liens de téléchargement (Modland, AMP). Si un site change sa présentation, sa source
  peut cesser de marcher jusqu'à une mise à jour du lecteur ; la roulette affiche alors
  « Aucun module récupéré ».
- **Amiga Collection (AMP)** : le module est tiré dans une plage fixe de numéros (de 1 à
  185 000, environ 182 500 en octobre 2026). Les modules ajoutés au-delà ne sont pas tirés. Une
  grande partie d'AMP est dans des formats Amiga que le lecteur ne sait pas lire : seuls les
  fichiers MOD, XM, S3M et IT sont gardés.
- **Modland** : la première utilisation télécharge la liste des fichiers (6 Mo environ), donc
  le premier tirage prend quelques secondes de plus.
- La roulette fait jusqu'à 6 tirages si un lien est mort ou si le module est dans un format non
  pris en charge. Elle abandonne tout de suite si le réseau est coupé.
- **Animation « Matrix »** : les notes qui défilent et les VU-mètres sont décoratifs. Ils ne
  reflètent pas le contenu réel du module.
- **Temps affiché** : il compte depuis le début du morceau, sans durée totale (pygame ne la
  fournit pas pour les modules).
- Les téléchargements se font en HTTPS **sans vérification du certificat**, pour éviter les
  erreurs de certificat sur certaines installations Windows.

## Journal des versions

### V1.6
- Le **nom du module** (titre stocké dans le fichier MOD, S3M, XM ou IT) s'affiche sous la barre
  de commandes, dans la barre de titre de la fenêtre et dans la playlist.
- **Vraies sources pour la roulette** : Modules.pl, Modland et Amiga Collection (AMP) tirent
  maintenant un module dans leur propre site, et non plus dans le catalogue de The Mod Archive.
  Les catégories de Modland deviennent Protracker, Fasttracker 2, Screamtracker 3 et
  Impulsetracker (au lieu de « Exotic »), et Amiga Collection propose All, MOD et XM.
- Correction : la recherche par catégorie sur ModArchive ne marchait plus : l'adresse d'API
  utilisée (`xml-search.php`) répond désormais « 404 Not Found ». Le lecteur passe maintenant
  par les pages de genre du site et sa page « module au hasard ». De plus, `config.ini` mettait
  les noms des sources en minuscules (`modarchive`), alors le test sur `ModArchive` ne
  réussissait jamais.
- Les archives zip (Modules.pl) et gzip (AMP) sont décompressées. Un fichier compressé par un
  packer Amiga (PowerPacker…) n'est plus pris pour un MOD.
- Les modules téléchargés sont nommés `Artiste - Titre.ext` d'après les informations du site,
  et chaque source n'accepte qu'un fichier venu de son propre site.
- Correction : le type d'un module téléchargé est reconnu d'après son contenu. Un XM n'est plus
  enregistré en `.mod`, et une page d'erreur n'est plus enregistrée comme un module.
- Correction : une playlist où aucun fichier n'est lisible ne fait plus planter le programme
  (récursion sans fin).
- La roulette télécharge en arrière-plan : l'interface ne se fige plus. Elle fait jusqu'à
  6 tirages si un lien est mort ou si le module n'est pas lisible.
- Double-clic sur une ligne de la playlist pour la jouer. Le morceau en cours est surligné.
- La source et la catégorie choisies sont mémorisées. Le réglage `delay` de `config.ini` est
  maintenant pris en compte.
- Le sélecteur de fichiers filtre les modules (`*.mod`, `*.s3m`, `*.xm`, `*.it`, et la
  convention Amiga `mod.*`).
- STOP remet le compteur à `00:00`.
- **Exe Windows** compilé et testé par GitHub Actions, publié dans les Releases (zip et exe
  portable), avec des mesures contre les faux positifs des antivirus.

### V1.5
- Première version publiée : trois modes d'affichage, roulette, playlist et `config.ini`.

## Crédits et licence

Projet libre d'utilisation pour tous les passionnés de musique tracker.

Bonne écoute ! Popov (mais pas Russe), 2026.

Merci à [Gemini](https://gemini.google.com) pour sa précieuse aide, et à
[The Mod Archive](https://modarchive.org), [Modules.pl](https://www.modules.pl),
[Modland](https://ftp.modland.com) et [AMP](https://amp.dascene.net) pour leurs collections.
