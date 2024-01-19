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
    notesdb.write(new_data)
    notesdb.write("\n")
    notesdb.close()

# read user data
def get_data():
    data_file = open("data.txt")
    content = data_file.read()
    data_file.close()
    data = content.split("\n")
    return data


# add user
def add_user(new_user):
    usersdb = open("/static/db/users.txt", "a")
    usersdb.write(new_user)
    usersdb.write("\n")
    usersdb.close()


# The home/login page
@app.route("/")
def home():
    return get_html("index")


# registeration page
@app.route("/register")
def register_page():
    return get_html("register")


# 
@app.route("/new-user")
def register():
    html_page = get_html("/")
    registerName = flask.request.args.get("registerName")
    registerUsername = flask.request.args.get("registerUsername")
    registerPassword = flask.request.args.get("registerPassword")
    new_user = registerName + "," + registerUsername + "," + registerPassword
    add_user(new_user)
    return html_page
    



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
    
    


#
@app.route("/dashboard")
def dashboard():
    html_page = get_html("dashboard")
    data = get_data()

    table_head = "<th>Name</th><th>Category</th><th>Date</th><th>Duration</th>"
    actual_values = ""

    activities_duraion = [0, 0, 0, 0, 0, 0, 0, 0]       # [Work, Study, Sport, Social, Spiritual, Creative, Chill, Other]

    for row in data:
        actual_values += "<tr>"
        col = row.split(",")

        if col[1] == 'Work':
            activities_duraion[0] += int(col[3])
        elif col[1] == 'Study':
            activities_duraion[1] += int(col[3])
        elif col[1] == 'Sport':
            activities_duraion[2] += int(col[3])
        elif col[1] == 'Social':
            activities_duraion[3] += int(col[3])
        elif col[1] == 'Spiritual':
            activities_duraion[4] += int(col[3])
        elif col[1] == 'Creative':
            activities_duraion[5] += int(col[3])
        elif col[1] == 'Chill':
            activities_duraion[6] += int(col[3])
        elif col[1] == 'Other':
            activities_duraion[7] += int(col[3])

        for td in col:
            actual_values += "<td>" + td + "</td>"

        actual_values += "</tr>"

    # if actual_values == "":
    #     return html_page.replace("$$NO_DATA_MESSAGE$$", "<p>No data yet<p>")     
    # else:
    #     return html_page.replace("$$DATA$$", actual_values).replace("$$TABLE_HEAD$$", table_head)
        
    # return html_page.replace("$$DATA$$", actual_values)
        
    # daily_date = flask.request.args.get("dailyDate")
    
    

    print(activities_duraion)

    height_chart = sorted(activities_duraion)[-1] * 1.2
    html_page = html_page.replace('$$HEIGHT$$', str(height_chart))

    html_page = html_page.replace('$$WORK$$', str(activities_duraion[0])).replace('$$STUDY$$', str(activities_duraion[1])).replace('$$SPORT$$', str(activities_duraion[2])).replace('$$SOCIAL$$', str(activities_duraion[3])).replace('$$SPIRITUAL$$', str(activities_duraion[4])).replace('$$CREATIVE$$', str(activities_duraion[5])).replace('$$CHILL$$', str(activities_duraion[6])).replace('$$OTHER$$', str(activities_duraion[7]))
    
    return html_page.replace("$$DATA$$", actual_values).replace("$$TABLE_HEAD$$", table_head)

