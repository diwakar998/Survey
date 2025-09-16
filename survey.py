# app.py
import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime

st.set_page_config(page_title="Agentic AI Readiness — Quick Survey", page_icon="🤖", layout="centered")

EXCEL_PATH = "agentic_ai_responses.xlsx"  # file on the server where responses are persisted

# --- Header ---
st.title("Agentic AI Readiness — Quick Survey")
st.write("Two quick questions to sensecheck your team's AI familiarity and expectations. "
         "This version saves responses to an Excel file on the server (and offers a download).")

# Use a form so the page doesn't auto-react to each widget change
with st.form(key="agentic_ai_form_v2"):
    st.header("Question 1 — Team familiarity with AI")
    q1 = st.radio(
        label="How familiar is your team with AI concepts and technologies?",
        options=["Very familiar", "Somewhat familiar", "Limited familiarity", "Not familiar"],
        index=1,
        key="q1_familiarity_v2"
    )

    st.markdown("---")
    st.header("Question 12 — Expectations from an Agentic AI framework")
    st.write("Select all that apply (you can pick multiple):")

    options_q12 = [
        "Increased productivity",
        "Better decision support",
        "Enhanced collaboration and communication",
        "Cost savings",
        "Competitive advantage",
        "Other (please specify)"
    ]
    q12_selected = st.multiselect(
        label="Expectations",
        options=options_q12,
        default=[],
        key="q12_expectations_v2"
    )

    other_text = ""
    if "Other (please specify)" in q12_selected:
        other_text = st.text_input(
            label="Please specify other expectations",
            placeholder="e.g. Reduce field ops truck rolls, improve SLA compliance...",
            key="q12_other_text_v2"
        )

    st.markdown("**Additional comments (optional):**")
    comments = st.text_area("", key="q12_comments_v2", height=80, placeholder="Any extra context?")

    submitted = st.form_submit_button(label="Submit responses")

# --- After submission: persist to Excel and show results ---
if submitted:
    timestamp = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    row = {
        "timestamp_utc": timestamp,
        "team_familiarity": q1,
        "expectations_selected": "; ".join(q12_selected) if q12_selected else "",
        "expectations_other_text": other_text or "",
        "additional_comments": comments or ""
    }

    df_new = pd.DataFrame([row])

    # Persist: append to Excel (read existing, concat, write back)
    try:
        if os.path.exists(EXCEL_PATH):
            # read existing sheet
            df_existing = pd.read_excel(EXCEL_PATH)
            df_all = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df_all = df_new

        # write back (overwrites with combined df)
        df_all.to_excel(EXCEL_PATH, index=False)
        st.success("Thanks — response saved to Excel ✅")
        st.write(f"Saved to server file: `{EXCEL_PATH}` (rows now: {len(df_all)})")

        # Prepare in-memory Excel for download (so user gets the latest snapshot)
        towrite = io.BytesIO()
        with pd.ExcelWriter(towrite, engine="openpyxl") as writer:
            df_all.to_excel(writer, index=False, sheet_name="responses")
        towrite.seek(0)

        filename = f"agentic_ai_responses_{timestamp.replace(':','-')}.xlsx"
        st.download_button(
            label="Download current responses as Excel",
            data=towrite,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_excel"
        )

        # Also show the submitted response summary
        st.write("### Your submission")
        st.write(f"**Team familiarity:** {row['team_familiarity']}")
        st.write(f"**Expectations:** {row['expectations_selected']}")
        if row["expectations_other_text"]:
            st.write(f"**Other (details):** {row['expectations_other_text']}")
        if row["additional_comments"]:
            st.write(f"**Comments:** {row['additional_comments']}")

    except Exception as e:
        st.error(f"Could not save to Excel file due to: {e}")
        st.info("If running this app on a multi-user/shared host, consider persisting to a DB, Google Sheet or cloud storage instead.")

# Tip for production
st.info("Tip: For multi-user apps or production usage, prefer a database, Google Sheets, S3, or Airtable to avoid file-locking and concurrency issues.")

