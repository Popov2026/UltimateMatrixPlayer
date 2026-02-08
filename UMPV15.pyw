import tkinter as tk
from tkinter import filedialog
import configparser
import os, pygame, random, urllib.request, ssl, sys, re

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

try:
    from PIL import Image, ImageTk
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False

class OpenCPMaster:
    def __init__(self, root):
        self.root = root
        self.root.title("UMP - V1.5 - By Popov ©2026")
        self.root.configure(bg="#000")
        
        if not os.path.exists(WEB_DIR): os.makedirs(WEB_DIR)
        self.config = configparser.ConfigParser()
        self.load_settings()

        try: pygame.mixer.init(44100, -16, 2, 512)
        except: pass

        self.playlist = []
        self.current_index = 0
        self.playing = False
        self.paused = False
        
        self.modes = ["full", "mini", "nano"]
        self.mode_symbols = ["-", "--", "+"]
        saved_mode = self.config.get("SETTINGS", "mode", fallback="full")
        self.mode_idx = self.modes.index(saved_mode) if saved_mode in self.modes else 0
        self.show_list = self.config.getboolean("SETTINGS", "show_list", fallback=True)
        
        self.chan_labels = []; self.vu_leds = []
        self.setup_ui()
        self.update_cats()
        self.apply_view_state() 
        self.auto_check_loop()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_settings(self):
        self.config.read(CONFIG_FILE)
        self.config["SOURCES"] = {
            "ModArchive": "All, Chiptune, Demo",
            "Modules.pl": "S3M, IT, XM",
            "Modland": "Exotic",
            "Amiga Collection": "All"
        }
        if "SETTINGS" not in self.config: 
            self.config["SETTINGS"] = {"mode": "full", "show_list": "True", "delay": "80"}
        with open(CONFIG_FILE, "w") as f: self.config.write(f)
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
        
        self.source_var = tk.StringVar(value=list(self.sources_map.keys())[0])
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

    def cycle_mode(self):
        self.mode_idx = (self.mode_idx + 1) % 3
        self.btn_cycle.config(text=self.mode_symbols[self.mode_idx])
        self.apply_view_state()

    def apply_view_state(self):
        mode = self.modes[self.mode_idx]
        self.header_main.pack_forget(); self.matrix_frame.pack_forget(); self.list_frame.pack_forget()
        self.btn_list.pack_forget(); self.btn_add.pack_forget(); self.src_menu.pack_forget(); self.cat_menu.pack_forget()
        
        if mode == "full":
            self.set_btns_text(True); self.logo_mini_label.pack_forget()
            self.src_menu.pack(side=tk.LEFT, padx=2); self.cat_menu.pack(side=tk.LEFT, padx=2)
            self.header_main.pack(fill=tk.X); self.matrix_frame.pack(expand=True, fill=tk.BOTH, pady=5)
            self.btn_add.pack(side=tk.RIGHT, padx=1); self.btn_list.pack(side=tk.RIGHT, padx=1)
            for txt_f, rows in self.chan_labels: txt_f.pack(fill=tk.X)
            self.root.geometry("1040x750" if self.show_list else "1040x600")
            if self.show_list: self.list_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5); self.listbox.config(height=8)
        elif mode == "mini":
            self.set_btns_text(True); self.logo_mini_label.pack(side=tk.LEFT, padx=5)
            self.src_menu.pack(side=tk.LEFT, padx=2); self.cat_menu.pack(side=tk.LEFT, padx=2)
            self.matrix_frame.pack(expand=True, fill=tk.BOTH, pady=5)
            self.btn_add.pack(side=tk.RIGHT, padx=1); self.btn_list.pack(side=tk.RIGHT, padx=1)
            for txt_f, rows in self.chan_labels: txt_f.pack_forget()
            self.root.geometry("1040x360" if self.show_list else "1040x220")
            if self.show_list: self.list_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5); self.listbox.config(height=5)
        elif mode == "nano":
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
        source, genre = self.source_var.get(), self.cat_var.get()
        ext = genre.lower() if genre in ["XM", "S3M", "IT"] else "mod"
        if source == "ModArchive":
            query = "Demo+Style" if genre == "Demo" else genre
            url_search = f"https://api.modarchive.org/xml-search.php?key=guest&request=search&type=genre&query={query}"
            try:
                resp = urllib.request.urlopen(url_search, timeout=10, context=ctx).read().decode('utf-8')
                ids = re.findall(r'<id>(\d+)</id>', resp)
                if ids:
                    mid = random.choice(ids); url_dl = f"https://api.modarchive.org/downloads.php?moduleid={mid}"
                    data = urllib.request.urlopen(url_dl, timeout=10, context=ctx).read()
                    fpath = os.path.join(WEB_DIR, f"{genre}_{mid}.{ext}")
                    with open(fpath, 'wb') as f: f.write(data)
                    self.playlist.append(fpath); self.listbox.insert(tk.END, f" [{source}] {genre}_{mid}.{ext}")
                    self.listbox.see(tk.END); self.current_index = len(self.playlist)-1; self.start_song()
            except: pass
        else:
            mid = random.randint(34000, 180000); url = f"https://api.modarchive.org/downloads.php?moduleid={mid}"
            try:
                data = urllib.request.urlopen(url, timeout=10, context=ctx).read()
                fpath = os.path.join(WEB_DIR, f"rand_{mid}.{ext}")
                with open(fpath, 'wb') as f: f.write(data)
                self.playlist.append(fpath); self.listbox.insert(tk.END, f" [{source}] rand_{mid}.{ext}")
                self.listbox.see(tk.END); self.current_index = len(self.playlist)-1; self.start_song()
            except: pass

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
    def pause_music(self):
        if self.playing: pygame.mixer.music.pause(); self.paused = True; self.playing = False
    def stop_music(self): pygame.mixer.music.stop(); self.playing = False; self.paused = False
    def start_song(self):
        try: pygame.mixer.music.load(self.playlist[self.current_index]); pygame.mixer.music.play(); self.playing = True; self.paused = False
        except: self.next_track()
    def next_track(self):
        if self.playlist: self.current_index = (self.current_index + 1) % len(self.playlist); self.start_song()
    def add_local(self):
        f = filedialog.askopenfilenames()
        for x in f: self.playlist.append(x); self.listbox.insert(tk.END, f" [LOC] {os.path.basename(x)}")
    def auto_check_loop(self):
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
        self.root.after(80, self.auto_check_loop)
    def on_close(self):
        self.config["SETTINGS"]["mode"] = self.modes[self.mode_idx]; self.config["SETTINGS"]["show_list"] = str(self.show_list)
        with open(CONFIG_FILE, "w") as f: self.config.write(f)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk(); app = OpenCPMaster(root); root.mainloop()