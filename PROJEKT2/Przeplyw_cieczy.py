import sys  
from datetime import datetime  
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMessageBox  
from PyQt5.QtCore import Qt, QTimer, QPointF  
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath, QBrush 


# === KLASA RURA  ===
class Rura:
    def __init__(self, punkty, grubosc=12, kolor=Qt.gray):  # Konstruktor rury
        self.punkty = [QPointF(float(p[0]), float(p[1])) for p in punkty]  
        self.kolor_rury = kolor 
        self.kolor_cieczy = QColor(0, 180, 255)  
        self.czy_plynie = False  
        self.grubosc = grubosc

    def ustaw_przeplyw(self, plynie):  # Metoda do wł./wył. wizualizacji przepływu
        self.czy_plynie = plynie   

    def draw(self, painter):  # Metoda rysująca rurę 
        if len(self.punkty) < 2: return  
        path = QPainterPath()  
        path.moveTo(self.punkty[0])  
        for p in self.punkty[1:]: path.lineTo(p) 

        #  Rysowanie rury 
        pen_rura = QPen(self.kolor_rury, self.grubosc, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)  # Ustawienie "pisaka": szary, gruby, zaokrąglone końce
        painter.setPen(pen_rura)  
        painter.setBrush(Qt.NoBrush)  
        painter.drawPath(path) 
        
        if self.czy_plynie:
            pen_ciecz = QPen(self.kolor_cieczy, self.grubosc - 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen_ciecz)  
            painter.drawPath(path)  


# === KLASA ZBIORNIK ===
class Zbiornik:
    def __init__(self, x, y, width=100, height=140, nazwa=""):  # Konstruktor zbiornika 
        
        #wsp. lewy góry róg; szerokokosc; wysokosc; nazwa; pojemnosc; aktulana ilosc;% wypełnienia;
        self.x = x  
        self.y = y  
        self.width = width  
        self.height = height  
        self.nazwa = nazwa 
        self.pojemnosc = 100.0  
        self.aktualna_ilosc = 0.0 
        self.poziom = 0.0  
        
        
        self.temperatura = 15.0 


    def dodaj_ciecz(self, ilosc):  # Metoda dodająca cieczy
        wolne = self.pojemnosc - self.aktualna_ilosc  
        dodano = min(ilosc, wolne)  
        self.aktualna_ilosc += dodano  
        self.aktualizuj_poziom()  
        return dodano 

    def usun_ciecz(self, ilosc):  # Metoda zabierająca cieczy
        usunieto = min(ilosc, self.aktualna_ilosc)  
        self.aktualna_ilosc -= usunieto  
        self.aktualizuj_poziom()  
        return usunieto  

    def ustaw_ilosc(self, ilosc):   #Metoda pilnująca poziom cieczy w zbiorniku
        self.aktualna_ilosc = max(0.0, min(ilosc, self.pojemnosc))  
        self.aktualizuj_poziom() 

    def aktualizuj_poziom(self):  # Metoda przeliczająca ilość z przedzialu 0.00 - 1.00 
        self.poziom = self.aktualna_ilosc / self.pojemnosc  

    def czy_pusty(self): return self.aktualna_ilosc == 0  
    def czy_pelny(self): return self.aktualna_ilosc == self.pojemnosc   

    # Metody zwracające wsp. punktów podłączenia rur
    def punkt_gora_srodek(self): return (self.x + self.width / 2, self.y)
    def punkt_dol_srodek(self): return (self.x + self.width / 2, self.y + self.height)
    def punkt_prawo_srodek(self): return (self.x + self.width, self.y + self.height / 2)
    def punkt_lewo_srodek(self): return (self.x, self.y + self.height / 2)

    def draw(self, painter):  # Metoda rysująca zbiornik
        if self.poziom > 0:  
            h_cieczy = self.height * self.poziom  # Obliczenie wysokości słupa cieczy 
            y_start = self.y + self.height - h_cieczy  # Obliczenie punktu Y, od którego rysować ciecz
            painter.setPen(Qt.NoPen) 
            
            
            r_cieczy = min(255, int((self.temperatura - 15) * 2))  # Obliczenie składowej czerwonej koloru na podstawie temperatury
            painter.setBrush(QColor(r_cieczy, 120, 255 - int(r_cieczy/2), 200))  # Ustawienie koloru wypełnienia (zmienia się od niebieskiego do czerwonego)
            painter.drawRect(int(self.x + 3), int(y_start), int(self.width), int(h_cieczy))  # Rysowanie prostokąta cieczy (z marginesem wewnątrz ścianek)

        pen = QPen(Qt.white, 4)  # ramka
        pen.setJoinStyle(Qt.MiterJoin)  # kąty proste
        painter.setPen(pen)  
        painter.setBrush(Qt.NoBrush)  # Brak wypełnienia 
        painter.drawRect(int(self.x), int(self.y), int(self.width), int(self.height))  #  obrys zbiornika


# === KLASA GRZAŁKA ===
class Grzalka:
    def __init__(self, zbiornik):  # Konstruktor grzałki 
        self.zbiornik = zbiornik  
        self.wlaczona = False  # Stan początkowy
        
        #połozenie grzalki
        margin = 15  
        self.start_x = zbiornik.x + margin  
        self.end_x = zbiornik.x + zbiornik.width - margin 
        self.base_y = zbiornik.y + zbiornik.height - 15  

    def przelacz(self):  # Metoda przełączająca włącznik
        self.wlaczona = not self.wlaczona  

    def draw(self, painter): #Metoda rysujaca ząbki 
        path = QPainterPath()
        
        # Punkty ząbków grzałki
        x = self.start_x
        y = self.base_y
        path.moveTo(x, y)
        
        path.lineTo(x + 7,  y - 10)  
        path.lineTo(x + 14, y)       
       
        path.lineTo(x + 21, y - 10)
        path.lineTo(x + 28, y)
      
        path.lineTo(x + 35, y - 10)
        path.lineTo(x + 42, y)
      
        path.lineTo(x + 49, y - 10)
        path.lineTo(x + 56, y)
      
        path.lineTo(x + 63, y - 10)
        path.lineTo(x + 70, y)       
      
        kolor = QColor(255, 30, 30) if self.wlaczona else QColor(80, 80, 80)
        
        
        if self.wlaczona:  # Efekty grzałki
            pen = QPen(kolor, 5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)  
            painter.setPen(pen)
            painter.drawPath(path)
            pen.setColor(QColor(255, 200, 100))  
            pen.setWidth(2)  
            painter.setPen(pen)
            painter.drawPath(path)  
        else:  
            pen = QPen(kolor, 4, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)  
            painter.setPen(pen)
            painter.drawPath(path)


# === GŁÓWNA KLASA APLIKACJI  ===
class SymulacjaKaskady(QWidget):
    def __init__(self):  # Konstruktor głównego okna
        super().__init__()  # Wywoływanie konstruktora klasy nadrzędnej (QWidget)
        self.setWindowTitle("Projekt 2 - Przepływ cieczy")  # tytuł paska okna
        self.setFixedSize(1100, 650)  # rozmiar okna
        self.setStyleSheet("background-color: #222;")   #kolor tła

        #tworzenie zbiorników
        self.z1 = Zbiornik(30, 50, nazwa="Zbiornik 1")  
        self.z2 = Zbiornik(280, 50, nazwa="Zbiornik 2")  
        self.z3 = Zbiornik(580, 220, nazwa="Zbiornik 3")  
        self.z4 = Zbiornik(400, 390, nazwa="Zbiornik 4")  
        self.z5 = Zbiornik(760, 390, nazwa="Zbiornik 5")  
        
        self.zbiorniki = [self.z1, self.z2, self.z3, self.z5, self.z4]  # Lista zbiornikow
        self.grzalka_z5 = Grzalka(self.z5)  # Utworzenie grzałki i przypisanie jej do zbiornika 5

        # --- ZMIENNA BLOKUJĄCA ALARM ---
        self.alarm_juz_byl = False  

        # --- ZAWÓR ---
        self.tryb_zaworu = 0  # 0: oba otwarte, 1: lewo, 2: prawo, 3: stop
        self.kolory_zaworu = [QColor(Qt.green), QColor(Qt.yellow), QColor(Qt.blue), QColor(Qt.red)]  # Kolory dla trybów
        self.opisy_zaworu = ["OBA", "LEWO", "PRAWO", "STOP"]  # Opisy tekstowe trybów

        # --- RURY ---
        self.rura_z1_z2 = Rura([self.z1.punkt_prawo_srodek(), self.z2.punkt_lewo_srodek()])  # Rura Z1 - Z2
        
        #  rura Z2 - Z3 
        p2s, p2k = self.z2.punkt_dol_srodek(), self.z3.punkt_gora_srodek()
        mid1 = (p2s[1] + p2k[1]) / 2  
        self.rura_z2_z3 = Rura([p2s, (p2s[0], mid1), (p2k[0], mid1), p2k]) 

        #  rozdzielacz pod Z3
        p3_start = self.z3.punkt_dol_srodek()
        p_z4_in = self.z4.punkt_gora_srodek() 
        p_z5_in = self.z5.punkt_gora_srodek() 
        idealny_srodek_x = (p_z4_in[0] + p_z5_in[0]) / 2  # Punkt środkowy między Z4 a Z5 
        self.split_point = (idealny_srodek_x, p3_start[1] + 10)  # Punkt rozgałęzienia rur

        # Tworzenie rur dolnych
        self.rura_z3_pion = Rura([p3_start, self.split_point])  # Pionowy odcinek  Z3
        self.rura_rozg_z4 = Rura([self.split_point, (p_z4_in[0], self.split_point[1]), p_z4_in])  # do Z4
        self.rura_rozg_z5 = Rura([self.split_point, (p_z5_in[0], self.split_point[1]), p_z5_in])  # do Z5
        self.rury = [self.rura_z1_z2, self.rura_z2_z3, self.rura_z3_pion, self.rura_rozg_z4, self.rura_rozg_z5]  # Lista  rur

        # --- TIMER  ---
        self.timer = QTimer()  
        self.timer.timeout.connect(self.logika_przeplywu)  
        self.running = False  
        self.flow_speed = 0.5  # Prędkość przepływu cieczy
        
        # Przycisk START/STOP 
        self.btn = QPushButton("START", self)  
        self.btn.setGeometry(30, 600, 100, 30)  
        self.btn.setStyleSheet("background-color: #2e7d32; color: white; font-weight: bold; border: 1px solid white;")  
        self.btn.clicked.connect(self.przelacz_symulacje)  #  funkcja kliknięcia
        
        #  reszta interfejsu
        self.setup_manual_controls()
        self.setup_labels()
        self.setup_valve_control()
        self.setup_heater_control()
        self.aktualizuj_napisy_zbiornikow() 

    def setup_heater_control(self):  # Budowa przycisku grzałki
        self.btn_grzalka = QPushButton("GRZAŁKA: WYŁ.", self)
        self.btn_grzalka.setGeometry(740, 600, 130, 30)
        self.btn_grzalka.setStyleSheet("background-color: #333; color: gray; font-weight: bold; border: 2px solid gray;")
        self.btn_grzalka.clicked.connect(self.obsluga_przycisku_grzalki)

    def obsluga_przycisku_grzalki(self):  # Logika kliknięcia w przycisk grzałki
        self.grzalka_z5.przelacz()  
        if self.grzalka_z5.wlaczona:  # Jeśli włączona
            self.btn_grzalka.setText("GRZAŁKA: WŁ.")
            self.btn_grzalka.setStyleSheet("background-color: #333; color: #ff3333; font-weight: bold; border: 2px solid #ff3333;")
        else:  # Jeśli wyłączona 
            self.btn_grzalka.setText("GRZAŁKA: WYŁ.")
            self.btn_grzalka.setStyleSheet("background-color: #333; color: gray; font-weight: bold; border: 2px solid gray;")
        self.update()  # Wymuszenie odrysowania okna

    def setup_labels(self):  # Tworzenie etykiet (tekstów) nad przyciskami
        
        # Napisy nad przyciskami
        styl_przyciski = "color: white; font-size: 12px; font-weight: bold;"  
        self.lbl_btn_z1 = QLabel("Zbiornik 1", self)
        self.lbl_btn_z1.setStyleSheet(styl_przyciski); self.lbl_btn_z1.setAlignment(Qt.AlignCenter)
        self.lbl_btn_z1.resize(85, 20)
        self.lbl_btn_z1.move(150, 575) 

        self.lbl_btn_z2 = QLabel("Zbiornik 2", self)
        self.lbl_btn_z2.setStyleSheet(styl_przyciski); self.lbl_btn_z2.setAlignment(Qt.AlignCenter)
        self.lbl_btn_z2.resize(85, 20)
        self.lbl_btn_z2.move(250, 575) 

        self.lbl_btn_z3 = QLabel("Zbiornik 3", self)
        self.lbl_btn_z3.setStyleSheet(styl_przyciski); self.lbl_btn_z3.setAlignment(Qt.AlignCenter)
        self.lbl_btn_z3.resize(85, 20)
        self.lbl_btn_z3.move(350, 575) 

        self.lbl_btn_z5 = QLabel("Zbiornik 5", self)
        self.lbl_btn_z5.setStyleSheet(styl_przyciski); self.lbl_btn_z5.setAlignment(Qt.AlignCenter)
        self.lbl_btn_z5.resize(85, 20)
        self.lbl_btn_z5.move(550, 575) 

        self.lbl_btn_z4 = QLabel("Zbiornik 4", self)
        self.lbl_btn_z4.setStyleSheet(styl_przyciski); self.lbl_btn_z4.setAlignment(Qt.AlignCenter)
        self.lbl_btn_z4.resize(85, 20)
        self.lbl_btn_z4.move(450, 575) 

        # napisy nad zbiornikami
        styl_zbiorniki = "color: white; font-size: 14px; font-weight: bold;"
        self.lbl_tank_z1 = QLabel("Zbiornik 1", self) 
        self.lbl_tank_z1.setStyleSheet(styl_zbiorniki); 
        self.lbl_tank_z1.resize(150, 25)
        self.lbl_tank_z1.move(25, 20)  

        self.lbl_tank_z2 = QLabel("Zbiornik 2", self)
        self.lbl_tank_z2.setStyleSheet(styl_zbiorniki); 
        self.lbl_tank_z2.resize(150, 25)
        self.lbl_tank_z2.move(275, 20) 

        self.lbl_tank_z3 = QLabel("Zbiornik 3", self)
        self.lbl_tank_z3.setStyleSheet(styl_zbiorniki); 
        self.lbl_tank_z3.resize(150, 25)
        self.lbl_tank_z3.move(575, 170) 

        self.lbl_tank_z4 = QLabel("Zbiornik 4", self)
        self.lbl_tank_z4.setStyleSheet(styl_zbiorniki); 
        self.lbl_tank_z4.resize(150, 25)
        self.lbl_tank_z4.move(400, 335) 

        self.lbl_tank_z5 = QLabel("Zbiornik 5", self)
        self.lbl_tank_z5.setStyleSheet(styl_zbiorniki); 
        self.lbl_tank_z5.resize(150, 25)
        self.lbl_tank_z5.move(760, 335) 
        
        # Etykieta temperatury dla z5
        self.lbl_temp_z5 = QLabel("15.0°C", self)
        self.lbl_temp_z5.resize(100, 30)
        self.lbl_temp_z5.move(870, 450)

    def aktualizuj_napisy_zbiornikow(self):  # Funkcja odświeżająca teksty 
        pary = [(self.z1, self.lbl_tank_z1), (self.z2, self.lbl_tank_z2), (self.z3, self.lbl_tank_z3), (self.z4, self.lbl_tank_z4), (self.z5, self.lbl_tank_z5)]
        for z, label in pary:  
            val = round(z.aktualna_ilosc, 1)  # Zaokrąglenie ilości
            txt = f"{val:.0f}%" if val.is_integer() else f"{val:.1f}%"  # Formatowanie tekstu (usuwanie .0 jeśli liczba całkowita)
            label.setText(f"{z.nazwa} ({txt})")  #
            label.setAlignment(Qt.AlignLeft)

        temp = self.z5.temperatura  # Pobranie temp. z Z5
        self.lbl_temp_z5.setText(f"{temp:.1f}°C")  # Aktualizacja tekstu temperatury
        # Zmiana koloru tekstu w zależności od temperatury
        if temp < 30: kolor_txt = "blue"
        elif temp < 60: kolor_txt = "yellow"
        elif temp < 90: kolor_txt = "orange"
        else: kolor_txt = "red" 
        self.lbl_temp_z5.setStyleSheet(f"color: {kolor_txt}; font-size: 16px; font-weight: bold;")  

    def setup_manual_controls(self):  # Tworzenie przycisków "+" i "-" pod zbiornikami
        coords = [(150, 600), (250, 600), (350, 600), (550, 600), (450, 600)]  # Pozycje przycisków 
        for i, z in enumerate(self.zbiorniki):
            self.create_tank_buttons(z, coords[i][0], coords[i][1])  # Wywołanie funkcji tworzącej parę przycisków

    def create_tank_buttons(self, zbiornik, x, y):  # Tworzenie pary przycisków dla konkretnego zbiornika
        btn_fill = QPushButton("+", self) 
        btn_fill.setGeometry(x, y, 40, 30)
        btn_fill.setStyleSheet("background-color: #2e7d32; color: white;")
        btn_fill.clicked.connect(lambda: self.zmien_ilosc(zbiornik, 100))  # napełnianie na 100%
        
        btn_empty = QPushButton("-", self)  # Przycisk odejmowania
        btn_empty.setGeometry(x + 45, y, 40, 30)
        btn_empty.setStyleSheet("background-color: #c62828; color: white;")
        btn_empty.clicked.connect(lambda: self.zmien_ilosc(zbiornik, -100))  # usuwanie cieczy - 100%

    def setup_valve_control(self):  # Tworzenie przycisku sterowania zaworem
        self.btn_zawor = QPushButton(f"ZAWÓR: {self.opisy_zaworu[self.tryb_zaworu]}", self)
        self.btn_zawor.setGeometry(900, 600, 150, 30)
        kolor_hex = self.kolory_zaworu[0].name()
        self.btn_zawor.setStyleSheet(f"background-color: #333; color: {kolor_hex}; font-weight: bold; border: 2px solid gray;")
        self.btn_zawor.clicked.connect(self.zmien_tryb_zaworu)

    def zmien_tryb_zaworu(self):  #Przelaczanie trybu 0->1->2->3->0 itd
        self.tryb_zaworu = (self.tryb_zaworu + 1) % 4  
        opis = self.opisy_zaworu[self.tryb_zaworu]  # Pobranie  opisu
        kolor = self.kolory_zaworu[self.tryb_zaworu].name()  # Pobranie  koloru
        self.btn_zawor.setText(f"ZAWÓR: {opis}")  # Aktualizacja tekstu 
        self.btn_zawor.setStyleSheet(f"background-color: #333; color: {kolor}; font-weight: bold; border: 2px solid {kolor};")  
        self.update()  

    def zmien_ilosc(self, zbiornik, wartosc):  # Obsługa zmiany ilości cieczy
        if wartosc > 0: zbiornik.dodaj_ciecz(wartosc)  
        else: zbiornik.usun_ciecz(-wartosc)  
        self.aktualizuj_napisy_zbiornikow() 
        self.update()

    def przelacz_symulacje(self):  # Start/Stop Timera
        if self.running:  
            self.timer.stop()  
            self.running = False
            self.btn.setText("START")  
            self.btn.setStyleSheet("background-color: #2e7d32; color: white; font-weight: bold; border: 1px solid white;")
        else:  
            self.timer.start(25)  
            self.running = True
            self.btn.setText("STOP")
            self.btn.setStyleSheet("background-color: #c62828; color: white; font-weight: bold; border: 1px solid white;")

    def zapisz_raport_txt(self, decyzja):  # Zapisywanie logów do pliku
        teraz = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Pobranie obecnej daty 
        linijka = f"[{teraz}] ALARM: 90°C -> Decyzja: {decyzja}\n"  # Przygotowanie treści linii logu
        try:
            with open("historia_awarii.txt", "a", encoding="utf-8") as plik:  # Otwarcie pliku w trybie 'append' - dopisywanie
                plik.write(linijka)  
            print(f"Zapisano log: {decyzja}")  
        except Exception as e:
            print(f"Błąd zapisu: {e}")  

    # === FIZYKA: PRZEPŁYW I TEMPERATURA ===
    def logika_przeplywu(self):  # Funkcja wywoływana cyklicznie przez Timer
        
        wzrost_na_cykl = 0.5  # O ile rośnie temp. w cyklu
        spadek_na_cykl = 0.2  # O ile spada temp. w cyklu 
        
        # ---  GRZANIE / CHŁODZENIE ---
        if self.grzalka_z5.wlaczona:  
            if self.z5.temperatura < 100.0:  # Jeśli mniej niż wrzenie
                self.z5.temperatura += wzrost_na_cykl  
                if self.z5.temperatura > 100.0: self.z5.temperatura = 100.0  # max. temp: 100 C
        else: 
            if self.z5.temperatura > 15.0:  # Jeśli cieplejsza niż otoczenie
                self.z5.temperatura -= spadek_na_cykl  
                if self.z5.temperatura < 15.0: self.z5.temperatura = 15.0  # min. temp: 15 C

        # ---  LOGIKA RUR, PRZEPŁYWY ---
        margin = 1.5  
        poziom_rury = 50.0  # Wysokość, na ktorej rura między Z1 a Z2
        plynie_0 = False  # Flaga  Z1-Z2
        
        # Z1 i Z2  
        if self.z1.aktualna_ilosc > poziom_rury or self.z2.aktualna_ilosc > poziom_rury:  # Jeśli woda sięga rury
            roznica = self.z1.aktualna_ilosc - self.z2.aktualna_ilosc  # Oblicz różnicę poziomów
            if abs(roznica) < margin and abs(roznica) > 0:  
                srednia = (self.z1.aktualna_ilosc + self.z2.aktualna_ilosc) / 2.0 
                self.z1.ustaw_ilosc(srednia); self.z2.ustaw_ilosc(srednia)  # Wyrównaj poziomy 
                plynie_0 = True
            elif abs(roznica) >= margin:  
                ile = self.flow_speed  
                if roznica > 0 and not self.z2.czy_pelny():  # Jeśli Z1 > Z2 i Z2 ma miejsce
                    self.z2.dodaj_ciecz(self.z1.usun_ciecz(ile))  # Przelej z Z1 do Z2
                    plynie_0 = True
                elif roznica < 0 and not self.z1.czy_pelny():  # Jeśli Z2 > Z1 i Z1 ma miejsce
                    self.z1.dodaj_ciecz(self.z2.usun_ciecz(ile))  # Przelej z Z2 do Z1
                    plynie_0 = True
        self.rura_z1_z2.ustaw_przeplyw(plynie_0)  

        # Z2 i Z3
        plynie_1 = False
        if not self.z2.czy_pusty() and not self.z3.czy_pelny():  # Jeśli Z2 ma wodę i Z3 ma miejsce
            ilosc = self.z2.usun_ciecz(self.flow_speed)  # Zabierz z Z2
            faktycznie = self.z3.dodaj_ciecz(ilosc)  # Dodaj do Z3 
            if faktycznie < ilosc: self.z2.dodaj_ciecz(ilosc - faktycznie)  # Jeśli nie wszystko weszło, zwróć do Z2
            if faktycznie > 0: plynie_1 = True  
        self.rura_z2_z3.ustaw_przeplyw(plynie_1)

        #  Z3 -> Z4 i Z5
        plynie_z3_out, plynie_z5, plynie_z4 = False, False, False
        if self.z3.aktualna_ilosc > 0:  # Jeśli w Z3 jest woda
            if self.tryb_zaworu == 0:  # Tryb OBA 
                if not self.z5.czy_pelny() or not self.z4.czy_pelny():  # Jeśli gdziekolwiek jest miejsce
                    ilosc = self.z3.usun_ciecz(self.flow_speed)  # Zabierz wodę z Z3
                    polowa = ilosc / 2.0  # Podziel na pół
                    d5 = self.z5.dodaj_ciecz(polowa); d4 = self.z4.dodaj_ciecz(polowa)  # Wlej połowę do Z4 i Z5
                    reszta5 = polowa - d5; reszta4 = polowa - d4  # Sprawdzenie czy cos się nie zmieściło
                    if reszta5 > 0: d4 += self.z4.dodaj_ciecz(reszta5)  # Nadmiar z Z5 do Z4
                    if reszta4 > 0: d5 += self.z5.dodaj_ciecz(reszta4)  # Nadmiar z Z4 do Z5
                    razem = d5 + d4
                    if razem < ilosc: self.z3.dodaj_ciecz(ilosc - razem)  # Jeśli nie weszło, oddaj do Z3
                    if razem > 0: plynie_z3_out = True
                    if d5 > 0: plynie_z5 = True
                    if d4 > 0: plynie_z4 = True
            elif self.tryb_zaworu == 1:  # Tryb LEWO 
                if not self.z4.czy_pelny():
                    ilosc = self.z3.usun_ciecz(self.flow_speed)
                    d4 = self.z4.dodaj_ciecz(ilosc)
                    if d4 < ilosc: self.z3.dodaj_ciecz(ilosc - d4)
                    if d4 > 0: plynie_z3_out = True; plynie_z4 = True; plynie_z5 = False 
            elif self.tryb_zaworu == 2:  # Tryb PRAWO 
                if not self.z5.czy_pelny():
                    ilosc = self.z3.usun_ciecz(self.flow_speed)
                    d5 = self.z5.dodaj_ciecz(ilosc)
                    if d5 < ilosc: self.z3.dodaj_ciecz(ilosc - d5)
                    if d5 > 0: plynie_z3_out = True; plynie_z5 = True; plynie_z4 = False

        # Aktualizacja wyglądu rur
        self.rura_z3_pion.ustaw_przeplyw(plynie_z3_out)
        self.rura_rozg_z5.ustaw_przeplyw(plynie_z5)
        self.rura_rozg_z4.ustaw_przeplyw(plynie_z4)
        
        self.aktualizuj_napisy_zbiornikow()  # Odświeżenie etykiet
        self.update()  # Wymuszenie przerysowania ekranu

    
        # === ALARM ===

       
        if self.z5.temperatura > 90.0 and self.grzalka_z5.wlaczona and not self.alarm_juz_byl:
            
            self.alarm_juz_byl = True  # Ustawienie flagi, że alarm już wystąpił żeby okno nie wyskakiwało cały  czas
            
            # Okno alarm
            msg = QMessageBox()
            msg.setWindowTitle("ZAGROŻENIE!")
            msg.setText("Temperatura krytyczna: 90°C")
            msg.setInformativeText("Czy chcesz wyłączyć grzałkę?")
            msg.setIcon(QMessageBox.Critical)
            
            # przyciski w oknie
            btn_wylacz = msg.addButton("WYŁĄCZ GRZAŁKĘ", QMessageBox.DestructiveRole)
            btn_ignoruj = msg.addButton("IGNORUJ", QMessageBox.RejectRole)
            msg.exec_()  # pauza programu i czekanie na wybor opcji
            
            # decyzja
            if msg.clickedButton() == btn_wylacz:
                self.grzalka_z5.przelacz()  # Wyłącz grzałkę
                self.btn_grzalka.setText("GRZAŁKA: WYŁĄCZONA")
                self.btn_grzalka.setStyleSheet("background-color: #333; color: gray; border: 2px solid gray;")
                self.zapisz_raport_txt("WYŁĄCZONO GRZAŁKĘ")
            else:
                self.zapisz_raport_txt("ZIGNOROWANO OSTRZEŻENIE")

        # Reset blokady alarmu dopiero gdy temperatura spadnie do 80
        if self.z5.temperatura < 80.0:
            self.alarm_juz_byl = False

    def draw_valve(self, painter):  #  symbol zaworu
        sx, sy = self.split_point  # Pwsp. środka
        r = 15  # Promień kółka
        kolor = self.kolory_zaworu[self.tryb_zaworu]  # Kolor  trybu
        
        # Rysowanie tła kółka
        painter.setPen(QPen(Qt.white, 2))
        painter.setBrush(QBrush(QColor(40, 40, 40)))
        painter.drawEllipse(QPointF(sx, sy), r, r)
        
        # Rysowanie symbolu w środku dla danego trybu
        painter.setBrush(QBrush(kolor))
        painter.setPen(Qt.NoPen)
        if self.tryb_zaworu == 0:  # Koło
            painter.drawEllipse(QPointF(sx, sy), r-4, r-4)
        elif self.tryb_zaworu == 1:  # Strzałka w lewo
            path = QPainterPath()
            path.moveTo(sx + 5, sy - 8); path.lineTo(sx + 5, sy + 8); path.lineTo(sx - 8, sy)
            painter.drawPath(path)
        elif self.tryb_zaworu == 2:  # Strzałka w prawo
            path = QPainterPath()
            path.moveTo(sx - 5, sy - 8); path.lineTo(sx - 5, sy + 8); path.lineTo(sx + 8, sy)
            painter.drawPath(path)
        elif self.tryb_zaworu == 3:  # Kwadrat 
            painter.drawRect(int(sx - 6), int(sy - 6), 12, 12)

    def paintEvent(self, event):  # Główna funkcja rysująca 
        p = QPainter(self)  # Utworzenie obiektu malarza 
        p.setRenderHint(QPainter.Antialiasing)  # Wygładzanie krawędzi
        for r in self.rury: r.draw(p)  # Narysuj  rury
        for z in self.zbiorniki: z.draw(p)  # Narysuj  zbiorniki
        self.grzalka_z5.draw(p)  # Narysuj grzałkę
        self.draw_valve(p)  # Narysuj zawór

# Blok uruchamiający aplikację
if __name__ == '__main__':
    app = QApplication(sys.argv)  
    okno = SymulacjaKaskady()  
    okno.show()  
    sys.exit(app.exec())  