#!/usr/bin/env python3
"""Cloudflare Workers AI helper — shared by all scripts."""

import os
import sys
import json
import requests

CF_API_BASE = "https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run"
TEXT_MODEL = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
IMAGE_MODEL = "@cf/black-forest-labs/FLUX-1-schnell"
TTS_MODEL = "@cf/myshell-ai/melotts"


def _headers():
    return {"Authorization": f"Bearer {os.environ['CF_API_TOKEN']}", "Content-Type": "application/json"}


def _url(model):
    account_id = os.environ["CF_ACCOUNT_ID"]
    return f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}"


def _check_response(resp, context=""):
    """Check response and print detailed error info on failure."""
    if resp.status_code >= 400:
        print(f"❌ CF API error ({context}): HTTP {resp.status_code}", file=sys.stderr)
        print(f"   URL: {resp.url}", file=sys.stderr)
        try:
            body = resp.json()
            print(f"   Response: {json.dumps(body, indent=2)}", file=sys.stderr)
        except Exception:
            print(f"   Response: {resp.text[:500]}", file=sys.stderr)
        resp.raise_for_status()


def chat(prompt: str, max_tokens: int = 2048, model: str = TEXT_MODEL) -> str:
    """Send a single-turn chat and return the assistant reply."""
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
    }
    resp = requests.post(_url(model), headers=_headers(), json=payload, timeout=120)
    _check_response(resp, f"chat/{model}")
    data = resp.json()
    if not data.get("success"):
        raise RuntimeError(f"CF AI error: {data.get('errors')}")
    return data["result"]["response"]


def generate_image(prompt: str) -> bytes:
    """Generate an image and return raw PNG bytes."""
    payload = {"prompt": prompt, "num_steps": 4}
    headers = _headers()
    headers["Accept"] = "image/png"
    resp = requests.post(_url(IMAGE_MODEL), headers=headers, json=payload, timeout=120)
    _check_response(resp, "image")
    if resp.headers.get("content-type", "").startswith("image/"):
        return resp.content
    # Fallback: JSON with base64
    import base64
    data = resp.json()
    return base64.b64decode(data["result"]["image"])


def tts(text: str, lang: str = "zh") -> bytes:
    """Generate speech audio bytes via MeloTTS. Returns WAV/MP3 bytes."""
    lang_map = {"zh": "zh", "en": "en", "ja": "ja", "ko": "ko", "fr": "fr", "es": "es"}
    payload = {"text": text, "lang": lang_map.get(lang, "en")}
    headers = _headers()
    headers["Accept"] = "audio/wav"
    resp = requests.post(_url(TTS_MODEL), headers=headers, json=payload, timeout=180)
    _check_response(resp, "tts")
    if resp.headers.get("content-type", "").startswith("audio/"):
        return resp.content
    # Fallback JSON
    import base64
    data = resp.json()
    return base64.b64decode(data["result"]["audio"])
