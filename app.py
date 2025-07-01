from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health_check():
    return jsonify(status="healthy", message="Application is running normally."), 200

if __name__ == '__main__':
    app.run(debug=True)
