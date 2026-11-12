from src.database.stored_proc_repository import StoredProcRepository


class EmployeeRepository(StoredProcRepository):
    sp_entity = "Employee"           # usa sp_Insert_Employee, sp_GetAll_Employee, ...
    pk = "id_employee"
    insert_params = ["id_employee_position_fk", "id_employee_area_fk", "id_user_fk", "working_hours"]
    update_params = insert_params

    def find_by_user(self, id_user, conn=None):
        return self.find_one_by("id_user_fk", id_user, conn=conn)
