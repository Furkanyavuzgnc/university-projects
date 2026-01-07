"""
search_service.py

Bu dosya, Neo4j veritabanında film arama işlemlerini gerçekleştiren
SearchService sınıfını içerir. Kullanıcıdan alınan anahtar kelimeye göre
film başlıkları üzerinde arama yapılır.
"""

from neo4j import GraphDatabase


class SearchService:
    """
    Neo4j veritabanında film arama işlemlerini yöneten servis sınıfı.

    Parametreler
    ----------
    uri : str
        Neo4j veritabanı bağlantı adresi (örn: bolt://localhost:7687)
    user : str
        Veritabanı kullanıcı adı
    password : str
        Veritabanı şifresi
    """

    def __init__(self, uri, user, password):
        # Veritabanı sürücüsü oluşturulur
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """
        Veritabanı bağlantısını kapatır.
        """
        self.driver.close()

    def search_movies(self, keyword):
        """
        Verilen anahtar kelimeyi içeren film başlıklarını arar.

        Arama işlemi, film başlıkları küçük harfe dönüştürülerek yapılır.
        Böylece büyük/küçük harf duyarlılığı ortadan kaldırılır.

        Parametreler
        ----------
        keyword : str
            Kullanıcı tarafından girilen arama kelimesi

        Dönüş
        -----
        list[neo4j.Record]
            Bulunan filmlerin başlık ve yayın yılı bilgilerini içeren liste
            (ör. title, year)
        """

        # Cypher sorgusu: başlıkta kelime geçen filmleri bul
        query = """
        MATCH (m:Movie)
        WHERE toLower(m.title) CONTAINS toLower($keyword)
        RETURN m.title AS title, m.released AS year
        ORDER BY m.released
        """

        # Veritabanı oturumu açılır ve sorgu çalıştırılır
        with self.driver.session() as session:
            result = session.run(query, keyword=keyword)

            # Sonuç listeye dönüştürülüp geri gönderilir
            return list(result)
