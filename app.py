import streamlit as st
import PyPDF2
from skills import skills

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ---------------- SIDEBAR ---------------- #
st.sidebar.title("🤖 AI Resume Analyzer")

st.sidebar.info(
    """
    ### Features

    ✅ Upload Resume PDF

    ✅ Detect Skills

    ✅ Calculate Match Score

    ✅ Suggest Missing Skills
    """
)

# ---------------- TITLE ---------------- #
st.markdown(
    """
    <h1 style='text-align:center;'>
    📄 AI Resume Analyzer
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h4 style='text-align:center; color:gray;'>
    Upload your resume and compare it with a job description.
    </h4>
    """,
    unsafe_allow_html=True
)

st.write("")
st.write("")

# ---------------- INPUTS ---------------- #
resume = st.file_uploader(
    "📤 Upload Resume (PDF)",
    type=["pdf"]
)

job_desc = st.text_area(
    "📝 Paste Job Description Here"
)

# ---------------- PDF TEXT EXTRACTION ---------------- #
def extract_text(file):
    text = ""

    pdf_reader = PyPDF2.PdfReader(file)

    for page in pdf_reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text.lower()


# ---------------- MAIN LOGIC ---------------- #
if resume is not None:

    resume_text = extract_text(resume)

    found_skills = []

    for skill in skills:
        if skill in resume_text:
            found_skills.append(skill)

    st.subheader("✅ Skills Detected")

    if found_skills:
        st.success(" | ".join(found_skills))
    else:
        st.error("No skills detected.")

    # ---------------- JOB DESCRIPTION MATCHING ---------------- #
    if job_desc:

        jd = job_desc.lower()

        jd_skills = []

        for skill in skills:
            if skill in jd:
                jd_skills.append(skill)

        matched = list(
            set(found_skills) &
            set(jd_skills)
        )

        if len(jd_skills) > 0:
            score = (
                len(matched)
                / len(jd_skills)
            ) * 100
        else:
            score = 0

        st.subheader("🎯 Match Score")

        st.progress(int(score))

        st.metric(
            label="Resume Match",
            value=f"{score:.2f}%"
        )

        if score >= 80:
            st.success("Excellent Match 🚀")

        elif score >= 50:
            st.warning("Good Match 👍")

        else:
            st.error("Needs Improvement 📈")

        # ---------------- MISSING SKILLS ---------------- #
        missing = list(
            set(jd_skills) -
            set(found_skills)
        )

        st.subheader("❌ Missing Skills")

        if missing:
            for skill in missing:
                st.error(skill)
        else:
            st.success(
                "No missing skills! Great match."
            )

# ---------------- FOOTER ---------------- #
st.markdown("---")

st.caption(
    "Built with ❤️ using Python, Streamlit and PyPDF2"
)