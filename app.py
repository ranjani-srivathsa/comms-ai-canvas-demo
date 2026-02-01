import streamlit as st
from groq import Groq

# Init Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="Communication AI Canvas", layout="wide")

st.title("Communication AI Canvas")
st.caption("Framework-driven communication generator (Demo)")

# ----------------------
# Mode Selection
# ----------------------
mode = st.radio(
    "Select Communication Maturity Mode",
    ["Quick Mode", "Deep Mode"]
)

st.divider()

# ----------------------
# QUICK MODE
# ----------------------
if mode == "Quick Mode":
    st.subheader("Quick Mode Inputs")

    audience = st.selectbox(
        "Audience",
        ["Employees", "Managers", "Leadership", "Global HQ", "Others"]
    )

    purpose = st.selectbox(
        "Purpose",
        ["Awareness", "Adoption", "Reassurance", "Alignment", "Others"]
    )

    change = st.text_input("What is changing? (1–2 lines)")

    geography = st.selectbox(
        "Geography",
        ["Global", "North America", "Europe", "India", "APAC", "Middle East & Africa", "Others"]
    )

    tone = st.selectbox(
        "Tone",
        ["Reassuring", "Inspirational", "Direct", "Neutral"]
    )

    outputs = st.multiselect(
        "Outputs Needed",
        ["Email", "1-page summary", "Leadership talking points"]
    )

    canvas_data = f"""
Audience: {audience}
Purpose: {purpose}
Change: {change}
Geography: {geography}
Tone: {tone}
"""

# ----------------------
# DEEP MODE (YOUR CANVAS)
# ----------------------
else:
    st.subheader("Deep Mode — Strategic Canvas")

    st.markdown("### Target Audience")
    exp_level = st.multiselect("Experience Level", ["Early career", "Mid-level", "Senior", "Executive"])
    geo = st.multiselect("Geography", ["Global", "North America", "Europe", "India", "APAC", "Middle East & Africa"])
    internal_external = st.selectbox("Internal / External", ["Internal", "External", "Both"])

    st.markdown("### Context")
    main_objective = st.text_input("Main Objective of Communication")

    problem_opportunity = st.text_area(
        "Problem / Opportunity (bullet-style)",
        placeholder="- Employee engagement\n- Knowledge sharing\n- Low visibility"
    )

    value_prop = st.text_area(
        "Value Proposition (What's in it for me?)",
        placeholder="- Recognition and visibility\n- Career growth\n- Learning opportunities"
    )

    value_reflections = st.multiselect(
        "Values / Emotions to Reflect",
        ["Collaboration", "Pride", "Innovation", "Trust", "Transparency", "Motivation", "Belonging", "Confidence"]
    )

    st.markdown("### Character")
    existing_perceptions = st.text_area("Existing Perceptions / Expectations")

    expression_style = st.selectbox(
        "Expression / Style",
        ["Professional", "Concise", "Warm", "Executive-style", "Inspirational"]
    )

    st.markdown("### Outputs")
    outputs = st.multiselect(
        "Outputs Needed",
        ["Email", "1-page summary", "Leadership talking points"]
    )

    canvas_data = f"""
Audience Experience Level: {exp_level}
Geography: {geo}
Internal/External: {internal_external}

Main Objective: {main_objective}

Problem / Opportunity:
{problem_opportunity}

Value Proposition:
{value_prop}

Value Reflections:
{value_reflections}

Existing Perceptions:
{existing_perceptions}

Expression Style:
{expression_style}
"""

# ----------------------
# GENERATE BUTTON
# ----------------------
st.divider()

if st.button("Generate Communication Assets"):
    with st.spinner("Generating..."):

        system_prompt = f"""
You are a consulting-grade communication assistant.
Use the structured canvas below to generate high-quality enterprise communications.

Canvas:
{canvas_data}

Generate the following outputs in professional consulting style:
{outputs}

Use these templates:
- Email: business context, what's changing, what's in it for me, emotional framing, call to action
- 1-page summary: executive-style structured one-pager
- Leadership talking points: structured speaking points for leaders
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Generate now."}
            ],
            temperature=0.4,
            max_tokens=1200
        )

        result = response.choices[0].message.content

        st.success("Generated Successfully")
        st.text_area("Generated Outputs", result, height=500)
