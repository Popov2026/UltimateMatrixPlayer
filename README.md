[README.txt](https://github.com/user-attachments/files/25170047/README.txt)
🎵 Ultimate Matrix Player (UMP)
Ultimate Matrix Player est un lecteur de modules (MOD, S3M, XM, IT) ultra-léger et personnalisable, conçu pour les amateurs de la scène démo et du chiptune. Il combine une esthétique rétro "Matrix" avec une connectivité moderne aux plus grandes bases de données de modules mondiales.

✨ Fonctionnalités
Multi-Sources : Accès direct aux catalogues de ModArchive, Modules.pl, Modland (Demo, Game, Pub) et Amiga Collection.

Mode Roulette [R] : Téléchargement et lecture instantanée d'un module aléatoire selon la catégorie choisie.

Interface Adaptative : Un bouton unique cyclique pour basculer entre 3 modes de vue :

+ Full (Géant) : Interface complète avec logo, VU-mètres et liste de lecture.

- Mini (Medium) : Compact avec VU-mètres uniquement.

-- Nano : Discrétion absolue (barre de contrôle minimaliste).

Visualisation Matrix : Canaux 8 pistes avec défilement de code et VU-mètres LED réactifs.

Persistance : Sauvegarde automatique de vos réglages (IP, dernier mode utilisé, source favorite) dans un fichier config.ini.

🚀 Installation & Lancement
Prérequis
Python 3.x

Bibliothèques nécessaires :

Bash
pip install pygame pillow
Lancement du script
Bash
python UMPV15.pyw
🛠 Compilation en Exécutable (.exe)
Pour créer un fichier .exe indépendant avec le logo et l'icône intégrés, utilisez PyInstaller :

Placez votre logo.jpg et votre mon_icone.ico dans le dossier du script.

Lancez la commande suivante :

Bash
python -m PyInstaller --noconsole --onefile --add-data "logo.jpg;." --icon="matrix.ico" UMPV15.pyw
Récupérez votre exécutable dans le dossier /dist.

📂 Structure des fichiers
UMPV15.pyw : Le code source principal.

logo.jpg : Bannière d'en-tête pour le mode Full.

config.ini : Généré automatiquement pour vos préférences (Sources et qualité).

/WebMods : Dossier de cache pour les modules téléchargés. (Ne se purge pas automatiquement, mais les fichiers sont petits)

📝 Licence
Projet libre d'utilisation pour tous les passionnés de tracker music.

Bonne écoute ! Popov mais pas Russe. 2026
