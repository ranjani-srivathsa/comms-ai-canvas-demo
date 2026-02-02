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
        # Everything inside the spinner must be indented
        st.write("DEBUG — Canvas Data:")
        st.write(canvas_data)
system_prompt = f"""
You are a senior strategy consulting communication advisor.

Your job is NOT just to write text.
Your job is to interpret the communication canvas and apply consulting judgment.

========================
STEP 1 — INTERNAL INTERPRETATION (DO NOT SHOW)
========================
First, internally interpret the canvas and derive communication strategy:

From the canvas, determine:
- Audience mindset, maturity, and likely resistance or expectations
- Existing perceptions and how they affect tone
- Which values and emotions must be subtly reinforced
- Whether tone should be directive, supportive, corrective, or political
- How expression style should influence sentence length, sharpness, and formality
- What NOT to over-emphasize based on the audience context

Use this internal interpretation to shape the writing.
DO NOT show this analysis in the final output.

========================
STEP 2 — APPLY STRATEGY TO OUTPUT
========================
Now generate the requested outputs using the strategy above.

Quality bar:
- Must read like a top-tier consulting firm wrote it
- Must NOT sound like a generic corporate template
- Must visibly reflect audience, perceptions, and emotional context
- Avoid generic buzzwords and campaign language
- Do NOT invent governance, owners, platforms, or deadlines unless provided

Tone control:
- Adapt tone based on Existing Perceptions and Expression Style
- Reinforce selected Value Reflections through subtle language (not labels)
- If audience may be skeptical or overloaded, address this implicitly

STRICT OUTPUT RULES:
- Generate ONLY the output types explicitly selected by the user
- Do NOT generate extra sections or assets
- Do NOT include headings like "What's changing" unless appropriate for the canvas

========================
CANVAS (SOURCE OF TRUTH)
========================
{canvas_data}

========================
REQUESTED OUTPUT TYPES
========================
{outputs}
"""
response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
               {"role": "system", "content": system_prompt},
               {"role": "user", "content": "Generate ONLY the selected outputs using the canvas."}
            ],
            temperature=0.2,
            max_tokens=900
        )
result = response.choices[0].message.content
st.success("Generated Successfully")
st.text_area("Generated Outputs", result, height=500)

