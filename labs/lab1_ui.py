import tkinter as tk
from tkinter import messagebox, filedialog
import math
from labs.lab1_lcg import LCGCore

class Lab1Frame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#B4517F")
        self.logic = LCGCore()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Лабораторна робота №1: LCG", 
                 font=("Consolas", 14, "bold"), bg="#B4517F", fg="white").pack(pady=10)

        input_frame = tk.Frame(self, bg="#B4517F")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Кількість чисел:", 
                 bg="#B4517F", fg="#F6F6F6", font=("Consolas", 12, "bold")).grid(row=0, column=0, padx=5)

        self.entry_n = tk.Entry(input_frame, font=("Consolas", 12), bg="#B4517F", fg="#F6F6F6", insertbackground="white")
        self.entry_n.insert(0, "100")
        self.entry_n.grid(row=0, column=1, padx=5)

        btn_style = {"bg": "#D775A3", "fg": "white", "font": ("Consolas", 10), "activebackground": "#8C3A61"}
        
        tk.Button(input_frame, text="Запустити", command=self.run_generator, **btn_style).grid(row=0, column=2, padx=5)
        tk.Button(input_frame, text="Оцінка π", command=self.run_pi_eval, **btn_style).grid(row=0, column=3, padx=5)
        tk.Button(input_frame, text="Період", command=self.count_period, **btn_style).grid(row=0, column=4, padx=5)
        tk.Button(input_frame, text="Очистити", command=self.clear_output, **btn_style).grid(row=0, column=5, padx=5)

        self.text_output = tk.Text(self, height=15, bg="#D775A3", fg="#F6F6F6", 
                                   font=("Consolas", 11), state="disabled")
        self.text_output.pack(pady=20, fill='both', expand=True, padx=20)

        tk.Button(self, text="← Назад до меню", command=self.master.show_main_menu, 
                  bg="#8C3A61", fg="white", font=("Consolas", 10)).pack(side="bottom", pady=15)

    def log(self, message):
        self.text_output.config(state="normal")
        self.text_output.insert(tk.END, message)
        self.text_output.see(tk.END)
        self.text_output.config(state="disabled")

    def run_generator(self):
        try:
            n = int(self.entry_n.get())
            seq = self.logic.lcg(n)
            
            self.log(f"Згенеровано {n} чисел. \nПерші 50: {seq[:50]}...\n\n")
            
            filename = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                   filetypes=[("Text files","*.txt")])
            if filename:
                with open(filename, "w") as f:
                    f.write("\n".join(map(str, seq)))
                messagebox.showinfo("Успіх", "Файл збережено!")
        except ValueError:
            messagebox.showerror("Помилка", "Будь ласка, введіть коректне ціле число!")

    def run_pi_eval(self):
        try:
            n = int(self.entry_n.get())
            pi_lcg = self.logic.estimate_pi_lcg(n)
            pi_sys = self.logic.estimate_pi_system(n)
            
            self.log(f"Оцінка π (LCG, n={n}): \t\t\t\t{pi_lcg}\n")
            self.log(f"Оцінка π (System random): \t\t\t\t{pi_sys}\n")
            self.log(f"Еталонне π: \t\t\t\t{math.pi}\n")
            self.log(f"Абсолютна похибка (LCG, n={n}): \t\t{abs(pi_lcg-math.pi):.6f}\n")
            self.log(f"Абсолютна похибка (System random): \t\t{abs(pi_sys-math.pi):.6f}\n\n")
        except ValueError:
            messagebox.showerror("Помилка", "Введіть ціле число для оцінки π!")

    def count_period(self):
        self.log("Обчислення періоду... \n")
        period = self.logic.lcg_period()
        self.log(f"Результат: Період = {period}\n\n")

    def clear_output(self):
        self.text_output.config(state="normal")
        self.text_output.delete("1.0", tk.END)
        self.text_output.config(state="disabled")