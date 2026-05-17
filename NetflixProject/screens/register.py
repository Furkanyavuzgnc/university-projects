import tkinter as tk
from tkinter import messagebox
from datetime import date
from database.db import db, cursor


class RegisterScreen:

    def __init__(self):

        self.window = tk.Toplevel()
        self.window.title("Kayıt Ol")
        self.window.geometry("400x650")

        # AD
        tk.Label(self.window, text="Ad").pack()
        self.name_entry = tk.Entry(self.window, width=30)
        self.name_entry.pack()

        # SOYAD
        tk.Label(self.window, text="Soyad").pack()
        self.surname_entry = tk.Entry(self.window, width=30)
        self.surname_entry.pack()

        # EMAIL
        tk.Label(self.window, text="E-Mail").pack()
        self.email_entry = tk.Entry(self.window, width=30)
        self.email_entry.pack()

        # ŞİFRE
        tk.Label(self.window, text="Şifre").pack()
        self.password_entry = tk.Entry(self.window, show="*", width=30)
        self.password_entry.pack()

        # ŞİFRE TEKRAR
        tk.Label(self.window, text="Şifre Tekrar").pack()
        self.password_again_entry = tk.Entry(self.window, show="*", width=30)
        self.password_again_entry.pack()

        # DOĞUM TARİHİ
        tk.Label(self.window, text="Doğum Tarihi (YIL-AY-GUN)").pack()
        self.birth_entry = tk.Entry(self.window, width=30)
        self.birth_entry.pack()

        # CİNSİYET
        tk.Label(self.window, text="Cinsiyet").pack()
        self.gender_entry = tk.Entry(self.window, width=30)
        self.gender_entry.pack()

        # ÜLKE
        tk.Label(self.window, text="Ülke").pack()
        self.country_entry = tk.Entry(self.window, width=30)
        self.country_entry.pack()

        # TÜR SEÇİMİ
        tk.Label(self.window, text="3 Favori Tür (virgülle yaz)").pack()
        self.genre_entry = tk.Entry(self.window, width=30)
        self.genre_entry.pack()

        tk.Label(self.window, text="Örnek: Aksiyon,Komedi,Dram").pack()

        tk.Button(
            self.window,
            text="Kayıt Ol",
            width=20,
            command=self.register
        ).pack(pady=20)

    def register(self):

        ad = self.name_entry.get()
        soyad = self.surname_entry.get()
        email = self.email_entry.get()
        sifre = self.password_entry.get()
        sifre_tekrar = self.password_again_entry.get()
        dogum = self.birth_entry.get()
        cinsiyet = self.gender_entry.get()
        ulke = self.country_entry.get()
        genres = self.genre_entry.get()

        # ❌ BOŞ KONTROL
        if not all([ad, soyad, email, sifre, sifre_tekrar, dogum, cinsiyet, ulke, genres]):
            messagebox.showerror("Hata", "Boş alan bırakmayınız")
            return

        # ❌ ŞİFRE KONTROL
        if len(sifre) < 6:
            messagebox.showerror("Hata", "Şifre en az 6 karakter olmalı")
            return

        if sifre != sifre_tekrar:
            messagebox.showerror("Hata", "Şifreler eşleşmiyor")
            return

        # ❌ DOĞUM TARİHİ KONTROL
        try:
            birth_date = date.fromisoformat(dogum)
            if birth_date > date.today():
                messagebox.showerror("Hata", "Doğum tarihi bugünden büyük olamaz")
                return
        except:
            messagebox.showerror("Hata", "Doğum tarihi formatı yanlış")
            return

        # ❌ EMAİL KONTROL
        cursor.execute("SELECT * FROM Kullanici WHERE email=%s", (email,))
        if cursor.fetchone():
            messagebox.showerror("Hata", "Bu email zaten kayıtlı")
            return

        # 👤 KULLANICI EKLE
        cursor.execute("""
            INSERT INTO Kullanici
            (ad, soyad, email, sifre, dogum_tarihi, cinsiyet, ulke, rol_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (ad, soyad, email, sifre, dogum, cinsiyet, ulke, 2))

        db.commit()

        user_id = cursor.lastrowid

        # 🎯 3 TÜR KONTROL
        genre_list = [g.strip() for g in genres.split(",")]

        if len(genre_list) != 3:
            messagebox.showerror("Hata", "Tam olarak 3 farklı tür seçmelisiniz")
            return

        # türleri kaydet
        for g in genre_list:
            cursor.execute("""
                INSERT INTO Kullanici_Tur (kullanici_id, tur_adi)
                VALUES (%s,%s)
            """, (user_id, g))

        db.commit()

        messagebox.showinfo("Başarılı", "Kayıt başarılı")

        self.window.destroy()

        # 🔥 KAYIT SONRASI ÖNERİ SİSTEMİ
        self.recommend(user_id)

    # ---------------- ÖNERİ SİSTEMİ ----------------
    def recommend(self, user_id):

        cursor.execute("""
            SELECT tur_adi
            FROM Kullanici_Tur
            WHERE kullanici_id=%s
        """, (user_id,))

        genres = cursor.fetchall()

        results = []

        for g in genres:

            cursor.execute("""
                SELECT *
                FROM Program
                WHERE program_tipi=%s
                ORDER BY ortalama_puan DESC
                LIMIT 2
            """, (g[0],))

            results += cursor.fetchall()

        win = tk.Toplevel()
        win.title("Sana Özel Öneriler")

        tk.Label(win, text="Önerilen İçerikler", font=("Arial", 14, "bold")).pack()

        for r in results:
            tk.Label(win, text=r[1]).pack()