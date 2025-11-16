import random

# Kategorilere göre kelimeler
WORDS = {
    "meyve": ["elma", "armut", "muz", "çilek", "portakal", "karpuz"],
    "hayvan": ["kedi", "köpek", "aslan", "fil", "kuş", "kaplan","zebra", "zürafa"],
    "teknoloji": ["bilgisayar", "yazilim", "donanim", "internet", "robot"],
    "Eşya": ["bilgisayar", "masa", "koltuk", "telefon", "defter"]

}

def select_word():
    """Rastgele kategori ve kelime seçer"""
    category = random.choice(list(WORDS.keys()))
    word = random.choice(WORDS[category])
    return category, word

if __name__ == "__main__":
    print(select_word())
