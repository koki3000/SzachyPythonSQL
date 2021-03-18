import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://postgres:12345@localhost:5432/postgres")
#engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

class bierka:
    def __init__(self,typ):
        self.typ = typ

    def ruch(self):
        pass

class pion(bierka):
    def ruch(self):
        print("Ktora bierke chcesz ruszyc?")
        start = input()
        pole = db.execute("SELECT " + start[slice(1)] +" FROM szachownica where id=:i;",{"i": start[slice(1,2)]}).fetchone()
        x = (ord(start[slice(1)])-1)%8
        y = int(start[slice(1,2)])

        if ('Pion' in pole[0]):
            wspolzedne = (y-1)*8+x
            szachownica [wspolzedne+8] = "x"
            szachownica [wspolzedne+16] = "x"
            db.execute("update szachownica set " + start[slice(1)] +"='x' where id=:i OR id=:j;",{"i": y+1, "j": y+2})
        else:
            print ("Na tym polu nie ma piona")

        """
        db.execute("update szachownica set " + start[slice(1)] +"='' where id=:i;",{"i": start[slice(1,2)]})
        
        print("Dokad chcesz ruszyc?")
        koniec = input()
        pole = db.execute("SELECT a FROM szachownica where id=:i;",{"i": koniec[slice(1,2)]}).fetchall()
        if (pole[0].a == ''):                                                                                                       # wymaga zmian
            db.execute("update szachownica set " + koniec[slice(1)] +"='Pion' where id=:i;",{"i": koniec[slice(1,2)]})
        else:
            print ("pole jest zajete")
        """

        db.commit()

bierki = ["Wieza","Konik","Goniec","Hetman","Krol","Goniec","Konik","Wieza","Pion"]
szachownica = []
for j in range (4):
    for i in range (16):
        if (i < 8):
            if (j==0):
                szachownica.append("c" + bierki[i])
            elif (j==3):
                szachownica.append("b" + bierki[8])
            else:
                szachownica.append("")
        if (i >= 8):
            if (j==0):
                szachownica.append("c" + bierki[8])
            elif (j==3):
                szachownica.append("b" + bierki[i%8])
            else:
                szachownica.append("")

kolumny = ['a',"b","c","d","e","f","g","h"]

def main():
    """
    flights = db.execute("SELECT origin, destination, duration FROM flights").fetchall()
    for flight in flights:
        print(f"{flight.origin} to {flight.destination}, {flight.duration} minutes.")
    """
    
    #db.execute("DELETE FROM szachownica;")

    for i in range(8):
        #for litera in kolumny:
        #db.execute("insert into szachownica (a,b,c,d,e,f,g,h) values (:a,:b,:c,:d,:e,:f,:g,:h);",
        db.execute("update szachownica set a=:a, b=:b, c=:c, d=:d, e=:e, f=:f, g=:g, h=:h where id=:i;",
        {"a": szachownica[8*i],"b": szachownica[8*i+1],"c": szachownica[8*i+2],"d": szachownica[8*i+3],
        "e": szachownica[8*i+4],"f": szachownica[8*i+5],"g": szachownica[8*i+6],"h": szachownica[8*i+7], "i": i+1})

    print ("dodano")
    db.commit()
if __name__ == "__main__":
    main()

pion1 = pion(bierki[8])
pion1.ruch()


