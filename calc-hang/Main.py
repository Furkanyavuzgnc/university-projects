from Game import HangmanGame

def main():
    print("=== CALC & HANG ===")
    print("Tahmin için harf gir. Ek komutlar: 'hesap', 'ipucu', 'q' (çıkış)")
    print("-" * 40)

    # Oyuncu adı al
    while True:
        player_name = input("Oyuncu adınızı girin: ").strip()
        if player_name:
            break
        print("❌ Lütfen geçerli bir isim girin!")

    game = HangmanGame()

    # Oyun döngüsü
    while not game.is_finished():
        game.display_state()
        action = input("Bir harf tahmin et veya komut gir:  ").lower().strip()

        if action == "q":
            print("Oyundan çıkılıyor...")
            break
        elif action == "hesap":
            game.perform_calculation()
        elif action == "ipucu":
            game.use_hint()
        elif len(action) == 1 and action.isalpha():
            game.guess_letter(action)
        else:
            print("❌ Geçersiz komut! Tek harf veya ek komut girin.")

    print("\nOyun bitti. Toplam skor:", game.score)

    # Skoru kaydet
    game.save_score(player_name)


if __name__ == "__main__":
    main()
