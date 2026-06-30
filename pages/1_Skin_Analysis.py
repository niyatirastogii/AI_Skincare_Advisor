import streamlit as st
from PIL import Image
import numpy as np
import cv2
import os

# Import custom modules
from modules.cv_analysis import analyze_skin, draw_face_mesh, HAS_MEDIAPIPE
from modules.gemini_analysis import analyze_skin_image
from modules.database import search_products_by_name, get_products_by_ingredients

# -------------------------
# PAGE SETUP
# -------------------------
st.set_page_config(
    page_title="Skin Analysis & Recommendations",
    page_icon="📸",
    layout="wide"
)

# Inject Premium CSS Styles
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

/* Global Font Override */
.main .block-container, p, span, div, h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif !important;
}

/* Glassmorphism Cards */
.glass-card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
}

.advisor-banner {
    background: linear-gradient(135deg, rgba(212, 175, 55, 0.1) 0%, rgba(200, 150, 40, 0.03) 100%);
    border: 1px solid rgba(212, 175, 55, 0.2);
    border-radius: 16px;
    padding: 30px;
    margin-bottom: 30px;
    text-align: center;
}

.banner-title {
    font-weight: 700;
    font-size: 2.5rem;
    margin-bottom: 8px;
    background: linear-gradient(135deg, #f5e0a3, #d4af37);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.banner-sub {
    font-size: 1.1rem;
    color: #aaaaaa;
    font-weight: 300;
}

/* Metric Cards */
.metric-container {
    display: flex;
    gap: 16px;
    margin-bottom: 20px;
}

.metric-card {
    flex: 1;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 18px;
    text-align: center;
    transition: transform 0.2s ease;
}

.metric-card:hover {
    transform: translateY(-2px);
    border-color: rgba(212, 175, 55, 0.2);
}

.metric-val {
    font-size: 1.8rem;
    font-weight: 700;
    color: #d4af37;
    margin-bottom: 4px;
}

.metric-lbl {
    font-size: 0.85rem;
    color: #888888;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Badges & Pills */
.severity-badge {
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    display: inline-block;
    margin-top: 5px;
}

.severity-Mild {
    background-color: rgba(46, 204, 113, 0.15);
    color: #2ecc71;
    border: 1px solid rgba(46, 204, 113, 0.3);
}

.severity-Moderate {
    background-color: rgba(241, 196, 15, 0.15);
    color: #f1c40f;
    border: 1px solid rgba(241, 196, 15, 0.3);
}

.severity-Severe {
    background-color: rgba(231, 76, 60, 0.15);
    color: #e74c3c;
    border: 1px solid rgba(231, 76, 60, 0.3);
}

.ingredient-pill {
    background: rgba(212, 175, 55, 0.08);
    color: #e0be53;
    border: 1px solid rgba(212, 175, 55, 0.25);
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 500;
    display: inline-block;
    margin: 4px;
}

/* Remedy Card */
.remedy-card {
    background: rgba(46, 204, 113, 0.02);
    border: 1px solid rgba(46, 204, 113, 0.08);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    transition: all 0.3s ease;
}

.remedy-card:hover {
    border-color: rgba(46, 204, 113, 0.25);
    background: rgba(46, 204, 113, 0.04);
}

.remedy-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #2ecc71;
    margin-bottom: 8px;
}

/* Product Recommendation Card Grid */
.product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

.product-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    display: flex;
    flex-direction: column;
    height: 100%;
}

.product-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
    border-color: rgba(212, 175, 55, 0.3);
    background: rgba(255, 255, 255, 0.04);
}

.product-image-container {
    height: 200px;
    background: rgba(255, 255, 255, 0.01);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    position: relative;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.product-image {
    max-height: 90%;
    max-width: 90%;
    object-fit: contain;
    padding: 10px;
    transition: transform 0.5s ease;
}

.product-card:hover .product-image {
    transform: scale(1.04);
}

.product-details {
    padding: 16px;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
}

.product-brand {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #888888;
    margin-bottom: 4px;
}

.product-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 8px;
    line-height: 1.4;
    height: 40px;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}

.product-reason {
    font-size: 0.75rem;
    background: rgba(212, 175, 55, 0.08);
    color: #d4af37;
    padding: 4px 8px;
    border-radius: 4px;
    align-self: flex-start;
    margin-bottom: 12px;
    border: 1px solid rgba(212, 175, 55, 0.15);
    font-weight: 500;
}

.product-link-btn {
    display: block;
    text-align: center;
    background: linear-gradient(135deg, #d4af37, #b8860b);
    color: #000000 !important;
    text-decoration: none !important;
    font-weight: 600;
    padding: 10px 16px;
    border-radius: 8px;
    font-size: 0.9rem;
    transition: all 0.2s ease;
    margin-top: auto;
}

.product-link-btn:hover {
    background: linear-gradient(135deg, #f3e5ab, #d4af37);
    transform: scale(1.02);
    box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
}

.error-card {
    background-color: rgba(231, 76, 60, 0.1);
    border: 1px solid rgba(231, 76, 60, 0.3);
    border-radius: 12px;
    padding: 20px;
    color: #e74c3c;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# INITIALIZE SESSION STATE
# -------------------------
if "analysis_results" not in st.session_state:
    st.session_state["analysis_results"] = None

# -------------------------
# HEADER BANNER
# -------------------------
st.markdown("""
<div class="advisor-banner">
    <div class="banner-title">✨ AI Skincare Diagnosis & Advisor</div>
    <div class="banner-sub">Upload an image of your skin to get a detailed computer vision scan, Gemini AI analysis, matching product links, and home remedies.</div>
</div>
""", unsafe_allow_html=True)

st.warning("⚠️ Disclaimer: This tool is powered by AI and computer vision. It is for informational and educational purposes only and does NOT substitute for professional medical advice, diagnosis, or treatment.")

# -------------------------
# IMAGE INPUT OPTIONS
# -------------------------
col_input, col_info = st.columns([2, 1])

with col_input:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    option = st.radio(
        "Choose Image Source",
        ["Upload Skin Image", "Use Camera Capture"],
        horizontal=True
    )

    image = None

    if option == "Upload Skin Image":
        uploaded_file = st.file_uploader(
            "Upload a clear photo of your skin or face",
            type=["jpg", "jpeg", "png"]
        )
        if uploaded_file is not None:
            image = Image.open(uploaded_file)

    elif option == "Use Camera Capture":
        st.info("📷 **Camera not loading?** If you see a black screen or loading spinner, please check the right side of your browser's address bar and click the camera icon to **Allow** camera access.")
        camera_image = st.camera_input("Capture a clear photo of your skin")
        if camera_image is not None:
            image = Image.open(camera_image)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col_info:
    st.markdown("""
    <div class="glass-card" style="height: 100%;">
        <h3>💡 Tips for Best Results</h3>
        <ul style="padding-left: 20px; margin-bottom: 0;">
            <li><strong>Lighting:</strong> Ensure good, even natural lighting. Avoid heavy shadows.</li>
            <li><strong>Focus:</strong> Hold the camera stable to get a sharp, in-focus shot.</li>
            <li><strong>Clean Skin:</strong> A face without makeup or sunscreen yields the most accurate readings.</li>
            <li><strong>Close-up:</strong> Frame your main skin concern area clearly in the center.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# -------------------------
# PROCESSING & ANALYSIS
# -------------------------
if image is not None:
    st.markdown("---")
    col_img_display, col_cv_results = st.columns([1, 1])
    
    # Run CV analysis immediately when image is loaded
    try:
        # Convert PIL image to OpenCV BGR image
        opencv_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        cv_results = analyze_skin(opencv_img)
    except Exception as e:
        st.error(f"Error executing computer vision analysis: {e}")
        cv_results = None

    with col_img_display:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📸 Your Skin Photo")
        
        # Face landmarks toggle
        if HAS_MEDIAPIPE:
            show_landmarks = st.checkbox("Overlay Face Mesh (MediaPipe)", value=False)
        else:
            show_landmarks = False
            st.info("ℹ️ Face mesh overlay is disabled (MediaPipe solutions not supported on this Python environment).")
        
        if show_landmarks and cv_results is not None and cv_results["landmarks"]:
            mesh_img = draw_face_mesh(opencv_img, cv_results["landmarks"])
            mesh_rgb = cv2.cvtColor(mesh_img, cv2.COLOR_BGR2RGB)
            st.image(mesh_rgb, use_container_width=True, caption="Face Landmarks Overlay")
        else:
            st.image(image, use_container_width=True, caption="Selected Image")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_cv_results:
        st.markdown('<div class="glass-card" style="height: 100%;">', unsafe_allow_html=True)
        st.subheader("🔍 Computer Vision Diagnostics")
        
        if cv_results is not None:
            # Display Score & Heatmap side by side
            cv_col_metrics, cv_col_heatmap = st.columns([1, 1])
            
            with cv_col_metrics:
                # Skin Score Metric
                st.markdown(f"""
                <div class="metric-card" style="margin-bottom: 15px;">
                    <div class="metric-val">{cv_results['skin_score']}/100</div>
                    <div class="metric-lbl">Overall Skin Score</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Redness Metric
                st.markdown(f"""
                <div class="metric-card" style="margin-bottom: 15px;">
                    <div class="metric-val">{cv_results['redness']}</div>
                    <div class="metric-lbl">Redness Index</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Acne Spot Count Metric
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-val">{cv_results['acne']}</div>
                    <div class="metric-lbl">Estimated Spots/Pores</div>
                </div>
                """, unsafe_allow_html=True)
                
            with cv_col_heatmap:
                heatmap_rgb = cv2.cvtColor(cv_results['heatmap'], cv2.COLOR_BGR2RGB)
                st.image(heatmap_rgb, use_container_width=True, caption="Skin Redness/Texture Heatmap")
        else:
            st.info("No face mesh details could be extracted. Please make sure your face is visible in the frame.")
            
        st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------
    # TRIGGER GEMINI AI ANALYSIS
    # -------------------------
    st.markdown('<div style="text-align: center; margin: 30px 0;">', unsafe_allow_html=True)
    analyze_btn = st.button("🔍 Run Full AI Skin Diagnosis", type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if analyze_btn:
        with st.spinner("AI analyzing your skin image & matching products..."):
            ai_data = analyze_skin_image(image)
            
            if "error" in ai_data:
                st.markdown(f"""
                <div class="error-card">
                    <strong>Error:</strong> {ai_data['error']}
                </div>
                """, unsafe_allow_html=True)
            else:
                # Match recommended products & ingredients to database
                recommended_names = ai_data.get("recommended_products", [])
                matched_by_name = search_products_by_name(recommended_names, limit=2)
                
                recommended_ingredients = ai_data.get("recommended_ingredients", [])
                matched_by_ing = get_products_by_ingredients(
                    recommended_ingredients,
                    skin_type=ai_data.get("skin_type"),
                    limit_per_ingredient=2
                )
                
                # Merge and de-duplicate recommendations
                seen_names = set()
                matched_products = []
                
                for p in matched_by_name:
                    if p["product_name"] not in seen_names:
                        matched_products.append(p)
                        seen_names.add(p["product_name"])
                
                for p in matched_by_ing:
                    if p["product_name"] not in seen_names:
                        matched_products.append(p)
                        seen_names.add(p["product_name"])
                
                # Save results in session state
                st.session_state["analysis_results"] = {
                    "ai": ai_data,
                    "matched_products": matched_products
                }
                st.success("✅ AI Diagnosis Complete!")

    # -------------------------
    # DISPLAY AI RESULTS
    # -------------------------
    if st.session_state["analysis_results"] is not None:
        results = st.session_state["analysis_results"]
        ai_data = results["ai"]
        matched_products = results["matched_products"]
        
        st.markdown("---")
        st.header("🧬 AI Diagnosis Report")
        
        col_type_issues, col_remedies = st.columns([1, 1])
        
        with col_type_issues:
            # Skin Type Card
            st.markdown(f"""
            <div class="glass-card">
                <h3>🧴 Diagnosed Skin Type</h3>
                <h1 style="color:#d4af37; margin: 10px 0; font-size: 2.8rem; font-weight:700;">{ai_data.get('skin_type', 'N/A')}</h1>
                <p style="color: #cccccc;">Your skin matches characteristics of <strong>{ai_data.get('skin_type', 'N/A').lower()}</strong> skin. Ensure you choose formulations targeted specifically for this skin type.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Skin Issues Card
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("<h3>⚠️ Detected Concerns</h3>", unsafe_allow_html=True)
            
            for issue_obj in ai_data.get("skin_issues", []):
                severity = issue_obj.get("severity", "Mild")
                st.markdown(f"""
                <div style="border-bottom: 1px solid rgba(255,255,255,0.05); padding: 12px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong style="font-size: 1.1rem; color: #ffffff;">{issue_obj.get('issue', 'Concern')}</strong>
                        <span class="severity-badge severity-{severity}">{severity}</span>
                    </div>
                    <p style="color: #aaaaaa; font-size: 0.9rem; margin-top: 4px; margin-bottom: 0;">{issue_obj.get('description', '')}</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Doctor's Advice
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #d4af37;">
                <h3>🩺 Dermatologist Advice</h3>
                <p style="font-style: italic; color: #dddddd; line-height: 1.6; margin-bottom: 0;">"{ai_data.get('doctor_advice', '')}"</p>
            </div>
            """, unsafe_allow_html=True)

        with col_remedies:
            # Recommended Ingredients
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("<h3>💊 Recommended Active Ingredients</h3>", unsafe_allow_html=True)
            st.markdown("<p style='color: #888888; font-size:0.9rem; margin-bottom: 12px;'>Dermatologists suggest looking for these ingredients in your skincare products:</p>", unsafe_allow_html=True)
            
            for ingredient in ai_data.get("recommended_ingredients", []):
                st.markdown(f'<span class="ingredient-pill">🔬 {ingredient}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Home Remedies Card
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("<h3>🌿 Custom Home Remedies</h3>", unsafe_allow_html=True)
            st.markdown("<p style='color: #888888; font-size: 0.9rem; margin-bottom: 15px;'>Natural treatments you can prepare at home to help soothe and heal:</p>", unsafe_allow_html=True)
            
            for remedy_obj in ai_data.get("home_remedies", []):
                remedy_html = f'<div class="remedy-card">' \
                              f'<div class="remedy-title">🟢 {remedy_obj.get("remedy", "Home Remedy")}</div>' \
                              f'<p style="margin-bottom: 6px; font-size: 0.95rem;"><strong>How to apply:</strong> {remedy_obj.get("instructions", "N/A")}</p>' \
                              f'<p style="margin-bottom: 0; font-size: 0.9rem; color: #88eeaa;"><strong>Why it works:</strong> {remedy_obj.get("benefits", "N/A")}</p>' \
                              f'</div>'
                st.markdown(remedy_html, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # -------------------------
        # PRODUCT GRID SECTION
        # -------------------------
        st.markdown("---")
        st.header("🛍️ Verified Product Matches & Buy Links")
        st.write("We scanned our verified product database (`merged_products.csv`) containing thousands of safe skincare formulations. Based on active ingredients and recommended product types, here are the top matching products with direct checkout/info links:")
        
        # Render product card grid
        if matched_products:
            html_grid = '<div class="product-grid">'
            for p in matched_products:
                # Fallback image if empty
                img_url = p["image_url"] if p["image_url"] else "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?q=80&w=300&auto=format&fit=crop"
                # Clean product url
                prod_url = p["product_url"] if p["product_url"] else "#"
                # Match reason
                reason = p.get("match_reason", "Recommended Formulation")
                # Clean brand
                brand = p.get("brand", "Skincare")
                
                card_html = f'<div class="product-card">' \
                            f'<div class="product-image-container"><img src="{img_url}" class="product-image" alt="{p["product_name"]}"></div>' \
                            f'<div class="product-details">' \
                            f'<div class="product-brand">{brand}</div>' \
                            f'<div class="product-title" title="{p["product_name"]}">{p["product_name"]}</div>' \
                            f'<div class="product-reason">🎯 {reason}</div>' \
                            f'<a href="{prod_url}" target="_blank" class="product-link-btn">🛒 View Product Link</a>' \
                            f'</div></div>'
                html_grid += card_html
            html_grid += '</div>'
            st.markdown(html_grid, unsafe_allow_html=True)
        else:
            st.info("We couldn't find products containing these exact active ingredients in our database. Consider searching for generic formulations with the recommended ingredients listed above.")

else:
    st.info("👋 Upload a skin photo or capture one using your camera above to begin analysis.")