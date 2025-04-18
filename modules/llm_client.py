## modules/llm_client.py
```python
import requests


def request_fix_from_llm(error_line: str, config: dict) -> str:
    # Выбор API
    provider = config.get('api_provider')
    model = config.get('model_name')
    prompt = f"Fix this Minecraft error:\n{error_line}\nRespond with JSON: {{'actions': [...]}}"

    if provider == 'ollama':
        url = config['ollama_api']
        payload = {'model': model, 'messages': [
            {'role': 'system', 'content': 'You are a Minecraft server expert.'},
            {'role': 'user', 'content': prompt}
        ], 'temperature': 0}
        r = requests.post(url, json=payload)
        r.raise_for_status()
        return r.json()['choices'][0]['message']['content']
    else:
        url = config['openwebui_api']
        payload = {'model': model, 'prompt': prompt, 'max_new_tokens': 512, 'temperature': 0}
        r = requests.post(url, json=payload)
        r.raise_for_status()
        return r.json()['results'][0]['text']
```