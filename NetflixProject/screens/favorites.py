import tkinter as tk
from tkinter import messagebox
from database.db import cursor, db


class FavoritesScreen:

    def __init__(self, user_id):

        self.user_id = user_id

        self.window = tk.Toplevel()
        self.window.title("Favoriler")
        self.window.geometry("750x550")

        tk.Label(
            self.window,
            text="Favorilerim",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        # ---------------- FILTER ----------------
        filter_frame = tk.Frame(self.window)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Tür:").grid(row=0, column=0)

        self.type_filter = tk.StringVar()
        self.type_filter.set("Tümü")

        tk.OptionMenu(
            filter_frame,
            self.type_filter,
            "Tümü",
            "Film",
            "Dizi"
        ).grid(row=0, column=1)

        tk.Button(
            filter_frame,
            text="Filtrele",
            command=self.load_favorites
        ).grid(row=0, column=2, padx=10)

        # ---------------- FRAME ----------------
        self.favorite_frame = tk.Frame(self.window)
        self.favorite_frame.pack(fill="both", expand=True)

        self.load_favorites()

    # ---------------- LOAD FAVORITES ----------------
    def load_favorites(self):

        for widget in self.favorite_frame.winfo_children():
            widget.destroy()

        selected_type = self.type_filter.get()

        query = """
        SELECT Favori.favori_id,
               Program.program_adi,
               Program.program_tipi
        FROM Favori
        INNER JOIN Program
        ON Favori.program_id = Program.program_id
        WHERE Favori.kullanici_id=%s
        """

        values = [self.user_id]

        # ---------------- TYPE FILTER ----------------
        if selected_type != "Tümü":
            query += " AND Program.program_tipi=%s"
            values.append(selected_type)

        cursor.execute(query, tuple(values))
        favorites = cursor.fetchall()

        # ---------------- EMPTY STATE ----------------
        if not favorites:

            tk.Label(
                self.favorite_frame,
                text="Favori içerik bulunamadı",
                font=("Arial", 14)
            ).pack(pady=30)

            return

        # ---------------- CARDS ----------------
        for fav in favorites:

            fav_id = fav[0]
            name = fav[1]
            type_ = fav[2]

            card = tk.Frame(
                self.favorite_frame,
                bd=2,
                relief="solid",
                padx=10,
                pady=10
            )

            card.pack(fill="x", padx=20, pady=8)

            tk.Label(
                card,
                text=name,
                font=("Arial", 14, "bold")
            ).pack(anchor="w")

            tk.Label(
                card,
                text=f"Tür: {type_}"
            ).pack(anchor="w")

            tk.Button(
                card,
                text="Favoriden Çıkar",
                command=lambda fid=fav_id: self.remove_favorite(fid)
            ).pack(anchor="e", pady=5)

    # ---------------- REMOVE FAVORITE ----------------
    def remove_favorite(self, favorite_id):

        cursor.execute("""
            DELETE FROM Favori
            WHERE favori_id=%s
        """, (favorite_id,))

        db.commit()

        messagebox.showinfo("OK", "Favoriden çıkarıldı")

        self.load_favorites()