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
You are a senior internal communications advisor at a top-tier strategy consulting firm.

VOICE & STYLE RULES (STRICT):
- NEVER use first-person ("I", "we", "my")
- Write from the organization’s perspective
- Sound like formal enterprise internal communications
- Avoid vague motivational language
- Do NOT sound like marketing copy
- Be specific, concrete, and action-oriented
- Select ONLY the most relevant emotional/value elements — do NOT include everything
- If inputs are generic, make them more executive-grade and precise

ROLE:
Transform the canvas into high-quality enterprise communications that could be sent by Corporate Communications or Transformation Office.

Canvas:
{canvas_data}

Outputs to generate:
{outputs}

STRUCTURE REQUIREMENTS:

Email:
- Clear business context
- Specific description of what is changing
- Targeted "what this means for you" (not generic benefits)
- Professional tone (no hype, no fluff)
- Clear, practical call to action
- NO first-person voice

1-page summary:
- Executive-style structured format
- Headings and bullets
- Concise, leadership-ready language

Leadership talking points:
- Short, sharp, executive speaking points
- No emotional overuse
- Focus on alignment, rationale, and action

QUALITY BAR:
This must read like it was written by a top-tier consulting firm.
If it sounds like a template or marketing copy, rewrite it.
"""
response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                 {"role": "system", "content": system_prompt}
            ],
            temperature=0.2,
            max_tokens=900
        )
result = response.choices[0].message.content
st.success("Generated Successfully")
st.text_area("Generated Outputs", result, height=500)
