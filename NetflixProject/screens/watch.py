import tkinter as tk
from tkinter import messagebox
from database.db import cursor, db


class WatchScreen:

    def __init__(self, user_id, program):

        self.user_id = user_id
        self.program = program
        self.program_id = program[0]

        self.window = tk.Toplevel()

        self.window.title("İzleme Ekranı")
        self.window.geometry("500x520")

        tk.Label(
            self.window,
            text=program[1],
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        # =================================================
        # PROGRAM BİLGİLERİ
        # =================================================

        tk.Label(
            self.window,
            text=f"Program Tipi: {program[3]}"
        ).pack()

        tk.Label(
            self.window,
            text=f"Toplam Bölüm: {program[5]}"
        ).pack()

        tk.Label(
            self.window,
            text=f"Süre: {program[6]} dk"
        ).pack()

        tk.Label(
            self.window,
            text=f"Ortalama Puan: {program[7]}"
        ).pack()

        tk.Label(
            self.window,
            text=f"İzlenme Sayısı: {program[8]}"
        ).pack(pady=10)

        # =================================================
        # BÖLÜM
        # =================================================

        tk.Label(
            self.window,
            text="Bölüm No"
        ).pack()

        self.episode_entry = tk.Entry(
            self.window,
            width=20
        )

        self.episode_entry.pack()

        # =================================================
        # İZLEME SÜRESİ
        # =================================================

        tk.Label(
            self.window,
            text="İzleme Süresi (dakika)"
        ).pack()

        self.time_entry = tk.Entry(
            self.window,
            width=20
        )

        self.time_entry.pack()

        # =================================================
        # PUAN
        # =================================================

        tk.Label(
            self.window,
            text="Puan (1-10)"
        ).pack()

        self.point_entry = tk.Entry(
            self.window,
            width=20
        )

        self.point_entry.pack()

        # =================================================
        # TAMAMLANDI
        # =================================================

        self.completed_var = tk.IntVar()

        tk.Checkbutton(
            self.window,
            text="İzlemeyi Tamamladım",
            variable=self.completed_var
        ).pack(pady=8)

        # =================================================
        # BUTTON
        # =================================================

        tk.Button(
            self.window,
            text="İzlemeyi Kaydet",
            width=25,
            command=self.save_watch
        ).pack(pady=15)

        # =================================================
        # DEVAM ET SİSTEMİ
        # =================================================

        self.check_resume()

    # =================================================
    # DEVAM ET
    # =================================================

    def check_resume(self):

        cursor.execute("""
            SELECT bolum_no, izleme_suresi, tamamlandi
            FROM IzlemeLog
            WHERE kullanici_id=%s
            AND program_id=%s
            ORDER BY log_id DESC
            LIMIT 1
        """, (self.user_id, self.program_id))

        data = cursor.fetchone()

        if data:

            # Eğer tamamlandıysa
            if data[2] == 1:
                messagebox.showinfo(
                    "Bilgi",
                    "Bu içeriği zaten izlediniz"
                )

                self.window.destroy()
                return

            # Devam et sistemi
            self.episode_entry.insert(0, data[0])
            self.time_entry.insert(0, data[1])

            messagebox.showinfo(
                "Devam Et",
                f"{data[0]}. bölüm {data[1]}. dakikadan devam ediliyor"
            )

    # =================================================
    # SAVE WATCH
    # =================================================

    def save_watch(self):

        try:

            episode = int(
                self.episode_entry.get()
            )

            watch_time = int(
                self.time_entry.get()
            )

            point = int(
                self.point_entry.get()
            )

        except:

            messagebox.showerror(
                "Hata",
                "Sayısal değer giriniz"
            )

            return

        # =================================================
        # PUAN KONTROL
        # =================================================

        # PUAN KONTROL
        if point < 1 or point > 10:
            messagebox.showerror("Hata", "Puan 1-10 arasında olmalı")
            return

        # BÖLÜM KONTROL
        total_episode = self.program[5]

        if episode < 1 or episode > total_episode:
            messagebox.showerror("Hata", f"Bu içerik toplam {total_episode} bölüm içeriyor")
            return

        # SÜRE KONTROL
        total_time = self.program[6]

        if watch_time < 1 or watch_time > total_time:
            messagebox.showerror("Hata", f"İzleme süresi 1 ile {total_time} dakika arasında olmalı")
            return

        completed = self.completed_var.get()

        # =================================================
        # DAHA ÖNCE İZLEMİŞ Mİ?
        # =================================================

        cursor.execute("""
            SELECT log_id
            FROM IzlemeLog
            WHERE kullanici_id=%s
            AND program_id=%s
            ORDER BY log_id DESC
            LIMIT 1
        """, (self.user_id, self.program_id))

        existing = cursor.fetchone()

        # =================================================
        # DAHA ÖNCE TAMAMLANMIŞ MI?
        # =================================================

        cursor.execute("""
            SELECT tamamlandi
            FROM IzlemeLog
            WHERE kullanici_id=%s
            AND program_id=%s
            ORDER BY log_id DESC
            LIMIT 1
        """, (self.user_id, self.program_id))

        completed_check = cursor.fetchone()

        if completed_check and completed_check[0] == 1:
            messagebox.showwarning(
                "Uyarı",
                "Bu içeriği zaten izlediniz"
            )

            return

        # =================================================
        # GÜNCELLE
        # =================================================

        if existing:

            cursor.execute("""
                UPDATE IzlemeLog
                SET bolum_no=%s,
                    izleme_suresi=%s,
                    tamamlandi=%s,
                    puan=%s
                WHERE log_id=%s
            """, (
                episode,
                watch_time,
                completed,
                point,
                existing[0]
            ))

        # =================================================
        # YENİ KAYIT
        # =================================================

        else:

            cursor.execute("""
                INSERT INTO IzlemeLog
                (
                    kullanici_id,
                    program_id,
                    bolum_no,
                    izleme_suresi,
                    tamamlandi,
                    puan
                )
                VALUES (%s,%s,%s,%s,%s,%s)
            """, (
                self.user_id,
                self.program_id,
                episode,
                watch_time,
                completed,
                point
            ))

        # =================================================
        # ORTALAMA PUAN GÜNCELLE
        # =================================================

        cursor.execute("""
            UPDATE Program
            SET ortalama_puan = (
                SELECT IFNULL(AVG(puan),0)
                FROM IzlemeLog
                WHERE program_id=%s
            )
            WHERE program_id=%s
        """, (
            self.program_id,
            self.program_id
        ))

        # =================================================
        # İZLENME SAYISI
        # =================================================

        cursor.execute("""
            UPDATE Program
            SET izlenme_sayisi =
            izlenme_sayisi + 1
            WHERE program_id=%s
        """, (self.program_id,))

        db.commit()

        messagebox.showinfo(
            "Başarılı",
            "İzleme bilgisi kaydedildi"
        )

        self.window.destroy()