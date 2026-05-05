import tkinter as tk
from labs.lab1_ui import Lab1Frame
from labs.lab2_ui import Lab2Frame
from labs.lab3_ui import Lab3Frame
from labs.lab4_ui import Lab4Frame
from labs.lab5_ui import Lab5Frame

class CryptoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Labs Solution")
        self.geometry("900x700")
        self.show_main_menu()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_screen()
        self.configure(bg="#B4517F")
        tk.Label(self, text="Головне меню", font=("Consolas", 18), bg="#B4517F", fg="white").pack(pady=20)
        btn_params = {"width": 30, "font": ("Consolas", 10)}

        tk.Button(self, text="ЛР №1: ГПВЧ", command=lambda: self.switch_frame(Lab1Frame), **btn_params).pack(pady=5)
        tk.Button(self, text="ЛР №2: MD5", command=lambda: self.switch_frame(Lab2Frame), **btn_params).pack(pady=5)
        tk.Button(self, text="ЛР №3: RC5 Шифрування", command=lambda: self.switch_frame(Lab3Frame), **btn_params).pack(pady=5)
        tk.Button(self, text="ЛР №4: RSA Асиметричне", command=lambda: self.switch_frame(Lab4Frame), **btn_params).pack(pady=5)
        tk.Button(self, text="ЛР №5: Цифровий підпис DSS", command=lambda: self.switch_frame(Lab5Frame), **btn_params).pack(pady=5)

    def switch_frame(self, frame_class):
        self.clear_screen()
        frame_class(self).pack(fill="both", expand=True)

if __name__ == "__main__":
    app = CryptoApp()
    app.mainloop()