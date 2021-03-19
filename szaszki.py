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

        if ('Pion' in pole[0]):
            if ('c' in pole[0]):
                wspolzedne = (y-1)*8+x
                szachownica [wspolzedne+8] = "x"
                szachownica [wspolzedne+16] = "x"
                db.execute("update szachownica set " + start[slice(1)] +"='x' where id=:i OR id=:j;",{"i": y+1, "j": y+2})
            else:
                wspolzedne = (y-1)*8+x
                szachownica [wspolzedne-8] = "x"
                szachownica [wspolzedne-16] = "x"
                db.execute("update szachownica set " + start[slice(1)] +"='x' where id=:i OR id=:j;",{"i": y-1, "j": y-2})
        else:
            print ("Na tym polu nie ma piona")
        db.commit()

        print("Dokad chcesz ruszyc?")
        koniec = input()
        pole = db.execute("SELECT " + koniec[slice(1)] +" FROM szachownica where id=:i;",{"i": koniec[slice(1,2)]}).fetchone()
        if (pole[0] == 'x'):                                                                                                       # wymaga zmian
            db.execute("update szachownica set " + start[slice(1)] +"='' where id=:i;",{"i": start[slice(1,2)]})
            db.execute("update szachownica set " + koniec[slice(1)] +"=:bierka where id=:i;",{"i": koniec[slice(1,2)],"bierka": szachownica[wspolzedne].tekst})
            db.execute("update szachownica set " + start[slice(1)] +"='' where " + start[slice(1)] +"='x';",{"i": koniec[slice(1,2)]})
        else:
            print ("pole jest zajete")

        db.commit()

class bierka:
    def __init__(self,typ,kolor):
        self.typ = typ
        self.kolor = kolor
        self.tekst = kolor+typ
        
    def ruch(self):
        pass

class wieza(bierka):
    def __init__ (self,kolor):
        super().__init__(typ="Wieza", kolor = kolor)

    def ruch(self):
        pass

class konik(bierka):
    def __init__ (self,kolor):
        super().__init__(typ="Konik", kolor = kolor)

    def ruch(self):
        pass

class laufer(bierka):
    def __init__ (self,kolor):
        super().__init__(typ="Laufer", kolor = kolor)
        
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
    
    def ruch(self):
        pass

czarny = "c"
bialy = "b"
czarneFigury = [wieza(czarny), konik(czarny), laufer(czarny), hetman(czarny), krol(czarny), laufer(czarny), konik(czarny), wieza(czarny)]
bialeFigury = [wieza(bialy), konik(bialy), laufer(bialy), hetman(bialy), krol(bialy), laufer(bialy), konik(bialy), wieza(bialy)]
szachownica = []
for j in range (4):
    for i in range (16):
        if (i < 8):
            if (j==0):
                szachownica.append(czarneFigury[i])
            elif (j==3):
                szachownica.append(pion("b"))
            else:
                szachownica.append("")
        if (i >= 8):
            if (j==0):
                szachownica.append(pion("c"))
            elif (j==3):
                szachownica.append(bialeFigury[i%8])
            else:
                szachownica.append("")

def main():


    for i in range(8):
        if (i in (0,1,6,7)):
            db.execute("update szachownica set a=:a, b=:b, c=:c, d=:d, e=:e, f=:f, g=:g, h=:h where id=:i;",
            {"a": szachownica[8*i].tekst,"b": szachownica[8*i+1].tekst,"c": szachownica[8*i+2].tekst,"d": szachownica[8*i+3].tekst,
            "e": szachownica[8*i+4].tekst,"f": szachownica[8*i+5].tekst,"g": szachownica[8*i+6].tekst,"h": szachownica[8*i+7].tekst, "i": i+1})
        else:
            db.execute("update szachownica set a=:a, b=:b, c=:c, d=:d, e=:e, f=:f, g=:g, h=:h where id=:i;",
            {"a": szachownica[8*i],"b": szachownica[8*i+1],"c": szachownica[8*i+2],"d": szachownica[8*i+3],
            "e": szachownica[8*i+4],"f": szachownica[8*i+5],"g": szachownica[8*i+6],"h": szachownica[8*i+7], "i": i+1})

    print ("dodano")
    db.commit()
if __name__ == "__main__":
    main()

wybor()