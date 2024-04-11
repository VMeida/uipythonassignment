import pytest

from UIAssignment import UIAssignment
    
if __name__ == "__main__":
  pytest.main(['./tests/TestBase.py'])
  UIA = UIAssignment(1)
  UIA.create_mysql_engine()
  UIA.load_all_data()
  UIA.get_best_function('y1')
  UIA.get_best_function('y2')
  UIA.get_best_function('y3')
  UIA.get_best_function('y4')
  UIA.plot_compare_ideal_and_test_before()
  UIA.calculate_test_points()
  UIA.plot_compare_ideal_and_test_after()
  