from flask import Flask, request, jsonify, render_template_string
import threading
from galaxy_bitcoin_system import GalaxyBitcoinSystem

app = Flask(__name__)

# Create a global system instance for the web UI
system = GalaxyBitcoinSystem(difficulty=2)
system.create_user_wallet('Miner')  # miner wallet exists

HTML = '''
<!doctype html>
<title>Galaxy Bitcoin System - Web Console</title>
<h1>Galaxy Bitcoin System - Web Console</h1>
<form action="/wallets/create" method="post">
  <label>New Wallet Name: <input name="name"></label>
  <button type="submit">Create Wallet</button>
</form>

<h2>Wallets</h2>
<ul>
{% for name, info in wallets.items() %}
  <li><strong>{{name}}</strong>: {{info.address}} - Balance: {{info.balance}} BTC</li>
{% endfor %}
</ul>

<h2>Create Transaction</h2>
<form action="/tx" method="post">
  <label>Sender: <input name="sender"></label><br>
  <label>Recipient: <input name="recipient"></label><br>
  <label>Amount: <input name="amount" value="1.0"></label><br>
  <button type="submit">Create TX</button>
</form>

<h2>Mine</h2>
<form action="/mine" method="post">
  <label>Miner (wallet name): <input name="miner" value="Miner"></label>
  <button type="submit">Start Mining (background)</button>
</form>
'''

@app.route('/')
def index():
    wallets = {}
    for name, w in system.system_wallets.items():
        wallets[name] = {'address': w.address, 'balance': system.blockchain.get_balance(w.address)}
    return render_template_string(HTML, wallets=wallets)

@app.route('/wallets/create', methods=['POST'])
def create_wallet():
    name = request.form.get('name')
    if not name:
        return 'Missing name', 400
    system.create_user_wallet(name)
    return ('', 302), 302, {'Location': '/'}

@app.route('/tx', methods=['POST'])
def create_tx():
    sender = request.form.get('sender')
    recipient = request.form.get('recipient')
    amount = float(request.form.get('amount') or 0)
    tx = system.create_validated_transaction(sender, recipient, amount)
    if not tx:
        return jsonify({'status': 'failed'}), 400
    system.blockchain.add_transaction(tx)
    return jsonify({'status': 'ok', 'tx_hash': tx.tx_hash})

@app.route('/mine', methods=['POST'])
def mine():
    miner = request.form.get('miner') or 'Miner'
    # Run mining in background thread to avoid blocking
    def run_mine():
        system.mine_block_with_ai(miner)
    t = threading.Thread(target=run_mine, daemon=True)
    t.start()
    return jsonify({'status': 'mining_started'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
