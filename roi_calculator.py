from os import system, name
import ascii

class Rental_Roi():

    def main_roi(self):
        while True:
            user_choice = input("Would you like to do a new ROI calculation or quit? ('new'/'quit'): ").lower()
            if "q" in user_choice:
                break
            else:
                self.clear()
                self.calc_income()
                self.do_expenses = 1
                while self.do_expenses:
                    self.calc_expenses()
                    self.calc_cash_flow()
                if self.negative_cashflow:
                    continue
                self.calc_upfront_inv()
                self.calc_roi()

    def calc_income(self):
        self.income_mo = self.positive_number_input(-1, "Enter total monthly income in numbers, without commas or other symbols,\nincluding rent and other income from this property: ")
        self.income_yr = self.income_mo * 12
        self.income_yr_str = self.simplify_and_comma(self.income_yr)

    def calc_expenses(self):
        user_choice = input("Would you like to enter itemized expenses data?(y/n)\n Say 'n' to enter the expenses grand total yourself: ").lower()
        if "n" in user_choice:
            self.did_manual_expenses = 0
            self.expenses_mo = self.positive_number_input(-1, "Enter total monthly expenses in numbers, without commas or other symbols: ")
        else:
            self.expenses_mo = self.calc_expenses_manual()
        self.expenses_yr = self.expenses_mo * 12
        self.expenses_yr_str = self.simplify_and_comma(self.expenses_yr)
    
    def calc_expenses_manual(self):
        self.did_manual_expenses = 1
        self.mortgage = self.positive_number_input(-1, "Enter monthly mortgage, without commas or other symbols (enter 0 if none): ")
        self.tax_and_insurance = self.positive_number_input(-1, "Enter monthly taxes and insurance in numbers, without commas or other symbols.\nIf already included in mortgage, enter 0: ")
        self.utilities = self.positive_number_input(-1, "Enter monthly utilities cost in numbers, without commas or other symbols.\nIf tenant pays all utilities, enter 0: ")
        self.hoa = self.positive_number_input(-1,"Enter monthly HOA fee in numbers, without commas or other symbols.\nIf tenant pays for HOA or there is no HOA, enter 0: ")
        self.repairs_and_capex = self.positive_number_input(-1, "Enter monthly repairs and capital expenditures in numbers, without commas or other symbols (enter 0 if none): ")
        self.other_costs = self.positive_number_input(-1, "Enter any additional monthly costs not accounted for above (enter 0 if none): ")
        return(self.mortgage+self.tax_and_insurance+self.utilities+self.hoa+self.repairs_and_capex+self.other_costs)

    def calc_cash_flow(self):
        self.cash_flow_mo = self.income_mo - self.expenses_mo
        self.cash_flow_yr = self.cash_flow_mo * 12
        self.cash_flow_yr_str = self.simplify_and_comma(self.cash_flow_yr)
        if self.cash_flow_yr < 0:
            print("Your expenses exceed your income. This will result in a negative ROI.\nIf your inputs were correct, you will only lose money with this investment.\nHere's what you entered so far:")
            print("Total income (yr): $", self.income_yr_str)
            print("Total expenses(yr): $", self.expenses_yr_str)
            if self.did_manual_expenses == 1:
                print("  Mortgage (yr): $",self.simplify_and_comma(self.mortgage*12))
                print("  Tax and Insurance (yr): $",self.simplify_and_comma(self.tax_and_insurance*12))
                print("  Utilities (yr): $",self.simplify_and_comma(self.utilities*12))
                print("  HOA (yr): $",self.simplify_and_comma(self.hoa*12))
                print("  Repairs and Capital Expenditures (yr): $",self.simplify_and_comma(self.repairs_and_capex*12))
                print("  Other Costs (yr): $",self.simplify_and_comma(self.other_costs*12))
            print("Cash flow: $,", self.cash_flow_yr_str)
            user_choice = input("Press 'y' to re-enter expenses, or 'n' to start over from the beginning: ")
            self.do_expenses = 1 if "y" in user_choice else 0
            self.negative_cashflow = 1
        else:
            self.do_expenses = 0
            self.negative_cashflow = 0

    def calc_upfront_inv(self):
        self.purchase_price = -1
        self.purchase_price = self.positive_number_input(self.purchase_price, "Enter purchase price: ")
        self.down_payment = -1
        while self.down_payment < 0 or self.down_payment > 100:
            try:
                self.down_payment = float(input("Enter percent down as a number between 0 and 100 (e.g., 15% = 15): %"))
                if self.down_payment < 0 or self.down_payment > 100:
                    print(self.invalid_entry_message())
            except:
                print(self.invalid_entry_message())
        self.ancillary_up_front_costs = -1
        self.ancillary_up_front_costs = self.positive_number_input(self.ancillary_up_front_costs, "Enter total additional up front costs\n(e.g., closing costs, rehab, other): ")
        self.upfront_inv = (self.purchase_price * (self.down_payment/100)) + self.ancillary_up_front_costs
        self.upfront_inv_str = self.simplify_and_comma(self.upfront_inv)

    def calc_roi(self):
        self.roi = round((self.cash_flow_yr/self.upfront_inv)*100, 1)
        if self.roi > 39:
            print("The numbers you've entered suggest a return on investment that is uncommonly high.\nYou might have mis-entered one or more values.\nHere's what you entered and the resulting ROI:")
            self.raw_print_results()
        else:
        # these padding checks are to make alignment in the house art work out
            roi_box_pad = "     " if len(str(self.roi)) == 3 else "    "
            income_yr_pad = " "*(18-len(self.income_yr_str))
            expenses_yr_pad = " "*(18-len(self.expenses_yr_str))
            cash_flow_yr_pad = " "*(18-len(self.cash_flow_yr_str))
            upfront_inv_pad = " "*(18-len(self.upfront_inv_str))
            print(ascii.house_art.format(self.roi, roi_box_pad,
                                        self.income_yr_str, income_yr_pad,
                                        self.expenses_yr_str, expenses_yr_pad,
                                        self.cash_flow_yr_str, cash_flow_yr_pad,
                                        self.upfront_inv_str, upfront_inv_pad))

    def simplify_and_comma(self, num_to_format):
        # this method rounds the input to 0 places, turns it to int, and adds comma separators
        # this is all solely for nicely displaying info to user. used for all non proportion
        # dollar inputs
        num_to_format = int(round(num_to_format,0))
        num_to_format = f"{num_to_format:,}"
        return(num_to_format)

    def positive_number_input(self, num_to_check, input_message):
        # this is a generic input validator for user input that is supposed
        # to be a non-negative number. Forces a loop until the user puts
        # in something valid.
        while num_to_check < 0:
            try:
                num_to_check = float(input(input_message))
                if num_to_check < 0:
                    print(self.invalid_entry_message())
            except:
                print(self.invalid_entry_message())
        
        return(num_to_check)

    def invalid_entry_message(self):
        return("Sorry, that's not a valid entry, please try again.")

    def raw_print_results(self):
        # these results get printed if the calculator comes up with an unreasonable
        # ROI result, skipping the house art.
        print("Total income (yr): $",self.income_yr_str)
        print("Total expenses (yr): $", self.expenses_yr_str)
        print("Cash flow (yr): $", self.cash_flow_yr_str)
        print("Upfront investment: $", self.upfront_inv_str)
        print("-----------")
        print("Resulting ROI: ",self.roi,"%")

    def clear(self):
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')
