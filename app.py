import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Jogo do Pontinho",
    page_icon="🃏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Remove cabeçalhos, rodapés e margens do Streamlit para ocupar 100% da tela do celular
st.markdown("""
    <style>
        #MainMenu, header, footer, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {
            display: none !important;
            visibility: hidden !important;
        }
        .block-container, .stMainBlockContainer {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        iframe {
            width: 100vw !important;
            height: 100dvh !important;
            border: none !important;
            display: block !important;
        }
        body, html {
            overflow: hidden !important;
            margin: 0 !important;
            padding: 0 !important;
            background-color: #f8fafc !important;
        }
    </style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Jogo do Pontinho</title>
<style>
  :root {
    --bg: #f8fafc;
    --card: #ffffff;
    --text: #0f172a;
    --muted: #64748b;
    --primary: #2563eb;
    --primary-active: #1d4ed8;
    --success: #16a34a;
    --danger: #dc2626;
    --warning: #d97706;
    --border: #e2e8f0;
  }
  * {
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
    touch-action: manipulation;
    user-select: none;
  }
  body {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    height: 100dvh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  /* Cabeçalho Compacto */
  .app-header {
    background: var(--card);
    border-bottom: 1px solid var(--border);
    padding: 10px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-shrink: 0;
  }
  .app-title {
    font-size: 16px;
    font-weight: 800;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .step-badge {
    font-size: 12px;
    font-weight: 700;
    color: var(--primary);
    background: #eff6ff;
    padding: 4px 10px;
    border-radius: 999px;
  }
  /* Área Rolável Central */
  .screen {
    display: none;
    flex: 1;
    overflow-y: auto;
    padding: 12px 14px 90px 14px;
    max-width: 500px;
    width: 100%;
    margin: 0 auto;
  }
  .screen.active {
    display: block;
  }
  /* Barra Inferior Fixa para o Polegar */
  .bottom-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(255, 255, 255, 0.96);
    backdrop-filter: blur(8px);
    border-top: 1px solid var(--border);
    padding: 10px 14px calc(10px + env(safe-area-inset-bottom));
    display: flex;
    gap: 10px;
    justify-content: center;
    z-index: 20;
  }
  .bottom-bar-inner {
    max-width: 500px;
    width: 100%;
    display: flex;
    gap: 10px;
  }
  /* Botões */
  .btn {
    border: none;
    border-radius: 12px;
    font-size: 15px;
    font-weight: 800;
    padding: 14px 16px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    width: 100%;
    transition: transform 0.08s ease, opacity 0.15s;
  }
  .btn:active:not(:disabled) {
    transform: scale(0.97);
  }
  .btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }
  .btn-primary {
    background: var(--primary);
    color: #fff;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
  }
  .btn-success {
    background: var(--success);
    color: #fff;
    box-shadow: 0 4px 12px rgba(22, 163, 74, 0.25);
  }
  .btn-outline {
    background: #f1f5f9;
    color: var(--text);
    border: 1px solid var(--border);
  }
  /* Etapa 1: Cadastro */
  .box {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 12px;
    margin-bottom: 12px;
  }
  .input-row {
    display: flex;
    gap: 8px;
    margin-top: 8px;
  }
  input[type="text"] {
    flex: 1;
    padding: 12px;
    font-size: 16px; /* 16px evita auto-zoom no iOS/Android */
    border: 1px solid var(--border);
    border-radius: 10px;
    outline: none;
    user-select: text;
  }
  input[type="text"]:focus {
    border-color: var(--primary);
  }
  .avatar-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 6px;
    margin-bottom: 8px;
  }
  .avatar-btn {
    font-size: 22px;
    padding: 6px 0;
    border-radius: 10px;
    border: 2px solid transparent;
    background: #f8fafc;
    text-align: center;
    cursor: pointer;
  }
  .avatar-btn.selected {
    border-color: var(--primary);
    background: #eff6ff;
  }
  /* Lista de Jogadores e Ranking */
  .player-item {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 10px 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
  }
  .player-item.eliminated {
    opacity: 0.55;
    background: #fef2f2;
    border-color: #fecaca;
  }
  .player-left {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .rank-num {
    font-size: 13px;
    font-weight: 800;
    color: var(--muted);
    width: 22px;
  }
  .avatar-circle {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    background: #eff6ff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
  }
  .player-name {
    font-weight: 700;
    font-size: 15px;
  }
  .player-sub {
    font-size: 11px;
    color: var(--muted);
  }
  .score-pill {
    font-size: 20px;
    font-weight: 900;
    color: var(--primary);
  }
  .score-pill.danger {
    color: var(--danger);
  }
  .score-pill.warning {
    color: var(--warning);
  }
  /* Etapa 3: Calculadora */
  .calc-top-nav {
    display: flex;
    gap: 6px;
    overflow-x: auto;
    padding-bottom: 6px;
    margin-bottom: 8px;
    scrollbar-width: none;
  }
  .calc-top-nav::-webkit-scrollbar {
    display: none;
  }
  .chip {
    flex-shrink: 0;
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 700;
    background: var(--card);
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 4px;
    cursor: pointer;
  }
  .chip.current {
    border-color: var(--primary);
    background: #eff6ff;
    color: var(--primary);
  }
  .chip.done {
    border-color: #bbf7d0;
    background: #f0fdf4;
    color: var(--success);
  }
  .current-player-banner {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 10px 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
  }
  /* Miniaturas das Cartas Compactas */
  .cards-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 6px;
    margin-bottom: 8px;
  }
  .mini-card {
    background: var(--card);
    border: 1.5px solid #cbd5e1;
    border-radius: 10px;
    padding: 8px 2px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    position: relative;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
  }
  .mini-card:active {
    transform: scale(0.93);
    background: #eff6ff;
    border-color: var(--primary);
  }
  .mini-card .c-rank {
    font-size: 17px;
    font-weight: 900;
    line-height: 1.1;
  }
  .mini-card .c-pts {
    font-size: 10px;
    font-weight: 700;
    color: var(--muted);
    margin-top: 2px;
  }
  .mini-card.joker {
    grid-column: span 2;
    background: #fefce8;
    border-color: #fde047;
  }
  .mini-card .badge-count {
    position: absolute;
    top: -5px;
    right: -5px;
    background: var(--danger);
    color: #fff;
    font-size: 11px;
    font-weight: 800;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  /* Botão Ganhador da Rodada Abaixo das Cartas */
  .winner-btn {
    width: 100%;
    padding: 11px;
    border-radius: 12px;
    border: 2px dashed #cbd5e1;
    background: var(--card);
    font-weight: 800;
    font-size: 14px;
    color: var(--text);
    cursor: pointer;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
  }
  .winner-btn.active {
    background: #dcfce7;
    border: 2px solid var(--success);
    color: #15803d;
  }
  /* Cartas Selecionadas na Mão */
  .selected-tray {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 8px 10px;
    min-height: 52px;
  }
  .tray-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    color: var(--muted);
    margin-bottom: 6px;
  }
  .hand-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }
  .hand-pill {
    background: #fee2e2;
    color: #991b1b;
    font-weight: 800;
    font-size: 13px;
    padding: 4px 8px;
    border-radius: 8px;
    cursor: pointer;
  }
  .top-actions {
    display: flex;
    gap: 6px;
    margin-bottom: 10px;
  }
  .btn-sm {
    padding: 7px 10px;
    font-size: 12px;
    border-radius: 8px;
    font-weight: 700;
    border: 1px solid var(--border);
    background: var(--card);
    cursor: pointer;
  }
</style>
</head>
<body>

<div class="app-header">
  <div class="app-title">🃏 Jogo do Pontinho</div>
  <div class="step-badge" id="stepBadge">1. Jogadores</div>
</div>

<!-- ETAPA 1: CONFIGURAR JOGADORES -->
<div class="screen active" id="screenSetup">
  <div class="box">
    <div style="font-size:13px; font-weight:700; margin-bottom:6px;">Escolha o avatar e digite o nome (até 10):</div>
    <div class="avatar-grid" id="avatarGrid"></div>
    <div class="input-row">
      <input type="text" id="playerNameInput" placeholder="Nome do jogador..." maxlength="16" onkeypress="if(event.key==='Enter') addPlayer()">
      <button class="btn btn-primary" style="width:auto; padding:12px 16px;" onclick="addPlayer()">+ Adicionar</button>
    </div>
  </div>

  <div id="setupPlayersList"></div>

  <div class="bottom-bar">
    <div class="bottom-bar-inner">
      <button class="btn btn-success" id="btnStartGame" onclick="goToRanking()" disabled>INICIAR JOGO (99 PTS) ➔</button>
    </div>
  </div>
</div>

<!-- ETAPA 2: RANKING PRINCIPAL -->
<div class="screen" id="screenRanking">
  <div class="top-actions">
    <button class="btn-sm" onclick="goToSetup()">⚙️ Jogadores</button>
    <button class="btn-sm" id="btnUndo" onclick="undoLastRound()" style="display:none;">↩️ Desfazer Rodada</button>
    <button class="btn-sm" onclick="resetScores()" style="margin-left:auto; color:var(--danger);">🔄 Reiniciar 99</button>
  </div>

  <div id="winnerAlert" style="display:none; background:#dcfce7; border:2px solid #16a34a; border-radius:12px; padding:12px; text-align:center; margin-bottom:10px;">
    <div style="font-size:24px;">🏆</div>
    <div style="font-weight:900; font-size:16px; color:#15803d;" id="winnerAlertText"></div>
  </div>

  <div id="rankingList"></div>

  <div class="bottom-bar">
    <div class="bottom-bar-inner">
      <button class="btn btn-primary" onclick="openCalculator()">🧮 CALCULAR PONTOS</button>
    </div>
  </div>
</div>

<!-- ETAPA 3: CALCULAR PONTOS DA RODADA -->
<div class="screen" id="screenCalc">
  <div class="calc-top-nav" id="calcPlayerChips"></div>

  <div class="current-player-banner">
    <div class="player-left">
      <div class="avatar-circle" id="calcAvatar">😀</div>
      <div>
        <div class="player-name" id="calcName">Jogador</div>
        <div class="player-sub" id="calcSub">Saldo atual: 99 pts</div>
      </div>
    </div>
    <div style="text-align:right;">
      <div style="font-size:11px; color:var(--muted);">Descontar</div>
      <div style="font-size:18px; font-weight:900; color:var(--danger);" id="calcDeduction">-0 pts</div>
    </div>
  </div>

  <div class="cards-grid" id="cardsGrid"></div>

  <button class="winner-btn" id="btnWinnerRound" onclick="toggleWinnerRound()">
    🏆 GANHADOR RODADA (0 pontos)
  </button>

  <div class="selected-tray">
    <div class="tray-header">
      <span id="trayStatusText">Cartas na mão (toque nela para remover):</span>
      <span style="color:var(--danger); font-weight:700; cursor:pointer;" onclick="clearCurrentHand()">Limpar mão</span>
    </div>
    <div class="hand-pills" id="handPills"></div>
  </div>

  <div id="pendingNotice" style="margin-top:8px; font-size:12px; text-align:center; color:var(--warning); font-weight:700;"></div>

  <div class="bottom-bar">
    <div class="bottom-bar-inner">
      <button class="btn btn-outline" style="flex:1;" onclick="prevPlayerCalc()">⬅ VOLTAR</button>
      <button class="btn btn-primary" style="flex:1.4;" id="btnNextOrRegister" onclick="nextOrRegisterCalc()">PRÓXIMO ➡</button>
    </div>
  </div>
</div>

<script>
  const AVATARS = ["😎","🤠","🦊","🦁","🐼","🐸","🐯","🦄","🐙","👽","🤖","🐶"];
  const CARDS = [
    { id: 'A', label: 'A', pts: 11 },
    { id: '2', label: '2', pts: 2 },
    { id: '3', label: '3', pts: 3 },
    { id: '4', label: '4', pts: 4 },
    { id: '5', label: '5', pts: 5 },
    { id: '6', label: '6', pts: 6 },
    { id: '7', label: '7', pts: 7 },
    { id: '8', label: '8', pts: 8 },
    { id: '9', label: '9', pts: 9 },
    { id: '10', label: '10', pts: 10 },
    { id: 'J', label: 'J', pts: 10 },
    { id: 'Q', label: 'Q', pts: 10 },
    { id: 'K', label: 'K', pts: 10 },
    { id: 'JOKER', label: '🃏 Coringa', pts: 20, joker: true }
  ];

  let state = {
    players: [],
    roundNumber: 1,
    history: [],
    selectedAvatar: AVATARS[0]
  };

  let calcState = {
    activePlayers: [],
    currentIndex: 0,
    winnerId: null,
    hands: {}
  };

  function saveState() {
    try { localStorage.setItem('pontinho_mobile_v1', JSON.stringify(state)); } catch(e) {}
  }

  function loadState() {
    try {
      const saved = localStorage.getItem('pontinho_mobile_v1');
      if (saved) state = JSON.parse(saved);
    } catch(e) {}
  }

  function showScreen(id, badgeText) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(id).classList.add('active');
    document.getElementById('stepBadge').innerText = badgeText;
  }

  // ETAPA 1
  function renderAvatars() {
    const grid = document.getElementById('avatarGrid');
    grid.innerHTML = AVATARS.map(av => `
      <div class="avatar-btn ${state.selectedAvatar === av ? 'selected' : ''}" onclick="selectAvatar('${av}')">${av}</div>
    `).join('');
  }

  function selectAvatar(av) {
    state.selectedAvatar = av;
    renderAvatars();
  }

  function addPlayer() {
    if (state.players.length >= 10) return alert('Máximo de 10 jogadores atingido!');
    const input = document.getElementById('playerNameInput');
    const name = input.value.trim();
    if (!name) return;

    state.players.push({
      id: 'p_' + Date.now() + Math.random().toString(36).slice(2,6),
      name: name,
      avatar: state.selectedAvatar,
      score: 99
    });
    input.value = '';
    const nextIdx = (AVATARS.indexOf(state.selectedAvatar) + 1) % AVATARS.length;
    state.selectedAvatar = AVATARS[nextIdx];
    saveState();
    renderSetup();
  }

  function removePlayer(id) {
    state.players = state.players.filter(p => p.id !== id);
    saveState();
    renderSetup();
  }

  function renderSetup() {
    renderAvatars();
    const list = document.getElementById('setupPlayersList');
    if (state.players.length === 0) {
      list.innerHTML = `<div style="text-align:center; color:var(--muted); padding:20px; font-size:14px;">Adicione pelo menos 2 jogadores para começar.</div>`;
    } else {
      list.innerHTML = state.players.map((p, i) => `
        <div class="player-item">
          <div class="player-left">
            <div class="rank-num">#${i+1}</div>
            <div class="avatar-circle">${p.avatar}</div>
            <div>
              <div class="player-name">${p.name}</div>
              <div class="player-sub">${p.score} pontos</div>
            </div>
          </div>
          <button class="btn-sm" style="color:var(--danger);" onclick="removePlayer('${p.id}')">Remover</button>
        </div>
      `).join('');
    }
    document.getElementById('btnStartGame').disabled = state.players.length < 2;
  }

  function goToSetup() {
    renderSetup();
    showScreen('screenSetup', '1. Jogadores');
  }

  // ETAPA 2
  function goToRanking() {
    renderRanking();
    showScreen('screenRanking', 'Rodada ' + state.roundNumber);
  }

  function renderRanking() {
    const sorted = [...state.players].sort((a, b) => b.score - a.score);
    const alive = sorted.filter(p => p.score > 0);
    const alertBox = document.getElementById('winnerAlert');

    if (state.players.length >= 2 && alive.length === 1) {
      alertBox.style.display = 'block';
      document.getElementById('winnerAlertText').innerText = `${alive[0].avatar} ${alive[0].name} venceu o jogo com ${alive[0].score} pts!`;
    } else {
      alertBox.style.display = 'none';
    }

    document.getElementById('btnUndo').style.display = state.history.length > 0 ? 'inline-block' : 'none';

    const list = document.getElementById('rankingList');
    list.innerHTML = sorted.map((p, idx) => {
      const isOut = p.score <= 0;
      const isLow = p.score > 0 && p.score <= 15;
      return `
        <div class="player-item ${isOut ? 'eliminated' : ''}">
          <div class="player-left">
            <div class="rank-num">${idx + 1}º</div>
            <div class="avatar-circle">${p.avatar}</div>
            <div>
              <div class="player-name">${p.name}</div>
              <div class="player-sub">${isOut ? '❌ Eliminado' : (isLow ? '⚠️ Corda bamba' : 'Em jogo')}</div>
            </div>
          </div>
          <div class="score-pill ${isOut ? 'danger' : (isLow ? 'warning' : '')}">${p.score}</div>
        </div>
      `;
    }).join('');
  }

  function resetScores() {
    if (!confirm('Reiniciar todos os jogadores para 99 pontos?')) return;
    state.players.forEach(p => p.score = 99);
    state.roundNumber = 1;
    state.history = [];
    saveState();
    renderRanking();
  }

  function undoLastRound() {
    if (state.history.length === 0) return;
    const prev = state.history.pop();
    state.players = prev.players;
    state.roundNumber = prev.roundNumber;
    saveState();
    renderRanking();
  }

  // ETAPA 3
  function openCalculator() {
    const alive = state.players.filter(p => p.score > 0);
    if (alive.length < 2) return alert('O jogo já tem um vencedor! Reinicie os 99 pontos para jogar novamente.');

    calcState.activePlayers = alive;
    calcState.currentIndex = 0;
    calcState.winnerId = null;
    calcState.hands = {};
    alive.forEach(p => { calcState.hands[p.id] = []; });

    renderCalcScreen();
    showScreen('screenCalc', `Calcular • Rodada ${state.roundNumber}`);
  }

  function isPlayerDone(pId) {
    return calcState.winnerId === pId || (calcState.hands[pId] && calcState.hands[pId].length > 0);
  }

  function isAllPlayersDone() {
    if (!calcState.winnerId) return false;
    return calcState.activePlayers.every(p => isPlayerDone(p.id));
  }

  function getHandPoints(pId) {
    if (calcState.winnerId === pId) return 0;
    return (calcState.hands[pId] || []).reduce((acc, c) => acc + c.pts, 0);
  }

  function renderCalcScreen() {
    const p = calcState.activePlayers[calcState.currentIndex];
    const totalPlayers = calcState.activePlayers.length;

    // Topo: chips dos jogadores
    document.getElementById('calcPlayerChips').innerHTML = calcState.activePlayers.map((pl, idx) => {
      const done = isPlayerDone(pl.id);
      const isCurr = idx === calcState.currentIndex;
      return `
        <div class="chip ${isCurr ? 'current' : ''} ${done ? 'done' : ''}" onclick="jumpToPlayerCalc(${idx})">
          <span>${pl.avatar}</span>
          <span>${pl.name}</span>
          <span>${calcState.winnerId === pl.id ? '🏆' : (done ? '✓' : '')}</span>
        </div>
      `;
    }).join('');

    // Banner do jogador atual
    const deduction = getHandPoints(p.id);
    const remaining = Math.max(0, p.score - deduction);
    document.getElementById('calcAvatar').innerText = p.avatar;
    document.getElementById('calcName').innerText = `${p.name} (${calcState.currentIndex + 1}/${totalPlayers})`;
    document.getElementById('calcSub').innerText = `Saldo: ${p.score} ➔ Ficará com ${remaining} pts`;
    document.getElementById('calcDeduction').innerText = calcState.winnerId === p.id ? '🏆 0 pts' : `-${deduction} pts`;

    // Grade de miniaturas de cartas
    const hand = calcState.hands[p.id] || [];
    document.getElementById('cardsGrid').innerHTML = CARDS.map(c => {
      const count = hand.filter(item => item.id === c.id).length;
      return `
        <div class="mini-card ${c.joker ? 'joker' : ''}" onclick="addCardToCurrent('${c.id}')">
          ${count > 0 ? `<div class="badge-count">${count}</div>` : ''}
          <div class="c-rank">${c.label}</div>
          <div class="c-pts">${c.pts} pts</div>
        </div>
      `;
    }).join('');

    // Botão Ganhador da Rodada
    const isWin = calcState.winnerId === p.id;
    const winBtn = document.getElementById('btnWinnerRound');
    winBtn.className = 'winner-btn ' + (isWin ? 'active' : '');
    winBtn.innerHTML = isWin ? '🏆 GANHADOR DA RODADA SELECIONADO (0 pts)' : '🏆 GANHADOR RODADA (0 pontos)';

    // Bandeja de cartas
    const pillsEl = document.getElementById('handPills');
    if (isWin) {
      pillsEl.innerHTML = `<span style="font-size:13px; font-weight:700; color:var(--success);">Bateu a rodada! Nenhuma carta descontada.</span>`;
    } else if (hand.length === 0) {
      pillsEl.innerHTML = `<span style="font-size:13px; color:var(--muted);">Toque nas cartas acima ou marque como Ganhador.</span>`;
    } else {
      pillsEl.innerHTML = hand.map((c, i) => `
        <div class="hand-pill" onclick="removeCardFromCurrent(${i})">${c.label} (${c.pts}) ✕</div>
      `).join('');
    }

    // Botão Próximo / Registrar
    const isLast = calcState.currentIndex === totalPlayers - 1;
    const allDone = isAllPlayersDone();
    const nextBtn = document.getElementById('btnNextOrRegister');
    const notice = document.getElementById('pendingNotice');

    if (isLast) {
      nextBtn.innerText = '✓ REGISTRAR';
      nextBtn.className = 'btn btn-success';
      nextBtn.disabled = !allDone;
      if (!allDone) {
        const missingWinner = !calcState.winnerId;
        const missingPlayer = calcState.activePlayers.find(pl => !isPlayerDone(pl.id));
        notice.innerText = missingWinner
          ? '⚠️ Falta marcar quem foi o GANHADOR DA RODADA!'
          : `⚠️ Falta preencher as cartas de: ${missingPlayer.name}`;
      } else {
        notice.innerText = '';
      }
    } else {
      nextBtn.innerText = 'PRÓXIMO ➡';
      nextBtn.className = 'btn btn-primary';
      nextBtn.disabled = false;
      notice.innerText = '';
    }
  }

  function addCardToCurrent(cardId) {
    const p = calcState.activePlayers[calcState.currentIndex];
    if (calcState.winnerId === p.id) calcState.winnerId = null;
    const cardObj = CARDS.find(c => c.id === cardId);
    calcState.hands[p.id].push(cardObj);
    renderCalcScreen();
  }

  function removeCardFromCurrent(idx) {
    const p = calcState.activePlayers[calcState.currentIndex];
    calcState.hands[p.id].splice(idx, 1);
    renderCalcScreen();
  }

  function clearCurrentHand() {
    const p = calcState.activePlayers[calcState.currentIndex];
    calcState.hands[p.id] = [];
    if (calcState.winnerId === p.id) calcState.winnerId = null;
    renderCalcScreen();
  }

  function toggleWinnerRound() {
    const p = calcState.activePlayers[calcState.currentIndex];
    if (calcState.winnerId === p.id) {
      calcState.winnerId = null;
    } else {
      calcState.winnerId = p.id;
      calcState.hands[p.id] = [];
    }
    renderCalcScreen();
  }

  function jumpToPlayerCalc(idx) {
    calcState.currentIndex = idx;
    renderCalcScreen();
  }

  function prevPlayerCalc() {
    if (calcState.currentIndex > 0) {
      calcState.currentIndex--;
      renderCalcScreen();
    } else {
      goToRanking();
    }
  }

  function nextOrRegisterCalc() {
    const total = calcState.activePlayers.length;
    if (calcState.currentIndex < total - 1) {
      calcState.currentIndex++;
      renderCalcScreen();
    } else if (isAllPlayersDone()) {
      registerRound();
    }
  }

  function registerRound() {
    state.history.push(JSON.parse(JSON.stringify({
      players: state.players,
      roundNumber: state.roundNumber
    })));

    calcState.activePlayers.forEach(activeP => {
      const target = state.players.find(p => p.id === activeP.id);
      if (target) {
        const pts = getHandPoints(activeP.id);
        target.score = Math.max(0, target.score - pts);
      }
    });

    state.roundNumber++;
    saveState();
    goToRanking();
  }

  loadState();
  if (state.players.length >= 2) {
    goToRanking();
  } else {
    goToSetup();
  }
</script>
</body>
</html>
"""

components.html(html_code, height=850, scrolling=False)
