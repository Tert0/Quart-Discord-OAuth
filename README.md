# Quart-Discord-OAuth
Discord OAuth Quart extension for APIs.
## Installation
```pip3 install quart-discord-oauth```

## Example
```python
from quart import Quart, jsonify, request
from quart_discord_oauth import DiscordOAuth2, requires_authorization, Unauthorized, InvalidRequest, RateLimited

app = Quart(__name__)

discord_oauth = DiscordOAuth2(app=app,
			      client_id=<your client id>,
			      client_secret="<your client secret>",
			      redirect_uri="<your redirect uri>",
			      scope="identify email guilds") # Your Scopes

@app.errorhandler(Unauthorized)
async def unauthorized(e):
    return {'error': 'Unauthorized'}


@app.errorhandler(InvalidRequest)
async def InvalidRequest(e):
    return {'error': 'InvalidRequest'}


@app.errorhandler(RateLimited)
async def RateLimited(e: RateLimited):
    return {
        'error': 'RateLimeted',
        'retry_after': e.retry_after
    }   


@app.route('/login')
async def login():
	return {"login_url": discord_oauth.DISCORD_LOGIN_URL}

@app.route('/callback')
async def callback():
	code = request.args.get("code")
	token = discord_oauth.get_access_token(code)
	return {"token": token}

@app.route('/user')
@requires_authorization
async def user():
	user = await discord_oauth.fetch_user()
	return jsonify(user.to_json())


@app.route('/guilds')
@requires_authorization
async def guilds():
	guilds, guilds_json = await discord_oauth.fetch_guilds()
	return jsonify(guilds.guilds_json)

@app.route('/authenticated')
async def authenticated():
    return {'authenticated': await discord_oauth.is_authenticated()}





app.run(debug=True, port=5555)
```
