import csv

class Stand:
    def __init__(self, codice, superficie, padiglione, prezzo_base): #stand generale
        self.codice = codice
        self.superficie = superficie
        self.padiglione = padiglione
        self.prezzo_base = prezzo_base

        self.disponibile = True
        self.assegnatario = None

    def __str__(self):
        return f"Codice stand: {self.codice} | Superficie: {self.superficie} mq, Padiglione: {self.padiglione}, Prezzo: {self.prezzo_base}"

    def prezzo_finale(self):
        return self.prezzo_base

    def __lt__(self, other):
        return self.prezzo_finale() < other.prezzo_finale() #confronta i due stand in base al prezzo
                                                            # è una regola di confronto
#devo mettere le parentesi tonde finali perchè sta chiamando due metodi (funzioni che restituiscono prezzo_finale)

class StandPreseExtra(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, prese_extra):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.prese_extra = prese_extra

    def prezzo_finale(self):
        return self.prezzo_base * (1 + 0.07 * self.prese_extra)

    def __str__(self):
        return f"{super().__str__()}, Numero prese extra: {self.prese_extra}, Prezzo finale: {self.prezzo_finale()}"


class PremiumStand(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, posizione):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.posizione = posizione

    def prezzo_finale(self):
        return self.prezzo_base * 1.30

    def __str__(self):
        return f"{super().__str__()}, Posizione: {self.posizione}, Prezzo finale: {self.prezzo_finale()}"


class Espositore:
    def __init__(self, codice, nome, cognome):
        self.codice = codice
        self.nome = nome
        self.cognome = cognome

    def __str__(self):
        return f"Codice espositore: {self.codice} | Nome: {self.nome} Cognome: {self.cognome}"

    def __eq__(self, other):
        return self.codice == other.codice
#non devo mettere le parentesi tonde perchè sto confrontando degli attributi


class LingottoFiere:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        self._nome = nome
        self.stands = []
        self.espositori = []

    """Aggiungere setter e getter se necessari"""
    @property
    def nome(self):              #per leggere il nome della fiera
        return self._nome
    @nome.setter
    def nome(self, nuovo_nome):  #per modificare il nome della fiera
        self._nome = nuovo_nome

    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        self.stands = []
        self.espositori = []

        try:
            file = open(file_path, "r", encoding = "utf-8")
            righe = csv.reader(file)
            for riga in righe:
                codice = riga[0]
                if len(riga) == 3:
                    nome = riga[1]
                    cognome = riga[2]
                    nuovo_espositore = Espositore(codice, nome, cognome)
                    self.espositori.append(nuovo_espositore)
                elif len(riga) == 4:
                    superficie = int(riga[1])
                    padiglione = int(riga[2])
                    prezzo_base = int(riga[3])
                    nuovo_stand = Stand(codice, superficie, padiglione, prezzo_base)
                    self.stands.append(nuovo_stand)
                elif len(riga) == 5:
                    superficie = int(riga[1])
                    padiglione = int(riga[2])
                    prezzo_base = int(riga[3])
                    if riga[4].isdigit():
                        prese_extra = int(riga[4])
                        nuovo_stand = StandPreseExtra(codice, superficie, padiglione, prezzo_base, prese_extra)
                        self.stands.append(nuovo_stand)
                    else:
                        posizione = riga[4]
                        nuovo_stand = PremiumStand(codice, superficie, padiglione, prezzo_base, posizione)
                        self.stands.append(nuovo_stand)
            file.close()
            return self.stands, self.espositori

        except FileNotFoundError:
            print("Attenzione, file non trovato!")
            return None


    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""

        #controllo che esista lo stand nella lista
        stand_trovato = None
        for stand in self.stands:
            if stand.codice == codice_stand:
                stand_trovato = stand
        if stand_trovato is None:
            raise ValueError("Stand non trovato!")

        #controllo che esista l'espositore nella lista
        espositore_trovato = None
        for espositore in self.espositori:
            if espositore.codice == codice_espositore:
                espositore_trovato = espositore
        if espositore_trovato is None:
            raise ValueError("Espositore non trovato!")

        #una volta che ho controllato l'esistenza dello stand, contollo se è disponibile
        if not stand_trovato.disponibile: #controlla se lo stand è occupato (not True = False)
            raise ValueError("Lo stand non è disponibile.")

        #ora controllo se lo stand è già stato assegnato a qualcuno
        for stand in self.stands:
            if stand.assegnatario == espositore_trovato:
                raise ValueError("L'espositore ha già uno stand assegnato.")

        #infine glielo posso assegnare
        stand_trovato.disponibile = False
        stand_trovato.assegnatario = espositore_trovato

    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        #passare in rassegna tutti gli stand per ogni singola persona
        for espositore in self.espositori:
            stand_trovato = None
            for stand in self.stands:
                if stand.assegnatario == espositore:
                    stand_trovato = stand
            if stand_trovato is None:
                print(f"Espositore: {espositore}, nessuno stand assegnato.")
            else:
                print(f"Espositore: {espositore}, stand assegnato: {stand_trovato.codice}")

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        stands_ordinati = sorted(self.stands)  #prima di definire la funzione __lt__ python non sapeva come
                                               # ordinare gli stand, dopo averla definita sa che deve farlo in base al prezzo finale
        return stands_ordinati
