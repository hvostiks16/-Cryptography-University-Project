import tkinter as tk
from tkinter import filedialog, messagebox
import time
from labs.lab3_rc5 import RC5Manager 

class Lab3Frame(tk.Frame):
    def __init__(self, master):
        self.bg_main = "#B4517F"
        self.bg_accent = "#8C3A61"
        self.bg_field = "#D775A3"
        self.fg_white = "#F6F6F6"
        
        super().__init__(master, bg=self.bg_main)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Лабораторна робота №3: RC5-64/8/16", 
                 font=("Consolas", 16, "bold"), bg=self.bg_main, fg="white").pack(pady=15)

        input_frame = tk.Frame(self, bg=self.bg_main)
        input_frame.pack(pady=5, padx=20)

        tk.Label(input_frame, text="Парольна фраза:", 
                 bg=self.bg_main, fg=self.fg_white, font=("Consolas", 12, "bold")).grid(row=0, column=0, sticky="e", padx=5, pady=10)

        self.entry_pass = tk.Entry(input_frame, font=("Consolas", 12), 
                                   bg=self.bg_field, fg="white", insertbackground="white", width=25)
        self.entry_pass.grid(row=0, column=1, padx=5, pady=10)

        tk.Label(input_frame, text="Ключ (біти):", 
                 bg=self.bg_main, fg=self.fg_white, font=("Consolas", 12, "bold")).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        
        self.key_size_var = tk.IntVar(value=128)
        radio_frame = tk.Frame(input_frame, bg=self.bg_main)
        radio_frame.grid(row=1, column=1, sticky="w", padx=5)
        
        radio_style = {"bg": self.bg_main, "fg": "white", "selectcolor": self.bg_accent, 
                       "activebackground": self.bg_main, "font": ("Consolas", 10)}
        
        tk.Radiobutton(radio_frame, text="64", variable=self.key_size_var, value=64, **radio_style).pack(side="left")
        tk.Radiobutton(radio_frame, text="128", variable=self.key_size_var, value=128, **radio_style).pack(side="left")
        tk.Radiobutton(radio_frame, text="256", variable=self.key_size_var, value=256, **radio_style).pack(side="left")

        btn_frame = tk.Frame(self, bg=self.bg_main)
        btn_frame.pack(pady=15)
        
        btn_style = {"bg": self.bg_field, "fg": "white", "font": ("Consolas", 11, "bold"), 
                     "activebackground": self.bg_accent, "width": 18, "cursor": "hand2"}
        
        tk.Button(btn_frame, text="Зашифрувати", command=self.encrypt_action, **btn_style).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Розшифрувати", command=self.decrypt_action, **btn_style).grid(row=0, column=1, padx=10)

        # Вивід логів
        self.text_output = tk.Text(self, height=10, bg=self.bg_accent, fg=self.fg_white,
                                   font=("Consolas", 10), state="disabled", padx=10, pady=10)
        self.text_output.pack(pady=10, fill='both', expand=True, padx=30)

        bottom_frame = tk.Frame(self, bg=self.bg_main)
        bottom_frame.pack(side="bottom", fill="x", pady=10)

        tk.Button(bottom_frame, text="Очистити лог", command=self.clear_log, 
                  bg=self.bg_main, fg="white", font=("Consolas", 9), bd=0).pack(side="right", padx=30)

        tk.Button(bottom_frame, text="← Назад до меню", command=self.master.show_main_menu, 
                  bg=self.bg_accent, fg="white", font=("Consolas", 10, "bold"), width=15).pack(side="left", padx=30)

    def log(self, msg):
        self.text_output.config(state="normal")
        timestamp = time.strftime("[%H:%M:%S] ")
        self.text_output.insert(tk.END, timestamp + msg + "\n")
        self.text_output.see(tk.END)
        self.text_output.config(state="disabled")

    def clear_log(self):
        self.text_output.config(state="normal")
        self.text_output.delete('1.0', tk.END)
        self.text_output.config(state="disabled")

    def validate_password(self):
        pwd = self.entry_pass.get()
        if not pwd:
            messagebox.showwarning("Помилка", "Введіть пароль для генерації ключа!")
            return None
        return pwd

    def encrypt_action(self):
        pwd = self.validate_password()
        if not pwd: return

        in_file = filedialog.askopenfilename(title="Виберіть файл для шифрування")
        if not in_file: return

        out_file = filedialog.asksaveasfilename(title="Зберегти зашифрований файл як", defaultextension=".enc")
        if not out_file: return

        try:
            k_size = self.key_size_var.get()
            RC5Manager.encrypt_file(in_file, out_file, pwd, k_size)
            self.log(f"ENCRYPT: {in_file} -> {out_file} ({k_size} bits)")
            messagebox.showinfo("Успіх", "Шифрування завершено успішно!")
        except Exception as e:
            self.log(f"ERROR: {str(e)}")
            messagebox.showerror("Помилка шифрування", str(e))

    def decrypt_action(self):
        pwd = self.validate_password()
        if not pwd: return

        in_file = filedialog.askopenfilename(title="Виберіть файл для дешифрування")
        if not in_file: return

        suggested_name = in_file.replace(".enc", "_decrypted")
        out_file = filedialog.asksaveasfilename(title="Зберегти розшифрований файл як", initialfile=suggested_name)
        if not out_file: return

        try:
            k_size = self.key_size_var.get()
            RC5Manager.decrypt_file(in_file, out_file, pwd, k_size)
            self.log(f"DECRYPT: {in_file} -> {out_file}")
            messagebox.showinfo("Успіх", "Дешифрування завершено успішно!")
        except Exception as e:
            self.log(f"ERROR: {str(e)}")
            messagebox.showerror("Помилка дешифрування", f"Перевірте пароль!\n{str(e)}")