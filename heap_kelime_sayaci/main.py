import heapq
import re
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def agac_ciz_grafik(heap):
    n = len(heap)
    if n == 0:
        return

    pos = {}
    current_x = [0]  # nonlocal yerine liste kullan (Python 2 uyumu da sağlar)

    def traverse(i, level):
        if i >= n:
            return
        traverse(2 * i + 1, level + 1)
        pos[i] = (current_x[0], -level)
        current_x[0] += 1
        traverse(2 * i + 2, level + 1)

    traverse(0, 0)

    max_level = max(lv for _, lv in pos.values()) if pos else 0

    # Düğüm başına 1.4 birim genişlik, minimum 15
    fig_width  = max(15, n * 1.4)
    # Seviye başına 2.5 birim yükseklik, minimum 8
    fig_height = max(8, (max_level + 1) * 2.5)

    # matplotlib maksimum figür boyutu sınırı (inç cinsinden)
    MAX_DIM = 300
    scale = min(1.0, MAX_DIM / max(fig_width, fig_height))
    fig_width  *= scale
    fig_height *= scale

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.set_title(
        f"Heap Ağaç Görselleştirme  (Toplam {n} düğüm)",
        fontsize=14, fontweight="bold", pad=15
    )

    # ── Bağlantılar ──────────────────────────────────────────────
    for i in range(n):
        for child in (2 * i + 1, 2 * i + 2):
            if child < n:
                ax.plot(
                    [pos[i][0], pos[child][0]],
                    [pos[i][1], pos[child][1]],
                    "k-", zorder=1, alpha=0.25, linewidth=0.8
                )

    # ── Düğüm & yazı boyutu: düğüm sayısına göre otomatik ────────
    #   Her düğüme ayrılan "slot" genişliği scale ile orantılı
    slot_w = fig_width / n          # inç / düğüm
    node_size  = max(80,  int(slot_w * 550))
    font_size  = max(4.5, slot_w * 7.5)

    # ── Düğümleri çiz ────────────────────────────────────────────
    for i, (neg_adet, kelime) in enumerate(heap):
        adet = -neg_adet
        x, y = pos[i]

        sol, sag = 2 * i + 1, 2 * i + 2
        if i == 0:
            renk = "#e74c3c"            # Kök
        elif sol >= n and sag >= n:
            renk = "#2ecc71"            # Yaprak
        else:
            renk = "#3498db"            # İç düğüm

        fs = font_size * (0.85 if len(kelime) > 8 else 1.0)

        ax.scatter(x, y, s=node_size, color=renk, zorder=2,
                   edgecolors="black", linewidths=0.8)
        ax.text(x, y, f"{kelime}\n({adet})",
                ha="center", va="center",
                fontsize=fs, fontweight="bold", zorder=3)

    # ── Açıklama kutusu ──────────────────────────────────────────
    ax.legend(
        handles=[
            mpatches.Patch(color="#e74c3c", label="Kök"),
            mpatches.Patch(color="#3498db", label="İç Düğüm"),
            mpatches.Patch(color="#2ecc71", label="Yaprak"),
        ],
        loc="upper right", fontsize=9
    )

    ax.axis("off")
    plt.tight_layout()
    plt.savefig("heap_agac.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("✓ heap_agac.png olarak kaydedildi.")


# ── Geri kalan fonksiyonlar değişmedi ────────────────────────────

def kelime_say(text):
    kelime_dict = {}
    for kelime in re.findall(r'\b\w+\b', text.lower()):
        kelime_dict[kelime] = kelime_dict.get(kelime, 0) + 1
    return kelime_dict

def heap_olustur(kelime_dict):
    heap = []
    for kelime, adet in kelime_dict.items():
        heapq.heappush(heap, (-adet, kelime))
    return heap

def heap_yazdir(heap):
    print("\nKELİME SAYILARI (Frekans ↓ + Alfabetik):\n")
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
    sol, sag = 2 * index + 1, 2 * index + 2
    if sol < n and sag < n:
        agac_ciz(heap, sol, yeni_prefix, True)
        agac_ciz(heap, sag, yeni_prefix, False)
    elif sol < n:
        agac_ciz(heap, sol, yeni_prefix, False)
    elif sag < n:
        agac_ciz(heap, sag, yeni_prefix, False)

def main():
    dosya_yolu = r"C:\Users\Furkan\Desktop\proje3txtbelgesi.txt"
    try:
        with open(dosya_yolu, "r", encoding="utf-8") as f:
            text = f.read()
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