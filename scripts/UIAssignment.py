import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from LoadData import LoadData

class UIAssignment(LoadData):
  """This class is responsible for solving the final assignment problem. 

  Args:
      dataset_type (int): 1 or 2, depending on the dataset provided by the professor.
  """  
  def __init__(self, dataset_type:int=1):
    super().__init__(dataset_type)
    self.best_results = {'y_train':[],'best_result':[],'max_deviation':[]}
    
  def calculate_mse(self, y_true:float, y:float): 
    """_summary_

    Args:
        y_true (float): true value of y
        y (float): predicted values of y

    Returns:
        tuple: return 2 values, the mean quared error, and the maximum deviation (maximum sum of squared errors)
    """     
    sse = np.power(np.subtract(y_true,y),2)
    mse = np.mean(sse)
    max_deviation = np.max(sse)

    return mse, max_deviation

  def plot_best_function_results(self, y:pd.Series):
    """Function that plots the receives pd.Series, and outputs its comparison against all 50 ideal functions

    Args:
        y (pd.Series): Values to be compared to the ideal functions
    """    
    fig, axes = plt.subplots(10, 5, figsize=(20,20))
    sum_squares_all = {'y_ideal':[],'sum_squared_error':[],'max_deviation':[]}
    
    # First Loop: find best result
    for i, ax in enumerate(axes.ravel()):
      y_axis = f'y{i + 1}'
      
      ss,max_deviation = self.calculate_mse(self.ideal[y_axis],y)
      sum_squares_all['y_ideal'].append(y_axis)
      sum_squares_all['sum_squared_error'].append(ss)
      sum_squares_all['max_deviation'].append(max_deviation)
      
    df_results = pd.DataFrame(sum_squares_all).set_index('y_ideal')
    best_result = df_results['sum_squared_error'].idxmin()
    best_result_dev = df_results[df_results.index == best_result]['max_deviation'].values[0]
    
    self.best_results['y_train'].append(y.name)
    self.best_results['best_result'].append(best_result)
    self.best_results['max_deviation'].append(best_result_dev)
    
    # Second loop: plot results
    for i, ax in enumerate(axes.ravel()):
      y_axis = f'y{i + 1}'

      ax.plot(self.ideal['x'], self.ideal[y_axis], ls='--', alpha=0.5, label='ideal')
      ax.plot(self.ideal['x'],y, ls='-', alpha=0.5, label='train')
      ax.set_title(f"Scatter for {y_axis}, MSE:{np.round(sum_squares_all['sum_squared_error'][i],3)}")
      if best_result == y_axis:
        ax.set_facecolor('xkcd:mint green')
      ax.legend()
    
    plt.tight_layout()

    print(f'Function that best fits this data is {best_result}')
    plt.savefig(f"img/ideal_function_{y.name}.png",bbox_inches='tight',dpi=100)
    plt.show()
    
  def get_best_function(self, column_name:str='y1'):
    """Wrapper that filters train data based on the name of the column received, and plots the results.

    Args:
        column_name (str, optional): Name of the column in train dataset. Defaults to 'y1'.
    """    
    self.plot_best_function_results(self.train[column_name])
    
  def plot_compare_ideal_and_test_before(self):
    """Function to plot the best results and all test points before testing is they are inside their deviation.
    """    
    plt.figure(figsize=(10,5))

    for result in self.best_results['best_result']:
      plt.plot(self.ideal.x, self.ideal[result], label=result)
    plt.scatter(self.test.x, self.test.y, color='lightgray', label='Test points')
    plt.legend()
    plt.title('Test points vs Ideal functions')
    plt.show()
    
  def row_is_in_deviation(self, row:pd.Series, best_result:str, deviation:float):
    """_summary_

    Args:
        row (pd.Series): Row containing the ideal and test values to be compared
        best_result (str): Column name of the ideal dataset to be compares with test dataset y
        deviation (float): Maximum deviation

    Returns:
        _type_: Column name of the ideal dataset to be compares with test dataset y, if value is smaller then the max deviation
    """    
    sse,_ = self.calculate_mse(row[best_result],row['y'])
    if sse <= deviation:
      return best_result
  
  def calculate_test_points(self):
    """Function to calculate which points are inside the maximum deviation of ideal functions
    """    
    df_best_results = pd.DataFrame(self.best_results)
    df_test_ideal = self.test.copy()
    for _,row in df_best_results.iterrows():
      df_test_ideal = pd.merge(df_test_ideal, self.ideal[['x',row['best_result']]], on='x', how='left')
      df_test_ideal.loc[:,f"test_ok_{row['best_result']}"] = df_test_ideal.apply(self.row_is_in_deviation, best_result=row['best_result'], deviation=row['max_deviation'],axis=1)
      
    test_columns = [col for col in df_test_ideal.columns if col.startswith('test_ok')]

    df_test_ideal.loc[:,f"test_ok"] = pd.NA
    for i,col in enumerate(test_columns):
      globals()[f'df_{i}'] = df_test_ideal[col]
      df_test_ideal['test_ok'] = df_test_ideal['test_ok'].combine_first(globals()[f'df_{i}'])

    df_test_ideal = df_test_ideal.drop(test_columns,axis=1)

    df_test_ideal.loc[:,'color'] = ['green' if not col == None else 'red' for col in df_test_ideal['test_ok']]

    print(df_test_ideal[df_test_ideal['test_ok'].notna()])
    
    self.df_test_ideal = df_test_ideal
    
  def plot_compare_ideal_and_test_after(self):
    """Function to plot the best results and all test points after testing is they are inside their deviation.
       Green for inside max devitaion and red for out.
    """    
    plt.figure(figsize=(10,5))
    for result in self.best_results['best_result']:
      plt.plot(self.ideal.x, self.ideal[result], label=result, alpha=0.8)
    plt.scatter(self.df_test_ideal.x, self.df_test_ideal.y, color=self.df_test_ideal.color, alpha=0.2, label='Test points')
    plt.legend()
    plt.title('Test points vs Ideal functions (green for assigned, red for not assigned)')
    plt.show()