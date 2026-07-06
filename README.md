# 🏎️ PID Kontrolcü ile Otonom Araç Şerit Takip Simülasyonu

<img width="1661" height="818" alt="resim" src="https://github.com/user-attachments/assets/12f1a1c3-3302-4ba0-b173-d3849f2fc942" />

![Unity](https://img.shields.io/badge/Unity-6-black?logo=unity)
![C#](https://img.shields.io/badge/C%23-12-blue?logo=dotnet)
![License](https://img.shields.io/badge/License-MIT-green)

## 📋 Proje Özeti

Unity oyun motoru ortamında geliştirilen, PID (Proportional-Integral-Derivative) kontrolcü kullanarak otonom bir aracın şerit takibi yapmasını sağlayan simülasyon projesidir. Araç, sahnede yerleştirilen referans noktalarını (waypoint) takip ederek şehir içi yollar, kavşaklar, virajlar ve otoyol rampası gibi farklı yol geometrilerinde otonom olarak ilerlemektedir. PID kontrolcü, araç ile hedef rota arasındaki açısal sapmayı (hata) minimize ederek direksiyon kontrolü sağlamaktadır.

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
┌──────────────────┐
│  Pure Pursuit     │ ──► Hedef Nokta (Lookahead)
│  (Rota Takibi)    │
└─────────┬─────────┘
          │ Açısal Hata e(t)
          ▼
┌──────────────────┐
│  PID Kontrolcü    │ ──► u(t) = Kp·e + Ki·∫e + Kd·de/dt
│  (Kp, Ki, Kd)     │
└─────────┬─────────┘
          │ Kontrol Sinyali u(t)
          ▼
┌──────────────────┐
│  Araç Fiziği      │ ──► Direksiyon + Hız Kontrolü
│  (Rigidbody)      │
└──────────────────┘
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
- **Araç Kütlesi:** Aracın Inspector'ındaki `Rigidbody > Mass` değerini değiştirin
- **CSV Çıktısı:** Play'den çıkınca otomatik olarak `pid_verileri.csv` oluşur

## 🛠️ Teknolojiler

- **Unity 6** — Oyun motoru ve fizik simülasyonu
- **C#** — Kontrol algoritmaları
- **Python** — Veri analizi ve grafik oluşturma
- **Matplotlib** — Bilimsel grafikler

---
---

# 🏎️ PID-Controlled Autonomous Vehicle Lane-Following Simulation

![Unity](https://img.shields.io/badge/Unity-6-black?logo=unity)
![C#](https://img.shields.io/badge/C%23-12-blue?logo=dotnet)
![License](https://img.shields.io/badge/License-MIT-green)

## 📋 Project Overview

A simulation project built in the Unity game engine where an autonomous vehicle follows a lane using a PID (Proportional-Integral-Derivative) controller. The vehicle autonomously navigates the scene by following placed reference points (waypoints), driving through varied road geometries such as city streets, intersections, curves, and a highway on-ramp. The PID controller minimizes the angular deviation (error) between the vehicle and the target path to provide steering control.

## 🎮 Features

- **Real-Time PID Control** — Kp, Ki, Kd parameters can be tuned live during the simulation
- **Dynamic Vehicle Parameters** — vehicle speed and mass are adjustable at runtime
- **Automatic Corner Braking** — the vehicle automatically slows down on sharp turns
- **Dynamic Lookahead** — lookahead distance adjusts automatically based on speed
- **Real-Time Charts** — e(t) and u(t) values are displayed live on screen
- **CSV Data Logging** — simulation data is automatically saved to CSV
- **30-Waypoint Route** — a comprehensive route including city streets + a highway ramp
- **Laplacian Smoothing** — smooth path generation between waypoints

## 🏗️ System Architecture

```
Reference Route (Waypoints)
        │
        ▼
┌──────────────────┐
│  Pure Pursuit     │ ──► Target Point (Lookahead)
│  (Path Following) │
└─────────┬─────────┘
          │ Angular Error e(t)
          ▼
┌──────────────────┐
│  PID Controller   │ ──► u(t) = Kp·e + Ki·∫e + Kd·de/dt
│  (Kp, Ki, Kd)     │
└─────────┬─────────┘
          │ Control Signal u(t)
          ▼
┌──────────────────┐
│  Vehicle Physics  │ ──► Steering + Speed Control
│  (Rigidbody)      │
└──────────────────┘
```

## ⚙️ Optimal PID Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| **Kp** | 0.99 | Proportional — response proportional to the error |
| **Ki** | 0.10 | Integral — eliminates steady-state error |
| **Kd** | 2.04 | Derivative — dampens oscillations |

## 📊 Performance Results

| Metric | Value |
|--------|-------|
| Average Tracking Error | 1.51° |
| RMS Error | 3.21° |
| Straight-Road Error | ±0.15° |
| Maximum Error (Sharp Turn) | 21.7° |
| Simulation Duration | 246 s |

## 📁 Project Structure

```
oto_kontrol/
├── Assets/
│   ├── Scripts/
│   │   ├── CarController.cs      # Vehicle control & CSV logging
│   │   ├── PIDController.cs      # PID algorithm
│   │   ├── TrackGenerator.cs     # Route generation & smoothing
│   │   └── MyUIManager.cs        # Real-time UI and charts
│   └── Scenes/
│       └── SampleScene.unity     # Main scene
├── rapor_grafikleri/              # Matplotlib charts
├── pid_verileri.csv               # Simulation output data
```

## 🚀 Setup & Run

1. Install **Unity 6** or newer
2. Clone this repo:
   ```bash
   git clone https://github.com/berkaslan7988/PID-vehicle-simulation.git
   ```
3. Open the project from Unity Hub
4. Open the `Assets/Scenes/SampleScene` scene
5. Press **Play**

## 🎛️ Usage

- **PID Parameters:** adjust the Kp, Ki, Kd sliders from the panel in the top-left corner
- **Vehicle Speed:** change it from the Inspector or the UI panel
- **Vehicle Mass:** change the vehicle's `Rigidbody > Mass` value in the Inspector
- **CSV Output:** `pid_verileri.csv` is generated automatically when you exit Play mode

## 🛠️ Technologies

- **Unity 6** — game engine & physics simulation
- **C#** — control algorithms
- **Python** — data analysis and chart generation
- **Matplotlib** — scientific charts
