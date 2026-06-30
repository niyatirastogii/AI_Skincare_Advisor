import pandas as pd
import streamlit as st
import re
import os

@st.cache_data
def load_product_database():
    """
    Loads and caches the merged product database from merged_products.csv.
    """
    csv_path = "merged_products.csv"
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            df = df.fillna("")
            return df
        except Exception as e:
            st.error(f"Error loading database: {e}")
            return pd.DataFrame()
    else:
        # Fallback to local products.csv if merged_products.csv doesn't exist
        fallback_path = "products.csv"
        if os.path.exists(fallback_path):
            try:
                df = pd.read_csv(fallback_path)
                # Map column names if different
                df = df.rename(columns={
                    "Product": "product_name",
                    "SkinType": "usage_type",
                    "Price": "price"
                })
                # Add default columns for compat
                for col in ["brand", "category", "ingredients", "image_url", "product_url"]:
                    if col not in df.columns:
                        df[col] = ""
                df = df.fillna("")
                return df
            except Exception as e:
                st.error(f"Error loading fallback database: {e}")
                return pd.DataFrame()
        st.warning("Product database files not found.")
        return pd.DataFrame()

def search_products_by_name(product_names, limit=3):
    """
    Search products in the database by their recommended names.
    Returns a list of matched product records.
    """
    df = load_product_database()
    if df.empty or not product_names:
        return []
    
    results = []
    seen_products = set()
    
    for name_query in product_names:
        if not name_query or len(name_query.strip()) < 3:
            continue
        
        # Tokenize query for word overlap
        query_words = set(re.findall(r'\w+', name_query.lower()))
        # Remove small/common words
        query_words = {w for w in query_words if len(w) > 2 and w not in ["the", "and", "for", "with", "gel", "cream", "skin", "face"]}
        if not query_words:
            continue
            
        # Fast pre-filtering: find products that contain at least one of the query keywords
        pattern = "|".join([re.escape(w) for w in query_words])
        sub_df = df[df['product_name'].str.lower().str.contains(pattern, na=False, regex=True)]
        
        matches = []
        for idx, row in sub_df.iterrows():
            prod_name = str(row['product_name']).lower()
            prod_words = set(re.findall(r'\w+', prod_name))
            
            overlap = len(query_words.intersection(prod_words))
            if overlap > 0:
                score = overlap / len(query_words.union(prod_words))
                matches.append((score, row))
                
        # Sort by match score
        matches.sort(key=lambda x: x[0], reverse=True)
        
        count = 0
        for score, row in matches:
            p_name = row['product_name']
            if p_name in seen_products:
                continue
            if score > 0.15:  # Relevance threshold
                results.append({
                    "product_name": row['product_name'],
                    "brand": row.get('brand', 'N/A'),
                    "usage_type": row.get('usage_type', 'N/A'),
                    "category": row.get('category', 'N/A'),
                    "ingredients": row.get('ingredients', ''),
                    "image_url": row.get('image_url', ''),
                    "product_url": row.get('product_url', ''),
                    "match_reason": f"Matches recommended product '{name_query}'",
                    "match_type": "name"
                })
                seen_products.add(p_name)
                count += 1
                if count >= limit:
                    break
                    
    return results

def get_products_by_ingredients(ingredients, skin_type=None, limit_per_ingredient=2):
    """
    Search products that contain recommended ingredients.
    """
    df = load_product_database()
    if df.empty or not ingredients:
        return []
        
    results = []
    seen_products = set()
    
    for ing in ingredients:
        if not ing or len(ing.strip()) < 3:
            continue
        
        # Word boundary search for ingredient name
        ing_clean = ing.strip().lower()
        pattern = r'\b' + re.escape(ing_clean) + r'\b'
        
        # Filter matching rows
        mask = df['ingredients'].str.lower().str.contains(pattern, na=False, regex=True)
        matched_df = df[mask]
        
        # If skin_type is provided, prioritize matching products
        if skin_type and 'usage_type' in df.columns:
            # Simple soft match for skin type in usage_type or product name
            st_pattern = re.escape(skin_type.lower())
            type_mask = matched_df['usage_type'].str.lower().str.contains(st_pattern, na=False) | \
                        matched_df['product_name'].str.lower().str.contains(st_pattern, na=False)
            
            # Prioritize type-matched items by concatenating them first
            matched_df = pd.concat([matched_df[type_mask], matched_df[~type_mask]])
            
        count = 0
        for idx, row in matched_df.iterrows():
            prod_name = row['product_name']
            if prod_name in seen_products:
                continue
                
            results.append({
                "product_name": row['product_name'],
                "brand": row.get('brand', 'N/A'),
                "usage_type": row.get('usage_type', 'N/A'),
                "category": row.get('category', 'N/A'),
                "ingredients": row.get('ingredients', ''),
                "image_url": row.get('image_url', ''),
                "product_url": row.get('product_url', ''),
                "match_reason": f"Contains active ingredient: {ing}",
                "match_type": "ingredient"
            })
            seen_products.add(prod_name)
            count += 1
            if count >= limit_per_ingredient:
                break
                
    return results
