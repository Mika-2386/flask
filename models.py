from sqlalchemy import Column, Integer, String, LargeBinary, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UploadedFile(Base):
    __tablename__ = 'uploaded_files'
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    data = Column(LargeBinary, nullable=False)

class DataAnalysisResult(Base):
    __tablename__ = 'analysis_results'
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer)
    mean = Column(String)  # можно сериализовать как строку
    median = Column(String)
    correlation = Column(String)