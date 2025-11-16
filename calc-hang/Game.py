import random
import json
import os
from Words import select_word
from Ascii_art import HANGMAN_PICS
from Calc import calc_operation, check_result

class HangmanGame:
    def __init__(self):
        self.category, self.secret_word = select_word()
        self.revealed = ["_"] * len(self.secret_word)
        self.used_letters = set()
        self.remaining_errors = 6
        self.score = 0
        self.bonus_points = 0

        # Her işlem 1 kez kullanılabilir
        self.ops_used = {
            "toplama": False,
            "çıkarma": False,
            "çarpma": False,
            "bölme": False
        }

    # --- Oyun ekranı ---
    def display_state(self):
        print(HANGMAN_PICS[6 - self.remaining_errors])
        print("Kelime:", " ".join(self.revealed))
        print(f"Kalan hata hakkı: {self.remaining_errors}")
        print(f"Kullanılan harfler: {', '.join(sorted(self.used_letters)) if self.used_letters else '—'}")
        print(f"Skor: {self.score} | Bonus: {self.bonus_points}")

        unused_ops = [op for op, used in self.ops_used.items() if not used]
        print("Ek komutlar: 'hesap', 'ipucu', 'q' (çıkış)")
        print(f"Kalan işlemler: {', '.join(unused_ops) if unused_ops else '—'}")
        print("-" * 35)

    # --- Harf tahmini ---
    def guess_letter(self, letter):
        letter = letter.lower()

        if not letter.isalpha() or len(letter) != 1:
            print("❌ Lütfen sadece bir harf gir!")
            return

        if letter in self.used_letters:
            print("⚠️ Bu harfi zaten denedin.")
            return

        self.used_letters.add(letter)

        if letter in self.secret_word:
            print("✅ Doğru tahmin!")
            self.score += 10  # +10 PUAN
            for i, ch in enumerate(self.secret_word):
                if ch == letter:
                    self.revealed[i] = letter
        else:
            print("❌ Yanlış tahmin.")
            self.score -= 5      # -5 PUAN
            self.remaining_errors -= 1  # HATA +1

    # --- Rastgele harf açma (bonus) ---
    def reveal_random_letter(self):
        indices = [i for i, ch in enumerate(self.revealed) if ch == "_"]

        if not indices:
            print("Tüm harfler zaten açık!")
            return

        i = random.choice(indices)
        letter = self.secret_word[i]
        self.revealed[i] = letter
        print(f"🎁 Bonus! '{letter}' harfi açıldı.")

    # --- Hesap Makinesi ---
    def perform_calculation(self):
        print("\n🧮 HESAP MAKİNESİ MODU 🧮")
        print("Kullanabileceğin işlemler:")
        for op, used in self.ops_used.items():
            status = "❌ kullanıldı" if used else "✅ kullanılabilir"
            print(f" - {op.capitalize()} ({status})")

        op = input("İşlem seç (toplama/çıkarma/çarpma/bölme veya 'iptal'): ").lower()

        if op == "iptal":
            print("İşlem iptal edildi.")
            return

        if op not in self.ops_used:
            print("❌ Geçersiz işlem!")
            return

        if self.ops_used[op]:
            print("❌ Bu işlemi zaten kullandın!")
            return

        # --- Kullanıcıdan iki sayı al ---
        try:
            a = float(input("Birinci sayıyı gir: "))
            b = float(input("İkinci sayıyı gir: "))
        except ValueError:
            print("❌ Hatalı giriş! Sayı girmen gerekiyor.")
            return

        # --- Bölme işleminde bölen 0 ise hata artır ---
        if op == "bölme" and b == 0:
            print("❌ HATA: Bölen 0 olamaz!")
            self.remaining_errors -= 1  # HATA +1
            self.score -= 10             # Yanlış işlem → −10
            print(f"Kalan hata hakkın: {self.remaining_errors}")
            return

        # --- Beklenen sonucu hesapla ---
        try:
            expected = calc_operation(op, a, b)
        except Exception as e:
            print("⚠️ Hesap hatası:", e)
            self.remaining_errors -= 1
            self.score -= 10  # Yanlış işlem puanı
            return

        print(f"Soru: {a} {op} {b} = ?")

        try:
            user_result = float(input("Cevabın: "))
        except ValueError:
            print("❌ Geçersiz sayı!")
            return

        # --- Sonuç kontrolü ---
        if check_result(expected, user_result):
            print("✅ Doğru!")
            self.score += 15  # +15 PUAN
            self.bonus_points += 1  # +1 BONUS
            self.reveal_random_letter()  # RASTGELE HARF AÇILIR
        else:
            print(f"❌ Yanlış! Doğru cevap: {round(expected, 2)}")
            self.score -= 10      # -10 PUAN
            self.remaining_errors -= 1  # HATA +1

        self.ops_used[op] = True

    # --- İpucu ---
    def use_hint(self):
        if self.bonus_points >= 1:
            self.bonus_points -= 1  # Bonus gider
            print(f"💡 İpucu: Bu kelimenin kategorisi -> '{self.category.upper()}'")
        else:
            print("❌ Yeterli bonus puanın yok!")

    # --- Bitme kontrolü ---
    def is_finished(self):
        if "_" not in self.revealed:
            print("\n🎉 Tebrikler! Kelimeyi buldun!")
            print(f"Kelime: {self.secret_word}")
            print(f"Kategori: {self.category.upper()}")
            self.score += 50  # Kazanma bonusu
            print(f"+50 kazanma bonusu! Toplam skor: {self.score}")
            return True

        if self.remaining_errors <= 0:
            print("\n💀 Kaybettin!")
            print(f"Kelime: {self.secret_word}")
            print(f"Kategori: {self.category.upper()}")
            self.score -= 20  # Kaybetme cezası
            print(f"-20 kaybetme cezası! Toplam skor: {self.score}")
            return True

        return False

    # --- Skor kaydetme ---
    def save_score(self, player_name):
        try:
            # Eğer scores.json yoksa oluştur
            if not os.path.exists("scores.json"):
                with open("scores.json", "w") as f:
                    json.dump([], f)

            # Mevcut skorları oku
            with open("scores.json", "r") as f:
                scores = json.load(f)

            # Yeni skoru ekle
            scores.append({"name": player_name, "score": self.score})

            # Skorları yüksekten düşüğe sırala ve en iyi 5'i al
            scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:5]

            # Dosyaya kaydet
            with open("scores.json", "w") as f:
                json.dump(scores, f, indent=4)

            # En iyi 5 skoru göster
            print("\n--- En İyi 5 Skor ---")
            for idx, s in enumerate(scores, 1):
                print(f"{idx}. {s['name']} - {s['score']} puan")

        except Exception as e:
            print("⚠️ Skor kaydedilirken hata oluştu:", e)
