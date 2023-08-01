from sanic import Sanic,response
from sanic_auth import Auth ,User
from models import CompleteLoginData
 
app = Sanic(__name__)

# AUTH_LOGIN_ENDPOINT
app.config.AUTH_LOGIN_ENDPOINT = 'login'
auth = Auth(app)


session = {}
@app.middleware('request')
async def add_session (request):
    request.ctx.session = session


LOGIN_FORM = '''
<h2>Please sign in, you can try:</h2>

<p>{}</p>
<form action="" method="POST" style ="font-size :21px;">
  <input class="username" id="name" name="username"
    placeholder="username" type="text" value="" style ="width :100%;height : 45px;font-size : 21px;border-radius:5px;margin-bottom : 10px;padding : 10px;"><br>
  <input class="password" id="password" name="password"
    placeholder="password" type="password" value="" style ="width :100%;height : 45px;font-size : 21px;border-radius:5px;margin-bottom : 10px;padding : 10px;"><br>
  <input id="submit" name="submit" type="submit" value="Sign In" style ="width :50%;height : 45px;font-size : 21px;border-radius:5px;margin-bottom : 10px;margin-left : 25%;padding : 10px;">
</form>
'''
@app.route('/login',methods=['GET' , 'POST'])
async def login(request) : 
    message = ''
    if request.method == 'POST' : 
        data = request.json
        Username = data.get("Username")
        Password = data.get("Password")
            # for demonstration purpose only, you should use more robust method
        if Username == CompleteLoginData.Username and Password == CompleteLoginData.Password:
                # use User proxy in sanic_auth, this should be some ORM model
                # object in production, the default implementation of
                # auth.login_user expects User.id and User.name available
                user = CompleteLoginData(Username = CompleteLoginData.Username,Password = CompleteLoginData.Password)
                auth.login_user(request, user)
                return response.redirect('/')
        message = 'invalid username or password'
    return response.html(LOGIN_FORM.format(message))


@app.route('/logout')
@auth.login_required
async def logout(request):
    auth.logout_user(request)
    return response.redirect('/login')
@app.route('/')
@auth.login_required(user_keyword='user')
async def profile(request, user):
    content = '<a href="/logout">Logout</a><p>Welcome, %s</p>' % user.name
    return response.html(content)

def handle_no_auth(request):
    return response.json(dict(message='unauthorized'), status=401)
@app.route('/api/user')
@auth.login_required(user_keyword='user', handle_no_auth=handle_no_auth)
async def api_profile(request, user):
    return response.json(dict(id=user.id, name=user.name))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)