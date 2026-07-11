# Deployment Guide

This project has two independent deployments:
- **`Main App/`** — the Streamlit app → deploy to **Streamlit Community Cloud**.
- **`Landing Page/`** — the static marketing page → deploy to **Netlify**.

## 1. Streamlit Community Cloud (`Main App/`)

1. Push this repo to GitHub (make sure `.gitignore` is committed first so `.env`/`.venv`/`data.db` never get pushed).
2. On [share.streamlit.io](https://share.streamlit.io), create a new app from your repo:
   - **Main file path:** `Main App/main.py`
   - **Python version:** 3.11 is preferred (Advanced settings → Python version, also pinned via the committed `.python-version` file). Note: as of mid-2026 Streamlit Community Cloud has a known bug ([streamlit/streamlit#15326](https://github.com/streamlit/streamlit/issues/15326)) where it sometimes ignores this setting and force-provisions Python 3.14 instead. To guard against that, every pin in `requirements.txt` below has been verified to install and run correctly on **both** Python 3.11 and 3.14, so deployment succeeds either way. The Python version can only be set at app *creation* time — if you need to change it later you must delete and redeploy the app.
3. **Secrets:** in the app's Settings → Secrets, add:
   ```toml
   GROQ_API_KEY = "your-real-key-here"
   ```
   The code already reads `st.secrets["GROQ_API_KEY"]` as a fallback (`Main App/main.py`), so no code change is needed — just don't commit your real key in `.env`.
4. `packages.txt` (repo root) installs the system libraries (`libgl1`, `libegl1`, `libgles2`, etc.) that `mediapipe`/`opencv` need on the minimal cloud container — this prevents `ImportError`/`OSError` crashes like `libGL.so.1` or `libGLESv2.so.2: cannot open shared object file`. MediaPipe's native library dlopens GLES/EGL even for CPU-only pose detection, so these are required even though the app never uses GPU rendering.
5. Once deployed, copy the app's live URL (something like `https://<your-app-name>.streamlit.app/`) and update the "Try it Live" button in `Landing Page/index.html` (the `href` on the `#cta-button` link) to point to it.

### Camera connectivity (STUN/TURN)
`get_ice_servers()` in `Main App/main.py` configures a public STUN server plus a free shared TURN relay (Open Relay Project) as a fallback, since Streamlit Cloud's network often can't establish a direct peer-to-peer WebRTC connection on STUN alone. The free relay is fine for testing/demos but is shared/rate-limited. For production reliability, get your own TURN credentials (e.g. Twilio, Metered.ca) and add them to Secrets:
```toml
TURN_URL = "turn:your-turn-host:3478"
TURN_USERNAME = "your-username"
TURN_CREDENTIAL = "your-credential"
```
`get_ice_servers()` picks these up automatically when present, ahead of the free fallback.

## 2. Netlify (`Landing Page/`)

A `netlify.toml` is committed at the repo root:
```toml
[build]
  publish = "Landing Page"
```
No build command is needed — it's plain static HTML/CSS. In Netlify, just "Import from Git" and it will pick up `netlify.toml` automatically. Alternatively, drag-and-drop the `Landing Page/` folder directly in the Netlify UI.

Before going live, add your own images/video into `Landing Page/IMGs_add_your_own/` and `Landing Page/videos_add_your_own/` (or update the `src` paths in `index.html`) — those folders are currently placeholders.

## 3. Tech stack / versions used

| Component | Version |
|---|---|
| Python | 3.11 preferred (`.python-version`); verified working on 3.14 too (see note above) |
| Streamlit | 1.54.0 |
| streamlit-webrtc | 0.64.5 |
| MediaPipe | 0.10.35 |
| OpenCV (contrib) | 4.11.0.86 |
| NumPy | 2.4.6 |
| pandas | 2.3.3 |
| groq (SDK) | 1.5.0 |
| gTTS | 2.5.3 |
| python-dotenv | 1.2.2 |
| LLM model | `llama-3.3-70b-versatile` (via Groq API) |
