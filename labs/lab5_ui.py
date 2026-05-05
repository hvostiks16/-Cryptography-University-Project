import tkinter as tk
from tkinter import filedialog, messagebox
import os
from labs.lab5_dsa import DSACore 

class Lab5Frame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#B4517F")
        self.public_key = None
        self.private_key = None
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Лабораторна робота №5: Цифровий підпис DSS", 
                 font=("Consolas", 16, "bold"), bg="#B4517F", fg="white").pack(pady=15)

        btn_style = {"bg": "#D775A3", "fg": "white", "font": ("Consolas", 10), 
                     "activebackground": "#8C3A61", "width": 22}

        key_frame = tk.LabelFrame(self, text="Керування ключами", bg="#B4517F", fg="white", 
                                  font=("Consolas", 12, "bold"), padx=10, pady=10)
        key_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Button(key_frame, text="Згенерувати ключі", command=self.generate_keys, **btn_style).pack(side="left", padx=10, expand=True)
        tk.Button(key_frame, text="Завантажити Priv Key", command=self.load_priv, **btn_style).pack(side="left", padx=10, expand=True)
        tk.Button(key_frame, text="Завантажити Pub Key", command=self.load_pub, **btn_style).pack(side="left", padx=10, expand=True)

        text_frame = tk.LabelFrame(self, text="Підпис рядка", bg="#B4517F", fg="white", 
                                   font=("Consolas", 12, "bold"), padx=10, pady=10)
        text_frame.pack(fill="x", padx=20, pady=5)
        
        self.text_input = tk.Entry(text_frame, font=("Consolas", 11), bg="#F6F6F6")
        self.text_input.pack(fill="x", padx=10, pady=5)
        tk.Button(text_frame, text="Підписати введений текст", command=self.sign_text, **btn_style).pack(pady=5)

        file_frame = tk.LabelFrame(self, text="Операції з файлами", bg="#B4517F", fg="white", 
                                   font=("Consolas", 12, "bold"), padx=10, pady=10)
        file_frame.pack(fill="x", padx=20, pady=5)

        tk.Button(file_frame, text="Підписати файл", command=self.sign_file, **btn_style).pack(side="left", padx=10, expand=True)
        tk.Button(file_frame, text="Перевірити підпис файлу", command=self.verify_file, **btn_style).pack(side="left", padx=10, expand=True)

        log_frame = tk.LabelFrame(self, text="Журнал подій та результати (HEX)", bg="#B4517F", fg="white", 
                                  font=("Consolas", 12, "bold"), padx=10, pady=5)
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)

        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side="right", fill="y")

        self.text_output = tk.Text(log_frame, height=10, bg="#D775A3", fg="#F6F6F6", 
                                   font=("Consolas", 11), state="disabled", yscrollcommand=scrollbar.set)
        self.text_output.pack(side="left", fill='both', expand=True)
        scrollbar.config(command=self.text_output.yview)

        bottom_frame = tk.Frame(self, bg="#B4517F")
        bottom_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Button(bottom_frame, text="Очистити журнал", command=self.clear_output, **btn_style).pack(side="right")
        tk.Button(bottom_frame, text="Зберегти у файл", command=self.save_log, **btn_style).pack(side="right", padx=10)

        if hasattr(self.master, "show_main_menu"):
            tk.Button(bottom_frame, text="← Назад до меню", command=self.master.show_main_menu, 
                      bg="#8C3A61", fg="white", font=("Consolas", 10)).pack(side="left")

    def log(self, msg):
        self.text_output.config(state="normal")
        self.text_output.insert(tk.END, msg + "\n")
        self.text_output.see(tk.END)
        self.text_output.config(state="disabled")

    def clear_output(self):
        self.text_output.config(state="normal")
        self.text_output.delete("1.0", tk.END)
        self.text_output.config(state="disabled")

    def generate_keys(self):
        try:
            priv, pub = DSACore.generate_keys()
            self.private_key = priv
            self.public_key = pub
            DSACore.save_private_key(priv, "dsa_private.pem")
            DSACore.save_public_key(pub, "dsa_public.pem")
            self.log("[+] Ключі згенеровано та збережено: 'dsa_private.pem', 'dsa_public.pem'.")
        except Exception as e:
            self.log(f"[-] Помилка генерації: {e}")

    def load_priv(self):
        filename = filedialog.askopenfilename(title="Виберіть private key", filetypes=[("PEM Files", "*.pem"), ("All Files", "*.*")])
        if filename:
            try:
                self.private_key = DSACore.load_private_key(filename)
                self.log(f"[+] Приватний ключ завантажено: {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося завантажити ключ: {e}")

    def load_pub(self):
        filename = filedialog.askopenfilename(title="Виберіть public key", filetypes=[("PEM Files", "*.pem"), ("All Files", "*.*")])
        if filename:
            try:
                self.public_key = DSACore.load_public_key(filename)
                self.log(f"[+] Публічний ключ завантажено: {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося завантажити ключ: {e}")

    def sign_text(self):
        if not self.private_key:
            messagebox.showwarning("Помилка", "Спочатку завантажте приватний ключ!")
            return
        text_data = self.text_input.get().encode()
        if not text_data:
            messagebox.showwarning("Помилка", "Поле вводу порожнє!")
            return
        
        signature = DSACore.sign_data(self.private_key, text_data)
        self.log(f"[*] Текст підписано: {self.text_input.get()}")
        self.log(f"[*] Підпис (HEX): {signature.hex()}")

    def sign_file(self):
        if not self.private_key:
            messagebox.showwarning("Помилка", "Завантажте приватний ключ!")
            return
        path = filedialog.askopenfilename(title="Виберіть файл для підпису")
        if path:
            try:
                with open(path, "rb") as f:
                    data = f.read()
                signature = DSACore.sign_data(self.private_key, data)
                sig_path = path + ".sig"
                with open(sig_path, "w") as f:
                    f.write(signature.hex())
                self.log(f"[+] Файл підписано: {os.path.basename(path)}")
                self.log(f"[*] Підпис збережено в: {os.path.basename(sig_path)}")
                self.log(f"[*] Значення (HEX): {signature.hex()}")
            except Exception as e:
                self.log(f"[-] Помилка підпису файлу: {e}")

    def verify_file(self):
        if not self.public_key:
            messagebox.showwarning("Помилка", "Завантажте публічний ключ!")
            return
        
        file_path = filedialog.askopenfilename(title="Виберіть файл даних")
        if not file_path: return
        
        sig_path = filedialog.askopenfilename(title="Виберіть файл підпису (.sig)")
        if not sig_path: return

        try:
            with open(file_path, "rb") as f:
                data = f.read()
            with open(sig_path, "r") as f:
                sig_hex = f.read().strip()
            
            signature = bytes.fromhex(sig_hex)
            is_valid = DSACore.verify_signature(self.public_key, signature, data)
            
            status = "ВЕРИФІКОВАНО (Дійсний)" if is_valid else "НЕПРАВИЛЬНО (Підроблено/Змінено)"
            self.log(f"[?] Результат перевірки {os.path.basename(file_path)}: {status}")
        except Exception as e:
            self.log(f"[-] Помилка верифікації: {e}")

    def save_log(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(self.text_output.get("1.0", tk.END))
                messagebox.showinfo("Успіх", "Журнал успішно збережено!")
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося зберегти файл: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("DSS Digital Signature Manager")
    root.geometry("800x700")
    app = Lab5Frame(root)
    app.pack(fill="both", expand=True)
    root.mainloop()