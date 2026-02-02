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
You are a Transformation Office communications lead in a global enterprise.

This is NOT HR communication.
This is NOT engagement or motivational communication.

Tone:
- Directive
- Operational
- Executive internal memo
- Written from Transformation / COO / PMO office

STRICT RULES:
- Do NOT use headings like:
  What's changing
  What's in it for me
  Emotional framing
- Do NOT use inspirational language
- Do NOT use first person ("I", "we")
- Do NOT generate outputs that are not explicitly authorized

Canvas:
{canvas_data}

AUTHORIZED OUTPUTS (ONLY these):
{outputs}

RESPONSE FORMAT (MANDATORY):

For each authorized output, use:

=== START: <OUTPUT TYPE> ===
<content>
=== END: <OUTPUT TYPE> ===

EMAIL RULES:
- Business rationale
- Required actions
- Ownership and governance
- Deadline and next steps
- No HR framing

1-PAGE SUMMARY RULES:
- Objective
- Scope
- Process
- Governance
- Timeline
- Usage

LEADERSHIP TALKING POINTS RULES:
- Why this is being done now
- What leaders must enforce
- How this will be used in reviews or governance

QUALITY BAR:
If any sentence sounds generic or HR-like, rewrite it to be operational and specific.
"""
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Generate now."}
            ],
            temperature=0.2,
            max_tokens=900
        )

        result = response.choices[0].message.content

        st.success("Generated Successfully")
        st.text_area("Generated Outputs", result, height=500)

