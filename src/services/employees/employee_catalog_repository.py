from src.database.stored_proc_repository import StoredProcRepository


class EmployeeAreaRepository(StoredProcRepository):
    sp_entity = "Employee_Area"      # sp_*_Employee_Area
    pk = "id_employee_area"
    insert_params = ["name_employee_area", "place_employee_area"]
    update_params = ["name_employee_area", "place_employee_area"]


class EmployeePositionRepository(StoredProcRepository):
    sp_entity = "Employee_Position"  # sp_*_Employee_Position
    pk = "id_employee_position"
    insert_params = ["name_employee_position"]
    update_params = ["name_employee_position"]
