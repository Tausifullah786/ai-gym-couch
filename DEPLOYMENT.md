# Deployment Guide

This project has two independent deployments:
- **`Main App/`** — the Streamlit app → deploy to **Streamlit Community Cloud**.
- **`Landing Page/`** — the static marketing page → deploy to **Netlify**.

## 1. Streamlit Community Cloud (`Main App/`)

1. Push this repo to GitHub (make sure `.gitignore` is committed first so `.env`/`.venv`/`data.db` never get pushed).
2. On [share.streamlit.io](https://share.streamlit.io), create a new app from your repo:
   - **Main file path:** `Main App/main.py`
   - **Python version:** 3.11 (Advanced settings → Python version). A `.python-version` file pinning `3.11` is also committed, since `mediapipe==0.10.14` only officially supports Python 3.8–3.11.
3. **Secrets:** in the app's Settings → Secrets, add:
   ```toml
   GROQ_API_KEY = "your-real-key-here"
   ```
   The code already reads `st.secrets["GROQ_API_KEY"]` as a fallback (`Main App/main.py`), so no code change is needed — just don't commit your real key in `.env`.
4. `packages.txt` (repo root) installs the system libraries (`libgl1`, etc.) that `mediapipe`/`opencv` need on the minimal cloud container — this prevents `ImportError: libGL.so.1` crashes.
5. Once deployed, copy the app's live URL (something like `https://<your-app-name>.streamlit.app/`) and update the "Try it Live" button in `Landing Page/index.html` (the `href` on the `#cta-button` link) to point to it.

### Known limitation: camera connectivity
`webrtc_streamer` is configured with a public STUN server only (no TURN server). Most users connect fine, but some behind restrictive/corporate NATs may fail to establish the camera stream. If this becomes a problem, add a TURN provider (e.g. Twilio, Metered, or an open TURN relay) and pass its credentials into `rtc_configuration` in `Main App/main.py`.

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
| Python | 3.11 (pinned via `.python-version`; dev machine used 3.12) |
| Streamlit | 1.54.0 |
| streamlit-webrtc | 0.64.5 |
| MediaPipe | 0.10.14 |
| OpenCV (headless) | 4.10.0.84 |
| NumPy | 2.5.0 |
| pandas | 2.2.3 |
| groq (SDK) | 1.5.0 |
| gTTS | 2.5.3 |
| python-dotenv | 1.2.2 |
| LLM model | `llama-3.3-70b-versatile` (via Groq API) |
