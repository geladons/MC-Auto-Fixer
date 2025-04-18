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
  "log_file": "logs/latest.log",
  "api_provider": "deepseek",
  "openai_api_key": "<YOUR_OPENAI_KEY>",
  "deepseek_api_key": "<YOUR_DEEPSEEK_KEY>",
  "deepseek_api_url": "https://api.deepseek.com/v1",
  "openwebui_api": "http://127.0.0.1:5000/api/v1/generate",
  "ollama_api": "http://127.0.0.1:11434/v1/chat/completions",
  "model_name": "gpt-4"
}
```
🗺 TODO
```bash
 1.Механизм дообучения модели

 2.Поддержка онлайн-синхронизации с форумами

 3.Плагин для Spigot/BungeeCord

 4.Расширенный UI

 5.Сбор телеметрии

6.🌍 Переводы (В разработке)
Автоматический перевод плагинов на выбранный язык.
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
