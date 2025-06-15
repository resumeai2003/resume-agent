import streamlit as st
from xhtml2pdf import pisa
from io import BytesIO
import base64

st.set_page_config(page_title="AI Resume Builder", layout="centered")

st.title("📄 AI Resume Builder")
st.markdown("Create your professional resume in minutes!")

# --- User Inputs ---
name = st.text_input("Full Name")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")
summary = st.text_area("Professional Summary")
skills = st.text_area("Skills (comma separated)")
experience = st.text_area("Work Experience")
education = st.text_area("Education")

# --- Create Resume HTML ---
def build_resume_html():
    return f"""
    <html>
    <body>
    <h1 style="color:#4CAF50;">{name}</h1>
    <p><strong>Email:</strong> {email}<br><strong>Phone:</strong> {phone}</p>
    <h2 style="color:#555;">Summary</h2>
    <p>{summary}</p>
    <h2 style="color:#555;">Skills</h2>
    <ul>{"".join(f"<li>{skill.strip()}</li>" for skill in skills.split(","))}</ul>
    <h2 style="color:#555;">Experience</h2>
    <p>{experience}</p>
    <h2 style="color:#555;">Education</h2>
    <p>{education}</p>
    </body>
    </html>
    """

# --- Convert HTML to PDF ---
def convert_html_to_pdf(source_html):
    result = BytesIO()
    pisa_status = pisa.CreatePDF(src=source_html, dest=result)
    return result.getvalue() if not pisa_status.err else None

# --- Generate Resume ---
if st.button("Generate Resume"):
    if name and email:
        resume_html = build_resume_html()
        st.markdown("### 🖥️ Resume Preview")
        st.markdown(resume_html, unsafe_allow_html=True)

        pdf = convert_html_to_pdf(resume_html)

        if pdf:
            b64 = base64.b64encode(pdf).decode("utf-8")
            href = f'<a href="data:application/pdf;base64,{b64}" download="resume.pdf">📥 Download PDF</a>'
            st.markdown(href, unsafe_allow_html=True)
        else:
            st.error("Error generating PDF.")
    else:
        st.warning("Please enter at least your name and email.")
Added main app code
