from app import app
from flask import render_template, request, redirect, url_for


###
# Routes
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')



### run statement
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
