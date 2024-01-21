import flask

app = flask.Flask("myTracker")

import os



# function to return the name of html page requested
def get_html(page_name):
    html_file = open(page_name + ".html")
    content = html_file.read()
    html_file.close()
    return content


# 
def create_data():
    if not os.path.exists("data.txt"):
        db = open("data.txt", "a")     #("static/db/" + str(find_username()) + ".txt", "a")
        # db.write(",,,")
        db.close()


# add data to text file seperated by new line
def add_data(new_data):
    notesdb = open("data.txt", "a")     #("static/db/" + str(find_username()) + ".txt", "a")
    notesdb.write("\n")
    notesdb.write(new_data)
    notesdb.close()

#
def add_data_first(new_data):
    notesdb = open("data.txt", "a")
    notesdb.write(new_data)
    notesdb.close()

# read user data
def get_data():
    data_file = open("data.txt")     #("static/db/" + str(find_username()) + ".txt")
    content = data_file.read()
    data_file.close()
    data = content.split("\n")
    return data



# #
# def find_username():
#     input_string = get_html("index")
#     target_word = "Welcome, "
#     end_character = "</p>"

#     # Find the index of the target word
#     index_of_word = input_string.find(target_word)
#     if index_of_word != -1:
#         # Move to the end of the target word
#         start_index = index_of_word + len(target_word)

#         # Find the index of the end character starting from the end of the target word
#         end_index = input_string.find(end_character, start_index)

#         if end_index != -1:
#             # Extract the desired substring
#             result = input_string[start_index:end_index]
#             return result
#         else:
#             # End character not found, return the substring from the target word to the end of the string
#             result = input_string[start_index:]
#             return result
#     else:
#         # Target word not found in the string
#         return None




# The home/login page
@app.route("/")
def home():
    create_data()
    return get_html("index")



# page to add new activity
@app.route("/add")
def add():
    html_page = get_html("add")
    
    # name = flask.request.args.get("name")
    # category = flask.request.args.get("category")
    # date = flask.request.args.get("date")
    # duration = flask.request.args.get("duration")
    # new_data = str(name) + "," + str(category) + "," + str(date) + "," + str(duration)
    # new_data_dublicated = ""
    # if new_data != "None,None,None,None" or new_data == new_data_dublicated:
    #     add_data(new_data)
    # new_data_dublicated = new_data
     
    return html_page



# page to view new activity added
@app.route("/addRedirected", methods=['POST'])
def add_redirected():
    data = get_data()
    
    name = flask.request.form['name']                     #args.get("name")
    category = flask.request.form['category']             #args.get("category")
    date = flask.request.form['date']                     #args.get("date")
    duration = flask.request.form['duration']             #args.get("duration")
    new_data = str(name) + "," + str(category) + "," + str(date) + "," + str(duration)
    
    if len(data) == 1 and data[0] == '':
        add_data_first(new_data)
    else:
        add_data(new_data)
    return flask.redirect(flask.url_for('activities'))



#
@app.route("/activities")
def activities():
    html_page = get_html("activities")
    data = get_data()
    
    # the table in the the right half of the dashboard page
    table_head = "<th>Name</th><th>Category</th><th>Date</th><th>Duration</th>"
    actual_values = ""

    if len(data) == 1 and data[0] == '':
        return html_page.replace("$$TABLE_HEAD$$", table_head).replace("$$DATA$$", "<tr><td></td><td></td><td></td><td></td></tr>")

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

    html_page = html_page.replace("$$DATA$$", actual_values).replace("$$TABLE_HEAD$$", table_head)
    return html_page


# The dashboard page
@app.route("/dashboard")
def dashboard():
    html_page = get_html("dashboard")
    data = get_data()
    
    
    

    if len(data) == 1 and data[0] == '':
        html_page = html_page.replace('$$HEIGHT$$', "1").replace('$$WORK$$', "0").replace('$$STUDY$$', "0").replace('$$SPORT$$', "0").replace('$$SOCIAL$$', "0").replace('$$SPIRITUAL$$', "0").replace('$$CREATIVE$$', "0").replace('$$CHILL$$', "0").replace('$$OTHER$$', "0")
        html_page = html_page.replace('$$COUNT$$', "1").replace('$$WORKF$$', "0").replace('$$STUDYF$$', "0").replace('$$SPORTF$$', "0").replace('$$SOCIALF$$', "0").replace('$$SPIRITUALF$$', "0").replace('$$CREATIVEF$$', "0").replace('$$CHILLF$$', "0").replace('$$OTHERF$$', "0")
        return html_page

    activities_duraion = [0, 0, 0, 0, 0, 0, 0, 0]       # [Work, Study, Sport, Social, Spiritual, Creative, Chill, Other]
    activities_frequency = [0, 0, 0, 0, 0, 0, 0, 0]       # [Work, Study, Sport, Social, Spiritual, Creative, Chill, Other]

    for row in data:
        col = row.split(",")

        if col[1] == 'Work':
            activities_duraion[0] += int(col[3])
            activities_frequency [0] += 1
        elif col[1] == 'Study':
            activities_duraion[1] += int(col[3])
            activities_frequency [1] += 1
        elif col[1] == 'Sport':
            activities_duraion[2] += int(col[3])
            activities_frequency [2] += 1
        elif col[1] == 'Social':
            activities_duraion[3] += int(col[3])
            activities_frequency [3] += 1
        elif col[1] == 'Spiritual':
            activities_duraion[4] += int(col[3])
            activities_frequency [4] += 1
        elif col[1] == 'Creative':
            activities_duraion[5] += int(col[3])
            activities_frequency [5] += 1
        elif col[1] == 'Chill':
            activities_duraion[6] += int(col[3])
            activities_frequency [6] += 1
        elif col[1] == 'Other':
            activities_duraion[7] += int(col[3])
            activities_frequency [7] += 1

    
    
    # 
    height_chart = sorted(activities_duraion)[-1] * 1.2
    html_page = html_page.replace('$$HEIGHT$$', str(height_chart))

    # sum_duration = sum(activities_duraion)
    # html_page = html_page.replace('$$SUM$$', str(sum_duration))

    count_activities = sum(activities_frequency)
    html_page = html_page.replace('$$COUNT$$', str(count_activities))

    html_page = html_page.replace('$$WORK$$', str(activities_duraion[0])).replace('$$STUDY$$', str(activities_duraion[1])).replace('$$SPORT$$', str(activities_duraion[2])).replace('$$SOCIAL$$', str(activities_duraion[3])).replace('$$SPIRITUAL$$', str(activities_duraion[4])).replace('$$CREATIVE$$', str(activities_duraion[5])).replace('$$CHILL$$', str(activities_duraion[6])).replace('$$OTHER$$', str(activities_duraion[7]))

    html_page = html_page.replace('$$WORKF$$', str(activities_frequency[0])).replace('$$STUDYF$$', str(activities_frequency[1])).replace('$$SPORTF$$', str(activities_frequency[2])).replace('$$SOCIALF$$', str(activities_frequency[3])).replace('$$SPIRITUALF$$', str(activities_frequency[4])).replace('$$CREATIVEF$$', str(activities_frequency[5])).replace('$$CHILLF$$', str(activities_frequency[6])).replace('$$OTHERF$$', str(activities_frequency[7]))
    
    
    return html_page

    