# MC-Auto-Fixer 🛠️ (В разработке)

> Интеллектуальный инструмент для автоматической диагностики и исправления ошибок Minecraft-серверов, включая поддержку Forge, Fabric, модов и плагинов.

---

## 🚀 Возможности

- Чтение логов Minecraft-сервера
- Отправка логов в локальную LLM через Ollama API
- Получение инструкции по починке
- Автоматическое исправление:
  - `config/*.json`, `*.toml`, `*.yml`
  - `.jar`-файлов модов и плагинов (анализ и патчинг классов)
- UI для настройки через браузер
- Поддержка всех версий Minecraft
- Возможность дообучения на форумах (в разработке)

---

## 📦 Установка

```bash
git clone https://github.com/geladons/MC-Auto-Fixer.git
cd MC-Auto-Fixer
pip install -r requirements.txt
# Убедись, что Ollama/OpenWebUI работают на своих портах:
#   OpenWebUI → http://<ip>:5000
#   Ollama →      http://<ip>:11434
# запускаем UI MC Auto Fixer:
python main.py
# открываем в браузере:
http://localhost:5500
```
🛠 Настройки
```bash
Создай settings.json или настрой через UI:

json

{
  "ollama_api": "http://<IP>:11434/api/generate",
  "model": "mistral",
  "minecraft_path": "/path/to/server"
}
```
🗺 TODO
```bash
 Механизм дообучения модели

 Поддержка онлайн-синхронизации с форумами

 Плагин для Spigot/BungeeCord

 Расширенный UI

 Сбор телеметрии (опционально)
```
🌍 Переводы
```bash
Добавь ?lang=ru к URL или используй GitHub Translate.
```
⚠️ Отказ от ответственности
```bash
Автоматическая правка .jar-файлов может поломать мод. Обязательно сделай бекап, преимущественно используйте на тестовых серверах.
```
🧠 Автор
```bash
Разработка: @geladons
2025 © MIT License
```
