import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

matplotlib.use('Agg')
matplotlib.rcParams['font.size'] = 11

# CSV dosyasini oku
csv_path = os.path.join(os.path.dirname(__file__), 'pid_verileri.csv')
df = pd.read_csv(csv_path, sep=';', decimal='.')

# Cikis klasoru
out_dir = os.path.join(os.path.dirname(__file__), 'rapor_grafikleri')
os.makedirs(out_dir, exist_ok=True)

t = df['Zaman(s)']
e = df['Hata_e(t)']
u = df['Cikis_u(t)']
v = df['Hiz(m/s)']

# ========================================================
# GRAFIK 1: Takip Hatasi e(t)
# ========================================================
fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(t, e, color='#2196F3', linewidth=0.6, alpha=0.9)
ax.axhline(y=0, color='#F44336', linewidth=1.5, linestyle='--', label='Referans (e=0)')
ax.fill_between(t, e, 0, alpha=0.15, color='#2196F3')
ax.set_xlabel('Zaman (s)')
ax.set_ylabel('Takip Hatasi e(t) [derece]')
ax.set_title('PID Kontrolcu - Takip Hatasi e(t)', fontweight='bold')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)
ax.set_xlim(t.min(), t.max())
plt.tight_layout()
plt.savefig(os.path.join(out_dir, '1_takip_hatasi_et.png'), dpi=200)
plt.close()
print("Grafik 1: Takip Hatasi e(t) kaydedildi.")

# ========================================================
# GRAFIK 2: Kontrolcu Cikisi u(t)
# ========================================================
fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(t, u, color='#FF9800', linewidth=0.6, alpha=0.9)
ax.axhline(y=0, color='gray', linewidth=1, linestyle='--')
ax.fill_between(t, u, 0, alpha=0.15, color='#FF9800')
ax.set_xlabel('Zaman (s)')
ax.set_ylabel('Kontrolcu Cikisi u(t)')
ax.set_title('PID Kontrolcu - Kontrol Sinyali u(t)', fontweight='bold')
ax.grid(True, alpha=0.3)
ax.set_xlim(t.min(), t.max())
plt.tight_layout()
plt.savefig(os.path.join(out_dir, '2_kontrolcu_cikisi_ut.png'), dpi=200)
plt.close()
print("Grafik 2: Kontrolcu Cikisi u(t) kaydedildi.")

# ========================================================
# GRAFIK 3: e(t) ve u(t) Birlikte
# ========================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

ax1.plot(t, e, color='#2196F3', linewidth=0.6)
ax1.axhline(y=0, color='#F44336', linewidth=1.5, linestyle='--', label='Referans')
ax1.fill_between(t, e, 0, alpha=0.12, color='#2196F3')
ax1.set_ylabel('e(t) [derece]')
ax1.set_title('Takip Hatasi e(t) ve Kontrolcu Cikisi u(t) - Karsilastirmali', fontweight='bold')
ax1.legend(loc='upper right')
ax1.grid(True, alpha=0.3)

ax2.plot(t, u, color='#FF9800', linewidth=0.6)
ax2.axhline(y=0, color='gray', linewidth=1, linestyle='--')
ax2.fill_between(t, u, 0, alpha=0.12, color='#FF9800')
ax2.set_xlabel('Zaman (s)')
ax2.set_ylabel('u(t)')
ax2.grid(True, alpha=0.3)

ax1.set_xlim(t.min(), t.max())
plt.tight_layout()
plt.savefig(os.path.join(out_dir, '3_et_ut_karsilastirma.png'), dpi=200)
plt.close()
print("Grafik 3: e(t) ve u(t) karsilastirmasi kaydedildi.")

# ========================================================
# GRAFIK 4: Arac Hizi
# ========================================================
fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(t, v, color='#4CAF50', linewidth=0.8)
ax.set_xlabel('Zaman (s)')
ax.set_ylabel('Hiz (m/s)')
ax.set_title('Arac Hizi - Zaman Grafigi', fontweight='bold')
ax.grid(True, alpha=0.3)
ax.set_xlim(t.min(), t.max())
plt.tight_layout()
plt.savefig(os.path.join(out_dir, '4_arac_hizi.png'), dpi=200)
plt.close()
print("Grafik 4: Arac Hizi kaydedildi.")

# ========================================================
# GRAFIK 5: Duz Yol Bolgeleri (Hata Yakin Zoom)
# ========================================================
# Duz yol: hata cok kucuk olan bolgeleri bul
duz_mask = e.abs() < 0.5
duz_bolge_baslangic = None
duz_bolgeler = []
for i in range(len(duz_mask)):
    if duz_mask.iloc[i] and duz_bolge_baslangic is None:
        duz_bolge_baslangic = i
    elif not duz_mask.iloc[i] and duz_bolge_baslangic is not None:
        if i - duz_bolge_baslangic > 100:  # En az 2 saniye
            duz_bolgeler.append((duz_bolge_baslangic, i))
        duz_bolge_baslangic = None

if duz_bolgeler:
    start, end = duz_bolgeler[0]
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(t.iloc[start:end], e.iloc[start:end], color='#2196F3', linewidth=1.0)
    ax.axhline(y=0, color='#F44336', linewidth=1.5, linestyle='--', label='Referans')
    ax.fill_between(t.iloc[start:end], e.iloc[start:end], 0, alpha=0.2, color='#2196F3')
    ax.set_xlabel('Zaman (s)')
    ax.set_ylabel('e(t) [derece]')
    ax.set_title(f'Duz Yol Bolgesi - Takip Hatasi (t={t.iloc[start]:.1f}s - {t.iloc[end]:.1f}s)', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, '5_duz_yol_hatasi.png'), dpi=200)
    plt.close()
    print(f"Grafik 5: Duz Yol Bolgesi ({t.iloc[start]:.1f}s - {t.iloc[end]:.1f}s) kaydedildi.")

# ========================================================
# GRAFIK 6: Viraj Bolgeleri (Hata Buyuk)
# ========================================================
# En buyuk hata bolgelerini bul (viraj geçişleri)
viraj_mask = e.abs() > 2.0
viraj_bolgeler = []
viraj_start = None
for i in range(len(viraj_mask)):
    if viraj_mask.iloc[i] and viraj_start is None:
        viraj_start = i
    elif not viraj_mask.iloc[i] and viraj_start is not None:
        viraj_bolgeler.append((viraj_start, i))
        viraj_start = None

if viraj_bolgeler:
    # Ilk viraj bolgesi
    start, end = viraj_bolgeler[0]
    # Biraz oncesini ve sonrasini da goster
    start = max(0, start - 100)
    end = min(len(t) - 1, end + 100)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
    ax1.plot(t.iloc[start:end], e.iloc[start:end], color='#F44336', linewidth=1.0)
    ax1.axhline(y=0, color='gray', linewidth=1, linestyle='--')
    ax1.set_ylabel('e(t) [derece]')
    ax1.set_title(f'Viraj Bolgesi - Hata ve Kontrol Sinyali (t={t.iloc[start]:.1f}s - {t.iloc[end]:.1f}s)', fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(t.iloc[start:end], u.iloc[start:end], color='#FF9800', linewidth=1.0)
    ax2.axhline(y=0, color='gray', linewidth=1, linestyle='--')
    ax2.set_xlabel('Zaman (s)')
    ax2.set_ylabel('u(t)')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, '6_viraj_hatasi.png'), dpi=200)
    plt.close()
    print(f"Grafik 6: Viraj Bolgesi ({t.iloc[start]:.1f}s - {t.iloc[end]:.1f}s) kaydedildi.")

# ========================================================
# ISTATISTIKLER
# ========================================================
print("\n" + "="*60)
print("PID SIMULASYON ISTATISTIKLERI")
print("="*60)
print(f"Toplam simulasyon suresi : {t.max():.2f} s")
print(f"Toplam veri noktasi      : {len(t)}")
print(f"Ornekleme frekansi       : {1/(t.iloc[1]-t.iloc[0]):.0f} Hz")
print(f"\n--- Takip Hatasi e(t) ---")
print(f"  Ortalama |e(t)|        : {e.abs().mean():.4f} derece")
print(f"  Maksimum |e(t)|        : {e.abs().max():.4f} derece")
print(f"  Standart Sapma         : {e.std():.4f} derece")
print(f"  RMS Hata               : {np.sqrt((e**2).mean()):.4f} derece")
print(f"\n--- Kontrolcu Cikisi u(t) ---")
print(f"  Ortalama |u(t)|        : {u.abs().mean():.4f}")
print(f"  Maksimum |u(t)|        : {u.abs().max():.4f}")
print(f"  Standart Sapma         : {u.std():.4f}")
print(f"\n--- Arac Hizi ---")
print(f"  Ortalama Hiz           : {v.mean():.2f} m/s ({v.mean()*3.6:.1f} km/h)")
print(f"  Maksimum Hiz           : {v.max():.2f} m/s ({v.max()*3.6:.1f} km/h)")
print(f"  Minimum Hiz            : {v.min():.2f} m/s ({v.min()*3.6:.1f} km/h)")

# Kararlılık: Son 50 veri noktasinda hata
son_bolum = e.iloc[-250:]
print(f"\n--- Kararlilik (Son 5 sn) ---")
print(f"  Ortalama |e(t)|        : {son_bolum.abs().mean():.4f} derece")
print(f"  Standart Sapma         : {son_bolum.std():.4f} derece")

# Yükselme süresi: e(t) ilk kez 0'a yaklaştığı zaman (ilk geçiş)
ilk_hata = e.iloc[0]
if abs(ilk_hata) > 0.01:
    for i in range(1, len(e)):
        if abs(e.iloc[i]) < 0.01:
            print(f"\n--- Gecis Sureleri ---")
            print(f"  Yukselme suresi (ilk sifir gecisi): {t.iloc[i]:.2f} s")
            break

print(f"\n--- PID Parametreleri ---")
print(f"  Kp = 0.99")
print(f"  Ki = 0.10")
print(f"  Kd = 2.04")
print(f"\nGrafikler '{out_dir}' klasorune kaydedildi.")
