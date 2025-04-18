## modules/log_parser.py
```python
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def extract_errors(log_path, watch=False, on_errors=None):
    errors = []
    pattern = re.compile(r"(ERROR|Exception)")
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if pattern.search(line):
                errors.append(line.strip())
    if watch and on_errors:
        class Handler(FileSystemEventHandler):
            def on_modified(self, event):
                new_errors = extract_errors(log_path)
                if new_errors:
                    on_errors(new_errors)
        obs = Observer(); obs.schedule(Handler(), path='.', recursive=False); obs.start()
    return errors
```