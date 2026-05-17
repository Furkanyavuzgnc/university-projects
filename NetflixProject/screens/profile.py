import tkinter as tk
from tkinter import messagebox
from database.db import cursor, db


class ProfileScreen:

    def __init__(self, user_data):

        self.user_data = user_data
        self.user_id = user_data[0]

        self.window = tk.Toplevel()
        self.window.title("Profil")
        self.window.geometry("600x700")

        # ================= SCROLL AREA =================
        canvas = tk.Canvas(self.window)
        scrollbar = tk.Scrollbar(self.window, orient="vertical", command=canvas.yview)

        self.scroll_frame = tk.Frame(canvas)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ================= TITLE =================
        tk.Label(
            self.scroll_frame,
            text="Profil Bilgileri",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        # ================= DATA =================
        cursor.execute("""
            SELECT ad, soyad, email, dogum_tarihi, ulke
            FROM Kullanici
            WHERE kullanici_id=%s
        """, (self.user_id,))

        user = cursor.fetchone()

        # ================= FIELDS =================
        self.name_entry = self.create_field("Ad", user[0])
        self.surname_entry = self.create_field("Soyad", user[1])
        self.email_entry = self.create_field("Email", user[2])
        self.birth_entry = self.create_field("Doğum Tarihi", user[3])
        self.country_entry = self.create_field("Ülke", user[4])

        # ================= PASSWORD =================
        tk.Label(self.scroll_frame, text="Yeni Şifre").pack()
        self.password_entry = tk.Entry(self.scroll_frame, width=30, show="*")
        self.password_entry.pack(pady=5)

        # ================= FAVORITES =================
        cursor.execute("""
            SELECT tur_adi
            FROM Kullanici_Tur
            WHERE kullanici_id=%s
        """, (self.user_id,))

        genres = cursor.fetchall()
        genre_text = ", ".join([g[0] for g in genres]) if genres else "-"

        tk.Label(
            self.scroll_frame,
            text=f"Favori Türler: {genre_text}"
        ).pack(pady=10)

        # ================= STATS =================
        self.show_stats()

        # ================= UPDATE BUTTON =================
        tk.Button(
            self.scroll_frame,
            text="Güncelle",
            bg="green",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.update_profile
        ).pack(pady=20)

    # =================================================
    def create_field(self, label, value):

        tk.Label(self.scroll_frame, text=label).pack()

        entry = tk.Entry(self.scroll_frame, width=40)
        entry.pack(pady=2)

        if value is not None:
            entry.insert(0, str(value))

        return entry

    # =================================================
    def show_stats(self):

        cursor.execute("""
            SELECT IFNULL(SUM(izleme_suresi),0)
            FROM IzlemeLog
            WHERE kullanici_id=%s
        """, (self.user_id,))
        total_time = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(DISTINCT program_id)
            FROM IzlemeLog
            WHERE kullanici_id=%s
        """, (self.user_id,))
        watched_count = cursor.fetchone()[0]

        cursor.execute("""
            SELECT IFNULL(AVG(puan),0)
            FROM IzlemeLog
            WHERE kullanici_id=%s
        """, (self.user_id,))
        avg_rating = cursor.fetchone()[0]

        tk.Label(
            self.scroll_frame,
            text="--- İSTATİSTİKLER ---",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        tk.Label(
            self.scroll_frame,
            text=f"Toplam İzleme Süresi: {total_time} dk"
        ).pack()

        tk.Label(
            self.scroll_frame,
            text=f"İzlenen İçerik Sayısı: {watched_count}"
        ).pack()

        tk.Label(
            self.scroll_frame,
            text=f"Ortalama Puan: {round(float(avg_rating), 2)}"
        ).pack()

    # =================================================
    def update_profile(self):

        name = self.name_entry.get()
        surname = self.surname_entry.get()
        email = self.email_entry.get()
        birth = self.birth_entry.get()
        country = self.country_entry.get()
        password = self.password_entry.get()

        if not all([name, surname, email, birth, country]):
            messagebox.showerror("Hata", "Boş alan bırakmayınız")
            return

        cursor.execute("""
            UPDATE Kullanici
            SET ad=%s,
                soyad=%s,
                email=%s,
                dogum_tarihi=%s,
                ulke=%s,
                sifre=CASE WHEN %s != '' THEN %s ELSE sifre END
            WHERE kullanici_id=%s
        """, (name, surname, email, birth, country, password, password, self.user_id))

        db.commit()

        messagebox.showinfo("Başarılı", "Profil güncellendi")