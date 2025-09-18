# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
import os
from PIL import Image

#st.set_page_config(layout="")
# ---------- Page config & light styling ----------
st.set_page_config(page_title="Agentic AI Framework Readiness Questionnaire", page_icon="📝", layout="centered")

LIGHT_BG = """
<style>
/* soft light gradient background */
#.stApp {
#  background: radial-gradient(1200px 600px at 20% 0%, #ffffff 0%, #f7f9fc 70%, #eef3f8 100%);
#}

/* card look for main container */
.block-container {
  padding-top: 1.2rem;
}

/* section cards */
.card {
  background: #ffffffaa;
  border: 1px solid #e9eef5;
  border-radius: 18px;
  padding: 1.2rem;
  margin-bottom: 1rem;
  box-shadow: 0 6px 22px rgba(16, 38, 73, 0.05);
}

/* headings */
h1, h2, h3 {
  font-weight: 700 !important;
  letter-spacing: .2px;
}

/* subtle divider */
.hr {
  height: 1px;
  background: linear-gradient(90deg, rgba(0,0,0,0), #e7edf5 20%, #e7edf5 80%, rgba(0,0,0,0));
  margin: .6rem 0 1.2rem 0;
}
</style>
"""
#st.markdown(LIGHT_BG, unsafe_allow_html=True)

# ---------- Header with logos ----------
c1, c2, c3 = st.columns([1, 2, 1])
with c1:
    # Adjust paths as needed. If running here, these exist at /mnt/data/...
    for path in ["./btlogo.png", "./nttlogo.png", "/mnt/data/btlogo.png", "/mnt/data/nttlogo.png"]:
        if os.path.exists(path) and "btlogo" in path:
            image = Image.open(path)
            new_image = image.resize((180, 80))
            st.image(new_image, width=180)
            break
with c2:
    st.subheader("Agentic AI Framework Readiness Questionnaire")
    st.caption("Please provide as much detail as you can—this helps us tailor the Agentic AI approach for your needs.")
           
with c3:
    for path in ["./nttlogo.png", "./btlogo.png", "/mnt/data/nttlogo.png", "/mnt/data/btlogo.png"]:
        if os.path.exists(path) and "nttlogo" in path:
            image = Image.open(path)
            new_image = image.resize((180, 80))
            st.image(new_image, width=180)
            break

#bottom_image = st.file_uploader('', type='jpg', key=6)
#if bottom_image is not None:
#    image = Image.open(bottom_image)
#    new_image = image.resize((600, 400))
#    st.image(new_image)
  

#st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
#st.title("AI Agentic Framework Readiness Questionnaire")
#st.caption("Please provide as much detail as you can—this helps us tailor the Agentic AI approach for your needs.")

# ---------- Helper: save to Excel ----------
OUTPUT_XLSX = "survey_responses.xlsx"
SHEET = "Responses"

def save_response(record: dict):
    """Append a single record to an Excel sheet, creating it if needed."""
    new_row = pd.DataFrame([record])
    if os.path.exists(OUTPUT_XLSX):
        try:
            existing = pd.read_excel(OUTPUT_XLSX, sheet_name=SHEET)
            df = pd.concat([existing, new_row], ignore_index=True)
        except Exception:
            # Fallback if sheet or file unreadable
            df = new_row
    else:
        df = new_row
    with pd.ExcelWriter(OUTPUT_XLSX, engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, index=False, sheet_name=SHEET)

# Custom CSS
st.markdown("""
<style>
.form-card {
    background-color: #3f6fde;
    border: 2px solid #e0e6ed;
    border-radius: 15px;
    margin-left: auto;
    margin-right: auto;
    width: 70%;
    padding: 20px 30px;
    margin-top: 15px;
    margin-bottom: 25px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    max-width: 700px;   /* control size */
    
}
</style>
""", unsafe_allow_html=True)

# Use the styled card
#st.markdown('<div class="form-card">', unsafe_allow_html=True)

# ---------- Questionnaire ----------
with st.form("survey_form", clear_on_submit=True):
    #st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Section A: Basic Info & Strategic Alignment")

    #colA1, colA2 = st.columns(2)
    role = st.text_input("What is your current role / department?")
    user_count = st.text_input("How many users would use this solution?")

    st.write("**Most important use cases (select all that apply):**")
    USE_CASES = [
        "1. Inventory update",
        "2. RAID Registration",
        "3. Central reporting and communication",
        "4. Program / Project performance trend and prediction",
        "5. ORT initiation",
        "6. Delays in task completion",
        "7. Inefficient resource allocation",
        "8. Poor visibility into project progress",
        "9. Communication gaps among stakeholders",
        "10. Difficulty in forecasting risks",
        "11. Manual reporting and documentation",
        "12. Others (specify below)"
    ]
    selected_use_cases = st.multiselect(" ", USE_CASES, placeholder="Select one or more")
    other_use_case = st.text_input("If you chose 'Others', please specify:")
    priority_order = st.text_input("Prioritize chosen use cases by number (e.g., 3,4,2):")

    ai_implemented = st.radio("Do you have any existing use cases where AI or automation has been implemented?", ["No", "Yes"], horizontal=True)
    ai_success_notes = st.text_area("If yes, how successful are they so far (what worked, what didn’t)?", disabled=(ai_implemented=="No"))

    centralized_data = st.radio("Do you have centralized data repositories ('single source(s) of truth') that agents could access?", ["No", "Yes"], horizontal=True)
    inhouse_expertise = st.radio("Do you have in-house expertise in AI/ML, data engineering, and/or agentic systems?", ["No", "Yes"], horizontal=True)

    vision = st.text_area("What is your vision for AI/ML, data engineering, and/or agentic systems in short term and long term?")

    expectations = st.multiselect(
        "What are your expectations from implementing an Agentic AI framework?",
        [
            "Increased productivity (Lean PMO)",
            "Better decision support",
            "Enhanced collaboration and communication",
            "Cost savings (Lean PM)",
            "Competitive advantage",
            "Project performance improvement",
            "Other (specify below)"
        ]
    )
    expectations_other = st.text_input("If 'Other', please specify:")
    st.markdown("</div>", unsafe_allow_html=True)

#with st.form():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Section B: Infrastructure & AI Eco-System")

    hosting = st.selectbox("Where do you plan to host Agentic AI?", ["Select...", "On-premises", "Cloud", "Hybrid"])
    cloud = st.selectbox("Preferred cloud provider", ["Select...", "Azure", "AWS", "GCP", "Private Cloud / Other"])
    gpu = st.radio("Do you have GPU availability if required for AI workloads?", ["No", "Yes"], horizontal=True)
    copilot_lic = st.radio("Any plan to purchase Copilot Studio licenses in near future?", ["No", "Yes", "Not sure"], horizontal=True)

    tieups_llms = st.text_area("Do you have OpenAI/Copilot/other tie-ups allowing LLM API access for AI agents?")
    third_party_llm = st.radio("Open to hosting any third-party free LLM (on-prem) in your environment?", ["No", "Yes"], horizontal=True)
    third_party_llm_notes = st.text_area("If yes / any tie-ups, please explain:", disabled=(third_party_llm=="No"))

    demo_vm = st.radio("For a demo AI Agent application—can we provision one Azure VM (with Python) in your secured cloud and get required data/shared folder access?", ["No", "Yes", "Needs approval"], horizontal=True)

    third_party_licenses = st.text_area("Any plan soon for Agentic environments third-party license purchasing (e.g., AI Cloud Foundry or other)?")

    policy_oss = st.text_area("Policy for third-party software approval & open-source license compliance (Streamlit, LangChain, LangGraph, MCP, Pandas, etc.)")

    vectordb_available = st.radio("Do you currently have a licensed vector database available for AI agents?", ["No", "Yes"], horizontal=True)
    vectordb_pref = st.text_input("If not, any preferred vector DB for RAG (e.g., Pinecone, Weaviate, Milvus)?")

    devops_framework = st.text_area("Do you have an existing DevOps/ML Ops framework?")
    monitoring_logging = st.text_area("How do you currently handle monitoring and logging?")
    poc_maintenance = st.text_input("Who will be the point of contact for ongoing maintenance/support?")

    st.markdown("</div>", unsafe_allow_html=True)

  # ---------- Submit ----------
  #st.markdown("<div class='card'>", unsafe_allow_html=True)
    submit = st.form_submit_button("📥 Submit Response", type="primary")
    if submit:
      timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

      record = {
          "timestamp_utc": timestamp,
          "role_department": role,
          "user_count": user_count,
          "use_cases_selected": "; ".join(selected_use_cases),
          "use_cases_other": other_use_case,
          "priority_order": priority_order,
          "ai_implemented": ai_implemented,
          "ai_success_notes": ai_success_notes,
          "centralized_data_sources": centralized_data,
          "inhouse_expertise": inhouse_expertise,
          "vision": vision,
          "expectations": "; ".join(expectations),
          "expectations_other": expectations_other,
          "hosting": hosting,
          "cloud_provider": cloud,
          "gpu_available": gpu,
          "copilot_studio_plan": copilot_lic,
          "llm_api_tieups": tieups_llms,
          "third_party_onprem_llm": third_party_llm,
          "third_party_onprem_llm_notes": third_party_llm_notes,
          "demo_vm_possible": demo_vm,
          "third_party_license_plans": third_party_licenses,
          "policy_open_source": policy_oss,
          "vector_db_available": vectordb_available,
          "vector_db_preferred": vectordb_pref,
          "devops_mlop_framework": devops_framework,
          "monitoring_logging": monitoring_logging,
          "maintenance_poc": poc_maintenance,
      }

      # Basic validation (optional but helpful)
      required_fields = [role, user_count]
      if any(x is None or str(x).strip()=="" for x in required_fields):
          st.error("Please complete Role/Department and Users fields before submitting.")
      else:
          save_response(record)
          st.success("Thanks! Your response has been saved to 'survey_responses.xlsx'.")
          st.dataframe(pd.DataFrame([record]))
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Helpful tip ----------
#with st.expander("🖼️ Image setup tips"):
#    st.write("""
#- This app tries common paths for the logos:
#  - `./btlogo.png` and `./nttlogo.png` (same folder as `app.py`)
#  - `/mnt/data/btlogo.png` and `/mnt/data/nttlogo.png`
#- Place your logo files at either location or update the image paths near the top of the script.
#""")
