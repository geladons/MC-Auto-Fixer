## modules/file_patcher.py
```python
import os
import json
import subprocess
from zipfile import ZipFile


def apply_fix_to_file(fix_json: str, config: dict) -> str:
    try:
        data = json.loads(fix_json)
    except json.JSONDecodeError:
        return 'Invalid JSON from LLM'
    for act in data.get('actions', []):
        t = act.get('type')
        if t == 'edit_file':
            path = act['path']
            if os.path.exists(path):
                with open(path, 'r+', encoding='utf-8') as f:
                    content = f.read()
                    for r in act.get('replacements', []):
                        content = content.replace(r['find'], r['replace'])
                    f.seek(0); f.write(content); f.truncate()
            return f'Edited {path}'
        # другие экшены: download, edit_jar, restart...
    return 'No actions applied'
```