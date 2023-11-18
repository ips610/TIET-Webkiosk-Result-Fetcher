from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/process_signup', methods=['POST'])
def process_signup():
    
    signup_username = request.form.get('signup_username')
    signup_email = request.form.get('signup_email')
    signup_password = request.form.get('signup_password')
    
    # Here you can process the signup data
    # For this example, let's just print the data
    print(f"Signup Username: {signup_username}")
    print(f"Signup Email: {signup_email}")
    print(f"Signup Password: {signup_password}")
    
    # Replace the print statements with your actual signup logic
    # For instance, you might want to create a new user in a database
    
    return "Signup successful!"


@app.route('/login')
def login():
    return render_template('login.html')
if __name__ == '__main__':
    app.run(debug=True)