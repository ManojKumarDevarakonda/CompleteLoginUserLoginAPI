from sanic import Sanic, response
from sanic.response import json
from models import CompleteLoginData
from database import db,Base,engine
import secrets
 

app = Sanic(__name__)
Base.metadata.create_all(engine)

def generate_token():
    return secrets.token_hex(60)

@app.route("/user-register",methods=['POST'])
async def registerUser(request) :
    data = request.json
    UploadId = data.get("UploadId")
    Username = data.get("Username")
    Password = data.get("Password")
    user = CompleteLoginData(UploadId = UploadId, Username = Username, Password = Password )
    db.add(user)
    db.commit()
    return json({'message':"User Registred Successfully!!!"})

@app.route("/user-login", methods=['POST'])
async def loginUser(request):
    data = request.json
    Username = data.get("Username")
    Password = data.get("Password")
 
    if not Username or not Password:
        return response.json({'error': 'Invalid Credentials'}, status=400)

    user = db.query(CompleteLoginData).filter(CompleteLoginData.Username==Username ,CompleteLoginData.Password==Password).first()
    if user:
        auth_token = generate_token()
        status = 200
        return json({'auth_token': auth_token, "status":status, "message":"Login Successfully!!!"})
    else:
        return response.json({'error': 'Invalid credentials'}, status=401)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
