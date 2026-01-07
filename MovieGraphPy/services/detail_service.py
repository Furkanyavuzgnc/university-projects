"""
detail_service.py

Bu dosya, Neo4j veritabanında seçili bir filme ait detay bilgileri
getirmek için kullanılan DetailService sınıfını içerir. Filmle ilişkili
oyuncular ve yönetmen bilgileri de aynı sorgu ile elde edilir.
"""

from neo4j import GraphDatabase


class DetailService:
    """
    Seçilen filme ait detay bilgileri Neo4j veritabanından getiren servis sınıfı.

    Parametreler
    ----------
    uri : str
        Neo4j veritabanı bağlantı adresi
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

    def get_movie_details(self, title):
        """
        Verilen film adına göre film detaylarını getirir.

        Bu fonksiyon;
        - Filmin adı
        - Yayın yılı
        - Tagline bilgisi
        - Yönetmen listesi
        - Oyuncu listesi

        gibi bilgileri tek bir Cypher sorgusu ile Neo4j'den çeker.

        Parametreler
        ----------
        title : str
            Detayları alınacak filmin adı

        Dönüş
        -----
        neo4j.Record
            Film detaylarını içeren tek bir kayıt döner.
            Alanlar:
                - title
                - year
                - tagline
                - directors (liste)
                - actors (liste)
        """

        # Cypher sorgusu: Film, yönetmen ve oyuncuları getir
        query = """
        MATCH (m:Movie {title:$title})
        OPTIONAL MATCH (m)<-[:DIRECTED]-(d:Person)
        OPTIONAL MATCH (m)<-[:ACTED_IN]-(a:Person)
        RETURN m.title AS title,
               m.released AS year,
               m.tagline AS tagline,
               collect(DISTINCT d.name) AS directors,
               collect(DISTINCT a.name) AS actors
        """

        # Oturum açılarak sorgu çalıştırılır
        with self.driver.session() as session:
            result = session.run(query, title=title)

            # Tek satır döndüğü için single() kullanıyoruz
            return result.single()
