# Copyright (c) 2026 AI Software Innovation Infotech And Hardware Enterprises. All Rights Reserved.
"""
Real LLM Client - OpenAI / Anthropic (Claude) / xAI (Grok)
Keys are read from Streamlit secrets or environment variables.
"""

import os
from typing import Optional, List, Dict

def _get_secret(key: str) -> Optional[str]:
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.environ.get(key)


def chat_with_llm(
    messages: List[Dict[str, str]],
    provider: str = "auto",
    model: Optional[str] = None,
) -> str:
    """
    provider: "openai" | "anthropic" | "xai" | "auto"
    messages: [{"role": "user"/"assistant"/"system", "content": "..."}]
    """
    provider = (provider or "auto").lower()

    # Auto-detect available key
    if provider == "auto":
        if _get_secret("OPENAI_API_KEY"):
            provider = "openai"
        elif _get_secret("ANTHROPIC_API_KEY"):
            provider = "anthropic"
        elif _get_secret("XAI_API_KEY") or _get_secret("GROK_API_KEY"):
            provider = "xai"
        else:
            return None  # no key → caller should fallback

    try:
        if provider == "openai":
            return _openai_chat(messages, model or "gpt-4o-mini")
        elif provider == "anthropic":
            return _anthropic_chat(messages, model or "claude-3-5-sonnet-20241022")
        elif provider in ("xai", "grok"):
            return _xai_chat(messages, model or "grok-beta")
        else:
            return None
    except Exception as e:
        return f"[LLM Error: {str(e)[:200]}]"


def _openai_chat(messages, model: str) -> str:
    from openai import OpenAI
    key = _get_secret("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY not found in secrets/env")
    client = OpenAI(api_key=key)
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=2048,
    )
    return resp.choices[0].message.content or ""


def _anthropic_chat(messages, model: str) -> str:
    from anthropic import Anthropic
    key = _get_secret("ANTHROPIC_API_KEY")
    if not key:
        raise ValueError("ANTHROPIC_API_KEY not found in secrets/env")
    client = Anthropic(api_key=key)

    system = ""
    chat_msgs = []
    for m in messages:
        if m["role"] == "system":
            system = m["content"]
        else:
            chat_msgs.append({"role": m["role"], "content": m["content"]})

    kwargs = {"model": model, "max_tokens": 2048, "messages": chat_msgs}
    if system:
        kwargs["system"] = system

    resp = client.messages.create(**kwargs)
    return resp.content[0].text if resp.content else ""


def _xai_chat(messages, model: str) -> str:
    """xAI Grok uses OpenAI-compatible API"""
    from openai import OpenAI
    key = _get_secret("XAI_API_KEY") or _get_secret("GROK_API_KEY")
    if not key:
        raise ValueError("XAI_API_KEY or GROK_API_KEY not found in secrets/env")
    client = OpenAI(
        api_key=key,
        base_url="https://api.x.ai/v1",
    )
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=2048,
    )
    return resp.choices[0].message.content or ""


def has_any_llm_key() -> bool:
    return bool(
        _get_secret("OPENAI_API_KEY")
        or _get_secret("ANTHROPIC_API_KEY")
        or _get_secret("XAI_API_KEY")
        or _get_secret("GROK_API_KEY")
    )
