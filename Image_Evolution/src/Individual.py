import numpy as np
from src.Draw import *
from src.Evaluator import *
from matplotlib import pyplot as plt 
import math

class Gene:
    uniprng = None
    point_nums = None
    def __init__(self, h, w):
        self.r = self.uniprng.randint(0, 255)
        self.g = self.uniprng.randint(0, 255)
        self.b = self.uniprng.randint(0, 255)
        self.alpha = self.uniprng.random()
        self.gene = [[self.uniprng.randint(0, w), self.uniprng.randint(0, h)] for _ in range(self.point_nums)] + [[self.r, self.g, self.b], self.alpha]

    def printGene(self):
        print(self.gene)

    def __getitem__(self, index):
        return self.gene[index]
    
    def __setitem__(self, idx, newval):
        self.gene[idx] = newval


class Ind:
    minMutRate = 1e-100
    maxMutRate = 1
    learningRate = None
    uniprng = None
    normprng = None
    num = None
    target = None
    h = None
    w = None
    
    def __init__(self):
        self.genes = [Gene(self.h, self.w) for _ in range(self.num)]
        self.state = np.ones((self.h, self.w, 3), dtype=np.uint8) * 255
        self.mutRate = self.uniprng.uniform(0.1, 0.9)
        self.fit = None
        self.fitness()
         

    def crossover(self, other):
        for i in range(len(self.genes)):
            if self.uniprng.random() <= 0.5:
                self.genes[i], other.genes[i] = other.genes[i], self.genes[i]  

        alpha = self.uniprng.random()
        tmp = alpha * self.mutRate + (1-alpha) * other.mutRate
        other.mutRate = alpha * other.mutRate + (1-alpha) * self.mutRate
        self.mutRate = tmp
                        
        self.fit = None
        other.fit = None

    def mutateMutRate(self):
        self.mutRate = self.mutRate * math.exp(self.learningRate * self.normprng.normalvariate(0, 1))
        
        if self.mutRate < self.minMutRate: 
            self.mutRate = self.minMutRate
        if self.mutRate > self.maxMutRate: 
            self.mutRate = self.maxMutRate

    def mutate(self):
            self.mutateMutRate() 

            prob = 0.4 
            for i in range(len(self.genes)):

                if self.uniprng.random() < prob:
                    # 取得目前的基因值
                    g = self.genes[i].gene 

                    # 計算變動幅度 (Scale)
                    scale_w = self.mutRate * self.w 
                    scale_h = self.mutRate * self.h 
                    scale_c = self.mutRate * 255 
                    
                    point_num = Gene.point_nums

                    for p in range(point_num):
                        g[p][0] = np.clip(g[p][0] + self.normprng.normalvariate(0, 1) * scale_w, 0, self.w)
                        g[p][1] = np.clip(g[p][1] + self.normprng.normalvariate(0, 1) * scale_h, 0, self.h) 
                    
                    
                    # 修改顏色
                    for i in range(3):
                        g[point_num][i] = np.clip(g[point_num][i] + self.normprng.normalvariate(0, 1) * scale_c, 0, 255) # R
                    
                    # 修改透明度 (確保不會變成完全透明或完全不透明)
                    g[point_num+1] = np.clip(g[point_num+1] + self.mutRate * self.normprng.normalvariate(0, 1), 0.1, 0.8)
                        
            self.fit = None
    
    
    def fitness(self):
        if self.fit == None:
            self.state = np.ones((self.h, self.w, 3), dtype=np.uint8) * 255
            for gene in self.genes:
                fill_poly(self.state, gene[:Gene.point_nums], np.array(gene[Gene.point_nums]), gene[Gene.point_nums+1])

            #self.fit = ssim(self.state, self.target)
            #self.fit = mse_fitness(self.state, self.target)
            self.fit = mse(self.state, self.target)

    def showInd(self):
        plt.imshow(self.state)
        plt.axis('off')
        plt.show()

