from pydantic import BaseModel, EmailStr
from datetime import date

# -------- EMPLOYEE --------
class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


# -------- LEAVE --------
class LeaveCreate(BaseModel):
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: str


class LeaveResponse(BaseModel):
    id: int
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: str
    status: str

    class Config:
        from_attributes = True
