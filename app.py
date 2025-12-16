import streamlit as st
import os
from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

st.set_page_config(page_title="Multi-Agent AI System")
st.title("🤖 Multi-Agent AI System")

goal = st.text_input("Enter your goal")

if st.button("Run Planner Agent"):
    if not goal:
        st.warning("Please enter a goal")
    else:
        with st.spinner("Planning..."):
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"""
Create a clear 30-day step-by-step learning plan for this goal:
{goal}
"""
                    }
                ],
                model="llama-3.1-8b-instant",
            )

        st.success("Planner Output")
        st.write(chat_completion.choices[0].message.content)