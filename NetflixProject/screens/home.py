import tkinter as tk
from tkinter import ttk, messagebox

from database.db import cursor, db

from screens.watch import WatchScreen
from screens.favorites import FavoritesScreen
from screens.history import HistoryScreen
from screens.profile import ProfileScreen


class HomeScreen:

    def __init__(self, user_data):

        self.user_data = user_data
        self.user_id = user_data[0]

        self.window = tk.Toplevel()
        self.window.title("Kullanıcı Ana Sayfa")
        self.window.geometry("1200x800")
        self.window.configure(bg="#f2f2f2")

        # =================================================
        # HEADER
        # =================================================
        tk.Label(
            self.window,
            text=f"Hoşgeldin {user_data[1]}",
            font=("Arial", 20, "bold"),
            bg="#f2f2f2"
        ).pack(pady=10)

        # =================================================
        # NAVIGATION
        # =================================================
        nav = tk.Frame(self.window, bg="#f2f2f2")
        nav.pack(pady=5)

        tk.Button(
            nav,
            text="Profil",
            width=15,
            command=self.open_profile
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            nav,
            text="Geçmiş",
            width=15,
            command=self.open_history
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            nav,
            text="Favoriler",
            width=15,
            command=self.open_favorites
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            nav,
            text="Öneriler",
            width=15,
            command=self.show_recommendations
        ).grid(row=0, column=3, padx=5)

        # =================================================
        # SEARCH
        # =================================================
        search = tk.Frame(self.window, bg="#f2f2f2")
        search.pack(pady=10)

        self.search_entry = tk.Entry(search, width=35)
        self.search_entry.grid(row=0, column=0, padx=5)

        self.type_filter = ttk.Combobox(
            search,
            values=["Tümü", "Film", "Dizi"],
            state="readonly",
            width=15
        )

        self.type_filter.current(0)
        self.type_filter.grid(row=0, column=1, padx=5)

        tk.Button(
            search,
            text="Ara",
            width=10,
            command=self.search
        ).grid(row=0, column=2)

        # =================================================
        # FILTER BUTTONS
        # =================================================
        filter_frame = tk.Frame(self.window, bg="#f2f2f2")
        filter_frame.pack(pady=5)

        tk.Button(
            filter_frame,
            text="En Yüksek Puanlılar",
            width=20,
            command=self.show_top_rated
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            filter_frame,
            text="En Çok İzlenenler",
            width=20,
            command=self.show_most_watched
        ).grid(row=0, column=1, padx=5)

        # =================================================
        # CONTENT AREA
        # =================================================
        self.frame = tk.Frame(self.window, bg="#f2f2f2")
        self.frame.pack(fill="both", expand=True)

        self.load_programs()

    # =================================================
    # CLEAR SCREEN
    # =================================================
    def clear(self):

        for widget in self.frame.winfo_children():
            widget.destroy()

    # =================================================
    # LOAD PROGRAMS
    # =================================================
    def load_programs(self, programs=None):

        self.clear()

        if programs is None:

            cursor.execute("""
                SELECT *
                FROM Program
                ORDER BY ortalama_puan DESC
            """)

            programs = cursor.fetchall()

        if not programs:

            tk.Label(
                self.frame,
                text="Program bulunamadı",
                font=("Arial", 16, "bold"),
                bg="#f2f2f2"
            ).pack(pady=30)

            return

        for p in programs:
            self.create_card(p)

    # =================================================
    # CREATE CARD
    # =================================================
    def create_card(self, p):

        card = tk.Frame(
            self.frame,
            bd=2,
            relief="solid",
            padx=10,
            pady=10,
            bg="white"
        )

        card.pack(fill="x", padx=10, pady=6)

        program_id = p[0]

        # DATABASE COLUMN STRUCTURE
        # 0 program_id
        # 1 program_adi
        # 2 aciklama
        # 3 program_tipi
        # 4 cikis_yili
        # 5 bolum_sayisi
        # 6 sure
        # 7 ortalama_puan
        # 8 izlenme_sayisi

        tk.Label(
            card,
            text=p[1],
            font=("Arial", 15, "bold"),
            bg="white"
        ).pack(anchor="w")

        tk.Label(
            card,
            text=f"Tip: {p[3]} | Çıkış Yılı: {p[4]}",
            bg="white"
        ).pack(anchor="w")

        tk.Label(
            card,
            text=f"Bölüm Sayısı: {p[5]} | Süre: {p[6]} dk",
            bg="white"
        ).pack(anchor="w")

        tk.Label(
            card,
            text=f"Ortalama Puan: {round(float(p[7]), 1)} | İzlenme: {p[8]}",
            bg="white"
        ).pack(anchor="w")

        tk.Label(
            card,
            text=p[2],
            wraplength=1000,
            justify="left",
            bg="white"
        ).pack(anchor="w", pady=5)

        btn_frame = tk.Frame(card, bg="white")
        btn_frame.pack(anchor="e", pady=5)

        tk.Button(
            btn_frame,
            text="İzle",
            command=lambda: self.watch(program_id)
        ).pack(side="left", padx=3)

        tk.Button(
            btn_frame,
            text="Favori",
            command=lambda: self.add_fav(program_id)
        ).pack(side="left", padx=3)

        tk.Button(
            btn_frame,
            text="Puan Ver",
            command=lambda: self.rate(program_id)
        ).pack(side="left", padx=3)

    # =================================================
    # SEARCH
    # =================================================
    def search(self):

        text = self.search_entry.get().strip()
        selected_type = self.type_filter.get()

        query = "SELECT * FROM Program WHERE 1=1"
        values = []

        if text:

            query += " AND program_adi LIKE %s"
            values.append(f"%{text}%")

        if selected_type != "Tümü":

            query += " AND program_tipi = %s"
            values.append(selected_type)

        query += " ORDER BY ortalama_puan DESC"

        cursor.execute(query, tuple(values))

        programs = cursor.fetchall()

        self.load_programs(programs)

    # =================================================
    # TOP RATED
    # =================================================
    def show_top_rated(self):

        cursor.execute("""
            SELECT *
            FROM Program
            WHERE ortalama_puan > 0
            ORDER BY ortalama_puan DESC
            LIMIT 10
        """)

        programs = cursor.fetchall()

        self.load_programs(programs)

    # =================================================
    # MOST WATCHED
    # =================================================
    def show_most_watched(self):

        cursor.execute("""
            SELECT *
            FROM Program
            ORDER BY izlenme_sayisi DESC
            LIMIT 10
        """)

        programs = cursor.fetchall()

        self.load_programs(programs)

    # =================================================
    # WATCH
    # =================================================
    def watch(self, program_id):

        cursor.execute("""
            SELECT *
            FROM Program
            WHERE program_id = %s
        """, (program_id,))

        program = cursor.fetchone()

        if not program:

            messagebox.showerror(
                "Hata",
                "Program bulunamadı"
            )

            return

        # İzlenme artır
        cursor.execute("""
            UPDATE Program
            SET izlenme_sayisi = izlenme_sayisi + 1
            WHERE program_id = %s
        """, (program_id,))

        db.commit()

        WatchScreen(self.user_id, program)

    # =================================================
    # FAVORITE
    # =================================================
    def add_fav(self, program_id):

        cursor.execute("""
            SELECT *
            FROM Favori
            WHERE kullanici_id = %s
            AND program_id = %s
        """, (self.user_id, program_id))

        if cursor.fetchone():

            messagebox.showwarning(
                "Uyarı",
                "Bu program zaten favorilerde"
            )

            return

        cursor.execute("""
            INSERT INTO Favori (
                kullanici_id,
                program_id
            )
            VALUES (%s, %s)
        """, (self.user_id, program_id))

        db.commit()

        messagebox.showinfo(
            "Başarılı",
            "Favorilere eklendi"
        )

    # =================================================
    # RATE
    # =================================================
    def rate(self, program_id):

        rate_window = tk.Toplevel()
        rate_window.title("Puan Ver")
        rate_window.geometry("300x150")

        tk.Label(rate_window, text="1 - 10 arası puan giriniz").pack(pady=10)

        entry = tk.Entry(rate_window)
        entry.pack(pady=5)

        def save_rating():

            try:
                rating = int(entry.get().strip())

                if not (1 <= rating <= 10):
                    messagebox.showerror("Hata", "Puan 1-10 arasında olmalı")
                    return

                # 🔥 TEK SORGULUK ÇÖZÜM (INSERT veya UPDATE otomatik)
                cursor.execute("""
                    INSERT INTO IzlemeLog (kullanici_id, program_id, puan)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE puan = VALUES(puan)
                """, (self.user_id, program_id, rating))

                # ortalama güncelle
                cursor.execute("""
                    SELECT IFNULL(AVG(puan), 0)
                    FROM IzlemeLog
                    WHERE program_id = %s
                """, (program_id,))

                avg = cursor.fetchone()[0]

                cursor.execute("""
                    UPDATE Program
                    SET ortalama_puan = %s
                    WHERE program_id = %s
                """, (avg, program_id))

                db.commit()

                messagebox.showinfo("Başarılı", "Puan kaydedildi")
                rate_window.destroy()
                self.show_top_rated()

            except Exception as e:
                db.rollback()
                messagebox.showerror("Hata", str(e))
                print("HATA:", e)

        tk.Button(rate_window, text="Kaydet", command=save_rating).pack(pady=10)


    # =================================================
    # PROFILE
    # =================================================
    def open_profile(self):

        ProfileScreen(self.user_data)

    # =================================================
    # HISTORY
    # =================================================
    def open_history(self):

        HistoryScreen(self.user_id)

    # =================================================
    # FAVORITES
    # =================================================
    def open_favorites(self):

        FavoritesScreen(self.user_id)

    # =================================================
    # RECOMMENDATION SYSTEM
    # =================================================
    def show_recommendations(self):

        self.clear()

        cursor.execute("""
            SELECT *
            FROM Program
            ORDER BY ortalama_puan DESC,
                     izlenme_sayisi DESC
            LIMIT 10
        """)

        programs = cursor.fetchall()

        print("PROGRAM SAYISI:", len(programs))
        print("PROGRAMS:", programs)

        if not programs:
            tk.Label(
                self.frame,
                text="Öneri yok",
                bg="#f2f2f2",
                font=("Arial", 14)
            ).pack()
            return

        for p in programs:
            print("CREATING CARD")
            self.create_card(p)