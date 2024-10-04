from flask import Flask, request, jsonify
from ports import PORT_SERVER
from colorama import Fore, Style, Back
import os
from blockchain import BlockChain

app = Flask(__name__)

# Inicializa a blockchain
blockchain = BlockChain()

@app.route('/')
def index():
    return "Welcome to the BM Server"

@app.route('/valid', methods=['POST'])
def valid():
    return ""

@app.route('/signup', methods=['POST'])
def create_account():
    account = blockchain.create_account()
    return jsonify(account)

@app.route('/block', methods=['GET'])
def get_blocks():
    blocks = blockchain.get_blocks()
    return jsonify(blocks)

@app.route('/transfer', methods=['POST'])
def transfer():
    data = request.json
    public_key = data.get('public_key')
    amount = data.get('amount')
    to_address = data.get('to_address')
    
    if not public_key or not amount or not to_address:
        return jsonify({"error": "Missing required fields"}), 400

    # Realiza a transferência
    message, code = blockchain.transfer(public_key, to_address, amount)
    return jsonify({"message": message}), code

@app.route('/balance', methods=['GET'])
def check_balance():
    public_key = request.args.get('public_key')  # Espera que a chave pública seja passada como um parâmetro de consulta
    if not public_key:
        return {"error": "Chave pública não fornecida."}, 400
    
    balance, code = blockchain.get_balance(public_key)
    return balance, code

@app.route('/deposit', methods=['POST'])
def deposit():
    data = request.json
    
    public_key = data.get('public_key')
    amount = data.get('amount')
    
    message, code = blockchain.deposit(public_key, amount)
    return message, code
    

if __name__ == "__main__":
    print(Fore.GREEN + Style.BRIGHT + f"Server started successfully on port {PORT_SERVER}." + Style.RESET_ALL)
    app.run(debug=True, port=PORT_SERVER)
