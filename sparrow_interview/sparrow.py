
USER_ROLES = {
    "EMPLOYEE",
    "ORGANIZATION_ADMIN",
    "ORGANIZATION_ADMIN"
}

# User class
class User:
    def __init__(self, id, name, role):
        self.id = id
        self.name = name
        self.role = role

# name <String>

# date_of_birth <Date>

# work_email <String>

# is_exempt <Bool>

# specialist_notes <String>

role_mapping = {
    "EMPLOYEE": {
        "read": ['name', 'date_of_birth', 'work_email'],
        "write": ['name', 'date_of_birth', 'work_email']
    },
    "PRODUCT_SPECIALIST": {
        "read": ["work_email", "is_exempt"],
        "write": ['name', 'work_email', 'is_exempt']
    },
    "ORGANIZATION_ADMIN": {
        "read": ['name', 'date_of_birth', 'work_email', 'is_exempt', 'specialist_notes'],
        "write": ['name', 'date_of_birth', 'work_email', 'is_exempt', 'specialist_notes']
    }
}

# # Employee class
class Employee:
    def __init__(self, name, date_of_birth, work_email, is_exempt, specialist_notes):
        # TODO: Add validation on provided values
        self.name = name
        self.date_of_birth = date_of_birth
        self.work_email = work_email
        self.is_exempt = is_exempt
        self.specialist_notes = specialist_notes

    def get_allowed_fields(self, allowed_fields: list[str], name, date_of_birth, work_email, is_exempt, specialist_notes):
        response = {}
        if "name" in allowed_fields:
            response["name"] = self.name
        if "date_of_birth" in allowed_fields:
            response["date_of_birth"] = self.date_of_birth
        if "work_email" in allowed_fields:
            response["work_email"] = self.work_email
        if "is_exempt" in allowed_fields:
            response["is_exempt"] = self.is_exempt
        if "specialist_notes" in allowed_fields:
            response["specialist_notes"] = self.specialist_notes

        return response
        

    def read_values(self, requesting_user):
        allowed_fields = role_mapping[requesting_user.role]['read']
        return self.get_allowed_fields(allowed_fields, self.name, self.date_of_birth, self.work_email, self.is_exempt, self.specialist_notes)
    
    def write_values(self, requesting_user, values_to_change):
        allowed_fields = role_mapping[requesting_user.role]['write']
        for key, new_value in values_to_change.items():
            if key in allowed_fields:
                setattr(self, key, new_value)
                # self[key] = new_value

        return self.read_values(requesting_user)


class EmployeeDataResponse:
    def __init__(self, employee: Employee, messages: list[str]):
        self.employee = employee
        self.messages = messages

# Should implement read and write methods as well as constructor



def main():
    # Init some data
    requesting_user = User(1, "bob", "EMPLOYEE")
    product_specialist = User(2, "stacy", "PRODUCT_SPECIALIST")
    employee = Employee("John", "01/01/1900", "john@john.john", True, [])

    # Perform a read request
    # employee_data = employee.read_values(requesting_user)
    # print(employee_data)

    # perform a write request
    updated_employee = employee.write_values(requesting_user, {"name": "Josh", "work_email": "test"})
    print(updated_employee)

    # perform a write request (invalid field)
    updated_employee = employee.write_values(requesting_user, {"is_exempt": False})
    data = employee.read_values(product_specialist)
    print(data)

    # Perform a read request
    # employee_data = employee.read_values(requesting_user)
    # print(employee_data)

if __name__ == "__main__":
    main()