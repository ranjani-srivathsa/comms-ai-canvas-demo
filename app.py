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
    role = st.text_input("Audience Role (e.g., Business Unit Lead, Project Manager)")
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
    
    cta = st.text_input("Call to Action (1 sentence) — e.g., 'Submit your story to X by Y date'")

    st.markdown("### Outputs")
    outputs = st.multiselect(
        "Outputs Needed",
        ["Email", "1-page summary", "Leadership talking points"]
    )

    canvas_data = f"""
Audience Experience Level: {exp_level}
Role: {role}
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
You are an internal communications assistant. Your job is to create professional internal communication outputs based on structured inputs.

INPUTS:
- Audience Role: {role}
- Experience Level: {exp_level}
- Geography: {geo}
- Internal/External: {internal_external}
- Main Objective: {main_objective}
- Problem / Opportunity: {problem_opportunity}
- Value Proposition: {value_prop}
- Values / Emotions: {value_reflections}
- Existing Perceptions: {existing_perceptions}
- Expression / Style: {expression_style}
- Call to Action: {cta}

TASK:
1. Generate ONLY the output types selected: {outputs}
2. Output instructions by type:

**Email:**
- Subject line concise & clear
- Greeting: "Dear {role},"
- Body: 3–5 short paragraphs or 5–6 sentences max
- Emphasize Value Proposition and Main Objective
- Address Existing Perceptions briefly if needed
- Reinforce Values/Emotions subtly
- Include CTA exactly as provided, at the END
- Avoid “I/we”, generic corporate phrasing, or abstract statements

**Leadership Talking Points:**
- 4–6 short bullets
- Highlight key messages from Value Proposition and Main Objective
- Reinforce Values/Emotions subtly
- Include CTA as action item
- Keep it short, punchy, actionable

**1-Page Summary:**
- 1 page (~200–250 words)
- Summarize Main Objective, Problem/Opportunity, Value Proposition
- Use short paragraphs
- Reinforce Values/Emotions subtly
- Include CTA at the end
- Avoid generic justifications or motivational fluff

STRICT RULES:
- Do NOT generate outputs not selected
- Do NOT add extra commentary or sections
- Do NOT invent deadlines, owners, platforms, or content
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

