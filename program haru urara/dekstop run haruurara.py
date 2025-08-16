import tkinter as tk
from tkinter import ttk
import os


from PIL import Image, ImageTk

class DesktopRunner:
    def __init__(self, root):
        self.root = root
        self.root.title("Kontrol Karakter Desktop")
        self.root.geometry("300x150")
        self.root.resizable(False, False)
        

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.run_frames = []
        self.char_window = None
        self.char_label = None
        self.animation_process = None
        
        self.icon_size = 48
        
        self.load_images()
        self.setup_control_window()
        
        if not self.run_frames:
            print("Error: Tidak ada gambar karakter yang ditemukan (contoh: run1.png, run2.png).")
            self.root.destroy()
            return

    def load_images(self):

        i = 1
        target_width = 100 
        target_height = 100
        
        while True:
            try:
                filepath = os.path.join(os.path.dirname(__file__), f'run{i}.png')
                if os.path.exists(filepath):
                    pil_image = Image.open(filepath)
                    pil_image = pil_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
                    tk_image = ImageTk.PhotoImage(pil_image)
                    self.run_frames.append(tk_image)
                    print(f"Loaded run{i}.png as {target_width}x{target_height}")
                    i += 1
                else:
                    break
            except Exception as e:
                print(f"Failed to load run{i}.png: {e}")
                break

    def setup_control_window(self):

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Atur Waktu Lari (detik):").pack(pady=(0, 5))

        self.duration_scale = ttk.Scale(main_frame, from_=1, to=20, orient=tk.HORIZONTAL)
        self.duration_scale.set(5)
        self.duration_scale.pack(fill=tk.X, expand=True, pady=5)

        start_button = ttk.Button(main_frame, text="Mulai Lari!", command=self.start_run)
        start_button.pack(pady=10)

    def create_character_window(self):
      
        if self.char_window:
            self.char_window.destroy()

        self.char_window = tk.Toplevel(self.root)
        self.char_window.overrideredirect(True) 
        self.char_window.wm_attributes('-topmost', True)
        transparent_color = 'magenta' 
        self.char_window.config(bg=transparent_color)
        self.char_window.wm_attributes('-transparentcolor', transparent_color)

        self.char_label = tk.Label(self.char_window, bg=transparent_color)
        self.char_label.pack()
        self.char_window.withdraw()

    def start_run(self):
        """penyiapan animasi"""
        if not self.run_frames:
            print("Tidak bisa memulai, gambar tidak ditemukan.")
            return
            
        if self.animation_process:
            self.root.after_cancel(self.animation_process)

        if not self.char_window or not self.char_window.winfo_exists():
            self.create_character_window()

        duration_seconds = self.duration_scale.get()
        image_width = self.icon_size
        self.char_pos_x = -image_width
        self.char_pos_y = self.screen_height - self.icon_size - 80
        
        update_interval_ms = 20
        total_distance = self.screen_width + image_width
        total_updates = (duration_seconds * 1000) / update_interval_ms
        self.step_x = total_distance / total_updates
        
        self.frame_index = 0
        
        self.char_window.deiconify()
        self.update_animation()

    def update_animation(self):
        self.char_pos_x += self.step_x
        
        if int(self.char_pos_x) % 3 == 0:
            self.frame_index = (self.frame_index + 1) % len(self.run_frames)
        
        self.char_label.config(image=self.run_frames[self.frame_index])
        self.char_window.geometry(f'+{int(self.char_pos_x)}+{int(self.char_pos_y)}')

        if self.char_pos_x < self.screen_width:
            self.animation_process = self.root.after(20, self.update_animation)
        else:
            self.char_window.withdraw()

if __name__ == "__main__":
    app_root = tk.Tk()
    app = DesktopRunner(app_root)
    app_root.mainloop()
