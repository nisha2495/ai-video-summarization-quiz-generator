import streamlit as st
import random
import re

st.set_page_config(page_title="Smart Study Buddy - Unique Project", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .main { background-color: #F8F9FA; }
    .title { text-align: center; color: #6A1B9A; font-size: 40px; font-weight: bold; }
    .subtitle { text-align: center; color: #555; font-size: 17px; }
    .card { background-color: white; padding: 25px; border-radius: 15px; border: 2px solid #6A1B9A; text-align: center; font-size: 20px; margin: 10px; }
    .stButton>button { background-color: #6A1B9A; color: white; border-radius: 10px; width: 100%; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🧠 Smart Study Buddy</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ek App, Teen Kaam - Quiz + Flashcards + Key Points</div>', unsafe_allow_html=True)
st.markdown("---")

summary = st.text_area("📝 Video ka Summary Yahan Likhein:", height=150, placeholder="Example: Python ek popular language hai. Ise Guido ne 1991 me banaya. Python AI or Websites me use hota hai...")
num_q = st.slider("Kitne MCQs chahiye?", 5, 50, 10)

if st.button("✨ Smart Study Material Banayein"):
    if not summary.strip():
        st.warning("Pehle summary likhein.")
    else:
        sentences = re.split(r'[.\n]', summary)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 15]
        words = list(set(re.findall(r'\b[A-Z][a-z]+\b|\b\d{4}\b|\b[A-Za-z]{5,}\b', summary)))
        if len(words) < 4: words += ["Python", "Computer", "Data"]

        questions = []
        flashcards = []
        idx, tries = 0, 0
        while len(questions) < num_q and tries < 600:
            tries += 1
            s = sentences[idx % len(sentences)]; idx += 1
            cand = [w for w in s.split() if len(w) > 3]
            if not cand: continue
            target = random.choice(cand); clean = target.strip(",.()")
            q_text = s.replace(target, "_____", 1)
            if q_text.lower() in [q['q'].lower() for q in questions]: continue
            wrongs = list(dict.fromkeys([w for w in words if w.lower() != clean.lower()]))[:3]
            opts = [clean] + wrongs; random.shuffle(opts)
            questions.append({"q": q_text, "opts": opts, "correct": clean})
            flashcards.append({"front": f"Blank me kya aayega?\n\n{q_text}", "back": clean})

        st.session_state['qs'] = questions
        st.session_state['cards'] = flashcards
        st.session_state['points'] = sentences
        st.success("Ho Gaya! Tumhara UNIQUE Study Material Tayyar Hai!")
        st.balloons()

if 'qs' in st.session_state:
    tab1, tab2, tab3 = st.tabs(["📚 QUIZ", "🃏 FLASHCARDS", "⭐ KEY POINTS"])

    with tab1:
        st.write(f"### Total MCQs: {len(st.session_state['qs'])}")
        for i, qq in enumerate(st.session_state['qs']):
            st.markdown(f"**Q{i+1}. {qq['q']}**")
            ans = st.radio(f"Q{i+1}", qq['opts'], key=f"q{i}", label_visibility="collapsed")
            st.session_state[f"a{i}"] = ans
            st.write("---")
        if st.button("Result Dekhein"):
            total = sum(1 for i, qq in enumerate(st.session_state['qs']) if str(st.session_state.get(f"a{i}")).strip() == str(qq['correct']).strip())
            st.success(f"Aapka Score: {total} / {len(st.session_state['qs'])}")

    with tab2:
        st.write("### Flashcards - Click kar ke Jawab Dekhein")
        st.write("Ye tareeka Topper use karte hain yaad karne ke liye!")
        for i, card in enumerate(st.session_state['cards'][:10]):
            with st.expander(f"Card {i+1}: {card['front'][:50]}..."):
                st.markdown(f'<div class="card">💡 Jawab: <b>{card["back"]}</b></div>', unsafe_allow_html=True)

    with tab3:
        st.write("### Summary ke Sab Se Important Points")
        for p in st.session_state['points']:
            st.write(f"✅ {p}")