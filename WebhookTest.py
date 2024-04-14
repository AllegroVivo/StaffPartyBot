from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    print(request.data)
    return 'success'
    
################################################################################        
if __name__ == '__main__':
    app.run()
    