from abc import ABC, abstractmethod

class Calculator(ABC):

    @abstractmethod
    def load_data(self, path: str):
        pass
    
    @abstractmethod
    def calculate_late_payment_interest(self, annual_anticipated_rate: float) -> float:
        pass

    @abstractmethod
    def calculate_overdue_rates(self, days: int):
        pass

    @abstractmethod
    def calculate_roi(self, amount: float, days: int, filepath: str = "") -> float:
        pass
    
    @abstractmethod
    def search_rate(self, amount: float, days: int):
        pass