import flask

app = flask.Flask("myTracker")


# function to return the name of html page requested
def get_html(page_name):
    html_file = open(page_name + ".html")
    content = html_file.read()
    html_file.close()
    return content

# add data to text file seperated by new line
def add_data(new_data):
    notesdb = open("data.txt", "a")
    notesdb.write("\n")
    notesdb.write(new_data)
    notesdb.close()


# The home/login page
@app.route("/")
def home():
    return get_html("index")


# registeration page
@app.route("/register")
def dashboard():
    return get_html("register")



# page to add new activity
@app.route("/add")
def add():
    html_page = get_html("add")
    name = flask.request.args.get("name")
    category = flask.request.args.get("category")
    date = flask.request.args.get("date")
    duration = flask.request.args.get("duration")
    new_data = str(name) + "," + str(category) + "," + str(date) + "," + str(duration)
    add_data(new_data)
    return html_page
  