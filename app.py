import streamlit as st

st.set_page_config(
    page_title="AI Skincare Advisor",
    page_icon="✨",
    layout="wide"
)

with st.sidebar:
    st.title("✨ AI Skincare Advisor")
    st.markdown("---")
    st.info("Choose a feature from the menu below to begin your skincare routine.")

pg = st.navigation([
    st.Page("pages/1_Skin_Analysis.py", title="Analyze Skin Issues", icon="📸"),
    st.Page("pages/home.py", title="Home", icon="🏠"),
    st.Page("pages/2_Product_Recommendations.py", title="Product Recommendations", icon="🧴"),
    st.Page("pages/3_Home_Remedies.py", title="Home Remedies", icon="🌿")
])

pg.run()
