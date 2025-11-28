# Image Evolution
* A small genetic-algorithm project that evolves images (or image features) over generations by using **polygon** to better match a target or to explore emergent visual solutions.
* This repository contains the implementation, results and source files used for experiments.

## Quick overview
- The project uses evolutionary techniques (selection, crossover, mutation) to generate image candidates and evolve them over time.
- Input assets and targets should live under `img/`.

|target Img|Gen 0|Gen 5000|Gen 25000|
|--|--|--|--|
|![p1](img_src/scream.png)|![p2](img_src/gen_0_pixel_200_rectNum_50.png)|![p3](./img_src/gen_5000_pixel_200_rectNum_50.png)|![p4](img_src/gen_25000_pixel_200_rectNum_50.png)|


## Difference of `main_ec.py` and `main.py`
- `main_ec.py` use evolution computing skills (selection、crossover、mutation) to implement image evolution
- `main.py` use only mutation skilss to implement image evolution

## Requirements
- Python 3.8+ (recommended)
- Typical libraries used by image-evolution experiments:
  - numpy
  - scipy
  - opencv-python
  - matplotlib 

Install dependencies:
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt   # if provided
# or
pip install pillow numpy matplotlib tqdm
```


## HOW TO RUN
1. Place your target image(s) in img/ (e.g. img/target.png).
2. Open the main script "main.py" or "main_ec.py"
3. Edit configuration parameters in the script (population size, generations, mutation rate, image size, etc.).
4. Run the script:
```bash
python main.py -i img/target.png # QUICK RUN
# OR
python main.py -i img/target.png -g GEN_NUM -n POLYGON_NUM -p POLYGON_SHAPE -s IMG_SIZE
```
or
```bash
python main_ec.py -i img/target.png # QUICK RUN
# OR
python main.py -i img/target.png -g GEN_NUM -n POLYGON_NUM -p POLYGON_SHAPE -s IMG_SIZE -pop POPULATION_SIZE
```

* Notes:
    * The exact script name and CLI options depend on the implementation inside 
    * Outputs (final images) are written to result* folders.
    * Make sure in right file path