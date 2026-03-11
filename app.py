from flask import Flask, render_template, request, session
from cipher.caesar import CaesarCipher

app = Flask(__name__)
app.secret_key = 'hutech2024'

#router routes for home page
@app.route("/")
def home():
    return render_template('index.html')

#router routes for caesar cypher
@app.route("/caesar")
def caesar():
    return render_template('caesar.html',
        enc_text='', enc_key='',
        dec_text='', dec_key='',
        encrypted_result=None, decrypted_result=None)

@app.route("/encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    Caesar = CaesarCipher()
    encrypted_text = Caesar.encrypt_text(text, key)
    # Giữ nguyên phần decrypt từ session
    dec_text = session.get('dec_text', '')
    dec_key = session.get('dec_key', '')
    dec_result = session.get('dec_result', None)
    # Lưu encrypt vào session
    session['enc_text'] = text
    session['enc_key'] = key
    return render_template('caesar.html',
        enc_text=text, enc_key=key,
        dec_text=dec_text, dec_key=dec_key,
        encrypted_result={'text': text, 'key': key, 'output': encrypted_text},
        decrypted_result=dec_result)

@app.route("/decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    Caesar = CaesarCipher()
    decrypted_text = Caesar.decrypt_text(text, key)
    # Giữ nguyên phần encrypt từ session
    enc_text = session.get('enc_text', '')
    enc_key = session.get('enc_key', '')
    enc_result = session.get('enc_result', None)
    # Lưu decrypt vào session
    session['dec_text'] = text
    session['dec_key'] = key
    return render_template('caesar.html',
        enc_text=enc_text, enc_key=enc_key,
        dec_text=text, dec_key=key,
        encrypted_result=enc_result,
        decrypted_result={'text': text, 'key': key, 'output': decrypted_text})

#main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
