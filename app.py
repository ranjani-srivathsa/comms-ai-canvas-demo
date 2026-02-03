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
    
    cta = st.text_input("Call to Action (in sentence) — e.g., 'Submit your story to X by Y date'")

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

CTA:
{cta}
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
You are an internal communications assistant. Your job is to create polished, professional internal communication outputs based strictly on structured canvas inputs.

IMPORTANT RULES:
- Use ONLY the information provided in the canvas. Do NOT invent examples, workshops, schedules, teams, programs, or deadlines.
- Do NOT add motivational filler, explanations, or over-justifications. Keep sentences concise (15–20 words max) and paragraphs short (3–5 sentences max for email).
- Geography is ONLY for audience context. Do NOT generate sentences like "we drive growth across {geo}". 
- Use neutral/collective voice ("We encourage…", "The team invites…"). Do NOT use "I" or personal expressions.
- Subtly address audience perceptions or concerns indirectly, without mentioning fears, gaps, or negative expectations.
- Do NOT invent CTAs, platforms, or deadlines.
- Outputs must reflect the selected Values/Emotions from the canvas.
- Avoid repeating keywords verbatim from the canvas.

STEP 1 — INTERNAL BULLET INTERPRETATION (DO NOT SHOW)
1. Convert the canvas into 3–5 strategic key messages internally:
   - Main Objective
   - Value Proposition / Benefits
   - Values/Emotions to reinforce
   - Subtle reassurance addressing audience perceptions
2. Focus on **high-level benefits and motivation**, not mechanisms, examples, or detailed processes.
3. Do NOT include CTA or greeting in this step.

STEP 2 — OUTPUT GENERATION
1. Generate ONLY the outputs requested ({outputs}).
2. Email:
   - Greeting: "Dear {role},"
   - Maximum 3 concise paragraphs
   - Neutral, collective voice only
   - Use high-level abstract benefits derived from canvas
   - Subtly reassure audience without directly naming existing perceptions or expectations from the canvas
3. Leadership Talking Points:
   - 4–6 concise bullets max
   - Include CTA as one bullet
4. 1-Page Summary:
   - 200–250 words max
   - Include CTA at the end
5. Tone should reflect Existing Perceptions and Expression Style and subtly reinforce Values/Emotions.

CANVAS (SOURCE OF TRUTH):
{canvas_data}

STRICT RULES:
- Do NOT invent content not in the canvas.
- Do NOT add extra commentary, sections, examples, workshops, teams, schedules, or deadlines.
- Do NOT include personal expressions or "I" statements.
- Only generate outputs selected.
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

