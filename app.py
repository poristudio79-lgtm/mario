<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Super Mario Bros - Peaceful Journey?</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            user-select: none;
        }
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
        canvas {
            display: block;
            background: #5c94fc;
            transition: filter 0.5s ease;
        }
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
            font-size: 16px;
            font-weight: bold;
            background: rgba(0,0,0,0.6);
            padding: 6px 16px;
            border-radius: 20px;
            text-shadow: 1px 1px #000;
            letter-spacing: 1px;
            z-index: 10;
            transition: all 0.3s ease;
        }
        .horror-hud {
            color: #ff3333 !important;
            border: 1px solid #ff3333;
            box-shadow: 0 0 10px #ff0000;
        }
        #controls-hint {
            margin-top: 15px;
            color: #aaa;
            font-size: 14px;
            text-align: center;
        }
    </style>
</head>
<body>

    <div id="game-wrapper">
        <div id="ui-bar">
            <div>LUIGI<br><span id="score">000000</span></div>
            <div>COINS<br>🪙 x<span id="coins">00</span></div>
            <div>WORLD<br><span id="world-title">1-1</span></div>
            <div>TIME<br><span id="timer">400</span></div>
        </div>

        <div id="hud-status">🌟 Chặng đường bình yên hướng về Lâu Đài!</div>

        <canvas id="gameCanvas" width="640" height="400"></canvas>
    </div>

    <div id="controls-hint">
        🎮 <b>Di chuyển:</b> ⬅️ ➡️ | <b>Nhảy:</b> Space / Z / ⬆️ | <b>Chạy nhanh:</b> Shift
    </div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// --- ÂM THANH SYNTHESIZER ---
const AudioContext = window.AudioContext || window.webkitAudioContext;
let audioCtx = null;

function initAudio() {
    if (!audioCtx) audioCtx = new AudioContext();
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
        } else if (type === 'glitch') {
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(80, now);
            osc.frequency.linearRampToValueAtTime(800, now + 0.3);
            gain.gain.setValueAtTime(0.25, now);
            gain.gain.linearRampToValueAtTime(0, now + 0.4);
            osc.start(now);
            osc.stop(now + 0.4);
        } else if (type === 'scream') {
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(700, now);
            osc.frequency.exponentialRampToValueAtTime(100, now + 0.8);
            gain.gain.setValueAtTime(0.3, now);
            gain.gain.linearRampToValueAtTime(0, now + 0.8);
            osc.start(now);
            osc.stop(now + 0.8);
        }
    } catch(e){}
}

// --- THUỘC TÍNH GAME & STATE ---
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

// Các phím điều khiển
const keys = { left: false, right: false, jump: false, shift: false };

window.addEventListener('keydown', e => {
    initAudio();
    if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') keys.left = true;
    if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') keys.right = true;
    if (e.key === 'Shift') keys.shift = true;
    if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W' || e.key === ' ' || e.key === 'z' || e.key === 'Z') {
        if (!keys.jump && luigi.grounded) {
            luigi.vy = -luigi.jumpPower;
            luigi.grounded = false;
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

// --- RENDER SPRITES ---
function drawLuigiSprite(ctx, x, y, facing, isJumping) {
    ctx.save();
    ctx.translate(x + 16, y + 16);
    if (facing === 'left') ctx.scale(-1, 1);

    // Mũ & Áo Xanh Lá
    ctx.fillStyle = '#00aa00';
    ctx.fillRect(-10, -16, 18, 6);
    ctx.fillRect(-8, -6, 14, 10);

    // Mặt
    ctx.fillStyle = '#fccc97';
    ctx.fillRect(-10, -10, 16, 6);

    // Râu & Mắt
    ctx.fillStyle = '#000';
    ctx.fillRect(2, -10, 3, 4);
    ctx.fillRect(-4, -6, 12, 3);

    // Quần yếm Xanh Dương
    ctx.fillStyle = '#0020c2';
    ctx.fillRect(-8, 2, 16, 8);

    // Giày Nâu
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

function drawMarioEXESprite(ctx, x, y) {
    ctx.save();
    ctx.translate(x + 16, y + 16);

    // Áo đỏ sẫm biến chất
    ctx.fillStyle = '#800000';
    ctx.fillRect(-10, -16, 18, 6);
    ctx.fillRect(-8, -6, 14, 10);

    // Mặt tái nhợt
    ctx.fillStyle = '#cfc0b0';
    ctx.fillRect(-10, -10, 16, 6);

    // Mắt Đen Chảy Máu (Cực kỳ đặc trưng của Mario.exe)
    ctx.fillStyle = '#000000';
    ctx.fillRect(-8, -10, 6, 5);
    ctx.fillRect(2, -10, 6, 5);

    // Lỗ hổng mắt có chấm đỏ rực
    ctx.fillStyle = '#ff0000';
    ctx.fillRect(-6, -8, 2, 2);
    ctx.fillRect(4, -8, 2, 2);

    // Dòng máu chảy xuống từ mắt
    ctx.fillStyle = '#990000';
    ctx.fillRect(-6, -5, 2, 6);
    ctx.fillRect(4, -5, 2, 6);

    // Nụ cười nứt nẻ rộng đến mang tai
    ctx.fillStyle = '#000000';
    ctx.fillRect(-8, -3, 16, 4);
    ctx.fillStyle = '#ffffff'; // Răng nhọn
    ctx.fillRect(-6, -3, 2, 2);
    ctx.fillRect(-2, -3, 2, 2);
    ctx.fillRect(2, -3, 2, 2);

    // Quần đen u tối
    ctx.fillStyle = '#111111';
    ctx.fillRect(-8, 2, 16, 8);

    // Giày đen
    ctx.fillStyle = '#000000';
    ctx.fillRect(-10, 10, 8, 6);
    ctx.fillRect(2, 10, 8, 6);

    ctx.restore();
}

// --- DỰNG BẢN ĐỒ ---
const levelLayout = [
    "                                                                                                    ",
    "                                                                                                    ",
    "                                                                                                    ",
    "                                                                                                    ",
    "                   ?                                                                                ",
    "               ?  ?$?                                                                               ",
    "                                                                                                    ",
    "                                    ---                                                        |    ",
    "         ?  ?$?                    -----                                                       |    ",
    "                                  -------                                                     [ ]   ",
    "==================   ==================================   ==========================================",
    "==================   ==================================   =========================================="
];

const mapBlocks = [];
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

// LUIGI OBJECT
const luigi = {
    x: 50,
    y: 200,
    w: 28,
    h: 32,
    vx: 0,
    vy: 0,
    speed: 3.5,
    jumpPower: 11,
    grounded: false,
    facing: 'right',

    update() {
        let currentSpeed = keys.shift ? this.speed * 1.4 : this.speed;

        if (keys.left) {
            this.vx = -currentSpeed;
            this.facing = 'left';
        } else if (keys.right) {
            this.vx = currentSpeed;
            this.facing = 'right';
        } else {
            this.vx = 0;
        }

        this.vy += GRAVITY;

        // Trục X Collision
        this.x += this.vx;
        for (let b of mapBlocks) {
            if (b.type === 'air' || (isHorrorPhase && b.type === 'flagpole')) continue;
            if (this.x < b.x + b.w && this.x + this.w > b.x &&
                this.y < b.y + b.h && this.y + this.h > b.y) {
                if (this.vx > 0) this.x = b.x - this.w;
                else if (this.vx < 0) this.x = b.x + b.w;
            }
        }

        // Trục Y Collision
        this.y += this.vy;
        this.grounded = false;
        for (let b of mapBlocks) {
            if (b.type === 'air' || (isHorrorPhase && b.type === 'flagpole')) continue;
            if (this.x < b.x + b.w && this.x + this.w > b.x &&
                this.y < b.y + b.h && this.y + this.h > b.y) {
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

        if (this.y > canvas.height + 60) gameOver = true;
    },

    draw() {
        drawLuigiSprite(ctx, this.x - cameraX, this.y, this.facing, !this.grounded);
    }
};

// MARIO.EXE OBJECT
const marioEXE = {
    x: 0,
    y: 0,
    w: 32,
    h: 32,
    speed: 3.2,

    update() {
        if (!exeSpawned) return;

        // Bám đuổi theo Luigi
        if (this.x < luigi.x) this.x += this.speed;
        if (this.x > luigi.x) this.x -= this.speed;
        if (this.y < luigi.y) this.y += 1;
        if (this.y > luigi.y) this.y -= 1;

        // Va chạm gây Game Over
        if (Math.abs(this.x - luigi.x) < 22 && Math.abs(this.y - luigi.y) < 26) {
            gameOver = true;
            playSound('scream');
        }
    },

    draw() {
        if (!exeSpawned) return;
        drawMarioEXESprite(ctx, this.x - cameraX, this.y);
    }
};

// --- GAME LOOP CHÍNH ---
function gameLoop() {
    ctx.save();

    // Rung màn hình khi gặp Horror
    if (shakeAmount > 0) {
        let rx = (Math.random() - 0.5) * shakeAmount;
        let ry = (Math.random() - 0.5) * shakeAmount;
        ctx.translate(rx, ry);
        shakeAmount *= 0.9;
    }

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (!gameOver && !gameWon) {
        luigi.update();
        marioEXE.update();

        // CAMERA THEO LUIGI
        if (luigi.x - cameraX > canvas.width / 2) {
            cameraX = luigi.x - canvas.width / 2;
        } else if (luigi.x - cameraX < canvas.width / 4 && cameraX > 0) {
            cameraX = luigi.x - canvas.width / 4;
        }

        // --- CÚ TWIST KHI SẮP TỚI NƠI VICTORY ---
        if (!isHorrorPhase && luigi.x >= flagX - 180) {
            // KÍCH HOẠT SỰ CỐ KINH DỊ
            isHorrorPhase = true;
            exeSpawned = true;
            marioEXE.x = flagX - 20; // Xuất hiện ngay trước Cột Cờ Victory!
            marioEXE.y = 10 * BLOCK_SIZE - 32;

            flashAlpha = 1.0;
            shakeAmount = 15;
            playSound('glitch');
            playSound('scream');

            // Cập nhật Giao diện
            document.body.style.background = '#1a0000';
            document.getElementById('hud-status').innerText = "⚠️ CỔNG CHIẾN THẮNG ĐÃ BỊ KHOÁ! CHẠY NGƯỢC LẠI NGÀY!!";
            document.getElementById('hud-status').classList.add('horror-hud');
            document.getElementById('world-title').innerText = "666";
            document.getElementById('world-title').style.color = "#ff0000";
        }

        // ĐIỀU KIỆN THẮNG MỚI (Chạy thoát ngược về phía bên trái điểm xuất phát)
        if (isHorrorPhase && luigi.x <= 20) {
            gameWon = true;
        }
    }

    // --- VẼ MÔI TRƯỜNG & MAP ---
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
            // Cột cờ biến mất khi vào Horror Phase
            ctx.fillStyle = '#fff';
            ctx.fillRect(b.x - cameraX, b.y, 6, b.h);
        }
    }

    // Draw Luigi & Mario.exe
    luigi.draw();
    marioEXE.draw();

    // HIỆU ỨNG KINH DỊ KHI ĐÃ SANG PHẦN HORROR
    if (isHorrorPhase) {
        canvas.style.background = '#120000';

        // Phủ sương đỏ máu tĩnh điện
        ctx.fillStyle = 'rgba(150, 0, 0, 0.15)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Hiệu ứng TV Glitch / Nhiễu sóng
        for (let i = 0; i < 5; i++) {
            ctx.fillStyle = `rgba(255, 0, 0, ${Math.random() * 0.2})`;
            ctx.fillRect(0, Math.random() * canvas.height, canvas.width, Math.random() * 4);
        }
    }

    // Flash chớp màn hình đỏ khi Mario.exe vừa hiện ra
    if (flashAlpha > 0) {
        ctx.fillStyle = `rgba(255, 0, 0, ${flashAlpha})`;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        flashAlpha -= 0.05;
    }

    // HUD Tracker
    document.getElementById('score').innerText = String(score).padStart(6, '0');
    document.getElementById('coins').innerText = String(coins).padStart(2, '0');

    // OVERLAYS (Thắng/Thua)
    if (gameOver) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.88)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#ff0000';
        ctx.font = 'bold 42px monospace';
        ctx.fillText("YOU DIED", canvas.width / 2 - 100, canvas.height / 2 - 10);
        ctx.fillStyle = '#aaa';
        ctx.font = '16px monospace';
        ctx.fillText("Mario.exe đã bắt được bạn...", canvas.width / 2 - 130, canvas.height / 2 + 30);
        ctx.fillText("Nhấn F5 / Tải lại trang để thử lại!", canvas.width / 2 - 150, canvas.height / 2 + 60);
    } else if (gameWon) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.85)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#22c55e';
        ctx.font = 'bold 36px monospace';
        ctx.fillText("ESCAPED!", canvas.width / 2 - 80, canvas.height / 2 - 10);
        ctx.fillStyle = '#fff';
        ctx.font = '16px monospace';
        ctx.fillText("Bạn đã thoát khỏi cơn ác mộng của Mario.exe thành công!", canvas.width / 2 - 220, canvas.height / 2 + 30);
    }

    ctx.restore();
    requestAnimationFrame(gameLoop);
}

// Chạy Game
requestAnimationFrame(gameLoop);
</script>
</body>
</html>
