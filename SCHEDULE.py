import hashlib
import colorama
import requests
from flask import Flask, request
from colorama import Fore, Style, Back
from bin.ports import PORT_SCHEDULE

colorama.init()

def POSTRequest(URL):
    response = requests.post(URL)

    if response.status_code == 200:
        return response.json()
    else:
        return Fore.RED + Style.BRIGHT + f"Request failed with status code: {response.status_code}" + Style.RESET_ALL

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the BM Schedule Server"

@app.route('/schedule', methods=['POST'])
def schedule():
    data = request.get_json()
    print(POSTRequest("http://localhost:4040/valid"))
    print(data)
    return data

if __name__ == '__main__':
    print( Fore.GREEN + Style.BRIGHT + f"Schedule Server started sucessfully on port {PORT_SCHEDULE}." + Style.RESET_ALL)
    app.run(debug=True, port=PORT_SCHEDULE)