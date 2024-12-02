from scripts.assistant import Assistant
from scripts.profitability_calculator import ProfitabilityCalculator

if __name__ == '__main__':
    calculator = ProfitabilityCalculator()
    Assistant(calculator).process()