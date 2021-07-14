## Understanding OOPs concepts and its immplementation in Python
## this is NOT Production grade code
## It is intentionally a Python101 level code to illusrate concepts


## Step 1: Lets start with what we want to acheive: the Problem Domain

# I want to model employee life cycle in a company
    # employee joins the company
    # employee provides their Bank acct details into which salary must be credited
    # company has 2 kinds of employees - Sales and Consulting
    # for Sales, salary structure is: Base + 3% of monthly bookings made by the sales person
    # for Consulting, salary is: Base + 2% of revenue booked by the consultant.
    # at the end of month, company has to do a batch process of payroll for all employess
    # employee can quits the company
    # after employee quite, payroll process must EXCLUDE the employee (let's keep it simple here)

## Step 2: Now that we have articulated the problem, we'll swithc to the Solution Domain

## Start with identifying entities in the Problem Domain
# what are the 'things' we encounter in the Problem Domain?
    # Entity #1: Employee
    # Enity #2: SalesPerson "is an" Employee
    # Entity #3: Consultant "is an" Employee
    # all employess "have a" Bank Account
    # Entity #4 Bank Account 
    # Company "has a" collection of employees

## then think about behavior (what do these things 'do' that's relevant to the Problem doimain.)
    # employee "joins" the company
    # employee "leaves" the company
    # Company must "process payroll" for all active employess
    # when payroll is processeed, salary must "credited" to the Bank Acct of each active emp
    # SalesPerson "generates" Booking
    # Consultant "generates" revenue


## Step 3: Now lets do the conceptual / logical modelling of the Solution Domain
# In this step we identify members of Entities - 
# both attributes which hold state, and methods which model behaviour

#Employee Entity
    # emp_id employee has an emp_id
    # bank_acct # has a bank account
    # base_pay # has a base pay
    # quit() # and can quit
    # what about joining? e.g join()
    # well, when emp is created, we can implement the onboarding process in the constructor

# SalesPerson is an Employee
    #  set_monthly_booking()     
    #  process_pay() # here we will implement sales person pay rules
# Consultant is an Employee
    # set_monthly_revenue()
    # process pay () >> implement consultant pay rules

## we need some helper functions: 
    # generate emp id: in real world, emp_numbers will be auto generated, so lets model this.
    # we do not want to pass emp id as parameter when creating a employee object
    # Because Emp ID's are typically maintained at Company level
    # so we need to model a Company
    # How do we do that?
    # Option 1 - create a class. 
        # Hmm...bad idea. As that will allow creating multiple instances of 
        # Company. That is not how things work in the real world - where only 1 instance of company exists
        # in other languages, we have the concept of a Singleton which ensure only 1 instance of a class
        # can be created.  
        # But here, we are doing a Level-101 implementaion, so lets not bother with Singletons
    # So..to keep things simple, lets implement the Company entity as a Module

# Company Module:
    # Company will generate emp ID
    # maintain a Collection of all employees (models the company's emp database)
         # Here, we will implement the Collection using the list data structure   
    # Company will onboard and employee: when emp is created, emp must be added to the list
    # when emp quits, Company will releive the employee. the emp must be removed from the list
    # And, most importantly, company will process pay roll.

#####################################################################################
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

#let's define Employee as an abstract class to model the real world reality
# Why abstract? 
# It's because in this company there are only 2 kinds of "real" employees
# Sales Person and Consultant
# every employee is either a Sales Person or Consultant
# e.g. if the comapny wants to increase Head Count by 5 people, and says "let's hire 5 employees"
# that is a meaningful statement, but cannot be acted upon
# to actually execute this, we need to ask one more question:
# "when you say 5 emps, how many are Sales Persons and how many are Consultants"
# You never find positions being opened for "we are hiring employee!!" - too abstract!!
# whereas "we are hiring Sales Persons", "we are hiring Consultants" - now that makes sense
# Which is why, even when we write code, it is good to model the entity "employee" as a abstract class

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
# # even after sp1 has quit, we were able to set monthly booking for sp1
# this does not model real world behavior
# the reader can figure out how to improve the code to handle this scenario properly
# This is a great example of why it is important to test the code you write
# But thankfully, payroll is NOT processed for sp1 after sp1 quit - which is what we expect
# in this simplistic implementation
# Enjoy Coding!!








