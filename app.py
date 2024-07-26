from flask import Flask, render_template, redirect, url_for,jsonify,request
import requests

app = Flask(__name__)

# Replace with your Keycloak configuration
KEYCLOAK_AUTH_URL = 'http://localhost:8080/realms/myorg/protocol/openid-connect/auth'
CLIENT_ID = 'flask_login_two'
REDIRECT_URI = 'http://localhost:5000/auth_callback'  # Replace with your actual callback URL


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    auth_url = f'{KEYCLOAK_AUTH_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=openid+profile+email'
    return redirect(auth_url)

@app.route('/auth_callback')
def auth_callback():
    # Handle the authentication callback here (optional for this basic example)
    code = request.args.get('code')
    return render_template('result.html', code=code)

@app.route('/get_token', methods=['POST'])
def get_token():
    print("came")
    if request.method == 'POST':  # Check if request is POST
        code = request.form.get('code')  # Access code from form data
        print(code)
        
        # Exchange authorization code for access token using your logic here
        # (Replace with your specific token exchange logic)

        # Example using requests (replace with your actual implementation)
        token_endpoint = 'http://localhost:8080/realms/myorg/protocol/openid-connect/token'
        client_secret = '4Ej5jg5WgT2pAIGkrtIy60A7WOlFyNfx'  # Replace with your client secret
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': CLIENT_ID,
            'client_secret': client_secret,
            'redirect_uri': REDIRECT_URI,
            'scope':'openid'
        }
        h = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(token_endpoint, data=payload, headers=h)
        print("keycloak=-=-=-=-=-=   ", response.json())

        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access_token')
            #return jsonify({'access_token': access_token})
            return render_template('profile.html', access_token=access_token)
        else:
            return jsonify({'error': 'Failed to exchange authorization code'}), response.status_code

    return jsonify({'error': 'Invalid request method'}), 405 


# @app.route('/get_profile',methods=['GET'])
# def get_profile():
#     if request.method == 'GET':
#         token = request.args.get('access_token')  # Access code from form data
#         print("\n blah blah.....=>access token :",token)
#     else:
#         print("token not yet received")
#     url='http://localhost:8080/realms/myorg/protocol/openid-connect/userinfo'
#     headers = {'Authorization': f'Bearer {token}'}
@app.route('/get_profile', methods=['GET'])
def get_profile():
    if request.method == 'GET':
        token = request.args.get('access_token')
        print("\n blah blah.....=>access token :", token)
        link1= 'http://localhost:8080/realms/myorg/protocol/openid-connect/userinfo'
        headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.get(link1, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            return jsonify({'data': user_data})
        else:
            print(f"Error fetching user data: {response.text}")
            return jsonify({'error': f'Error fetching user data: {response.text}'}), response.status_code
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500


        


if __name__ == '__main__':
    app.run(debug=True)







    

