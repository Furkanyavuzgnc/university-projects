import tkinter as tk
from tkinter import messagebox
from database.db import cursor, db


class AdminScreen:

    def __init__(self):

        self.window = tk.Toplevel()
        self.window.title("Yönetici Paneli")
        self.window.geometry("950x650")

        tk.Label(
            self.window,
            text="ADMIN PANEL",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        # ---------------- BUTTONS ----------------
        tk.Button(self.window, text="Yeni İçerik Ekle", command=self.add_content).pack(pady=5)
        tk.Button(self.window, text="İçerik Sil", command=self.delete_content).pack(pady=5)
        tk.Button(self.window, text="İçerik Güncelle", command=self.update_content).pack(pady=5)

        tk.Button(self.window, text="Yeni Tür Ekle", command=self.add_genre).pack(pady=5)

        tk.Button(self.window, text="Kullanıcıları Listele", command=self.list_users).pack(pady=5)
        tk.Button(self.window, text="En Çok İzlenenler", command=self.most_watched).pack(pady=5)
        tk.Button(self.window, text="En Yüksek Puanlılar", command=self.top_rated).pack(pady=5)

    # ==============================
    # İÇERİK EKLE (GELİŞTİRİLDİ)
    # ==============================
    def add_content(self):

        win = tk.Toplevel(self.window)
        win.title("İçerik Ekle")

        fields = {}

        labels = [
            "Ad", "Açıklama", "Tip (Film/Dizi)",
            "Tür", "Bölüm Sayısı", "Süre", "Yıl"
        ]

        for i, label in enumerate(labels):

            tk.Label(win, text=label).grid(row=i, column=0)

            e = tk.Entry(win)
            e.grid(row=i, column=1)

            fields[label] = e

        def save():

            cursor.execute("""
                INSERT INTO Program
                (program_adi, aciklama, program_tipi, tur, bolum_sayisi, sure, yil)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (
                fields["Ad"].get(),
                fields["Açıklama"].get(),
                fields["Tip (Film/Dizi)"].get(),
                fields["Tür"].get(),
                fields["Bölüm Sayısı"].get(),
                fields["Süre"].get(),
                fields["Yıl"].get()
            ))

            db.commit()
            messagebox.showinfo("OK", "İçerik eklendi")
            win.destroy()

        tk.Button(win, text="Kaydet", command=save).grid(row=len(labels), column=1)

    # ==============================
    # İÇERİK SİL (GÜVENLİ)
    # ==============================
    def delete_content(self):

        win = tk.Toplevel(self.window)
        win.title("İçerik Sil")

        tk.Label(win, text="Program ID").pack()
        entry = tk.Entry(win)
        entry.pack()

        def delete():

            cursor.execute("""
                DELETE FROM Program
                WHERE program_id=%s
            """, (entry.get(),))

            db.commit()
            messagebox.showinfo("OK", "Silindi")
            win.destroy()

        tk.Button(win, text="Sil", command=delete).pack()

    # ==============================
    # İÇERİK GÜNCELLE (GENİŞLETİLDİ)
    # ==============================
    def update_content(self):

        win = tk.Toplevel(self.window)
        win.title("İçerik Güncelle")

        tk.Label(win, text="ID").grid(row=0, column=0)
        id_entry = tk.Entry(win)
        id_entry.grid(row=0, column=1)

        tk.Label(win, text="Yeni Ad").grid(row=1, column=0)
        name_entry = tk.Entry(win)
        name_entry.grid(row=1, column=1)

        tk.Label(win, text="Yeni Tür").grid(row=2, column=0)
        type_entry = tk.Entry(win)
        type_entry.grid(row=2, column=1)

        def update():

            cursor.execute("""
                UPDATE Program
                SET program_adi=%s,
                    program_tipi=%s
                WHERE program_id=%s
            """, (
                name_entry.get(),
                type_entry.get(),
                id_entry.get()
            ))

            db.commit()
            messagebox.showinfo("OK", "Güncellendi")
            win.destroy()

        tk.Button(win, text="Güncelle", command=update).grid(row=3, column=1)

    # ==============================
    # TÜR EKLE
    # ==============================
    def add_genre(self):

        win = tk.Toplevel(self.window)
        win.title("Tür Ekle")

        entry = tk.Entry(win)
        entry.pack()

        def save():

            cursor.execute("""
                INSERT INTO Tur (tur_adi)
                VALUES (%s)
            """, (entry.get(),))

            db.commit()
            messagebox.showinfo("OK", "Tür eklendi")
            win.destroy()

        tk.Button(win, text="Kaydet", command=save).pack()

    # ==============================
    # KULLANICILAR
    # ==============================
    def list_users(self):

        win = tk.Toplevel(self.window)
        win.title("Kullanıcılar")

        cursor.execute("""
            SELECT kullanici_id, ad, email
            FROM Kullanici
        """)

        for u in cursor.fetchall():
            tk.Label(win, text=f"{u[0]} - {u[1]} - {u[2]}").pack()

    # ==============================
    # EN ÇOK İZLENEN (GELİŞTİRİLDİ)
    # ==============================
    def most_watched(self):

        win = tk.Toplevel(self.window)
        win.title("En Çok İzlenenler")
        win.geometry("400x400")

        try:

            cursor.execute("""
                SELECT Program.program_adi,
                       COUNT(IzlemeLog.log_id) AS izlenme
                FROM IzlemeLog
                INNER JOIN Program
                    ON Program.program_id = IzlemeLog.program_id
                GROUP BY IzlemeLog.program_id
                ORDER BY izlenme DESC
                LIMIT 10
            """)

            rows = cursor.fetchall()

            if not rows:
                tk.Label(
                    win,
                    text="Henüz izleme verisi yok"
                ).pack(pady=20)

                return

            for row in rows:
                tk.Label(
                    win,
                    text=f"{row[0]} - {row[1]} izlenme",
                    font=("Arial", 12)
                ).pack(pady=5)

        except Exception as e:

            messagebox.showerror(
                "Hata",
                str(e)
            )

            print("HATA:", e)

    # ==============================
    # EN YÜKSEK PUANLILAR
    # ==============================
    def top_rated(self):

        win = tk.Toplevel(self.window)
        win.title("En Yüksek Puanlılar")

        cursor.execute("""
            SELECT program_adi, ortalama_puan
            FROM Program
            ORDER BY ortalama_puan DESC
            LIMIT 10
        """)

        for row in cursor.fetchall():
            tk.Label(win, text=f"{row[0]} - {row[1]}").pack()