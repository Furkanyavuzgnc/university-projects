import tkinter as tk
from tkinter import messagebox
from screens.register import RegisterScreen
from database.db import cursor
from screens.home import HomeScreen
from screens.admin import AdminScreen


class LoginScreen:

    def __init__(self):

        self.window = tk.Tk()
        self.window.title("Netflix Login")
        self.window.geometry("400x300")

        tk.Label(self.window, text="E-Mail").pack(pady=5)

        self.email_entry = tk.Entry(self.window, width=30)
        self.email_entry.pack()

        tk.Label(self.window, text="Şifre").pack(pady=5)

        self.password_entry = tk.Entry(self.window, show="*", width=30)
        self.password_entry.pack()

        tk.Button(
            self.window,
            text="Giriş Yap",
            width=20,
            command=self.login
        ).pack(pady=10)

        tk.Button(
            self.window,
            text="Kayıt Ol",
            width=20,
            command=self.open_register
        ).pack()

        self.window.mainloop()

    def login(self):

        email = self.email_entry.get()
        password = self.password_entry.get()

        if email == "" or password == "":
            messagebox.showerror("Hata", "Boş alan bırakmayınız")
            return

        # 🔐 ADMIN CHECK (SABİT HESAP)
        if email == "admin" and password == "admin":

            messagebox.showinfo("Başarılı", "Admin girişi başarılı")

            AdminScreen()
            return

        # 👤 NORMAL USER CHECK
        query = """
        SELECT * FROM Kullanici
        WHERE email=%s AND sifre=%s
        """

        cursor.execute(query, (email, password))
        user = cursor.fetchone()

        if user:

            messagebox.showinfo("Başarılı", "Giriş başarılı")

            HomeScreen(user)

        else:

            messagebox.showerror("Hata", "Email veya şifre yanlış")

    def open_register(self):
        RegisterScreen()