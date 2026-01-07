"""
graph_service.py

Bu dosya, seçilen filme ait graf yapısını (film - oyuncular - yönetmenler
arasındaki ilişkileri) Neo4j veritabanından okuyup JSON formatında dışa
aktaran GraphService sınıfını içerir.

Oluşan JSON dosyası daha sonra graf görselleştirme araçlarında
(network graph, force graph vb.) kullanılabilir.
"""

from neo4j import GraphDatabase
import json
import os


class GraphService:
    """
    Seçilen film için graf verisini oluşturan servis sınıfı.

    Parametreler
    ----------
    uri : str
        Neo4j bağlantı adresi
    user : str
        Kullanıcı adı
    password : str
        Şifre
    """

    def __init__(self, uri, user, password):
        # Neo4j sürücüsü oluşturulur
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """
        Veritabanı bağlantısını kapatır.
        """
        self.driver.close()

    def create_graph_json(self, title):
        """
        Seçilen film için graph.json dosyası oluşturur.

        Bu fonksiyon:
        - Filmi düğüm (node) olarak ekler
        - Film ile ilişkili kişileri (oyuncu / yönetmen) node olarak ekler
        - Aralarındaki ACTED_IN ve DIRECTED ilişkilerini ekler
        - Sonuçları JSON formatında exports/graph.json dosyasına kaydeder

        Parametreler
        ----------
        title : str
            Grafı oluşturulacak filmin adı

        Dönüş
        -----
        bool
            İşlem başarılı ise True, film bulunamazsa False döner.
        """

        # Film, ilişkili kişiler ve ilişkileri getiren Cypher sorgusu
        query = """
        MATCH (m:Movie {title:$title})
        OPTIONAL MATCH (p:Person)-[r]->(m)
        RETURN m, collect(p) AS persons, collect(r) AS relations
        """

        # Veritabanı oturumu açılır ve sorgu çalıştırılır
        with self.driver.session() as session:
            result = session.run(query, title=title).single()

            # Sonuç bulunamazsa işlem başarısız
            if not result:
                return False

            movie = result["m"]
            persons = result["persons"]
            relations = result["relations"]

            nodes = []
            links = []

            # --- Movie düğümü eklenir ---
            nodes.append({
                "id": movie.id,         # benzersiz Neo4j ID
                "label": "Movie",       # düğüm tipi
                "title": movie["title"] # film adı
            })

            # --- Person düğümleri eklenir ---
            for p in persons:
                nodes.append({
                    "id": p.id,
                    "label": "Person",
                    "name": p["name"]
                })

            # --- İlişkiler eklenir ---
            for r in relations:
                links.append({
                    "source": r.start_node.id,  # ilişkiyi başlatan düğüm
                    "target": r.end_node.id,    # hedef düğüm
                    "type": type(r).__name__    # ilişki tipi (ACTED_IN / DIRECTED)
                })

            # JSON formatında saklanacak veri yapısı
            data = {
                "nodes": nodes,
                "links": links
            }

            # exports klasörü yoksa oluştur
            os.makedirs("exports", exist_ok=True)

            # JSON dosyasını yaz
            with open("exports/graph.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            return True
