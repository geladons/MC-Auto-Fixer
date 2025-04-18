## modules/file_patcher.py
import os
import json
import subprocess
from zipfile import ZipFile


def download_file(url: str, dest: str) -> str:
    """
    Скачивает файл по URL в dest с помощью requests или wget.
    """
    try:
        import requests
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(dest, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        return f"Downloaded {url} -> {dest}"
    except ImportError:
        subprocess.run(['wget', url, '-O', dest], check=True)
        return f"Downloaded {url} -> {dest}"


def edit_jar(jar_path: str, class_name: str, diff_patch: str) -> str:
    """
    Распаковывает JAR, сохраняет патч и собирает новый JAR.
    """
    temp_dir = jar_path + '_tmp'
    if os.path.exists(temp_dir):
        subprocess.run(['rm', '-rf', temp_dir], check=True)
    os.makedirs(temp_dir)

    # Распаковать JAR
    with ZipFile(jar_path, 'r') as jar:
        jar.extractall(temp_dir)

    # Сохранить патч
    patch_file = os.path.join(temp_dir, f"{class_name.split('.')[-1]}.patch")
    with open(patch_file, 'w', encoding='utf-8') as f:
        f.write(diff_patch)

    # Собрать новый JAR
    new_jar = jar_path.replace('.jar', '_fixed.jar')
    cwd = os.getcwd()
    os.chdir(temp_dir)
    subprocess.run(['jar', 'cf', os.path.join(cwd, new_jar), '.'], check=True)
    os.chdir(cwd)

    return f"Patched JAR created: {new_jar}"


def restart_server(command: str) -> str:
    """
    Перезапускает сервер командой shell.
    """
    subprocess.run(command, shell=True, check=True)
    return f"Server restarted with: {command}"


def apply_fix_to_file(fix_json: str, config: dict) -> str:
    """
    Применяет список действий из JSON, возвращает строку с результатами.
    """
    try:
        data = json.loads(fix_json)
    except json.JSONDecodeError:
        return 'Invalid JSON from LLM'

    results = []
    for act in data.get('actions', []):
        act_type = act.get('type')
        if act_type == 'edit_file':
            path = act.get('path')
            if os.path.exists(path):
                with open(path, 'r+', encoding='utf-8') as f:
                    content = f.read()
                    for r in act.get('replacements', []):
                        content = content.replace(r['find'], r['replace'])
                    f.seek(0)
                    f.write(content)
                    f.truncate()
                results.append(f"Edited file: {path}")
            else:
                results.append(f"File not found: {path}")
        elif act_type == 'download':
            url = act.get('url')
            dest = act.get('to')
            results.append(download_file(url, dest))
        elif act_type == 'edit_jar':
            jar_path = act.get('jar_path')
            cls = act.get('class')
            patch = act.get('patch')
            results.append(edit_jar(jar_path, cls, patch))
        elif act_type == 'restart_server':
            cmd = act.get('command')
            results.append(restart_server(cmd))
        else:
            results.append(f"Unknown action type: {act_type}")

    return '; '.join(results)
