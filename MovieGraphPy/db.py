"""
db.py

Bu dosya, Neo4j veritabanı ile bağlantı kurmak ve bağlantıyı test etmek
için kullanılan Database sınıfını içerir. Python Neo4j Driver (Bolt)
üzerinden veritabanına bağlanılır.
"""

from neo4j import GraphDatabase


class Database:
    """
    Neo4j veritabanı bağlantısını yöneten sınıf.

    Parametreler
    ----------
    uri : str
        Neo4j veritabanının bağlantı adresi (Örn: bolt://localhost:7687)
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
        Açık olan veritabanı bağlantısını kapatır.
        """
        self.driver.close()

    def test_connection(self):
        """
        Neo4j veritabanına bağlantının başarılı olup olmadığını test eder.

        Bağlantı başarılı ise:
            Neo4j bağlantısı başarılı

        şeklinde çıktı verir.

        Herhangi bir hata oluşursa yakalanır ve ekrana yazdırılır.
        """
        try:
            # Neo4j oturumu açılır
            with self.driver.session() as session:

                # Basit bir test sorgusu çalıştırılır
                result = session.run("RETURN 'Neo4j bağlantısı başarılı' AS msg")

                # Sonuç ekrana yazdırılır
                for record in result:
                    print(record["msg"])

        except Exception as e:
            # Hata durumunda kullanıcı bilgilendirilir
            print("Bağlantı hatası:", e)


# Bu dosya doğrudan çalıştırıldığında bağlantı testi yapılır
if __name__ == "__main__":

    # Database sınıfından bir nesne oluşturuluyor
    db = Database(
        "bolt://localhost:7687",
        "neo4j",
        "123456789"
    )

    # Bağlantı testi yapılır
    db.test_connection()

    # Bağlantı kapatılır
    db.close()
