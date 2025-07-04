from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

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

class DecisionMaker(BaseModel):
    name: str
    title: str

class CompanyProfile(BaseModel):
    # 🔹 Core Company Info
    Company: str
    Website: HttpUrl
    Industry: str
    Year_Founded: int
    Company_Type: str
    Street: str
    City: str
    State: str
    ZIP: int
    Company_Phone: str
    Company_Email: str

    # 📈 Business Metrics
    Revenue: str
    Employees_Count: int
    Growth_Rate: str
    Funding_Amount: str
    Valuation: str
    Tech_Stack: List[str]
    Traffic: str

    # 🧑‍💼 Key People
    CEO_Name: str
    CEO_Title: str
    CEO_LinkedIn: HttpUrl
    CEO_Email: str
    CEO_Phone: str
    Decision_Makers: List[DecisionMaker]

    # 🧪 Lead Qualification Signals
    Business_Model: str
    Customer_Segments: str
    Hiring_Activity: str
    Recent_Funding: str
    Job_Openings: int

    # 🛰️ Social & Web Presence
    Company_LinkedIn: HttpUrl
    Twitter: HttpUrl
    YouTube: HttpUrl
    Glassdoor_Rating: float
    BBB_Rating: str
    Customer_Reviews: str

    # Meta
    Source: str
    Confidence_Score: int