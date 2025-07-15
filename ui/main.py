# ui/main.py
import streamlit as st
from ai.ai_dummy import check_legality_dummy

# Styling (can expand with st.markdown CSS if needed)
PRIMARY_COLOR = "#2B4F81"  # Deep blue
ACCENT_COLOR = "#A9CCE3"   # Light blue
BG_COLOR = "#FAFAFA"

def render():
    st.markdown(f"""
        <style>
            body {{
                background-color: {BG_COLOR};
            }}
            .reportview-container {{
                background-color: {BG_COLOR};
            }}
            h1, h3, .stButton>button {{
                color: {PRIMARY_COLOR};
            }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <h1 style='text-align: center;'>⚖️ Law Checker</h1>
    <p style='text-align: center; font-size: 18px;'>
        Ask your legal question and get a quick AI-based judgment.
    </p>
    """, unsafe_allow_html=True)

    st.write("\n")
    st.subheader("💬 Ask a legal question")

    with st.form(key="law_check_form"):
        user_input = st.text_area("Type your legal question or describe your scenario:", height=150)
        submitted = st.form_submit_button("🔍 Check Legality")

        if submitted:
            if not user_input.strip():
                st.warning("Please enter a question.")
            else:
                result = check_legality_dummy(user_input, country="Greece")
                st.success("AI Response:")
                st.markdown(f"""
                <div style='background-color:#EDF4FB;padding:15px;border-radius:10px;'>
                    <code>{result}</code>
                </div>
                """, unsafe_allow_html=True)

    st.write("\n")
    st.subheader("👨‍⚖️ Recommended Lawyers")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://randomuser.me/api/portraits/men/32.jpg", width=100)
        st.markdown("**Alex Papadopoulos**")
        st.caption("Criminal & Civil Law - Athens")

    with col2:
        st.image("https://randomuser.me/api/portraits/women/45.jpg", width=100)
        st.markdown("**Maria Georgiou**")
        st.caption("Human Rights & Immigration Law - Thessaloniki")

    with col3:
        st.image("https://randomuser.me/api/portraits/men/17.jpg", width=100)
        st.markdown("**Nikos Economou**")
        st.caption("Commercial & Tech Law - Patras")
