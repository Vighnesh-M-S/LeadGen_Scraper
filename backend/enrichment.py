import random
from bs4 import BeautifulSoup
import requests

def guess_website(company_name):
    try:
        query = f"{company_name} official site"
        url = f"https://duckduckgo.com/html/?q={requests.utils.quote(query)}"
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")
        results = soup.select("a.result__a")
        return results[0]['href'] if results else f"https://{company_name.lower().replace(' ', '')}.com"
    except:
        return f"https://{company_name.lower().replace(' ', '')}.com"
    
def scrape_bbb_rating(company):
    try:
        query = f"{company} site:bbb.org"
        url = f"https://duckduckgo.com/html/?q={requests.utils.quote(query)}"
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")
        links = soup.select("a.result__a")
        for link in links:
            if "bbb.org" in link["href"]:
                bbb_page = requests.get(link["href"], headers={"User-Agent": "Mozilla/5.0"})
                rating_soup = BeautifulSoup(bbb_page.text, "html.parser")
                rating = rating_soup.find(text=lambda x: x and "BBB Rating" in x)
                if rating:
                    return rating.strip()
        return "NR"
    except:
        return "NR"
    
def fetch_from_apollo(company_name):
    url = "https://api.apollo.io/v1/mixed_companies/search"
    headers = {
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "Api-Key": "YOUR_APOLLO_API_KEY"
    }

    payload = {
        "q_organization_name": company_name,
        "page": 1,
        "per_page": 1
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        companies = response.json().get("organizations", [])
        if companies:
            return companies[0]
    return None

def fetch_from_growjo(company_name):
    try:
        search_url = f"https://growjo.com/search?searchterm={company_name.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0"}
        html = requests.get(search_url, headers=headers).text
        soup = BeautifulSoup(html, "html.parser")

        # Find first company link
        link = soup.select_one("a[href^='/company/']")
        if not link:
            return None

        profile_url = "https://growjo.com" + link["href"]
        profile_html = requests.get(profile_url, headers=headers).text
        profile_soup = BeautifulSoup(profile_html, "html.parser")

        # Safe parsing with fallback
        employee_elem = profile_soup.select_one(".employee_estimate")
        growth_elem = profile_soup.select_one(".growth_score")
        founded_elem = profile_soup.find("td", string="Founded")

        data = {
            "Employee Count": employee_elem.text.strip() if employee_elem else None,
            "Growth Score": growth_elem.text.strip() if growth_elem else None,
            "Founded": (
                founded_elem.find_next_sibling("td").text.strip()
                if founded_elem and founded_elem.find_next_sibling("td")
                else None
            )
        }

        return data
    except Exception as e:
        print("Growjo error:", e)
        return None

def enrich_lead(lead):
    # Simulate enrichment with fake/random values
    company = lead["Company"]
    apollo_data = fetch_from_apollo(company) or {}
    growjo_data = fetch_from_growjo(company) or {}
    return {
        "Company": company,
        "Website": apollo_data.get("website_url", guess_website(company)),
        "Industry": apollo_data.get("industry", lead.get("Industry", "Unknown")),
        "Product_Service_Category": apollo_data.get("tags", ["CRM"])[0],
        "Business_Type": apollo_data.get("organization_type", "B2B"),
        "Employees_Count": apollo_data.get("estimated_num_employees", growjo_data.get("Employee Count", random.randint(10, 1000))),
        "Revenue": apollo_data.get("estimated_annual_revenue", "$20M"),
        "Year_Founded": apollo_data.get("founded_year", growjo_data.get("Founded", 2016)),
        "BBB_Rating": scrape_bbb_rating(company),
        "Street": apollo_data.get("street_address", "123 Main St"),
        "City": apollo_data.get("city", "San Francisco"),
        "State": apollo_data.get("state", "CA"),
        "Company_Phone": apollo_data.get("phone", lead.get("Phone", "123-456-7890")),
        "Company_LinkedIn": apollo_data.get("linkedin_url", f"https://linkedin.com/company/{company.lower().replace(' ', '')}"),
        "Owner_First_Name": "Alice",
        "Owner_Last_Name": "Smith",
        "Owner_Title": "CEO",
        "Owner_LinkedIn": "https://linkedin.com/in/founder123",
        "Owner_Phone": "987-654-3210",
        "Owner_Email": f"ceo@{company.lower().replace(' ', '')}.com",
        "Source": "Apollo + Growjo + Mock",
        "Confidence_Score": random.randint(80, 95)
    }