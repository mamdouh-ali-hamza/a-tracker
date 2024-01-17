import flask

app = flask.Flask("myTracker")


# function to return the name of html page requested
def get_html(page_name):
    html_file = open(page_name + ".html")
    content = html_file.read()
    html_file.close()
    return content



# The home/login page
@app.route("/")
def home():
    return get_html("index")


# registeration page
@app.route("/register")
def dashboard():
    return get_html("register")



   