#Heitor, Hojin, Gustavo

import CongruenteLinear

#congruente = CongruenteLinear.CongruenteLinear(75,2**16 + 1,153,74,True)
# print(congruente.geraAleatorio())


class FilaAtendimento():
    def __init__(self, nomeFila: str ,quantidadeServidores: int ,tamanhoFilaMax:int, chegadaTimeBounds, saidaTimeBounds, congruent, queue ):
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
        self.congruent = congruent
        self.queue = queue

    def Chegada(self, currentTime: float):
    # contabiliza tempo
        global historicoDeEventos
        fila = self
        historicoDeEventos.append("Chegada na fila: " + fila.nomeFila+ ", Tempo: "+ str(currentTime))
        if fila.currentFilaSize < fila.tamanhoFilaMax:
            fila.increaseCurrentFilaSize(currentTime)
            if fila.quantidadeServidores >= fila.currentFilaSize:
                # agenda saida
                self.queue.agendaSaida(fila, fila.getRandomSaidaTime(currentTime))
        self.queue.agendaChegada(fila,fila.getRandomChegadaTime(currentTime))

    def Saida(self , currentTime: float):
        global historicoDeEventos
        fila = self
        historicoDeEventos.append("Saida da fila: " + fila.nomeFila+ ", Tempo: "+ str(currentTime))
        fila.decreaseCurrentFilaSize(currentTime)
        if fila.currentFilaSize > 0: # >= 1
            self.queue.agendaSaida(fila, fila.getRandomSaidaTime(currentTime))

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
        randomResult = self.getRandom(self.chegadaLowerBound, self.chegadaUpperBound)
        result = current + randomResult
        #print(type(current))
        #print("current: "+ current + " randomResult: "+ randomResult + "result: "+ result)
        return result

    def getRandom(self, lower: float, upper: float) -> float :
        congruent = self.congruent
        random = float(congruent.geraAleatorio())
        u = (upper - lower)*random  + lower
        return u

class Event():
     def __init__(self, fila: FilaAtendimento ,type: str, time: float):
        self.fila = fila
        self.type = type
        self.time = time

     def __str__(self) -> str:
        return "tempo: "+ str(self.time) + ", tipo: "+  self.type




class Queue:
    def __init__(self):
        self.eventQueue = []
        self.count = 0
        self.contEventosEscalonados = 0
        self.limite = 100000

    def addToQueue(self, event: Event):
        def keyFunc(e):
            return e.time
        self.eventQueue.append(event)
        self.eventQueue.sort(key=keyFunc, reverse=True)
        self.count += 1

    def agendaChegada(self, fila: FilaAtendimento , futureTime: float):

        if self.contEventosEscalonados < self.limite:
            self.contEventosEscalonados += 1
            self.addToQueue(Event(fila, "C", futureTime))

    def agendaSaida(self, fila: FilaAtendimento, futureTime: float):

        if self.contEventosEscalonados < self.limite:
            self.contEventosEscalonados += 1
            self.addToQueue(Event(fila, "S", futureTime))

historicoDeEventos = []

# Mark: algoritmo aqui

def run(fila: FilaAtendimento, firstTime: float, queue: Queue):

    global historicoDeEventos
    historicoDeEventos = []
    print(type(queue))
    queue.addToQueue(Event(fila, "C", firstTime))
    while len(queue.eventQueue) > 0:
        """
        print("FilaSize current: " + str(eventQueue[0].fila.currentFilaSize))
        for i in eventQueue:
            print(i)
        print("---")
        """

        nextEvent = queue.eventQueue.pop()
        if nextEvent.type == "C":
            nextEvent.fila.Chegada(nextEvent.time)
        elif nextEvent.type == "S" :
            nextEvent.fila.Saida(nextEvent.time)

    #for i in historicoDeEventos:
    #   print(i)

    #for (c, t) in enumerate(fila.tableOfTimes):
    #    print( "time spent with " + str(c) + " custumers: " + str(t) )

    totalTime = fila.lastTime
    relativeTimeTable = []
    for (c, t) in enumerate(fila.tableOfTimes):
        relativeTimeTable.append((c, t/totalTime))
        print( "percent time spent with " + str(c) + " custumers: " + str(t/totalTime) )
    print("---")
    return relativeTimeTable


queue = Queue()


congruente = CongruenteLinear.CongruenteLinear(75,2**16 + 1,153,74,True)
fila1 = FilaAtendimento("fila1",1,5,[2,4],[3,5],congruente, queue)
fila1table1 = run(fila1,2.5, queue)

congruente2 = CongruenteLinear.CongruenteLinear(130, 10 + 1, 1, 1,True)
fila2 = FilaAtendimento("fila2",1,5,[2,4],[3,5],congruente2, queue)
fila1table2 = run(fila1,2.5, queue)

congruente3 = CongruenteLinear.CongruenteLinear(752,7**16 + 2,351,41,True)
fila3 = FilaAtendimento("fila2",1,5,[2,4],[3,5],congruente2, queue)
fila1table3 = run(fila1,2.5, queue)

