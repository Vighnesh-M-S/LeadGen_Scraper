import streamlit as st
import pandas as pd
import requests
import urllib.parse

# ---- CONFIG ----
st.set_page_config(page_title="Lead Selector", layout="wide")
API_URL = "http://localhost:8000/enrich"

# ---- HANDLE DIRECT URL ACCESS TO COMPANY PAGE ----
query_params = st.query_params
selected_company_name = query_params.get("company", None)

if selected_company_name:
    try:
        df_enriched = pd.read_csv("enriched_data.csv")
        selected_row = df_enriched[df_enriched["Company"] == selected_company_name]

        if not selected_row.empty:
            row = selected_row.iloc[0]
            st.markdown(f"# 🏢 {row['Company']} Profile")

            st.markdown("### 🯞 Basic Info")
            st.write(f"**Website**: [{row.get('Website', 'N/A')}]({row.get('Website', '#')})")
            st.write(f"**Industry**: {row.get('Industry', 'N/A')}")
            st.write(f"**Employees**: {row.get('Employees_Count', 'N/A')}")
            st.write(f"**Revenue**: {row.get('Revenue', 'N/A')}")
            st.write(f"**Founded**: {row.get('Year_Founded', 'N/A')}")

            st.markdown("### 👤 Owner Info")
            st.write(f"**Name**: {row.get('Owner_First_Name', '')} {row.get('Owner_Last_Name', '')}")
            st.write(f"**Title**: {row.get('Owner_Title', 'N/A')}")
            st.write(f"**Email**: {row.get('Owner_Email', 'N/A')}")
            st.write(f"**Phone**: {row.get('Owner_Phone', 'N/A')}")
            st.write(f"**LinkedIn**: {row.get('Owner_LinkedIn', 'N/A')}")

            st.markdown("---")
            st.markdown("[🔙 Back to Main Page](./)")
            st.stop()

    except FileNotFoundError:
        st.error("⚠️ Enriched data not found. Please enrich leads before viewing profiles.")
        st.stop()

# ---- NORMAL MAIN PAGE ----
st.title("🔍 Lead Enrichment Selector")
st.write("Upload your leads or add them manually, then select which ones to enrich.")

# Session: Manual leads
if "manual_leads" not in st.session_state:
    st.session_state.manual_leads = []

# File Upload
uploaded_file = st.file_uploader("📁 Upload Lead CSV", type=["csv"])
uploaded_df = pd.read_csv(uploaded_file) if uploaded_file else pd.DataFrame()

# Manual Form
with st.expander("📝 Add Lead Manually"):
    with st.form("manual_lead_form"):
        col1, col2 = st.columns(2)
        with col1:
            company = st.text_input("Company")
            industry = st.text_input("Industry")
            address = st.text_input("Address")
        with col2:
            rating = st.text_input("BBB Rating")
            phone = st.text_input("Phone")
            website = st.text_input("Website")
        submitted = st.form_submit_button("➕ Add Lead")
        if submitted:
            st.session_state.manual_leads.append({
                "Company": company,
                "Industry": industry,
                "Address": address,
                "BBB Rating": rating,
                "Phone": phone,
                "Website": website
            })
            st.success("✅ Lead added!")

# Combine data
manual_df = pd.DataFrame(st.session_state.manual_leads)
combined_df = pd.concat([uploaded_df, manual_df], ignore_index=True)

if not combined_df.empty:
    combined_df["Select"] = False
    edited_df = st.data_editor(
        combined_df,
        use_container_width=True,
        key="lead_editor",
        column_config={"Select": st.column_config.CheckboxColumn("✅ Enrich?", default=False)}
    )

    selected_leads = edited_df[edited_df["Select"] == True]
    st.markdown("---")
    st.subheader(f"Selected Leads for Enrichment: {len(selected_leads)}")
    st.dataframe(selected_leads.drop(columns=["Select"]), use_container_width=True)

    if not selected_leads.empty and st.button("🚀 Enrich Selected Leads"):
        with st.spinner("Enriching leads..."):
            try:
                response = requests.post(API_URL, json=selected_leads.to_dict(orient="records"))
                if response.status_code == 200:
                    df_enriched = pd.DataFrame(response.json())
                    st.session_state.df_enriched = df_enriched
                    df_enriched.to_csv("enriched_data.csv", index=False)
                    st.success("✅ Enrichment Complete")
                else:
                    st.error(f"❌ API returned {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"❌ Request failed: {e}")

# Show enriched table
if "df_enriched" in st.session_state:
    df_enriched = st.session_state.df_enriched
    st.subheader("📊 Enriched Lead Table (click company name)")

    all_columns = df_enriched.columns.tolist()
    table_html = """
    <style>
    .lead-table {width: 100%; border-collapse: collapse; margin-bottom: 2rem;}
    .lead-table th, .lead-table td {border: 1px solid #ccc; padding: 8px; text-align: left; font-size: 13px;}
    .hover-container {position: relative; display: inline-block; cursor: pointer;}
    .hover-container .hover-card {
        visibility: hidden; width: 280px; background-color: #f9f9f9; color: #333;
        text-align: left; border-radius: 10px; border: 1px solid #ccc; padding: 10px;
        position: absolute; z-index: 1; bottom: 125%; left: 50%; margin-left: -140px;
        box-shadow: 0px 8px 16px rgba(0,0,0,0.2); white-space: normal;
    }
    .hover-container:hover .hover-card {visibility: visible;}
    </style>
    <table class='lead-table'><thead><tr>
    """
    table_html += "".join([f"<th>{col}</th>" for col in all_columns])
    table_html += "</tr></thead><tbody>"

    for _, row in df_enriched.iterrows():
        table_html += "<tr>"
        for col in all_columns:
            cell_data = str(row.get(col, ""))
            if col == "Company":
                company_encoded = urllib.parse.quote_plus(cell_data)
                hover_card = f"""
                    <b>Industry:</b> {row.get('Industry', 'N/A')}<br>
                    <b>Revenue:</b> {row.get('Revenue', 'N/A')}<br>
                    <b>Employees:</b> {row.get('Employees_Count', 'N/A')}<br>
                    <b>Owner:</b> {row.get('Owner_First_Name', '')} {row.get('Owner_Last_Name', '')}<br>
                    <b>Email:</b> {row.get('Owner_Email', 'N/A')}
                """
                cell_html = f"""
                    <div class='hover-container'>
                        <a href='/?company={company_encoded}' target='_blank'>{cell_data} 🔗</a>
                        <div class='hover-card'>{hover_card}</div>
                    </div>
                """
            else:
                cell_html = cell_data
            table_html += f"<td>{cell_html}</td>"
        table_html += "</tr>"
    table_html += "</tbody></table>"

    st.markdown(table_html, unsafe_allow_html=True)

    st.download_button(
        "📥 Download Enriched Leads",
        df_enriched.to_csv(index=False),
        "enriched_leads.csv",
        "text/csv"
    )
