#Heitor, Hojin, Gustavo

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
        self.tableOfTimes = [0] * (self.tamanhoFilaMax+1)
        self.lastTime = 0

    def increaseCurrentFilaSize(self, currentTime: float):
        deltaTime = currentTime - self.lastTime
        self.tableOfTimes[self.currentFilaSize] += deltaTime
        self.currentFilaSize += 1
        self.lastTime = currentTime

    def decreaseCurrentFilaSize(self, currentTime: float):
        deltaTime = currentTime - self.lastTime
        self.tableOfTimes[self.currentFilaSize] += deltaTime
        self.currentFilaSize -= 1
        self.lastTime = currentTime


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
count = 0
def addToQueue(event: Event):
    global eventQueue
    def keyFunc(e):
        return e.time
    eventQueue.append(event)
    eventQueue.sort(key=keyFunc, reverse=True)
    global count
    count += 1

historicoDeEventos = []
contEventosEscalonados = 0
limite = 0

# Mark: algoritmo aqui

def Chegada(fila: FilaAtendimento, currentTime: float):
    # contabiliza tempo
    global historicoDeEventos
    historicoDeEventos.append("Chegada na fila: " + fila.nomeFila+ ", Tempo: "+ str(currentTime))
    if fila.currentFilaSize < fila.tamanhoFilaMax:
        fila.increaseCurrentFilaSize(currentTime)
        if fila.quantidadeServidores >= fila.currentFilaSize:
            # agenda saida
            agendaSaida(fila, fila.getRandomSaidaTime(currentTime))
    agendaChegada(fila,fila.getRandomChegadaTime(currentTime))

def Saida(fila: FilaAtendimento, currentTime: float):
    global historicoDeEventos
    historicoDeEventos.append("Saida da fila: " + fila.nomeFila+ ", Tempo: "+ str(currentTime))
    fila.decreaseCurrentFilaSize(currentTime)
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

def run(fila: FilaAtendimento, firstTime: float, newLimite = int):
    global eventQueue
    global contEventosEscalonados
    global limite
    global historicoDeEventos
    eventQueue = []
    contEventosEscalonados = 0
    limite = newLimite + 2
    historicoDeEventos = []
    addToQueue(Event(fila, "C", firstTime))

    while len(eventQueue) > 0:
        """
        print("FilaSize current: " + str(eventQueue[0].fila.currentFilaSize))
        for i in eventQueue:
            print(i)
        print("---")
        """

        nextEvent = eventQueue.pop()
        if nextEvent.type == "C":
            Chegada(nextEvent.fila, nextEvent.time)
        elif nextEvent.type == "S" :
            Saida(nextEvent.fila, nextEvent.time)

    #for i in historicoDeEventos:
    #   print(i)

    for (c, t) in enumerate(fila.tableOfTimes):
        print( "time spent with " + str(c) + " custumers: " + str(t) )

    totalTime = fila.lastTime
    relativeTimeTable = []
    for (c, t) in enumerate(fila.tableOfTimes):
        relativeTimeTable.append((c/totalTime, t/totalTime))
        print( "percent time spent with " + str(c/totalTime) + " custumers: " + str(t/totalTime) )
    
    return relativeTimeTable

fila1 = FilaAtendimento("fila1",1,3,[2,3],[2,5])

run(fila1,2.5,100000)



