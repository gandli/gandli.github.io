#!/usr/bin/env python3
"""Cloudflare Workers AI helper — shared by all scripts."""

import os
import json
import requests

CF_API_BASE = "https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run"
TEXT_MODEL = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
IMAGE_MODEL = "@cf/black-forest-labs/FLUX-1-schnell"


def _headers():
    return {"Authorization": f"Bearer {os.environ['CF_API_TOKEN']}", "Content-Type": "application/json"}


def _url(model):
    account_id = os.environ["CF_ACCOUNT_ID"]
    return f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}"


def chat(prompt: str, max_tokens: int = 2048, model: str = TEXT_MODEL) -> str:
    """Send a single-turn chat and return the assistant reply."""
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
    }
    resp = requests.post(_url(model), headers=_headers(), json=payload, timeout=120)
    resp.raise_for_status()
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
    resp.raise_for_status()
    if resp.headers.get("content-type", "").startswith("image/"):
        return resp.content
    # Fallback: JSON with base64
    import base64
    data = resp.json()
    return base64.b64decode(data["result"]["image"])
