from pydantic import BaseModel

class AttendanceRequest(BaseModel):
    emp_id: str
    start_date: str
    end_date: str
