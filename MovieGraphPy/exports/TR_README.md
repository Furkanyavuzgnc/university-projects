# 🎬 MovieGraphPy — Neo4j Movies Dataset Python Uygulaması

Bu proje, Neo4j veritabanındaki **Movies Dataset** kullanılarak film–oyuncu–yönetmen ilişkilerini sorgulayan ve seçilen film için **graph.json** formatında grafik veri çıktısı oluşturan bir Python konsol uygulamasıdır.

Amaç; graf veritabanı yapısını, Python–Neo4j entegrasyonunu ve ilişkisel film verilerinin grafik modelde temsil edilmesini göstermektir.

---

## 🧠 Kullanılan Teknolojiler

- 🐍 Python  
- 🗄 Neo4j Desktop  
- 🔌 Bolt Protocol  
- 🧾 Cypher Query Language  
- 📦 neo4j Python Driver  

---

## ⚙️ Kurulum Adımları

### 1️⃣ Neo4j Kurulumu

✔ Neo4j Desktop yüklenir  
✔ Yeni bir veritabanı oluşturulur  
✔ Veritabanı çalıştırılır (**Running** olmalı)

Movies dataset eklemek için::play movies


ve komutlar sırasıyla çalıştırılır.

---

### 2️⃣ Python Sanal Ortam (Virtualenv)

Proje klasöründe:python -m venv .venv


Aktif edin ve gerekli paketi kurun:pip install neo4j


---

### 3️⃣ Bağlantı Bilgileri

Uygulamada kullanılan bağlantı ayarları:
bolt://localhost:7687
kullanıcı: neo4j
şifre: ********


---

## ▶️ Uygulamayı Çalıştırma

python main.py


Karşınıza şu menü gelecektir:
    Film Ara
    Film Detayı Göster
    Seçili Film için graph.json Oluştur
    Çıkış


---

## 🔍 Özellikler

### ✔ Film Arama  
Girilen anahtar kelimeye göre film listesi getirir.

### ✔ Film Detayı Göster  
Seçilen film için:

- Film adı  
- Yayın yılı  
- Tagline  
- Yönetmen listesi  
- Oyuncu listesi  

ekrana yazdırılır.

### ✔ graph.json Oluştur  
Seçilen film için şu veriler dışa aktarılır:
    nodes → Film ve kişiler
    links → Aralarındaki ilişkiler


Oluşan dosya konumu:exports/graph.json 
Her oluşturulduğunda **üzerine yazılır.**

---

## 🧠 JSON Yapısı Hakkında

Örnek olarak:

```json
{
  "nodes": [...],
  "links": [...]
}

✔ nodes → graf düğümleri (Film & Person)
✔ links → düğümler arası ilişkiler (ACTED_IN / DIRECTED)

Bu dosya grafik görselleştirme araçlarında kullanılabilir.

📂 Proje Klasör Yapısı
MovieGraphPy
 ├ main.py
 ├ db.py
 ├ services
 │   ├ search_service.py
 │   ├ detail_service.py
 │   ├ graph_service.py
 ├ exports
 │   └ graph.json
 └ README.md

🧾 Kod Yapısı
Uygulama 3 temel servis ile çalışır:
| Dosya               | Görevi                        |
| ------------------- | ----------------------------- |
| `search_service.py` | Film arama işlemleri          |
| `detail_service.py` | Film detay sorgulama          |
| `graph_service.py`  | JSON graph çıktısı üretme     |
| `db.py`             | Veritabanı bağlantı testi     |
| `main.py`           | Menü tabanlı uygulama arayüzü |


🎯 Projenin Kazandırdıkları

✔ Neo4j ile graf veritabanı mantığını öğrenme
✔ Python–Neo4j bağlantısı kurma
✔ Cypher sorgularını kullanma
✔ JSON graph modeli üretme
✔ Menü tabanlı uygulama geliştirme

📌 Notlar

Veritabanı çalışır durumda olmalıdır

Yanlış şifre bağlantı hatasına neden olur

graph.json her çalıştırmada güncellenir (overwrite)

✅ Lisans
Bu proje eğitim amaçlı geliştirilmiştir.