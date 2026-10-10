# AISIH Multi-Agent Gateway v3.0 – Full Manual

## Features
- Home = AI Chat (Hinglish + English + 15 languages)
- Real LLM: OpenAI / Claude / Grok (API key)
- Image Studio: Upload, brightness/contrast/blur/grayscale, AI image prompt
- Video Studio: Upload, AI script + shot list, YouTube search helper, related topics
- Learning Agent: Save lessons, sub-tasks, self-improvement notes
- Web Research: Related topics + info collection plan
- Multi-Agent System
- Admin panel

## Limits (honest)
- Real DALL·E image pixels → needs OpenAI image API
- Full Canva / pro video editor → not inside Streamlit
- YouTube bulk download → legal/ToS; use local tools
- True neural self-training → needs GPU training infra; here we store learning memory

## Install
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Cloud Secrets
```toml
OPENAI_API_KEY = "sk-..."
ANTHROPIC_API_KEY = "sk-ant-..."
XAI_API_KEY = "xai-..."
```

## Default admin
ceo / AI Software Innovation Infotech And Hardware Enterprises@CEO2026

