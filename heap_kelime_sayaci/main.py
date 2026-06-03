import heapq
import re
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def agac_ciz_grafik(heap):
    n = len(heap)
    if n == 0:
        return

    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_title("Heap Ağaç Görselleştirme", fontsize=14, fontweight="bold")

    pos = {}

    for i in range(n):
        level = i.bit_length() - 1
        level_start = 2 ** level - 1
        pos_in_level = i - level_start
        total_in_level = 2 ** level

        x = (pos_in_level + 0.5) / total_in_level
        y = -level
        pos[i] = (x, y)

    # Bağlantılar
    for i in range(n):
        sol = 2 * i + 1
        sag = 2 * i + 2
        if sol < n:
            ax.plot([pos[i][0], pos[sol][0]],
                    [pos[i][1], pos[sol][1]], "k-", zorder=1)
        if sag < n:
            ax.plot([pos[i][0], pos[sag][0]],
                    [pos[i][1], pos[sag][1]], "k-", zorder=1)

    # Düğümler: (-adet, kelime) formatı
    for i, (neg_adet, kelime) in enumerate(heap):
        adet = -neg_adet
        x, y = pos[i]

        sol = 2 * i + 1
        sag = 2 * i + 2

        if i == 0:
            renk = "#e74c3c"        # Kök → kırmızı
        elif sol >= n and sag >= n:
            renk = "#2ecc71"        # Yaprak → yeşil
        else:
            renk = "#3498db"        # İç düğüm → mavi

        ax.scatter(x, y, s=2200, color=renk, zorder=2,
                   edgecolors="black", linewidths=1.2)
        ax.text(x, y, f"{kelime}\n({adet})",
                ha="center", va="center", fontsize=8,
                fontweight="bold", zorder=3)

    legend_elements = [
        mpatches.Patch(color="#e74c3c", label="Kök"),
        mpatches.Patch(color="#3498db", label="İç Düğüm"),
        mpatches.Patch(color="#2ecc71", label="Yaprak"),
    ]
    ax.legend(handles=legend_elements, loc="upper right", fontsize=10)

    ax.axis("off")
    plt.tight_layout()
    plt.show()


def kelime_say(text):
    kelime_dict = {}
    kelimeler = re.findall(r'\b\w+\b', text.lower())
    for kelime in kelimeler:
        kelime_dict[kelime] = kelime_dict.get(kelime, 0) + 1
    return kelime_dict


# Ana kriter: en yüksek frekans önce (-adet), eşitlikte alfabetik (kelime)
def heap_olustur(kelime_dict):
    heap = []
    for kelime, adet in kelime_dict.items():
        heapq.heappush(heap, (-adet, kelime))
    return heap


def heap_yazdir(heap):
    print("\nKELİME SAYILARI (Frekans ↓ + Alfabetik Sırası):\n")
    for neg_adet, kelime in sorted(heap):
        print(f"  {kelime:20s} -> {-neg_adet}")


def agac_ciz(heap, index=0, prefix="", is_left=True):
    n = len(heap)
    if index >= n:
        return

    neg_adet, kelime = heap[index]
    adet = -neg_adet

    if index == 0:
        print(f"[KÖK] {kelime} ({adet})")
        yeni_prefix = ""
    else:
        baglanti = "├── " if is_left else "└── "
        print(prefix + baglanti + f"{kelime} ({adet})")
        yeni_prefix = prefix + ("│   " if is_left else "    ")

    sol = 2 * index + 1
    sag = 2 * index + 2

    if sol < n and sag < n:
        agac_ciz(heap, sol, yeni_prefix, is_left=True)
        agac_ciz(heap, sag, yeni_prefix, is_left=False)
    elif sol < n:
        agac_ciz(heap, sol, yeni_prefix, is_left=False)
    elif sag < n:
        agac_ciz(heap, sag, yeni_prefix, is_left=False)


def main():
    dosya_yolu = r"C:\Users\Furkan\Desktop\proje3txtbelgesi.txt"

    try:
        with open(dosya_yolu, "r", encoding="utf-8") as dosya:
            text = dosya.read()

        kelime_dict = kelime_say(text)
        heap = heap_olustur(kelime_dict)

        heap_yazdir(heap)

        print("\nHEAP AĞAÇ GÖRÜNÜMÜ:\n")
        agac_ciz(heap)

        agac_ciz_grafik(heap)

    except FileNotFoundError:
        print("Hata: Dosya bulunamadı →", dosya_yolu)
    except Exception as e:
        print("Hata:", e)


main()