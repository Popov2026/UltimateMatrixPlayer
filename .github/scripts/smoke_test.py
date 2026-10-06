"""Vérifications avant publication, sur Windows avec le vrai pygame.

    python .github/scripts/smoke_test.py            # lecture d'un MOD fabriqué ici + interface
    python .github/scripts/smoke_test.py --network  # en plus : un tirage réel par source et catégorie
    python .github/scripts/smoke_test.py --write-mod test.mod  # écrit seulement le MOD de test
"""
import os, sys, struct, tempfile, collections, types, importlib.machinery, importlib.util

os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

def tiny_mod():
    # MOD 4 voies minimal : un instrument de 32 octets, une position, un motif vide
    head = b"smoke test".ljust(20, b"\0")
    sample = b"sample".ljust(22, b"\0") + struct.pack(">HBBHH", 16, 0, 64, 0, 1)
    head += sample + b"\0" * 30 * 30 + bytes([1, 127]) + b"\0" * 128 + b"M.K."
    return head + b"\0" * 1024 + bytes(range(0, 256, 8))

if "--write-mod" in sys.argv:
    # Fichier de test pour l'exe compilé : UltimateMatrixPlayer.exe --selftest <fichier>
    with open(sys.argv[sys.argv.index("--write-mod") + 1], "wb") as f: f.write(tiny_mod())
    sys.exit(0)

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
loader = importlib.machinery.SourceFileLoader("ump", os.path.join(ROOT, "UMPV16.pyw"))
ump = importlib.util.module_from_spec(importlib.util.spec_from_loader("ump", loader))
loader.exec_module(ump)
pygame, tk = ump.pygame, ump.tk

tmp = tempfile.mkdtemp()
ump.WEB_DIR = tmp
ump.MODLAND_INDEX = os.path.join(tmp, "modland_allmods.zip")
pygame.mixer.init(44100, -16, 2, 512)
failed = 0

path = os.path.join(tmp, "smoke.mod")
with open(path, "wb") as f: f.write(tiny_mod())
assert ump.read_module_title(path) == "smoke test"
pygame.mixer.music.load(path); pygame.mixer.music.play(); pygame.mixer.music.stop()
print("OK  pygame lit un MOD")

# L'interface se construit (les trois tailles) et se ferme sans erreur
root = tk.Tk()
app = ump.OpenCPMaster(root)
assert app.logo_img, "logo.jpg non chargé (voir ump.log)"
for _ in range(3): app.cycle_mode()
root.update(); root.destroy()
print("OK  interface")

if "--network" in sys.argv:
    worker = object.__new__(ump.OpenCPMaster); worker.modland_cache = {}
    q = collections.deque(); worker.downloads = types.SimpleNamespace(put=q.append)
    for source, cats in [("ModArchive", ["All", *ump.MODARCHIVE_GENRES]), ("Modules.pl", list(ump.MODULES_PL_FORMATS)),
                         ("Modland", list(ump.MODLAND_DIRS)), ("Amiga Collection", list(ump.AMP_FORMATS))]:
        for cat in cats:
            worker.roulette_worker(source, cat); r = q.pop()
            if not r or r[0] == "error":
                # roulette_worker renvoie ("error", raison) en cas d'échec
                print(f"ECHEC  {source} / {cat} : {r[1] if r else 'aucun résultat'}"); failed += 1; continue
            try:
                pygame.mixer.music.load(r[1]); print(f"OK  {source} / {cat} : {os.path.basename(r[1])}")
            except Exception as e:
                print(f"ECHEC  {source} / {cat} : pygame refuse {os.path.basename(r[1])} ({e})"); failed += 1

sys.exit(1 if failed else 0)
