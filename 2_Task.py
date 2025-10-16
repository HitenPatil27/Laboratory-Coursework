import streamlit as st
from groq import Groq

# ⚙️ Initialize Groq client
client = Groq(api_key="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")

# 🧱 Streamlit page setup
st.set_page_config(
    page_title="LLM Comparative Study – Groq",
    page_icon="🧠",
    layout="centered"
)
st.title("🧠 LLM Comparative Study")
st.write("""
This app compares responses generated from:
1. **User Prompt + LLM**  
2. **System + User Prompt + LLM**
""")

# 🔤 User input
prompt_text = st.text_area(
    "Enter your prompt:",
    "Explain SIP vs mutual funds in simple terms.",
    height=120
)

if st.button("Run Comparison"):
    with st.spinner("Generating responses..."):
        # Case A – User Prompt Only
        response_a = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt_text}],
            temperature=0.2
        )
        text_a = response_a.choices[0].message.content.strip()

        # Case B – System + User Prompt
        system_msg = (
            "You are a subject-matter expert. "
            "Answer succinctly with structured output where applicable."
        )
        response_b = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.2
        )
        text_b = response_b.choices[0].message.content.strip()

    # 📊 Display results side-by-side
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("A. User Prompt Only")
        st.text_area("Response A", text_a, height=300)
    with col2:
        st.subheader("B. System + User Prompt")
        st.text_area("Response B", text_b, height=300)

    # Optional summary
    st.markdown("---")
    st.markdown("✅ *Comparison complete. Observe how the system prompt improves structure, tone, and accuracy.*")

