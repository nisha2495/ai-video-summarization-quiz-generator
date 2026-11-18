from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = """
<style>
body{font-family:Arial;background:#1a0b2e;color:white;text-align:center;padding:20px}
.box{background:white;color:black;max-width:700px;margin:auto;padding:25px;border-radius:20px;box-shadow:0 0 20px #a855f7}
textarea{width:95%;padding:12px;border-radius:10px;border:2px solid #a855f7;font-size:15px}
button{background:#7c3aed;color:white;padding:12px 25px;border:none;border-radius:10px;font-size:17px;font-weight:bold;cursor:pointer}
h2{color:#facc15;font-size:28px}
.card{background:#f3e8ff;padding:15px;border-radius:12px;text-align:left;margin-top:15px}
</style>
<h2>🎬 AI Video Summarization + Quiz Generator</h2>
<div class="box">
<form method="POST">
<textarea name="text" rows="6" placeholder="Yahan Video ka Text paste karo..."></textarea><br><br>
<button type="submit">✨ Summary + Quiz Banao</button>
</form>
{% if summary %}
<div class="card"><h3>📝 Summary:</h3><p>{{ summary }}</p></div>
<div class="card"><h3>❓ Quiz:</h3>
<p><b>1. Is video ka main topic kya hai?</b><br>A) {{ q1_a }}<br>B) Kuch nahi<br>C) Sirf intro<br><b>Answer: A</b></p>
<p><b>2. Video me sab se important baat kya thi?</b><br>A) Intro<br>B) {{ q2_b }}<br>C) Outro<br><b>Answer: B</b></p>
</div>
{% endif %}
</div>
<p style="color:#c4b5fd">Made with Python + Flask</p>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    summary = None
    q1_a = q2_b = ""
    if request.method == "POST":
        text = request.form["text"]
        sentences = text.split(".")
        summary = ". ".join(sentences[:3]) + "."
        words = summary.split()
        q1_a = " ".join(words[:5])
        q2_b = " ".join(words[5:12])
    return render_template_string(HTML, summary=summary, q1_a=q1_a, q2_b=q2_b)

if __name__ == "__main__":
    app.run(debug=True)