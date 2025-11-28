from random import Random
import cv2
import copy
import argparse
import os


from src.Draw import *
from src.Evaluator import *
from src.Individual import Gene

class Ind:
    uniprng = None
    normprng = None
    num = None
    h = None
    w = None
    target = None
    def __init__(self):
        self.genes = [Gene(self.h, self.w) for _ in range(self.num)]
        self.state = np.ones((self.h, self.w, 3), dtype=np.uint8) * 255
        self.fit = None
        self.fitness()

    def mutate(self):
        target = self.uniprng.randint(0, self.num-1)                   
        old_gnene = copy.deepcopy(self.genes[target])
        old_fit = copy.copy(self.fit)
        old_state = copy.deepcopy(self.state)

        g = self.genes[target].gene
        a = self.uniprng.random()

        point_num = Gene.point_nums

        if a < 0.5:
            # 修改座標
            for p in range(point_num):
                g[p][0] = np.clip(g[p][0] + self.normprng.normalvariate(0, 1) * self.w, 0, self.w)
                g[p][1] = np.clip(g[p][1] + self.normprng.normalvariate(0, 1) * self.h, 0, self.h) 

        else:        
            # 修改顏色
            for c in range(3):
                g[point_num][c] = np.clip(g[point_num][c] + self.normprng.normalvariate(0, 1) * 255, 0, 255) # R

            # 修改透明度 (確保不會變成完全透明或完全不透明)
            g[point_num+1] = np.clip(g[point_num+1] + self.normprng.normalvariate(0, 1), 0.1, 0.8)
        
        self.fit = None
        self.fitness()  # recalcuate fitness
        
        # if fitness worsens, revert the mutation
        if self.fit < old_fit:
            self.genes[target] = old_gnene
            self.fit = old_fit
            self.state = old_state


    def fitness(self):
        if self.fit == None:
            self.state = np.ones((self.h, self.w, 3), dtype=np.uint8) * 255
            for gene in self.genes:
                fill_poly(self.state, gene[:Gene.point_nums], np.array(gene[Gene.point_nums]), gene[Gene.point_nums+1])

            #self.fit = ssim(self.state, self.target)
            #self.fit = mse_fitness(self.state, self.target)
            self.fit = mse(self.state, self.target)


    def save(self, filename):
        img = self.state
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imwrite(filename, img)


def initEnv(h, w, target_img, poly_shape = 3, num = 10, seed1=None, seed2=None):
    uniprng = Random()
    uniprng.seed(seed1)
    normprng = Random()
    normprng.seed(seed2)

    Gene.uniprng = uniprng
    Gene.point_nums = poly_shape
    Ind.uniprng = uniprng
    Ind.normprng = normprng
    Ind.num = num  # num of polygon
    Ind.target = target_img
    Ind.h = h
    Ind.w = w


def main():

    parser = argparse.ArgumentParser(description="Evolve an image using polygons.")
    parser.add_argument("-i", "--input", type=str, required=True, help="file path")
    parser.add_argument("-g", "--gen", type=int, required=False, help="number of generations", default=1000)
    parser.add_argument("-n", "--polygon_num", type=int, required=False, help="number of polygons", default=50)
    parser.add_argument("-p", "--polygon_shape", type=int, required=False, help="shape of polygon", default=3)
    parser.add_argument("-s", "--img_size", type=int, required=False, help="image size", default=200)


    args = parser.parse_args()
    target_img = cv2.imread(args.input)
    target_img = cv2.cvtColor(target_img, cv2.COLOR_BGR2RGB)

    # resize img
    img_size = args.img_size
    h, w, _ = target_img.shape
    scale = img_size / w
    new_h, new_w = int(h * scale), img_size
    target_img = cv2.resize(target_img, (new_w, new_h))


    # initialize environment
    initEnv(new_h, new_w, target_img, poly_shape=args.polygon_shape, num = args.polygon_num)

    # create result folder
    path = "./result"
    if not os.path.isdir(path):
        os.makedirs(path)
        print("Folder 'result' created.")
    else:
        print("Folder 'result' already exists.")

    pic = Ind()

    total_gen = args.gen
    save_interval = total_gen // 20

    for gen in range(total_gen):
        print(f"Gen {gen} : {pic.fit}")
        pic.mutate()
        if gen % save_interval == 0:
            pic.save(f"./result/gen_{gen}_pixel_{args.img_size}_polyNum_{args.polygon_num}.png")
    pic.save(f"./result/gen_final_pixel_{args.img_size}_polyNum_{args.polygon_num}.png")    

if __name__ == "__main__":
    main()