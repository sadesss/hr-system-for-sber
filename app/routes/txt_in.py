from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
import time

upload_txt = Blueprint("upload_txt", __name__)

# Папка для txt-требований
REQ_DIR = Path("requirements")
REQ_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_TXT_EXT = {".txt"}

def is_txt(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_TXT_EXT

@upload_txt.post("/requirements")
def upload_requirements():
    """
    Приём формальных требований к вакансии (txt файл или текстом)
    ---
    consumes:
      - multipart/form-data
    parameters:
      - in: formData
        name: file
        type: file
        required: false
        description: Текстовый файл .txt с требованиями
      - in: formData
        name: text
        type: string
        required: false
        description: Требования как обычный текст (если не загружается файл)
    responses:
      201:
        description: Требования приняты
        schema:
          type: object
          properties:
            message:
              type: string
            filename:
              type: string
              nullable: true
            path:
              type: string
              nullable: true
            length:
              type: integer
            preview:
              type: string
            text:
              type: string
      400:
        description: Нет текста и файла
      415:
        description: Поддерживаются только .txt файлы
    """
    # Можно прислать либо file=.txt, либо text=...
    form_text = request.form.get("text")
    f = request.files.get("file")

    if not form_text and not f:
        return jsonify(error="provide either 'text' field or 'file' (.txt)"), 400

    saved_filename = None
    saved_path = None

    if f:
        if f.filename == "":
            return jsonify(error="empty filename"), 400
        if not is_txt(f.filename):
            return jsonify(error="only .txt files are allowed"), 415

        safe_name = secure_filename(f.filename)
        final_name = f"{int(time.time())}-{safe_name}"
        save_path = REQ_DIR / final_name
        f.save(save_path)
        saved_filename = final_name
        saved_path = str(save_path.resolve())

        # читаем содержимое
        with open(save_path, "r", encoding="utf-8", errors="ignore") as fp:
            text = fp.read()
    else:
        text = (form_text or "").strip()

    preview = text[:500]  # короткий просмотр

    return jsonify(
        message="requirements accepted",
        filename=saved_filename,
        path=saved_path,
        length=len(text),
        preview=preview,
        text=text
    ), 201
