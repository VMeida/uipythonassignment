import pandas as pd
from sqlalchemy import create_engine

def create_mysql_engine():
    uri = f"sqlite:///data/uiassignmentdb.db"
    engine = create_engine(uri)

    return engine
!
def load_data(engine):
    with engine.connect() as conn: 
        train_query = 'SELECT * FROM train'
        test_query = 'SELECT * FROM test'
        ideal_query = 'SELECT * FROM ideal'
        train = pd.read_sql(train_query, conn)
        test = pd.read_sql(test_query, conn)
        ideal = pd.read_sql(ideal_query, conn)

    print(train.head())
    print(test.head())
    print(ideal.head())
    
    return train, test, ideal
    
def main():
    engine = create_mysql_engine()
    train, test, ideal = load_data(engine)
    
    
if __name__ == "__main__":
    main()