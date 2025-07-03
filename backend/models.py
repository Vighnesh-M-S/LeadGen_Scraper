from pydantic import BaseModel, Field
from typing import Optional

class LeadInput(BaseModel):
    Company: str
    Website: Optional[str] = None
    Industry: Optional[str] = None
    Address: Optional[str] = None
    BBB_Rating: Optional[str] = Field(None, alias="BBB Rating")
    Phone: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        allow_population_by_alias = True

class LeadEnriched(BaseModel):
    Company: str
    Website: Optional[str]
    Industry: Optional[str]
    Product_Service_Category: Optional[str]
    Business_Type: Optional[str]
    Employees_Count: Optional[int]
    Revenue: Optional[str]
    Year_Founded: Optional[int]
    BBB_Rating: Optional[str]
    Street: Optional[str]
    City: Optional[str]
    State: Optional[str]
    Company_Phone: Optional[str]
    Company_LinkedIn: Optional[str]
    Owner_First_Name: Optional[str]
    Owner_Last_Name: Optional[str]
    Owner_Title: Optional[str]
    Owner_LinkedIn: Optional[str]
    Owner_Phone: Optional[str]
    Owner_Email: Optional[str]
    Source: Optional[str]
    Confidence_Score: Optional[int]