const canvas = document.getElementById("myCanvas");
const ctx = canvas.getContext("2d");
const startTime = Date.now();
const geneLength = 34; // 7+3+24
var mutation_rate = 0.2;
const ballLife = 500;
var generate_cycle = 2500;
const foodList = [];
var frame = 0
var currentTime = Math.floor((Date.now() - startTime) / 1000);
var balls = [];
var numBalls = 6; // init number of balls

// Food Score Calcuation Function
function hexToRgb(hex) {
    hex = hex.replace('#', '');
    if (hex.length === 3) {
        hex = hex[0]+hex[0]+hex[1]+hex[1]+hex[2]+hex[2];
    }
    const bigint = parseInt(hex, 16);
    return [
        (bigint >> 16) & 255,
        (bigint >> 8) & 255,
        bigint & 255
    ];
}

class Food{
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.edge = 4; // radius of food
        // random color to increase genetic evolution pressure
        this.color = '#' + Math.floor(Math.random()*16777215).toString(16).padStart(6, '0');
        this.life = 50.00; // life cycle of food
    }

    draw(ctx) {
        this.life -= 0.01; // decrease life cycle of food
        ctx.beginPath();
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x, this.y, this.edge, this.edge);
        ctx.closePath();
    }
}

class Ball {
    constructor(x, y, gene) {
        this.x = x;
        this.y = y;
        this.gene = gene;
        const [radius, speed, color] = convertGene(gene);
        this.radius = radius;
        this.color = color;

        // speed 1 ~ 8 
        this.dx = speed/4 * 1/radius * 15; 
        this.dy = 4/speed * 1/radius * 15;
        this.dirx = Math.random() < 0.5 ? -1 : 1;
        this.diry = Math.random() < 0.5 ? -1 : 1;
        this.life = 1;
        this.score = 0;
    }

    draw(ctx, index) {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
        ctx.strokeStyle = "#000000";
        ctx.lineWidth = 2;
        ctx.stroke();
        ctx.closePath();

        // Draw ball index
        ctx.font = `${Math.max(12, this.radius)}px Arial`;
        ctx.fillStyle = "#fff";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(index + 1, this.x, this.y);
    }

    update(canvas) {
        this.x += this.dirx * this.dx;
        this.y += this.diry * this.dy;
        this.life += (0.0001 * this.radius);

        // checking food collision
        for (let i = foodList.length - 1; i >= 0; i--) {
            const food = foodList[i];
            const foodCenterX = food.x + food.edge / 2;
            const foodCenterY = food.y + food.edge / 2;
            const dist = Math.sqrt(
                (this.x - foodCenterX) ** 2 + (this.y - foodCenterY) ** 2
            );
            if (dist < this.radius + food.edge / 2) {
                // higher score for closer colors
                const foodRGB = hexToRgb(food.color);
                const ballRGB = hexToRgb(this.color);
                const colorDist = Math.sqrt(
                    (foodRGB[0] - ballRGB[0]) ** 2 +
                    (foodRGB[1] - ballRGB[1]) ** 2 +
                    (foodRGB[2] - ballRGB[2]) ** 2
                );
                const colorScore = 1 / (colorDist + 1);
                const s = 1 + food.life * colorScore;
                this.score += s;
                this.life -= Math.min(0, food.life * (this.radius / 127));
                foodList.splice(i, 1);
            }
        }

        // Ball collision and bounce
        for (const other of balls) {
            if (other !== this) {
                const dx = other.x - this.x;
                const dy = other.y - this.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                if (distance < this.radius + other.radius) {
                    const nx = dx / distance;
                    const ny = dy / distance;
                    const overlap = (this.radius + other.radius) - distance;
                    this.x -= nx * (overlap / 2);
                    this.y -= ny * (overlap / 2);
                    other.x += nx * (overlap / 2);
                    other.y += ny * (overlap / 2);
                    // Exchange direction and adjust slightly to avoid getting stuck
                    let tmpx = this.dirx, tmpy = this.diry;
                    this.dirx = -other.dirx + (Math.random() - 0.5) * 0.5;
                    this.diry = -other.diry + (Math.random() - 0.5) * 0.5;
                    other.dirx = -tmpx + (Math.random() - 0.5) * 0.5;
                    other.diry = -tmpy + (Math.random() - 0.5) * 0.5;
                    // regularize
                    let len1 = Math.sqrt(this.dirx * this.dirx + this.diry * this.diry);
                    let len2 = Math.sqrt(other.dirx * other.dirx + other.diry * other.diry);
                    if (len1 !== 0) {
                        this.dirx /= len1;
                        this.diry /= len1;
                    }
                    if (len2 !== 0) {
                        other.dirx /= len2;
                        other.diry /= len2;
                    }
                }
            }
        }
        // left and right wall
        if (this.x + this.radius > canvas.width) {
            this.x = canvas.width - this.radius;
            this.dirx *= -1;
            // random adjustment to direction to avoid sticking
            this.diry += (Math.random() - 0.5) * 0.5;
        }
        if (this.x - this.radius < 0) {
            this.x = this.radius;
            this.dirx *= -1;
            this.diry += (Math.random() - 0.5) * 0.5;
        }
        // top and bottom wall
        if (this.y + this.radius > canvas.height) {
            this.y = canvas.height - this.radius;
            this.diry *= -1;
            this.dirx += (Math.random() - 0.5) * 0.5;
        }
        if (this.y - this.radius < 0) {
            this.y = this.radius;
            this.diry *= -1;
            this.dirx += (Math.random() - 0.5) * 0.5;
        }
        // keep direction as unit length
        let len = Math.sqrt(this.dirx * this.dirx + this.diry * this.diry);
        if (len !== 0) {
            this.dirx /= len;
            this.diry /= len;
        }
    }
}

// gene generator
function geneGenerator() {
    let gene = "";
    for(let i = 0; i < geneLength; i++) {
        gene += Math.random() < 0.5 ? "0" : "1";
    }
    return gene;
}

// decoder of genes
function convertGene(gene){
    // 7 bits size, 3 bits speed, 24 bits color
    var size = parseInt(gene.substring(0, 7), 2);
    var speed = parseInt(gene.substring(7, 10), 2);
    var color = gene.substring(10, 34); // 24 bits
    var colorHex = parseInt(color, 2).toString(16).padStart(6, '0');
    colorHex = "#" + colorHex;
    return [Math.max(5, size), speed+1, colorHex];
}

// calculate current time
function drawTime() {
    currentTime = Math.floor((Date.now() - startTime) / 1000);
    ctx.font = "18px Arial";
    ctx.fillStyle = "black";
    ctx.textAlign = "left";
    ctx.fillText(`Time：${currentTime} sec`, 10, 25);
    ctx.fillText(`Frame: ${frame}`, 10, 50);
}

// food generator 
function createFood() {
    const foodNum = Math.floor(Math.random() * 10) + 5;
    for (let i = 0; i < foodNum; i++) {
        let tryCount = 0;
        let valid = false;
        let x, y;
        while (!valid && tryCount < 100) {
            x = Math.random() * (canvas.width - 4);
            y = Math.random() * (canvas.height - 4);
            valid = true;
            for (const ball of balls) {
                const dist = Math.sqrt(
                    (x + 2 - ball.x) ** 2 + (y + 2 - ball.y) ** 2
                );
                if (dist < ball.radius + 2) {
                    valid = false;
                    break;
                }
            }
            tryCount++;
        }
        if (valid) {
            foodList.push(new Food(x, y));
        }
    }
}

// generate init balls
for (let i = 0; i < numBalls; i++) {
    const x = Math.random() * (canvas.width - 127);
    const y = Math.random() * (canvas.height - 127);
    const gene = geneGenerator();
    balls.push(new Ball(x, y, gene));
}

// compare function for sorting
function compare(ball1, ball2) {
    return (ball2.score / ball2.life) - (ball1.score / ball1.life);
}

// crossover
function crossOver(gene1, gene2) {
    const crossoverPoint = Math.floor(Math.random() * geneLength);
    var newGene = gene1.substring(0, crossoverPoint) + gene2.substring(crossoverPoint);
    // mutation
    let arr = newGene.split('');
    for(let i = 0; i < arr.length; i++) {
        if (Math.random() < mutation_rate) {
            arr[i] = arr[i] === '0' ? '1' : '0';
        }
    }
    return arr.join('');
}

// show ranking
function updateRanking() {
    const rankingList = document.getElementById('ranking-list');
    const sortedBalls = balls.slice().sort(compare);
    rankingList.innerHTML = sortedBalls.map((ball, idx) => {
        return `<li>
            <span style="display:inline-block; width:16px; height:16px; background:${ball.color}; border:1px solid #000; margin-right:5px;vertical-align:middle;"></span>
            <b>Score:</b> ${(ball.score / ball.life).toFixed(7)}<br>
            <small>Gene: ${ball.gene}</small>
        </li>`;
    }).join('');
}

// animation loop
function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // generate food every 500 frames
    if (frame % 500 === 0  && foodList.length < 20) {
        createFood();
    }

    // crossover
    if(frame !== 0 && frame % generate_cycle === 0) {
        // select parents from top 4
        const sortedBalls = balls.slice().sort(compare);
        var parent1 = Math.floor(Math.random() * 4);
        var parent2 = Math.floor(Math.random() * 4);
        if(parent2 === parent1) parent2 = (parent2 + 1)%4;
        const gene1 = sortedBalls[parent1].gene; 
        const gene2 = sortedBalls[parent2].gene;
        const x = Math.random() * (canvas.width - 127);
        const y = Math.random() * (canvas.height - 127);
        const gene = crossOver(gene1, gene2);
        var child = new Ball(x, y, gene);
        balls.push(child);

        generate_cycle += 500;
        generate_cycle = Math.min(generate_cycle, 5000);

        // record crossover data
        const logDiv = document.getElementById('mating-log');
        logDiv.innerHTML = 
        `<span style="color:#333;">crossover：</span>
        <span style="display:inline-block;width:18px;height:18px;background:${ sortedBalls[parent1].color};border:1px solid #000;vertical-align:middle;"></span>
        + 
        <span style="display:inline-block;width:18px;height:18px;background:${ sortedBalls[parent2].color};border:1px solid #000;vertical-align:middle;"></span>
        = 
        <span style="display:inline-block;width:18px;height:18px;background:${child.color};border:1px solid #000;vertical-align:middle;"></span>`;
    }

    // 每 5000 frame 調整突變率
    if(frame !==0 && frame % 5000 === 0 && mutation_rate > 0.01){
        mutation_rate -= 0.05;
    }

    // step 2. update ranking
    updateRanking();

    //===============drawing part======================================================

    // draw food
    for (let i = foodList.length - 1; i >= 0; i--) {
        const food = foodList[i];
        if(food.life <= 0) {
            foodList.splice(i, 1);
        } else {
            food.draw(ctx);
        }
    }

    // draw balls
    for (let i = balls.length - 1; i >= 0; i--) {
        const ball = balls[i];
        if (ball.life > ballLife ) {
            balls.splice(i, 1);
            continue;
        }
        ball.update(canvas);
        ball.draw(ctx, i);
    }
    // draw time
    drawTime();

    frame += 1;
    requestAnimationFrame(animate);
}

// start animation
animate();