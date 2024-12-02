import unittest
from unittest.mock import MagicMock, patch
from scripts.assistant import Assistant
from scripts.interface.calculator import Calculator

class TestAssistant(unittest.TestCase):

    def setUp(self):
        self.mock_calculator = MagicMock(spec=Calculator)
        self.assistant = Assistant(self.mock_calculator) 
        
    @patch('builtins.print')
    def test_answer_not_found(self, mock_print):
        self.assistant.answer_not_found()
        mock_print.assert_called_once_with("Opción no encontrada\n")

    def test_call_option_valid(self):
        self.assistant.selected_option = 0
        self.assistant.options["Tasa vencida"] = MagicMock()
        self.assistant.call_option()
        self.assistant.options["Tasa vencida"].assert_called_once()
    
    def test_call_option_invalid(self):
        mock_answer_not_found = MagicMock()
        self.assistant.answer_not_found = mock_answer_not_found
        self.assistant.selected_option = 99
        self.assistant.call_option()
        mock_answer_not_found.assert_called_once()

    def test_calculate_overdue_rate(self):
        self.assistant.days = 30
        self.assistant.calculate_overdue_rate()
        self.mock_calculator.calculate_overdue_rates.assert_called_once_with(30)

    def test_calculate_roi(self):
        self.assistant.amount_to_invest = 1000
        self.assistant.days = 30
        self.assistant.calculate_roi()
        self.mock_calculator.calculate_roi.assert_called_once_with(1000, 30)

    def test_search_rate(self):
        self.assistant.amount_to_invest = 1000
        self.assistant.days = 30
        self.assistant.search_rate()
        self.mock_calculator.search_rate.assert_called_once_with(1000, 30)

    def test_ask_days_valid(self):
        with unittest.mock.patch('builtins.input', return_value='30'):
            self.assistant.ask_days()
            self.assertEqual(self.assistant.days, 30)

    def test_ask_days_invalid(self):
        with unittest.mock.patch('builtins.input', side_effect=['invalid', '30']):
            self.assistant.ask_days()
            self.assertEqual(self.assistant.days, 30)

    def test_ask_amount_valid(self):
        with unittest.mock.patch('builtins.input', return_value='1000'):
            self.assistant.ask_amount_to_invest()
            self.assertEqual(self.assistant.amount_to_invest, 1000)

    def test_ask_amount_invalid(self):
        with unittest.mock.patch('builtins.input', side_effect=['invalid', '1000']):
            self.assistant.ask_amount_to_invest()
            self.assertEqual(self.assistant.amount_to_invest, 1000)

    @patch('builtins.print')
    def test_display_options(self, mock_print: MagicMock):
        self.assistant.ask_option = MagicMock()
        self.assistant.display_options()
        mock_print.assert_called_with("3. Buscar tasas")

    def test_ask_option_valid(self):
        with unittest.mock.patch('builtins.input', return_value='1'):
            self.assistant.ask_option()
            self.assertEqual(self.assistant.selected_option, 0)

    def test_ask_option_invalid(self):
        with unittest.mock.patch('builtins.input', side_effect=['invalid', '1']):
            self.assistant.ask_option()
            self.assertEqual(self.assistant.selected_option, 0)

    def test_process(self):
        self.assistant.display_options = MagicMock()
        self.assistant.call_option = MagicMock()
        self.assistant.process()
        self.assistant.display_options.assert_called_once()
        self.assistant.call_option.assert_called_once()

if __name__ == "__main__":
    unittest.main()