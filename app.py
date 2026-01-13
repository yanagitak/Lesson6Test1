# app.py
# 標準ライブラリのみで動く最小BMI計算Webアプリ（Render対応）

import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <title>BMI計算機</title>
  <style>
    body {{ font-family: sans-serif; background: #f5f5f5; }}
    .card {{ max-width: 420px; margin: 40px auto; padding: 20px;
              background: #fff; border-radius: 8px; }}
    label {{ display: block; margin-top: 12px; }}
    input {{ width: 100%; padding: 8px; margin-top: 4px; }}
    button {{ margin-top: 16px; padding: 10px; width: 48%; }}
    .row {{ display: flex; justify-content: space-between; }}
    .result {{ margin-top: 20px; font-weight: bold; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>BMI計算機</h1>
    <form method="post">
      <label>身長（cm）
        <input type="number" step="0.1" name="height" value="{height}">
      </label>
      <label>体重（kg）
        <input type="number" step="0.1" name="weight" value="{weight}">
      </label>
      <div class="row">
        <button type="submit">計算</button>
        <button type="button" onclick="clearForm()">クリア</button>
      </div>
    </form>
    <div class="result">{result}</div>
  </div>
  <script>
    function clearForm() {{
      document.querySelector('input[name="height"]').value = '';
      document.querySelector('input[name="weight"]').value = '';
      document.querySelector('.result').innerText = '';
    }}
  </script>
</body>
</html>
"""

def calc_bmi(height_cm, weight_kg):
    try:
        h = float(height_cm) / 100.0
        w = float(weight_kg)
        if h <= 0:
            return None, ""
        bmi = w / (h * h)
    except Exception:
        return None, ""
    if bmi < 18.5:
        judge = "低体重"
    elif bmi < 25:
        judge = "普通体重"
    elif bmi < 30:
        judge = "肥満（1度）"
    else:
        judge = "肥満（2度以上）"
    return bmi, judge

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.respond("", "", "")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        data = parse_qs(body)
        height = data.get("height", [""])[0]
        weight = data.get("weight", [""])[0]

        bmi, judge = calc_bmi(height, weight)
        if bmi is None:
            result = "数値を正しく入力してください"
        else:
            result = f"BMI: {bmi:.2f} / 判定: {judge}"

        self.respond(height, weight, result)

    def respond(self, height, weight, result):
        html = HTML.format(height=height, weight=weight, result=result)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"Listening on port {port}")
    server.serve_forever()
