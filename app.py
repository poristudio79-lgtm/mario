import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Mario vs Mario.exe - Dark Drill Edition", layout="centered")

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
        canvas { display: block; background: #5c94fc; transition: background 0.8s ease; }
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
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            padding: 12px 28px;
            font-size: 20px;
            font-weight: bold;
            font-family: 'Courier New', Courier, monospace;
            color: #fff;
            background: #e52521;
            border: 3px solid #fff;
            border-radius: 8px;
            cursor: pointer;
            z-index: 50;
            box-shadow: 0 0 15px rgba(255, 0, 0, 0.7);
        }
        #retry-btn:hover { background: #ff0000; transform: translateX(-50%) scale(1.08); }

        #intro-overlay {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.96);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 20px;
            z-index: 50;
        }
        .mario-logo {
            font-size: 42px;
            font-weight: 900;
            font-family: 'Arial Black', Gadget, sans-serif;
            letter-spacing: 2px;
            margin-bottom: 15px;
            text-shadow: 3px 3px #000;
            display: flex;
            gap: 4px;
        }
        .c-blue { color: #002db3; }
        .c-yellow { color: #ffcc00; }
        .c-red { color: #e52521; }
        .c-green { color: #22c55e; }

        #intro-desc {
            font-size: 13px;
            color: #ddd;
            max-width: 480px;
            line-height: 1.5;
            margin-bottom: 20px;
        }
        .menu-buttons {
            display: flex;
            gap: 12px;
        }
        #start-btn, #howtoplay-btn, #easy-btn, #hard-btn {
            padding: 11px 24px;
            font-size: 16px;
            font-weight: bold;
            font-family: 'Courier New', Courier, monospace;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            box-shadow: 0 0 10px rgba(0,0,0,0.5);
        }
        #start-btn { color: #000; background: #ffcc00; }
        #start-btn:hover { background: #fff; transform: scale(1.05); }

        #howtoplay-btn { color: #fff; background: #22c55e; }
        #howtoplay-btn:hover { background: #16a34a; transform: scale(1.05); }

        #difficulty-screen {
            display: none;
            flex-direction: column;
            align-items: center;
            gap: 15px;
        }
        #easy-btn { color: #000; background: #22c55e; }
        #easy-btn:hover { background: #16a34a; transform: scale(1.05); }

        #hard-btn { color: #fff; background: #e52521; }
        #hard-btn:hover { background: #ff0000; transform: scale(1.05); }

        #instructions-modal {
            display: none;
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(10, 10, 15, 0.95);
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 25px;
            z-index: 60;
        }
        #instructions-modal h2 {
            color: #ffcc00;
            font-size: 22px;
            margin-bottom: 12px;
            text-shadow: 2px 2px #ff0000;
        }
        .instruction-content {
            font-size: 13px;
            color: #e2e8f0;
            max-width: 480px;
            line-height: 1.6;
            text-align: left;
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #444;
            margin-bottom: 20px;
        }
        #back-menu-btn {
            padding: 10px 24px;
            font-size: 15px;
            font-weight: bold;
            font-family: 'Courier New', Courier, monospace;
            color: #fff;
            background: #e52521;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }
        #back-menu-btn:hover { background: #ff0000; transform: scale(1.05); }
    </style>
</head>
<body>

    <div id="game-wrapper">
        <div id="intro-overlay">
            <div class="mario-logo">
                <span class="c-blue">S</span><span class="c-yellow">U</span><span class="c-red">P</span><span class="c-green">E</span><span class="c-yellow">R</span>
            </div>
            <div class="mario-logo" style="margin-top: -15px; margin-bottom: 15px;">
                <span class="c-red">M</span><span class="c-green">A</span><span class="c-yellow">R</span><span class="c-blue">I</span><span class="c-green">O</span>
            </div>
            <div id="intro-desc">
                Phiên bản Dark Drill Edition!<br>
                Chọn độ khó (Chế độ Khó đã được tinh chỉnh lại vừa tay hơn).
            </div>

            <div id="main-menu-buttons" class="menu-buttons">
                <button id="start-btn" onclick="showDifficultyMenu()">▶️ BẮT ĐẦU</button>
                <button id="howtoplay-btn" onclick="openHowToPlay()">📖 HƯỚNG DẪN</button>
            </div>

            <div id="difficulty-screen">
                <div style="font-size: 16px; font-weight: bold; color: #ffcc00; margin-bottom: 5px;">CHỌN ĐỘ KHÓ:</div>
                <div class="menu-buttons">
                    <button id="easy-btn" onclick="initGame('easy')">🟢 DỄ</button>
                    <button id="hard-btn" onclick="initGame('hard')">🔴 KHÓ</button>
                </div>
            </div>
        </div>

        <div id="instructions-modal">
            <h2>📖 HƯỚNG DẪN CÁCH CHƠI</h2>
            <div class="instruction-content">
                <b>1. Điều khiển cơ bản:</b><br>
                • Di chuyển: Phím mũi tên <b>Trái / Phải</b> (hoặc <b>A / D</b>)<br>
                • Nhảy: Phím <b>Space</b>, <b>Z</b> hoặc mũi tên <b>Lên / W</b><br>
                • Chạy nhanh: Giữ phím <b>Shift</b><br><br>
                <b>2. Mục tiêu trò chơi:</b><br>
                • Chế độ Dễ: Thoải mái, ít cản trở.<br>
                • Chế độ Khó: Đã được cân bằng lại, thử thách vừa phải.<br>
                • Tiêu diệt phản diện và chạm cột cờ gặp Công chúa Peach!
            </div>
            <button id="back-menu-btn" onclick="closeHowToPlay()">↩️ TRỞ VỀ MENU</button>
        </div>

        <div id="ui-bar">
            <div>MARIO<br><span id="score">000000</span></div>
            <div>COINS<br>🪙 x<span id="coins">00</span></div>
            <div>WORLD<br><span id="world-title">1-1</span></div>
        </div>

        <button id="music-btn" onclick="toggleMusic()">🔊 Nhạc nền: BẬT</button>

        <div id="dialog-box">
            <div id="dialog-speaker">😈 MARIO.EXE:</div>
            <div id="dialog-text">"Ngươi nghĩ mình có thể cứu được công chúa sao? Hãy chứng tỏ bản lĩnh đàn ông đi!"</div>
        </div>

        <div id="hud-status">🌟 Chặng đường thử thách hướng về Lâu Đài!</div>
        <canvas id="gameCanvas" width="640" height="400"></canvas>
        
        <button id="retry-btn" onclick="resetGame()">🔄 TRY AGAIN</button>
    </div>

    <div id="controls-hint">
        🎮 <b>Di chuyển:</b> ⬅️ ➡️ | <b>Nhảy:</b> Space / Z / ⬆️ | <b>Chạy nhanh:</b> Shift
    </div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const retryBtn = document.getElementById('retry-btn');
const musicBtn = document.getElementById('music-btn');
const introOverlay = document.getElementById('intro-overlay');
const instructionsModal = document.getElementById('instructions-modal');
const dialogBox = document.getElementById('dialog-box');
const mainMenuButtons = document.getElementById('main-menu-buttons');
const difficultyScreen = document.getElementById('difficulty-screen');

const AudioContext = window.AudioContext || window.webkitAudioContext;
let audioCtx = null;
let isMusicMuted = false;
let gameStarted = false;
let currentDifficulty = 'easy';
let bgMusicInterval = null;

function initAudio() {
    if (!audioCtx) audioCtx = new AudioContext();
    if (audioCtx.state === 'suspended') audioCtx.resume();
}

function showDifficultyMenu() {
    initAudio();
    mainMenuButtons.style.display = 'none';
    difficultyScreen.style.display = 'flex';
}

function openHowToPlay() {
    instructionsModal.style.display = 'flex';
}

function closeHowToPlay() {
    instructionsModal.style.display = 'none';
}

function toggleMusic() {
    initAudio();
    isMusicMuted = !isMusicMuted;
    if (isMusicMuted) {
        musicBtn.innerText = "🔇 Nhạc nền: TẮT";
        stopBGM();
    } else {
        musicBtn.innerText = "🔊 Nhạc nền: BẬT";
        if (isHorrorPhase && !gameOver && !gameWon) {
            startBGM();
        }
    }
}

function startBGM() {
    if (isMusicMuted || bgMusicInterval) return;
    const notes = [130.81, 155.56, 174.61, 196.00, 220.00, 261.63, 311.13];
    let step = 0;
    bgMusicInterval = setInterval(() => {
        if (!audioCtx || isMusicMuted || gameOver || gameWon) return;
        try {
            const now = audioCtx.currentTime;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);

            osc.type = 'sawtooth';
            let freq = notes[step % notes.length];
            osc.frequency.setValueAtTime(freq, now);
            gain.gain.setValueAtTime(0.08, now);
            gain.gain.linearRampToValueAtTime(0, now + 0.18);
            osc.start(now);
            osc.stop(now + 0.18);
            step++;
        } catch(e){}
    }, 200);
}

function stopBGM() {
    if (bgMusicInterval) {
        clearInterval(bgMusicInterval);
        bgMusicInterval = null;
    }
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
let maxMapWidth = 0;
let isHorrorPhase = false;
let isCutscene = false;
let exeSpawned = false;
let exeDefeated = false;
let gameOver = false;
let gameWon = false;
let flashAlpha = 0;
let shakeAmount = 0;
let animFrame = 0;

let isStabbing = false;
let stabTimer = 0;
let swordX = 220;
let swordY = 260;

let activeCoins = [];
let mapBlocks = [];
let spikes = [];
let goombas = [];
let flagpoleObj = null;
let flagX = 0;

const keys = { left: false, right: false, jump: false, shift: false };

window.addEventListener('keydown', e => {
    if (!gameStarted || isStabbing || isCutscene || instructionsModal.style.display === 'flex' || gameOver || gameWon) return;
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
    ctx.fillStyle = '#ffff00';
    ctx.fillRect(-6, 3, 3, 3);
    ctx.fillRect(3, 3, 3, 3);

    ctx.fillStyle = '#ffffff';
    ctx.fillRect(-12, 3, 4, 5);
    ctx.fillRect(8, 3, 4, 5);

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
    if (exeDefeated) return;
    ctx.save();
    ctx.translate(x + 16, y + 16);

    ctx.fillStyle = '#8b0000';
    ctx.fillRect(-10, -16, 18, 6);
    ctx.fillRect(-12, -12, 20, 6);

    ctx.fillStyle = '#0a0a0a';
    ctx.fillRect(-10, -8, 16, 10);

    ctx.fillStyle = '#ff0000';
    ctx.fillRect(-6, -7, 3, 4);
    ctx.fillRect(2, -7, 3, 4);
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(-5, -6, 1, 2);
    ctx.fillRect(3, -6, 1, 2);

    ctx.fillStyle = '#000000';
    ctx.fillRect(-8, -3, 16, 4);

    ctx.fillStyle = '#7a0000';
    ctx.fillRect(-10, 2, 20, 8);
    ctx.fillStyle = '#1b4d8a';
    ctx.fillRect(-8, 6, 16, 6);
    ctx.fillStyle = '#ffcc00';
    ctx.fillRect(-5, 7, 2, 2);
    ctx.fillRect(3, 7, 2, 2);

    ctx.fillStyle = '#ff3333';
    ctx.fillRect(-14, 4, 5, 5);
    ctx.fillRect(9, 4, 5, 5);

    ctx.fillStyle = '#3a3a22';
    let legOffset = Math.sin(animFrame * 0.4) * 5;
    ctx.fillRect(-10 + legOffset, 12, 8, 4);
    ctx.fillRect(2 - legOffset, 12, 8, 4);

    ctx.restore();
}

function drawMarioEXEJumpscare(ctx, cx, cy) {
    ctx.save();
    ctx.translate(cx, cy);
    ctx.scale(3.2, 3.2);

    ctx.fillStyle = '#6e0a0a';
    ctx.fillRect(-25, -45, 50, 16);
    ctx.fillRect(-30, -32, 60, 14);
    ctx.fillStyle = '#fce8e6';
    ctx.fillRect(-6, -42, 12, 10);

    ctx.fillStyle = '#0f0505';
    ctx.fillRect(-32, -18, 64, 45);

    ctx.fillStyle = '#ff0000';
    ctx.fillRect(-18, -12, 10, 10);
    ctx.fillRect(8, -12, 10, 10);
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(-14, -10, 3, 4);
    ctx.fillRect(11, -10, 3, 4);

    ctx.fillStyle = '#fce8e6';
    ctx.beginPath();
    ctx.arc(0, -2, 10, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#000000';
    ctx.fillRect(-24, 6, 48, 10);

    ctx.fillStyle = '#000000';
    ctx.fillRect(-22, 16, 44, 38);

    ctx.strokeStyle = '#fce8e6';
    ctx.lineWidth = 3;
    ctx.strokeRect(-22, 16, 44, 38);

    ctx.fillStyle = '#fce8e6';
    for (let rx = -18; rx < 18; rx += 7) {
        ctx.fillRect(rx, 16, 5, 10);
    }
    for (let rx = -18; rx < 18; rx += 7) {
        ctx.fillRect(rx, 44, 5, 10);
    }

    ctx.restore();
}

function drawPrincessPixelArt(ctx, x, y) {
    ctx.save();
    ctx.translate(x, y);

    ctx.fillStyle = '#ffcc00';
    ctx.fillRect(-14, -22, 18, 24);
    ctx.fillStyle = '#e69500';
    ctx.fillRect(-16, -18, 4, 18);
    ctx.fillRect(-14, 2, 14, 8);

    ctx.fillStyle = '#ffcc00';
    ctx.fillRect(-6, -30, 12, 6);
    ctx.fillStyle = '#00cccc';
    ctx.fillRect(-5, -28, 2, 3);
    ctx.fillStyle = '#ff33cc';
    ctx.fillRect(-1, -29, 2, 4);
    ctx.fillStyle = '#00cccc';
    ctx.fillRect(3, -28, 2, 3);

    ctx.fillStyle = '#fccc97';
    ctx.fillRect(-6, -20, 12, 12);
    ctx.fillStyle = '#ffcc00';
    ctx.fillRect(-8, -24, 16, 5);

    ctx.fillStyle = '#000000';
    ctx.fillRect(-3, -16, 2, 4);
    ctx.fillRect(1, -16, 2, 4);
    ctx.fillRect(-1, -10, 2, 1);

    ctx.fillStyle = '#00cccc';
    ctx.fillRect(-8, -14, 3, 3);

    ctx.fillStyle = '#ff33cc';
    ctx.fillRect(-10, -6, 20, 14);
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(-12, -4, 4, 8);
    ctx.fillRect(8, -4, 4, 8);
    ctx.fillStyle = '#e0115f';
    ctx.fillRect(-14, 8, 28, 14);
    ctx.fillStyle = '#ff66cc';
    ctx.fillRect(-12, 12, 24, 8);

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

function drawFlagpoleAndBanner(ctx, flagpole) {
    let fx = flagpole.x - cameraX;
    let fy = flagpole.y;

    ctx.fillStyle = '#d0d0d0';
    ctx.fillRect(fx, fy, 8, flagpole.h);
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(fx, fy, 3, flagpole.h);

    ctx.fillStyle = '#ffcc00';
    ctx.beginPath();
    ctx.arc(fx + 4, fy, 8, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#e52521';
    ctx.beginPath();
    ctx.moveTo(fx + 8, fy + 8);
    ctx.lineTo(fx + 64, fy + 26);
    ctx.lineTo(fx + 8, fy + 44);
    ctx.closePath();
    ctx.fill();

    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 20px monospace';
    ctx.fillText('M', fx + 18, fy + 33);
}

function drawCastleAndPrincess(ctx) {
    let castleX = flagX - 70 - cameraX;
    let castleY = 5 * BLOCK_SIZE;

    ctx.fillStyle = isHorrorPhase ? '#4a1515' : '#b8521a';
    ctx.fillRect(castleX, castleY, 128, 128);
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 2;
    ctx.strokeRect(castleX, castleY, 128, 128);

    ctx.fillStyle = isHorrorPhase ? '#2d0b0b' : '#873600';
    for(let gx = castleX; gx < castleX + 128; gx += 16) {
        for(let gy = castleY; gy < castleY + 128; gy += 16) {
            ctx.strokeRect(gx, gy, 16, 16);
        }
    }

    ctx.fillStyle = '#ffffff';
    ctx.fillRect(castleX, castleY, 24, 16);
    ctx.fillRect(castleX + 52, castleY, 24, 16);
    ctx.fillRect(castleX + 104, castleY, 24, 16);

    ctx.fillRect(castleX, castleY + 64, 24, 16);
    ctx.fillRect(castleX + 104, castleY + 64, 24, 16);

    ctx.fillStyle = '#000000';
    ctx.beginPath();
    ctx.arc(castleX + 64, castleY + 128, 24, Math.PI, 0, false);
    ctx.fill();
    ctx.fillRect(castleX + 40, castleY + 96, 48, 32);

    ctx.fillRect(castleX + 32, castleY + 36, 16, 24);
    ctx.fillRect(castleX + 80, castleY + 36, 16, 24);

    drawPrincessPixelArt(ctx, castleX + 40, castleY + 46);
}

// KHỞI TẠO MAP THEO ĐỘ KHÓ (CHẾ ĐỘ KHÓ ĐÃ ĐƯỢC GIẢM BỚT ĐỘ GẮT CHO VỪA TAY)
function loadLevel(difficulty) {
    mapBlocks = [];
    spikes = [];
    goombas = [];
    flagpoleObj = null;

    let layout = [];
    if (difficulty === 'easy') {
        layout = [
            "                                                            ",
            "                                                            ",
            "                   ?  $?                 ?  ?$?             ",
            "               ---------                 -----              ",
            "                                                            ",
            "         ?  ?$?                         -----            |  ",
            "                                        -----            |  ",
            "        ---                                             [ ] ",
            "===================   =============   ======================",
            "===================   =============   ======================"
        ];
    } else {
        // CHẾ ĐỘ KHÓ: Đã tinh chỉnh bớt gai hiểm và giãn khoảng cách hố sâu cho vừa tay hơn
        layout = [
            "                                                                          ",
            "                                                                          ",
            "                   ?  $?                                 ?  ?$?           ",
            "               ^  ------                 ^               -----            ",
            "                                                                          ",
            "         ?  ?$?             -----       -----                        |   ",
            "                            -----       -----                        |   ",
            "        ---     ^                        ^                          [ ]  ",
            "=== == ===   === === ===   === === ===   === === ===   === === === === ===",
            "=== == ===   === === ===   === === ===   === === ===   === === === === ==="
        ];
    }

    maxMapWidth = layout[0].length * BLOCK_SIZE;

    for (let r = 0; r < layout.length; r++) {
        for (let c = 0; c < layout[r].length; c++) {
            const char = layout[r][c];
            const x = c * BLOCK_SIZE;
            const y = r * BLOCK_SIZE;

            if (char === '=') mapBlocks.push({ x, y, w: BLOCK_SIZE, h: BLOCK_SIZE, type: 'ground' });
            else if (char === '?') mapBlocks.push({ x, y, w: BLOCK_SIZE, h: BLOCK_SIZE, type: 'question', empty: false, bounce: 0 });
            else if (char === '$') mapBlocks.push({ x, y, w: BLOCK_SIZE, h: BLOCK_SIZE, type: 'brick' });
            else if (char === '-') mapBlocks.push({ x, y, w: BLOCK_SIZE, h: BLOCK_SIZE, type: 'pipe' });
            else if (char === '^') spikes.push({ x, y: y + 16, w: BLOCK_SIZE, h: 16 });
            else if (char === '|') {
                flagX = x;
                flagpoleObj = { x, y: y - 2 * BLOCK_SIZE, w: 10, h: 3 * BLOCK_SIZE };
                mapBlocks.push({ x, y, w: 10, h: BLOCK_SIZE, type: 'flagpole' });
            }
        }
    }

    if (difficulty === 'easy') {
        goombas.push({ x: 300, y: 8 * BLOCK_SIZE - 28, vx: -1, minX: 250, maxX: 400, alive: true });
    } else {
        goombas.push(
            { x: 260, y: 8 * BLOCK_SIZE - 28, vx: -1, minX: 200, maxX: 340, alive: true },
            { x: 480, y: 8 * BLOCK_SIZE - 28, vx: -1, minX: 420, maxX: 560, alive: true }
        );
    }
}

const mario = {
    x: 50, y: 200, w: 28, h: 32, vx: 0, vy: 0, speed: 3.5, jumpPower: 11, grounded: false, facing: 'right', moving: false,
    update() {
        if (isStabbing || isCutscene || gameOver || gameWon) return;

        let currentSpeed = keys.shift ? this.speed * 1.4 : this.speed;
        this.moving = false;

        if (keys.left) { this.vx = -currentSpeed; this.facing = 'left'; this.moving = true; }
        else if (keys.right) { this.vx = currentSpeed; this.facing = 'right'; this.moving = true; }
        else this.vx = 0;

        let prevY = this.y;
        this.vy += GRAVITY;

        this.x += this.vx;
        if (this.x < 0) this.x = 0;

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
                    if (b.type === 'question' && !b.empty) {
                        b.empty = true;
                        b.bounce = 6;
                        coins++;
                        score += 200;
                        playSound('coin');
                        activeCoins.push({ x: b.x + 8, y: b.y, vy: -6, alpha: 1.0 });
                    }
                }
            }
        }

        if (exeDefeated && flagpoleObj) {
            if (this.x + this.w >= flagpoleObj.x && this.x <= flagpoleObj.x + flagpoleObj.w + 20) {
                gameWon = true;
                retryBtn.style.display = 'block';
                stopBGM();
            }
        }

        for (let g of goombas) {
            if (!g.alive) continue;
            if (this.x < g.x + 28 && this.x + this.w > g.x && this.y < g.y + 28 && this.y + this.h > g.y) {
                if (this.vy > 0 && prevY + this.h <= g.y + 12) {
                    g.alive = false;
                    this.vy = -7.5;
                    score += 100;
                    playSound('stomp');
                } else {
                    triggerGameOver();
                }
            }
        }

        for (let s of spikes) {
            if (this.x < s.x + s.w && this.x + this.w > s.x && this.y < s.y + s.h && this.y + this.h > s.y) {
                triggerGameOver();
            }
        }

        if (this.y > canvas.height + 60) {
            triggerGameOver();
        }
    },
    draw() { drawMarioSprite(ctx, this.x - cameraX, this.y, this.facing, !this.grounded, this.moving); }
};

const marioEXE = {
    x: 0, y: 0, w: 32, h: 32, speed: 2.5,
    update() {
        if (!exeSpawned || exeDefeated || isStabbing || isCutscene || gameOver) return;

        if (this.x < mario.x) this.x += this.speed;
        if (this.x > mario.x) this.x -= this.speed;
        if (this.y < mario.y) this.y += 1;
        if (this.y > mario.y) this.y -= 1;

        if (Math.abs(this.x - mario.x) < 22 && Math.abs(this.y - mario.y) < 26) {
            triggerGameOver();
        }
    },
    draw() { if (exeSpawned && !exeDefeated) drawMarioEXESprite(ctx, this.x - cameraX, this.y); }
};

function initGame(difficulty) {
    initAudio();
    currentDifficulty = difficulty;
    loadLevel(currentDifficulty);

    if (currentDifficulty === 'hard') {
        marioEXE.speed = 3.2; // Đã giảm tốc độ rượt đuổi của Mario.exe ở chế độ khó cho vừa tay hơn
    } else {
        marioEXE.speed = 2.4;
    }

    introOverlay.style.display = 'none';
    gameStarted = true;
}

function triggerGameOver() {
    if (gameOver) return;
    gameOver = true;
    retryBtn.style.display = 'block';
    dialogBox.style.display = 'none';
    playSound('scream');
    stopBGM();
}

function resetGame() {
    score = 0;
    coins = 0;
    cameraX = 0;
    isHorrorPhase = false;
    isCutscene = false;
    exeSpawned = false;
    exeDefeated = false;
    gameOver = false;
    gameWon = false;
    isStabbing = false;
    stabTimer = 0;
    flashAlpha = 0;
    shakeAmount = 0;
    activeCoins = [];

    mario.x = 50;
    mario.y = 200;
    mario.vx = 0;
    mario.vy = 0;

    stopBGM();
    retryBtn.style.display = 'none';
    dialogBox.style.display = 'none';

    gameStarted = false;
    introOverlay.style.display = 'flex';
    mainMenuButtons.style.display = 'none';
    difficultyScreen.style.display = 'flex';

    document.body.style.background = '#050505';
    canvas.style.background = '#5c94fc';
    document.getElementById('hud-status').innerText = "🌟 Chặng đường thử thách hướng về Lâu Đài!";
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

        if (!isCutscene) {
            cameraX = mario.x - canvas.width / 3;
            if (cameraX < 0) cameraX = 0;
            if (cameraX > maxMapWidth - canvas.width) cameraX = maxMapWidth - canvas.width;
        }

        if (!isHorrorPhase && mario.x >= flagX - 180) {
            isHorrorPhase = true;
            isCutscene = true;
            exeSpawned = true;
            marioEXE.x = flagX - 20;
            marioEXE.y = 8 * BLOCK_SIZE - 32;

            cameraX = flagX - canvas.width / 2 + 50;

            flashAlpha = 1.0;
            shakeAmount = 18;
            playSound('scream');
            startBGM();

            dialogBox.style.display = 'block';

            setTimeout(() => {
                dialogBox.style.display = 'none';
                isCutscene = false;
            }, 5000);

            document.body.style.background = '#1a0000';
            canvas.style.background = '#120000';
            document.getElementById('hud-status').innerText = "⚠️ CINEMATIC: MARIO.EXE ĐÃ XUẤT HIỆN! HÃY TÌM KIẾM THÁNH KIẾM!";
            document.getElementById('hud-status').classList.add('horror-hud');
            document.getElementById('world-title').innerText = "DRILL";
            document.getElementById('world-title').style.color = "#ff0000";
        }

        if (isHorrorPhase && !exeDefeated && !isStabbing && Math.abs(mario.x - swordX) < 30 && Math.abs(mario.y - swordY) < 35) {
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
                exeDefeated = true;
                isStabbing = false;
                stopBGM();
                canvas.style.background = '#5c94fc';
                document.body.style.background = '#050505';
                document.getElementById('hud-status').innerText = "🚩 ĐÃ DIỆT PHẢN DIỆN! HÃY CHẠY ĐẾN CỘT CỜ GIẢI CỨU CÔNG CHÚA!";
                document.getElementById('hud-status').classList.remove('horror-hud');
                document.getElementById('world-title').innerText = "1-1";
                document.getElementById('world-title').style.color = "#fff";
            }
        }
    }

    for (let b of mapBlocks) {
        if (b.x + b.w < cameraX || b.x > cameraX + canvas.width) continue;
        
        let renderY = b.y;
        if (b.bounce > 0) {
            renderY -= Math.sin((b.bounce / 6) * Math.PI) * 8;
            b.bounce--;
        }

        if (b.type === 'ground') {
            ctx.fillStyle = (isHorrorPhase && !exeDefeated) ? '#3a0d0d' : '#d86818';
            ctx.fillRect(b.x - cameraX, renderY, b.w, b.h);
            ctx.strokeStyle = '#000';
            ctx.strokeRect(b.x - cameraX, renderY, b.w, b.h);
        } else if (b.type === 'question') {
            ctx.fillStyle = (isHorrorPhase && !exeDefeated) ? '#2a1100' : (b.empty ? '#b87040' : '#fcb040');
            ctx.fillRect(b.x - cameraX, renderY, b.w, b.h);
            ctx.strokeStyle = '#000';
            ctx.strokeRect(b.x - cameraX, renderY, b.w, b.h);
            if (!b.empty) {
                ctx.fillStyle = '#000';
                ctx.font = 'bold 18px monospace';
                ctx.fillText('?', b.x - cameraX + 10, renderY + 22);
            }
        } else if (b.type === 'brick') {
            ctx.fillStyle = (isHorrorPhase && !exeDefeated) ? '#550000' : '#b84418';
            ctx.fillRect(b.x - cameraX, renderY, b.w, b.h);
            ctx.strokeStyle = '#000';
            ctx.strokeRect(b.x - cameraX, renderY, b.w, b.h);
        } else if (b.type === 'pipe') {
            ctx.fillStyle = (isHorrorPhase && !exeDefeated) ? '#1c3a1c' : '#00a800';
            ctx.fillRect(b.x - cameraX, renderY, b.w, b.h);
            ctx.strokeStyle = '#000';
            ctx.strokeRect(b.x - cameraX, renderY, b.w, b.h);
        }
    }

    for (let i = activeCoins.length - 1; i >= 0; i--) {
        let ac = activeCoins[i];
        ac.y += ac.vy;
        ac.vy += 0.4;
        ac.alpha -= 0.03;

        ctx.save();
        ctx.globalAlpha = Math.max(0, ac.alpha);
        ctx.fillStyle = '#ffcc00';
        ctx.strokeStyle = '#b8860b';
        ctx.beginPath();
        ctx.ellipse(ac.x - cameraX, ac.y, 6, 10, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
        ctx.restore();

        if (ac.alpha <= 0) {
            activeCoins.splice(i, 1);
        }
    }

    if (flagpoleObj) {
        drawFlagpoleAndBanner(ctx, flagpoleObj);
    }

    drawCastleAndPrincess(ctx);

    for (let s of spikes) {
        if (s.x + s.w < cameraX || s.x > cameraX + canvas.width) continue;
        ctx.fillStyle = (isHorrorPhase && !exeDefeated) ? '#ff0000' : '#888';
        ctx.beginPath();
        ctx.moveTo(s.x - cameraX, s.y + s.h);
        ctx.lineTo(s.x - cameraX + s.w / 2, s.y);
        ctx.lineTo(s.x - cameraX + s.w, s.y + s.h);
        ctx.fill();
    }

    for (let g of goombas) drawGoomba(ctx, g);

    if (isHorrorPhase && !exeDefeated && !isStabbing && !gameWon) {
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

    if (!gameOver) {
        mario.draw();
        marioEXE.draw();
    }

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

    if (isHorrorPhase && !exeDefeated) {
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
        ctx.fillStyle = '#080101';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        drawMarioEXEJumpscare(ctx, canvas.width / 2, canvas.height / 2 - 20);

        ctx.fillStyle = '#ff0000';
        ctx.font = 'bold 28px monospace';
        ctx.textAlign = 'center';
        ctx.shadowColor = '#000';
        ctx.shadowBlur = 12;
        ctx.fillText("YOU DIED", canvas.width / 2, 45);
        ctx.textAlign = 'left';
    } else if (gameWon) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.88)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        drawPrincessPixelArt(ctx, canvas.width / 2, canvas.height / 2 - 20);

        ctx.fillStyle = '#22c55e';
        ctx.font = 'bold 30px monospace';
        ctx.textAlign = 'center';
        ctx.fillText("VICTORY! PRINCESS SAVED!", canvas.width / 2, canvas.height / 2 + 50);
        ctx.fillStyle = '#ffffff';
        ctx.font = '14px monospace';
        ctx.fillText("Bạn đã vượt qua thử thách thành công, tiêu diệt Mario.exe và cứu công chúa Peach!", canvas.width / 2, canvas.height / 2 + 80);
        ctx.textAlign = 'left';
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
