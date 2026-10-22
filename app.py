<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Super Mario Mini Game</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            user-select: none;
        }
        body {
            background-color: #111;
            color: #fff;
            font-family: 'Courier New', Courier, monospace;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            overflow: hidden;
        }
        #game-container {
            position: relative;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8);
            border: 4px solid #fff;
            border-radius: 8px;
            overflow: hidden;
            background: #5c94fc;
        }
        canvas {
            display: block;
            background: #5c94fc;
        }
        #ui-overlay {
            position: absolute;
            top: 10px;
            left: 15px;
            right: 15px;
            display: flex;
            justify-content: space-between;
            font-size: 18px;
            font-weight: bold;
            text-shadow: 2px 2px #000;
            z-index: 10;
        }
        #controls-hint {
            margin-top: 12px;
            text-align: center;
            color: #ccc;
            font-size: 14px;
        }
        /* Touch Controls for Mobile */
        #touch-controls {
            display: none;
            margin-top: 15px;
            gap: 20px;
            z-index: 20;
        }
        .btn {
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid #fff;
            color: white;
            padding: 12px 20px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 8px;
            touch-action: manipulation;
        }
        .btn:active {
            background: rgba(255, 255, 255, 0.5);
        }
        @media (max-width: 768px) {
            #touch-controls {
                display: flex;
            }
        }
    </style>
</head>
<body>

    <div id="game-container">
        <div id="ui-overlay">
            <div>MARIO<br><span id="score">000000</span></div>
            <div>COINS<br>🪙 x<span id="coins">00</span></div>
            <div>WORLD<br>1-1</div>
            <div>TIME<br><span id="timer">400</span></div>
        </div>
        <canvas id="canvas" width="640" height="400"></canvas>
    </div>

    <div id="controls-hint">
        🎮 <b>Điều khiển:</b> ⬅️ ➡️ Di chuyển | <b>Z / Space / ⬆️</b> Nhảy
    </div>

    <div id="touch-controls">
        <button class="btn" id="btn-left">⬅️ Left</button>
        <button class="btn" id="btn-jump">🚀 Jump</button>
        <button class="btn" id="btn-right">Right ➡️</button>
    </div>

<script>
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// --- Audio Synthesizer (Không cần tệp MP3 bên ngoài) ---
const AudioContext = window.AudioContext || window.webkitAudioContext;
let audioCtx = null;

function initAudio() {
    if (!audioCtx) audioCtx = new AudioContext();
}

function playSound(type) {
    if (!audioCtx) return;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.connect(gain);
    gain.connect(audioCtx.destination);

    const now = audioCtx.currentTime;
    if (type === 'jump') {
        osc.type = 'square';
        osc.frequency.setValueAtTime(150, now);
        osc.frequency.exponentialRampToValueAtTime(600, now + 0.15);
        gain.gain.setValueAtTime(0.1, now);
        gain.gain.linearRampToValueAtTime(0, now + 0.15);
        osc.start(now);
        osc.stop(now + 0.15);
    } else if (type === 'coin') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(987.77, now);
        osc.frequency.setValueAtTime(1318.51, now + 0.08);
        gain.gain.setValueAtTime(0.15, now);
        gain.gain.linearRampToValueAtTime(0, now + 0.3);
        osc.start(now);
        osc.stop(now + 0.3);
    } else if (type === 'stomp') {
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(120, now);
        osc.frequency.linearRampToValueAtTime(30, now + 0.1);
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.linearRampToValueAtTime(0, now + 0.1);
        osc.start(now);
        osc.stop(now + 0.1);
    } else if (type === 'win') {
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(400, now);
        osc.frequency.setValueAtTime(600, now + 0.1);
        osc.frequency.setValueAtTime(800, now + 0.2);
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.linearRampToValueAtTime(0, now + 0.5);
        osc.start(now);
        osc.stop(now + 0.5);
    }
}

// --- Cấu hình Game ---
const GRAVITY = 0.45;
const BLOCK_SIZE = 32;

let score = 0;
let coins = 0;
let gameOver = false;
let gameWon = false;
let cameraX = 0;

// Keys
const keys = { left: false, right: false, jump: false };

window.addEventListener('keydown', e => {
    initAudio();
    if (e.key === 'ArrowLeft' || e.key === 'a') keys.left = true;
    if (e.key === 'ArrowRight' || e.key === 'd') keys.right = true;
    if (e.key === 'ArrowUp' || e.key === 'w' || e.key === ' ' || e.key === 'z') {
        if (!keys.jump && mario.grounded) {
            mario.vy = -mario.jumpPower;
            mario.grounded = false;
            playSound('jump');
        }
        keys.jump = true;
    }
});

window.addEventListener('keyup', e => {
    if (e.key === 'ArrowLeft' || e.key === 'a') keys.left = false;
    if (e.key === 'ArrowRight' || e.key === 'd') keys.right = false;
    if (e.key === 'ArrowUp' || e.key === 'w' || e.key === ' ' || e.key === 'z') keys.jump = false;
});

// Mobile Touch
document.getElementById('btn-left').addEventListener('touchstart', (e) => { e.preventDefault(); initAudio(); keys.left = true; });
document.getElementById('btn-left').addEventListener('touchend', () => keys.left = false);
document.getElementById('btn-right').addEventListener('touchstart', (e) => { e.preventDefault(); initAudio(); keys.right = true; });
document.getElementById('btn-right').addEventListener('touchend', () => keys.right = false);
document.getElementById('btn-jump').addEventListener('touchstart', (e) => {
    e.preventDefault();
    initAudio();
    if (mario.grounded) {
        mario.vy = -mario.jumpPower;
        mario.grounded = false;
        playSound('jump');
    }
});

// --- Vẽ Pixel Art bằng Canvas ---
function drawMarioSprite(ctx, x, y, facing, isJumping) {
    ctx.save();
    ctx.translate(x + 16, y + 16);
    if (facing === 'left') ctx.scale(-1, 1);

    // Mũ & Áo đỏ
    ctx.fillStyle = '#e52521';
    ctx.fillRect(-10, -16, 18, 6); // Cap
    ctx.fillRect(-8, -6, 14, 10);  // Shirt

    // Mặt màu da
    ctx.fillStyle = '#fccc97';
    ctx.fillRect(-10, -10, 16, 6);

    // Mắt & Râu
    ctx.fillStyle = '#000';
    ctx.fillRect(2, -10, 3, 4);
    ctx.fillRect(-4, -6, 12, 3);

    // Quần yếm xanh
    ctx.fillStyle = '#0020c2';
    ctx.fillRect(-8, 2, 16, 8);

    // Giày nâu
    ctx.fillStyle = '#8b4513';
    if (isJumping) {
        ctx.fillRect(-12, 8, 8, 6);
        ctx.fillRect(4, 6, 8, 6);
    } else {
        ctx.fillRect(-10, 10, 8, 6);
        ctx.fillRect(2, 10, 8, 6);
    }

    ctx.restore();
}

function drawGoombaSprite(ctx, x, y, frame) {
    // Đầu/Thân
    ctx.fillStyle = '#b84418';
    ctx.beginPath();
    ctx.arc(x + 16, y + 14, 14, Math.PI, 0, false);
    ctx.fill();
    ctx.fillRect(x + 2, y + 14, 28, 10);

    // Mắt
    ctx.fillStyle = '#fff';
    ctx.fillRect(x + 6, y + 8, 5, 8);
    ctx.fillRect(x + 21, y + 8, 5, 8);
    ctx.fillStyle = '#000';
    ctx.fillRect(x + 8, y + 10, 3, 6);
    ctx.fillRect(x + 21, y + 10, 3, 6);

    // Chân
    ctx.fillStyle = '#000';
    if (frame % 20 < 10) {
        ctx.fillRect(x, y + 24, 10, 8);
        ctx.fillRect(x + 20, y + 22, 10, 8);
    } else {
        ctx.fillRect(x + 2, y + 22, 10, 8);
        ctx.fillRect(x + 22, y + 24, 10, 8);
    }
}

// --- Lớp Đối tượng Game ---
class Mario {
    constructor() {
        this.x = 50;
        this.y = 200;
        this.w = 28;
        this.h = 32;
        this.vx = 0;
        this.vy = 0;
        this.speed = 3.5;
        this.jumpPower = 11;
        this.grounded = false;
        this.facing = 'right';
    }

    update(map) {
        if (keys.left) {
            this.vx = -this.speed;
            this.facing = 'left';
        } else if (keys.right) {
            this.vx = this.speed;
            this.facing = 'right';
        } else {
            this.vx = 0;
        }

        this.vy += GRAVITY;

        // Trục X Collision
        this.x += this.vx;
        this.checkCollisionX(map);

        // Trục Y Collision
        this.y += this.vy;
        this.grounded = false;
        this.checkCollisionY(map);

        // Rơi xuống vực
        if (this.y > canvas.height + 50) {
            gameOver = true;
        }
    }

    checkCollisionX(map) {
        for (let b of map) {
            if (b.type === 'air') continue;
            if (this.x < b.x + b.w && this.x + this.w > b.x &&
                this.y < b.y + b.h && this.y + this.h > b.y) {
                if (this.vx > 0) this.x = b.x - this.w;
                else if (this.vx < 0) this.x = b.x + b.w;
            }
        }
    }

    checkCollisionY(map) {
        for (let b of map) {
            if (b.type === 'air') continue;
            if (this.x < b.x + b.w && this.x + this.w > b.x &&
                this.y < b.y + b.h && this.y + this.h > b.y) {
                if (this.vy > 0) {
                    this.y = b.y - this.h;
                    this.vy = 0;
                    this.grounded = true;
                } else if (this.vy < 0) {
                    this.y = b.y + b.h;
                    this.vy = 0;
                    if (b.type === 'question' && !b.empty) {
                        b.empty = true;
                        coins++;
                        score += 200;
                        playSound('coin');
                    }
                }
            }
        }
    }

    draw() {
        drawMarioSprite(ctx, this.x - cameraX, this.y, this.facing, !this.grounded);
    }
}

class Goomba {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.w = 32;
        this.h = 32;
        this.vx = -1;
        this.alive = true;
        this.animFrame = 0;
    }

    update(map) {
        if (!this.alive) return;
        this.x += this.vx;
        this.animFrame++;

        for (let b of map) {
            if (b.type === 'air') continue;
            if (this.x < b.x + b.w && this.x + this.w > b.x &&
                this.y < b.y + b.h && this.y + this.h > b.y) {
                this.vx *= -1;
                this.x += this.vx;
            }
        }
    }

    draw() {
        if (!this.alive) return;
        drawGoombaSprite(ctx, this.x - cameraX, this.y, this.animFrame);
    }
}

// --- Tạo Bản Đồ (Level Map Design) ---
const levelLayout = [
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                   ?                                                            ",
    "               ?  ?$?                                                           ",
    "                                                                                ",
    "                                    ---                                     |   ",
    "         ?  ?$?                    -----                                    |   ",
    "                                  -------                                  [ ]  ",
    "==================   ==================================   ======================",
    "==================   ==================================   ======================"
];

const mapBlocks = [];
const goombas = [];
let flagX = 0;

for (let r = 0; r < levelLayout.length; r++) {
    for (let c = 0; c < levelLayout[r].length; c++) {
        const char = levelLayout[r][c];
        const x = c * BLOCK_SIZE;
        const y = r * BLOCK_SIZE;

        if (char === '=') mapBlocks.push({ x, y, w: BLOCK_SIZE, h: BLOCK_SIZE, type: 'ground' });
        else if (char === '?') mapBlocks.push({ x, y, w: BLOCK_SIZE, h: BLOCK_SIZE, type: 'question', empty: false });
        else if (char === '$') mapBlocks.push({ x, y, w: BLOCK_SIZE, h: BLOCK_SIZE, type: 'brick' });
        else if (char === '-') mapBlocks.push({ x, y, w: BLOCK_SIZE, h: BLOCK_SIZE, type: 'pipe' });
        else if (char === '|') {
            flagX = x;
            mapBlocks.push({ x, y, w: 10, h: BLOCK_SIZE, type: 'flagpole' });
        }
    }
}

// Thêm một số quái Goomba
goombas.push(new Goomba(400, 11 * BLOCK_SIZE - 32));
goombas.push(new Goomba(750, 11 * BLOCK_SIZE - 32));
goombas.push(new Goomba(1200, 11 * BLOCK_SIZE - 32));

const mario = new Mario();

// --- Game Loop Chính ---
function gameLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (!gameOver && !gameWon) {
        mario.update(mapBlocks);

        // Xử lý camera cuộn theo Mario
        if (mario.x - cameraX > canvas.width / 2) {
            cameraX = mario.x - canvas.width / 2;
        }

        // Cập nhật Goombas
        for (let g of goombas) {
            g.update(mapBlocks);

            // Tương tác Mario & Goomba
            if (g.alive && mario.x < g.x + g.w && mario.x + mario.w > g.x &&
                mario.y < g.y + g.h && mario.y + mario.h > g.y) {
                if (mario.vy > 0 && mario.y + mario.h - mario.vy <= g.y + 12) {
                    g.alive = false;
                    mario.vy = -7; // Bật nảy lên khi giẫm
                    score += 100;
                    playSound('stomp');
                } else {
                    gameOver = true;
                }
            }
        }

        // Kiểm tra Thắng (Cột cờ)
        if (mario.x >= flagX) {
            gameWon = true;
            playSound('win');
        }
    }

    // --- Vẽ Bản Đồ & Đối Tượng ---
    for (let b of mapBlocks) {
        if (b.x + b.w < cameraX || b.x > cameraX + canvas.width) continue;

        if (b.type === 'ground') {
            ctx.fillStyle = '#d86818';
            ctx.fillRect(b.x - cameraX, b.y, b.w, b.h);
            ctx.strokeStyle = '#000';
            ctx.strokeRect(b.x - cameraX, b.y, b.w, b.h);
        } else if (b.type === 'question') {
            ctx.fillStyle = b.empty ? '#b87040' : '#fcb040';
            ctx.fillRect(b.x - cameraX, b.y, b.w, b.h);
            ctx.strokeStyle = '#000';
            ctx.strokeRect(b.x - cameraX, b.y, b.w, b.h);
            if (!b.empty) {
                ctx.fillStyle = '#000';
                ctx.font = 'bold 18px sans-serif';
                ctx.fillText('?', b.x - cameraX + 10, b.y + 22);
            }
        } else if (b.type === 'brick') {
            ctx.fillStyle = '#b84418';
            ctx.fillRect(b.x - cameraX, b.y, b.w, b.h);
            ctx.strokeStyle = '#000';
            ctx.strokeRect(b.x - cameraX, b.y, b.w, b.h);
        } else if (b.type === 'pipe') {
            ctx.fillStyle = '#00a800';
            ctx.fillRect(b.x - cameraX, b.y, b.w, b.h);
            ctx.strokeStyle = '#000';
            ctx.strokeRect(b.x - cameraX, b.y, b.w, b.h);
        } else if (b.type === 'flagpole') {
            ctx.fillStyle = '#fff';
            ctx.fillRect(b.x - cameraX, b.y, 6, b.h);
        }
    }

    // Vẽ Goombas
    for (let g of goombas) g.draw();

    // Vẽ Mario
    mario.draw();

    // Cập nhật HUD Score
    document.getElementById('score').innerText = String(score).padStart(6, '0');
    document.getElementById('coins').innerText = String(coins).padStart(2, '0');

    // Màn hình Game Over / Victory
    if (gameOver) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#fff';
        ctx.font = 'bold 36px monospace';
        ctx.fillText("GAME OVER", canvas.width / 2 - 100, canvas.height / 2);
        ctx.font = '18px monospace';
        ctx.fillText("Tải lại trang để chơi lại", canvas.width / 2 - 130, canvas.height / 2 + 40);
    } else if (gameWon) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#22c55e';
        ctx.font = 'bold 36px monospace';
        ctx.fillText("VICTORY!", canvas.width / 2 - 80, canvas.height / 2);
        ctx.fillStyle = '#fff';
        ctx.font = '18px monospace';
        ctx.fillText("Bạn đã về đích thành công!", canvas.width / 2 - 140, canvas.height / 2 + 40);
    }

    requestAnimationFrame(gameLoop);
}

// Bắt đầu game
requestAnimationFrame(gameLoop);
</script>
</body>
</html>
