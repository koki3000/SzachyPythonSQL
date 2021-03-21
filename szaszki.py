import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://postgres:12345@localhost:5432/postgres")
#engine = create_engine(os.getenv("DATABASE_URL")) # korzystajac z tego rozwiazania nalezy w terminalu ustawic DATABASE_URL, dla windows "set DATABASE_URL=postgres://postgres:12345@localhost:5432/postgres"
db = scoped_session(sessionmaker(bind=engine))

def wybor():
        print("Ktora bierke chcesz ruszyc?")
        start = input()
        pole = db.execute("SELECT " + start[slice(1)] +" FROM szachownica where id=:i;",{"i": start[slice(1,2)]}).fetchone()
        x = (ord(start[slice(1)])-1)%8
        y = int(start[slice(1,2)])
        wspolrzedneStart = (y-1)*8+x
        szachownica[wspolrzedneStart].ruch(x,y,start) 

        print("Dokad chcesz ruszyc?")
        koniec = input()
        x = (ord(koniec[slice(1)])-1)%8
        y = int(koniec[slice(1,2)])
        wspolrzedneKoniec = (y-1)*8+x
        pole = db.execute("SELECT " + koniec[slice(1)] +" FROM szachownica where id=:i;",{"i": koniec[slice(1,2)]}).fetchone()
        if ('x' in pole[0]):                                                                                                       # wymaga zmian
            db.execute("update szachownica set " + start[slice(1)] +"='' where id=:i;",{"i": start[slice(1,2)]})
            db.execute("update szachownica set " + koniec[slice(1)] +"=:bierka where id=:i;",{"i": koniec[slice(1,2)],"bierka": szachownica[wspolrzedneStart].tekst})
            db.execute("update szachownica set " + start[slice(1)] +"='' where " + start[slice(1)] +"='x';",{"i": koniec[slice(1,2)]})
            
            bufor = szachownica[wspolrzedneStart]
            szachownica[wspolrzedneStart] = pustePole()
            szachownica[wspolrzedneKoniec] = bufor
        else:
            print ("pole nieprawidlowe")

        db.commit()

class bierka:
    def __init__(self,typ,kolor):
        self.typ = typ
        self.kolor = kolor
        self.tekst = kolor+typ
        
    def ruch(self,x,y):
        pass

class wieza(bierka):
    def __init__ (self,kolor):
        super().__init__(typ="Wieza", kolor = kolor)

    def ruch(self,x,y,start):
        print (f"wybrales figure: {self.tekst}")
        i=0
        while (szachownica[(y+i)*8+x].tekst == "" and (y+1+i)<=8):
            db.execute("update szachownica set " + start[slice(1)] +"='x' where id=:i;",{"i": y+i+1})
            i += 1
        i=0
        while (szachownica[(y-2-i)*8+x].tekst == "" and (y-1-i)>=0):
            db.execute("update szachownica set " + start[slice(1)] +"='x' where id=:i;",{"i": y-1-i})
            i += 1
        i=0
        while (szachownica[(y-1)*8+x+1+i].tekst == "" and (x+1+i)<=7):
            db.execute("update szachownica set " + chr(ord(start[slice(1)])+1+i) +"='x' where id=:i;",{"i": y})
            i += 1
        i=0
        while (szachownica[(y-1)*8+x-1-i].tekst == "" and (x-1-i)>=0):
            db.execute("update szachownica set " + chr(ord(start[slice(1)])-1-i) +"='x' where id=:i;",{"i": y})
            i += 1

        db.commit()

class konik(bierka):
    def __init__ (self,kolor):
        super().__init__(typ="Konik", kolor = kolor)

    def ruch(self):
        pass

class goniec(bierka):
    def __init__ (self,kolor):
        super().__init__(typ="Goniec", kolor = kolor)
        
    def ruch(self):
        pass

class hetman(bierka):
    def __init__ (self,kolor):
        super().__init__(typ="Hetman", kolor = kolor)
    
    def ruch(self):
        pass

class krol(bierka):
    def __init__ (self,kolor):
        super().__init__(typ="Krol", kolor = kolor)
    
    def ruch(self):
        pass

class pion(bierka):
    def __init__ (self,kolor):
        super().__init__(typ="Pion", kolor = kolor)
    
    def ruch(self,x,y,start):
        print (f"wybrales figure: {self.tekst}")        
        if (self.kolor == "c"):
            if (y == 2):
                for i in range (2):
                    if (szachownica[(y+i)*8+x].tekst == ""):
                        db.execute("update szachownica set " + start[slice(1)] +"='x' where id=:i;",{"i": y+i+1})
            else:
                if (szachownica[y*8+x].tekst == ""):
                    db.execute("update szachownica set " + start[slice(1)] +"='x' where id=:i;",{"i": y+1})
            if (szachownica[y*8+(x+1)].kolor == "b" and x < 7):
                db.execute("update szachownica set " + chr(ord(start[slice(1)])+1) +"='" + ("x/" + szachownica[y*8+(x+1)].tekst) +"' where id=:i;",{"i": y+1})
            if (szachownica[y*8+(x-1)].kolor == "b" and x > 0):
                db.execute("update szachownica set " + chr(ord(start[slice(1)])-1) +"='" + ("x/" + szachownica[y*8+(x-1)].tekst) +"' where id=:i;",{"i": y+1})
        
        elif (self.kolor == "b"):
            if (y == 7):
                for i in range (2):
                    if (szachownica[(y-2-i)*8+x].tekst == ""):
                        db.execute("update szachownica set " + start[slice(1)] +"='x' where id=:i;",{"i": y-i-1})
            else:
                if (szachownica[(y-2)*8+x].tekst == ""):
                    db.execute("update szachownica set " + start[slice(1)] +"='x' where id=:i;",{"i": y-1})
            if (szachownica[(y-2)*8+(x+1)].kolor == "c" and x < 7):
                db.execute("update szachownica set " + chr(ord(start[slice(1)])+1) +"='" + ("x/" + szachownica[(y-2)*8+(x+1)].tekst) +"' where id=:i;",{"i": y-1})
            if (szachownica[(y-2)*8+(x-1)].kolor == "c" and x > 0):
                db.execute("update szachownica set " + chr(ord(start[slice(1)])-1) +"='" + ("x/" + szachownica[(y-2)*8+(x-1)].tekst) +"' where id=:i;",{"i": y-1})
        db.commit()

class pustePole:
    def __init__(self):
        self.tekst = ""
        self.kolor = ""

czarny = "c"
bialy = "b"
czarneFigury = [wieza(czarny), konik(czarny), goniec(czarny), hetman(czarny), krol(czarny), goniec(czarny), konik(czarny), wieza(czarny)]
bialeFigury = [wieza(bialy), konik(bialy), goniec(bialy), hetman(bialy), krol(bialy), goniec(bialy), konik(bialy), wieza(bialy)]
szachownica = []
for j in range (4):
    for i in range (16):
        if (i < 8):
            if (j==0):
                szachownica.append(czarneFigury[i])
            elif (j==3):
                szachownica.append(pion("b"))
            else:
                szachownica.append(pustePole())
        if (i >= 8):
            if (j==0):
                szachownica.append(pion("c"))
            elif (j==3):
                szachownica.append(bialeFigury[i%8])
            else:
                szachownica.append(pustePole())

def main():
    for i in range(8):
        #if (i in (0,1,6,7)):
            db.execute("update szachownica set a=:a, b=:b, c=:c, d=:d, e=:e, f=:f, g=:g, h=:h where id=:i;",
            {"a": szachownica[8*i].tekst,"b": szachownica[8*i+1].tekst,"c": szachownica[8*i+2].tekst,"d": szachownica[8*i+3].tekst,
            "e": szachownica[8*i+4].tekst,"f": szachownica[8*i+5].tekst,"g": szachownica[8*i+6].tekst,"h": szachownica[8*i+7].tekst, "i": i+1})
    print ("dodano")
    db.commit()


    db.execute("update szachownica set d='x' where id=4;")
    db.commit()
    wybor()
    wybor()
    wybor()



if __name__ == "__main__":
    main()
