import unittest
import sys

sys.path.append('../Functions/')

from group01 import Group01

class TestGroup01(unittest.TestCase):
    
    def setUp(self):
        self.my_object = Group01("my_object")
    
    def test_get_data(self):
        self.assertIsNone(self.my_object.get_data())

    def test_get_countries(self):
        self.assertRaises(TypeError, self.my_object.get_countries, 123)
        
        # Add more test cases

    def test_plot_quantity(self):
        self.assertIsNone(self.my_object.plot_quantity())
        self.assertRaises(TypeError, self.my_object.plot_quantity, 123)
        
        # Add more test cases

    def plot_area_chart(self):
        self.assertIsNone(self.my_object.plot_area_chart("World"))
        self.assertRaises(TypeError, self.my_object.plot_area_chart, 123)
        self.assertRaises(ValueError, self.my_object.plot_area_chart, "Non-existent country")
        
        # Add more test cases
        
    def test_plot_country_chart(self):
        self.assertIsNone(self.my_object.plot_country_chart("United States"))
        self.assertRaises(TypeError, self.my_object.plot_country_chart, 123)
        self.assertRaises(ValueError, self.my_object.plot_country_chart, "Non-existent country")
        
        # Add more test cases
        
    def test_gapminder(self):
        self.assertIsNone(self.my_object.gapminder(2000))
        self.assertRaises(TypeError, self.my_object.gapminder, -1)
        self.assertRaises(ValueError, self.my_object.gapminder, 3000)
        
        # Add more test cases
        
if __name__ == '__main__':
    unittest.main()
