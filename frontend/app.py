import streamlit as st
import pandas as pd
import requests

API_URL = "http://localhost:8000/enrich"

st.set_page_config(page_title="Lead Selector", layout="wide")

st.title("🔍 Lead Enrichment Selector")
st.write("Upload your leads or add them manually, then select which ones to enrich.")

# Session storage for manual entries
if "manual_leads" not in st.session_state:
    st.session_state["manual_leads"] = []

# 1. Upload CSV
uploaded_file = st.file_uploader("📁 Upload Lead CSV", type=["csv"])
uploaded_df = pd.DataFrame()

if uploaded_file:
    uploaded_df = pd.read_csv(uploaded_file)

# 2. Manual Input Section
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
            new_lead = {
                "Company": company,
                "Industry": industry,
                "Address": address,
                "BBB Rating": rating,
                "Phone": phone,
                "Website": website
            }
            st.session_state["manual_leads"].append(new_lead)
            st.success("Lead added!")

# Combine uploaded and manual leads
manual_df = pd.DataFrame(st.session_state["manual_leads"])
combined_df = pd.concat([uploaded_df, manual_df], ignore_index=True)

# 3. Display combined table with checkbox
if not combined_df.empty:
    combined_df["Select"] = False
    edited_df = st.data_editor(
        combined_df,
        use_container_width=True,
        key="lead_editor",
        column_config={
            "Select": st.column_config.CheckboxColumn("✅ Enrich?", default=False)
        }
    )

    # 4. Filter selected rows
    selected_leads = edited_df[edited_df["Select"] == True]

    st.markdown("---")
    st.subheader(f"Selected Leads for Enrichment: {len(selected_leads)}")
    st.dataframe(selected_leads.drop(columns=["Select"]), use_container_width=True)

    # Enrich Button
    if not selected_leads.empty:
        if st.button("🚀 Enrich Selected Leads"):
            st.session_state["to_enrich"] = selected_leads.to_dict(orient="records")
            st.success("Ready to enrich! Proceed to enrichment step.")
    else:
        st.info("✅ Select one or more leads to enrich.")
else:
    st.info("Upload a CSV or add at least one manual lead to get started.")

# 🔁 After "🚀 Enrich Selected Leads" button is clicked
if "to_enrich" in st.session_state:
    leads_to_enrich = st.session_state["to_enrich"]

    st.markdown("## 🚀 Enriching Selected Leads")
    with st.spinner("Enriching... please wait"):
        try:
            response = requests.post(API_URL, json=leads_to_enrich)
            if response.status_code == 200:
                enriched_data = response.json()
                df_enriched = pd.DataFrame(enriched_data)

                st.success("✅ Enrichment Complete")

                # Show basic dataframe
                st.subheader("📊 Enriched Lead Table (with Hover Info)")

                # Inject CSS for hover tooltips
                hover_css = """
                <style>
                    .lead-table {
                        width: 100%;
                        border-collapse: collapse;
                        margin-bottom: 2rem;
                    }
                    .lead-table th, .lead-table td {
                        border: 1px solid #ccc;
                        padding: 8px;
                        text-align: left;
                        font-size: 13px;
                    }
                    .hover-container {
                        position: relative;
                        display: inline-block;
                        cursor: pointer;
                    }
                    .hover-container .hover-card {
                        visibility: hidden;
                        width: 280px;
                        background-color: #f9f9f9;
                        color: #333;
                        text-align: left;
                        border-radius: 10px;
                        border: 1px solid #ccc;
                        padding: 10px;
                        position: absolute;
                        z-index: 1;
                        bottom: 125%;
                        left: 50%;
                        margin-left: -140px;
                        box-shadow: 0px 8px 16px rgba(0,0,0,0.2);
                        white-space: normal;
                    }
                    .hover-container:hover .hover-card {
                        visibility: visible;
                    }
                </style>
                """

                st.markdown(hover_css, unsafe_allow_html=True)

                # Display all columns from the enriched data
                all_columns = df_enriched.columns.tolist()

                table_html = "<table class='lead-table'><thead><tr>"
                for col in all_columns:
                    table_html += f"<th>{col}</th>"
                table_html += "</tr></thead><tbody>"

                # Add data rows with hover on "Company"
                for _, row in df_enriched.iterrows():
                    table_html += "<tr>"
                    for col in all_columns:
                        cell_data = str(row.get(col, ""))
                        if col == "Company":
                            # Build hover card content
                            hover_card = f"""
                                <b>Industry:</b> {row.get('Industry', 'N/A')}<br>
                                <b>Revenue:</b> {row.get('Revenue', 'N/A')}<br>
                                <b>Employees:</b> {row.get('Employees_Count', 'N/A')}<br>
                                <b>Owner:</b> {row.get('Owner_First_Name', '')} {row.get('Owner_Last_Name', '')}<br>
                                <b>Email:</b> {row.get('Owner_Email', 'N/A')}
                            """
                            cell_html = f"""
                            <div class="hover-container">{cell_data}
                                <div class="hover-card">{hover_card}</div>
                            </div>
                            """
                        else:
                            cell_html = cell_data
                        table_html += f"<td>{cell_html}</td>"
                    table_html += "</tr>"
                table_html += "</tbody></table>"

                st.markdown(table_html, unsafe_allow_html=True)


                # Optional: Download enriched CSV
                st.download_button(
                    "📥 Download Enriched Leads",
                    df_enriched.to_csv(index=False),
                    "enriched_leads.csv",
                    "text/csv"
                )

            else:
                st.error(f"❌ API returned {response.status_code}: {response.text}")

        except Exception as e:
            st.error(f"❌ Request failed: {e}")


            