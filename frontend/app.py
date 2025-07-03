import streamlit as st
import pandas as pd

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
