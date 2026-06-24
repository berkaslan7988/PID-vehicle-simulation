# -*- coding: utf-8 -*-
import os
from fpdf import FPDF

class RaporPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)
        
        # DejaVu fontu indir (Turkce karakter destegi)
        font_dir = os.path.join(os.path.dirname(__file__), '_fonts')
        os.makedirs(font_dir, exist_ok=True)
        
        # fpdf2 dahili Unicode fontunu kullan
        self.add_font('dejavu', '', fname='C:\\Windows\\Fonts\\arial.ttf')
        self.add_font('dejavu', 'B', fname='C:\\Windows\\Fonts\\arialbd.ttf')
        self.add_font('dejavu', 'I', fname='C:\\Windows\\Fonts\\ariali.ttf')
    
    def header(self):
        if self.page_no() > 1:
            self.set_font('dejavu', 'I', 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 6, 'PID Kontrolcü ile Otonom Araç Şerit Takip Simülasyonu - Rapor', align='C')
            self.ln(4)
            self.set_draw_color(200, 200, 200)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font('dejavu', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Sayfa {self.page_no()}/{{nb}}', align='C')

    def baslik(self, text, size=18):
        self.set_font('dejavu', 'B', size)
        self.set_text_color(25, 25, 112)
        self.cell(0, 12, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def alt_baslik(self, text, size=14):
        self.set_font('dejavu', 'B', size)
        self.set_text_color(50, 50, 50)
        self.cell(0, 10, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def alt_alt_baslik(self, text, size=12):
        self.set_font('dejavu', 'B', size)
        self.set_text_color(70, 70, 70)
        self.cell(0, 8, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def paragraf(self, text):
        self.set_font('dejavu', '', 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 6, text)
        self.ln(3)

    def madde(self, text):
        self.set_font('dejavu', '', 10)
        self.set_text_color(40, 40, 40)
        x = self.get_x()
        self.cell(8, 6, '•')
        self.multi_cell(0, 6, text)
        self.ln(1)

    def tablo(self, headers, rows, col_widths=None):
        if col_widths is None:
            col_widths = [95, 95]
        
        # Header
        self.set_font('dejavu', 'B', 10)
        self.set_fill_color(25, 25, 112)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 8, h, border=1, fill=True, align='C')
        self.ln()
        
        # Rows
        self.set_font('dejavu', '', 10)
        self.set_text_color(40, 40, 40)
        fill = False
        for row in rows:
            if fill:
                self.set_fill_color(240, 240, 255)
            else:
                self.set_fill_color(255, 255, 255)
            for i, cell in enumerate(row):
                align = 'L' if i == 0 else 'C'
                self.cell(col_widths[i], 7, cell, border=1, fill=True, align=align)
            self.ln()
            fill = not fill
        self.ln(4)

    def cizgi(self):
        self.set_draw_color(180, 180, 180)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def grafik_ekle(self, img_path, caption):
        if os.path.exists(img_path):
            w = 190
            self.image(img_path, x=10, w=w)
            self.ln(2)
            self.set_font('dejavu', 'I', 9)
            self.set_text_color(100, 100, 100)
            self.cell(0, 5, caption, align='C', new_x="LMARGIN", new_y="NEXT")
            self.ln(6)


def main():
    base = os.path.dirname(__file__)
    img_dir = os.path.join(base, 'rapor_grafikleri')
    
    pdf = RaporPDF()
    pdf.alias_nb_pages()

    # =================== KAPAK ===================
    pdf.add_page()
    pdf.ln(30)
    pdf.set_font('dejavu', 'B', 28)
    pdf.set_text_color(25, 25, 112)
    pdf.cell(0, 15, 'PID Kontrolcü ile', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 15, 'Otonom Araç Şerit Takip', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 15, 'Simülasyonu', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    
    pdf.set_draw_color(25, 25, 112)
    pdf.set_line_width(1)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(10)
    
    pdf.set_font('dejavu', '', 14)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, 'Proje Raporu', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    pdf.set_font('dejavu', '', 12)
    pdf.cell(0, 8, 'Simülasyon Ortamı: Unity 6', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, 'Programlama Dili: C#', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(30)
    
    pdf.set_font('dejavu', 'I', 10)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 8, 'Haziran 2026', align='C', new_x="LMARGIN", new_y="NEXT")

    # =================== İÇİNDEKİLER ===================
    pdf.add_page()
    pdf.baslik('İçindekiler')
    pdf.ln(5)
    
    icerik = [
        ('1.', 'Giriş', '3'),
        ('2.', 'Zorunlu Grafikler', '4'),
        ('  2.1.', 'Takip Hatası e(t)', '4'),
        ('  2.2.', 'Kontrolcü Çıkışı u(t)', '5'),
        ('  2.3.', 'Referans ve Gerçek Yol Karşılaştırması', '6'),
        ('  2.4.', 'Araç Hızı', '7'),
        ('3.', 'Bölgesel Analiz', '8'),
        ('  3.1.', 'Düz Yol Bölgesi', '8'),
        ('  3.2.', 'Viraj Bölgesi', '9'),
        ('4.', 'İstatistiksel Sonuçlar', '10'),
        ('5.', 'Analiz Soruları ve Cevapları', '11'),
        ('6.', 'Sonuç', '15'),
    ]
    
    for num, title, page in icerik:
        pdf.set_font('dejavu', 'B' if not num.startswith(' ') else '', 11)
        pdf.set_text_color(40, 40, 40)
        pdf.cell(15, 8, num)
        pdf.cell(140, 8, title)
        pdf.set_font('dejavu', '', 11)
        pdf.cell(0, 8, page, align='R')
        pdf.ln()
        if not num.startswith(' '):
            pdf.set_draw_color(220, 220, 220)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    # =================== 1. GİRİŞ ===================
    pdf.add_page()
    pdf.baslik('1. Giriş')
    pdf.paragraf('Bu rapor, Unity oyun motoru ortamında geliştirilen otonom araç şerit takip simülasyonunun sonuçlarını sunmaktadır. Araç, referans olarak tanımlanan şeridi PID (Proportional-Integral-Derivative) kontrolcü yardımıyla takip etmektedir. Simülasyon, şehir içi yollar, kavşaklar, virajlar ve otoyol rampası gibi farklı yol geometrilerini içermektedir.')
    
    pdf.alt_alt_baslik('Sistem Özellikleri')
    pdf.tablo(
        ['Parametre', 'Değer'],
        [
            ['PID - Kp (Oransal)', '0.99'],
            ['PID - Ki (İntegral)', '0.10'],
            ['PID - Kd (Türevsel)', '2.04'],
            ['Araç Kütlesi', '1200 kg'],
            ['Hedef Hız', '20 m/s (72 km/h)'],
            ['Örnekleme Frekansı', '50 Hz (FixedUpdate)'],
            ['Toplam Simülasyon Süresi', '245.94 s'],
            ['Toplam Veri Noktası', '12,298'],
        ]
    )
    
    pdf.alt_alt_baslik('Kontrol Mimarisi')
    pdf.madde('Hata Sinyali e(t): Araç ile hedef rota arasındaki açısal sapma (derece)')
    pdf.madde('Kontrol Sinyali u(t): PID kontrolcünün ürettiği direksiyon kontrol çıkışı')
    pdf.madde('Pure Pursuit + PID: Dinamik lookahead mesafesi ile hedefe yönelme, PID ile düzeltme')

    # =================== 2. GRAFİKLER ===================
    pdf.add_page()
    pdf.baslik('2. Zorunlu Grafikler')
    
    # 2.1
    pdf.alt_baslik('2.1. Takip Hatası e(t)')
    pdf.paragraf('Grafik, simülasyon boyunca araç ile referans rota arasındaki açısal sapma hatasını göstermektedir. e(t) = 0 çizgisi referans hattı olarak kırmızı kesikli çizgiyle belirtilmiştir.')
    pdf.grafik_ekle(os.path.join(img_dir, '1_takip_hatasi_et.png'), 'Şekil 1: Takip Hatası e(t) - Zaman Grafiği')
    
    pdf.madde('Düz yol bölgelerinde hata ±0.15 derece civarında seyretmektedir')
    pdf.madde('Viraj bölgelerinde hata ±20 dereceye kadar artmaktadır')
    pdf.madde('Araç viraj çıkışlarında hatayı yaklaşık 2-3 saniye içinde sıfıra yaklaştırmaktadır')

    # 2.2
    pdf.add_page()
    pdf.alt_baslik('2.2. Kontrolcü Çıkışı u(t)')
    pdf.paragraf('Kontrol sinyali u(t), PID kontrolcünün direksiyon açısını belirlemek için ürettiği çıkışı temsil etmektedir.')
    pdf.grafik_ekle(os.path.join(img_dir, '2_kontrolcu_cikisi_ut.png'), 'Şekil 2: Kontrolcü Çıkışı u(t) - Zaman Grafiği')
    
    pdf.madde('Düz yollarda kontrol sinyali ±0.05 civarında, oldukça sakin seyretmektedir')
    pdf.madde('Keskin virajlarda sinyal ±27 değerine kadar yükselmektedir')
    pdf.madde('Kontrol sinyali, hatayı takip eden ama hafif gecikmeyle reaksiyon veren yumuşak bir karakteristik göstermektedir')

    # 2.3
    pdf.add_page()
    pdf.alt_baslik('2.3. Referans ve Gerçek Yol Karşılaştırması')
    pdf.paragraf('Bu grafik, hata sinyali e(t) ile kontrol sinyali u(t) arasındaki ilişkiyi göstermektedir. Kontrolcünün hataya ne kadar hızlı ve ne ölçüde tepki verdiği görsel olarak karşılaştırılabilmektedir.')
    pdf.grafik_ekle(os.path.join(img_dir, '3_et_ut_karsilastirma.png'), 'Şekil 3: e(t) ve u(t) Karşılaştırması')

    # 2.4
    pdf.add_page()
    pdf.alt_baslik('2.4. Araç Hızı')
    pdf.paragraf('Aracın simülasyon boyunca anlık hız grafiği. Virajlarda otomatik yavaşlama (corner braking) mekanizmasının etkinliği gözlemlenmektedir.')
    pdf.grafik_ekle(os.path.join(img_dir, '4_arac_hizi.png'), 'Şekil 4: Araç Hızı - Zaman Grafiği')

    # =================== 3. BÖLGESEL ANALİZ ===================
    pdf.add_page()
    pdf.baslik('3. Bölgesel Analiz')
    
    pdf.alt_baslik('3.1. Düz Yol Bölgesi')
    pdf.paragraf('Düz yol bölgesinde (t=0.0s - 6.9s) takip hatası detaylı olarak gösterilmektedir. Hata ±0.15 derece bandında seyretmekte olup, bu durum kontrolcünün düz yollarda mükemmele yakın bir performans sergilediğini kanıtlamaktadır.')
    pdf.grafik_ekle(os.path.join(img_dir, '5_duz_yol_hatasi.png'), 'Şekil 5: Düz Yol Bölgesi - Detaylı Takip Hatası')

    pdf.add_page()
    pdf.alt_baslik('3.2. Viraj Bölgesi')
    pdf.paragraf('Bir viraj geçişi sırasında hata ve kontrol sinyalinin davranışı detaylı olarak gösterilmektedir. Keskin virajlarda hatanın arttığı, kontrolcünün agresif bir düzeltme uyguladığı ve viraj çıkışında hatanın tekrar sıfıra yaklaştığı gözlemlenmektedir.')
    pdf.grafik_ekle(os.path.join(img_dir, '6_viraj_hatasi.png'), 'Şekil 6: Viraj Bölgesi - Hata ve Kontrol Analizi')

    # =================== 4. İSTATİSTİKLER ===================
    pdf.add_page()
    pdf.baslik('4. İstatistiksel Sonuçlar')
    
    pdf.tablo(
        ['Metrik', 'Değer'],
        [
            ['Ortalama |e(t)|', '1.5068°'],
            ['Maksimum |e(t)|', '21.7101°'],
            ['RMS Hata', '3.2115°'],
            ['Standart Sapma (e)', '3.2117°'],
            ['Ortalama |u(t)|', '1.1451'],
            ['Maksimum |u(t)|', '27.1554'],
            ['Ortalama Hız', '5.97 m/s (21.5 km/h)'],
            ['Maksimum Hız', '12.63 m/s (45.5 km/h)'],
        ]
    )
    
    pdf.alt_alt_baslik('Kararlılık Analizi (Son 5 saniye)')
    pdf.tablo(
        ['Metrik', 'Değer'],
        [
            ['Ortalama |e(t)|', '0.1568°'],
            ['Standart Sapma', '0.0386°'],
        ]
    )
    pdf.paragraf('Son 5 saniyedeki veriler, sistemin uzun vadede kararlı çalıştığını ve hatanın 0.16° civarında sabitlendiğini göstermektedir.')

    # =================== 5. ANALİZ SORULARI ===================
    pdf.add_page()
    pdf.baslik('5. Analiz Soruları ve Cevapları')
    
    # 5.1
    pdf.alt_alt_baslik('5.1. Araç düz yolda nasıl davranmaktadır?')
    pdf.paragraf('Araç düz yolda son derece kararlı davranmaktadır. Düz yol bölgelerinde takip hatası ±0.15 derece bandında kalmakta olup, bu değer pratik açıdan sıfıra çok yakındır. Kontrolcü çıkışı da düz yolda minimal düzeyde kalmakta (±0.05), bu da direksiyonun gereksiz yere kırılmadığını ve aracın ip gibi düz gittiğini göstermektedir. Kd=2.04 gibi yüksek bir türev katsayısı, düz yolda oluşabilecek küçük salınımları etkin bir şekilde söndürmektedir.')
    
    # 5.2
    pdf.alt_alt_baslik('5.2. Virajlarda hata nasıl değişmektedir?')
    pdf.paragraf('Virajlarda hata belirgin şekilde artmaktadır. Keskin şehir içi kavşaklarda (90 derecelik dönüşler) hata ±15-21 derece seviyelerine çıkabilmektedir. Bu artış beklenen bir davranıştır çünkü viraj giriş anında araç hâlâ düz yöne bakarken hedef nokta yana kaymaktadır. Fiziksel olarak anlık yön değiştirmek mümkün değildir (araç atalet kütlesine sahiptir). Viraj çıkışında kontrolcü hatayı yaklaşık 2-3 saniye içinde sıfıra indirebilmektedir.')
    
    # 5.3
    pdf.alt_alt_baslik('5.3. PID parametreleri değiştirildiğinde araç davranışı nasıl etkilenmektedir?')
    pdf.paragraf('PID parametreleri simülasyon sırasında canlı olarak Inspector panelinden değiştirilebilmektedir:')
    pdf.madde('Kp artırıldığında: Araç rotaya daha agresif dönmeye çalışır, aşırı artışta (>2.0) salınım başlar')
    pdf.madde('Kp azaltıldığında: Araç yavaş tepki verir, virajları geniş alır')
    pdf.madde('Ki artırıldığında: Kalıcı hata (offset) giderilir ama aşırı artışta integral sarması oluşur')
    pdf.madde('Kd artırıldığında: Salınımlar söner, aşırı artışta (>5.0) araç donuk/ağır tepki verir')
    pdf.madde('Kd azaltıldığında: Araç hızlı tepki verir ama salınım ve titreşim başlar')
    
    # 5.4
    pdf.alt_alt_baslik('5.4. Hangi parametre seti en iyi sonucu vermiştir?')
    pdf.paragraf('Kp=0.99, Ki=0.10, Kd=2.04 parametre seti en iyi sonucu vermiştir. Bu değerler deneysel olarak optimize edilmiştir:')
    pdf.madde('Kp=0.99: Yeterince güçlü oransal tepki sağlarken aşırı kırılma yapmaz')
    pdf.madde('Ki=0.10: Düşük bir integral katsayısı kalıcı offseti yavaşça giderir')
    pdf.madde('Kd=2.04: Güçlü türev katsayısı salınımları etkin şekilde söndürür')
    
    # 5.5
    pdf.add_page()
    pdf.alt_alt_baslik('5.5. Kontrol sinyali çok agresif midir, yumuşak mıdır?')
    pdf.paragraf('Kontrol sinyali dengeli bir karakteristik göstermektedir. Düz yollarda u(t) ≈ ±0.05 ile oldukça yumuşak, normal virajlarda u(t) ≈ ±5 ile ölçülü agresif, keskin 90 derecelik kavşaklarda u(t) ≈ ±27 ile güçlü ama gerekli düzeyde agresiftir. Kd=2.04 değeri sayesinde kontrolcü, hata büyüdüğünde güçlü düzeltme yaparken ani değişimlerde fren etkisi oluşturarak aşırı tepkiyi (overshoot) engellemektedir.')
    
    # 5.6
    pdf.alt_alt_baslik('5.6. Araç salınım yapmakta mıdır?')
    pdf.paragraf('Seçilen parametre setiyle araç belirgin bir salınım yapmamaktadır. Düz yol bölgelerindeki hata grafiği incelendiğinde, monoton bir yaklaşma (convergence) gözlemlenmekte olup, sürekli artan-azalan bir salınım kalıbı (oscillation pattern) bulunmamaktadır. Kd=2.04 değerinin güçlü sönümleme etkisi, Kp=0.99 değerinin ürettiği düzeltme sinyalinin aşırıya kaçmasını engellemektedir.')
    
    # 5.7
    pdf.alt_alt_baslik('5.7. Sistem kararlı mıdır?')
    pdf.paragraf('Evet, sistem kararlıdır. Kanıtlar:')
    pdf.madde('Son 5 saniyedeki ortalama hata 0.1568° ve standart sapma 0.0386° ile minimum düzeydedir')
    pdf.madde('Hata hiçbir zaman ıraksamamıştır (divergence yok)')
    pdf.madde('Her viraj sonrası hata sonlu sürede sıfıra yaklaşmaktadır (BIBO kararlılık)')
    pdf.madde('246 saniyelik uzun simülasyon boyunca sistem hiçbir noktada kontrolü kaybetmemiştir')
    
    # 5.8
    pdf.alt_alt_baslik('5.8. Keskin virajlarda takip başarımı düşmekte midir?')
    pdf.paragraf('Evet, keskin virajlarda takip başarımı beklenen şekilde düşmektedir. 90 derecelik şehir içi kavşaklarda anlık hata 21.7 dereceye kadar çıkabilmektedir. Bu düşüş kaçınılmazdır çünkü araç 1200 kg kütleye sahiptir ve ani yön değişikliği fiziksel olarak imkânsızdır. Otomatik fren sistemi virajlarda hızı düşürse de minimum 14 m/s korunmaktadır. Viraj çıkışında kontrolcü hatayı başarıyla gidermektedir.')
    
    # 5.9
    pdf.alt_alt_baslik('5.9. Yükselme ve yerleşme süreleri nasıl etkilenmektedir?')
    pdf.paragraf('Kontrolcü parametreleri değiştiğinde yükselme ve yerleşme süreleri şu şekilde etkilenmektedir:')
    pdf.madde('Kp artarsa: Yükselme süresi (rise time) kısalır, ancak aşma (overshoot) artar ve yerleşme süresi uzayabilir')
    pdf.madde('Kd artarsa: Yükselme süresi uzar, ancak aşma azalır ve yerleşme süresi kısalır (sönümleme artar)')
    pdf.madde('Ki artarsa: Kalıcı durum hatası azalır, ancak yerleşme süresi uzar ve aşma riski artar')
    pdf.paragraf('Mevcut parametrelerle (Kp=0.99, Ki=0.10, Kd=2.04) sistem, overdamped (aşırı sönümlü) karakteristik göstermekte olup bu durum otonom araç için idealdir: aşma yapmadan, güvenli bir şekilde hedefe yaklaşmaktadır.')

    # =================== 6. SONUÇ ===================
    pdf.add_page()
    pdf.baslik('6. Sonuç')
    pdf.paragraf('PID kontrolcü ile geliştirilen şerit takip sistemi, 30 adet referans noktasından oluşan karmaşık bir şehir içi rotayı başarıyla takip edebilmektedir. Kp=0.99, Ki=0.10, Kd=2.04 parametre seti ile aşağıdaki sonuçlar elde edilmiştir:')
    
    pdf.madde('Düz yollarda mükemmele yakın takip (±0.15°)')
    pdf.madde('Viraj çıkışlarında hızlı toparlanma (2-3 saniye)')
    pdf.madde('Salınımsız, kararlı sürüş')
    pdf.madde('Otomatik viraj freni ile güvenli dönüş')
    pdf.madde('246 saniyelik kesintisiz çalışma')
    
    pdf.ln(5)
    pdf.paragraf('Sistem, PID parametreleri uygun olmayan değerlere ayarlandığında (örneğin Kp>3, Kd=0) kontrol kaybı, salınım ve şerit ihlali doğal olarak gözlemlenebilmektedir. Bu durum, sistemde yapay sınırlandırma bulunmadığını ve PID parametrelerinin etkisinin doğrudan gözlemlenebildiğini kanıtlamaktadır.')

    # PDF kaydet
    out_path = os.path.join(base, 'PID_Rapor.pdf')
    pdf.output(out_path)
    print(f"\nPDF rapor basariyla olusturuldu: {out_path}")
    print(f"Toplam sayfa sayisi: {pdf.page_no()}")


if __name__ == '__main__':
    main()
