class Nodo:
    def __init__(self, nome):
        self.nome = nome
        # Tavola di routing: {destinazione: (distanza, next_hop)}
        self.tavola_routing = {nome: (0, nome)}
        self.vicini = {}  # Distanze verso i vicini

    def aggiungi_vicino(self, vicino, distanza):
        self.vicini[vicino] = distanza
        self.tavola_routing[vicino.nome] = (distanza, vicino.nome)  # Inizializza il next hop al vicino stesso

    def invia_aggiornamenti(self):
        # Invia la tavola di routing ai vicini
        aggiornato = False
        for vicino in self.vicini:
            if vicino.ricevi_aggiornamento(self.nome, self.tavola_routing):
                aggiornato = True
        return aggiornato

    def ricevi_aggiornamento(self, nodo_vicino, tavola_vicino):
        aggiornato = False
        distanza_vicino = self.tavola_routing[nodo_vicino][0]  # Distanza attuale verso il vicino
        
        # Aggiorna la tavola di routing in base alla tavola ricevuta dal vicino
        for destinazione, (distanza, next_hop) in tavola_vicino.items():
            nuova_distanza = distanza_vicino + distanza
            if (destinazione not in self.tavola_routing or
                nuova_distanza < self.tavola_routing[destinazione][0]):
                # Aggiorna distanza e next hop
                self.tavola_routing[destinazione] = (nuova_distanza, nodo_vicino)
                aggiornato = True

        return aggiornato

    def stampa_tavola_routing(self):
        print(f"Tavola di routing per {self.nome}:")
        for destinazione, (distanza, next_hop) in self.tavola_routing.items():
            print(f"  {destinazione}: {distanza}, Next hop: {next_hop}")
        print("\n")


# Creazione dei nodi
a = Nodo("A")
b = Nodo("B")
c = Nodo("C")
d = Nodo("D")

# Definizione dei vicini (grafo della rete)
a.aggiungi_vicino(b, 1)
a.aggiungi_vicino(c, 4)
b.aggiungi_vicino(a, 1)
b.aggiungi_vicino(c, 2)
b.aggiungi_vicino(d, 5)
c.aggiungi_vicino(a, 4)
c.aggiungi_vicino(b, 2)
c.aggiungi_vicino(d, 1)
d.aggiungi_vicino(b, 5)
d.aggiungi_vicino(c, 1)

# Simulazione del processo di aggiornamento delle rotte
convergente = False
while not convergente:
    convergente = True
    for nodo in [a, b, c, d]:
        if nodo.invia_aggiornamenti():
            convergente = False

# Stampa delle tabelle di routing finali
for nodo in [a, b, c, d]:
    nodo.stampa_tavola_routing()
