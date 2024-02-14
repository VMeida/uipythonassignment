import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

from LoadDataAndTests import LoadDataAndTests

class UIAssignment(LoadDataAndTests):
  def __init__(self, dataset_type:int=1):
    super().__init__(dataset_type)
  
  def calculate_mse(self, y):
    fig, axes = plt.subplots(10, 5, figsize=(20,20))
    sum_squares_all = {'y_ideal':[],'sum_squared_error':[]}

    # Find best y
    for i, ax in enumerate(axes.ravel()):
      y_axis = f'y{i + 1}'
      ss = np.mean(np.power(np.subtract(self.ideal[y_axis],y),2))
      sum_squares_all['y_ideal'].append(y_axis)
      sum_squares_all['sum_squared_error'].append(ss)
      
    df_results = pd.DataFrame(sum_squares_all).set_index('y_ideal')
    best_result = df_results.idxmin().values

    for i, ax in enumerate(axes.ravel()):
      y_axis = f'y{i + 1}'
      ss = np.mean(np.power(np.subtract(self.ideal[y_axis],y),2))
      sum_squares_all['y_ideal'].append(y_axis)
      sum_squares_all['sum_squared_error'].append(ss)
      ax.plot(self.ideal['x'],self.ideal[y_axis], ls='--', alpha=0.5, label='ideal')
      ax.plot(self.ideal['x'],y, ls='-', alpha=0.5, label='train')
      ax.set_title(f'Scatter for {y_axis}, MSE:{np.round(ss,3)}')
      if best_result == y_axis:
        ax.set_facecolor('xkcd:mint green')
      ax.legend()
    
    plt.tight_layout()

    print(f'Function that best fits this data is {best_result}')
    plt.show()
    
  def get_best_function(self, column_name:str='y1'):
    self.calculate_mse(self.train[column_name])    

if __name__ == "__main__":
  UIA = UIAssignment(1)
  UIA.load_all_data()
  UIA.get_best_function('y1')
  UIA.get_best_function('y2')
  UIA.get_best_function('y3')
  UIA.get_best_function('y4')