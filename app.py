import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Mario vs Mario.exe - Hồng Nhan Drill", layout="centered")

html_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
        body {
            background-color: #050505;
            color: #fff;
            font-family: 'Courier New', Courier, monospace;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            overflow: hidden;
        }
        #game-wrapper {
            position: relative;
            box-shadow: 0 10px 40px rgba(0,0,0,0.9);
            border: 4px solid #fff;
            border-radius: 6px;
            overflow: hidden;
        }
        canvas { display: block; background: #5c94fc; }
        #ui-bar {
            position: absolute;
            top: 10px;
            left: 20px;
            right: 20px;
            display: flex;
            justify-content: space-between;
            font-size: 18px;
            font-weight: bold;
            text-shadow: 2px 2px #000;
            z-index: 10;
        }
        #hud-status {
            position: absolute;
            bottom: 15px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 13px;
            font-weight: bold;
            background: rgba(0,0,0,0.8);
            padding: 8px 18px;
            border-radius: 20px;
            text-shadow: 1px 1px #000;
            z-index: 10;
            white-space: nowrap;
            max-width: 90%;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .horror-hud {
            color: #ff3333 !important;
            border: 1px solid #ff3333;
            box-shadow: 0 0 12px #ff0000;
            animation: pulse-red 1s infinite alternate;
        }
        @keyframes pulse-red {
            from { box-shadow: 0 0 5px #ff0000; }
            to { box-shadow: 0 0 18px #ff0000; }
        }
        #controls-hint {
            margin-top: 12px;
            color: #aaa;
            font-size: 14px;
            text-align: center;
        }

        #dialog-box {
            display: none;
            position: absolute;
            top: 30%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(20, 0, 0, 0.95);
            border: 3px solid #ff0000;
            border-radius: 8px;
            padding: 16px;
            width: 80%;
            text-align: center;
            z-index: 40;
            box-shadow: 0 0 20px #ff0000;
        }
        #dialog-speaker {
            color: #ff3333;
            font-weight: bold;
            font-size: 18px;
            margin-bottom: 8px;
        }
        #dialog-text {
            color: #ffffff;
            font-size: 15px;
            line-height: 1.5;
            font-weight: bold;
        }

        #music-btn {
            position: absolute;
            top: 55px;
            right: 20px;
            background: rgba(0, 0, 0, 0.8);
            border: 2px solid #fff;
            color: #fff;
            padding: 6px 14px;
            font-size: 13px;
            font-weight: bold;
            border-radius: 6px;
            cursor: pointer;
            z-index: 30;
            font-family: 'Courier New', Courier, monospace;
        }
        #music-btn:hover { background: rgba(255, 255, 255, 0.3); }

        #retry-btn {
            display: none;
            position: absolute;
            top: 65%;
            left: 50%;
            transform: translate(-50%, -50%);
            padding: 12px 28px;
            font-size: 20px;
            font-weight: bold;
            font-family: 'Courier New', Courier, monospace;
            color: #fff;
            background: #e52521;
            border: 3px solid #fff;
            border-radius: 8px;
            cursor: pointer;
            z-index: 30;
            box-shadow: 0 0 15px rgba(255, 0, 0, 0.7);
        }
        #retry-btn:hover { background: #ff0000; transform: translate(-50%, -50%) scale(1.08); }

        #intro-overlay {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.92);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 20px;
            z-index: 50;
        }
        #intro-title {
            font-size: 26px;
            color: #ffcc00;
            margin-bottom: 15px;
            text-shadow: 2px 2px #ff0000;
        }
        #intro-desc {
            font-size: 15px;
            color: #ddd;
            max-width: 500px;
            line-height: 1.6;
            margin-bottom: 25px;
        }
        #start-btn {
            padding: 12px 30px;
            font-size: 18px;
            font-weight: bold;
            font-family: 'Courier New', Courier, monospace;
            color: #000;
            background: #ffcc00;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            box-shadow: 0 0 10px #ffcc00;
        }
        #start-btn:hover { background: #fff; transform: scale(1.05); }
    </style>
</head>
<body>

    <div id="game-wrapper">
        <div id="intro-overlay">
            <div id="intro-title">🎬 WORLD 1-1: PEACEFUL JOURNEY</div>
            <div id="intro-desc">
                Mario đang trên đường trở về Lâu Đài chiến thắng trong một ngày nắng đẹp bình yên.<br><br>
                Hãy giúp Mario nhảy dẫm đè bẹp các con nấm, vượt qua hố sâu để tiến về Cột Cờ...<br>
                <b>Cho đến khi điều không ngờ xảy ra!</b>
            </div>
            <button id="start-btn" onclick="startGame()">▶️ BẮT ĐẦU CHƠI</button>
        </div>

        <div id="ui-bar">
            <div>MARIO<br><span id="score">000000</span></div>
            <div>COINS<br>🪙 x<span id="coins">00</span></div>
            <div>WORLD<br><span id="world-title">1-1</span></div>
        </div>

        <button id="music-btn" onclick="toggleMusic()">🔊 Hồng Nhan Drill: BẬT</button>

        <div id="dialog-box">
            <div id="dialog-speaker">😈 MARIO.EXE:</div>
            <div id="dialog-text">"Ngươi là kẻ yếu nhất ta từng thấy! Hãy chứng tỏ ngươi là một người đàn ông để giải cứu công chúa!"</div>
        </div>

        <div id="hud-status">🌟 Chặng đường bình yên hướng về Lâu Đài!</div>
        <canvas id="gameCanvas" width="640" height="400"></canvas>
        
        <button id="retry-btn" onclick="resetGame()">🔄 TRY AGAIN</button>
    </div>

    <div id="controls-hint">
        🎮 <b>Di chuyển:</b> ⬅️ ➡️ | <b>Nhảy:</b> Space / Z / ⬆️ | <b>Chạy nhanh:</b> Shift
    </div>

    <audio id="drillAudio" loop preload="auto">
        <source src="https://files.catbox.moe/k3t2p4.mp3" type="audio/mpeg">
    </audio>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const retryBtn = document.getElementById('retry-btn');
const musicBtn = document.getElementById('music-btn');
const drillAudio = document.getElementById('drillAudio');
const introOverlay = document.getElementById('intro-overlay');
const dialogBox = document.getElementById('dialog-box');

const AudioContext = window.AudioContext || window.webkitAudioContext;
let audioCtx = null;
let isMusicMuted = false;
let gameStarted = false;

function initAudio() {
    if (!audioCtx) audioCtx = new AudioContext();
    if (audioCtx.state === 'suspended') audioCtx.resume();
}

function startGame() {
    initAudio();
    introOverlay.style.display = 'none';
    gameStarted = true;
}

function toggleMusic() {
    initAudio();
    isMusicMuted = !isMusicMuted;
    if (isMusicMuted) {
        musicBtn.innerText = "🔇 Hồng Nhan Drill: TẮT";
        drillAudio.pause();
    } else {
        musicBtn.innerText = "🔊 Hồng Nhan Drill: BẬT";
        if (isHorrorPhase && !gameOver && !gameWon) {
            drillAudio.play().catch(e => {});
        }
    }
}

function startHongNhanDrill() {
    if (!isMusicMuted) {
        drillAudio.currentTime = 0;
        drillAudio.play().catch(e => {});
    }
}

function stopHongNhanDrill() {
    drillAudio.pause();
    drillAudio.currentTime = 0;
}

function playSound(type) {
    if (!audioCtx) return;
    try {
        const now = audioCtx.currentTime;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);

        if (type === 'jump') {
            osc.type = 'square';
            osc.frequency.setValueAtTime(160, now);
            osc.frequency.exponentialRampToValueAtTime(550, now + 0.15);
            gain.gain.setValueAtTime(0.1, now);
            gain.gain.linearRampToValueAtTime(0, now + 0.15);
            osc.start(now);
            osc.stop(now + 0.15);
        } else if (type === 'coin') {
            osc.type = 'sine';
            osc.frequency.setValueAtTime(987.77, now);
            osc.frequency.setValueAtTime(1318.51, now + 0.08);
            gain.gain.setValueAtTime(0.12, now);
            gain.gain.linearRampToValueAtTime(0, now + 0.25);
            osc.start(now);
            osc.stop(now + 0.25);
        } else if (type === 'stomp') {
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(300, now);
            osc.frequency.linearRampToValueAtTime(80, now + 0.12);
            gain.gain.setValueAtTime(0.2, now);
            gain.gain.linearRampToValueAtTime(0, now + 0.12);
            osc.start(now);
            osc.stop(now + 0.12);
        } else if (type === 'scream') {
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(650, now);
            osc.frequency.exponentialRampToValueAtTime(90, now + 0.9);
            gain.gain.setValueAtTime(0.35, now);
            gain.gain.linearRampToValueAtTime(0, now + 0.9);
            osc.start(now);
            osc.stop(now + 0.9);
        } else if (type === 'slash') {
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(1200, now);
            osc.frequency.exponentialRampToValueAtTime(100, now + 0.4);
            gain.gain.setValueAtTime(0.4, now);
            gain.gain.linearRampToValueAtTime(0, now + 0.4);
            osc.start(now);
            osc.stop(now + 0.4);
        }
    } catch(e){}
}

const GRAVITY = 0.48;
const BLOCK_SIZE = 32;

let score = 0;
let coins = 0;
let cameraX = 0;
let isHorrorPhase = false;
let exeSpawned = false;
let gameOver = false;
let gameWon = false;
let flashAlpha = 0;
let shakeAmount = 0;
let animFrame = 0;

let isStabbing = false;
let stabTimer = 0;
let swordX = 320;
let swordY = 260;

const keys = { left: false, right: false, jump: false, shift: false };

window.addEventListener('keydown', e => {
    if (!gameStarted || isStabbing) return;
    initAudio();
    if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') keys.left = true;
    if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') keys.right = true;
    if (e.key === 'Shift') keys.shift = true;
    if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W' || e.key === ' ' || e.key === 'z' || e.key === 'Z') {
        if (!keys.jump && mario.grounded) {
            mario.vy = -mario.jumpPower;
            mario.grounded = false;
            playSound('jump');
        }
        keys.jump = true;
    }
});

window.addEventListener('keyup', e => {
    if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') keys.left = false;
    if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') keys.right = false;
    if (e.key === 'Shift') keys.shift = false;
    if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W' || e.key === ' ' || e.key === 'z' || e.key === 'Z') keys.jump = false;
});

function drawMarioSprite(ctx, x, y, facing, isJumping, moving) {
    ctx.save();
    ctx.translate(x + 16, y + 16);
    if (facing === 'left') ctx.scale(-1, 1);

    ctx.fillStyle = '#ff0000';
    ctx.fillRect(-10, -16, 18, 6);
    ctx.fillRect(-8, -6, 14, 10);

    ctx.fillStyle = '#fccc97';
    ctx.fillRect(-10, -10, 16, 6);

    ctx.fillStyle = '#000';
    ctx.fillRect(2, -10, 3, 4);
    ctx.fillRect(-4, -6, 12, 3);

    ctx.fillStyle = '#0020c2';
    ctx.fillRect(-8, 2, 16, 8);

    ctx.fillStyle = '#8b4513';
    if (isJumping) {
        ctx.fillRect(-12, 8, 8, 6);
        ctx.fillRect(4, 6, 8, 6);
    } else if (moving) {
        let legOffset = Math.sin(animFrame * 0.3) * 5;
        ctx.fillRect(-10 + legOffset, 10, 8, 6);
        ctx.fillRect(2 - legOffset, 10, 8, 6);
    } else {
        ctx.fillRect(-10, 10, 8, 6);
        ctx.fillRect(2, 10, 8, 6);
    }
    ctx.restore();
}

function drawMarioEXESprite(ctx, x, y) {
    ctx.save();
    ctx.translate(x + 16, y + 16);

    ctx.fillStyle = '#800000';
    ctx.fillRect(-10, -16, 18, 6);
    ctx.fillRect(-8, -6, 14, 10);

    ctx.fillStyle = '#cfc0b0';
    ctx.fillRect(-10, -10, 16, 6);

    ctx.fillStyle = '#000000';
    ctx.fillRect(-8, -10, 6, 5);
    ctx.fillRect(2, -10, 6, 5);

    ctx.fillStyle = '#ff0000';
    ctx.fillRect(-6, -8, 2, 2);
    ctx.fillRect(4, -8, 2, 2);

    ctx.fillStyle = '#990000';
    ctx.fillRect(-6, -5, 2, 6);
    ctx.fillRect(4, -5, 2, 6);

    ctx.fillStyle = '#000000';
    ctx.fillRect(-8, -3, 16, 4);
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(-6, -3, 2, 2);
    ctx.fillRect(-2, -3, 2, 2);
    ctx.fillRect(2, -3, 2, 2);

    ctx.fillStyle = '#111111';
    ctx.fillRect(-8, 2, 16, 8);

    ctx.fillStyle = '#000000';
    let legOffset = Math.sin(animFrame * 0.4) * 6;
    ctx.fillRect(-10 + legOffset, 10, 8, 6);
    ctx.fillRect(2 - legOffset, 10, 8, 6);

    ctx.restore();
}

function drawGoomba(ctx, g) {
    if (!g.alive) return;
    ctx.save();
    ctx.translate(g.x - cameraX + 16, g.y + 16);
    let legOffset = Math.sin(animFrame * 0.2) * 3;

    ctx.fillStyle = isHorrorPhase ? '#4a0000' : '#8b4513';
    ctx.beginPath();
    ctx.arc(0, -2, 14, Math.PI, 0, false);
    ctx.fill();

    ctx.fillStyle = isHorrorPhase ? '#ff0000' : '#ffe4c4';
    ctx.fillRect(-10, -2, 20, 12);

    ctx.fillStyle = isHorrorPhase ? '#ff0000' : '#000';
    ctx.fillRect(-6, 0, 3, 5);
    ctx.fillRect(3, 0, 3, 5);

    ctx.fillStyle = '#000';
    ctx.fillRect(-10 + legOffset, 10, 8, 5);
    ctx.fillRect(2 - legOffset, 10, 8, 5);
    ctx.restore();
}

const levelLayout = [
    "                                                                                                                    ",
    "                                                                                                                    ",
    "                                                                                                                    ",
    "                   ?                                        ?  ?$?                                                  ",
    "               ?  ?$?                                      -----                                                    ",
    "                                                                                                                    ",
    "                                    ---       ^^^^              ---                                            |    ",
    "         ?  ?$?                    -----     ======            -----                                           |    ",
    "                                  -------   ========          -------                                         [ ]   ",
    "==================   ==========   ==================   ==================   ================   =====================",
    "==================   ==========   ==================   ==================   ================   ====================="
];

const mapBlocks = [];
const spikes = [];
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
        else if (char === '^') spikes.push({ x, y: y + 16, w: BLOCK_SIZE, h: 16 });
        else if (char === '|') {
            flagX = x;
            mapBlocks.push({ x, y, w: 10, h: BLOCK_SIZE, type: 'flagpole' });
        }
    }
}

const goombas = [
    { x: 400, y: 9 * BLOCK_SIZE - 28, vx: -1, minX: 320, maxX: 500, alive: true },
    { x: 1200, y: 9 * BLOCK_SIZE - 28, vx: -1.2, minX: 1100, maxX: 1350, alive: true },
    { x: 1800, y: 9 * BLOCK_SIZE - 28, vx: -1.5, minX: 1700, maxX: 1950, alive: true }
];

const mario = {
    x: 50, y: 200, w: 28, h: 32, vx: 0, vy: 0, speed: 3.5, jumpPower: 11, grounded: false, facing: 'right', moving: false,
    update() {
        if (isStabbing) return;

        let currentSpeed = keys.shift ? this.speed * 1.4 : this.speed;
        this.moving = false;

        if (keys.left) { this.vx = -currentSpeed; this.facing = 'left'; this.moving = true; }
        else if (keys.right) { this.vx = currentSpeed; this.facing = 'right'; this.moving = true; }
        else this.vx = 0;

        let prevY = this.y;
        this.vy += GRAVITY;

        this.x += this.vx;
        for (let b of mapBlocks) {
            if (b.type === 'air' || (isHorrorPhase && b.type === 'flagpole')) continue;
            if (this.x < b.x + b.w && this.x + this.w > b.x && this.y < b.y + b.h && this.y + this.h > b.y) {
                if (this.vx > 0) this.x = b.x - this.w;
                else if (this.vx < 0) this.x = b.x + b.w;
            }
        }

        this.y += this.vy;
        this.grounded = false;
        for (let b of mapBlocks) {
            if (b.type === 'air' || (isHorrorPhase && b.type === 'flagpole')) continue;
            if (this.x < b.x + b.w && this.x + this.w > b.x && this.y < b.y + b.h && this.y + this.h > b.y) {
                if (this.vy > 0) {
                    this.y = b.y - this.h;
                    this.vy = 0;
                    this.grounded = true;
                } else if (this.vy < 0) {
                    this.y = b.y + b.h;
                    this.vy = 0;
                    if (b.type === 'question' && !b.empty && !isHorrorPhase) {
                        b.empty = true;
                        coins++;
                        score += 200;
                        playSound('coin');
                    }
                }
            }
        }

        // KIỂM TRA VA CHẠM VỚI GOOMBA (DẪM ĐẦU VS VA CHẠM NGANG)
        for (let g of goombas) {
            if (!g.alive) continue;
            if (this.x < g.x + 28 && this.x + this.w > g.x && this.y < g.y + 28 && this.y + this.h > g.y) {
                // Nếu Mario đang rơi xuống từ trên cao và nằm phía trên nấm -> DẪM ĐỀ BẸP NẤM & TƯNG LÊN
                if (this.vy > 0 && prevY + this.h <= g.y + 12) {
                    g.alive = false;
                    this.vy = -7.5; // Tưng nảy vọt lên trên!
                    score += 100;
                    playSound('stomp');
                } else {
                    // Ngược lại nếu va hông -> Mario chết
                    gameOver = true;
                    retryBtn.style.display = 'block';
                    playSound('scream');
                    stopHongNhanDrill();
                }
            }
        }

        for (let s of spikes) {
            if (this.x < s.x + s.w && this.x + this.w > s.x && this.y < s.y + s.h && this.y + this.h > s.y) {
                gameOver = true;
                retryBtn.style.display = 'block';
                playSound('scream');
                stopHongNhanDrill();
            }
        }

        if (this.y > canvas.height + 60) {
            gameOver = true;
            retryBtn.style.display = 'block';
            dialogBox.style.display = 'none';
            stopHongNhanDrill();
        }
    },
    draw() { drawMarioSprite(ctx, this.x - cameraX, this.y, this.facing, !this.grounded, this.moving); }
};

const marioEXE = {
    x: 0, y: 0, w: 32, h: 32, speed: 3.1,
    update() {
        if (!exeSpawned || isStabbing) return;

        if (this.x < mario.x) this.x += this.speed;
        if (this.x > mario.x) this.x -= this.speed;
        if (this.y < mario.y) this.y += 1;
        if (this.y > mario.y) this.y -= 1;

        if (Math.abs(this.x - mario.x) < 22 && Math.abs(this.y - mario.y) < 26) {
            gameOver = true;
            retryBtn.style.display = 'block';
            dialogBox.style.display = 'none';
            playSound('scream');
            stopHongNhanDrill();
        }
    },
    draw() { if (exeSpawned) drawMarioEXESprite(ctx, this.x - cameraX, this.y); }
};

function resetGame() {
    score = 0;
    coins = 0;
    cameraX = 0;
    isHorrorPhase = false;
    exeSpawned = false;
    gameOver = false;
    gameWon = false;
    isStabbing = false;
    stabTimer = 0;
    flashAlpha = 0;
    shakeAmount = 0;

    mario.x = 50;
    mario.y = 200;
    mario.vx = 0;
    mario.vy = 0;

    for (let g of goombas) g.alive = true;

    stopHongNhanDrill();
    retryBtn.style.display = 'none';
    dialogBox.style.display = 'none';

    for (let b of mapBlocks) {
        if (b.type === 'question') b.empty = false;
    }

    document.body.style.background = '#050505';
    canvas.style.background = '#5c94fc';
    document.getElementById('hud-status').innerText = "🌟 Chặng đường bình yên hướng về Lâu Đài!";
    document.getElementById('hud-status').classList.remove('horror-hud');
    document.getElementById('world-title').innerText = "1-1";
    document.getElementById('world-title').style.color = "#fff";
}

function gameLoop() {
    animFrame++;
    ctx.save();

    if (shakeAmount > 0) {
        ctx.translate((Math.random() - 0.5) * shakeAmount, (Math.random() - 0.5) * shakeAmount);
        shakeAmount *= 0.9;
    }
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (gameStarted && !gameOver && !gameWon) {
        mario.update();
        marioEXE.update();

        for (let g of goombas) {
            if (!g.alive) continue;
            g.x += g.vx;
            if (g.x < g.minX || g.x > g.maxX) g.vx *= -1;
        }

        if (mario.x - cameraX > canvas.width / 2) cameraX = mario.x - cameraX - canvas.width / 2;
        else if (mario.x - cameraX < canvas.width / 4 && cameraX > 0) cameraX = mario.x - canvas.width / 4;

        if (!isHorrorPhase && mario.x >= flagX - 180) {
            isHorrorPhase = true;
            exeSpawned = true;
            marioEXE.x = flagX - 20;
            marioEXE.y = 9 * BLOCK_SIZE - 32;

            flashAlpha = 1.0;
            shakeAmount = 15;
            playSound('scream');
            startHongNhanDrill();

            dialogBox.style.display = 'block';
            setTimeout(() => { dialogBox.style.display = 'none'; }, 5000);

            document.body.style.background = '#1a0000';
            document.getElementById('hud-status').innerText = "⚠️ MARIO.EXE: 'Ngươi là kẻ yếu nhất ta từng thấy! Hãy chứng tỏ ngươi là một người đàn ông để giải cứu công chúa!'";
            document.getElementById('hud-status').classList.add('horror-hud');
            document.getElementById('world-title').innerText = "DRILL";
            document.getElementById('world-title').style.color = "#ff0000";
        }

        if (isHorrorPhase && !isStabbing && Math.abs(mario.x - swordX) < 30 && Math.abs(mario.y - swordY) < 35) {
            isStabbing = true;
            stabTimer = 0;
            playSound('slash');
            shakeAmount = 20;
            flashAlpha = 1.0;
        }

        if (isStabbing) {
            stabTimer++;
            mario.facing = 'right';
            mario.x = marioEXE.x - 22;
            mario.y = marioEXE.y;

            if (stabTimer > 60) {
                gameWon = true;
                retryBtn.style.display = 'block';
                stopHongNhanDrill();
            }
        }
    }

    for (let b of mapBlocks) {
        if (b.x + b.w < cameraX || b.x > cameraX + canvas.width) continue;
        if (b.type === 'ground') {
            ctx.fillStyle = isHorrorPhase ? '#3a0d0d' : '#d86818';
            ctx.fillRect(b.x - cameraX, b.y, b.w, b.h);
            ctx.strokeStyle = '#000';
            ctx.strokeRect(b.x - cameraX, b.y, b.w, b.h);
        } else if (b.type === 'question') {
            ctx.fillStyle = isHorrorPhase ? '#2a1100' : (b.empty ? '#b87040' : '#fcb040');
            ctx.fillRect(b.x - cameraX, b.y, b.w, b.h);
            ctx.strokeStyle = '#000';
            ctx.strokeRect(b.x - cameraX, b.y, b.w, b.h);
        } else if (b.type === 'brick') {
            ctx.fillStyle = isHorrorPhase ? '#550000' : '#b84418';
            ctx.fillRect(b.x - cameraX, b.y, b.w, b.h);
            ctx.strokeStyle = '#000';
            ctx.strokeRect(b.x - cameraX, b.y, b.w, b.h);
        } else if (b.type === 'pipe') {
            ctx.fillStyle = isHorrorPhase ? '#1c3a1c' : '#00a800';
            ctx.fillRect(b.x - cameraX, b.y, b.w, b.h);
            ctx.strokeStyle = '#000';
            ctx.strokeRect(b.x - cameraX, b.y, b.w, b.h);
        } else if (b.type === 'flagpole' && !isHorrorPhase) {
            ctx.fillStyle = '#fff';
            ctx.fillRect(b.x - cameraX, b.y, 6, b.h);
        }
    }

    for (let s of spikes) {
        ctx.fillStyle = isHorrorPhase ? '#ff0000' : '#888';
        ctx.beginPath();
        ctx.moveTo(s.x - cameraX, s.y + s.h);
        ctx.lineTo(s.x - cameraX + s.w / 2, s.y);
        ctx.lineTo(s.x - cameraX + s.w, s.y + s.h);
        ctx.fill();
    }

    for (let g of goombas) drawGoomba(ctx, g);

    if (isHorrorPhase && !isStabbing && !gameWon) {
        ctx.save();
        ctx.translate(swordX - cameraX + 10, swordY + Math.sin(animFrame * 0.1) * 4);
        ctx.fillStyle = '#ffcc00';
        ctx.shadowColor = '#ffff00';
        ctx.shadowBlur = 12;
        ctx.fillRect(-2, -18, 4, 22);
        ctx.fillRect(-7, 2, 14, 4);
        ctx.fillRect(-2, 6, 4, 6);
        ctx.restore();
    }

    mario.draw();
    marioEXE.draw();

    if (isStabbing) {
        ctx.save();
        ctx.translate(mario.x - cameraX + 16, mario.y + 16);
        ctx.fillStyle = '#ffff00';
        ctx.shadowColor = '#ff0000';
        ctx.shadowBlur = 20;
        ctx.fillRect(5, -2, 28, 5);
        ctx.fillRect(2, -6, 4, 13);
        ctx.restore();
    }

    if (isHorrorPhase) {
        canvas.style.background = '#120000';
        ctx.fillStyle = 'rgba(150, 0, 0, 0.15)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }

    if (flashAlpha > 0) {
        ctx.fillStyle = `rgba(255, 0, 0, ${flashAlpha})`;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        flashAlpha -= 0.05;
    }

    document.getElementById('score').innerText = String(score).padStart(6, '0');
    document.getElementById('coins').innerText = String(coins).padStart(2, '0');

    if (gameOver) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.88)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#ff0000';
        ctx.font = 'bold 42px monospace';
        ctx.fillText("YOU DIED", canvas.width / 2 - 100, canvas.height / 2 - 20);
    } else if (gameWon) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.88)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#22c55e';
        ctx.font = 'bold 32px monospace';
        ctx.fillText("MARIO.EXE DESTROYED!", canvas.width / 2 - 200, canvas.height / 2 - 20);
        ctx.fillStyle = '#ffffff';
        ctx.font = '16px monospace';
        ctx.fillText("Bạn đã đâm kiếm kết liễu Mario.exe và giải cứu công chúa thành công!", canvas.width / 2 - 280, canvas.height / 2 + 20);
    }

    ctx.restore();
    requestAnimationFrame(gameLoop);
}

requestAnimationFrame(gameLoop);
</script>
</body>
</html>
"""

components.html(html_code, height=520)
