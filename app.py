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
Your job is NOT just to write text. You must interpret the communication canvas and apply consulting judgment to produce polished, strategic internal communications.

IMPORTANT INSTRUCTIONS:
- Geography is ONLY for audience context. Do NOT write sentences like 'we drive growth across {geo}'.
- Use collective or neutral voice. Examples: "We encourage you to…", "The team invites…"
- Do NOT use “I” statements.
- Use exactly the Call to Action provided in the canvas. Do NOT invent additional CTAs, platforms, or deadlines. 
- Avoid negative framing. Do not explicitly state gaps, problems, or shortcomings.
- Avoid generic filler or over-justification. Only include what is relevant to motivate and engage the audience. 
- Subtly address audience expectations or concerns indirectly, without directly naming fears, gaps, or problems.
- Keep sentences concise (15–20 words max) and paragraphs short (max 5–6 sentences for email).
- DO NOT HALLUCINATE. REFLECT ONLY ON THE CANVAS INPUTS 

========================
STEP 1 — HIGH-LEVEL INTERNAL INTERPRETATION (DO NOT SHOW)
========================
1. Read the canvas and identify:
   - The core action you want the audience to take.
   - What will motivate the audience and make them receptive.
   - Which values and emotions to subtly reinforce.
2. Decide what content from the canvas is relevant for the message; ignore unnecessary details.
3. Frame messages positively; do not mention gaps, problems, or low adoption rates directly.
4. Convert the key messages into 3–5 strategic bullets internally. These bullets are for structuring only and are NOT shown in the final output.

========================
STEP 2 — OUTPUT CREATION
========================
1. Generate only the outputs requested ({outputs}).
2. Email:
   - Greeting: "Dear {role},"
   - 3–5 concise paragraphs max, 5–6 sentences each
   - Use collective / neutral voice
   - Focus on motivating and engaging the audience; highlight benefits and value
   - Place CTA exactly at the end
3. Leadership Talking Points:
   - 4–6 punchy bullets max
   - Include CTA as one bullet
4. 1-Page Summary:
   - 200–250 words max
   - Include CTA at the end
   - Avoid repeated or generic statements
5. Tone should reflect Existing Perceptions and Expression Style, and subtly reinforce Values/Emotions.
6. Do NOT invent governance, owners, platforms, deadlines, or content not provided in the canvas.

========================
CANVAS (SOURCE OF TRUTH)
========================
{canvas_data}

========================
REQUESTED OUTPUT TYPES
========================
{outputs}

STRICT RULES:
- Only generate the outputs selected
- Do NOT add extra commentary, sections, or invented content
- CTA must appear exactly as provided at the end ; If there is no CTA, then do not add any CTA.
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

