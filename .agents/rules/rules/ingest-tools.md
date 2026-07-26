---
paths:
  - "raw/**"
---

# Ingest tooling: markitdown

Когда обрабатываешь новые источники в `raw/` (PDF, docx, pptx, xlsx, аудио, изображения, HTML) — конвертируй их в markdown через `markitdown`, а не парси вручную.

## Базовая конвертация

```bash
markitdown path-to-file.pdf > document.md
# или явно указать выходной файл
markitdown path-to-file.pdf -o document.md
```

## Правила

- Всегда сохраняй результат конвертации рядом с оригиналом в `raw/`, с тем же именем, но расширением `.md` — оригинальный файл (pdf/docx/...) не удаляй, он остаётся источником правды.
- Если конвертация с `markitdown` не даёт читаемого текста (например, скан без OCR-слоя) — не пытайся угадывать содержимое, сообщи об этом и предложи Azure Document Intelligence (`-d`) или ручную обработку.
- Для аудио-источников (подкасты, войс-заметки) конвертация зависит от ffmpeg — если увидишь `RuntimeWarning: Couldn't find ffmpeg`, предупреди пользователя, что нужно `brew install ffmpeg`, конвертация может не сработать.

## Опциональные возможности

Azure Document Intelligence для сложных PDF/сканов (нужен настроенный Azure-ресурс):
```bash
markitdown path-to-file.pdf -o document.md -d -e "<endpoint>"
```

Python API (используй, если нужно встроить конвертацию в более сложный скрипт, а не разовый вызов):
```python
from markitdown import MarkItDown
md = MarkItDown(enable_plugins=False)
result = md.convert("test.xlsx")
print(result.text_content)
```

## Не делай

- Не запускай `markitdown` без виртуального окружения / без проверки, что команда вообще доступна (`which markitdown`) — если не установлен глобально через `uv tool install`, может понадобиться активировать venv.
- Не конвертируй файлы вне `raw/` этим правилом — оно предназначено только для пайплайна ingest.
