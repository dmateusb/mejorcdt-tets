import pandas as pd
import sys
from typing import Text
from scripts.interface.calculator import Calculator


class ProfitabilityCalculator(Calculator):
    
    columns_labels = {
        "consecutivo": "Consecutivo",
        "fecha": "Fecha",
        "minmonto": "Monto mínimo",
        "maxmonto": "Monto máximo",
        "minplazo": "Plazo mínimo",
        "maxplazo": "Plazo máximo",
        "tasa": "Tasa",
        "banco": "Banco",
    }
    
    def __init__(self):
        """
        Initialize the ProfitabilityCalculator and load data.
        """
        self.data = self.load_data()
        
    def load_data(self, path="data/raw/rates.csv"):
        """
        Load data from a CSV file.

        :param path: Path to the CSV file.
        :return: DataFrame containing the loaded data.
        """
        data = pd.read_csv(path, sep=";")
        
        if set(data.columns) != set(self.columns_labels.keys()):
            print("El archivo no tiene las columnas correctas, favor ingresar " \
                f"un archivo con las siguientes columnas: {', '.join(list(self.columns_labels))}\n")
            sys.exit(1)
        
        data["minmonto"] = data["minmonto"].str.replace(".", "").astype(float)
        data["maxmonto"] = data["maxmonto"].str.replace(".", "").astype(float)
        return data
            
    def get_rates_in_period(self, data: pd.DataFrame, days: int) -> pd.DataFrame:
        """
        Filter rates based on the specified period.

        :param data: DataFrame containing the data.
        :param days: Number of days for the period.
        :return: DataFrame containing the filtered rates.
        """
        return data[(data["minplazo"] <= days) & (data["maxplazo"] >= days)].copy()
            
    def get_rates_in_amount(self, data: pd.DataFrame, amount: float) -> pd.DataFrame:
        """
        Filter rates based on the specified amount.

        :param data: DataFrame containing the data.
        :param amount: Amount to filter the rates.
        :return: DataFrame containing the filtered rates.
        """
        return data[(data["minmonto"] <= amount) & (data["maxmonto"] >= amount)].copy()
    
    def calculate_late_payment_interest(self, annual_anticipated_rate: float) -> float:
        """
        Calculate the late payment interest based on the annual anticipated rate.

        :param annual_anticipated_rate: Annual anticipated rate.
        :return: Late payment interest.
        """
        daily_anticipated_rate = annual_anticipated_rate / 365
        return 1 / ( 1 -  daily_anticipated_rate)

    def calculate_return_on_rate(self, rate: float, amount:float, days: int) -> float:
        """
        Calculate the return on rate for the specified rate, amount, and period.

        :param rate: Rate to use for the calculation.
        :param amount: Amount to invest.
        :param days: Number of days for the investment.
        :return: Return on rate calculated.
        """      
        return amount * (rate * days / 360)

    def calculate_effective_rate(self, rate: float, amount:float, days: int) -> float:
        """
        Calculate the effective rate for the specified rate, amount, and period.

        :param rate: Rate to use for the calculation.
        :param amount: Amount to invest.
        :param days: Number of days for the investment.
        :return: Effective rate calculated.
        """
        return self.calculate_return_on_rate(rate, amount, days) / amount
    
    def format_response(self, df: pd.DataFrame) -> str:
        """
        Format the response DataFrame to a string.

        :param data: DataFrame to format.
        :return: String representation of the DataFrame.
        """
        right_columns_df = df.drop(columns=["fecha", "consecutivo"])

        right_columns_df["maxmonto"] = right_columns_df["maxmonto"].apply(
            lambda x: "${:,.2f}".format(x))

        right_columns_df["minmonto"] = right_columns_df["minmonto"].apply(
            lambda x: "${:,.2f}".format(x))

        right_columns_df = right_columns_df.rename(columns=self.columns_labels)
        return right_columns_df.to_string(index=False)

    def calculate_overdue_rates(self, days: int) -> str:
        """
        Calculate the overdue rates for the specified period.

        :param days: Number of days for the period.
        :return: DataFrame containing the overdue rates.
        """
        rates_in_period = self.get_rates_in_period(self.data, days)

        if rates_in_period.empty:
            return "No se encontraron tasas vencidas para el periodo ingresado"

        rates_in_period.loc[:, "Tasa Vencida"] = rates_in_period["tasa"].apply(
            lambda x: self.calculate_late_payment_interest(x))
        
        return self.format_response(rates_in_period)
    
    def calculate_roi(self, amount: float, days: int, filepath: Text = "") -> float:
        """
        Calculate the return on investment (ROI) for the specified amount and period.

        :param amount: Amount to invest.
        :param days: Number of days for the investment.
        :param filepath: Optional path to a CSV file to load data from.
        :return: ROI calculated.
        """
        if filepath != "":
            self.data = self.load_data(filepath)
            
        rates_in_period = self.get_rates_in_period(self.data, days)
        rates_in_amount = self.get_rates_in_amount(rates_in_period, amount)
        
        if rates_in_amount.empty:
            return "No se encontraron tasas para el monto ingresado"

        rates_in_amount.loc[:, "ROI"] = rates_in_amount["tasa"].apply(
            lambda rate: self.calculate_effective_rate(rate, amount, days))        
        
        return self.format_response(rates_in_amount)
        
    
    def search_rate(self, amount: float, days: int, filepath: Text = "") -> float:
        """
        Search and return the rates for the specified amount and period.

        :param amount: Amount to invest.
        :param days: Number of days for the investment.
        :return: String representation of the rates found.
        """
        if filepath != "":
            self.data = self.load_data(filepath)
            
        rates_in_period = self.get_rates_in_period(self.data, days)
        rates_in_amount = self.get_rates_in_amount(rates_in_period, amount)
        rates_in_amount.loc[:, "Tasa Efectiva Anual"] = rates_in_amount["tasa"].apply(
            lambda rate: self.calculate_effective_rate(rate, amount, days))
        
        return self.format_response(rates_in_amount)
    