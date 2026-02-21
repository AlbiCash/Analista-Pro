import streamlit as st
import random
import time

# ============================================================
#   ANALISTA PRO — v15 ULTRA (beta 0.3.2)
#   BLOCCO 1/4 — HEADER, AUDIO, CSS, FUNZIONI BASE
# ============================================================

st.set_page_config(page_title="Analista Pro", layout="wide")

# --- FUNZIONE DI FALLBACK PER RERUN ---
def safe_rerun():
    """Compatibile con più versioni di Streamlit:
    se esiste experimental_rerun() la chiama, altrimenti usa st.stop() come fallback."""
    if hasattr(st, "experimental_rerun") and callable(getattr(st, "experimental_rerun")):
        try:
            st.experimental_rerun()
        except Exception:
            st.stop()
    else:
        st.stop()

# --- AUDIO SYSTEM ---
st.markdown("""
<audio id="snd_success" src="https://assets.mixkit.co/sfx/preview/mixkit-video-game-win-2016.mp3"></audio>
<audio id="snd_error" src="https://assets.mixkit.co/sfx/preview/mixkit-arcade-retro-game-over-213.mp3"></audio>
<audio id="snd_click" src="https://assets.mixkit.co/sfx/preview/mixkit-select-click-1109.mp3"></audio>
<audio id="snd_alert" src="https://assets.mixkit.co/sfx/preview/mixkit-warning-alarm-buzzer-991.mp3"></audio>
<audio id="snd_levelup" src="https://assets.mixkit.co/sfx/preview/mixkit-achievement-bell-600.mp3"></audio>

<script>
function playSound(id) {
    var audio = document.getElementById(id);
    if (audio) { audio.currentTime = 0; audio.play(); }
}
</script>
""", unsafe_allow_html=True)

# --- CSS GLOBALE ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&family=Share+Tech+Mono&display=swap');

.stApp {
    background: radial-gradient(circle at top, #0d0d18 0%, #05050a 40%, #000000 100%);
    color: #e0e0e0;
    font-family: 'Inter', sans-serif;
}

.neon-title { font-family: 'Orbitron', sans-serif; font-size: 2.2rem; text-align:center; color:#00f2ff; text-shadow:0 0 10px #00f2ff; }
.glass-card { background: rgba(15,15,30,0.75); border:1px solid rgba(0,242,255,0.18); border-radius:12px; padding:14px; margin-bottom:12px; backdrop-filter: blur(8px); }
.stat-label { color:#888; font-size:0.75rem; text-transform:uppercase; }
.stat-value { font-size:1rem; color:#fff; font-weight:600; font-family:'Share Tech Mono', monospace; }
.stButton>button { background: linear-gradient(135deg,#02131a,#04303f); border:1px solid #00f2ff; color:#00f2ff; border-radius:999px; font-family:'Orbitron', sans-serif; }
.stButton>button:hover { background:#00f2ff; color:#000; }
.risk-flag { font-size:0.85rem; color:#ff6b6b; }
.version-tag { text-align:center; font-size:0.75rem; color:#777; margin-top:18px; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# FUNZIONI BASE
# ============================================================

def genera_mercato(difficulty: str):
    scenari = [
        {"nome": "BOOM_ECONOMICO", "funding": 0.02, "default_mult": 0.5,
         "desc": "Liquidità abbondante, spread bassi, appetito al rischio elevato."},
        {"nome": "STRETTA_CREDITIZIA", "funding": 0.09, "default_mult": 2.5,
         "desc": "Inflazione alta, regolatore nervoso, rischio default elevato."},
        {"nome": "CIGNO_NERO", "funding": 0.15, "default_mult": 5.0,
         "desc": "Shock sistemico, volatilità estrema, margine di errore minimo."}
    ]
    m = random.choice(scenari)
    if difficulty == "Easy":
        m["funding"] = max(0.0, m["funding"] - 0.01)
        m["default_mult"] *= 0.7
    elif difficulty == "Hard":
        m["funding"] += 0.02
        m["default_mult"] *= 1.4
    elif difficulty == "Nightmare":
        m["funding"] += 0.04
        m["default_mult"] *= 1.9
        m["nome"] = "CIGNO_NERO_PERMANENTE"
    return m

def genera_dossier(difficulty: str):
    lavori = [
        {"tipo": "STATALE", "min_r": 1300, "max_r": 3200},
        {"tipo": "AUTONOMO", "min_r": 2000, "max_r": 9000},
        {"tipo": "INVESTITORE_RISCHIO", "min_r": 6000, "max_r": 25000},
        {"tipo": "PENSIONATO", "min_r": 1100, "max_r": 2500},
        {"tipo": "MANAGER_PRIVATO", "min_r": 2800, "max_r": 12000},
    ]
    l = random.choice(lavori)
    eta = random.randint(21, 78)
    reddito = random.randint(l['min_r'], l['max_r'])
    richiesta = random.randint(5000, 90000)
    durata = random.choice([24, 36, 48, 72, 120])
    base_frode = {"Easy": 0.02, "Normal": 0.05, "Hard": 0.08, "Nightmare": 0.12}[difficulty]
    is_frode = ((l['tipo'] == "INVESTITORE_RISCHIO" and random.random() < base_frode * 3) or random.random() < base_frode)
    motivazioni = [
        "Ristrutturazione immobile", "Consolidamento debiti", "Acquisto auto di lusso",
        "Espansione attività", "Liquidità personale", "Investimenti ad alto rischio",
        "Criptovalute e trading"
    ]
    return {
        "id": f"DSR-{random.randint(1000, 9999)}",
        "eta": eta,
        "job": l['tipo'],
        "reddito": reddito,
        "impegni": random.choice([0, 250, 500, 800]),
        "carico": random.randint(0, 3),
        "casa": random.random() < 0.45,
        "richiesta": richiesta,
        "durata": durata,
        "crif": random.choices(["ECCELLENTE", "BUONO", "MEDIO", "CRITICO"], weights=[30,35,25,10])[0],
        "is_frode": is_frode,
        "motivazione": random.choice(motivazioni)
    }

def format_euro(x: int | float) -> str:
    return f"€ {x:,.0f}".replace(",", ".")

def calcola_flag_rischio(c, dti, eta_f):
    flags = []
    if c["eta"] < 25 and c["reddito"] > 6000:
        flags.append("Reddito molto alto rispetto all'età — possibile profilo non genuino.")
    if c["job"] == "PENSIONATO" and c.get("durata",0) > 48:
        flags.append("Durata lunga per profilo pensionato — rischio temporale.")
    if eta_f > 80:
        flags.append("Età a scadenza molto elevata — sostenibilità critica.")
    if c["motivazione"] in ["Investimenti ad alto rischio", "Criptovalute e trading"]:
        flags.append("Motivazione ad alto rischio — possibile speculazione.")
    if c["job"] == "STATALE" and c["richiesta"] > 50000:
        flags.append("Importo molto alto per profilo statale.")
    if c["job"] == "AUTONOMO" and c["richiesta"] > 70000:
        flags.append("Importo elevato per profilo autonomo — volatilità reddito.")
    if c["crif"] in ["ECCELLENTE", "BUONO"] and dti > 45:
        flags.append("Storico buono ma DTI molto alto — peggioramento recente.")
    if c["casa"] and c["reddito"] < 1400:
        flags.append("Proprietario con reddito basso — possibile intestazione fittizia.")
    if c["carico"] == 0 and c["reddito"] > 9000:
        flags.append("Reddito molto alto senza carichi — profilo potenzialmente artefatto.")
    return flags
# ============================================================
#   ANALISTA PRO — v15 ULTRA (beta 0.3.2)
#   BLOCCO 2/4 — SESSIONE, TUTORIAL, DIFFICOLTÀ, SIGMA‑9, ACHIEVEMENTS
# ============================================================

# --- INIZIALIZZAZIONE SESSIONE ---
if "initialized" not in st.session_state:
    st.session_state.initialized = True

    # Impostazioni di gioco
    st.session_state.difficulty_locked = False
    st.session_state.difficulty = None
    st.session_state.tutorial_done = False

    # Stato giocatore
    st.session_state.audio_on = True
    st.session_state.bilancio = 40000
    st.session_state.ammonizioni = 0
    st.session_state.turno = 1
    st.session_state.corrette = 0
    st.session_state.sbagliate = 0
    st.session_state.max_capitale = 40000

    # Stato SIGMA‑9
    st.session_state.sigma_capitale = 40000
    st.session_state.sigma_log = []

    # Stato partita
    st.session_state.mercato = None
    st.session_state.cliente = None
    st.session_state.esito_turno = None
    st.session_state.evento = None
    st.session_state.streak_ok = 0
    st.session_state.streak_default = 0
    st.session_state.log = []
    st.session_state.highscores = []

    # Achievements
    st.session_state.achievements = {
        "prudente": False,
        "squalo": False,
        "occhio_clinico": False,
        "equilibrato": False,
        "fenomeno": False,
        "leggenda": False,
        "antifrode_supremo": False,
        "ceo_material": False
    }

    # Contatori achievement
    st.session_state.achv_rifiuti_corretti = 0
    st.session_state.achv_approvazioni_corrette = 0
    st.session_state.achv_frodi_evitate = 0
    st.session_state.achv_turni_senza_ammonizioni = 0

    # Easter egg flag
    st.session_state.salvatore_event = False

# ============================================================
#   TUTORIAL OPZIONALE (solo all'inizio)
# ============================================================

if not st.session_state.tutorial_done:
    st.markdown("<div class='neon-title'>Analista Pro</div>", unsafe_allow_html=True)
    st.markdown("<div class='neon-sub'>Simulatore avanzato di valutazione del rischio</div>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### Vuoi attivare il tutorial iniziale?")
    st.write("Il tutorial spiega come leggere il dossier, interpretare il DTI, riconoscere anomalie e capire gli eventi di mercato.")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        if st.button("📘 Sì, attiva il tutorial"):
            st.session_state.show_tutorial = True
    with col_t2:
        if st.button("⏭️ No, inizia subito"):
            st.session_state.show_tutorial = False
            st.session_state.tutorial_done = True
    st.markdown("</div>", unsafe_allow_html=True)

    if "show_tutorial" in st.session_state and st.session_state.show_tutorial:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("## 📘 Tutorial — Come funziona Analista Pro")
        st.markdown("""
        - **Profilo cliente**: età, lavoro, casa, carico familiare
        - **Situazione economica**: reddito, impegni, rata
        - **Indicatori di rischio**: DTI, età a scadenza, CRIF
        - **Alert rischio**: pannelli rossi per anomalie
        - **SIGMA‑9**: rivale freddo e pungente
        - **Easter Egg**: evento rarissimo dedicato a Salvatore Russiello
        """)
        if st.button("✔️ Ho capito, iniziamo"):
            st.session_state.tutorial_done = True
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ============================================================
#   SCELTA DIFFICOLTÀ (solo all'inizio)
# ============================================================

if not st.session_state.difficulty_locked:
    st.markdown("<div class='neon-title'>Analista Pro</div>", unsafe_allow_html=True)
    st.markdown("<div class='neon-sub'>Seleziona la difficoltà per iniziare</div>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    diff = st.radio("Livello di difficoltà", ["Easy", "Normal", "Hard", "Nightmare"], index=1)
    if st.button("🚀 Inizia la partita"):
        st.session_state.difficulty = diff
        st.session_state.difficulty_locked = True
        st.session_state.mercato = genera_mercato(diff)
        st.session_state.cliente = genera_dossier(diff)
        st.session_state.esito_turno = None
        st.session_state.turno = 1
        st.session_state.evento = None
        st.session_state.salvatore_event = False
        safe_rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ============================================================
#   SIGMA‑9 — LOGICA BASE
# ============================================================

SIGMA_AVATAR = r"""
        ███████╗ ██╗  ██████╗  ███╗   ███╗  ███╗  ██╗
        ██╔════╝ ██║ ██╔═══██╗ ████╗ ████║ ████║  ██║
        ███████╗ ██║ ██║   ██║ ██╔████╔██║ ██╔██╗ ██║
        ╚════██║ ██║ ██║   ██║ ██║╚██╔╝██║ ██║╚██╗██║
        ███████║ ██║ ╚██████╔╝ ██║ ╚═╝ ██║ ██║ ╚████║
        ╚══════╝ ╚═╝  ╚═════╝  ╚═╝     ╚═╝ ╚═╝  ╚═══╝
                   SIGMA‑9 — Risk Engine v4.7
"""

def sigma_decision(c, dti, eta_f, risk_flags):
    if dti < 30 and c["crif"] == "ECCELLENTE" and eta_f < 70 and len(risk_flags) == 0:
        return "APPROVA"
    return "RIFIUTA"

def sigma_commento(tipo):
    frasi = {
        "tu_default": [
            "Decisione… creativa. Io l’avrei evitata.",
            "Il rischio ti piace, vedo. Io preferisco i risultati.",
            "Interessante. Non efficace, ma interessante."
        ],
        "tu_successo": [
            "Complimenti. Non pensavo ci riuscissi.",
            "Anomalia rilevata: l'umano ha avuto successo.",
            "Statisticamente improbabile. Ma bravo."
        ],
        "sigma_meglio": [
            "Il mio capitale cresce. Il tuo… è in fase sperimentale.",
            "Io seguo i numeri. Tu segui l'istinto. Vediamo chi vince."
        ],
        "sigma_peggio": [
            "Errore? No, sto solo testando la tua autostima.",
            "Interessante. Hai fatto meglio di me. Bug temporaneo."
        ]
    }
    return random.choice(frasi[tipo])

# ============================================================
#   ACHIEVEMENTS — LOGICA BASE
# ============================================================

def check_achievements():
    ach = st.session_state.achievements
    if st.session_state.achv_rifiuti_corretti >= 5:
        ach["prudente"] = True
    if st.session_state.achv_approvazioni_corrette >= 5:
        ach["squalo"] = True
    if st.session_state.achv_frodi_evitate >= 1:
        ach["occhio_clinico"] = True
    if st.session_state.achv_turni_senza_ammonizioni >= 10:
        ach["equilibrato"] = True
    if st.session_state.bilancio >= 150000:
        ach["fenomeno"] = True
    if st.session_state.corrette >= 20 and st.session_state.sbagliate == 0:
        ach["leggenda"] = True
    if st.session_state.achv_frodi_evitate >= 3:
        ach["antifrode_supremo"] = True
    if st.session_state.bilancio >= 200000:
        ach["ceo_material"] = True
# ============================================================
#   ANALISTA PRO — v15 ULTRA (beta 0.3.2)
#   BLOCCO 3/4 — UI PRINCIPALE, DOSSIER, DECISIONI, SIGMA‑9, EASTER EGG
#   (NESSUNA LOGICA DI TIMER: avanzamento manuale con AVANTI)
# ============================================================

# --- HEADER VISIVO ---
st.markdown("<div class='neon-title'>Analista Pro</div>", unsafe_allow_html=True)
st.markdown("<div class='neon-sub'>Valuta. Analizza. Supera SIGMA‑9.</div>", unsafe_allow_html=True)
st.write("")

# ============================================================
#   POSSIBILE ATTIVAZIONE EASTER EGG (1% ogni caricamento di pagina)
# ============================================================

# Nota: senza timer, l'evento può attivarsi quando la pagina viene ricaricata o si avanza turno.
if random.random() < 0.01:
    st.session_state.salvatore_event = True
else:
    if "salvatore_event" not in st.session_state:
        st.session_state.salvatore_event = False

salvatore_bonus = False
if st.session_state.salvatore_event:
    st.markdown("<div class='glass-card glass-card-accent'>", unsafe_allow_html=True)
    st.markdown("## 🥚 EASTER EGG — SALVATORE RUSSIELLO")
    st.markdown("""
    Un giovane stagista napoletano entra in ufficio con un cuoppo di frittura e dice:

    **“Uagliò… ma che è tutto sto rischio?  
    Io voglio solo magnà e diventà ricco!”**

    Effetti per il turno corrente:
    - +500€ motivazione (bonus diretto)
    - -5% rischio default per questo turno
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    st.session_state.bilancio += 500
    salvatore_bonus = True

# ============================================================
#   FINE GIOCO (LICENZIAMENTO / BANCAROTTA / CEO)
# ============================================================

def registra_highscore(motivo: str):
    st.session_state.max_capitale = max(st.session_state.max_capitale, st.session_state.bilancio)
    st.session_state.highscores.append({
        "capitale": st.session_state.bilancio,
        "sigma": st.session_state.sigma_capitale,
        "turni": st.session_state.turno,
        "corrette": st.session_state.corrette,
        "sbagliate": st.session_state.sbagliate,
        "motivo": motivo
    })

if st.session_state.ammonizioni >= 3:
    registra_highscore("Licenziato per inefficienza")
    if st.session_state.audio_on:
        st.markdown("<script>playSound('snd_error');</script>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:red; text-align:center;'>💀 LICENZIATO</h1>", unsafe_allow_html=True)
    st.error("HR: inefficienza operativa reiterata. SIGMA‑9 ha già preso il tuo posto.")
    st.code(SIGMA_AVATAR)
    if st.button("RESETTA CARRIERA"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        safe_rerun()
    st.stop()

if st.session_state.bilancio <= -50000:
    registra_highscore("Bancarotta")
    if st.session_state.audio_on:
        st.markdown("<script>playSound('snd_error');</script>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:red; text-align:center;'>📉 BANCAROTTA</h1>", unsafe_allow_html=True)
    st.error("La banca è collassata. SIGMA‑9 ha segnalato la tua inadeguatezza.")
    st.code(SIGMA_AVATAR)
    if st.button("REBOOT"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        safe_rerun()
    st.stop()

if st.session_state.bilancio >= 250000:
    registra_highscore("Raggiunto ruolo CEO")
    if st.session_state.audio_on:
        st.markdown("<script>playSound('snd_levelup');</script>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:#00f2ff; text-align:center;'>🏆 NUOVO CEO</h1>", unsafe_allow_html=True)
    st.success("Hai superato SIGMA‑9. Il board ti considera un prodigio umano.")
    st.code(SIGMA_AVATAR)
    if st.button("RICOMINCIA SFIDA"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        safe_rerun()
    st.stop()

# ============================================================
#   SCENARIO DI MERCATO + DOSSIER + INDICATORI
# ============================================================

m = st.session_state.mercato
c = st.session_state.cliente

col_a, col_b, col_c = st.columns([2,1,1])

with col_a:
    st.markdown(f"<div class='glass-card'><p class='stat-label'>Scenario di Mercato</p><p class='stat-value'>{m['nome']}</p><p style='color:#bbb'>{m['desc']}</p></div>", unsafe_allow_html=True)

with col_b:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<p class='stat-label'>Capitale</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='stat-value'>{format_euro(st.session_state.bilancio)}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_c:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<p class='stat-label'>Turno</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='stat-value'>Turno {st.session_state.turno}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Calcoli
tasso_f = m['funding'] + 0.05
rata = (c['richiesta'] * (1 + tasso_f)) / c['durata']
reddito_n = c['reddito'] - c['impegni'] - (c['carico'] * 350)
dti = (rata / reddito_n) * 100 if reddito_n > 0 else 999
eta_f = c['eta'] + (c['durata'] / 12)
risk_flags = calcola_flag_rischio(c, dti, eta_f)

if salvatore_bonus:
    dti *= 0.95

# Dossier
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
b1, b2, b3 = st.columns([1.2,1.2,1])
with b1:
    st.markdown("<p class='stat-label'>Profilo Cliente</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='stat-value'>{c['id']}</p>", unsafe_allow_html=True)
    st.markdown(f"Età: **{c['eta']} anni**")
    st.markdown(f"Occupazione: **{c['job']}**")
    st.markdown(f"Casa: **{'Proprietario' if c['casa'] else 'Affitto'}**")
    st.markdown(f"Carico familiare: **{c['carico']} persone**")
with b2:
    st.markdown("<p class='stat-label'>Situazione Economica</p>", unsafe_allow_html=True)
    st.markdown(f"Reddito netto: **{format_euro(c['reddito'])}**")
    st.markdown(f"Impegni mensili: **{format_euro(c['impegni'])}**")
    st.markdown("<p class='stat-label' style='margin-top:8px;'>Richiesta</p>", unsafe_allow_html=True)
    st.markdown(f"Importo: **{format_euro(c['richiesta'])}**")
    st.markdown(f"Durata: **{c['durata']} mesi**")
    st.markdown(f"Motivazione: **{c['motivazione']}**")
with b3:
    st.markdown("<p class='stat-label'>Indicatori di Rischio</p>", unsafe_allow_html=True)
    color_dti = "#ff4100" if dti > 40 else "#00f2ff"
    st.markdown(f"DTI: **<span style='color:{color_dti}'>{dti:.1f}%</span>**", unsafe_allow_html=True)
    st.markdown(f"Età a scadenza: **{int(eta_f)} anni**")
    col_crif = "#ff4100" if c["crif"] == "CRITICO" else "#00f2ff" if c["crif"] == "ECCELLENTE" else "#ffae00"
    st.markdown(f"Rating CRIF: **<span style='color:{col_crif}'>{c['crif']}</span>**", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Alert rischio
if risk_flags:
    st.markdown("<div class='glass-card glass-card-accent'>", unsafe_allow_html=True)
    st.markdown("<p class='stat-label'>⚠️ Alert Rischio — qualcosa non torna</p>", unsafe_allow_html=True)
    for f in risk_flags:
        st.markdown(f"<p class='risk-flag'>• {f}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
#   DECISIONI (SENZA TIMER): APPROVA / RIFIUTA
# ============================================================

if not st.session_state.esito_turno:
    c1, c2 = st.columns(2)

    with c1:
        if st.button("✅ APPROVA"):
            if st.session_state.audio_on:
                st.markdown("<script>playSound('snd_click');</script>", unsafe_allow_html=True)

            prob_def = 0.05 * m['default_mult']
            if dti > 45:
                prob_def += 0.4
            if c['crif'] == "CRITICO":
                prob_def += 0.3
            if salvatore_bonus:
                prob_def *= 0.8

            default = (random.random() < prob_def) or c['is_frode'] or (eta_f > 82)

            if default:
                perdita = 150000 if c['is_frode'] else c['richiesta']
                st.session_state.bilancio -= perdita
                st.session_state.esito_turno = f"❌ DEFAULT! Perdita: {format_euro(perdita)}"
                st.session_state.sbagliate += 1
                st.session_state.streak_default += 1
                st.session_state.streak_ok = 0
                st.session_state.log.append(f"❌ DEFAULT su {c['id']} → -{format_euro(perdita)}")
                if c['is_frode']:
                    st.session_state.achv_frodi_evitate += 1
                if st.session_state.audio_on:
                    st.markdown("<script>playSound('snd_error');</script>", unsafe_allow_html=True)
                st.session_state.sigma_comment = sigma_commento("tu_default")
            else:
                utile = int(c['richiesta'] * tasso_f)
                st.session_state.bilancio += utile
                st.session_state.esito_turno = f"💎 SUCCESSO! Utile: {format_euro(utile)}"
                st.session_state.corrette += 1
                st.session_state.streak_ok += 1
                st.session_state.streak_default = 0
                st.session_state.log.append(f"✅ APPROVATO {c['id']} → +{format_euro(utile)}")
                st.session_state.achv_approvazioni_corrette += 1
                if st.session_state.audio_on:
                    st.markdown("<script>playSound('snd_success');</script>", unsafe_allow_html=True)
                st.session_state.sigma_comment = sigma_commento("tu_successo")

            st.session_state.max_capitale = max(st.session_state.max_capitale, st.session_state.bilancio)

            # SIGMA‑9 decisione parallela (simulata)
            sigma_choice = sigma_decision(c, dti, eta_f, risk_flags)
            if sigma_choice == "APPROVA":
                if default:
                    st.session_state.sigma_capitale -= perdita
                    st.session_state.sigma_log.append(f"❌ SIGMA‑9 APPROVA → DEFAULT → -{format_euro(perdita)}")
                else:
                    st.session_state.sigma_capitale += utile
                    st.session_state.sigma_log.append(f"💎 SIGMA‑9 APPROVA → +{format_euro(utile)}")
            else:
                st.session_state.sigma_log.append("🛡️ SIGMA‑9 RIFIUTA")

            safe_rerun()

    with c2:
        if st.button("❌ RIFIUTA"):
            if st.session_state.audio_on:
                st.markdown("<script>playSound('snd_click');</script>", unsafe_allow_html=True)

            giusto = (dti > 40 or c['crif'] == "CRITICO" or c['is_frode'] or eta_f > 78)
            penalty = 3000

            if giusto:
                st.session_state.bilancio += 700
                st.session_state.esito_turno = "🛡️ FILTRO CORRETTO: rischio evitato."
                st.session_state.corrette += 1
                st.session_state.streak_ok += 1
                st.session_state.streak_default = 0
                st.session_state.log.append(f"🛡️ RIFIUTATO {c['id']} → +700€")
                st.session_state.achv_rifiuti_corretti += 1
                if st.session_state.audio_on:
                    st.markdown("<script>playSound('snd_success');</script>", unsafe_allow_html=True)
                st.session_state.sigma_comment = sigma_commento("tu_successo")
            else:
                st.session_state.bilancio -= penalty
                st.session_state.esito_turno = f"⚠️ ERRORE COMMERCIALE: cliente solido perso. Penale {format_euro(penalty)}"
                st.session_state.sbagliate += 1
                st.session_state.streak_ok = 0
                st.session_state.log.append(f"⚠️ ERRORE: rifiutato {c['id']} → -{format_euro(penalty)}")
                if st.session_state.audio_on:
                    st.markdown("<script>playSound('snd_alert');</script>", unsafe_allow_html=True)
                st.session_state.sigma_comment = sigma_commento("tu_default")

            st.session_state.max_capitale = max(st.session_state.max_capitale, st.session_state.bilancio)

            sigma_choice = sigma_decision(c, dti, eta_f, risk_flags)
            if sigma_choice == "APPROVA":
                if giusto:
                    st.session_state.sigma_capitale -= penalty
                    st.session_state.sigma_log.append(f"❌ SIGMA‑9 APPROVA → ERRORE → -{format_euro(penalty)}")
                else:
                    st.session_state.sigma_capitale += 700
                    st.session_state.sigma_log.append(f"💎 SIGMA‑9 APPROVA → +700€")
            else:
                st.session_state.sigma_log.append("🛡️ SIGMA‑9 RIFIUTA")

            safe_rerun()

else:
    # mostra esito e commento SIGMA‑9
    st.info(st.session_state.esito_turno)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 🤖 SIGMA‑9 dice:")
    st.markdown(f"**{st.session_state.sigma_comment}**")
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("AVANTI >>"):
        # prepara nuovo turno manuale
        st.session_state.cliente = genera_dossier(st.session_state.difficulty)
        st.session_state.mercato = genera_mercato(st.session_state.difficulty)
        st.session_state.esito_turno = None
        st.session_state.turno += 1
        st.session_state.evento = None
        st.session_state.salvatore_event = False
        safe_rerun()
# ============================================================
#   ANALISTA PRO — v15 ULTRA (beta 0.3.2)
#   BLOCCO 4/4 — ACHIEVEMENTS, SIGMA‑9 PANEL, LEADERBOARD, VERSIONE
# ============================================================

# Aggiorna achievements (contatore turni senza ammonizioni)
st.session_state.achv_turni_senza_ammonizioni += 1
check_achievements()

# SIGMA‑9 PANEL
st.markdown("<h3 style='margin-top:20px;'>🤖 SIGMA‑9 — Stato Attuale</h3>", unsafe_allow_html=True)
s1, s2 = st.columns([1,2])
with s1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<p class='stat-label'>Capitale SIGMA‑9</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='stat-value'>{format_euro(st.session_state.sigma_capitale)}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
with s2:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<p class='stat-label'>Ultime decisioni SIGMA‑9</p>", unsafe_allow_html=True)
    if st.session_state.sigma_log:
        for row in st.session_state.sigma_log[-6:][::-1]:
            st.markdown(f"<p style='font-size:0.85rem;'>{row}</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color:#777;'>In attesa delle prime decisioni...</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ACHIEVEMENTS VISUALI
st.markdown("<h3 style='margin-top:20px;'>🏆 Achievement Sbloccati</h3>", unsafe_allow_html=True)
ach = st.session_state.achievements
ach_list = {
    "prudente": "🛡️ Prudente — 5 rifiuti corretti consecutivi",
    "squalo": "💎 Squalo del Credito — 5 approvazioni corrette consecutive",
    "occhio_clinico": "👁️ Occhio Clinico — individuata una frode",
    "equilibrato": "⚖️ Equilibrato — 10 turni senza ammonizioni",
    "fenomeno": "🔥 Fenomeno — capitale oltre 150.000",
    "leggenda": "🌟 Leggenda del Rischio — 20 decisioni corrette senza errori",
    "antifrode_supremo": "🕵️ Antifrode Supremo — 3 frodi evitate",
    "ceo_material": "🏆 CEO Material — capitale oltre 200.000"
}
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
any_ach = False
for key, label in ach_list.items():
    if ach.get(key):
        any_ach = True
        st.markdown(f"<p style='font-size:0.9rem;'>{label}</p>", unsafe_allow_html=True)
if not any_ach:
    st.markdown("<p style='color:#777;'>Nessun achievement sbloccato… per ora.</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# LEADERBOARD LOCALE
if st.session_state.highscores:
    st.markdown("<h3 style='margin-top:20px;'>📊 Storico Carriera</h3>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    for hs in sorted(st.session_state.highscores, key=lambda x: x["capitale"], reverse=True)[:5]:
        st.markdown(f"<p style='font-size:0.9rem;'>{format_euro(hs['capitale'])} | SIGMA‑9: {format_euro(hs['sigma'])} | Turni: {hs['turni']} | ✔ {hs['corrette']} / ✖ {hs['sbagliate']} — <i>{hs['motivo']}</i></p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# VERSIONE
st.markdown("<div class='version-tag'>Analista Pro — beta 0.3.2</div>", unsafe_allow_html=True)
