from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
import time

upload_bp = Blueprint("upload", __name__)

# Настройки
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_EXT = {".pdf"}

def is_pdf(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXT


@upload_bp.post("/pdf")
def upload_pdf():
    """
    Загрузка PDF файла
    ---
    consumes:
      - multipart/form-data
    parameters:
      - in: formData
        name: file
        type: file
        required: true
        description: PDF-файл для загрузки
    responses:
      201:
        description: Файл успешно сохранен
        schema:
          type: object
          properties:
            message:
              type: string
              example: saved
            filename:
              type: string
              example: 1691582451-test.pdf
            path:
              type: string
              example: /full/path/to/uploads/1691582451-test.pdf
      400:
        description: Ошибка валидации
      415:
        description: Неверный тип файла
    """
    if "file" not in request.files:
        return jsonify(error="expected form field 'file'"), 400

    f = request.files["file"]

    if f.filename == "":
        return jsonify(error="empty filename"), 400

    if not is_pdf(f.filename):
        return jsonify(error="only .pdf files are allowed"), 415

    safe_name = secure_filename(f.filename)
    ts = int(time.time())
    final_name = f"{ts}-{safe_name}"
    save_path = UPLOAD_DIR / final_name
    f.save(save_path)

    return jsonify(
        message="saved",
        filename=final_name,
        path=str(save_path.resolve())
    ), 201
