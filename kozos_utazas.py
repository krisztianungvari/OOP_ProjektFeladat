from abc import ABC, abstractmethod
from datetime import datetime

# 1. Absztrakt alaposztály
class Jarat(ABC):
    def __init__(self, jaratszam, celallomas, jegyar):
        self._jaratszam = jaratszam
        self._celallomas = celallomas
        self._jegyar = jegyar

    @property
    def jaratszam(self):
        return self._jaratszam

    @property
    def jegyar(self):
        return self._jegyar

# 2. Származtatott osztályok
class BelföldiJarat(Jarat):
    def __init__(self, jaratszam, celallomas, jegyar):
        super().__init__(jaratszam, celallomas, jegyar)
        self.tipus = "Belföldi"

class NemzetkoziJarat(Jarat):
    def __init__(self, jaratszam, celallomas, jegyar):
        super().__init__(jaratszam, celallomas, jegyar)
        self.tipus = "Nemzetközi"

# 3. Légitársaság
class Legitarsasag:
    def __init__(self, nev):
        self.nev = nev
        self.jaratok = []

    def jarat_hozzaadas(self, jarat):
        self.jaratok.append(jarat)

# 4. JegyFoglalás
class JegyFoglalas:
    def __init__(self, jarat, utas_nev, datum):
        self.jarat = jarat
        self.utas_nev = utas_nev
        self.datum = datum

# 5. Foglalási Rendszer logikája
class FoglalasiRendszer:
    def __init__(self, legitarsasag):
        self.legitarsasag = legitarsasag
        self.foglalasok = []

    def foglalas(self, jaratszam, nev, datum_str):
        try:
            foglalas_datuma = datetime.strptime(datum_str, "%Y-%m-%d")
            if foglalas_datuma < datetime.now():
                return "Hiba: Csak jövőbeli időpontra lehet foglalni!"
            
            for jarat in self.legitarsasag.jaratok:
                if jarat.jaratszam == jaratszam:
                    uj_foglalas = JegyFoglalas(jarat, nev, datum_str)
                    self.foglalasok.append(uj_foglalas)
                    return f"Sikeres foglalás! Utas: {nev}, Ár: {jarat.jegyar} Ft"
            
            return "Hiba: A megadott járatszám nem létezik!"
        except ValueError:
            return "Hiba: Érvénytelen dátum formátum! Használd: ÉÉÉÉ-HH-NN"

    def lemondas(self, nev, jaratszam):
        for f in self.foglalasok:
            if f.utas_nev == nev and f.jarat.jaratszam == jaratszam:
                self.foglalasok.remove(f)
                return f"Siker: {nev} foglalása törölve."
        return "Hiba: Nincs ilyen foglalás!"

    def elerheto_jaratok_listazasa(self):
        print("\n--- Elérhető Járatok ---")
        for j in self.legitarsasag.jaratok:
            print(f"Járatszám: {j.jaratszam} | Cél: {j._celallomas} | Ár: {j.jegyar} Ft | Típus: {j.tipus}")

    def foglalasok_listazasa(self):
        if not self.foglalasok:
            print("\nNincsenek aktív foglalások.")
            return
        print("\n--- Aktuális Foglalások ---")
        for f in self.foglalasok:
            print(f"Utas: {f.utas_nev} | Járat: {f.jarat.jaratszam} | Cél: {f.jarat._celallomas} | Dátum: {f.datum}")

# --- Inicializálás ---
kozos_utazas = Legitarsasag("KözösUtazás")
kozos_utazas.jarat_hozzaadas(BelföldiJarat("HU101", "Debrecen", 12500))
kozos_utazas.jarat_hozzaadas(BelföldiJarat("HU102", "Szeged", 11000))
kozos_utazas.jarat_hozzaadas(NemzetkoziJarat("INT503", "Barcelona", 52000))
kozos_utazas.jarat_hozzaadas(NemzetkoziJarat("INT504", "London", 45000))

rendszer = FoglalasiRendszer(kozos_utazas)

# 6 alapfoglalás (Dátum: jövőbeli)
alap_nevek = ["Krisz", "Anna", "Péter", "Kata", "Gábor", "Heni"]
for i, nev in enumerate(alap_nevek):
    jszam = "HU101" if i % 2 == 0 else "INT503"
    rendszer.foglalas(jszam, nev, "2026-06-15")

# --- Felhasználói Interfész ---
def interface():
    while True:
        print(f"\n===== {kozos_utazas.nev} Menü =====")
        print("1. Elérhető járatok megtekintése") 
        print("2. Jegy foglalása")
        print("3. Foglalás lemondása")
        print("4. Foglalások listázása")
        print("5. Kilépés")
        
        valasztas = input("\nVálassz (1-5): ")
        
        try:
            if valasztas == "1":
                rendszer.elerheto_jaratok_listazasa()
            elif valasztas == "2":
                jszam = input("Járatszám: ")
                nev = input("Utas neve: ")
                datum = input("Dátum (ÉÉÉÉ-HH-NN): ")
                print(rendszer.foglalas(jszam, nev, datum))
            elif valasztas == "3":
                nev = input("Név: ")
                jszam = input("Járatszám: ")
                print(rendszer.lemondas(nev, jszam))
            elif valasztas == "4":
                rendszer.foglalasok_listazasa()
            elif valasztas == "5":
                print(f"Viszlát, jó utat!")
                break
            else:
                print("Hiba: Kérlek 1 és 5 közötti számot adj meg!")
        except Exception as e:
            print(f"Hiba: {e}")

if __name__ == "__main__":
    interface()