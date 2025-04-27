# YigitTools GUI

**YigitTools**, çok amaçlı bir araç kutusudur. Web veri çekmeden, HTTP isteklerine, basit browser otomasyonundan port taramaya, e-posta göndermeden hava durumu sorgulamaya kadar birçok farklı işlemi kullanıcı dostu bir arayüz ile bir araya getirir.  
Geleceğe dönük tasarımı ve esnek modüler yapısıyla, hem hobi projeleri hem de günlük işler için pratik çözümler sunar. Bu proje: YigitTools projesinin GUI (Graphical User Interface) versiyonudur.

## Özellikler

- 🌐 **Web Veri Çekme:** Belirli bir URL'den HTML elementlerini etiket veya class/id filtresi ile çekin.
- 📡 **HTTP İstekleri:** GET, POST, PUT, DELETE metodları ile hızlı API testleri yapın.
- 🛜 **Tarayıcı Otomasyonu:** Basit web tarayıcı işlemleri gerçekleştirin (URL açma, scroll yapma, içerik çekme).
- 🔥 **Socket İletişimi:** IP ve port üzerinden socket işlemleri gerçekleştirin.
- 🎲 **Rastgele Üretici:** Rastgele sayı ve string üreteçleri.
- 🛰️ **Port Tarayıcı:** IP adresleri üzerinde port taramaları yapın.
- ✉️ **E-Posta Gönderici:** SMTP ile e-posta gönderin.
- 📥 **Dosya İndirici:** Belirtilen URL'den dosya indirme işlemleri.
- ☀️ **Hava Durumu:** OpenWeatherMap API entegrasyonu ile anlık hava durumu alın.
- 🗃️ **Geçmiş Yönetimi:** Yapılan işlemleri veritabanına kaydedin ve geçmişe göz atın.
- ⚙️ **Ayarlar:** API anahtarı ve SMTP sunucu bilgilerini kolayca yapılandırın.

## Kurulum

> **Not:** Şu anda sadece masaüstü ortamında (Windows, Linux, Mac) çalışmaktadır. Mobil desteği hedeflenmemiştir.

### Gereksinimler
- Python 3.8+
- [Kivy](https://kivy.org/#home)
- [Requests](https://docs.python-requests.org/en/latest/)
- [Selenium](https://www.selenium.dev/)
- Google Chrome + [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) (Browser otomasyonu için)
- BeautifulSoup4 (`bs4`) (Web veri çekimi için)

### Yükleme Adımları

```bash
git clone https://github.com/YigitRobotics/YigitToolsGUI.git
cd YigitToolsGUI
pip install -r requirements.txt
python gui.py
```

**Ekstra Not:**  
İlk çalıştırmada `config.json` otomatik olarak oluşturulur. Ayarlar ekranından API anahtarlarınızı ve SMTP bilgilerinizi girmeyi unutmayın.

## Kullanım

Program, açılışta kısa bir intro ekranı gösterir. Ardından Ana Menü üzerinden istediğiniz aracı seçerek çalışabilirsiniz.

Her modül kendi içinde küçük ve bağımsızdır, bir hata durumunda yalnızca o modül etkilenir.  
**Kritik not:** Browser otomasyon modülünde ChromeDriver sürümünüz ile Chrome sürümünüzün uyumlu olması gerekir, aksi halde selenium hataları alabilirsiniz.

## Yapılacaklar (Roadmap)

- [ ] Kapsamlı socket chat client/server sistemi
- [ ] Port taramada çoklu IP aralığı desteği
- [ ] Download Manager özellikleri
- [ ] SMTP Auth destekli şifreli e-posta gönderimi
- [ ] Browser otomasyonda Headless Mode
- [ ] Tema (Dark/Light) desteği
- [ ] Hata kayıtlarını ayrı log dosyalarına alma

## Bilinen Hatalar

- Bazı internet sitelerinde veri çekimi sırasında Cloudflare gibi korumalar bypass edilemeyebilir.
- Selenium işlemlerinde Chrome sürüm güncellemeleri sonrası uyumsuzluk çıkabilir.
- Büyük dosya indirme işlemleri sırasında uygulama donabilir (threading iyileştirmesi planlanıyor).

## Katkıda Bulunmak

> Şüphe her ilerlemenin temelidir.  
Bu nedenle, daha iyi ve daha güvenli bir araç geliştirmek için katkılarınızı bekliyoruz.

Katkı yapmak isterseniz:
- Forklayın
- Değişiklik yapın
- Pull request gönderin
- Issue açın ve tartışalım!

## Lisans

Bu proje, **GNU Affero General Public License v3 (AGPL v3)** ile lisanslanmıştır.  
AGPL v3 lisansı, projenin ve tüm türevlerinin açık kaynak olarak kalmasını zorunlu kılar.  
Yazılımı kullanmak, değiştirmek ve dağıtmak serbesttir; ancak yapılan tüm değişikliklerin ve türevlerin de aynı lisans altında paylaşılması gerekir.  
Lütfen yazılımı kullanırken veya dağıtırken, emeğe saygı göstermek ve bu lisans şartlarına uymak zorundasınız.

Copyright © 2025 YigitRobotics