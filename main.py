import yt_dlp
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading


def download_audio():
    url = entry_url.get().strip()
    if not url:
        messagebox.showerror("Erreur", "Veuillez entrer un lien YouTube.")
        return

    dossier = filedialog.askdirectory(title="Choisissez le dossier de sauvegarde")
    if not dossier:
        return

    progress_bar['value'] = 0
    label_progress.config(text="Téléchargement en cours...")

    def hook(d):
        if d['status'] == 'downloading':
            try:
                percent = float(d['_percent_str'].strip('%'))
                progress_bar['value'] = percent
                root.update_idletasks()
            except:
                pass
        elif d['status'] == 'finished':
            label_progress.config(text="Conversion en MP3...")

    def task_download():
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'extractaudio': True,
                'audioformat': 'mp3',
                'outtmpl': f'{dossier}/%(title)s.%(ext)s',
                'noplaylist': True,
                'progress_hooks': [hook],
                'quiet': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            label_progress.config(text="Téléchargement terminé ✅")
            messagebox.showinfo("Succès", "Téléchargement terminé avec succès !")
            progress_bar['value'] = 0
            label_progress.config(text="")
            entry_url.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue :\n{e}")
            label_progress.config(text="Erreur ❌")

    threading.Thread(target=task_download, daemon=True).start()


def past_url():
    try:
        text = root.clipboard_get()
        entry_url.delete(0, tk.END)
        entry_url.insert(0, text)
    except tk.TclError:
        messagebox.showerror("Erreur", "Le presse-papiers est vide ou inaccessible.")


# --- Interface graphique ---
root = tk.Tk()
root.title("YouTube → MP3")
root.geometry("500x200")
root.resizable(False, False)

label_url = tk.Label(root, text="Lien YouTube :", font=("Arial", 12))
label_url.pack(pady=5)

frame_url = tk.Frame(root)
frame_url.pack(pady=5)

entry_url = tk.Entry(frame_url, width=45)
entry_url.pack(side=tk.LEFT, padx=(0, 5))

btn_paste = tk.Button(frame_url, text="Coller", command=past_url)
btn_paste.pack(side=tk.LEFT)

btn_dl = tk.Button(root, text="Télécharger en MP3", command=download_audio, bg="#4CAF50", fg="white")
btn_dl.pack(pady=10)

progress_bar = ttk.Progressbar(root, length=350, mode='determinate')
progress_bar.pack(pady=5)

label_progress = tk.Label(root, text="", font=("Arial", 10))
label_progress.pack()

root.mainloop()
