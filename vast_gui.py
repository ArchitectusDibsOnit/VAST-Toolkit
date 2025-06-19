
import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from mutagen import File as AudioFile

# Preset directory relative to the script
PRESET_DIR = os.path.join(os.path.dirname(__file__), 'presets')
GENRE_PRESET_MAP = {
    "dubstep": "vlc_bass_rave_glitch.conf",
    "electronic": "vlc_bass_rave_glitch.conf",
    "glitchcore": "vlc_bass_rave_glitch.conf",
    "hardstyle": "vlc_bass_rave_glitch.conf",
    "industrial": "vlc_bass_rave_glitch.conf",
    "rock": "vlc_crisp_rock.conf",
    "alternative": "vlc_crisp_rock.conf",
    "hip hop": "vlc_phonetic_rap_flow.conf",
    "rap": "vlc_phonetic_rap_flow.conf",
    "default": "vlc_balanced_loud.conf"
}

def detect_genre_and_preset(path):
    try:
        audio = AudioFile(path)
        genre = "default"
        if audio and audio.tags:
            for tag in audio.tags:
                if "genre" in tag.lower():
                    genre = str(audio.tags[tag][0]).lower()
                    break
        preset = GENRE_PRESET_MAP.get(genre, GENRE_PRESET_MAP["default"])
        return genre, preset
    except Exception:
        return "default", GENRE_PRESET_MAP["default"]

def apply_preset(preset_filename):
    try:
        preset_path = os.path.join(PRESET_DIR, preset_filename)
        user_home = os.path.expanduser("~")
        vlcrc_path = os.path.join(user_home, "AppData", "Roaming", "vlc", "vlcrc")
        backup_path = vlcrc_path + ".bak"
        if os.path.exists(vlcrc_path):
            os.replace(vlcrc_path, backup_path)
        with open(preset_path, 'r') as src, open(vlcrc_path, 'w') as dst:
            dst.write(src.read())
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to apply preset.\n{e}")
        return False

def run_gui():
    root = tk.Tk()
    root.title("V.A.S.T. Preset Wizard")
    root.geometry("460x260")
    root.resizable(False, False)

    def browse_file():
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.flac *.wav *.ogg")])
        if file_path:
            genre, preset = detect_genre_and_preset(file_path)
            result_var.set(f"🎧 Genre: {genre.upper()}\n🎚 Preset: {preset}")
            apply_button.config(state="normal")
            apply_button.preset = preset

    def apply_selected_preset():
        if apply_preset(apply_button.preset):
            messagebox.showinfo("Success", f"Preset '{apply_button.preset}' applied!")
            apply_button.config(state="disabled")

    result_var = tk.StringVar()
    tk.Label(root, text="🎧 Drop or Select a Song File", font=("Arial", 12)).pack(pady=10)
    tk.Button(root, text="📁 Browse File", command=browse_file).pack(pady=5)
    tk.Label(root, textvariable=result_var, wraplength=400, font=("Courier", 10)).pack(pady=20)
    apply_button = tk.Button(root, text="✅ Apply Preset to VLC", state="disabled", command=apply_selected_preset)
    apply_button.pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
