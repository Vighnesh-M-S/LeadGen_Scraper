import random

def deep_search(lead):
    return {
        # 🔹 Core Company Info
        "Company": lead["Company"],
        "Website": lead.get("Website", f"https://{lead['Company'].lower().replace(' ', '')}.com"),
        "Industry": lead.get("Industry", random.choice(["SaaS", "Healthcare", "E-commerce"])),
        "Year_Founded": random.choice([2008, 2012, 2016, 2020]),
        "Company_Type": random.choice(["Private", "Public", "Subsidiary"]),
        "Street": "123 Main St",
        "City": random.choice(["New York", "San Francisco", "Austin"]),
        "State": random.choice(["NY", "CA", "TX"]),
        "ZIP": random.randint(10000, 99999),
        "Company_Phone": lead.get("Phone", "123-456-7890"),
        "Company_Email": f"info@{lead['Company'].lower().replace(' ', '')}.com",

        # 📈 Business Metrics
        "Revenue": f"${random.randint(1, 100)}M",
        "Employees_Count": random.randint(10, 1000),
        "Growth_Rate": f"{random.randint(5, 40)}%",
        "Funding_Amount": f"${random.randint(1, 300)}M",
        "Valuation": f"${random.randint(100, 3000)}M",
        "Tech_Stack": random.sample(["React", "Node.js", "PostgreSQL", "AWS", "Python", "Docker"], 3),
        "Traffic": f"{random.randint(50000, 1000000)} visitors/month",

        # 🧑‍💼 Key People
        "CEO_Name": f"{random.choice(['Alice', 'Bob', 'Carlos'])} {random.choice(['Smith', 'Johnson', 'Lee'])}",
        "CEO_Title": "Chief Executive Officer",
        "CEO_LinkedIn": "https://linkedin.com/in/founder123",
        "CEO_Email": f"ceo@{lead['Company'].lower().replace(' ', '')}.com",
        "CEO_Phone": "987-654-3210",
        "Decision_Makers": [
            {"name": "John Doe", "title": "CTO"},
            {"name": "Jane Roe", "title": "CMO"},
            {"name": "Dan Foo", "title": "VP Sales"},
        ],

        # 🧪 Lead Qualification Signals
        "Business_Model": random.choice(["B2B", "B2C", "SaaS", "Marketplace"]),
        "Customer_Segments": random.choice(["Enterprises", "SMBs", "Consumers"]),
        "Hiring_Activity": random.choice(["Hiring Engineers", "Hiring Sales Reps", "Stable"]),
        "Recent_Funding": f"Series {random.choice(['A', 'B', 'C'])} in {random.choice(['2023', '2024'])}",
        "Job_Openings": random.randint(1, 30),

        # 🛰️ Social & Web Presence
        "Company_LinkedIn": f"https://linkedin.com/company/{lead['Company'].lower().replace(' ', '')}",
        "Twitter": f"https://twitter.com/{lead['Company'].lower().replace(' ', '')}",
        "YouTube": f"https://youtube.com/{lead['Company'].lower().replace(' ', '')}",
        "Glassdoor_Rating": round(random.uniform(2.5, 4.9), 1),
        "BBB_Rating": lead.get("BBB_Rating", random.choice(["A+", "B", "NR"])),
        "Customer_Reviews": random.choice(["G2", "Capterra", "Trustpilot"]),

        # Other
        "Source": "MockSource (Growjo + Apollo)",
        "Confidence_Score": random.randint(80, 95)
    }