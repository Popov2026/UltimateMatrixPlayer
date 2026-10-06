## Ultimate Matrix Player — Windows

**Français** · [English below](#english)

### Quel fichier télécharger ?

| Fichier | Pour qui |
|---|---|
| `UltimateMatrixPlayer-…-windows.zip` | **Recommandé.** Décompresse le dossier où tu veux, puis lance `UltimateMatrixPlayer.exe`. Démarrage rapide, et moins souvent signalé par les antivirus. |
| `UltimateMatrixPlayer-…-portable.exe` | Un seul fichier, sans installation. Il démarre un peu plus lentement (il se décompresse à chaque lancement). |
| `SHA256SUMS.txt` | Empreintes pour vérifier que le fichier n'a pas été modifié. |

Rien à installer : Python, pygame et Pillow sont inclus. `config.ini` et le dossier `WebMods/` sont créés à côté de l'exe.

### « Windows a protégé votre ordinateur »

L'exe n'est pas signé avec un certificat de développeur payant, donc Windows SmartScreen ne le connaît pas encore. Au premier lancement :

1. Clique sur **Informations complémentaires** ;
2. puis sur **Exécuter quand même**.

Si Windows bloque le fichier téléchargé : clic droit sur le zip ou l'exe → **Propriétés** → coche **Débloquer** → **OK** (à faire sur le zip *avant* de le décompresser).

Pour vérifier le fichier (PowerShell) : `Get-FileHash .\UltimateMatrixPlayer-…-windows.zip` puis compare avec `SHA256SUMS.txt`.

Si Microsoft Defender signale l'exe, c'est un faux positif connu des programmes Python empaquetés avec PyInstaller. Le code source est public et l'exe est compilé par GitHub Actions directement depuis ce dépôt. Tu peux le signaler à Microsoft : https://www.microsoft.com/wdsi/filesubmission

---

### English

| File | For |
|---|---|
| `UltimateMatrixPlayer-…-windows.zip` | **Recommended.** Unzip the folder anywhere and run `UltimateMatrixPlayer.exe`. Starts fast and is flagged less often by antivirus software. |
| `UltimateMatrixPlayer-…-portable.exe` | A single file, no install. Starts a little slower (it unpacks itself on each launch). |
| `SHA256SUMS.txt` | Checksums to check the files were not altered. |

**"Windows protected your PC"**: the exe is not signed with a paid developer certificate, so SmartScreen does not know it yet. Click **More info**, then **Run anyway**. If Windows blocks the downloaded file: right-click it → **Properties** → tick **Unblock** → **OK** (on the zip, *before* unzipping).

If Microsoft Defender flags the exe, it is a known false positive for Python programs packaged with PyInstaller. The source code is public and the exe is built by GitHub Actions straight from this repository. You can report it to Microsoft: https://www.microsoft.com/wdsi/filesubmission
