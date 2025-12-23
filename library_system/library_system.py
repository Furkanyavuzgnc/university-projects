class Book:
    def __init__(self, name, author, year):
        self.name = name
        self.author = author
        self.year = year

    def __str__(self):
        return f"Kitap Adı: {self.name} | Yazar: {self.author} | Yayın Yılı: {self.year}"

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        return "Kitap başarıyla eklendi."

    def list_books(self):
        return self.books

    def remove_book(self, book_name):
        for book in self.books:
            if book.name.lower() == book_name.lower():
                self.books.remove(book)
                return "Kitap başarıyla silindi."
        return "Kitap bulunamadı."

    def search_by_name(self, book_name):
        return [book for book in self.books if book_name.lower() in book.name.lower()]

    def search_by_author(self, author_name):
        return [book for book in self.books if author_name.lower() in book.author.lower()]


def run_library_system():
    library = Library()

    while True:
        print("\n--- KÜTÜPHANE YÖNETİM SİSTEMİ ---")
        print("1- Kitap Ekle")
        print("2- Kitap Sil")
        print("3- İsme Göre Kitap Ara")
        print("4- Yazara Göre Kitap Ara")
        print("5- Tüm Kitapları Listele")
        print("6- Çıkış")

        choice = input("Seçiminizi girin (1-6): ")

        if choice == "1":
            name = input("Kitap adı: ")
            author = input("Yazar adı: ")
            year = input("Yayın yılı: ")

            book = Book(name, author, year)
            library.add_book(book)

        elif choice == "2":
            name = input("Silinecek kitap adı: ")
            library.remove_book(name)

        elif choice == "3":
            name = input("Aranacak kitap adı: ")
            library.search_by_name(name)

        elif choice == "4":
            author = input("Aranacak yazar adı: ")
            library.search_by_author(author)

        elif choice == "5":
            library.list_books()

        elif choice == "6":
            print("Programdan çıkılıyor...")
            break

        else:
            print("Geçersiz seçim! Lütfen 1-6 arasında bir değer girin.")

    result = library.add_book(book)
    print(result)
