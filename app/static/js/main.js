document.addEventListener("DOMContentLoaded", function() {
    console.log("Fishing Game: Logic Tách Biệt (Red = Trap)");

    const canvas = document.getElementById('fishingCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const loadingOverlay = document.getElementById('loading-overlay');
    const scoreElement = document.getElementById('score');

    // --- CẤU HÌNH LOGIC ---
    const CONFIG = {
        trapChance: 0.15,      // 15% tỉ lệ ra bẫy
        // Danh sách các skin MÀU ĐỎ (Trap)
        trapVariants: ['09', '10', '11'], 
        totalSkins: 29        // Tổng số skin từ 01 đến 29
    };

    // Tạo danh sách skin THƯỜNG (Loại bỏ 09, 10, 11 ra khỏi list thường)
    let normalVariants = [];
    for (let i = 1; i <= CONFIG.totalSkins; i++) {
        let s = i.toString().padStart(2, '0');
        if (!CONFIG.trapVariants.includes(s)) {
            normalVariants.push(s);
        }
    }

    let gameState = {
        score: 0,
        mapping: {},
        fishList: [],
        currentSequence: [],
        currentIndex: 0,
        status: 'LOADING',
        caughtFish: null,
        feedback: "",
        feedbackColor: "white",
        loadedArrowImages: {} 
    };

    const DIRECTIONS = ['up', 'down', 'left', 'right'];
    const OPPOSITES = { 'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left' };
    const KEY_MAP = {
        'ArrowUp': 'up', 'ArrowDown': 'down', 'ArrowLeft': 'left', 'ArrowRight': 'right',
        'w': 'up', 's': 'down', 'a': 'left', 'd': 'right'
    };

    // --- 1. TẢI TÀI NGUYÊN ---
    async function initGame() {
        try {
            const res = await fetch(`${ASSETS_BASE_URL}/fish_mapping.json`);
            gameState.mapping = await res.json();
            gameState.fishList = Object.keys(gameState.mapping);
            
            console.log(`Đã tải ${gameState.fishList.length} loài cá.`);
            if(loadingOverlay) loadingOverlay.style.display = 'none';
            
            startNewRound();
            drawLoop();
        } catch (e) {
            console.error(e);
            if(loadingOverlay) loadingOverlay.innerHTML = "Lỗi kết nối Server Assets!";
        }
    }

    // --- 2. TẠO DÃY MŨI TÊN (CORE LOGIC) ---
    function startNewRound() {
        gameState.status = 'PLAYING';
        gameState.caughtFish = null;
        gameState.feedback = "";
        gameState.currentIndex = 0;
        gameState.currentSequence = [];

        // Random độ dài (5-7)
        const len = Math.floor(Math.random() * 3) + 5; 
        
        for(let i=0; i<len; i++) {
            const dir = DIRECTIONS[Math.floor(Math.random() * DIRECTIONS.length)];
            
            // Random xem có phải bẫy không
            const isTrap = Math.random() < CONFIG.trapChance;
            
            let variant = "";
            
            if (isTrap) {
                // Nếu là BẪY: Lấy ngẫu nhiên trong nhóm [09, 10, 11]
                variant = CONFIG.trapVariants[Math.floor(Math.random() * CONFIG.trapVariants.length)];
            } else {
                // Nếu là THƯỜNG: Lấy ngẫu nhiên trong nhóm còn lại
                variant = normalVariants[Math.floor(Math.random() * normalVariants.length)];
            }

            gameState.currentSequence.push({
                direction: dir,
                // [QUAN TRỌNG] Nếu là Trap (Đỏ) -> Phải bấm ngược. Không thì bấm đúng.
                requiredInput: isTrap ? OPPOSITES[dir] : dir,
                isTrap: isTrap,
                imgUrl: `${ASSETS_BASE_URL}/arrows/${dir}/arrow_${dir}_${variant}.webp`
            });
        }
    }

    // --- 3. XỬ LÝ INPUT ---
    function checkInput(inputDir) {
        if (gameState.status !== 'PLAYING') return;

        const currentArrow = gameState.currentSequence[gameState.currentIndex];
        
        // So sánh nút bấm với requiredInput
        if (inputDir === currentArrow.requiredInput) {
            // ĐÚNG
            gameState.currentIndex++;
            if (gameState.currentIndex >= gameState.currentSequence.length) {
                catchFish();
            }
        } else {
            // SAI
            // Logic hiển thị thông báo lỗi cho người chơi hiểu
            let msg = "TRƯỢT!";
            if (currentArrow.isTrap) msg = "ĐỪNG TIN NÓ!"; // Bấm nhầm vào trap
            
            failRound(msg);
        }
    }

    function catchFish() {
        gameState.status = 'SUCCESS';
        gameState.feedback = "PERFECT!";
        gameState.feedbackColor = "#00ff00"; 
        
        const randomFishKey = gameState.fishList[Math.floor(Math.random() * gameState.fishList.length)];
        const fishData = gameState.mapping[randomFishKey];
        
        const img = new Image();
        img.crossOrigin = "Anonymous";
        img.src = `${ASSETS_BASE_URL}/fish/${fishData.new_file}`;
        
        gameState.caughtFish = {
            image: img,
            name: fishData.code_name
        };

        // Điểm thưởng: Dãy càng dài, càng nhiều trap thì điểm càng cao
        let bonus = gameState.currentSequence.filter(a => a.isTrap).length * 50;
        const points = 100 + (gameState.currentSequence.length * 10) + bonus;
        
        gameState.score += points;
        if(scoreElement) scoreElement.innerText = gameState.score;
        saveScore(gameState.score);

        setTimeout(startNewRound, 3000);
    }

    function failRound(msg) {
        gameState.status = 'WAITING';
        gameState.feedback = msg;
        gameState.feedbackColor = "#ff0000";
        setTimeout(startNewRound, 1000);
    }

    async function saveScore(score) {
        try {
            await fetch('/save_score', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({score: score})
            });
        } catch(e) {}
    }

    document.addEventListener('keydown', (e) => {
        if (KEY_MAP[e.key]) {
            e.preventDefault();
            checkInput(KEY_MAP[e.key]);
        }
    });

    // --- 4. HỆ THỐNG VẼ ---
    function drawImageFromUrl(ctx, url, x, y, size, isDone) {
        let img = gameState.loadedArrowImages[url];
        if (!img) {
            img = new Image();
            img.crossOrigin = "Anonymous";
            img.src = url;
            gameState.loadedArrowImages[url] = img;
        }

        if (img.complete) {
            ctx.save();
            if (isDone) {
                ctx.globalAlpha = 0.3; // Mờ đi khi đã bấm xong
                ctx.filter = "grayscale(100%)";
            }
            ctx.drawImage(img, x, y, size, size);
            ctx.restore();
        }
    }

    function drawLoop() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Background
        const gradient = ctx.createLinearGradient(0, 0, 0, 600);
        gradient.addColorStop(0, "#87CEEB");
        gradient.addColorStop(1, "#006994");
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Dây câu
        ctx.beginPath();
        ctx.moveTo(400, 0);
        ctx.lineTo(400, 400);
        ctx.strokeStyle = "rgba(255,255,255,0.6)";
        ctx.lineWidth = 2;
        ctx.stroke();

        // Vẽ dãy mũi tên
        if (gameState.status === 'PLAYING' || gameState.status === 'WAITING') {
            const arrowSize = 64;
            const gap = 15;
            const totalWidth = gameState.currentSequence.length * (arrowSize + gap);
            const startX = (canvas.width - totalWidth) / 2;

            gameState.currentSequence.forEach((arrow, index) => {
                const x = startX + index * (arrowSize + gap);
                const y = 100;
                const isDone = index < gameState.currentIndex;
                
                drawImageFromUrl(ctx, arrow.imgUrl, x, y, arrowSize, isDone);
                
                // Khung highlight mũi tên đang cần bấm
                if (index === gameState.currentIndex && gameState.status === 'PLAYING') {
                    ctx.strokeStyle = "gold";
                    ctx.lineWidth = 4;
                    ctx.strokeRect(x - 5, y - 5, arrowSize + 10, arrowSize + 10);
                }
            });
        }

        // Vẽ Cá & Thông báo
        if (gameState.status === 'SUCCESS' && gameState.caughtFish && gameState.caughtFish.image.complete) {
            ctx.drawImage(gameState.caughtFish.image, 300, 350, 200, 150);
            ctx.fillStyle = "white";
            ctx.font = "bold 24px Arial";
            ctx.textAlign = "center";
            ctx.fillText(gameState.caughtFish.name, 400, 530);
        }

        if (gameState.feedback) {
            ctx.fillStyle = gameState.feedbackColor;
            ctx.font = "900 50px Arial";
            ctx.textAlign = "center";
            ctx.strokeStyle = "black";
            ctx.lineWidth = 4;
            ctx.strokeText(gameState.feedback, 400, 250);
            ctx.fillText(gameState.feedback, 400, 250);
        }

        requestAnimationFrame(drawLoop);
    }

    initGame();
});