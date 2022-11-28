#Heitor, Hojin, Gustavo

import sys
import CongruenteLinear
import copy
import numpy

#congruente = CongruenteLinear.CongruenteLinear(75,2**16 + 1,153,74,True)
# print(congruente.geraAleatorio())
quantidadeAleatorios = 100000

class FilaAtendimento():
    def __init__(self, nomeFila: str ,quantidadeServidores: int ,tamanhoFilaMax:int, chegadaTimeBounds, saidaTimeBounds, queue ):
        self.nomeFila = nomeFila
        self.quantidadeServidores = quantidadeServidores
        self.chegadaLowerBound = float(chegadaTimeBounds[0])
        self.chegadaUpperBound = float(chegadaTimeBounds[1])
        self.saidaLowerBound = float(saidaTimeBounds[0])
        self.saidaUpperBound = float(saidaTimeBounds[1])
        self.currentFilaSize = 0
        if tamanhoFilaMax != None:
            self.tamanhoFilaMax = 5
            self.tableOfTimes = [0] * (self.tamanhoFilaMax+1)
        else:
            self.tamanhoFilaMax = sys.maxsize
            self.tableOfTimes = [0]*100000
            

        self.lastTime = 0
        self.queue = queue
        self.congruent = self.queue.congruent
        self.valuesAndFilas = []
        self.automaticReEntry = True
        #print("tamanhoFilaMax: " + str(self.tamanhoFilaMax))


    def Chegada(self, currentTime: float):
    # contabiliza tempo
        if self.queue.limite < self.queue.congruent.cont:
            return

        global historicoDeEventos
        fila = self
        historicoDeEventos.append("Chegada na fila: " + fila.nomeFila+ ", Tempo: "+ str(currentTime))
        if fila.currentFilaSize < fila.tamanhoFilaMax:
            fila.increaseCurrentFilaSize(currentTime)
            if fila.quantidadeServidores >= fila.currentFilaSize:
                # agenda saida
                self.queue.agendaSaida(fila, fila.getRandomSaidaTime(currentTime))
        if self.automaticReEntry:
            self.queue.agendaChegada(fila,fila.getRandomChegadaTime(currentTime))

    def Saida(self , currentTime: float):
        if self.queue.limite < self.queue.congruent.cont:
            return
        global historicoDeEventos
        fila = self
        historicoDeEventos.append("Saida da fila: " + fila.nomeFila+ ", Tempo: "+ str(currentTime))
        fila.decreaseCurrentFilaSize(currentTime)
        if fila.currentFilaSize > 0: # >= 1
            self.queue.agendaSaida(fila, fila.getRandomSaidaTime(currentTime))
        self.runRouter(currentTime)

    def increaseCurrentFilaSize(self, currentTime: float):
        deltaTime = currentTime - self.lastTime
        try:
            self.tableOfTimes[self.currentFilaSize] += deltaTime
        except IndexError:
            print(self.currentFilaSize)
            self.tableOfTimes.append(0)
            self.tableOfTimes[self.currentFilaSize] += deltaTime
        
        self.currentFilaSize += 1
        self.lastTime = currentTime

    def decreaseCurrentFilaSize(self, currentTime: float):
        deltaTime = currentTime - self.lastTime
        try:
            self.tableOfTimes[self.currentFilaSize] += deltaTime
        except:
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
    def setRouter(self, probailityFilaArray):
        self.valuesAndFilas = probailityFilaArray
        def keyProbFunc(e):
            return e.probability
        self.valuesAndFilas.sort(key=keyProbFunc, reverse=False)
        
        acumula = 0
        for i in range(len(self.valuesAndFilas)): 
            acumula += self.valuesAndFilas[i].probability
            self.valuesAndFilas[i].probability = acumula
 
    def runRouter(self, currentTime):
        if len(self.valuesAndFilas) > 1:
            random = float(self.congruent.geraAleatorio())
            for probabilityAndFila in self.valuesAndFilas:
                if random <= probabilityAndFila.probability:
                    probabilityAndFila.fila.Chegada(currentTime)
                    break
#        elif len(self.valuesAndFilas) == 1:
#            self.valuesAndFilas[0].fila.Chegada(currentTime)


class Event():
     def __init__(self, fila: FilaAtendimento ,type: str, time: float):
        self.fila = fila
        self.type = type
        self.time = time

     def __str__(self) -> str:
        return "tempo: "+ str(self.time) + ", tipo: "+  self.type

class Queue:
    def __init__(self, congruent: CongruenteLinear):
        self.eventQueue = []
        self.count = 0
        self.contEventosEscalonados = 0
        global quantidadeAleatorios
        self.limite = quantidadeAleatorios
        self.congruent = congruent

    def addToQueue(self, event: Event):
        def keyFunc(e):
            return e.time
        self.eventQueue.append(event)
        self.eventQueue.sort(key=keyFunc, reverse=True)
        self.count += 1

    def agendaChegada(self, fila: FilaAtendimento , futureTime: float):
        self.addToQueue(Event(fila, "C", futureTime))

    def agendaSaida(self, fila: FilaAtendimento, futureTime: float):
        self.addToQueue(Event(fila, "S", futureTime))


class EmptyFilaAtendimento(FilaAtendimento):
    def __init__(self):
        pass
    def Chegada(self, currentTime: float):
        return
    def Saida(self, currentTime: float):
        return

historicoDeEventos = []

# Mark: algoritmo aqui

def run(fila: FilaAtendimento, firstTime: float, queue: Queue):

    global historicoDeEventos
    historicoDeEventos = []
    queue.addToQueue(Event(fila, "C", firstTime))
    while queue.limite > queue.congruent.cont:
        nextEvent = queue.eventQueue.pop()
        if nextEvent.type == "C":
            nextEvent.fila.Chegada(nextEvent.time)
        elif nextEvent.type == "S" :
            nextEvent.fila.Saida(nextEvent.time)


class ProbailityFila:
    def __init__(self, fila: FilaAtendimento, probability: float):
        self.fila = fila
        self.probability = probability

relativeTimeTable = []
lastTimes = []
# first simulation

congruente = CongruenteLinear.CongruenteLinear(75,2**16 + 1,153,74,True)
queue = Queue(congruente)
maxInt = int(sys.maxsize )
fila1 = FilaAtendimento("F1",1,None,[1,4],[1,1.5], queue)
fila2 = FilaAtendimento("F2",3,5,[maxInt,maxInt],[5,10], queue)
fila2.automaticReEntry = False
fila3 = FilaAtendimento("F3",2,8,[maxInt,maxInt],[10,20], queue)
fila3.automaticReEntry = False

fila1.setRouter([ProbailityFila(fila3, 0.2), ProbailityFila(fila2, 0.8)])
fila2.setRouter([ProbailityFila(EmptyFilaAtendimento(), 0.2) ,ProbailityFila(fila1, 0.3), ProbailityFila(fila3, 0.5)])
fila3.setRouter([ProbailityFila(EmptyFilaAtendimento(), 0.3), ProbailityFila(fila2, 0.7)])

run(fila1,2.5, queue)

fila1table1 =  numpy.array(fila1.tableOfTimes)
fila2table1 =  numpy.array(fila2.tableOfTimes)
fila3table1 =  numpy.array(fila3.tableOfTimes)

last1 = copy.deepcopy(max([fila1.lastTime, fila2.lastTime, fila3.lastTime]))
tables = copy.deepcopy([fila1table1/last1, fila2table1/last1, fila3table1/last1])

relativeTimeTable.append(tables)
lastTimes.append(last1)

#second sinualtion

congruente = CongruenteLinear.CongruenteLinear(218,41**7 + 330, 60,222,True)
queue = Queue(congruente)
maxInt = int(sys.maxsize )
fila1 = FilaAtendimento("F1",1,None,[1,4],[1,1.5], queue)
fila2 = FilaAtendimento("F2",3,5,[maxInt,maxInt],[5,10], queue)
fila2.automaticReEntry = False
fila3 = FilaAtendimento("F3",2,8,[maxInt,maxInt],[10,20], queue)
fila3.automaticReEntry = False

fila1.setRouter([ProbailityFila(fila3, 0.2), ProbailityFila(fila2, 0.8)])
fila2.setRouter([ProbailityFila(EmptyFilaAtendimento(), 0.2) ,ProbailityFila(fila1, 0.3), ProbailityFila(fila3, 0.5)])
fila3.setRouter([ProbailityFila(EmptyFilaAtendimento(), 0.3), ProbailityFila(fila2, 0.7)])

run(fila1,2.5, queue)

fila1table1 =  numpy.array(fila1.tableOfTimes)
fila2table1 =  numpy.array(fila2.tableOfTimes)
fila3table1 =  numpy.array(fila3.tableOfTimes)

last2 = copy.deepcopy(max([fila1.lastTime, fila2.lastTime, fila3.lastTime]))
tables2 = copy.deepcopy([fila1table1/last2, fila2table1/last2, fila3table1/last2])

relativeTimeTable.append(tables2)
lastTimes.append(last2)


#third sinualtion

congruente = CongruenteLinear.CongruenteLinear(78375,5**17 + 331,68253,86784,True)
queue = Queue(congruente)
maxInt = int(sys.maxsize )
fila1 = FilaAtendimento("F1",1,None,[1,4],[1,1.5], queue)
fila2 = FilaAtendimento("F2",3,5,[maxInt,maxInt],[5,10], queue)
fila2.automaticReEntry = False
fila3 = FilaAtendimento("F3",2,8,[maxInt,maxInt],[10,20], queue)
fila3.automaticReEntry = False

fila1.setRouter([ProbailityFila(fila3, 0.2), ProbailityFila(fila2, 0.8)])
fila2.setRouter([ProbailityFila(EmptyFilaAtendimento(), 0.2) ,ProbailityFila(fila1, 0.3), ProbailityFila(fila3, 0.5)])
fila3.setRouter([ProbailityFila(EmptyFilaAtendimento(), 0.3), ProbailityFila(fila2, 0.7)])

run(fila1,1.0, queue)



fila1table1 =  numpy.array(fila1.tableOfTimes)
fila2table1 =  numpy.array(fila2.tableOfTimes)
fila3table1 =  numpy.array(fila3.tableOfTimes)

last3 = copy.deepcopy(max([fila1.lastTime, fila2.lastTime, fila3.lastTime]))
tables3 = copy.deepcopy([fila1table1/last3, fila2table1/last3, fila3table1/last3])

relativeTimeTable.append(tables3)
lastTimes.append(last3)


#4th sinualtion

congruente = CongruenteLinear.CongruenteLinear(1735,3*17 + 31,1453,3724,True)
queue = Queue(congruente)
maxInt = int(sys.maxsize )
fila1 = FilaAtendimento("F1",1,None,[1,4],[1,1.5], queue)
fila2 = FilaAtendimento("F2",3,5,[maxInt,maxInt],[5,10], queue)
fila2.automaticReEntry = False
fila3 = FilaAtendimento("F3",2,8,[maxInt,maxInt],[10,20], queue)
fila3.automaticReEntry = False

fila1.setRouter([ProbailityFila(fila3, 0.2), ProbailityFila(fila2, 0.8)])
fila2.setRouter([ProbailityFila(EmptyFilaAtendimento(), 0.2) ,ProbailityFila(fila1, 0.3), ProbailityFila(fila3, 0.5)])
fila3.setRouter([ProbailityFila(EmptyFilaAtendimento(), 0.3), ProbailityFila(fila2, 0.7)])

run(fila1,1.0, queue)

fila1table1 =  numpy.array(fila1.tableOfTimes)
fila2table1 =  numpy.array(fila2.tableOfTimes)
fila3table1 =  numpy.array(fila3.tableOfTimes)

last4 = copy.deepcopy(max([fila1.lastTime, fila2.lastTime, fila3.lastTime]))
tables4 = copy.deepcopy([fila1table1/last4, fila2table1/last4, fila3table1/last4])

relativeTimeTable.append(tables4)
lastTimes.append(last4)


#5th sinualtion

congruente = CongruenteLinear.CongruenteLinear(75123,7**12 + 12,1532,734,True)
queue = Queue(congruente)
maxInt = int(sys.maxsize )
fila1 = FilaAtendimento("F1",1,None,[1,4],[1,1.5], queue)
fila2 = FilaAtendimento("F2",3,5,[maxInt,maxInt],[5,10], queue)
fila2.automaticReEntry = False
fila3 = FilaAtendimento("F3",2,8,[maxInt,maxInt],[10,20], queue)
fila3.automaticReEntry = False

fila1.setRouter([ProbailityFila(fila3, 0.2), ProbailityFila(fila2, 0.8)])
fila2.setRouter([ProbailityFila(EmptyFilaAtendimento(), 0.2) ,ProbailityFila(fila1, 0.3), ProbailityFila(fila3, 0.5)])
fila3.setRouter([ProbailityFila(EmptyFilaAtendimento(), 0.3), ProbailityFila(fila2, 0.7)])

run(fila1,1.0, queue)

fila1table1 =  numpy.array(fila1.tableOfTimes)
fila2table1 =  numpy.array(fila2.tableOfTimes)
fila3table1 =  numpy.array(fila3.tableOfTimes)


last5 = copy.deepcopy(max([fila1.lastTime, fila2.lastTime, fila3.lastTime]))
tables5 = copy.deepcopy([fila1table1/last5, fila2table1/last5, fila3table1/last5])



relativeTimeTable.append(tables5)
lastTimes.append(last5)

# compiling data for display


for i in range(len(relativeTimeTable)):
    for filaIndex in range(len(relativeTimeTable[i])):
        for (i,p) in enumerate(relativeTimeTable[i][filaIndex]):
            if p > 0.00001:
                filaNum = int(i)
                print("fila: "+ str(filaNum)+ " clientes: "+ "probabilidade: " + str(p))


"""
filasRelativasSomadas = [[0.0]]*3

for i in range(len(relativeTimeTable)):
    for filaIndex in range(len(relativeTimeTable[i])):
        for numero in range(len(relativeTimeTable[i][filaIndex])):
            if len(filasRelativasSomadas[filaIndex]) < relativeTimeTable[i][filaIndex]:
                filasRelativasSomadas[filaIndex] +=  relativeTimeTable[i][filaIndex]
            else:
                filasRelativasSomadas[filaIndex].append(0.0)
                filasRelativasSomadas[filaIndex] +=  relativeTimeTable[i][filaIndex]


for i in (historicoDeEventos):
   print(i)
"""
