import streamlit as st

st.set_page_config(
    page_title="Natural Home Remedies",
    page_icon="🌿",
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
    background: linear-gradient(135deg, rgba(46, 204, 113, 0.1) 0%, rgba(40, 180, 100, 0.03) 100%);
    border: 1px solid rgba(46, 204, 113, 0.2);
    border-radius: 16px;
    padding: 30px;
    margin-bottom: 30px;
    text-align: center;
}

.banner-title {
    font-weight: 700;
    font-size: 2.5rem;
    margin-bottom: 8px;
    background: linear-gradient(135deg, #a3f5b7, #2ecc71);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.banner-sub {
    font-size: 1.1rem;
    color: #aaaaaa;
    font-weight: 300;
}

/* Remedy Card */
.remedy-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
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
    font-size: 1.25rem;
    font-weight: 600;
    color: #2ecc71;
    margin-bottom: 10px;
}

.safety-note {
    background: rgba(231, 76, 60, 0.05);
    border: 1px solid rgba(231, 76, 60, 0.15);
    border-radius: 8px;
    padding: 12px;
    margin-top: 10px;
    color: #e74c3c;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="advisor-banner">
    <div class="banner-title">🌿 Natural Skincare Remedies</div>
    <div class="banner-sub">Safe, easy-to-prepare natural home remedies for common skin concerns.</div>
</div>
""", unsafe_allow_html=True)

st.warning("⚠️ Patch Test Warning: Always perform a patch test on a small area of your skin (e.g., inner forearm) for 24 hours before applying any remedy to your face to ensure you do not have an allergic reaction.")

# Search Bar Card
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
search_query = st.text_input("🔍 Search Remedies", placeholder="Search by skin concern, ingredients, or remedy name... (e.g. Honey, Acne, Oatmeal, Aloe)")
st.markdown('</div>', unsafe_allow_html=True)

# Categorized Remedies
concerns = {
    "Acne & Blemishes": [
        {
            "name": "Tea Tree Oil Spot Application",
            "ingredients": "1-2 drops Tea Tree Essential Oil, 1 tablespoon Carrier Oil (like Jojoba Oil or Aloe Vera gel).",
            "instructions": "Mix the tea tree oil with the carrier oil. Dip a cotton swab into the mixture and gently dab it directly onto blemishes. Leave it on overnight and wash off in the morning.",
            "benefits": "Tea tree oil contains natural antibacterial and anti-inflammatory properties that help combat acne-causing bacteria and reduce swelling.",
            "safety": "Never apply pure tea tree oil directly to the skin, as it can cause severe irritation and chemical burns."
        },
        {
            "name": "Honey & Cinnamon Paste",
            "ingredients": "2 tablespoons raw organic honey, 1 teaspoon ground cinnamon.",
            "instructions": "Combine raw honey and cinnamon in a small bowl until it forms a smooth paste. Apply to face or spot-treat blemishes. Leave on for 10-15 minutes, then rinse thoroughly with warm water.",
            "benefits": "Honey is a natural humectant and antibacterial agent, while cinnamon helps improve circulation and acts as a mild anti-microbial agent.",
            "safety": "Cinnamon can cause redness/irritation on highly sensitive skin. Perform a patch test first."
        }
    ],
    "Skin Redness & Inflammation": [
        {
            "name": "Colloidal Oatmeal Mask",
            "ingredients": "2 tablespoons finely ground oat flour, 1-2 tablespoons warm water or plain yogurt.",
            "instructions": "Mix ground oatmeal with water or yogurt to form a paste. Apply a thick layer to irritated areas. Let sit for 15 minutes. Gently rinse with cool water without rubbing the skin.",
            "benefits": "Oats contain compounds called avenanthramides, which are highly anti-inflammatory, soothing itching, redness, and eczema flares.",
            "safety": "Ensure the oatmeal is unflavored and has no additives."
        },
        {
            "name": "Cool Green Tea Compress",
            "ingredients": "1-2 organic green tea bags, 1 cup hot water.",
            "instructions": "Steep tea bags in hot water for 5 minutes. Remove tea bags and let them cool down completely in the refrigerator. Place the cooled tea bags or a cotton pad soaked in the cold tea on red, irritated areas for 10 minutes.",
            "benefits": "Green tea is rich in epigallocatechin gallate (EGCG) and polyphenols, which reduce skin redness, soothe sunburns, and constrict blood vessels.",
            "safety": "Make sure the compress is fully cooled to avoid heat irritation."
        }
    ],
    "Dryness & Dehydration": [
        {
            "name": "Avocado & Honey Nourishing Mask",
            "ingredients": "1/4 ripe avocado (mashed), 1 tablespoon raw honey.",
            "instructions": "Mash the avocado until completely smooth. Stir in the honey. Spread evenly over face and neck. Leave on for 15-20 minutes. Wipe off gently with a warm, damp cloth and rinse.",
            "benefits": "Avocado is packed with healthy monounsaturated fats, Vitamin E, and fatty acids that deeply hydrate and repair the skin barrier. Honey locks in moisture.",
            "safety": "Avoid if you have known allergies to avocado."
        },
        {
            "name": "Aloe Vera & Cucumber Soother",
            "ingredients": "2 tablespoons fresh Aloe Vera Gel, 2 tablespoons Cucumber Juice (grated and strained).",
            "instructions": "Mix fresh aloe vera gel with cucumber juice. Apply to clean skin as a refreshing mask. Leave on for 15 minutes, then rinse off with cool water.",
            "benefits": "Cucumber has high water content and cooling enzymes, while Aloe Vera is renowned for cell regeneration and deep hydration.",
            "safety": "For best results, extract aloe fresh from the plant, or use pure commercial gel without added alcohols."
        }
    ],
    "Dark Spots & Pigmentation": [
        {
            "name": "Turmeric & Yogurt Brightener",
            "ingredients": "1/2 teaspoon organic turmeric powder, 1 tablespoon plain Greek yogurt, 1/2 teaspoon honey.",
            "instructions": "Mix turmeric, yogurt, and honey thoroughly. Apply to hyperpigmented areas or full face. Leave on for 10-12 minutes. Rinse off with lukewarm water. (Note: Turmeric may temporarily stain skin yellow, which can be wiped off with a cotton pad dipped in milk).",
            "benefits": "Turmeric contains curcumin, which inhibits melanin production and brightens skin tone. Yogurt has lactic acid (a gentle AHA) that exfoliates dead skin cells.",
            "safety": "Do not leave turmeric on for too long to avoid strong yellow staining. Lactic acid increases sun sensitivity; always wear sunscreen."
        }
    ]
}

# Filter remedies based on search query
filtered_concerns = {}

if search_query:
    query = search_query.lower().strip()
    for concern, remedies in concerns.items():
        matching_remedies = []
        for r in remedies:
            if query in concern.lower() or \
               query in r["name"].lower() or \
               query in r["ingredients"].lower() or \
               query in r["instructions"].lower() or \
               query in r["benefits"].lower():
                matching_remedies.append(r)
        if matching_remedies:
            filtered_concerns[concern] = matching_remedies
else:
    filtered_concerns = concerns

# Render filtered remedies
if filtered_concerns:
    for concern, remedies in filtered_concerns.items():
        st.markdown(f'<div class="glass-card">', unsafe_allow_html=True)
        st.subheader(concern)
        
        for r in remedies:
            remedy_html = f'<div class="remedy-card">' \
                          f'<div class="remedy-title">🌿 {r["name"]}</div>' \
                          f'<p style="margin-bottom: 6px; font-size: 0.95rem;"><strong>Ingredients:</strong> {r["ingredients"]}</p>' \
                          f'<p style="margin-bottom: 6px; font-size: 0.95rem;"><strong>Directions:</strong> {r["instructions"]}</p>' \
                          f'<p style="margin-bottom: 6px; font-size: 0.95rem; color: #88eeaa;"><strong>Why it helps:</strong> {r["benefits"]}</p>' \
                          f'<div class="safety-note">⚠️ <strong>Caution:</strong> {r["safety"]}</div>' \
                          f'</div>'
            st.markdown(remedy_html, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("🔍 No remedies found matching your search. Try searching for other terms like 'Honey', 'Acne', 'Oatmeal', 'Aloe', or 'Redness'.")
