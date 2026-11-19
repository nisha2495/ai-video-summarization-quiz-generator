from flask import Flask, request
import random

app = Flask(__name__)

# HOME PAGE - Yahi Quiz Wala Page Hai
@app.route('/')
def home():
    return '''
    <html><head><title>Quiz Generator</title></head>
    <body style="font-family:Arial; padding:20px; max-width:700px; margin:auto;">
    <h1>🎥 AI Video Quiz Generator</h1>
    <p>Video ka text paste karo, 50 MCQs wala quiz banao!</p>
    <form action="/generate" method="post">
        <label><b>Video Text Paste Karo:</b></label><br>
        <textarea name="text" rows="8" style="width:100%" placeholder="Yahan video ka text paste karo..." required></textarea><br><br>

        <label><b>Level Choose Karo:</b></label><br>
        <select name="level" style="padding:8px; width:100%">
            <option>Mix</option>
            <option>Easy</option>
            <option>Medium</option>
            <option>Hard</option>
        </select><br><br>

        <label><b>Kitne MCQs Chahiye?</b></label><br>
        <select name="num_q" style="padding:8px; width:100%">
            <option value="10">10 MCQs</option>
            <option value="25">25 MCQs</option>
            <option value="50" selected>50 MCQs</option>
        </select><br><br>

        <button style="padding:12px 20px; background:blue; color:white; border:none; cursor:pointer;">Generate Summary & Quiz</button>
    </form>
    </body></html>
    '''

@app.route('/generate', methods=['POST'])
def generate():
    text = request.form.get('text', '')
    level = request.form.get('level', 'Mix')
    num_q = int(request.form.get('num_q', 50))

    sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 50]
    if not sentences:
        sentences = ["Is topic ka main idea"]
    summary = ". ".join(sentences[:3]) + "."

    # Quiz HTML banao
    quiz_html = ""
    for i in range(1, num_q + 1):
        line = sentences[i % len(sentences)]
        quiz_html += f'''
        <div style="border:1px solid #ccc; padding:10px; margin:10px 0;">
        <p><b>Q{i}. {line[:90]}... se kya seekha? (Level: {level})</b></p>
        <input type="radio" name="q{i}" value="0"> A) Is ka ulta hai<br>
        <input type="radio" name="q{i}" value="1"> B) Is se related nahi hai<br>
        <input type="radio" name="q{i}" value="2"> C) Thora sa sahi hai<br>
        <input type="radio" name="q{i}" value="3"> D) {line[:40]} sahi hai<br>
        </div>
        '''

    return f'''
    <html><body style="font-family:Arial; padding:20px; max-width:700px; margin:auto;">
    <h2>📝 Summary</h2><p>{summary}</p>
    <h2>Quiz - {num_q} MCQs - Level: {level}</h2>
    <h3>Time Left: <span id="timer">10:00</span></h3>
    <form id="quizForm">{quiz_html}
    <button type="button" onclick="checkScore()" style="padding:12px 20px; background:green; color:white; border:none;">Submit & Check Score</button>
    </form>
    <h2 id="score"></h2>
    <a href="/">Wapis Jao</a>
    <script>
    let time = 600;
    setInterval(()=>{{
        let m = Math.floor(time/60); let s = time%60;
        document.getElementById('timer').innerText = m+":"+(s<10?"0"+s:s);
        time--; if(time<0) checkScore();
    }},1000);
    function checkScore(){{
        let correct=0;
        for(let i=1;i<={num_q};i++){{
            let ans=document.querySelector('input[name="q'+i+'"]:checked');
            if(ans && ans.value=="3") correct++;
        }}
        let msg = "Your Score: "+correct+" / {num_q} - " + (correct>25 ? "Excellent! 🎉" : correct>10 ? "Good! 👍" : "Try Again! 💪");
        document.getElementById('score').innerText = msg;
        alert(msg);
    }}
    </script>
    </body></html>
    '''

if __name__ == '__main__':
    app.run(debug=True)