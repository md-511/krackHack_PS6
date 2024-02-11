/** @type {HTMLCanvasElement} */

const canvas = document.getElementById('background-canvas');
const ctx = canvas.getContext('2d');
const width = canvas.width = window.innerWidth * 0.99;
const height = canvas.height = window.innerHeight * 0.99;
const noParticles = 30;

class Particle
{
    constructor()
    {
        this.x = Math.random() * width;
        this.y = Math.random() * height;
        this.size = Math.random() * 5 + 5;
        this.xSpeed = Math.random() * 2 - 1;
        this.ySpeed = Math.random() * 2 - 1;
        this.closest = undefined;
    }

    update()
    {
        this.closest = undefined;   
        this.closest = findClosest(this);

        if(this.closest != undefined)
        {
            this.xSpeed *= 2;
            this.ySpeed *= 2;
        }
        
        if(this.x < 0 || this.x >= width)
        {
            this.xSpeed *= -1;
        }
        if(this.y < 0 || this.y >= height)
        {
            this.ySpeed *= -1;
        }
        this.x += this.xSpeed;
        this.y += this.ySpeed;

        if(this.closest != undefined)
        {
            this.xSpeed *= 0.5;
            this.ySpeed *= 0.5;
        }
    }
    
    draw(){
        this.update(); 
        if(this.closest != undefined) drawLine(this, this.closest);  
        let opacity = 1; 
        (this.closest != undefined) ? opacity = 1 : opacity = 0.3;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, 2*Math.PI);
        ctx.fillStyle = 'rgba(244, 97, 100, ' + opacity + ')';
        ctx.fill();
    }
};

function drawLine(pt1, pt2)
{
    ctx.beginPath();
    ctx.moveTo(pt1.x, pt1.y);
    ctx.lineTo(pt2.x, pt2.y);
    ctx.stroke();
}

let particles = [];
for(let i = 0; i < noParticles; ++i)
{
    particles.push(new Particle());
}

ctx.strokeStyle = 'rgb(255, 255, 255)';

function findClosest(p)
{
    let minDist = 75;
    let par = undefined;
    for(let particle of particles)
    {
        let dist = Math.sqrt(Math.pow(particle.x - p.x, 2) + Math.pow(particle.y - p.y, 2));
        if(dist < minDist && dist != 0)
        {
            minDist = dist;
            par = particle;
        }
    }
    return par;
}

function sketch(){
    ctx.clearRect(0, 0, width, height);
    particles.forEach((e) => {e.draw()});
    requestAnimationFrame(sketch);
}

sketch();
