from typing import Optional

from fastapi import FastAPI

from fastapi.responses import HTMLResponse

import random  # randomライブラリを追加

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/omikuji")
def omikuji():
    omikuji_list = {
        "大吉":  "大吉！素晴らしい幸運が舞い込むでしょう。",
        "中吉": "中吉！努力が実を結び、良い結果が待っています。",
        "小吉": "小吉！ちょっとした幸運があなたの元にやってきます",
        "吉": "吉！安定した幸せな日々が続くでしょう。",
        "末吉": "末吉！努力が実り始め、良い方向に進む時期です。",
        "凶": "凶。悪いことが起こるかもしれませんが、気を引き締めてください。",
        "小凶": "小凶。注意が必要な日です。慎重に行動しましょう。",
        "大凶": "凶。悪いことが起こるかもしれませんが、気を引き締めてください。"
    }

    lucky_result = random.choice(list(omikuji_list.keys()))
    summary = omikuji_list[lucky_result]

    return {"result": omikuji_list[random.randrange(10)], "summary": summary}

@app.get("/index")
def index():
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>FastAPI おみくじ</title>
            <style>
                body {
                    font-family: 'Helvetica Neue', Arial, sans-serif;
                    text-align: center;
                    background-color: #f7f7f7;
                    padding-top: 50px;
                }
                .card {
                    background: white;
                    max-width: 400px;
                    margin: 0 auto;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                }
                h1 { color: #333; }
                .result-box {
                    font-size: 2.5rem;
                    font-weight: bold;
                    color: #d9534f;
                    margin: 30px 0;
                    min-height: 60px;
                }
                button {
                    background-color: #5cb85c;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    font-size: 1.2rem;
                    border-radius: 5px;
                    cursor: pointer;
                    transition: background 0.2s;
                }
                button:hover {
                    background-color: #4cae4c;
                }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>今日の運勢は？</h1>
                <div id="omikuji-result" class="result-box">？？？</div>
                <div id="omikuji-summary"></div>
                <button onclick="drawOmikuji()">おみくじを引く</button>
            </div>

            <script>
                async function drawOmikuji() {
                    try {
                        const response = await fetch('/omikuji');
                        const data = await response.json();
                        
                        document.getElementById('omikuji-result').innerText = data.result;
                        document.getElementById('omikuji-summary').innerText = data.summary;
                    } catch (error) {
                        console.error('エラーが発生しました:', error);
                        document.getElementById('omikuji-result').innerText = 'エラー発生';
                    }
                }
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/present")
async def give_present(present):
    return {"response": f"サーバです。メリークリスマス！ {present}ありがとう。お返しはキャンディーです。"}  # f文字列というPythonの機能を使っている