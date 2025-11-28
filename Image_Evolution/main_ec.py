from random import Random
import cv2
import copy
import argparse
import os


from src.Individual import *
from src.Population import *



def initEnv(h, w, target_img, poly_shape = 3, num = 10, pop_size = 50, seed1=None, seed2=None):
    uniprng = Random()
    uniprng.seed(seed1)
    normprng = Random()
    normprng.seed(seed2)

    Gene.uniprng = uniprng
    Gene.point_nums = poly_shape
    Ind.uniprng = uniprng
    Ind.normprng = normprng
    Ind.num = num  # num of triangle
    Ind.target = target_img
    Ind.learningRate = 1/ math.sqrt(50)
    Ind.h = h
    Ind.w = w
    Population.h = h
    Population.w = w
    Population.uniprng = uniprng
    Population.crossoverFraction = 0.7
    Population.size = pop_size  # num of individual



def main():
    
    parser = argparse.ArgumentParser(description="Evolve an image using polygons.")
    parser.add_argument("-i", "--input", type=str, required=True, help="file path")
    parser.add_argument("-g", "--gen", type=int, required=False, help="number of generations", default=1000)
    parser.add_argument("-n", "--polygon_num", type=int, required=False, help="number of polygons", default=50)
    parser.add_argument("-p", "--polygon_shape", type=int, required=False, help="shape of polygon", default=3)
    parser.add_argument("-s", "--img_size", type=int, required=False, help="image size", default=200)
    parser.add_argument("-pop", "--pop_size", type=int, required=False, help="population size", default=50)

    args = parser.parse_args()
    
    target_img = cv2.imread(args.input)  
    target_img = cv2.cvtColor(target_img, cv2.COLOR_BGR2RGB)

    # resize img
    img_size = args.img_size
    h, w, _ = target_img.shape
    scale = img_size / w
    new_h, new_w = int(h * scale), img_size
    target_img = cv2.resize(target_img, (new_w, new_h))

    # create result folder
    path = "./result"
    if not os.path.isdir(path):
        os.makedirs(path)
        print("Folder 'result' created.")
    else:
        print("Folder 'result' already exists.")
    

    # initialize environment
    initEnv(new_h, new_w, target_img, poly_shape=args.polygon_shape, num=args.polygon_num, pop_size = args.pop_size)

    pop = Population()
    pop.evalFitness()
    pop.printState()

    total_gen = args.gen
    save_freq = total_gen // 20

    for gen in range(total_gen):
        print(f"==============={gen}========================")
        child = copy.deepcopy(pop)
        child.binaryTournament()
        child.newInd(10)
        child.crossover()
        child.mutate()
        child.evalFitness()

        pop.merge(child)
        pop.truncation()
        pop.printState()
        if gen % save_freq == 0:
            pop.saveBest(f"./result/Gen_{gen}_pixel_{img_size}_polyNum_{args.polygon_num}.png")
    # pop.showPic()
    pop.saveBest(f"./result/Gen_final_pixel_{img_size}_polyNum_{args.polygon_num}.png")    

if __name__ == "__main__":
    main()