# 🏎️ PID Kontrolcü ile Otonom Araç Şerit Takip Simülasyonu

Unity oyun motoru ortamında geliştirilen, PID (Proportional-Integral-Derivative) kontrolcü kullanarak otonom bir aracın şerit takibi yapmasını sağlayan simülasyon projesidir.

![Unity](https://img.shields.io/badge/Unity-6-black?logo=unity)
![C#](https://img.shields.io/badge/C%23-12-blue?logo=dotnet)
![License](https://img.shields.io/badge/License-MIT-green)

## 📋 Proje Özeti

Araç, sahnede yerleştirilen referans noktalarını (waypoint) takip ederek şehir içi yollar, kavşaklar, virajlar ve otoyol rampası gibi farklı yol geometrilerinde otonom olarak ilerlemektedir. PID kontrolcü, araç ile hedef rota arasındaki açısal sapmayı (hata) minimize ederek direksiyon kontrolü sağlamaktadır.

## 🎮 Özellikler

- **Gerçek Zamanlı PID Kontrolü** — Kp, Ki, Kd parametreleri simülasyon sırasında canlı olarak değiştirilebilir
- **Dinamik Araç Parametreleri** — Araç hızı ve kütlesi çalışma anında ayarlanabilir
- **Otomatik Viraj Freni** — Keskin virajlarda araç otomatik olarak yavaşlar
- **Dinamik Lookahead** — Hıza göre bakış mesafesi otomatik ayarlanır
- **Gerçek Zamanlı Grafikler** — e(t) ve u(t) değerleri ekranda canlı olarak görüntülenir
- **CSV Veri Kaydı** — Simülasyon verileri otomatik olarak CSV'ye kaydedilir
- **30 Waypoint Rotası** — Şehir içi + otoyol rampası içeren kapsamlı rota
- **Laplacian Smoothing** — Waypoint'ler arası pürüzsüz rota oluşturma

## 🏗️ Sistem Mimarisi

```
Referans Rota (Waypoints)
        │
        ▼
┌─────────────────┐
│  Pure Pursuit    │ ──► Hedef Nokta (Lookahead)
│  (Yol Takibi)    │
└────────┬────────┘
         │ Açısal Hata e(t)
         ▼
┌─────────────────┐
│  PID Kontrolcü   │ ──► u(t) = Kp·e + Ki·∫e + Kd·de/dt
│  (Kp, Ki, Kd)    │
└────────┬────────┘
         │ Kontrol Sinyali u(t)
         ▼
┌─────────────────┐
│  Araç Fiziği     │ ──► Direksiyon + Hız Kontrolü
│  (Rigidbody)     │
└─────────────────┘
```

## ⚙️ Optimum PID Parametreleri

| Parametre | Değer | Açıklama |
|-----------|-------|----------|
| **Kp** | 0.99 | Oransal — Hata ile orantılı tepki |
| **Ki** | 0.10 | İntegral — Kalıcı hatayı giderir |
| **Kd** | 2.04 | Türevsel — Salınımları söndürür |

## 📊 Performans Sonuçları

| Metrik | Değer |
|--------|-------|
| Ortalama Takip Hatası | 1.51° |
| RMS Hata | 3.21° |
| Düz Yol Hatası | ±0.15° |
| Maksimum Hata (Keskin Viraj) | 21.7° |
| Simülasyon Süresi | 246 s |

## 📁 Dosya Yapısı

```
oto_kontrol/
├── Assets/
│   ├── Scripts/
│   │   ├── CarController.cs      # Araç kontrol ve CSV kayıt
│   │   ├── PIDController.cs      # PID algoritması
│   │   ├── TrackGenerator.cs     # Rota oluşturma ve smoothing
│   │   └── MyUIManager.cs        # Gerçek zamanlı UI ve grafikler
│   └── Scenes/
│       └── SampleScene.unity     # Ana sahne
├── rapor_grafikleri/              # Matplotlib grafikleri
├── pid_verileri.csv               # Simülasyon çıktı verisi
```

## 🚀 Kurulum ve Çalıştırma

1. **Unity 6** veya üstünü yükleyin
2. Bu repoyu klonlayın:
   ```bash
   git clone https://github.com/berkaslan7988/PID-vehicle-simulation.git
   ```
3. Unity Hub'dan projeyi açın
4. `Assets/Scenes/SampleScene` sahnesini açın
5. **Play** butonuna basın

## 🎛️ Kullanım

- **PID Parametreleri:** Sol üstteki panelden Kp, Ki, Kd slider'larını ayarlayın
- **Araç Hızı:** Inspector'dan veya UI panelinden değiştirin
- **Araç Kütlesi:** Fortina > Rigidbody > Mass değerini değiştirin
- **CSV Çıktısı:** Play'den çıkınca otomatik olarak `pid_verileri.csv` oluşur

## 📈 Rapor Grafiklerini Yeniden Oluşturma

```bash
pip install matplotlib pandas
python rapor_grafikleri.py
```

## 🛠️ Teknolojiler

- **Unity 6** — Oyun motoru ve fizik simülasyonu
- **C#** — Kontrol algoritmaları
- **Python** — Veri analizi ve grafik oluşturma
- **Matplotlib** — Bilimsel grafikler
- **fpdf2 / python-docx** — Rapor oluşturma
