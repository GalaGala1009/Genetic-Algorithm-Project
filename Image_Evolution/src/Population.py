from src.Individual import *
import numpy as np
import cv2

class Population:
    uniprng = None
    crossoverFraction = None
    h = None
    w = None    
    size = None

    def __init__(self):
        self.pop = []
        for _ in range(self.size):
            self.pop.append(Ind())
    
    def mutate(self):     
        for ind in self.pop:
            ind.mutate()
    
    def crossover(self):
        indexList1 = list(range(len(self.pop)))
        indexList2 = list(range(len(self.pop)))
        self.uniprng.shuffle(indexList1)
        self.uniprng.shuffle(indexList2)
            
        if self.crossoverFraction == 1.0:             
            for index1, index2 in zip(indexList1, indexList2):
                self.pop[index1].crossover(self.pop[index2])
        else:
            for index1, index2 in zip(indexList1, indexList2):
                rn = self.uniprng.random()
                if rn < self.crossoverFraction:
                    self.pop[index1].crossover(self.pop[index2])


    def binaryTournament(self):
        # generate random binary tournament pairs
        indexList1 = list(range(len(self.pop)))
        indexList2 = list(range(len(self.pop)))

        self.uniprng.shuffle(indexList1)
        self.uniprng.shuffle(indexList2)
        
        # do not allow self competition
        for i in range(len(self.pop)):
            if indexList1[i] == indexList2[i]:
                temp = indexList2[i]
                if i == 0:
                    indexList2[i] = indexList2[-1]
                    indexList2[-1] = temp
                else:
                    indexList2[i] = indexList2[i-1]
                    indexList2[i-1] = temp

        #compete
        newPop = []        
        for index1, index2 in zip(indexList1, indexList2):
            if self.pop[index1].fit > self.pop[index2].fit : 
                newPop.append(self.pop[index1])
            elif self.pop[index1].fit < self.pop[index2].fit:
                newPop.append(self.pop[index2])
            else:
                if self.uniprng.random() > 0.5:
                    newPop.append(self.pop[index1])
                else:
                    newPop.append(self.pop[index2])

        self.pop = newPop


    def truncation(self):
        self.pop.sort(key=lambda x : x.fit, reverse=True)
        self.pop = self.pop[:self.size]

    def merge(self, other):
        self.pop.extend(other.pop)

    def evalFitness(self):
        for ind in self.pop: 
            ind.fitness()

    def printState(self):
        for i, ind in enumerate(self.pop):
            print(i, ind.fit, ind.mutRate)

    def showPic(self):
        for ind in self.pop:
            ind.showInd()

    def newInd(self, num):
        for i in  range(num):
            self.pop.append(Ind())

    def saveBest(self, filename):
        img = self.pop[0].state
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imwrite(filename, img)