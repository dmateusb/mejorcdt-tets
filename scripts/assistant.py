from scripts.interface.calculator import Calculator


class Assistant:
    
    def __init__(self, calculator: Calculator) -> None:
        """
        Initialize the Assistant with a Calculator instance.

        :param calculator: An instance of the Calculator class.
        """
        self.calculator = calculator
        self.options = {
            "Tasa vencida": self.calculate_overdue_rate,
            "ROI": self.calculate_roi,
            "Buscar tasas": self.search_rate,
        }
        self.selected_option = None
        self.amount_to_invest = None
        self.days = None
                
    def answer_not_found(self):
        """
        Print a message indicating that the selected option was not found.
        """
        print("Opción no encontrada\n")
    
    def call_option(self):
        """
        Call the method corresponding to the selected option.

        :return: The result of the called method or the answer_not_found method.
        """
        if self.selected_option >= len(self.options):
            return self.answer_not_found()
        
        key = list(self.options)[self.selected_option]
        return self.options.get(key, self.answer_not_found)()

    def calculate_overdue_rate(self):
        """
        Calculate and print the overdue rate for the specified number of days.
        """
        print("Calculando tasa vencida...\n")
        self.ask_days()
        overdue_rates = self.calculator.calculate_overdue_rates(self.days)
        print(f"Tasa vencida a {self.days} días:\n\n{overdue_rates}")
        
    def calculate_roi(self):  
        """
        Calculate and print the return on investment (ROI) for the specified amount and period.
        """
        self.ask_amount_to_invest()
        self.ask_days()
        roi = self.calculator.calculate_roi(self.amount_to_invest, self.days)
        print(f"Tu ROI con una inversión de ${self.amount_to_invest} a "\
            f"{self.days} días es de \n\n{roi}\n")

    def search_rate(self):
        """
        Calculate and print the return on investment (ROI) for the specified amount and period.
        """
        self.ask_amount_to_invest()
        self.ask_days()
        effective_rate_rentability = self.calculator.search_rate(self.amount_to_invest, self.days)
        print(f"Las tasas para una inversión de ${self.amount_to_invest} a "\
            f"{self.days} días son:\n\n{effective_rate_rentability}\n")
        
    def ask_option(self):
        """
        Prompt the user to enter the number of days for the calculation.
        """
        option = None
        while option is None:
            try:
                option = int(input("Opción: "))        
                if option not in range(1, len(self.options) + 1):
                    print(f"Opción inválida, ingrese un número entre 1 y {len(self.options)}\n")
                    option = None
                    
            except ValueError:
                print("Opción inválida, ingrese un número\n")
                option = None
        
        self.selected_option = option - 1
        
    def display_options(self):
        """
        Prompt the user to enter the amount to invest.
        """
        print("¿Que deseas calcular?\n")
        
        for i, option in enumerate(self.options):
            print(f"{i + 1}. {option}")
        
        self.ask_option()

    def ask_amount_to_invest(self):
        """
        Prompt the user to enter the amoung to invest for the calculation.
        """
        while (self.amount_to_invest is None):
            try:
                self.amount_to_invest = float(input("¿Cuánto deseas invertir?\n"))
                if self.amount_to_invest <= 0:
                    print("Cantidad inválida, favor ingrese un valor mayor a 0\n")
                    self.amount_to_invest = None
            except ValueError:
                print("Cantidad inválida, favor ingrese un valor numérico\n")
                
    def ask_days(self):
        """
        Prompt the user to enter the number of days for the calculation
        """
        while self.days is None:
            try:
                self.days = int(input("¿A cuántos días deseas calcular la tasa vencida?\n"))
                if self.days <= 0:
                    print("Días inválidos, favor ingrese un valor mayor a 0\n")
                    self.days = None
                    
            except ValueError:
                print("Días inválidos, favor ingrese un valor numérico\n")
                self.days = None
            
    def process(self):
        """
        Process the assistant.
        """
        print("¡Bienvenido a Mejor CDT!\n")
        self.display_options()
        self.call_option()