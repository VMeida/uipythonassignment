import pandas as pd
from sqlalchemy import create_engine

class LoadData:
    """This class is responsible for loading and testing the bases for the UI Assignment.
    
        Parameters:
            dataset_type (int): 1 or 2 depending on the dataset used for this assignment. Default is 1.
    """    
    
    def __init__(self, dataset_type:int=1):
        self.dataset_type = dataset_type
        
    def create_mysql_engine(self):
        """Creates the engine for reading SQlLite files, depending on the self.dataset_type.
        """        
        if self.dataset_type == 1:
            uri = f"sqlite:///data/uiassignmentdb.db"
        elif self.dataset_type == 2:
            uri = f"sqlite:///data/uiassignmentdb2.db"
        self.engine = create_engine(uri)

    def load_train(self):
        """Loads the 'train' dataset
        """        
        with self.engine.connect() as conn: 
            train_query = 'SELECT * FROM train'
            self.train = pd.read_sql(train_query, conn)

        print(self.train.head())

    def load_ideal(self):
        """Loads the 'ideal' dataset
        """  
        with self.engine.connect() as conn: 
            ideal_query = 'SELECT * FROM ideal'
            self.ideal = pd.read_sql(ideal_query, conn)

        print(self.ideal.head())

    def load_test(self):
        """Loads the 'test' dataset
        """  
        with self.engine.connect() as conn: 
            test_query = 'SELECT * FROM test'
            self.test = pd.read_sql(test_query, conn)

        print(self.test.head())
        
    def load_all_data(self):
        """Wrapper of all load functions
        """  
        self.load_train()
        self.load_test()
        self.load_ideal()