import random

def enrich_lead(lead):
    # Simulate enrichment with fake/random values
    return {
        "Company": lead["Company"],
        "Website": lead.get("Website", f"https://{lead['Company'].lower().replace(' ', '')}.com"),
        "Industry": lead.get("Industry", random.choice(["SaaS", "Healthcare", "E-commerce"])),
        "Product_Service_Category": random.choice(["CRM", "HR", "Marketing", "Payments"]),
        "Business_Type": random.choice(["B2B", "B2B2C"]),
        "Employees_Count": random.randint(10, 1000),
        "Revenue": f"${random.randint(1, 100)}M",
        "Year_Founded": random.choice([2008, 2012, 2016, 2020]),
        "BBB_Rating": lead.get("BBB_Rating", random.choice(["A+", "B", "NR"])),
        "Street": "123 Main St",
        "City": random.choice(["New York", "San Francisco", "Austin"]),
        "State": random.choice(["NY", "CA", "TX"]),
        "Company_Phone": lead.get("Phone", "123-456-7890"),
        "Company_LinkedIn": f"https://linkedin.com/company/{lead['Company'].lower().replace(' ', '')}",
        "Owner_First_Name": random.choice(["Alice", "Bob", "Carlos"]),
        "Owner_Last_Name": random.choice(["Smith", "Johnson", "Lee"]),
        "Owner_Title": "Founder & CEO",
        "Owner_LinkedIn": "https://linkedin.com/in/founder123",
        "Owner_Phone": "987-654-3210",
        "Owner_Email": f"ceo@{lead['Company'].lower().replace(' ', '')}.com",
        "Source": "MockSource (Growjo + Apollo)",
        "Confidence_Score": random.randint(80, 95)
    }
