import tkinter as tk
from tkinter import filedialog, messagebox
from labs.lab2_md5 import MD5Core

class Lab2Frame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#B4517F")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Лабораторна робота №2: MD5", 
                 font=("Consolas", 14, "bold"), bg="#B4517F", fg="white").pack(pady=10)

        input_frame = tk.Frame(self, bg="#B4517F")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Рядок для хешування:", 
                 bg="#B4517F", fg="#F6F6F6", font=("Consolas", 12, "bold")).grid(row=0, column=0, padx=5)

        self.entry_text = tk.Entry(input_frame, font=("Consolas", 12), 
                                   bg="#B4517F", fg="#F6F6F6", insertbackground="white", width=40)
        self.entry_text.grid(row=0, column=1, padx=5)

        btn_style = {"bg": "#D775A3", "fg": "white", "font": ("Consolas", 10), "activebackground": "#8C3A61"}
        
        tk.Button(input_frame, text="Хеш рядка", command=self.hash_string, **btn_style).grid(row=0, column=2, padx=5)
        tk.Button(input_frame, text="Хеш файлу", command=self.hash_file, **btn_style).grid(row=0, column=3, padx=5)
        tk.Button(input_frame, text="Перевірити файл", command=self.verify_file, **btn_style).grid(row=0, column=4, padx=5)
        tk.Button(input_frame, text="Тест", command=self.run_tests, **btn_style).grid(row=0, column=5, padx=5)
        tk.Button(input_frame, text="Очистити", command=self.clear_output, **btn_style).grid(row=0, column=6, padx=5)
        tk.Button(input_frame, text="Зберегти у файл", command=self.save_output, **btn_style).grid(row=0, column=7, padx=5)

        self.text_output = tk.Text(self, height=15, bg="#D775A3", fg="#F6F6F6", 
                                   font=("Consolas", 11), state="disabled")
        self.text_output.pack(pady=20, fill='both', expand=True, padx=20)

        tk.Button(self, text="← Назад до меню", command=self.master.show_main_menu, 
                  bg="#8C3A61", fg="white", font=("Consolas", 10)).pack(side="bottom", pady=15)

    def log(self, msg):
        self.text_output.config(state="normal")
        self.text_output.insert(tk.END, msg + "\n")
        self.text_output.see(tk.END)
        self.text_output.config(state="disabled")

    def hash_string(self):
        s = self.entry_text.get()
        h = MD5Core.hash_string(s)
        self.log(f"H({s}) = {h}")

    def hash_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            h = MD5Core.hash_file(filename)
            self.log(f"{h}")

    def verify_file(self):
        filename = filedialog.askopenfilename(title="Виберіть файл для перевірки")
        md5file = filedialog.askopenfilename(title="Виберіть .md5 файл")
        if filename and md5file:
            if MD5Core.verify_file(filename, md5file):
                messagebox.showinfo("Перевірка", "Файл цілісний ✅")
            else:
                messagebox.showerror("Перевірка", "Файл пошкоджено ❌")

    def run_tests(self):
        results = MD5Core.run_tests()
        self.log(results)

    def clear_output(self):
        self.text_output.config(state="normal")
        self.text_output.delete("1.0", tk.END)
        self.text_output.config(state="disabled")

    def save_output(self):
        content = self.text_output.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Збереження", "Немає даних для збереження!")
            return
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Збереження", f"Результати збережено у файл:\n{filename}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("MD5 Хешування")
    app = Lab2Frame(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
