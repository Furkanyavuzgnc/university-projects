import tkinter as tk
from tkinter import messagebox
from database.db import cursor, db


class ContentDetailScreen:

    def __init__(self, user_id, program):

        self.user_id = user_id
        self.program = program
        self.program_id = program[0]

        self.window = tk.Toplevel()
        self.window.title("İçerik Detay")
        self.window.geometry("500x600")

        # ---------------- PROGRAM DATA ----------------
        self.ad = program[1]
        self.aciklama = program[2]
        self.tip = program[3]
        self.tur = program[4]
        self.bolum_sayisi = program[5]
        self.sure = program[6]
        self.puan = program[7]
        self.izlenme = program[8]

        # ---------------- TITLE ----------------
        tk.Label(self.window, text=self.ad, font=("Arial", 16, "bold")).pack()

        tk.Label(self.window, text=self.aciklama).pack()

        tk.Label(self.window, text=f"Tip: {self.tip}").pack()
        tk.Label(self.window, text=f"Tür: {self.tur}").pack()
        tk.Label(self.window, text=f"Bölüm: {self.bolum_sayisi}").pack()
        tk.Label(self.window, text=f"Süre: {self.sure} dk").pack()
        tk.Label(self.window, text=f"Puan: {self.puan}").pack()
        tk.Label(self.window, text=f"İzlenme: {self.izlenme}").pack()

        # ---------------- USER STATUS ----------------
        self.check_status()

        # ---------------- FAVORITE BUTTON ----------------
        tk.Button(
            self.window,
            text="Favori Ekle / Çıkar",
            command=self.toggle_favorite
        ).pack(pady=5)

        # ---------------- WATCH BUTTON ----------------
        tk.Button(
            self.window,
            text="İzle",
            command=self.watch
        ).pack(pady=5)

        # ---------------- RATE ----------------
        tk.Button(
            self.window,
            text="Puan Ver",
            command=self.rate
        ).pack(pady=5)

        # ---------------- SERIES OPTIONS ----------------
        if self.tip.lower() == "dizi":

            tk.Label(self.window, text="Bölüm Seç").pack()

            self.ep_entry = tk.Entry(self.window)
            self.ep_entry.pack()

            tk.Button(
                self.window,
                text="Bölümü İzle",
                command=self.watch_episode
            ).pack(pady=5)

            tk.Button(
                self.window,
                text="Kaldığı Yerden Devam Et",
                command=self.continue_watching
            ).pack(pady=5)

    # ---------------- CHECK USER STATUS ----------------
    def check_status(self):

        # favori mi?
        cursor.execute("""
            SELECT * FROM Favori
            WHERE kullanici_id=%s AND program_id=%s
        """, (self.user_id, self.program_id))

        fav = cursor.fetchone()

        # izledi mi?
        cursor.execute("""
            SELECT * FROM Izleme
            WHERE kullanici_id=%s AND program_id=%s
        """, (self.user_id, self.program_id))

        watched = cursor.fetchone()

        tk.Label(
            self.window,
            text=f"Favori: {'Evet' if fav else 'Hayır'}"
        ).pack()

        tk.Label(
            self.window,
            text=f"İzledi: {'Evet' if watched else 'Hayır'}"
        ).pack()

    # ---------------- FAVORITE TOGGLE ----------------
    def toggle_favorite(self):

        cursor.execute("""
            SELECT * FROM Favori
            WHERE kullanici_id=%s AND program_id=%s
        """, (self.user_id, self.program_id))

        fav = cursor.fetchone()

        if fav:

            cursor.execute("""
                DELETE FROM Favori
                WHERE kullanici_id=%s AND program_id=%s
            """, (self.user_id, self.program_id))

            db.commit()
            messagebox.showinfo("OK", "Favoriden çıkarıldı")

        else:

            cursor.execute("""
                INSERT INTO Favori (kullanici_id, program_id)
                VALUES (%s,%s)
            """, (self.user_id, self.program_id))

            db.commit()
            messagebox.showinfo("OK", "Favoriye eklendi")

    # ---------------- WATCH ----------------
    def watch(self):

        cursor.execute("""
            INSERT INTO Izleme (kullanici_id, program_id, izlenme_sayisi)
            VALUES (%s,%s,1)
        """, (self.user_id, self.program_id))

        db.commit()
        messagebox.showinfo("OK", "İçerik izleniyor")

    # ---------------- RATE ----------------
    def rate(self):

        win = tk.Toplevel()
        win.title("Puan Ver")

        entry = tk.Entry(win)
        entry.pack()

        def save():

            rating = int(entry.get())

            cursor.execute("""
                UPDATE Program
                SET ortalama_puan = (ortalama_puan + %s) / 2
                WHERE program_id=%s
            """, (rating, self.program_id))

            db.commit()
            messagebox.showinfo("OK", "Puan verildi")
            win.destroy()

        tk.Button(win, text="Kaydet", command=save).pack()

    # ---------------- EPISODE WATCH ----------------
    def watch_episode(self):

        ep = self.ep_entry.get()

        cursor.execute("""
            INSERT INTO Izleme (kullanici_id, program_id, izlenme_sayisi, son_bolum)
            VALUES (%s,%s,1,%s)
        """, (self.user_id, self.program_id, ep))

        db.commit()
        messagebox.showinfo("OK", f"{ep}. bölüm izleniyor")

    # ---------------- CONTINUE WATCHING ----------------
    def continue_watching(self):

        cursor.execute("""
            SELECT son_bolum
            FROM Izleme
            WHERE kullanici_id=%s AND program_id=%s
            ORDER BY id DESC
            LIMIT 1
        """, (self.user_id, self.program_id))

        data = cursor.fetchone()

        if data and data[0]:

            messagebox.showinfo(
                "Devam",
                f"{data[0]}. bölümden devam ediliyor"
            )

        else:
            messagebox.showinfo("Bilgi", "Kayıtlı izleme yok")