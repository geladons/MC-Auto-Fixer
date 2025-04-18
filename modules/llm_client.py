## modules/llm_client.py
import os
import json
import requests

# Для OpenAI
import openai

def request_fix_from_llm(error_line: str, config: dict) -> str:
    """
    Универсальный клиент LLM: поддерживает ollama, openwebui, openai, deepseek.
    """
    provider = config.get('api_provider', 'ollama').lower()
    model    = config.get('model_name')

    prompt = (
        "You are a Minecraft server expert. "
        f"Please fix this error:\n\n{error_line}\n\n"
        "Respond with JSON: {'actions': [...]}"
    )

    if provider == 'openai':
        # :contentReference[oaicite:7]{index=7}
        openai.api_key = os.getenv('OPENAI_API_KEY') or config.get('openai_api_key')
        resp = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return resp.choices[0].message.content  # :contentReference[oaicite:8]{index=8}

    elif provider == 'deepseek':
        # :contentReference[oaicite:9]{index=9}
        api_key = config.get('deepseek_api_key')
        base_url = config.get('deepseek_api_url', 'https://api.deepseek.com/v1')
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': model,
            'messages': [{"role": "user", "content": prompt}],
            'temperature': 0
        }
        r = requests.post(f"{base_url}/chat/completions", 
                          headers=headers, 
                          json=payload)
        r.raise_for_status()
        return r.json()['choices'][0]['message']['content']  # :contentReference[oaicite:10]{index=10}

    elif provider == 'ollama':
        url = config['ollama_api']
        payload = {'model': model, 'messages': [
            {'role': 'system', 'content': 'You are a Minecraft expert.'},
            {'role': 'user', 'content': prompt}
        ], 'temperature': 0}
        r = requests.post(url, json=payload)
        r.raise_for_status()
        return r.json()['choices'][0]['message']['content']  # :contentReference[oaicite:11]{index=11}

    else:  # openwebui
        url = config['openwebui_api']
        payload = {'model': model, 'prompt': prompt,
                   'max_new_tokens': 512, 'temperature': 0}
        r = requests.post(url, json=payload)
        r.raise_for_status()
        return r.json()['results'][0]['text']