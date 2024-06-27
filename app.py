from flask import Flask, request, render_template, redirect, url_for, flash
from crypto import generate_key, encrypt_message, decrypt_message
from twilio.rest import Client

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Twilio configuration (replace with your actual Twilio credentials)
TWILIO_ACCOUNT_SID = 'AC79fb3c180a32f8cae1c2741b8fa15b14'
TWILIO_AUTH_TOKEN = 'd9d280b75f254ce6c1abbcac494f840a'
TWILIO_PHONE_NUMBER = '+16186176561'
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    phone_number = request.form['phone_number']
    message = request.form['message']
    
    # Generate a new AES key for this request
    key = generate_key()
    
    # Encrypt the message
    encrypted_message = encrypt_message(key, message)
    
    # Send the encrypted message via SMS along with the key
    client.messages.create(
        body=f"Encrypted Message:\n{encrypted_message}\n\n Key:\n{key.hex()}",
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    
    flash('Message sent successfully!')
    return redirect(url_for('index'))

@app.route('/decrypt', methods=['POST'])
def decrypt():
    encrypted_message = request.form['encrypted_message']
    decryption_key = request.form['decryption_key']

    print(f"Received decryption key: {decryption_key}")
    print(f"Received encrypted message: {encrypted_message}")
    
    try:
        key = bytes.fromhex(decryption_key)
        # Decrypt the message using the provided key
        decrypted_message = decrypt_message(key, encrypted_message)
        flash(f'Decrypted message: {decrypted_message}')
        return render_template('index.html', decrypted_message=decrypted_message)

    except Exception as e:
        flash('Failed to decrypt message. Please check the encrypted text and try again.')
        print(f"Decryption error: {str(e)}")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
