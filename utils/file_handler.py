import pandas as pd
import io

def read_file(file_storage):
    filename = file_storage.filename
    data_bytes = file_storage.read()

    if filename.endswith('.csv'):
        df = pd.read_csv(io.BytesIO(data_bytes))
    elif filename.endswith('.xlsx') or filename.endswith('.xls'):
        df = pd.read_excel(io.BytesIO(data_bytes))
    else:
        raise ValueError("Unsupported file format")
    return df, data_bytes