from typing import Optional
import random
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

omikuji_counters = {
    "大吉": 0, "中吉": 0, "小吉": 0, "吉": 0,
    "末吉": 0, "凶": 0, "小凶": 0, "大凶": 0
}

class OmikujiCountRequest(BaseModel):
    result: str


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/omikuji")
def omikuji():
    omikuji_list = {
        "大吉": "大吉！素晴らしい幸運が舞い込むでしょう。",
        "中吉": "中吉！努力が実を結び、良い結果が待っています。",
        "小吉": "小吉！ちょっとした幸運があなたの元にやってきます",
        "吉": "吉！安定した幸せな日々が続くでしょう。",
        "末吉": "末吉！努力が実り始め、良い方向に進む時期です。",
        "凶": "凶。悪いことが起こるかもしれませんが、気を引き締めてください。",
        "小凶": "小凶。注意が必要な日です。慎重に行動しましょう。",
        "大凶": "大凶。最悪な日かもしれませんが、これ以上下がることはありません。"
    }
    lucky_result = random.choice(list(omikuji_list.keys()))
    summary = omikuji_list[lucky_result]
    return {"result": lucky_result, "summary": summary}

@app.put("/omikuji/count")
async def increment_omikuji_count(data: OmikujiCountRequest):
    global omikuji_counters
    if data.result in omikuji_counters:
        omikuji_counters[data.result] += 1
        return {"status": "success", "counters": omikuji_counters}
    return {"status": "error", "message": "無効な結果です"}

@app.get("/omikuji/stats")
async def get_omikuji_stats():
    return omikuji_counters

@app.get("/index")
def index():
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>FastAPI おみくじ集計システム</title>
            <style>
                body {
                    font-family: 'Helvetica Neue', Arial, sans-serif;
                    text-align: center;
                    background-color: #f7f7f7;
                    padding-top: 30px;
                }
                .card {
                    background: white;
                    max-width: 400px;
                    margin: 0 auto 20px auto;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                }
                h1 { color: #333; font-size: 1.5rem; }
                .result-box {
                    font-size: 2.5rem;
                    font-weight: bold;
                    color: #d9534f;
                    margin: 20px 0;
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
                button:hover { background-color: #4cae4c; }
                .stats-card { background: #fff; max-width: 450px; }
                .stats-table { width: 100%; margin-top: 15px; border-collapse: collapse; }
                .stats-table th, .stats-table td { border: 1px solid #ddd; padding: 10px; text-align: center; }
                .stats-table th { background-color: #f2f2f2; font-weight: bold; }
                .count-num { font-weight: bold; color: #2e6da4; }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>🔮 今日の運勢は？</h1>
                <div id="omikuji-result" class="result-box">？？？</div>
                <div id="omikuji-summary"></div>
                <br>
                <button onclick="drawAndCountOmikuji()">おみくじを引く</button>
            </div>

            <div class="card stats-card">
                <h3>📊 これまでの出現回数（集計結果）</h3>
                <table class="stats-table">
                    <thead>
                        <tr><th>大吉</th><th>中吉</th><th>小吉</th><th>吉</th></tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td id="count-大吉" class="count-num">0 回</td>
                            <td id="count-中吉" class="count-num">0 回</td>
                            <td id="count-小吉" class="count-num">0 回</td>
                            <td id="count-吉" class="count-num">0 回</td>
                        </tr>
                    </tbody>
                    <thead>
                        <tr><th>末吉</th><th>凶</th><th>小凶</th><th>大凶</th></tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td id="count-末吉" class="count-num">0 回</td>
                            <td id="count-凶" class="count-num">0 回</td>
                            <td id="count-小凶" class="count-num">0 回</td>
                            <td id="count-大凶" class="count-num">0 回</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <script>
                window.onload = function() {
                    updateStatsResult();
                };

                async function updateStatsResult() {
                    try {
                        const response = await fetch('/omikuji/stats');
                        const stats = await response.json();
                        for (const key in stats) {
                            const element = document.getElementById('count-' + key);
                            if (element) {
                                element.innerText = stats[key] + " 回";
                            }
                        }
                    } catch (error) {
                        console.error('集計データの取得エラー:', error);
                    }
                }

                async function drawAndCountOmikuji() {
                    try {
                        const response = await fetch('/omikuji');
                        const data = await response.json();
                        
                        document.getElementById('omikuji-result').innerText = data.result;
                        document.getElementById('omikuji-summary').innerText = data.summary;

                        await fetch('/omikuji/count', {
                            method: 'PUT',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                result: data.result  
                            })
                        });
                        
                        updateStatsResult();

                    } catch (error) {
                        console.error('通信エラー:', error);
                    }
                }
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)