import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Super Mario - Epic Shadow Edition", layout="centered")

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
        canvas { display: block; background: #5c94fc; transition: background 1s ease; }
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
            top: 25%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(10, 0, 0, 0.96);
            border: 3px solid #ff0000;
            border-radius: 8px;
            padding: 16px;
            width: 82%;
            text-align: center;
            z-index: 40;
            box-shadow: 0 0 25px #ff0000;
        }
        #dialog-speaker {
            color: #ff3333;
            font-weight: bold;
            font-size: 18px;
            margin-bottom: 8px;
            letter-spacing: 1px;
        }
        #dialog-text {
            color: #ffffff;
            font-size: 14px;
            line-height: 1.6;
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
            margin-bottom: 12px;
            text-shadow: 3px 3px #000;
            display: flex;
            gap: 4px;
        }
        .c-blue { color: #002db3; }
        .c-yellow { color: #ffcc00; }
        .c-red { color: #e52521; }
        .c-green { color: #22c55e; }

        #menu-instructions {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid #555;
            border-radius: 8px;
            padding: 12px 20px;
            margin-bottom: 20px;
            max-width: 440px;
            text-align: left;
            font-size: 13px;
            line-height: 1.5;
            color: #e2e8f0;
        }
        #menu-instructions b { color: #ffcc00; }

        .menu-buttons { display: flex; gap: 12px; }
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
            <div class="mario-logo" style="margin-top: -15px; margin-bottom: 12px;">
                <span class="c-red">M</span><span class="c-green">A</span><span class="c-yellow">R</span><span class="c-blue">I</span><span class="c-green">O</span>
            </div>
            
            <div id="menu-instructions">
                🎮 <b>HƯỚNG DẪN ĐIỀU KHIỂN:</b><br>
                • Di chuyển: Phím mũi tên <b>Trái / Phải</b> (hoặc <b>A / D</b>)<br>
                • Nhảy: Phím <b>Space</b>, <b>Z</b> hoặc mũi tên <b>Lên / W</b><br>
                • Chạy nhanh: Giữ phím <b>Shift</b>
            </div>

            <div id="main-menu-buttons" class="menu-buttons">
                <button id="start-btn" onclick="showDifficultyMenu()">▶️ BẮT ĐẦU</button>
                <button id="howtoplay-btn" onclick="openHowToPlay()">📖 LUẬT CHƠI</button>
            </div>

            <div id="difficulty-screen">
                <div style="font-size: 16px; font-weight: bold; color: #ffcc00; margin-bottom: 5px;">CHỌN ĐỘ KHÓ:</div>
                <div class="menu-buttons">
                    <button id="easy-btn" onclick="initGame('easy')">🟢 DỄ</button>
                    <button id="hard-btn" onclick="initGame('hard')">🔴 KHÓ (Cân bằng)</button>
                </div>
            </div>
        </div>

        <div id="instructions-modal">
            <h2>📖 LUẬT CHƠI CHI TIẾT</h2>
            <div class="instruction-content">
                <b>1. Mẹo thu thập xu:</b><br>
                • Nhảy đội trán lên khối `(?)` vàng rực rỡ để nhận xu.<br><br>
                <b>2. Sinh tử chiến:</b><br>
                • Tìm <b>Thánh Kiếm</b> xuất hiện ngẫu nhiên trên bản đồ.<br>
                • Khi đến lâu đài, Mario.EXE xuất hiện. Nhấp chuột vào màn hình để dùng thánh kiếm kết liễu hắn!
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
            <div id="dialog-text">"Chào đường hầm tử thần, bản sao yếu đuối! Mạng mày tới đây là hết rồi!"</div>
        </div>

        <div id="hud-status">🌟 Khám phá bản đồ & Tìm Thánh Kiếm!</div>
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
const hudStatus = document.getElementById('hud-status');

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

function openHowToPlay() { instructionsModal.style.display = 'flex'; }
function closeHowToPlay() { instructionsModal.style.display = 'none'; }

function toggleMusic() {
    initAudio();
    isMusicMuted = !isMusicMuted;
    if (isMusicMuted) {
        musicBtn.innerText = "🔇 Nhạc nền: TẮT";
        stopBGM();
    } else {
        musicBtn.innerText = "🔊 Nhạc nền: BẬT";
        startBGM();
    }
}

function startBGM() {
    if (isMusicMuted || bgMusicInterval) return;
    let step = 0;
    const cheerfulNotes = [261.63, 329.63, 392.00, 523.25, 392.00, 329.63, 293.66, 349.23, 440.00, 349.23];
    const horrorNotes = [130.81, 155.56, 174.61, 196.00, 220.00, 261.63, 311.13];

    bgMusicInterval = setInterval(() => {
        if (!audioCtx || isMusicMuted || gameOver || gameWon) return;
        try {
            const now = audioCtx.currentTime;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);

            if (!isHorrorPhase) {
                osc.type = 'triangle';
                let freq = cheerfulNotes[step % cheerfulNotes.length];
                osc.frequency.setValueAtTime(freq, now);
                gain.gain.setValueAtTime(0.06, now);
                gain.gain.linearRampToValueAtTime(0, now + 0.15);
                osc.start(now);
                osc.stop(now + 0.15);
            } else {
                osc.type = 'sawtooth';
                let freq = horrorNotes[step % horrorNotes.length];
                osc.frequency.setValueAtTime(freq, now);
                gain.gain.setValueAtTime(0.09, now);
                gain.gain.linearRampToValueAtTime(0, now + 0.18);
                osc.start(now);
                osc.stop(now + 0.18);
            }
            step++;
        } catch(e){}
    }, isHorrorPhase ? 200 : 180);
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
            osc.start(now); osc.stop(now + 0.15);
        } else if (type === 'coin') {
            osc.type = 'sine';
            osc.frequency.setValueAtTime(987.77, now);
            osc.frequency.setValueAtTime(1318.51, now + 0.08);
            gain.gain.setValueAtTime(0.12, now);
            gain.gain.linearRampToValueAtTime(0, now + 0.25);
            osc.start(now); osc.stop(now + 0.25);
        } else if (type === 'sword') {
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(440, now);
            osc.frequency.exponentialRampToValueAtTime(880, now + 0.3);
            gain.gain.setValueAtTime(0.2, now);
            gain.gain.linearRampToValueAtTime(0, now + 0.3);
            osc.start(now); osc.stop(now + 0.3);
        } else if (type === 'slash') {
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(1200, now);
            osc.frequency.exponentialRampToValueAtTime(100, now + 0.4);
            gain.gain.setValueAtTime(0.4, now);
            gain.gain.linearRampToValueAtTime(0, now + 0.4);
            osc.start(now); osc.stop(now + 0.4);
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
let exeDefeated = false;
let gameOver = false;
let gameWon = false;
let animFrame = 0;

let hasSword = false;
let swordItem = { x: 0, y: 0, w: 28, h: 28, collected: false };

let mapBlocks = [];
let goombas = [];
let flagpoleObj = null;
let flagX = 0;

const keys = { left: false, right: false, jump: false, shift: false };

window.addEventListener('keydown', e => {
    if (!gameStarted || isCutscene || instructionsModal.style.display === 'flex' || gameOver || gameWon) return;
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

canvas.addEventListener('click', e => {
    if (isHorrorPhase && hasSword && !exeDefeated) {
        exeDefeated = true;
        playSound('slash');
        dialogBox.style.display = 'none';
        hudStatus.innerText = "🏆 MARIO.EXE ĐÃ BỊ TIÊU DIỆT! HÃY CHẠY TỚI CỜ LÂU ĐÀI!";
        hudStatus.classList.remove('horror-hud');
    }
});

// Hàm vẽ chuẩn nhân vật NES Mario 8-bit theo đúng hình ảnh người dùng cung cấp
function drawMarioSprite(ctx, x, y, facing, isJumping, moving) {
    ctx.save();
    ctx.translate(x + 16, y + 16);
    if (facing === 'left') ctx.scale(-1, 1);

    const p = 2; // pixel size factor
    const R = '#e52521'; // Red
    const B = '#002db3'; // Blue
    const S = '#fccc97'; // Skin
    const H = '#8b4513'; // Hair/Boots
    const Y = '#ffcc00'; // Yellow buttons

    // Bản đồ lưới pixel chính xác chuẩn hình mẫu NES Mario
    const marioPixels = [
        "      RRRRRR        ",
        "    RRRRRRRRRR      ",
        "    HHHSSHS         ",
        "   HSHSSSHSS        ",
        "   HSHHSSSHSSS      ",
        "    HHHHSSSSS       ",
        "      SSSSS         ",
        "     B BBBB         ",
        "    BBBBYBBYB       ",
        "    BBBBBBBBB       ",
        "     BBBBBBB        ",
        "      RRRRR         ",
        "    RRRRRRRRR       ",
        "    R R R R R       ",
        "    H H   H H       ",
        "   HH H   H HH      "
    ];

    for (let r = 0; r < marioPixels.length; r++) {
        for (let c = 0; c < marioPixels[r].length; c++) {
            let char = marioPixels[r][c];
            if (char !== ' ') {
                if (char === 'R') ctx.fillStyle = R;
                else if (char === 'B') ctx.fillStyle = B;
                else if (char === 'S') ctx.fillStyle = S;
                else if (char === 'H') ctx.fillStyle = H;
                else if (char === 'Y') ctx.fillStyle = Y;
                
                ctx.fillRect((c - 8) * 1.6, (r - 8) * 1.8, 1.8, 1.8);
            }
        }
    }
    ctx.restore();
}

function drawMarioEXESprite(ctx, x, y) {
    if (exeDefeated) return;
    ctx.save();
    ctx.translate(x + 16, y + 16);
    ctx.fillStyle = '#8b0000'; ctx.fillRect(-10, -16, 18, 6);
    ctx.fillStyle = '#0a0a0a'; ctx.fillRect(-10, -8, 16, 10);
    ctx.fillStyle = '#ff0000'; ctx.fillRect(-6, -7, 3, 4); ctx.fillRect(2, -7, 3, 4);
    ctx.fillStyle = '#7a0000'; ctx.fillRect(-10, 2, 20, 8);
    ctx.restore();
}

// Vẽ gạch nền mặt đất cổ điển chuẩn NES (giống hình mẫu bản đồ)
function drawGroundBlock(ctx, x, y, w, h) {
    ctx.fillStyle = '#c84c0c';
    ctx.fillRect(x, y, w, h);
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 2;
    ctx.strokeRect(x, y, w, h);

    // Đường viền sáng góc trên & trái
    ctx.fillStyle = '#fcbc5c';
    ctx.fillRect(x + 2, y + 2, w - 4, 6);
    ctx.fillStyle = '#880000';
    ctx.fillRect(x, y + 14, w, 2);
    ctx.fillRect(x + 14, y, 2, h);
}

// Khối dấu chấm hỏi (?) siêu nét, có hiệu ứng pixel cổ điển
function drawQuestionBlock(ctx, x, y, w, h, empty) {
    if (!empty) {
        ctx.fillStyle = '#ffcc00';
        ctx.fillRect(x, y, w, h);
        ctx.strokeStyle = '#000000';
        ctx.lineWidth = 2.5;
        ctx.strokeRect(x, y, w, h);

        ctx.fillStyle = '#ffee66';
        ctx.fillRect(x + 3, y + 3, 6, 6);
        ctx.fillRect(x + w - 9, y + 3, 6, 6);

        ctx.fillStyle = '#000000';
        ctx.font = 'bold 20px "Courier New", monospace';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('?', x + w / 2, y + h / 2 + 1);
    } else {
        ctx.fillStyle = '#777777';
        ctx.fillRect(x, y, w, h);
        ctx.strokeStyle = '#333333';
        ctx.lineWidth = 2;
        ctx.strokeRect(x, y, w, h);
        ctx.fillStyle = '#555555';
        ctx.fillRect(x + 4, y + 4, w - 8, h - 8);
    }
}

function drawTraditionalBrick(ctx, x, y, w, h, empty) {
    if (!empty) {
        ctx.fillStyle = '#b8521a';
        ctx.fillRect(x, y, w, h);
        ctx.strokeStyle = '#331100';
        ctx.lineWidth = 2;
        ctx.strokeRect(x, y, w, h);

        ctx.fillStyle = '#ffcc99';
        ctx.fillRect(x + 2, y + 2, 12, 12);
        ctx.fillRect(x + 18, y + 2, 12, 12);
        ctx.fillRect(x + 2, y + 18, 12, 12);
        ctx.fillRect(x + 18, y + 18, 12, 12);

        ctx.fillStyle = '#662200';
        ctx.fillRect(x, y + 15, w, 2);
        ctx.fillRect(x + 15, y, 2, h);
    } else {
        ctx.fillStyle = '#555';
        ctx.fillRect(x, y, w, h);
        ctx.strokeStyle = '#222';
        ctx.lineWidth = 2;
        ctx.strokeRect(x, y, w, h);
    }
}

// Vẽ Lâu đài gạch chuẩn cổ điển NES kèm cờ ngôi sao đỏ trên đỉnh
function drawCastleAndPrincess(ctx) {
    let castleX = flagX - 70 - cameraX;
    let castleY = 5 * BLOCK_SIZE;

    // Thân lâu đài gạch
    ctx.fillStyle = isHorrorPhase ? '#300a0a' : '#b8521a';
    ctx.fillRect(castleX, castleY, 128, 128);
    ctx.strokeStyle = '#000'; ctx.lineWidth = 2; 
    ctx.strokeRect(castleX, castleY, 128, 128);

    // Cửa ra vào màu đen
    ctx.fillStyle = '#000000'; 
    ctx.fillRect(castleX + 40, castleY + 96, 48, 32);

    // Cửa sổ lâu đài
    ctx.fillRect(castleX + 24, castleY + 32, 20, 24);
    ctx.fillRect(castleX + 84, castleY + 32, 20, 24);

    // Cột cờ trên đỉnh lâu đài
    let poleX = castleX + 64;
    let poleY = castleY - 32;
    ctx.fillStyle = '#fff';
    ctx.fillRect(poleX - 2, poleY, 4, 32);

    // Lá cờ đỏ có ngôi sao trắng
    ctx.fillStyle = '#e52521';
    ctx.fillRect(poleX + 2, poleY + 4, 24, 16);
    ctx.fillStyle = '#fff';
    ctx.font = 'bold 12px Arial';
    ctx.fillText('★', poleX + 7, poleY + 17);
}

// Vẽ mây trắng cổ điển NES trên bầu trời
function drawClouds(ctx) {
    ctx.fillStyle = '#ffffff';
    let cloudPositions = [150, 450, 850, 1250, 1650];
    for (let cx of cloudPositions) {
        let renderX = cx - cameraX * 0.4; // Hiệu ứng Parallax nhẹ
        if (renderX > -100 && renderX < canvas.width + 100) {
            ctx.fillRect(renderX, 60, 64, 24);
            ctx.fillRect(renderX + 12, 48, 40, 12);
            ctx.fillRect(renderX + 20, 84, 24, 8);
        }
    }
}

// Vẽ lùm cây và ngọn đồi xanh chuẩn NES
function drawScenery(ctx) {
    // Ngọn đồi xanh
    ctx.fillStyle = '#00aa00';
    ctx.beginPath();
    let hillX = 220 - cameraX;
    ctx.arc(hillX, 8 * BLOCK_SIZE, 64, Math.PI, 0, false);
    ctx.fill();

    // Lùm bụi pixel
    ctx.fillStyle = '#008800';
    let bushX = 400 - cameraX;
    ctx.fillRect(bushX, 8 * BLOCK_SIZE - 24, 64, 24);
}

function drawHolySword(ctx, x, y) {
    ctx.save();
    ctx.translate(x, y);
    let glow = ctx.createRadialGradient(0, 0, 2, 0, 0, 25);
    glow.addColorStop(0, 'rgba(0, 229, 255, 0.9)');
    glow.addColorStop(0.5, 'rgba(0, 150, 255, 0.4)');
    glow.addColorStop(1, 'rgba(0, 0, 255, 0)');
    ctx.fillStyle = glow;
    ctx.beginPath(); ctx.arc(0, 0, 25, 0, Math.PI * 2); ctx.fill();

    let grad = ctx.createLinearGradient(-4, 0, 4, 0);
    grad.addColorStop(0, '#e0f7fa'); grad.addColorStop(0.5, '#00e5ff'); grad.addColorStop(1, '#00838f');
    ctx.fillStyle = grad;
    ctx.beginPath(); ctx.moveTo(0, -18); ctx.lineTo(4, -8); ctx.lineTo(3, 8); ctx.lineTo(-3, 8); ctx.lineTo(-4, -8); ctx.closePath(); ctx.fill();

    ctx.fillStyle = '#ffd700'; ctx.fillRect(-8, 8, 16, 4);
    ctx.fillStyle = '#8d6e63'; ctx.fillRect(-2, 12, 4, 7);
    ctx.fillStyle = '#ff1744'; ctx.beginPath(); ctx.arc(0, 10, 2, 0, Math.PI * 2); ctx.fill();
    ctx.restore();
}

let score = 0;
let coins = 0;
let cameraX = 0;
let maxMapWidth = 0;
let isHorrorPhase = false;
let isCutscene = false;
let exeDefeated = false;
let gameOver = false;
let gameWon = false;
let animFrame = 0;

let hasSword = false;
let swordItem = { x: 0, y: 0, w: 28, h: 28, collected: false };

let mapBlocks = [];
let goombas = [];
let flagpoleObj = null;
let flagX = 0;

const keys = { left: false, right: false, jump: false, shift: false };

window.addEventListener('keydown', e => {
    if (!gameStarted || isCutscene || instructionsModal.style.display === 'flex' || gameOver || gameWon) return;
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

canvas.addEventListener('click', e => {
    if (isHorrorPhase && hasSword && !exeDefeated) {
        exeDefeated = true;
        playSound('slash');
        dialogBox.style.display = 'none';
        hudStatus.innerText = "🏆 MARIO.EXE ĐÃ BỊ TIÊU DIỆT! HÃY CHẠY TỚI CỜ LÂU ĐÀI!";
        hudStatus.classList.remove('horror-hud');
    }
});

function loadLevel(difficulty) {
    mapBlocks = []; goombas = []; flagpoleObj = null;
    hasSword = false; swordItem.collected = false;
    isHorrorPhase = false; exeDefeated = false;
    canvas.style.background = "#5c94fc";

    let layout = [
        "                                                                ",
        "                                                                ",
        "                    ?   $?                 ?   ?$               ",
        "                ---------                 -----                 ",
        "                                                                ",
        "         ?   ?$                        -----            |       ",
        "                                     -----              |       ",
        "        ---                                            [ ]      ",
        "===================   =============   ==========================",
        "===================   =============   =========================="
    ];

    maxMapWidth = layout[0].length * BLOCK_SIZE;

    for (let r = 0; r < layout.length; r++) {
        for (let c = 0; c < layout[r].length; c++) {
            const char = layout[r][c];
            const x = c * BLOCK_SIZE;
            const y = r * BLOCK_SIZE;

            if (char === '=') mapBlocks.push({ x, y, w: BLOCK_SIZE, h: BLOCK_SIZE, type: 'ground' });
            else if (char === '?') mapBlocks.push({ x, y, w: BLOCK_SIZE, h: BLOCK_SIZE, type: 'question', empty: false });
            else if (char === '$') mapBlocks.push({ x, y, w: BLOCK_SIZE, h: BLOCK_SIZE, type: 'brick', empty: false });
            else if (char === '-') mapBlocks.push({ x, y, w: BLOCK_SIZE, h: BLOCK_SIZE, type: 'pipe' });
            else if (char === '|') {
                flagX = x;
                flagpoleObj = { x, y: y - 2 * BLOCK_SIZE, w: 10, h: 3 * BLOCK_SIZE };
            }
        }
    }

    swordItem.x = (350 + Math.floor(Math.random() * 500));
    swordItem.y = 6 * BLOCK_SIZE;
    goombas.push({ x: 300, y: 8 * BLOCK_SIZE - 28, vx: -1, alive: true });
}

const mario = {
    x: 50, y: 200, w: 28, h: 32, vx: 0, vy: 0, speed: 3.5, jumpPower: 11, grounded: false, facing: 'right', moving: false,
    update() {
        if (isCutscene || gameOver || gameWon) return;

        let currentSpeed = keys.shift ? this.speed * 1.4 : this.speed;
        this.moving = false;

        if (keys.left) { this.vx = -currentSpeed; this.facing = 'left'; this.moving = true; }
        else if (keys.right) { this.vx = currentSpeed; this.facing = 'right'; this.moving = true; }
        else this.vx = 0;

        this.vy += GRAVITY;
        this.x += this.vx; if (this.x < 0) this.x = 0;

        for (let b of mapBlocks) {
            if (this.x < b.x + b.w && this.x + this.w > b.x && this.y < b.y + b.h && this.y + this.h > b.y) {
                if (this.vx > 0) this.x = b.x - this.w;
                else if (this.vx < 0) this.x = b.x + b.w;
            }
        }

        this.y += this.vy; this.grounded = false;
        for (let b of mapBlocks) {
            if (this.x < b.x + b.w && this.x + this.w > b.x && this.y < b.y + b.h && this.y + this.h > b.y) {
                if (this.vy > 0) {
                    this.y = b.y - this.h; this.vy = 0; this.grounded = true;
                } else if (this.vy < 0) {
                    this.y = b.y + b.h; this.vy = 0;
                    if ((b.type === 'question' || b.type === 'brick') && !b.empty) {
                        b.empty = true; coins++; score += 200;
                        playSound('coin');
                    }
                }
            }
        }

        if (!swordItem.collected && this.x < swordItem.x + swordItem.w && this.x + this.w > swordItem.x && this.y < swordItem.y + swordItem.h && this.y + this.h > swordItem.y) {
            swordItem.collected = true;
            hasSword = true;
            playSound('sword');
            hudStatus.innerText = "⚔️ BẠN ĐÃ NHẶT ĐƯỢC THÁNH KIẾM! HÃY TIẾN LÊN PHÍA TRƯỚC!";
        }

        if (this.x > flagX - 350 && !isHorrorPhase) {
            isHorrorPhase = true;
            canvas.style.background = "#4a0000";
            hudStatus.innerText = "⚠️ BẦU TRỜI HÓA ĐỎ! MARIO.EXE XUẤT HIỆN!";
            hudStatus.classList.add('horror-hud');
            dialogBox.style.display = 'block';
            stopBGM();
            startBGM();
        }

        if (exeDefeated && flagpoleObj && this.x + this.w >= flagpoleObj.x) {
            gameWon = true;
            retryBtn.style.display = 'block';
            stopBGM();
        }

        if (this.y > canvas.height + 60) triggerGameOver();
    },
    draw() { drawMarioSprite(ctx, this.x - cameraX, this.y, this.facing, !this.grounded, this.moving); }
};

const marioEXE = {
    x: 0, y: 0,
    draw() {
        this.x = flagX - 180;
        this.y = 8 * BLOCK_SIZE - 32;
        drawMarioEXESprite(ctx, this.x - cameraX, this.y);
    }
};

function triggerGameOver() {
    gameOver = true;
    retryBtn.style.display = 'block';
    stopBGM();
}

function initGame(difficulty) {
    currentDifficulty = difficulty;
    gameStarted = true;
    gameOver = false; gameWon = false;
    score = 0; coins = 0;
    introOverlay.style.display = 'none';
    mario.x = 50; mario.y = 200;
    loadLevel(difficulty);
    startBGM();
}

function resetGame() {
    retryBtn.style.display = 'none';
    dialogBox.style.display = 'none';
    hudStatus.classList.remove('horror-hud');
    hudStatus.innerText = "🌟 Khám phá bản đồ & Tìm Thánh Kiếm!";
    initGame(currentDifficulty);
}

function gameLoop() {
    animFrame++;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (gameStarted) {
        mario.update();
        cameraX = mario.x - canvas.width / 3;
        if (cameraX < 0) cameraX = 0;

        // Hiệu ứng sét đánh chớp lóe khi ở pha kinh dị
        if (isHorrorPhase && !exeDefeated && Math.random() < 0.02) {
            ctx.fillStyle = "rgba(255, 255, 255, 0.8)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        }

        // Vẽ mây và phong cảnh cổ điển chuẩn NES
        drawClouds(ctx);
        drawScenery(ctx);

        // Render Blocks
        for (let b of mapBlocks) {
            if (b.type === 'ground') {
                drawGroundBlock(ctx, b.x - cameraX, b.y, b.w, b.h);
            } else if (b.type === 'question') {
                drawQuestionBlock(ctx, b.x - cameraX, b.y, b.w, b.h, b.empty);
            } else if (b.type === 'brick') {
                drawTraditionalBrick(ctx, b.x - cameraX, b.y, b.w, b.h, b.empty);
            } else if (b.type === 'pipe') {
                ctx.fillStyle = '#00aa00';
                ctx.fillRect(b.x - cameraX, b.y, b.w, b.h);
                ctx.strokeStyle = '#000'; ctx.lineWidth = 2;
                ctx.strokeRect(b.x - cameraX, b.y, b.w, b.h);
            }
        }

        if (!swordItem.collected) {
            drawHolySword(ctx, swordItem.x - cameraX + 14, swordItem.y + 14);
        }

        if (flagpoleObj) {
            ctx.fillStyle = '#fff';
            ctx.fillRect(flagpoleObj.x - cameraX, flagpoleObj.y, flagpoleObj.w, flagpoleObj.h);
        }
        drawCastleAndPrincess(ctx);

        mario.draw();
        if (isHorrorPhase) marioEXE.draw();

        document.getElementById('score').innerText = String(score).padStart(6, '0');
        document.getElementById('coins').innerText = String(coins).padStart(2, '0');
    }

    requestAnimationFrame(gameLoop);
}

gameLoop();
</script>
</body>
</html>
"""

components.html(html_code, height=520)
