## Module to model a Company


_company_emp_id = 0 #flag to treat this as private, though it cannot be enforced
_company_emps = list()  #flag to treat this as private, though it cannot be enforced   

def generate_emp_id():
    global _company_emp_id 
    _company_emp_id += 1
    return _company_emp_id

def process_payroll():
    global _company_emps
    for emp in _company_emps:
        emp.process_pay()

def on_board_emp(emp):
    global _company_emps
    _company_emps.append(emp)

def releive_emp(emp):
    global _company_emps
    print("releving:", emp.get_emp_id())
    _company_emps.remove(emp)    