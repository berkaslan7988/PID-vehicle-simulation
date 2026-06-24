# 🏎️ PID-Controlled Autonomous Vehicle Lane-Following Simulation / PID Kontrolcü ile Otonom Araç Şerit Takip Simülasyonu

A simulation project built in the Unity game engine where an autonomous vehicle follows a lane using a PID (Proportional-Integral-Derivative) controller. / Unity oyun motoru ortamında geliştirilen, PID (Proportional-Integral-Derivative) kontrolcü kullanarak otonom bir aracın şerit takibi yapmasını sağlayan simülasyon projesidir.

![Unity](https://img.shields.io/badge/Unity-6-black?logo=unity)
![C#](https://img.shields.io/badge/C%23-12-blue?logo=dotnet)
![License](https://img.shields.io/badge/License-MIT-green)

## 📋 Project Overview / Proje Özeti

The vehicle autonomously navigates the scene by following placed reference points (waypoints), driving through varied road geometries such as city streets, intersections, curves, and a highway on-ramp. The PID controller minimizes the angular deviation (error) between the vehicle and the target path to provide steering control. / Araç, sahnede yerleştirilen referans noktalarını (waypoint) takip ederek şehir içi yollar, kavşaklar, virajlar ve otoyol rampası gibi farklı yol geometrilerinde otonom olarak ilerlemektedir. PID kontrolcü, araç ile hedef rota arasındaki açısal sapmayı (hata) minimize ederek direksiyon kontrolü sağlamaktadır.

## 🎮 Features / Özellikler

- **Real-Time PID Control / Gerçek Zamanlı PID Kontrolü** — Kp, Ki, Kd parameters can be tuned live during the simulation / Kp, Ki, Kd parametreleri simülasyon sırasında canlı olarak değiştirilebilir
- **Dynamic Vehicle Parameters / Dinamik Araç Parametreleri** — vehicle speed and mass are adjustable at runtime / Araç hızı ve kütlesi çalışma anında ayarlanabilir
- **Automatic Corner Braking / Otomatik Viraj Freni** — the vehicle automatically slows down on sharp turns / Keskin virajlarda araç otomatik olarak yavaşlar
- **Dynamic Lookahead** — lookahead distance adjusts automatically based on speed / Hıza göre bakış mesafesi otomatik ayarlanır
- **Real-Time Charts / Gerçek Zamanlı Grafikler** — e(t) and u(t) values are displayed live on screen / e(t) ve u(t) değerleri ekranda canlı olarak görüntülenir
- **CSV Data Logging / CSV Veri Kaydı** — simulation data is automatically saved to CSV / Simülasyon verileri otomatik olarak CSV'ye kaydedilir
- **30-Waypoint Route / 30 Waypoint Rotası** — a comprehensive route including city streets + a highway ramp / Şehir içi + otoyol rampası içeren kapsamlı rota
- **Laplacian Smoothing** — smooth path generation between waypoints / Waypoint'ler arası pürüzsüz rota oluşturma

## 🏗️ System Architecture / Sistem Mimarisi

```
Reference Route (Waypoints) / Referans Rota (Waypoints)
        │
        ▼
┌──────────────────┐
│  Pure Pursuit     │ ──► Target Point (Lookahead) / Hedef Nokta
│  (Path Following) │
└─────────┬─────────┘
          │ Angular Error / Açısal Hata e(t)
          ▼
┌──────────────────┐
│  PID Controller   │ ──► u(t) = Kp·e + Ki·∫e + Kd·de/dt
│  (Kp, Ki, Kd)     │
└─────────┬─────────┘
          │ Control Signal / Kontrol Sinyali u(t)
          ▼
┌──────────────────┐
│  Vehicle Physics  │ ──► Steering + Speed Control / Direksiyon + Hız Kontrolü
│  (Rigidbody)      │
└──────────────────┘
```

## ⚙️ Optimal PID Parameters / Optimum PID Parametreleri

| Parameter / Parametre | Value / Değer | Description / Açıklama |
|------------------------|----------------|--------------------------|
| **Kp** | 0.99 | Proportional — response proportional to the error / Oransal — Hata ile orantılı tepki |
| **Ki** | 0.10 | Integral — eliminates steady-state error / İntegral — Kalıcı hatayı giderir |
| **Kd** | 2.04 | Derivative — dampens oscillations / Türevsel — Salınımları söndürür |

## 📊 Performance Results / Performans Sonuçları

| Metric / Metrik | Value / Değer |
|------------------|----------------|
| Average Tracking Error / Ortalama Takip Hatası | 1.51° |
| RMS Error / RMS Hata | 3.21° |
| Straight-Road Error / Düz Yol Hatası | ±0.15° |
| Maximum Error (Sharp Turn) / Maksimum Hata (Keskin Viraj) | 21.7° |
| Simulation Duration / Simülasyon Süresi | 246 s |

## 📁 Project Structure / Dosya Yapısı

```
oto_kontrol/
├── Assets/
│   ├── Scripts/
│   │   ├── CarController.cs      # Vehicle control & CSV logging / Araç kontrol ve CSV kayıt
│   │   ├── PIDController.cs      # PID algorithm / PID algoritması
│   │   ├── TrackGenerator.cs     # Route generation & smoothing / Rota oluşturma ve smoothing
│   │   └── MyUIManager.cs        # Real-time UI and charts / Gerçek zamanlı UI ve grafikler
│   └── Scenes/
│       └── SampleScene.unity     # Main scene / Ana sahne
├── rapor_grafikleri/              # Matplotlib charts / Matplotlib grafikleri
├── pid_verileri.csv               # Simulation output data / Simülasyon çıktı verisi
```

## 🚀 Setup & Run / Kurulum ve Çalıştırma

1. Install **Unity 6** or newer / **Unity 6** veya üstünü yükleyin
2. Clone this repo / Bu repoyu klonlayın:
   ```bash
   git clone https://github.com/berkaslan7988/PID-vehicle-simulation.git
   ```
3. Open the project from Unity Hub / Unity Hub'dan projeyi açın
4. Open the `Assets/Scenes/SampleScene` scene / `Assets/Scenes/SampleScene` sahnesini açın
5. Press **Play** / **Play** butonuna basın

## 🎛️ Usage / Kullanım

- **PID Parameters / PID Parametreleri:** adjust the Kp, Ki, Kd sliders from the panel in the top-left corner / Sol üstteki panelden Kp, Ki, Kd slider'larını ayarlayın
- **Vehicle Speed / Araç Hızı:** change it from the Inspector or the UI panel / Inspector'dan veya UI panelinden değiştirin
- **Vehicle Mass / Araç Kütlesi:** change the vehicle's `Rigidbody > Mass` value in the Inspector / Aracın Inspector'ındaki `Rigidbody > Mass` değerini değiştirin
- **CSV Output / CSV Çıktısı:** `pid_verileri.csv` is generated automatically when you exit Play mode / Play'den çıkınca otomatik olarak `pid_verileri.csv` oluşur


## 🛠️ Technologies / Teknolojiler

- **Unity 6** — game engine & physics simulation / Oyun motoru ve fizik simülasyonu
- **C#** — control algorithms / Kontrol algoritmaları
- **Python** — data analysis and chart generation / Veri analizi ve grafik oluşturma
- **Matplotlib** — scientific charts / Bilimsel grafikler
