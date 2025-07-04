from fastapi import FastAPI
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

from .enrichment import enrich_lead
from .models import LeadInput, LeadEnriched, DecisionMaker, CompanyProfile
from .page import deep_search

app = FastAPI()

# CORS setup so Streamlit frontend can call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Lead Enrichment API is running"}

@app.post("/enrich", response_model=List[LeadEnriched])
def enrich_leads(leads: List[LeadInput]):
    enriched = [enrich_lead(lead.dict()) for lead in leads]
    return enriched

@app.get("/company", response_model=CompanyProfile)
def get_company_profile(name: str):
    lead = {"Company": name}
    detail = deep_search(lead)
    return detail
