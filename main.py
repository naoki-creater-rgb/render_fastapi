from typing import Optional
import random
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

latest_omikuji_result = {
    "result": "まだ引かれていません",
    "summary": ""
}

class OmikujiRecord(BaseModel):
    result: str
    summary: str


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

# おみくじをランダムに生成するエンドポイント
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


@app.put("/omikuji/latest")
async def update_latest_omikuji(data: OmikujiRecord):
    global latest_omikuji_result
    latest_omikuji_result["result"] = data.result
    latest_omikuji_result["summary"] = data.summary
    return {"message": "結果を記録しました", "recorded": latest_omikuji_result}


@app.get("/omikuji/latest")
async def get_latest_omikuji():
    return latest_omikuji_result


@app.get("/index")
def index():
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>FastAPI おみくじ履歴システム</title>
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
                button:hover {
                    background-color: #4cae4c;
                }
                .history-card {
                    background: #e9ecef;
                    border: 1px dashed #ccc;
                }
                .history-result {
                    font-size: 1.3rem;
                    font-weight: bold;
                    color: #2e6da4;
                    margin-top: 10px;
                }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>今日の運勢は？</h1>
                <div id="omikuji-result" class="result-box">？？？</div>
                <div id="omikuji-summary"></div>
                <br>
                <button onclick="drawAndRecordOmikuji()">おみくじを引く</button>
            </div>

            <div class="card history-card">
                <h3>サーバーに記録された最新データ</h3>
                <div id="server-recorded-result" class="history-result">確認中...</div>
                <div id="server-recorded-summary" style="font-size: 0.9rem; color: #555;"></div>
            </div>

            <script>
                // ページが読み込まれた時に、サーバーに保存されている現在の最新結果を表示する
                window.onload = async function() {
                    fetchLatestRecord();
                };

                // サーバーから最新の記録を取得して画面に表示する関数
                async function fetchLatestRecord() {
                    try {
                        const response = await fetch('/omikuji/latest');
                        const data = await response.json();
                        document.getElementById('server-recorded-result').innerText = data.result;
                        document.getElementById('server-recorded-summary').innerText = data.summary;
                    } catch (error) {
                        console.error('記録の取得に失敗:', error);
                    }
                }

                // ★おみくじを引き、その結果をPUTでサーバーに送る関数
                async function drawAndRecordOmikuji() {
                    try {
                        // 1. まず普通におみくじを引く (GET)
                        const response = await fetch('/omikuji');
                        const data = await response.json();
                        
                        // 画面上のメイン表示を更新
                        document.getElementById('omikuji-result').innerText = data.result;
                        document.getElementById('omikuji-summary').innerText = data.summary;

                        // 2. 出た結果をPUTメソッドでサーバーに送り、記録を更新する (PUT)
                        const putResponse = await fetch('/omikuji/latest', {
                            method: 'PUT',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                result: data.result,
                                summary: data.summary
                            })
                        });
                        
                        const putData = await putResponse.json();
                        console.log('サーバーの応答:', putData.message);

                        // 3. サーバー側の記録が更新されたので、下の「最新データ表示」も更新する
                        fetchLatestRecord();

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