from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello():
    return "Hello from EKS! Deployed across multiple regions using GitHub Actions and AWS!"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
