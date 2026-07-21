import sys
import os
import requests
import ctypes
import subprocess
import threading
import tkinter as tk
from tkinter import ttk

def upload_file(file_path):
    url = "https://catbox.moe/user/api.php"
    data = {"reqtype": "fileupload"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        with open(file_path, "rb") as f:
            files = {"fileToUpload": (os.path.basename(file_path), f)}
            response = requests.post(url, data=data, files=files, headers=headers, timeout=300)
            if response.status_code == 200:
                return response.text
            else:
                return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Exception: {str(e)}"

def copy_to_clipboard(text):
    subprocess.run(['clip'], input=text, text=True, check=True)

def show_message(title, text):
    ctypes.windll.user32.MessageBoxW(0, text, title, 0x40 | 0x0 | 0x40000)

def show_error(title, text):
    ctypes.windll.user32.MessageBoxW(0, text, title, 0x10 | 0x0 | 0x40000)

class UploadApp:
    def __init__(self, files):
        self.files = files
        self.urls = []
        self.errors = []
        
        self.root = tk.Tk()
        self.root.title("Catbox Uploader")
        self.root.geometry("350x140")
        self.root.resizable(False, False)
        
        # Center the window on the screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')
        
        # Keep window always on top
        self.root.attributes('-topmost', True)
        
        # UI Elements
        self.label = ttk.Label(self.root, text="Uploading files to Catbox...\nPlease wait, this may take a while.", justify="center")
        self.label.pack(pady=15)
        
        self.progress = ttk.Progressbar(self.root, mode='indeterminate', length=250)
        self.progress.pack(pady=5)
        self.progress.start(15)
        
        self.credits = ttk.Label(self.root, text="Made by Paulitos", foreground="gray")
        self.credits.pack(side="bottom", pady=10)
        
        # Start upload in a separate thread so GUI doesn't freeze
        self.thread = threading.Thread(target=self.process_uploads, daemon=True)
        self.thread.start()
        
        # Check thread status every 100ms
        self.root.after(100, self.check_thread)
        
        self.root.mainloop()
        
    def process_uploads(self):
        for file_path in self.files:
            if os.path.isfile(file_path):
                result = upload_file(file_path)
                if result.startswith("http"):
                    self.urls.append(result)
                else:
                    self.errors.append(f"{os.path.basename(file_path)}: {result}")
            else:
                self.errors.append(f"{os.path.basename(file_path)}: Not a valid file.")
                
    def check_thread(self):
        if self.thread.is_alive():
            self.root.after(100, self.check_thread)
        else:
            self.root.destroy()
            self.finish_upload()
            
    def finish_upload(self):
        final_text = ""
        if self.urls:
            joined_urls = "\n".join(self.urls)
            copy_to_clipboard(joined_urls)
            final_text += f"Upload(s) completed successfully!\nLinks copied to clipboard:\n\n{joined_urls}"
        
        if self.errors:
            if final_text:
                final_text += "\n\nErrors:\n" + "\n".join(self.errors)
            else:
                final_text = "Errors occurred:\n" + "\n".join(self.errors)

        if self.urls and not self.errors:
            show_message("Catbox Uploader", final_text)
        elif self.errors and not self.urls:
            show_error("Catbox Uploader - Error", final_text)
        else:
            show_message("Catbox Uploader - Partial Upload", final_text)

def main():
    if len(sys.argv) <= 1:
        show_error("Catbox Uploader", "No files received.\n\nTo use this, drag and drop one or more files onto this application.")
        return

    files = sys.argv[1:]
    app = UploadApp(files)

if __name__ == "__main__":
    main()
