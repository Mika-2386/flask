# from flask import Flask, request
# import os
# from models import Base, UploadedFile, DataAnalysisResult

# app = Flask(__name__)

# UPLOAD_FOLDER = 'Downloaded'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route('/upload', methods=['POST'])
# def upload():
#     filename = request.headers.get('X-Filename')
#     if not filename:
#         return "Заголовок X-Filename не найден", 400
#     save_path = os.path.join(UPLOAD_FOLDER, filename)
#     with open(save_path, 'wb') as f:
#         f.write(request.data)
#     return f"Файл {filename} успешно загружен", 200

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)


# ----------------------2----------------------

from flask import Flask, request, Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, UploadedFile, DataAnalysisResult
import config
from utils.file_handler import read_file
from utils.data_utils import clean_data, analyze_data
# import json

app = Flask(__name__)

# Настройка базы данных
engine = create_engine(config.DATABASE_URI)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@app.route('/upload', methods=['POST'])
def upload():
    session = Session()
    try:
        file = request.files['file']
        df, data_bytes = read_file(file)

        # Сохраняем файл в БД
        new_file = UploadedFile(filename=file.filename, data=data_bytes)
        session.add(new_file)
        session.commit()
        file_id = new_file.id

        # Очистка данных
        df_clean = clean_data(df)

        # Анализ данных
        mean, median, corr = analyze_data(df_clean)

        # Сохраняем результаты
        result = DataAnalysisResult(
            file_id=file_id,
            mean=str(mean),
            median=str(median),
            correlation=str(corr)
        )
        session.add(result)
        session.commit()

        return Response(f"Файл успешно загружен и проанализирован. ID файла: {file_id}", status=200)
    except Exception as e:
        session.rollback()
        return Response(f"Ошибка: {str(e)}", status=400)
    finally:
        session.close()

@app.route('/stats/<int:file_id>', methods=['GET'])
def get_stats(file_id):
    session = Session()
    try:
        result = session.query(DataAnalysisResult).filter_by(file_id=file_id).first()
        if not result:
            return Response("Результаты не найдены", status=404)
        # Можно возвращать как plain text или в другом формате
        response_text = f"Средние значения: {result.mean}\nМедиана: {result.median}\nКоэффициент корреляции: {result.correlation}"
        return Response(response_text, content_type='text/plain')
    except Exception as e:
        return Response(f"Ошибка: {str(e)}", status=500)
    finally:
        session.close()

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(debug=True)


