import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk

class DesktopRunnerLoop:
    def __init__(self, root):
        self.root = root
        self.root.title("Kontrol Karakter Loop")
        self.root.geometry("300x200")
        self.root.resizable(False, False)
        
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.run_frames = []
        self.char_window = None
        self.char_label = None
        self.animation_process = None
        
        self.icon_size = 100
        
        self.load_images()
        self.setup_control_window()
        
        if not self.run_frames:
            print("Error: Tidak ada gambar karakter yang ditemukan (contoh: run1.png, run2.png).")
            self.root.destroy()
            return

    def load_images(self):
   
        i = 1
        target_width = self.icon_size
        target_height = self.icon_size
        
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
        self.status_label = ttk.Label(main_frame, text="Status: Berhenti")
        self.status_label.pack(pady=(0, 10))

        ttk.Label(main_frame, text="Kecepatan:").pack()
        self.speed_scale = ttk.Scale(main_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.speed_scale.set(5)
        self.speed_scale.pack(fill=tk.X, expand=True, pady=5)
        ttk.Label(main_frame, text="Frame Delay:").pack()
        self.frame_delay_scale = ttk.Scale(main_frame, from_=1, to=30, orient=tk.HORIZONTAL)
        self.frame_delay_scale.set(10)
        self.frame_delay_scale.pack(fill=tk.X, expand=True, pady=5)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        self.start_button = ttk.Button(button_frame, text="Mulai Loop", command=self.start_loop)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_loop)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.quit_button = ttk.Button(button_frame, text="Keluar", command=self.quit_program)
        self.quit_button.pack(side=tk.LEFT, padx=5)

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

    def start_loop(self):
        if not self.run_frames:
            print("Tidak bisa memulai, gambar tidak ditemukan.")
            return
            
        if self.animation_process:
            self.root.after_cancel(self.animation_process)

        if not self.char_window or not self.char_window.winfo_exists():
            self.create_character_window()

        self.char_pos_x = -self.icon_size
        self.char_pos_y = self.screen_height - self.icon_size - 80
        
        speed = self.speed_scale.get()
        self.step_x = speed

        self.frame_delay = int(self.frame_delay_scale.get())
        
        self.frame_index = 0
        self.frame_counter = 0
        
        self.char_window.deiconify()
        self.status_label.config(text="Status: Berjalan")
        self.update_loop_animation()

    def update_loop_animation(self):

        self.char_pos_x += self.step_x
        
        if self.char_pos_x > self.screen_width:
            self.char_pos_x = -self.icon_size
    
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_index = (self.frame_index + 1) % len(self.run_frames)
            self.frame_counter = 0
        
        self.char_label.config(image=self.run_frames[self.frame_index])
        self.char_window.geometry(f'+{int(self.char_pos_x)}+{int(self.char_pos_y)}')

        if self.char_window.winfo_exists():
            self.animation_process = self.root.after(50, self.update_loop_animation)

    def stop_loop(self):

        if self.animation_process:
            self.root.after_cancel(self.animation_process)
            self.animation_process = None
        if self.char_window:
            self.char_window.withdraw()
        self.status_label.config(text="Status: Berhenti")

    def quit_program(self):

        self.stop_loop()
        if self.char_window:
            self.char_window.destroy()
        self.root.destroy()

if __name__ == "__main__":
    app_root = tk.Tk()
    app = DesktopRunnerLoop(app_root)
    app_root.mainloop()
