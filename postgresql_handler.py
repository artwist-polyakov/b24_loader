from sqlalchemy import create_engine, inspect, text
from tqdm import tqdm

def get_columns_and_types_postgresql(table, host, port, user, password, db_name):
    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}") 
    inspector = inspect(engine)
    columns = inspector.get_columns(table)
    return columns

def test_connection(host, port, user, password, db_name):
    try:
        engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}") 
        result = engine.execute("SELECT 1")
        print("Successfully connected to the database.")
    except Exception as e:
        print("Failed to connect to the database.")
        print(str(e))

def load_data_to_sql(data, table, fields_matching, host, port, user, password, db_name):
    # Создаем движок SQLAlchemy
    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}") 
    total = len(data)
    progress_bar = tqdm(total=total, position=0, leave=True)
    k = 0
    # Начинаем транзакцию
    with engine.begin() as connection:
        for row in data:
            row = {fields_matching.get(key, key): value for key, value in row.items()}
            # Форматируем SQL запрос
            sql = text(f"INSERT INTO {table} ({','.join(row.keys())}) VALUES ({','.join(':' + key for key in row.keys())})")
            # Выполняем SQL запрос
            connection.execute(sql, **row)
            k+=1
            if k % 100 == 0:
                progress_bar.update(100)
