import tkinter as tk
from database.db import cursor


class HistoryScreen:

    def __init__(self, user_id):

        self.user_id = user_id

        self.window = tk.Toplevel()
        self.window.title("İzleme Geçmişi")
        self.window.geometry("850x650")

        tk.Label(
            self.window,
            text="İzleme Geçmişi",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        # ---------------- FRAME ----------------
        self.frame = tk.Frame(self.window)
        self.frame.pack(fill="both", expand=True)

        self.load_history()

    # ---------------- LOAD HISTORY ----------------
    def load_history(self):

        for w in self.frame.winfo_children():
            w.destroy()

        query = """
        SELECT 
            Program.program_adi,
            IzlemeLog.izleme_tarihi,
            IzlemeLog.bolum_no,
            IzlemeLog.izleme_suresi,
            IzlemeLog.puan,
            IzlemeLog.tamamlandi
        FROM IzlemeLog
        INNER JOIN Program
            ON IzlemeLog.program_id = Program.program_id
        WHERE IzlemeLog.kullanici_id=%s
        ORDER BY IzlemeLog.izleme_tarihi DESC
        """

        cursor.execute(query, (self.user_id,))
        histories = cursor.fetchall()

        # ---------------- EMPTY STATE ----------------
        if not histories:

            tk.Label(
                self.frame,
                text="Henüz izleme geçmişi yok",
                font=("Arial", 14)
            ).pack(pady=30)

            return

        # ---------------- CARDS ----------------
        for h in histories:

            program_name = h[0]
            date = h[1]
            episode = h[2]
            watch_time = h[3]
            rating = h[4]
            completed = "Evet" if h[5] else "Hayır"

            card = tk.Frame(
                self.frame,
                bd=2,
                relief="solid",
                padx=10,
                pady=10
            )

            card.pack(fill="x", padx=20, pady=8)

            tk.Label(
                card,
                text=program_name,
                font=("Arial", 14, "bold")
            ).pack(anchor="w")

            tk.Label(card, text=f"Tarih: {date}").pack(anchor="w")
            tk.Label(card, text=f"Bölüm: {episode}").pack(anchor="w")
            tk.Label(card, text=f"İzleme Süresi: {watch_time} dk").pack(anchor="w")
            tk.Label(card, text=f"Puan: {rating}").pack(anchor="w")
            tk.Label(card, text=f"Tamamlandı: {completed}").pack(anchor="w")