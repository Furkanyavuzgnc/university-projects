"""
MovieGraphPy - Neo4j tabanlı film graf uygulaması

Bu uygulama, Neo4j veritabanına bağlanarak filmler üzerinde arama yapmayı,
seçilen filmin detaylarını görüntülemeyi ve o filme ait graph.json çıktısı
oluşturmayı sağlayan menü tabanlı bir Python programıdır.
"""

from services.search_service import SearchService
from services.detail_service import DetailService
from services.graph_service import GraphService

# 🔐 Neo4j bağlantı bilgileri
URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "123456789"

# Servis sınıflarının oluşturulması
search_service = SearchService(URI, USER, PASSWORD)
detail_service = DetailService(URI, USER, PASSWORD)
graph_service = GraphService(URI, USER, PASSWORD)

# Son seçilen filmi global değişkende tutuyoruz
selected_movie = None


def main_menu():
    """
    Uygulamanın ana menüsünü çalıştırır.

    Kullanıcı bu menü üzerinden:
    1 - Film arayabilir
    2 - Seçilen filmin detaylarını görüntüleyebilir
    3 - Seçili film için graph.json dosyası oluşturabilir
    4 - Programdan çıkış yapabilir
    """
    global selected_movie

    while True:
        print("\n--- MovieGraphPy ---")
        print("1. Film Ara")
        print("2. Film Detayı Göster")
        print("3. Seçili Film için graph.json Oluştur")
        print("4. Çıkış")

        choice = input("Seçiminiz: ")

        # --- 1. FİLM ARAMA ---
        if choice == "1":
            # Kullanıcıdan aranacak film adı alınır
            keyword = input("Aranacak film adı: ")

            # Boş aramayı engelliyoruz
            if not keyword.strip():
                print("❌ Boş arama yapılamaz.")
                continue

            # Servis üzerinden arama yapılır
            results = search_service.search_movies(keyword)

            # Sonuç yoksa kullanıcı bilgilendirilir
            if not results:
                print("❌ Film bulunamadı.")
                continue

            # Bulunan filmler listelenir
            print("\nBulunan Filmler:")
            for i, movie in enumerate(results, start=1):
                print(f"{i}) {movie['title']} ({movie['year']})")

            secim = input("Seçmek için numara girin: ")

            try:
                # Kullanıcı seçimi index'e çevrilir
                index = int(secim) - 1
                selected_movie = results[index]['title']
                print(f"\n✔ Seçilen film: {selected_movie}")
            except:
                # Hatalı seçimde film temizlenir
                selected_movie = None
                print("❌ Geçersiz seçim!")

        # --- 2. FİLM DETAYI ---
        elif choice == "2":
            # Eğer film seçilmediyse uyarı verilir
            if not selected_movie:
                print("❌ Önce film seçmelisiniz (1. menü).")
                continue

            # Seçili filmin detayları alınır
            details = detail_service.get_movie_details(selected_movie)

            if not details:
                print("❌ Film bulunamadı.")
                continue

            # Detaylar ekrana yazdırılır
            print("\n--- Film Detayı ---")
            print("Adı:", details["title"])
            print("Yıl:", details["year"])
            print("Tagline:", details["tagline"])

            print("\nYönetmenler:")
            for d in details["directors"]:
                print("-", d)

            print("\nOyuncular (ilk 5):")
            for a in details["actors"][:5]:
                print("-", a)

        # --- 3. GRAPH.JSON OLUŞTURMA ---
        elif choice == "3":
            # Film seçili değilse işlem yapılmaz
            if not selected_movie:
                print("❌ Önce film seçmelisiniz (1. menü).")
                continue

            # JSON dosyası oluşturulur
            ok = graph_service.create_graph_json(selected_movie)

            if ok:
                print("✔ graph.json oluşturuldu: exports/graph.json")
            else:
                print("❌ Graph oluşturulamadı.")

        # --- 4. ÇIKIŞ ---
        elif choice == "4":
            print("Programdan çıkılıyor...")
            break

        else:
            # Menü dışı girişlere karşı kontrol
            print("❌ Geçersiz seçim!")


# Program ana dosya olarak çalıştırıldığında menü başlatılır
if __name__ == "__main__":
    main_menu()
