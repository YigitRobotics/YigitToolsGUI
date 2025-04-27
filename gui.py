# GitHub: @YigitRobotics
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.uix.image import Image
import requests
import socket
import random
import sqlite3
import threading
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import smtplib

CONFIG_FILE = 'config.json'

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except:
        cfg = {'openweathermap_api_key': '', 'smtp': {'server': '', 'port': 587}}
        with open(CONFIG_FILE, 'w') as f:
            json.dump(cfg, f)
        return cfg

def save_config(cfg):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(cfg, f)

config = load_config()
class DBHelper:
    def __init__(self, path='yigittools.db'):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self._create_tables()

    def _create_tables(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        action TEXT,
                        detail TEXT
                    )''')
        self.conn.commit()

    def log(self, action, detail=''):
        c = self.conn.cursor()
        c.execute("INSERT INTO history (timestamp,action,detail) VALUES (datetime('now'),?,?)", (action, detail))
        self.conn.commit()

    def fetch_history(self):
        c = self.conn.cursor()
        c.execute("SELECT timestamp,action,detail FROM history ORDER BY id DESC LIMIT 100")
        return c.fetchall()

db = DBHelper()
class BaseScreen(Screen):
    def add_back(self):
        btn = Button(text='Geri', size_hint=(None,None), size=(100,40), pos=(10,10))
        btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'ana_ekran'))
        self.add_widget(btn)

class ArkaPlan(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 0.95)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.degisim, pos=self.degisim)

    def degisim(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos
class Intro(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        img2 = Image(source="logo.png", size=(100,100))
        self.pb = ProgressBar(max=100, value=0)
        layout.add_widget(img2)
        layout.add_widget(self.pb)
        self.add_widget(layout)
        Clock.schedule_interval(self.load, 0.05)

    def load(self, dt):
        if self.pb.value >= 100:
            self.manager.current = 'ana_ekran'
            return False
        self.pb.value += 5
        return True

class AnaEkran(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        main = GridLayout(cols=2, padding=20, spacing=10)
        ops = [
            ("Veri Çekme", "veri_cekme_ekrani"),
            ("İstek Atma", "istek_atma_ekrani"),
            ("Tarayıcı", "tarayici_ekrani"),
            ("Soket", "soket_ekrani"),
            ("Rastgele", "rastgele_ekrani"),
            ("Port Tarayıcı", "port_scan_ekrani"),
            ("E-posta Gönder", "email_ekrani"),
            ("Dosya İndir", "download_ekrani"),
            ("Hava Durumu", "weather_ekrani"),
            ("Geçmiş", "history_ekrani"),
            ("Ayarlar", "settings_ekrani")
        ]
        for text, screen in ops:
            btn = Button(text=text, size_hint=(.4, .2))
            btn.bind(on_press=lambda inst, s=screen: setattr(self.manager, 'current', s))
            main.add_widget(btn)
        self.add_widget(main)
class SettingsEkran(BaseScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text="Ayarlar", font_size=24))
        self.owm = TextInput(text=config.get('openweathermap_api_key',''), hint_text="OpenWeatherMap API Key", size_hint_y=None, height=40)
        layout.add_widget(self.owm)
        smtp = config.get('smtp',{})
        self.smtp_srv = TextInput(text=smtp.get('server',''), hint_text="SMTP Server", size_hint_y=None, height=40)
        self.smtp_port = TextInput(text=str(smtp.get('port',587)), hint_text="SMTP Port", size_hint_y=None, height=40)
        layout.add_widget(self.smtp_srv)
        layout.add_widget(self.smtp_port)
        save_btn = Button(text="Kaydet", size_hint_y=None, height=50)
        save_btn.bind(on_press=self.save)
        layout.add_widget(save_btn)
        self.add_widget(layout)
        self.add_back()

    def save(self, inst):
        config['openweathermap_api_key'] = self.owm.text
        config['smtp']['server'] = self.smtp_srv.text
        config['smtp']['port'] = int(self.smtp_port.text)
        save_config(config)
        popup = Popup(title='Bilgi', content=Label(text='Ayarlar kaydedildi.'), size_hint=(.6,.4))
        popup.open()
        db.log('settings', json.dumps(config))
class VeriCekmeEkran(BaseScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.layout.add_widget(Label(text="Web Veri Çekme", font_size=22))
        self.url = TextInput(hint_text="URL")
        self.tag = TextInput(hint_text="Etiket")
        self.attr = TextInput(hint_text="ID/Class (opsiyonel)")
        self.layout.add_widget(self.url); self.layout.add_widget(self.tag); self.layout.add_widget(self.attr)
        btn = Button(text="Çek")
        btn.bind(on_press=self.fetch)
        self.layout.add_widget(btn)
        self.out = TextInput(readonly=True)
        self.layout.add_widget(self.out)
        self.add_widget(self.layout)
        self.add_back()

    def fetch(self, inst):
        try:
            r = requests.get(self.url.text)
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(r.text, 'html.parser')
            items = soup.find_all(self.tag.text, class_=self.attr.text) if self.attr.text else soup.find_all(self.tag.text)
            texts = [i.get_text().strip() for i in items]
            self.out.text = '\n'.join(texts)
            db.log('fetch', f"{self.url.text} tag={self.tag.text}")
        except Exception as e:
            self.out.text = str(e)

class IstekAtmaEkran(BaseScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        lay = BoxLayout(orientation='vertical', padding=20)
        lay.add_widget(Label(text="HTTP İstek"))
        self.url = TextInput(hint_text="URL")
        self.method = Spinner(text='GET', values=('GET','POST','PUT','DELETE'))
        self.body = TextInput(hint_text="JSON Body (opsiyonel)")
        send = Button(text="Gönder")
        send.bind(on_press=self.send)
        self.res = TextInput(readonly=True)
        lay.add_widget(self.url); lay.add_widget(self.method); lay.add_widget(self.body); lay.add_widget(send); lay.add_widget(self.res)
        self.add_widget(lay)
        self.add_back()

    def send(self, inst):
        try:
            m = self.method.text
            data = None
            if self.body.text:
                data = json.loads(self.body.text)
            r = requests.request(m, self.url.text, json=data)
            self.res.text = f"{r.status_code}\n{r.text[:500]}..."
            db.log('request', f"{m} {self.url.text}")
        except Exception as e:
            self.res.text = str(e)

class TarayiciEkran(BaseScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        lay = BoxLayout(orientation='vertical', padding=20)
        lay.add_widget(Label(text="Browser Otomasyon"))
        self.url = TextInput(hint_text="URL")
        self.action = Spinner(text='Open', values=('Open','Scroll','GetText'))
        self.sel = TextInput(hint_text="CSS Selector (for GetText)")
        run = Button(text="Çalıştır")
        run.bind(on_press=self.run_auto)
        self.log = TextInput(readonly=True)
        lay.add_widget(self.url); lay.add_widget(self.action); lay.add_widget(self.sel); lay.add_widget(run); lay.add_widget(self.log)
        self.add_widget(lay)
        self.add_back()
        opts = Options(); opts.add_argument('--headless')
        self.driver = webdriver.Chrome(options=opts)

    def run_auto(self, inst):
        try:
            self.driver.get(self.url.text)
            act = self.action.text
            if act == 'Scroll':
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.log.text = "Scrolled"
            elif act == 'GetText' and self.sel.text:
                elems = self.driver.find_elements_by_css_selector(self.sel.text)
                self.log.text = '\n'.join([e.text for e in elems])
            else:
                self.log.text = "Opened"
            db.log('browser', act)
        except Exception as e:
            self.log.text = str(e)

class SoketEkran(BaseScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        lay = BoxLayout(orientation='vertical', padding=20)
        lay.add_widget(Label(text="TCP Socket"))
        self.host = TextInput(hint_text="Host")
        self.port = TextInput(hint_text="Port")
        self.msg = TextInput(hint_text="Message")
        btn = Button(text="Send")
        btn.bind(on_press=self.send)
        self.out = TextInput(readonly=True)
        lay.add_widget(self.host); lay.add_widget(self.port); lay.add_widget(self.msg); lay.add_widget(btn); lay.add_widget(self.out)
        self.add_widget(lay)
        self.add_back()

    def send(self, inst):
        try:
            s = socket.socket(); s.connect((self.host.text, int(self.port.text)))
            s.send(self.msg.text.encode())
            data = s.recv(4096)
            self.out.text = data.decode()
            s.close()
            db.log('socket', f"{self.host.text}:{self.port.text}")
        except Exception as e:
            self.out.text = str(e)

class RastgeleEkran(BaseScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        lay = BoxLayout(orientation='vertical', padding=20)
        lay.add_widget(Label(text="Random Generator"))
        self.type = Spinner(text='Number', values=('Number','Text'))
        self.length = TextInput(hint_text="Max/Length")
        btn = Button(text="Generate")
        btn.bind(on_press=self.gen)
        self.out = TextInput(readonly=True)
        lay.add_widget(self.type); lay.add_widget(self.length); lay.add_widget(btn); lay.add_widget(self.out)
        self.add_widget(lay)
        self.add_back()

    def gen(self, inst):
        try:
            l = int(self.length.text)
            if self.type.text == 'Number':
                val = random.randint(0, l)
            else:
                letters = 'abcdefghijklmnopqrstuvwxyz'
                val = ''.join(random.choice(letters) for _ in range(l))
            self.out.text = str(val)
            db.log('random', f"{self.type.text} {val}")
        except Exception as e:
            self.out.text = str(e)

class PortScanEkran(BaseScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        lay = BoxLayout(orientation='vertical', padding=20)
        lay.add_widget(Label(text="Port Scanner"))
        self.host = TextInput(hint_text="Host")
        self.start = TextInput(hint_text="Start Port")
        self.end = TextInput(hint_text="End Port")
        btn = Button(text="Scan")
        btn.bind(on_press=self.scan)
        self.out = TextInput(readonly=True)
        lay.add_widget(self.host); lay.add_widget(self.start); lay.add_widget(self.end); lay.add_widget(btn); lay.add_widget(self.out)
        self.add_widget(lay)
        self.add_back()

    def scan(self, inst):
        open_ports = []
        h = self.host.text
        s = int(self.start.text); e = int(self.end.text)
        for p in range(s, e+1):
            sock = socket.socket(); sock.settimeout(0.5)
            if sock.connect_ex((h,p)) == 0:
                open_ports.append(str(p))
            sock.close()
        self.out.text = 'Open: ' + ','.join(open_ports)
        db.log('portscan', f"{h}:{s}-{e}")

class EmailEkran(BaseScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        lay = BoxLayout(orientation='vertical', padding=20)
        lay.add_widget(Label(text="Email Sender"))
        self.server = TextInput(text=config['smtp']['server'], hint_text="SMTP Server")
        self.port = TextInput(text=str(config['smtp']['port']), hint_text="Port")
        self.user = TextInput(hint_text="User Email")
        self.pw = TextInput(hint_text="Password", password=True)
        self.to = TextInput(hint_text="To Email")
        self.subject = TextInput(hint_text="Subject")
        self.body = TextInput(hint_text="Body", size_hint_y=2)
        btn = Button(text="Send")
        btn.bind(on_press=self.send_mail)
        self.out = TextInput(readonly=True)
        for w in [self.server, self.port, self.user, self.pw, self.to, self.subject, self.body, btn, self.out]: lay.add_widget(w)
        self.add_widget(lay)
        self.add_back()

    def send_mail(self, inst):
        try:
            srv = smtplib.SMTP(self.server.text, int(self.port.text))
            srv.starttls()
            srv.login(self.user.text, self.pw.text)
            msg = f"Subject: {self.subject.text}\n\n{self.body.text}"
            srv.sendmail(self.user.text, self.to.text, msg)
            srv.quit()
            self.out.text = "Sent"
            db.log('email', f"to {self.to.text}")
        except Exception as e:
            self.out.text = str(e)

class DownloadEkran(BaseScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        lay = BoxLayout(orientation='vertical', padding=20)
        lay.add_widget(Label(text="File Download"))
        self.url = TextInput(hint_text="File URL")
        btn = Button(text="Download")
        btn.bind(on_press=self.download)
        self.pb = ProgressBar(max=100)
        self.out = TextInput(readonly=True)
        lay.add_widget(self.url); lay.add_widget(btn); lay.add_widget(self.pb); lay.add_widget(self.out)
        self.add_widget(lay)
        self.add_back()

    def download(self, inst):
        def _dl():
            r = requests.get(self.url.text, stream=True)
            total = int(r.headers.get('content-length',0))
            fname = self.url.text.split('/')[-1]
            with open(fname,'wb') as f:
                dl=0
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        dl += len(chunk)
                        self.pb.value = dl*100/total
            self.out.text = f"Saved {fname}"
            db.log('download', fname)
        threading.Thread(target=_dl).start()

class WeatherEkran(BaseScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        lay = BoxLayout(orientation='vertical', padding=20)
        lay.add_widget(Label(text="Weather"))
        self.city = TextInput(hint_text="City Name")
        btn = Button(text="Get Weather")
        btn.bind(on_press=self.get)
        self.out = TextInput(readonly=True)
        lay.add_widget(self.city); lay.add_widget(btn); lay.add_widget(self.out)
        self.add_widget(lay)
        self.add_back()

    def get(self, inst):
        key = config.get('openweathermap_api_key','')
        if not key:
            self.out.text = "Ayarlar'dan API anahtarı girin"
            return
        try:
            r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={self.city.text}&appid={key}&units=metric")
            d = r.json()
            txt = f"{d['name']}: {d['weather'][0]['description']}, {d['main']['temp']}°C"
            self.out.text = txt
            db.log('weather', self.city.text)
        except Exception as e:
            self.out.text = str(e)

class HistoryEkran(BaseScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        lay = BoxLayout(orientation='vertical', padding=20)
        lay.add_widget(Label(text="History"))
        self.out = TextInput(readonly=True)
        btn = Button(text="Yenile")
        btn.bind(on_press=self.load)
        lay.add_widget(btn); lay.add_widget(self.out)
        self.add_widget(lay)
        self.add_back()
        self.load()

    def load(self, *a):
        recs = db.fetch_history()
        self.out.text = '\n'.join([f"{t} | {a} | {d}" for t,a,d in recs])

class YigitToolsApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Intro(name='intro'))
        sm.add_widget(AnaEkran(name='ana_ekran'))
        sm.add_widget(VeriCekmeEkran(name='veri_cekme_ekrani'))
        sm.add_widget(IstekAtmaEkran(name='istek_atma_ekrani'))
        sm.add_widget(TarayiciEkran(name='tarayici_ekrani'))
        sm.add_widget(SoketEkran(name='soket_ekrani'))
        sm.add_widget(RastgeleEkran(name='rastgele_ekrani'))
        sm.add_widget(PortScanEkran(name='port_scan_ekrani'))
        sm.add_widget(EmailEkran(name='email_ekrani'))
        sm.add_widget(DownloadEkran(name='download_ekrani'))
        sm.add_widget(WeatherEkran(name='weather_ekrani'))
        sm.add_widget(HistoryEkran(name='history_ekrani'))
        sm.add_widget(SettingsEkran(name='settings_ekrani'))
        return sm

if __name__ == '__main__':
    YigitToolsApp().run()