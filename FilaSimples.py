import CongruenteLinear

congruente = CongruenteLinear.CongruenteLinear(75,2**16 + 1,153,74,True)
# print(congruente.geraAleatorio())


class FilaAtendimento():
    def __init__(self, nomeFila: str ,quantidadeServidores: int ,tamanhoFilaMax:int, chegadaTimeBounds, saidaTimeBounds ):
        self.nomeFila = nomeFila
        self.quantidadeServidores = quantidadeServidores
        self.tamanhoFilaMax = tamanhoFilaMax
        self.chegadaLowerBound = float(chegadaTimeBounds[0])
        self.chegadaUpperBound = float(chegadaTimeBounds[1])
        self.saidaLowerBound = float(saidaTimeBounds[0])
        self.saidaUpperBound = float(saidaTimeBounds[1])
        self.currentFilaSize = 0


    def getRandomSaidaTime(self, current: float)-> float:
        random = self.getRandom(self.saidaLowerBound, self.saidaUpperBound)
        result = current + random
        return result

    def getRandomChegadaTime(self, current: float)-> float:
        global congruente
        
        randomResult = self.getRandom(self.chegadaLowerBound, self.chegadaUpperBound)
        result = current + randomResult
        #print(type(current))
        #print("current: "+ current + " randomResult: "+ randomResult + "result: "+ result)
        return result

    def getRandom(self, lower: float, upper: float) -> float :
        global congruente
        random = float(congruente.geraAleatorio())
        u = (upper - lower)*random  + lower
        return u

class Event():
     def __init__(self, fila: FilaAtendimento ,type: str, time: float):
        self.fila = fila
        self.type = type
        self.time = time

     def __str__(self) -> str:
        return "tempo: "+ str(self.time) + ", tipo: "+  self.type


eventQueue = []
def addToQueue(event: Event):
    global eventQueue
    def keyFunc(e):
        return e.time
    eventQueue.append(event)
    eventQueue.sort(key=keyFunc, reverse=True)

historicoDeEventos = []
contEventosEscalonados = 0
limite = 7 - 2

# Mark: algoritmo aqui

def Chegada(fila: FilaAtendimento, currentTime: float):
    # contabiliza tempo
    global historicoDeEventos
    historicoDeEventos.append("Chegada na fila: " + fila.nomeFila+ ", Tempo: "+ str(currentTime))
    if fila.currentFilaSize < fila.tamanhoFilaMax:
        fila.currentFilaSize += 1
        if fila.quantidadeServidores >= fila.currentFilaSize:
            # agenda saida
            agendaSaida(fila, fila.getRandomSaidaTime(currentTime))
    agendaChegada(fila,fila.getRandomChegadaTime(currentTime))

def Saida(fila: FilaAtendimento, currentTime: float):
    global historicoDeEventos
    historicoDeEventos.append("Saida da fila: " + fila.nomeFila+ ", Tempo: "+ str(currentTime))
    fila.currentFilaSize -= 1
    if fila.currentFilaSize > 0: # >= 1
        agendaSaida(fila, fila.getRandomSaidaTime(currentTime))

def agendaChegada(fila: FilaAtendimento, futureTime: float):
    global contEventosEscalonados
    global limite
    if contEventosEscalonados < limite:
        contEventosEscalonados += 1
        addToQueue(Event(fila, "C", futureTime))

def agendaSaida(fila: FilaAtendimento, futureTime: float):
    global contEventosEscalonados
    global limite
    if contEventosEscalonados < limite:
        contEventosEscalonados += 1    
        addToQueue(Event(fila, "S", futureTime))

addToQueue(Event(FilaAtendimento("fila do Hojin",1,3,[1,2],[3,6]), "C", 2.0))
while len(eventQueue) > 0:
    for i in eventQueue:
        print(i)
    print("---")

    nextEvent = eventQueue.pop()
    #nextEvent = nextEvent
    if nextEvent.type == "C":
        Chegada(nextEvent.fila, nextEvent.time)
    elif nextEvent.type == "S" :
        Saida(nextEvent.fila, nextEvent.time)

for i in historicoDeEventos:
    print(i)

print("end")