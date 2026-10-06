import tkinter as tk
from tkinter import filedialog
import configparser
import os, pygame, random, urllib.request, ssl, sys, re, threading, queue

ctx = ssl._create_unverified_context()

if getattr(sys, 'frozen', False):
    # PyInstaller extrait les fichiers internes (logo) ici :
    BASE_DIR = sys._MEIPASS
    # L'EXE écrit ses fichiers externes (config, musiques) ici :
    EXE_DIR = os.path.dirname(sys.executable)
else:
    # Mode normal (Python ton_script.py)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    EXE_DIR = BASE_DIR

CONFIG_FILE = os.path.join(EXE_DIR, "config.ini")
WEB_DIR = os.path.join(EXE_DIR, "WebMods")
LOGO_PATH = os.path.join(BASE_DIR, "logo.jpg")
MOD_EXTS = ("mod", "s3m", "xm", "it")

try:
    from PIL import Image, ImageTk
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False

# Signatures des MOD Amiga (octets 1080-1083) : M.K., FLT4, 6CHN, 16CH...
MOD_TAGS = (b"M.K.", b"M!K!", b"M&K!", b"N.T.", b"CD81", b"CD61", b"OKTA", b"OCTA", b"FA04", b"FA06", b"FA08")
MOD_TAG_RE = re.compile(rb"\dCHN|\d\dCH|FLT\d|TDZ\d")

def detect_module(data, allow_legacy=True):
    """Renvoie (extension, titre) d'après l'en-tête du module, ou (None, '') si ce n'en est pas un.
    Le titre est stocké dans le fichier : 20 octets (MOD/XM), 28 (S3M) ou 26 (IT)."""
    tag = data[1080:1084]
    if data[:17] == b"Extended Module: ": ext, raw = "xm", data[17:37]
    elif data[:4] == b"IMPM": ext, raw = "it", data[4:30]
    elif data[44:48] == b"SCRM": ext, raw = "s3m", data[0:28]
    elif tag in MOD_TAGS or MOD_TAG_RE.fullmatch(tag): ext, raw = "mod", data[0:20]
    # Vieux MOD Amiga à 15 instruments : pas de signature, on l'accepte si ce n'est pas une page HTML
    elif allow_legacy and len(data) > 600 and data.lstrip()[:1] != b"<": ext, raw = "mod", data[0:20]
    else: return None, ""
    title = raw.split(b"\0")[0].decode("latin-1")
    title = "".join(c for c in title if c.isprintable()).strip()
    return ext, title

def read_module_title(path):
    name = os.path.basename(path).lower()
    try:
        with open(path, "rb") as f: data = f.read(1084)
    except OSError: return ""
    # Sans signature, n'interpréter l'en-tête comme un MOD que si le nom le dit (x.mod ou mod.x à l'Amiga)
    return detect_module(data, allow_legacy=name.endswith(".mod") or name.startswith("mod."))[1]

class OpenCPMaster:
    def __init__(self, root):
        self.root = root
        self.app_title = "UMP - V1.6 - By Popov ©2026"
        self.root.title(self.app_title)
        self.root.configure(bg="#000")

        if not os.path.exists(WEB_DIR): os.makedirs(WEB_DIR)
        self.config = configparser.ConfigParser()
        # Garde la casse des clés : sinon "ModArchive" devient "modarchive" et la recherche par genre n'est jamais utilisée
        self.config.optionxform = str
        self.load_settings()

        try: pygame.mixer.init(44100, -16, 2, 512)
        except: pass

        self.playlist = []
        self.current_index = 0
        self.playing = False
        self.paused = False
        self.downloads = queue.Queue()
        self.downloading = False
        self.current_title = ""

        self.modes = ["full", "mini", "nano"]
        self.mode_symbols = ["-", "--", "+"]
        saved_mode = self.config.get("SETTINGS", "mode", fallback="full")
        self.mode_idx = self.modes.index(saved_mode) if saved_mode in self.modes else 0
        self.show_list = self.config.getboolean("SETTINGS", "show_list", fallback=True)
        try: self.delay = max(20, self.config.getint("SETTINGS", "delay", fallback=80))
        except ValueError: self.delay = 80

        self.chan_labels = []; self.vu_leds = []
        self.setup_ui()
        self.update_cats()
        saved_cat = self.config.get("SETTINGS", "category", fallback="")
        if saved_cat in self.sources_map.get(self.source_var.get(), []): self.cat_var.set(saved_cat)
        self.apply_view_state()
        self.auto_check_loop()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_settings(self):
        self.config.read(CONFIG_FILE, encoding="utf-8")
        self.config["SOURCES"] = {
            "ModArchive": "All, Chiptune, Demo",
            "Modules.pl": "S3M, IT, XM",
            "Modland": "Exotic",
            "Amiga Collection": "All"
        }
        if "SETTINGS" not in self.config:
            self.config["SETTINGS"] = {"mode": "full", "show_list": "True", "delay": "80"}
        with open(CONFIG_FILE, "w", encoding="utf-8") as f: self.config.write(f)
        self.sources_map = {k: [c.strip() for c in v.split(",")] for k, v in self.config.items("SOURCES")}

    def setup_ui(self):
        self.header_main = tk.Frame(self.root, bg="#000")
        if HAS_PILLOW and os.path.exists(LOGO_PATH):
            try:
                img = Image.open(LOGO_PATH)
                img = img.resize((1030, 140), Image.Resampling.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img)
                tk.Label(self.header_main, image=self.logo_img, bg="#000").pack(pady=5)
            except: pass

        self.ctrl_bar = tk.Frame(self.root, bg="#111", bd=1, relief=tk.FLAT)
        self.ctrl_bar.pack(fill=tk.X, side=tk.TOP, padx=5, pady=2)

        self.left_group = tk.Frame(self.ctrl_bar, bg="#111")
        self.left_group.pack(side=tk.LEFT)
        self.logo_mini_label = tk.Label(self.left_group, text="UMP", font=("Impact", 18), fg="#0f0", bg="#000")

        saved_src = self.config.get("SETTINGS", "source", fallback="")
        self.source_var = tk.StringVar(value=saved_src if saved_src in self.sources_map else list(self.sources_map.keys())[0])
        self.src_menu = tk.OptionMenu(self.left_group, self.source_var, *self.sources_map.keys(), command=self.update_cats)
        self.src_menu.config(bg="#000", fg="#0f0", font=("Consolas", 10), width=15, bd=1, highlightthickness=0)
        self.src_menu["menu"].config(bg="#000", fg="#0f0", font=("Consolas", 10))

        self.cat_var = tk.StringVar(); self.cat_menu = tk.OptionMenu(self.left_group, self.cat_var, "")
        self.cat_menu.config(bg="#000", fg="#0f0", font=("Consolas", 10), width=12, bd=1, highlightthickness=0)
        self.cat_menu["menu"].config(bg="#000", fg="#0f0", font=("Consolas", 10))

        self.btn_play = tk.Button(self.ctrl_bar, text="PLAY", command=self.play_current, bg="#222", fg="#0f0", font=("Consolas", 10, "bold"), bd=1)
        self.btn_play.pack(side=tk.LEFT, padx=1)
        self.btn_pause = tk.Button(self.ctrl_bar, text="PAUSE", command=self.pause_music, bg="#222", fg="#0f0", font=("Consolas", 10, "bold"), bd=1)
        self.btn_pause.pack(side=tk.LEFT, padx=1)
        self.time_label = tk.Label(self.ctrl_bar, text="00:00", font=("Consolas", 11, "bold"), fg="#0f0", bg="#000", width=6)
        self.time_label.pack(side=tk.LEFT, padx=5)
        self.btn_stop = tk.Button(self.ctrl_bar, text="STOP", command=self.stop_music, bg="#222", fg="#0f0", font=("Consolas", 10, "bold"), bd=1)
        self.btn_stop.pack(side=tk.LEFT, padx=1)
        self.btn_next = tk.Button(self.ctrl_bar, text="NEXT", command=self.next_track, bg="#222", fg="#0f0", font=("Consolas", 10, "bold"), bd=1)
        self.btn_next.pack(side=tk.LEFT, padx=1)
        self.btn_roulette = tk.Button(self.ctrl_bar, text="[R]", command=self.spin_roulette, bg="#400", fg="#ff0", font=("Consolas", 10, "bold"), bd=1)
        self.btn_roulette.pack(side=tk.LEFT, padx=5)

        self.btn_cycle = tk.Button(self.ctrl_bar, text=self.mode_symbols[self.mode_idx], command=self.cycle_mode, bg="#004400", fg="#fff", font=("Consolas", 11, "bold"), width=3)
        self.btn_cycle.pack(side=tk.RIGHT, padx=5)

        self.btn_list = tk.Button(self.ctrl_bar, text="LIST", command=self.toggle_list, bg="#222", fg="#0f0", font=("Consolas", 10, "bold"), bd=1)
        self.btn_add = tk.Button(self.ctrl_bar, text="ADD", command=self.add_local, bg="#222", fg="#0f0", font=("Consolas", 10, "bold"), bd=1)

        # Nom du module en cours (titre lu dans l'en-tête du fichier MOD/S3M/XM/IT)
        self.title_frame = tk.Frame(self.root, bg="#000")
        self.title_label = tk.Label(self.title_frame, text="", font=("Consolas", 12, "bold"), fg="#ff0", bg="#000", anchor="w")
        self.title_label.pack(fill=tk.X, padx=5)

        self.matrix_frame = tk.Frame(self.root, bg="#000")
        for i in range(8):
            col = tk.Frame(self.matrix_frame, bg="#000", bd=1, width=128, relief=tk.SOLID)
            col.pack(side=tk.LEFT, fill=tk.Y, padx=1); col.pack_propagate(False)
            tk.Label(col, text=f"CH {i+1}", bg="#050", fg="#fff", font=("Consolas", 8, "bold")).pack(fill=tk.X)
            txt_f = tk.Frame(col, bg="#000"); txt_f.pack(fill=tk.X)
            rows = [tk.Label(txt_f, text="--- --", bg="#000", fg="#006600", font=("Consolas", 9)) for _ in range(12)]
            for r in rows: r.pack()
            self.chan_labels.append((txt_f, rows))
            cv = tk.Canvas(col, height=180, width=110, bg="#000", highlightthickness=0); cv.pack(side=tk.BOTTOM, pady=5)
            leds = [cv.create_rectangle(10, 160-(j*13), 100, 160-(j*13)+10, fill="#111", outline="") for j in range(12)]
            self.vu_leds.append((cv, leds))

        self.list_frame = tk.Frame(self.root, bg="#050")
        self.listbox = tk.Listbox(self.list_frame, bg="#000", fg="#0f0", font=("Consolas", 10))
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.listbox.bind("<Double-Button-1>", self.play_selected)

    def cycle_mode(self):
        self.mode_idx = (self.mode_idx + 1) % 3
        self.btn_cycle.config(text=self.mode_symbols[self.mode_idx])
        self.apply_view_state()

    def apply_view_state(self):
        mode = self.modes[self.mode_idx]
        self.header_main.pack_forget(); self.title_frame.pack_forget(); self.matrix_frame.pack_forget(); self.list_frame.pack_forget()
        self.btn_list.pack_forget(); self.btn_add.pack_forget(); self.src_menu.pack_forget(); self.cat_menu.pack_forget()

        if mode == "full":
            self.set_btns_text(True); self.logo_mini_label.pack_forget()
            self.src_menu.pack(side=tk.LEFT, padx=2); self.cat_menu.pack(side=tk.LEFT, padx=2)
            self.header_main.pack(fill=tk.X); self.title_frame.pack(fill=tk.X)
            self.matrix_frame.pack(expand=True, fill=tk.BOTH, pady=5)
            self.btn_add.pack(side=tk.RIGHT, padx=1); self.btn_list.pack(side=tk.RIGHT, padx=1)
            for txt_f, rows in self.chan_labels: txt_f.pack(fill=tk.X)
            self.root.geometry("1040x780" if self.show_list else "1040x630")
            if self.show_list: self.list_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5); self.listbox.config(height=8)
        elif mode == "mini":
            self.set_btns_text(True); self.logo_mini_label.pack(side=tk.LEFT, padx=5)
            self.src_menu.pack(side=tk.LEFT, padx=2); self.cat_menu.pack(side=tk.LEFT, padx=2)
            self.title_frame.pack(fill=tk.X)
            self.matrix_frame.pack(expand=True, fill=tk.BOTH, pady=5)
            self.btn_add.pack(side=tk.RIGHT, padx=1); self.btn_list.pack(side=tk.RIGHT, padx=1)
            for txt_f, rows in self.chan_labels: txt_f.pack_forget()
            self.root.geometry("1040x390" if self.show_list else "1040x250")
            if self.show_list: self.list_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5); self.listbox.config(height=5)
        elif mode == "nano":
            # Trop étroit pour la ligne du titre : le nom du module reste affiché dans la barre de titre de la fenêtre
            self.set_btns_text(False); self.logo_mini_label.pack(side=tk.LEFT, padx=5)
            self.btn_add.pack(side=tk.RIGHT, padx=1)
            self.root.geometry("340x40")

    def set_btns_text(self, full_text):
        if full_text:
            self.btn_add.config(text="ADD"); self.btn_list.config(text="LIST")
            self.btn_play.config(text="PLAY"); self.btn_pause.config(text="PAUSE")
            self.btn_stop.config(text="STOP"); self.btn_next.config(text="NEXT"); self.btn_roulette.config(text="ROULETTE [R]")
        else:
            self.btn_add.config(text="ADD"); self.btn_play.config(text=">"); self.btn_pause.config(text="||")
            self.btn_stop.config(text="■"); self.btn_next.config(text=">>"); self.btn_roulette.config(text="[R]")

    def spin_roulette(self):
        # Le téléchargement tourne dans un thread pour ne pas figer l'interface ; le résultat
        # revient par self.downloads et est traité par auto_check_loop, dans le thread Tk.
        if self.downloading: return
        self.downloading = True; self.btn_roulette.config(state=tk.DISABLED)
        self.title_label.config(text="... téléchargement / downloading ...")
        threading.Thread(target=self.roulette_worker, args=(self.source_var.get(), self.cat_var.get()), daemon=True).start()

    def roulette_worker(self, source, genre):
        result = None
        try:
            if source == "ModArchive":
                query = "Demo+Style" if genre == "Demo" else genre
                url_search = f"https://api.modarchive.org/xml-search.php?key=guest&request=search&type=genre&query={query}"
                resp = urllib.request.urlopen(url_search, timeout=10, context=ctx).read().decode('utf-8', 'replace')
                ids = re.findall(r'<id>(\d+)</id>', resp)
                if ids: result = self.download_module(source, random.choice(ids), genre)
            else:
                # Plusieurs essais : un identifiant tiré au hasard peut ne correspondre à aucun module
                for _ in range(5):
                    result = self.download_module(source, random.randint(34000, 180000), "rand")
                    if result: break
        except Exception: pass
        self.downloads.put(result)

    def download_module(self, source, mid, prefix):
        try: data = urllib.request.urlopen(f"https://api.modarchive.org/downloads.php?moduleid={mid}", timeout=10, context=ctx).read()
        except Exception: return None
        ext, title = detect_module(data)
        if not ext: return None  # page d'erreur HTML ou fichier inconnu
        # L'extension vient du contenu réel (un XM n'est plus enregistré en .mod)
        fpath = os.path.join(WEB_DIR, f"{prefix}_{mid}.{ext}")
        with open(fpath, 'wb') as f: f.write(data)
        return source, fpath, title

    def roulette_done(self, result):
        self.downloading = False; self.btn_roulette.config(state=tk.NORMAL)
        if not result:
            self.title_label.config(text="Aucun module récupéré / No module downloaded")
            self.root.after(3000, self.restore_title); return
        source, fpath, title = result
        self.add_to_playlist(fpath, source, title)
        self.current_index = len(self.playlist)-1; self.start_song()

    def add_to_playlist(self, fpath, tag, title=None):
        if title is None: title = read_module_title(fpath)
        self.playlist.append(fpath)
        name = os.path.basename(fpath)
        self.listbox.insert(tk.END, f" [{tag}] {title}  ({name})" if title else f" [{tag}] {name}")

    def update_cats(self, *args):
        src = self.source_var.get(); menu = self.cat_menu['menu']; menu.delete(0, 'end')
        cats = self.sources_map.get(src, ["All"])
        for c in cats: menu.add_command(label=c, command=lambda v=c: self.cat_var.set(v))
        self.cat_var.set(cats[0])

    def toggle_list(self): self.show_list = not self.show_list; self.apply_view_state()
    def play_current(self):
        if self.paused: pygame.mixer.music.unpause(); self.paused = False; self.playing = True
        elif self.playlist: self.start_song()
        else: self.add_local()
    def play_selected(self, event=None):
        sel = self.listbox.curselection()
        if sel: self.current_index = sel[0]; self.start_song()
    def pause_music(self):
        if self.playing: pygame.mixer.music.pause(); self.paused = True; self.playing = False
    def stop_music(self):
        pygame.mixer.music.stop(); self.playing = False; self.paused = False; self.time_label.config(text="00:00")
    def start_song(self, tries=0):
        # tries évite une récursion sans fin quand aucun fichier de la playlist n'est lisible
        if not self.playlist or tries >= len(self.playlist): self.playing = False; return
        path = self.playlist[self.current_index]
        try: pygame.mixer.music.load(path); pygame.mixer.music.play(); self.playing = True; self.paused = False
        except Exception:
            self.current_index = (self.current_index + 1) % len(self.playlist); self.start_song(tries + 1); return
        self.show_title(read_module_title(path) or os.path.splitext(os.path.basename(path))[0])
        self.time_label.config(text="00:00")
        self.listbox.selection_clear(0, tk.END); self.listbox.selection_set(self.current_index); self.listbox.see(self.current_index)
    def restore_title(self):
        if not self.downloading: self.title_label.config(text=f"♪ {self.current_title}" if self.current_title else "")
    def show_title(self, title):
        self.current_title = title
        self.title_label.config(text=f"♪ {title}")
        self.root.title(f"{title} - {self.app_title}")
    def next_track(self):
        if self.playlist: self.current_index = (self.current_index + 1) % len(self.playlist); self.start_song()
    def add_local(self):
        pattern = " ".join(f"*.{e} *.{e.upper()} {e}.* {e.upper()}.*" for e in MOD_EXTS)
        f = filedialog.askopenfilenames(filetypes=[("Modules", pattern), ("Tous / All", "*.*")])
        for x in f: self.add_to_playlist(x, "LOC")
    def auto_check_loop(self):
        while not self.downloads.empty(): self.roulette_done(self.downloads.get_nowait())
        if self.playing and not pygame.mixer.music.get_busy() and not self.paused: self.next_track()
        if self.playing and pygame.mixer.music.get_busy():
            ms = pygame.mixer.music.get_pos()
            if ms > 0:
                m, s = divmod(ms // 1000, 60); self.time_label.config(text=f"{m:02d}:{s:02d}")
            for i in range(8):
                if self.modes[self.mode_idx] == "full":
                    txt_f, rows = self.chan_labels[i]
                    for j in range(11): rows[j].config(text=rows[j+1].cget("text"))
                    rows[11].config(text=f"{random.choice(['C-5','D-4','F-5','---'])} {random.randint(1,9):X}")
                cv, leds = self.vu_leds[i]; lvl = random.randint(0, 12)
                for idx, led in enumerate(leds): cv.itemconfig(led, fill=["#003300", "#005500", "#007700", "#009900", "#00BB00", "#00DD00", "#00FF00", "#FFFF00", "#FFCC00", "#FFAA00", "#FF5500", "#FF0000"][idx] if idx < lvl else "#111")
        self.root.after(self.delay, self.auto_check_loop)
    def on_close(self):
        s = self.config["SETTINGS"]
        s["mode"] = self.modes[self.mode_idx]; s["show_list"] = str(self.show_list)
        s["source"] = self.source_var.get(); s["category"] = self.cat_var.get()
        with open(CONFIG_FILE, "w", encoding="utf-8") as f: self.config.write(f)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk(); app = OpenCPMaster(root); root.mainloop()
