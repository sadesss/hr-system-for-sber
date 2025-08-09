from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
from pypdf import PdfReader
import time

from app.db import Resume, SessionLocal

from app.agents.agent import get_reqest
from app.agents.promts import resume_in

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

    reader = PdfReader(f)
    text = ""
    for page in reader.pages:
        text = text + page.extract_text()

    created = 0
    with SessionLocal() as session:
        objs = [Resume(resume_text=text)]
        session.add_all(objs)
        session.commit()
        created = len(objs)

    text_resume = session.query(Resume).first().resume_text
    #print(all_resume)

    result = get_reqest(text_resume, resume_in)
    print(result)

    return jsonify(
        message="saved",
        filename=final_name,
        path=str(save_path.resolve()),
        text=result  # содержимое PDF
    ), 201
