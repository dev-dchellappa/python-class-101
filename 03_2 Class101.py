# Now that we have done the modelling, lets start the Coding
# Lets write the Company module first. Refer Company.py
# Then let's import the Company module

import Company   
from abc import ABC, abstractmethod

class BankAccount:
    """Models Bank Account of Employee"""
    
    def __init__(self, acct_id, bank_id):
        self.acct_id = acct_id
        self.bank_id = bank_id

    def deposit(self, amount):
        print("Salary Credited in Acct", self.acct_id, 'at Bank', self.bank_id, ':', amount)
        # placeholder code to call Bank API and do a deposit   

class Employee(ABC):
    """Employee is a abstract superclass"""
    
    @abstractmethod
    def __init__(self, bank_acct, base_sal):
        self.bank_acct = bank_acct
        self.base_sal = base_sal
        self.emp_id = Company.generate_emp_id()
        Company.on_board_emp(self)

    # it is good practice to override the "==" operator for user defined data types
    # why?
    # say we add a few employess objects to a list
    # and we want to remove a particular object from list
    # we will use the command list.remove("item_to_remove")
    # the remove function will iterate thru the list and compare (do equality check) 
    # of items in the list with the item_to_remove
    # that's an great example of why we need to override the == operator for in a class
    def __eq__(self, other):
        return self.emp_id == other.emp_id

    def get_emp_id(self):
        return self.emp_id 

    def quit(self):
        Company.releive_emp(self)

    # why process_pay is defined as an abstract method?
    # though no action is implemented here, specifying  this as an abstract method in the parent class
    # enforces a constraint that every child call inheriting Employee MUST necessarily implement this function
    # needless to say, if there is any logicall action that is common for all employees,
    # we can implement it here, in which case it will not be abstract
    # an example could be: Tax deduction, when processing pay. that is common for all emps, so can ne implemented here.
    @abstractmethod
    def process_pay(self): pass 

    

class SalesPerson(Employee):
    """Sales Person Class, inherited from Employee. Sales Person 'is an' Employee"""
    def __init__(self, bank_acct, base_sal):
        super().__init__(bank_acct, base_sal)
        self.booking = 0 #initialize instance variable booking to 0

    def set_monthly_booking(self, booking):
        self.booking = booking

    def process_pay(self):
        print("processing pay for:", self.get_emp_id())
        pay = self.base_sal + (0.03 * self.booking)
        self.bank_acct.deposit(pay)
        return pay

class Consultant(Employee):
    """Sales Person Class, inherited from Employee. Consultant 'is an' Employee"""
    def __init__(self, bank_acct, base_sal):
        super().__init__(bank_acct, base_sal)
        self.revenue = 0

    def set_monthly_revenue(self, rev=0):
        self.revenue = rev

    def process_pay(self):
        print("processing pay for:", self.get_emp_id())
        pay = self.base_sal + (0.02 * self.revenue)
        self.bank_acct.deposit(pay)
        return pay


def test():
    # Create SalesPerson. BanAccount Object is passed on the fly to the constructor
    sp1 = SalesPerson(BankAccount("64781", "sbi_001"), 40000)
    
    sp2 = SalesPerson(BankAccount("12345", "sbi_087"), 45000)
    sp2.set_monthly_booking(80000)

    # Create Consultant
    c1 = Consultant(BankAccount("87436888", "icici_097"),50000)
    c2 = Consultant(BankAccount("236655361", "axis_865"),53000)
    c2.set_monthly_revenue(20000)

    Company.process_payroll()
    sp1.quit()
    # lets process the 2nd pay cycle
    sp1.set_monthly_booking(60000)
    sp2.set_monthly_booking(50000)
    c1.set_monthly_revenue(30000)
    c1.set_monthly_revenue(40000)
    Company.process_payroll()
#execute the test       
test()

## Can you see what is happening?
# even after sp1 has quit, we were able to set monthly booking for sp1
# this does not model real world behavior
# the reader can figure out how to improve the code to handle this scenario properly
# This is a great example of why it is important to test the code you write
# But thankfully, payroll is NOT processed for sp1 after sp1 quit - which is what we expect
# in this simplistic implementation
# Enjoy Coding!!








