import time
import flask
import BlockChainSystem
from bin.ports import PORT_API
from colorama import Fore, Style, Back

app = flask.Flask(__name__)

@app.route('/')
def index():
    print(time.time_ns())    
    return "Welcome to the API!"

@app.route('/info', methods=['POST'])
def get_info():
    return 'Informação'
    
if __name__ == "__main__":
    print( Fore.GREEN + Style.BRIGHT + f"API Server started sucessfully on port {PORT_API}." + Style.RESET_ALL)
    app.run(debug=True, port=PORT_API)