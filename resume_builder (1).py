
import streamlit as st
from jinja2 import Template
from fpdf import FPDF
import base64

# Function to generate resume text from template
def generate_resume(data):
    template_str = '''
{{ name }}  
{{ education }}  
📞 {{ phone }} | 📧 {{ email }} | 📍 {{ location }}

🎯 OBJECTIVE  
{{ objective }}

🛠️ SKILLS  
{% for skill in skills %}• {{ skill }}  
{% endfor %}

📚 EDUCATION  
{{ education }}

📁 PROJECTS  
{% for project in projects %}**{{ project.title }}**  
• {{ project.description }}
{% endfor %}

🏅 CERTIFICATIONS  
{% for cert in certifications %}• {{ cert }}  
{% endfor %}

💬 LANGUAGES  
{{ languages }}

🎨 INTERESTS  
{{ interests }}
'''
    template = Template(template_str)
    return template.render(**data)

# Convert text to PDF
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)
    return pdf.output(dest='S').encode('latin-1')

# Download link for PDF
def get_download_link(pdf_bytes, filename):
    b64 = base64.b64encode(pdf_bytes).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">📄 Download Resume PDF</a>'

# Streamlit UI
st.title("💼 Role-Based Resume Builder")

with st.form("resume_form"):
    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")
    location = st.text_input("Location")
    role = st.text_input("Job Role")
    experience = st.selectbox("Experience Level", ["Fresher", "1-2 years", "3-5 years", "5+ years"])
    education = st.text_input("Education")
    skills = st.text_area("Skills (comma-separated)").split(',')
    languages = st.text_input("Languages Known")
    interests = st.text_input("Hobbies / Interests")
    objective = st.text_area("Career Objective")

    st.markdown("**Projects**")
    project_titles = st.text_area("Project Titles (comma-separated)").split(',')
    project_descriptions = st.text_area("Project Descriptions (match order, comma-separated)").split(',')
    projects = [{'title': t.strip(), 'description': d.strip()} for t, d in zip(project_titles, project_descriptions)]

    st.markdown("**Certifications**")
    certifications = st.text_area("Certifications (comma-separated)").split(',')

    submitted = st.form_submit_button("Generate Resume")

if submitted:
    data = {
        'name': name,
        'phone': phone,
        'email': email,
        'location': location,
        'role': role,
        'experience': experience,
        'education': education,
        'skills': [s.strip() for s in skills if s.strip()],
        'languages': languages,
        'interests': interests,
        'objective': objective,
        'projects': projects,
        'certifications': [c.strip() for c in certifications if c.strip()],
    }
    resume_text = generate_resume(data)
    pdf_bytes = create_pdf(resume_text)
    st.markdown(get_download_link(pdf_bytes, f"{name}_Resume.pdf"), unsafe_allow_html=True)
    st.success("Resume generated successfully!")
