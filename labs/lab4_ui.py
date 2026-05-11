import tkinter as tk
from tkinter import filedialog, messagebox
import time
import os
from labs.lab4_rsa import RSACore
from labs.lab3_rc5 import RC5Manager

class Lab4Frame(tk.Frame):
    err = "Помилка"

    def __init__(self, master):
        super().__init__(master, bg="#B4517F")
        self.public_key = None
        self.private_key = None
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Лабораторна робота №4: RSA", 
                 font=("Consolas", 16, "bold"), bg="#B4517F", fg="white").pack(pady=15)

        btn_style = {"bg": "#D775A3", "fg": "white", "font": ("Consolas", 10), 
                     "activebackground": "#8C3A61", "width": 20}

        key_frame = tk.LabelFrame(self, text="Керування ключами", bg="#B4517F", fg="white", 
                                  font=("Consolas", 12, "bold"), padx=10, pady=10)
        key_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Button(key_frame, text="Згенерувати ключі", command=self.generate_keys, **btn_style).pack(side="left", padx=10, expand=True)
        tk.Button(key_frame, text="Завантажити Pub Key", command=self.load_pub, **btn_style).pack(side="left", padx=10, expand=True)
        tk.Button(key_frame, text="Завантажити Priv Key", command=self.load_priv, **btn_style).pack(side="left", padx=10, expand=True)

        crypto_frame = tk.LabelFrame(self, text="Операції з файлами", bg="#B4517F", fg="white", 
                                     font=("Consolas", 12, "bold"), padx=10, pady=10)
        crypto_frame.pack(fill="x", padx=20, pady=5)

        tk.Button(crypto_frame, text="Зашифрувати файл", command=self.encrypt, **btn_style).pack(side="left", padx=10, expand=True)
        tk.Button(crypto_frame, text="Дешифрувати файл", command=self.decrypt, **btn_style).pack(side="left", padx=10, expand=True)

        bench_frame = tk.LabelFrame(self, text="Порівняння швидкості", bg="#B4517F", fg="white", 
                                    font=("Consolas", 12, "bold"), padx=10, pady=10)
        bench_frame.pack(fill="x", padx=20, pady=5)

        tk.Button(bench_frame, text="Вибрати файл та порівняти з RC5", command=self.select_and_benchmark, 
                  bg="#8C3A61", fg="white", font=("Consolas", 10, "bold"), width=45).pack(pady=5)

        log_frame = tk.LabelFrame(self, text="Журнал подій ", bg="#B4517F", fg="white", 
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
        priv, pub = RSACore.generate_keys()
        self.private_key = priv
        self.public_key = pub

        RSACore.save_private_key(priv, "private.pem")
        RSACore.save_public_key(pub, "public.pem")
        self.log("[+] Ключі згенеровано та збережено як 'private.pem' та 'public.pem'.")

    def load_pub(self):
        filename = filedialog.askopenfilename(title="Виберіть public.pem", filetypes=[("PEM Files", "*.pem"), ("All Files", "*.*")])
        if filename:
            try:
                self.public_key = RSACore.load_public_key(filename)
                self.log(f"[+] Публічний ключ завантажено з: {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror(self.err, f"Не вдалося завантажити ключ: {e}")

    def load_priv(self):
        filename = filedialog.askopenfilename(title="Виберіть private.pem", filetypes=[("PEM Files", "*.pem"), ("All Files", "*.*")])
        if filename:
            try:
                self.private_key = RSACore.load_private_key(filename)
                self.log(f"[+] Приватний ключ завантажено з: {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror(self.err, f"Не вдалося завантажити ключ: {e}")

    def encrypt(self):
        if not self.public_key:
            messagebox.showwarning(self.err, "Спочатку завантажте або згенеруйте публічний ключ!")
            return
            
        filename = filedialog.askopenfilename(title="Файл для шифрування")
        if filename:
            out_file = filename + ".rsa"
            start_time = time.time()
            try:
                RSACore.encrypt_file(filename, out_file, self.public_key)
                elapsed = time.time() - start_time
                self.log(f"[*] Файл зашифровано: {os.path.basename(out_file)}")
                self.log(f"[*] Час шифрування: {elapsed:.4f} сек")
            except Exception as e:
                self.log(f"[-] Помилка шифрування: {e}")

    def decrypt(self):
        if not self.private_key:
            messagebox.showwarning(self.err, "Спочатку завантажте або згенеруйте приватний ключ!")
            return
            
        filename = filedialog.askopenfilename(title="Файл для дешифрування")
        if filename:
            out_file = filename.replace(".rsa", "")
            if out_file == filename:
                out_file = filename + ".dec"
            
            start_time = time.time()
            try:
                RSACore.decrypt_file(filename, out_file, self.private_key)
                elapsed = time.time() - start_time
                self.log(f"[*] Файл розшифровано: {os.path.basename(out_file)}")
                self.log(f"[*] Час розшифрування: {elapsed:.4f} сек")
            except Exception as e:
                self.log(f"[-] Помилка дешифрування: {e}")
                
    def select_and_benchmark(self):
        filename = filedialog.askopenfilename(title="Виберіть файл для тестування швидкості")
        if filename:
            self.run_benchmark(filename)

    def run_benchmark(self, input_file_path):
        if not os.path.exists(input_file_path):
            self.log(f"[!] Помилка: Файл {input_file_path} не знайдено.")
            return

        if not self.public_key or not self.private_key:
            self.log("[!] Для тесту потрібні ключі RSA. Генерую тимчасові...")
            self.generate_keys()

        file_size_kb = os.path.getsize(input_file_path) / 1024
        self.log(f"\n--- ПОРІВНЯННЯ ШВИДКОСТІ (Файл: {os.path.basename(input_file_path)}, Розмір: {file_size_kb:.2f} КБ) ---")
        self.update()

        rsa_enc = "temp_rsa.enc"
        rsa_dec = "temp_rsa.dec"
        rc5_enc = "temp_rc5.enc"
        rc5_dec = "temp_rc5.dec"

        try:
            t0 = time.perf_counter()
            RSACore.encrypt_file(input_file_path, rsa_enc, self.public_key)
            rsa_enc_time = time.perf_counter() - t0
            
            t0 = time.perf_counter()
            RSACore.decrypt_file(rsa_enc, rsa_dec, self.private_key)
            rsa_dec_time = time.perf_counter() - t0
            
            rc5_password = "benchmark_password"
            t0 = time.perf_counter()
            RC5Manager.encrypt_file(input_file_path, rc5_enc, rc5_password, key_size_bits=128)
            rc5_enc_time = time.perf_counter() - t0
            
            t0 = time.perf_counter()
            RC5Manager.decrypt_file(rc5_enc, rc5_dec, rc5_password, key_size_bits=128)
            rc5_dec_time = time.perf_counter() - t0
            
            self.log(f"Час RSA (Шифр/Дешифр): {rsa_enc_time:.4f} с / {rsa_dec_time:.4f} с")
            self.log(f"Час RC5 (Шифр/Дешифр): {rc5_enc_time:.4f} с / {rc5_dec_time:.4f} с")

            if rc5_enc_time > 0:
                ratio = rsa_enc_time / rc5_enc_time
                self.log(f"\nРезультат: ширування RC5 швидше за RSA у {ratio:.1f} разів.")
                ratio = rsa_dec_time / rc5_dec_time
                self.log(f"\nРезультат: деширування RC5 швидше за RSA у {ratio:.1f} разів.")
        except Exception as e:
            self.log(f"[!] Сталася помилка під час тестування: {str(e)}")
        finally:
            for f in [rsa_enc, rsa_dec, rc5_enc, rc5_dec]:
                if os.path.exists(f):
                    os.remove(f)
        self.log("--- ТЕСТУВАННЯ ЗАВЕРШЕНО ---\n")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("RSA Шифрування")
    root.geometry("600x700") 
    app = Lab4Frame(root)
    app.pack(fill="both", expand=True)
    root.mainloop()