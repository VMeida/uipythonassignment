import pandas as pd
from sqlalchemy import create_engine

class LoadDataAndTests:
    def __init__(self, dataset_type:int=1):
        self.dataset_type = dataset_type
        
    def create_mysql_engine(self):
        if self.dataset_type == 1:
            uri = f"sqlite:///data/uiassignmentdb.db"
        elif self.dataset_type == 1:
            uri = f"sqlite:///data/uiassignmentdb2.db"
        self.engine = create_engine(uri)

    def load_train(self):
        with self.engine.connect() as conn: 
            train_query = 'SELECT * FROM train'
            self.train = pd.read_sql(train_query, conn)

        print(self.train.head())

    def load_ideal(self):
        with self.engine.connect() as conn: 
            ideal_query = 'SELECT * FROM ideal'
            self.ideal = pd.read_sql(ideal_query, conn)

        print(self.ideal.head())

    def load_test(self):
        with self.engine.connect() as conn: 
            test_query = 'SELECT * FROM test'
            self.test = pd.read_sql(test_query, conn)

        print(self.test.head())
        
    def load_all_data(self):
        self.create_mysql_engine()
        self.load_train()
        self.load_test()
        self.load_ideal()