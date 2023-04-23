import unittest
from roi_calculator import Rental_Roi

class Test_Roi(unittest.TestCase):

    def test_negative_cash_flow_(self):
        test_roi = Rental_Roi()
        test_roi.income_mo = 2000
        test_roi.expenses_mo = 3000
        test_roi.income_yr = test_roi.income_mo*12
        test_roi.expenses_yr = test_roi.expenses_mo*12
        test_roi.income_yr_str = test_roi.simplify_and_comma(test_roi.income_yr)
        test_roi.expenses_yr_str = test_roi.simplify_and_comma(test_roi.expenses_yr)
        test_roi.did_manual_expenses = 0
        test_roi.calc_cash_flow()
        self.assertEqual(test_roi.negative_cashflow, 1)
    
    def test_large_num_to_string_formatting(self):
        num_to_test = 582039485
        test_roi = Rental_Roi()
        self.assertEqual(test_roi.simplify_and_comma(num_to_test),"582,039,485")
    
    def test_decimal_to_string_formatting(self):
        num_to_test = 4038.88
        test_roi = Rental_Roi()
        self.assertEqual(test_roi.simplify_and_comma(num_to_test), "4,039")


if __name__ == '__main__':
    unittest.main()

