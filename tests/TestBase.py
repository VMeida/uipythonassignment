import pandas as pd
from sqlalchemy import create_engine
import pytest

@pytest.mark.parametrize('dataset_type',[1])
class TestBase:
        
    def create_mysql_engine(self, dataset_type:int=1):
        if dataset_type == 1:
            uri = f"sqlite:///data/uiassignmentdb.db"
        elif dataset_type == 2:
            uri = f"sqlite:///data/uiassignmentdb2.db"
        self.engine = create_engine(uri)

        
    def test_train_base_exists(self, dataset_type:int):
        self.create_mysql_engine(dataset_type)
        with self.engine.connect() as conn:
            query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='train';"
            res = pd.read_sql(query, conn)
            
        assert len(res) > 0
    
    def test_test_base_exists(self, dataset_type:int):
        self.create_mysql_engine(dataset_type)
        with self.engine.connect() as conn:
            query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='test';"
            res = pd.read_sql(query, conn)
            
        assert len(res) > 0
        
    def test_ideal_base_exists(self,dataset_type:int):
        self.create_mysql_engine(dataset_type)
        with self.engine.connect() as conn:
            query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='ideal';"
            res = pd.read_sql(query, conn)
            
        assert len(res) > 0
        
    def test_train_ideal_lenght(self, dataset_type:int):
        self.create_mysql_engine(dataset_type)
        with self.engine.connect() as conn:
            query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='train';"
            train = pd.read_sql(query, conn)
        self.create_mysql_engine(dataset_type)
        with self.engine.connect() as conn:
            query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='ideal';"
            ideal = pd.read_sql(query, conn)
        
        assert train.shape[0] == ideal.shape[0]