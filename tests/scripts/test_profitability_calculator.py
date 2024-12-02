import unittest
import pandas as pd
from scripts.profitability_calculator import ProfitabilityCalculator

class TestProfitabilityCalculator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        data = {
            "consecutivo": [1, 2],
            "fecha": ["2023-01-01", "2023-01-02"],
            "minmonto": ["1000", "2000"],
            "maxmonto": ["5000", "10000"],
            "minplazo": [30, 60],
            "maxplazo": [60, 90],
            "tasa": [0.05, 0.10],
            "banco": ["Bank A", "Bank B"]
        }
        cls.sample_data = pd.DataFrame(data)
        cls.sample_data["minmonto"] = cls.sample_data["minmonto"].str.replace(".", "").astype(float)
        cls.sample_data["maxmonto"] = cls.sample_data["maxmonto"].str.replace(".", "").astype(float)
        cls.calculator = ProfitabilityCalculator()
        cls.calculator.data = cls.sample_data

    def test_load_data(self):
        self.assertEqual(set(self.calculator.data.columns), set(self.calculator.columns_labels.keys()))

    def test_get_rates_in_period(self):
        result = self.calculator.get_rates_in_period(self.calculator.data, 45)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["consecutivo"], 1)

        result = self.calculator.get_rates_in_period(self.calculator.data, 75)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["consecutivo"], 2)

    def test_get_rates_in_amount(self):
        result = self.calculator.get_rates_in_amount(self.calculator.data, 3000)
        self.assertEqual(len(result), 2)
        self.assertEqual(result.iloc[0]["consecutivo"], 1)

        result = self.calculator.get_rates_in_amount(self.calculator.data, 7000)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["consecutivo"], 2)

    def test_calculate_late_payment_interest(self):
        result = self.calculator.calculate_late_payment_interest(0.10)
        self.assertAlmostEqual(result, 1 / (1 - (0.10 / 365)))

        result = self.calculator.calculate_late_payment_interest(0.05)
        self.assertAlmostEqual(result, 1 / (1 - (0.05 / 365)))

    def test_calculate_overdue_rates(self):
        result = self.calculator.calculate_overdue_rates(45)
        self.assertIn("Tasa Vencida", result)

        result = self.calculator.calculate_overdue_rates(75)
        self.assertIn("Tasa Vencida", result)

    def test_calculate_roi(self):
        pass

if __name__ == "__main__":
    unittest.main()