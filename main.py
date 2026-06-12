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
    omikuji_list = [
        "大吉",
        "中吉",
        "小吉",
        "吉",
        "半吉",
        "末吉",
        "末小吉",
        "凶",
        "小凶",
        "大凶"
    ]

    return {"result": omikuji_list[random.randrange(10)]}

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
                <button onclick="drawOmikuji()">おみくじを引く</button>
            </div>

            <script>
                async function drawOmikuji() {
                    try {
                        const response = await fetch('/omikuji');
                        const data = await response.json();
                        
                        document.getElementById('omikuji-result').innerText = data.result;
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