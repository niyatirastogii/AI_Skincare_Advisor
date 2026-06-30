import streamlit as st
import pandas as pd
import re
from modules.database import load_product_database

st.set_page_config(
    page_title="Product Recommendations",
    page_icon="🧴",
    layout="wide"
)

# Inject Premium CSS Styles
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

.main .block-container, p, span, div, h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif !important;
}

.glass-card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(12px);
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
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="advisor-banner">
    <div class="banner-title">🧴 Skincare Product Database</div>
    <div class="banner-sub">Search and filter safe skincare formulations from our database of thousands of products.</div>
</div>
""", unsafe_allow_html=True)

# Load Database
df = load_product_database()

if not df.empty:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    # Search and Filter Layout
    col_search, col_brand, col_category = st.columns([2, 1, 1])
    
    with col_search:
        search_query = st.text_input("🔍 Search by Product Name or Ingredient", placeholder="e.g. Cleanser, Niacinamide, CeraVe...")
        
    with col_brand:
        # Get unique brands
        brands = ["All Brands"] + sorted([b for b in list(df['brand'].unique()) if b])
        selected_brand = st.selectbox("Filter by Brand", brands)
        
    with col_category:
        categories = ["All Categories"] + sorted([c for c in list(df['category'].unique()) if c])
        selected_category = st.selectbox("Filter by Category", categories)
    st.markdown('</div>', unsafe_allow_html=True)
        
    # Filtering Dataframe
    filtered_df = df.copy()
    
    if search_query:
        query = search_query.lower()
        filtered_df = filtered_df[
            filtered_df['product_name'].str.lower().str.contains(query, na=False) |
            filtered_df['ingredients'].str.lower().str.contains(query, na=False) |
            filtered_df['brand'].str.lower().str.contains(query, na=False)
        ]
        
    if selected_brand != "All Brands":
        filtered_df = filtered_df[filtered_df['brand'] == selected_brand]
        
    if selected_category != "All Categories":
        filtered_df = filtered_df[filtered_df['category'] == selected_category]
        
    # Display product count
    st.write(f"Showing **{len(filtered_df)}** matching products")
    
    # Limit output length to prevent overloading browser (show top 24)
    limit = 24
    display_df = filtered_df.head(limit)
    
    if not display_df.empty:
        html_grid = '<div class="product-grid">'
        for idx, row in display_df.iterrows():
            img_url = row["image_url"] if row["image_url"] else "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?q=80&w=300&auto=format&fit=crop"
            prod_url = row["product_url"] if row["product_url"] else "#"
            brand = row.get("brand", "Skincare")
            category = row.get("category", "General")
            
            card_html = f'<div class="product-card">' \
                        f'<div class="product-image-container"><img src="{img_url}" class="product-image" alt="{row["product_name"]}"></div>' \
                        f'<div class="product-details">' \
                        f'<div class="product-brand">{brand}</div>' \
                        f'<div class="product-title" title="{row["product_name"]}">{row["product_name"]}</div>' \
                        f'<div class="product-reason">🎯 Category: {category}</div>' \
                        f'<a href="{prod_url}" target="_blank" class="product-link-btn">🛒 View Product Link</a>' \
                        f'</div></div>'
            html_grid += card_html
        html_grid += '</div>'
        st.markdown(html_grid, unsafe_allow_html=True)
        
        if len(filtered_df) > limit:
            st.info(f"Showing the first {limit} matches. Refine your search to find specific items.")
    else:
        st.info("No matching products found. Try using different keywords.")
else:
    st.error("Unable to load product database.")
