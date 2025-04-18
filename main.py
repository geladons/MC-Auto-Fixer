## main.py
```python
#!/usr/bin/env python3
import os
import json
import threading
from flask import Flask, request, jsonify, send_from_directory
from modules.log_parser import extract_errors
from modules.llm_client import request_fix_from_llm
from modules.file_patcher import apply_fix_to_file

CONFIG_FILE = 'settings.json'
app = Flask(__name__, static_folder='static')

# Меняем рабочий каталог на папку запуска
import sys
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))
else:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))


def load_config():
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def index():
    return send_from_directory('static', 'settings_page.html')

@app.route('/api/config', methods=['GET', 'POST'])
def config_endpoint():
    if request.method == 'POST':
        data = request.json
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return jsonify({'status': 'saved'})
    config = load_config()
    return jsonify(config)

@app.route('/api/run', methods=['POST'])
def run_endpoint():
    config = load_config()
    log_path = config.get('log_file')
    errors = extract_errors(log_path)
    results = []
    for err in errors:
        fix = request_fix_from_llm(err, config)
        res = apply_fix_to_file(fix, config)
        results.append({'error': err, 'result': res})
    return jsonify(results)

def run_background_monitor():
    config = load_config()
    extract_errors(config.get('log_file'), watch=True,
                   on_errors=lambda errs: [apply_fix_to_file(request_fix_from_llm(e, config), config) for e in errs])

if __name__ == '__main__':
    # Запускаем мониторинг в фоне
    threading.Thread(target=run_background_monitor, daemon=True).start()
    # Запускаем веб-сервер настроек и контроллера
    app.run(host='0.0.0.0', port=5500)
```

---