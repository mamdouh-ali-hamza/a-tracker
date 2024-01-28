import os
import datetime
import flask

app = flask.Flask("myTracker")


# Class 
class Activity:
    def __init__(self, name, category, date, duration):
        self.name = name
        self.category = category
        self.date = date
        self.duration = duration
    # add line in data file for the activity
    def make_activity(self):
        activity = str(self.name) + "," + str(self.category) + "," + str(self.date) + "," + str(self.duration)
        return activity
    # get the name of the week day from the date
    def get_weekday_name(self):
        date_activity = datetime.datetime.strptime(self.date, '%Y-%m-%d')
        day_activity = date_activity.strftime('%A')
        return day_activity


# function to return the name of html page requested
def get_html(page_name):
    html_file = open(page_name + ".html")
    content = html_file.read()
    html_file.close()
    return content


# function to create the file if not exist
def create_data():
    if not os.path.exists("data.txt"):
        db = open("data.txt", "a")     #("static/db/" + str(find_username()) + ".txt", "a")
        db.close()


# add data to text file seperated by new line
def add_data(new_data):
    db = open("data.txt", "a")     #("static/db/" + str(find_username()) + ".txt", "a")
    db.write("\n")
    db.write(new_data)
    db.close()


# add the first data in newly created file
def add_data_first(new_data):
    db = open("data.txt", "a")
    db.write(new_data)
    db.close()


# read user data
def get_data():
    data_file = open("data.txt")     #("static/db/" + str(find_username()) + ".txt")
    content = data_file.read()
    data_file.close()
    data = content.split("\n")
    return data


# delete last line in file
def delete_last_line():
    # Read all lines from the file
    lines = get_data()
    # Remove the last line
    modified_lines = lines[:-1]
    # Write the modified lines back to the file
    with open("data.txt", 'w') as file:
        file.write("\n".join(modified_lines))


# delelte all lines in file
def delete_all_lines():
    # Create an empty list to represent an empty file
    modified_lines = []
    # Write the modified lines (empty list) back to the file
    with open("data.txt", 'w') as file:
        file.write("\n".join(modified_lines))


# function to calculate the activity duration for every day: recieve object of class Activity, the dictionary, category, duration of activity and return updated dictionary
def weekday_activity_duration(activity_obj_day, weekday_dict_duration, category, duration):
    weekday_name = activity_obj_day.get_weekday_name()
    if weekday_name == 'Monday':
        weekday_dict_duration['Monday'][category] += duration
    elif weekday_name == 'Tuesday':
        weekday_dict_duration['Tuesday'][category] += duration
    elif weekday_name == 'Wednesday':
        weekday_dict_duration['Wednesday'][category] += duration
    elif weekday_name == 'Thursday':
        weekday_dict_duration['Thursday'][category] += duration
    elif weekday_name == 'Friday':
        weekday_dict_duration['Friday'][category] += duration
    elif weekday_name == 'Saturday':
        weekday_dict_duration['Saturday'][category] += duration
    elif weekday_name == 'Sunday':
        weekday_dict_duration['Sunday'][category] += duration
    return weekday_dict_duration


# The home page
@app.route("/")
def home():
    create_data()
    return get_html("index")


# page to add new activity
@app.route("/add")
def add():
    html_page = get_html("add")
    return html_page


# page to redirect from add activity to all activities pages  ("Post/Redirect/Get": solving the problem when refreshing the page the form auto submit last data)
@app.route("/addRedirected", methods=['POST'])
def add_redirected():
    data = get_data()  
    name = flask.request.form['name']                     
    category = flask.request.form['category']             
    date = flask.request.form['date']                     
    duration = flask.request.form['duration']          

    # creation object of Activity class and calling a methond of the class to concat the form inputs to make the line (activity)
    activity_obj_add = Activity(name, category, date, duration)
    new_data = activity_obj_add.make_activity()
    # if it is the first activity line in the file (for not producing empty line in the beginning)
    if len(data) == 1 and data[0] == '':
        add_data_first(new_data)
    else:
        add_data(new_data)
    return flask.redirect(flask.url_for('add'))


# page to view table of all activities
@app.route("/activities")
def activities():
    html_page = get_html("activities")
    data = get_data()
    # the table head
    table_head = "<th>Name</th><th>Category</th><th>Date</th><th>Duration</th>"
    
    # if the data file is empty, just add the table head and empty tags for the body
    if len(data) == 1 and data[0] == '':
        return html_page.replace("$$TABLE_HEAD$$", table_head).replace("$$DATA$$", "<tr><td></td><td></td><td></td><td></td></tr>")
    # intialize the variable holding the data of the body of the table
    actual_values = ""
    # data is a list of lines of the data file, spliting the line to get every data cell and adding the tags for every row and column of the table
    for row in data:
        if row.strip():
            # the opending row tag
            actual_values += "<tr>"
            # spliting the line to columns
            col = row.split(",")
            # adding every cell for the table body
            for td in col:
                actual_values += "<td>" + td + "</td>"
            # the closing row tag opened before
            actual_values += "</tr>"
    # replacing table head and body data which been held in the variables to the corresponding words in the html file
    html_page = html_page.replace("$$DATA$$", actual_values).replace("$$TABLE_HEAD$$", table_head)
    return html_page


# delete last activity in the table and redirect to activities page
@app.route("/deleteLast", methods=['POST'])
def delete_last():
    delete_last_line()
    return flask.redirect(flask.url_for('activities'))


# delete ALL activities in the table and redirect to activities page
@app.route("/deleteAll", methods=['POST'])
def delete_all():
    delete_all_lines()
    return flask.redirect(flask.url_for('activities'))


# The dashboard page
@app.route("/dashboard")
def dashboard():
    html_page = get_html("dashboard")
    data = get_data()

    # using datatime to calculate current date
    current_date = datetime.datetime.now()
    today_date = current_date.date()
    html_page = html_page.replace("$$DATESELECTED$$", str(today_date))

    # Convert the input date string to a datetime object
    input_date = datetime.datetime.strptime(str(today_date), '%Y-%m-%d')
    # Calculate the start of the week (Monday) by subtracting the day of the week
    start_of_week = input_date - datetime.timedelta(days=input_date.weekday())
    # Calculate the dates of the entire week (Monday to Sunday)
    week_dates = [start_of_week + datetime.timedelta(days=i) for i in range(7)]
    week_dates_str = []
    for date in week_dates:
        week_dates_str.append(date.strftime('%Y-%m-%d'))

    # if the file data empty return zeros
    if len(data) == 1 and data[0] == '':
        html_page = (html_page.replace('$$HEIGHT$$', "1")
                     .replace('$$WORK$$', "0")
                     .replace('$$STUDY$$', "0")
                     .replace('$$SPORT$$', "0")
                     .replace('$$SOCIAL$$', "0")
                     .replace('$$SPIRITUAL$$', "0")
                     .replace('$$CREATIVE$$', "0")
                     .replace('$$CHILL$$', "0")
                     .replace('$$OTHER$$', "0")
                    )
        html_page = (html_page.replace('$$COUNT$$', "1")
                     .replace('$$WORKF$$', "0")
                     .replace('$$STUDYF$$', "0")
                     .replace('$$SPORTF$$', "0")
                     .replace('$$SOCIALF$$', "0")
                     .replace('$$SPIRITUALF$$', "0")
                     .replace('$$CREATIVEF$$', "0")
                     .replace('$$CHILLF$$', "0")
                     .replace('$$OTHERF$$', "0")
                    )
        html_page = (html_page.replace('$$HeightLine$$', "0")
                        .replace('$$Monday-Work$$', "0")
                        .replace('$$Monday-Study$$', "0")
                        .replace('$$Monday-Sport$$', "0")
                        .replace('$$Monday-Social$$', "0")
                        .replace('$$Monday-Spiritual$$', "0")
                        .replace('$$Monday-Creative$$', "0")
                        .replace('$$Monday-Chill$$', "0")
                        .replace('$$Monday-Other$$', "0")
                        .replace('$$Tuesday-Work$$', "0")
                        .replace('$$Tuesday-Study$$', "0")
                        .replace('$$Tuesday-Sport$$', "0")
                        .replace('$$Tuesday-Social$$', "0")
                        .replace('$$Tuesday-Spiritual$$', "0")
                        .replace('$$Tuesday-Creative$$', "0")
                        .replace('$$Tuesday-Chill$$', "0")
                        .replace('$$Tuesday-Other$$', "0")
                        .replace('$$Wednesday-Work$$', "0")
                        .replace('$$Wednesday-Study$$', "0")
                        .replace('$$Wednesday-Sport$$', "0")
                        .replace('$$Wednesday-Social$$', "0")
                        .replace('$$Wednesday-Spiritual$$', "0")
                        .replace('$$Wednesday-Creative$$', "0")
                        .replace('$$Wednesday-Chill$$', "0")
                        .replace('$$Wednesday-Other$$', "0")
                        .replace('$$Thursday-Work$$', "0")
                        .replace('$$Thursday-Study$$', "0")
                        .replace('$$Thursday-Sport$$', "0")
                        .replace('$$Thursday-Social$$', "0")
                        .replace('$$Thursday-Spiritual$$', "0")
                        .replace('$$Thursday-Creative$$', "0")
                        .replace('$$Thursday-Chill$$', "0")
                        .replace('$$Thursday-Other$$', "0")
                        .replace('$$Friday-Work$$', "0")
                        .replace('$$Friday-Study$$', "0")
                        .replace('$$Friday-Sport$$', "0")
                        .replace('$$Friday-Social$$', "0")
                        .replace('$$Friday-Spiritual$$', "0")
                        .replace('$$Friday-Creative$$', "0")
                        .replace('$$Friday-Chill$$', "0")
                        .replace('$$Friday-Other$$', "0")
                        .replace('$$Saturday-Work$$', "0")
                        .replace('$$Saturday-Study$$', "0")
                        .replace('$$Saturday-Sport$$', "0")
                        .replace('$$Saturday-Social$$', "0")
                        .replace('$$Saturday-Spiritual$$', "0")
                        .replace('$$Saturday-Creative$$', "0")
                        .replace('$$Saturday-Chill$$', "0")
                        .replace('$$Saturday-Other$$', "0")
                        .replace('$$Sunday-Work$$', "0")
                        .replace('$$Sunday-Study$$', "0")
                        .replace('$$Sunday-Sport$$', "0")
                        .replace('$$Sunday-Social$$', "0")
                        .replace('$$Sunday-Spiritual$$', "0")
                        .replace('$$Sunday-Creative$$', "0")
                        .replace('$$Sunday-Chill$$', "0")
                        .replace('$$Sunday-Other$$', "0")
                        )
        html_page = (html_page.replace('$$HEIGHTMONTH$$', "1")
                     .replace('$$WORKMONTH$$', "0")
                     .replace('$$STUDYMONTH$$', "0")
                     .replace('$$SPORTMONTH$$', "0")
                     .replace('$$SOCIALMONTH$$', "0")
                     .replace('$$SPIRITUALMONTH$$', "0")
                     .replace('$$CREATIVEMONTH$$', "0")
                     .replace('$$CHILLMONTH$$', "0")
                     .replace('$$OTHERMONTH$$', "0")
                    )
        return html_page
    
    # here the data file not empty 
    # initializing variable used in charts
    activities_duraion = [0, 0, 0, 0, 0, 0, 0, 0]                       # [Work, Study, Sport, Social, Spiritual, Creative, Chill, Other]
    activities_frequency = [0, 0, 0, 0, 0, 0, 0, 0]                     # [Work, Study, Sport, Social, Spiritual, Creative, Chill, Other]
    weekday_dict_duration = {'Monday': [0, 0, 0, 0, 0, 0, 0, 0],        # [Work, Study, Sport, Social, Spiritual, Creative, Chill, Other]
                            'Tuesday': [0, 0, 0, 0, 0, 0, 0, 0],
                            'Wednesday': [0, 0, 0, 0, 0, 0, 0, 0],
                            'Thursday': [0, 0, 0, 0, 0, 0, 0, 0],
                            'Friday': [0, 0, 0, 0, 0, 0, 0, 0],
                            'Saturday': [0, 0, 0, 0, 0, 0, 0, 0],
                            'Sunday': [0, 0, 0, 0, 0, 0, 0, 0]
                            }
    days_passed = 0
    month_average = [0, 0, 0, 0, 0, 0, 0, 0]                            # [Work, Study, Sport, Social, Spiritual, Creative, Chill, Other]

    # data file returned as list of lines
    for row in data:
        #spliting the lines to 4 columns
        col = row.split(",")
        # for the column and pie charts checking for the same day of today
        if col[2] == str(today_date):
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

        # using method weekday_activity_duration of class Activity to return the name of day of week
        activity_obj_day = Activity(col[0], col[1], col[2], col[3])
        # for line chart using list of dates of the days in the week of today
        if col[2] in week_dates_str:
            if col[1] == 'Work':
                weekday_dict_duration = weekday_activity_duration(activity_obj_day, weekday_dict_duration, 0, int(col[3]))
            elif col[1] == 'Study':
                weekday_dict_duration = weekday_activity_duration(activity_obj_day, weekday_dict_duration, 1, int(col[3]))
            elif col[1] == 'Sport':
                weekday_dict_duration = weekday_activity_duration(activity_obj_day, weekday_dict_duration, 2, int(col[3]))
            elif col[1] == 'Social':
                weekday_dict_duration = weekday_activity_duration(activity_obj_day, weekday_dict_duration, 3, int(col[3]))
            elif col[1] == 'Spiritual':
                weekday_dict_duration = weekday_activity_duration(activity_obj_day, weekday_dict_duration, 4, int(col[3]))
            elif col[1] == 'Creative':
                weekday_dict_duration = weekday_activity_duration(activity_obj_day, weekday_dict_duration, 5, int(col[3]))
            elif col[1] == 'Chill':
                weekday_dict_duration = weekday_activity_duration(activity_obj_day, weekday_dict_duration, 6, int(col[3]))
            elif col[1] == 'Other':
                weekday_dict_duration = weekday_activity_duration(activity_obj_day, weekday_dict_duration, 7, int(col[3]))

        #for bar chart using average duration of month per day for days passed already for every category
        if int(str(today_date).split('-')[2]) > days_passed:
            days_passed = int(col[2].split('-')[2])
        if str(col[2]).split('-')[1] == str(today_date).split('-')[1]:
            if col[1] == 'Work':
                month_average[0] += int(col[3])
            elif col[1] == 'Study':
                month_average[1] += int(col[3])
            elif col[1] == 'Sport':
                month_average[2] += int(col[3])
            elif col[1] == 'Social':
                month_average[3] += int(col[3])
            elif col[1] == 'Spiritual':
                month_average[4] += int(col[3])
            elif col[1] == 'Creative':
                month_average[5] += int(col[3])
            elif col[1] == 'Chill':
                month_average[6] += int(col[3])
            elif col[1] == 'Other':
                month_average[7] += int(col[3])  
    
    # column chart height depending on the 1.2* tallest column
    height_chart = sorted(activities_duraion)[-1] * 1.2
    html_page = html_page.replace('$$HEIGHT$$', str(height_chart))
    html_page = (html_page.replace('$$WORK$$', str(activities_duraion[0]))
                 .replace('$$STUDY$$', str(activities_duraion[1]))
                 .replace('$$SPORT$$', str(activities_duraion[2]))
                 .replace('$$SOCIAL$$', str(activities_duraion[3]))
                 .replace('$$SPIRITUAL$$', str(activities_duraion[4]))
                 .replace('$$CREATIVE$$', str(activities_duraion[5]))
                 .replace('$$CHILL$$', str(activities_duraion[6]))
                 .replace('$$OTHER$$', str(activities_duraion[7]))
                )

    # pie chart depending on portion of every category in the data of count of all categories
    count_activities = sum(activities_frequency)
    html_page = html_page.replace('$$COUNT$$', str(count_activities))
    html_page = (html_page.replace('$$WORKF$$', str(activities_frequency[0]))
                 .replace('$$STUDYF$$', str(activities_frequency[1]))
                 .replace('$$SPORTF$$', str(activities_frequency[2]))
                 .replace('$$SOCIALF$$', str(activities_frequency[3]))
                 .replace('$$SPIRITUALF$$', str(activities_frequency[4]))
                 .replace('$$CREATIVEF$$', str(activities_frequency[5]))
                 .replace('$$CHILLF$$', str(activities_frequency[6]))
                 .replace('$$OTHERF$$', str(activities_frequency[7]))
                )
    
    # height of line chart
    max_height_chart_line = max(max(sublist) for sublist in weekday_dict_duration.values())
    html_page = html_page.replace('$$HeightLine$$', str(max_height_chart_line))
    html_page = (html_page.replace('$$Monday-Work$$', str(weekday_dict_duration['Monday'][0]))
                        .replace('$$Monday-Study$$', str(weekday_dict_duration['Monday'][1]))
                        .replace('$$Monday-Sport$$', str(weekday_dict_duration['Monday'][2]))
                        .replace('$$Monday-Social$$', str(weekday_dict_duration['Monday'][3]))
                        .replace('$$Monday-Spiritual$$', str(weekday_dict_duration['Monday'][4]))
                        .replace('$$Monday-Creative$$', str(weekday_dict_duration['Monday'][5]))
                        .replace('$$Monday-Chill$$', str(weekday_dict_duration['Monday'][6]))
                        .replace('$$Monday-Other$$', str(weekday_dict_duration['Monday'][7]))
                        .replace('$$Tuesday-Work$$', str(weekday_dict_duration['Tuesday'][0]))
                        .replace('$$Tuesday-Study$$', str(weekday_dict_duration['Tuesday'][1]))
                        .replace('$$Tuesday-Sport$$', str(weekday_dict_duration['Tuesday'][2]))
                        .replace('$$Tuesday-Social$$', str(weekday_dict_duration['Tuesday'][3]))
                        .replace('$$Tuesday-Spiritual$$', str(weekday_dict_duration['Tuesday'][4]))
                        .replace('$$Tuesday-Creative$$', str(weekday_dict_duration['Tuesday'][5]))
                        .replace('$$Tuesday-Chill$$', str(weekday_dict_duration['Tuesday'][6]))
                        .replace('$$Tuesday-Other$$', str(weekday_dict_duration['Tuesday'][7]))
                        .replace('$$Wednesday-Work$$', str(weekday_dict_duration['Wednesday'][0]))
                        .replace('$$Wednesday-Study$$', str(weekday_dict_duration['Wednesday'][1]))
                        .replace('$$Wednesday-Sport$$', str(weekday_dict_duration['Wednesday'][2]))
                        .replace('$$Wednesday-Social$$', str(weekday_dict_duration['Wednesday'][3]))
                        .replace('$$Wednesday-Spiritual$$', str(weekday_dict_duration['Wednesday'][4]))
                        .replace('$$Wednesday-Creative$$', str(weekday_dict_duration['Wednesday'][5]))
                        .replace('$$Wednesday-Chill$$', str(weekday_dict_duration['Wednesday'][6]))
                        .replace('$$Wednesday-Other$$', str(weekday_dict_duration['Wednesday'][7]))
                        .replace('$$Thursday-Work$$', str(weekday_dict_duration['Thursday'][0]))
                        .replace('$$Thursday-Study$$', str(weekday_dict_duration['Thursday'][1]))
                        .replace('$$Thursday-Sport$$', str(weekday_dict_duration['Thursday'][2]))
                        .replace('$$Thursday-Social$$', str(weekday_dict_duration['Thursday'][3]))
                        .replace('$$Thursday-Spiritual$$', str(weekday_dict_duration['Thursday'][4]))
                        .replace('$$Thursday-Creative$$', str(weekday_dict_duration['Thursday'][5]))
                        .replace('$$Thursday-Chill$$', str(weekday_dict_duration['Thursday'][6]))
                        .replace('$$Thursday-Other$$', str(weekday_dict_duration['Thursday'][7]))
                        .replace('$$Friday-Work$$', str(weekday_dict_duration['Friday'][0]))
                        .replace('$$Friday-Study$$', str(weekday_dict_duration['Friday'][1]))
                        .replace('$$Friday-Sport$$', str(weekday_dict_duration['Friday'][2]))
                        .replace('$$Friday-Social$$', str(weekday_dict_duration['Friday'][3]))
                        .replace('$$Friday-Spiritual$$', str(weekday_dict_duration['Friday'][4]))
                        .replace('$$Friday-Creative$$', str(weekday_dict_duration['Friday'][5]))
                        .replace('$$Friday-Chill$$', str(weekday_dict_duration['Friday'][6]))
                        .replace('$$Friday-Other$$', str(weekday_dict_duration['Friday'][7]))
                        .replace('$$Saturday-Work$$', str(weekday_dict_duration['Saturday'][0]))
                        .replace('$$Saturday-Study$$', str(weekday_dict_duration['Saturday'][1]))
                        .replace('$$Saturday-Sport$$', str(weekday_dict_duration['Saturday'][2]))
                        .replace('$$Saturday-Social$$', str(weekday_dict_duration['Saturday'][3]))
                        .replace('$$Saturday-Spiritual$$', str(weekday_dict_duration['Saturday'][4]))
                        .replace('$$Saturday-Creative$$', str(weekday_dict_duration['Saturday'][5]))
                        .replace('$$Saturday-Chill$$', str(weekday_dict_duration['Saturday'][6]))
                        .replace('$$Saturday-Other$$', str(weekday_dict_duration['Saturday'][7]))
                        .replace('$$Sunday-Work$$', str(weekday_dict_duration['Sunday'][0]))
                        .replace('$$Sunday-Study$$', str(weekday_dict_duration['Sunday'][1]))
                        .replace('$$Sunday-Sport$$', str(weekday_dict_duration['Sunday'][2]))
                        .replace('$$Sunday-Social$$', str(weekday_dict_duration['Sunday'][3]))
                        .replace('$$Sunday-Spiritual$$', str(weekday_dict_duration['Sunday'][4]))
                        .replace('$$Sunday-Creative$$', str(weekday_dict_duration['Sunday'][5]))
                        .replace('$$Sunday-Chill$$', str(weekday_dict_duration['Sunday'][6]))
                        .replace('$$Sunday-Other$$', str(weekday_dict_duration['Sunday'][7]))
                        )

    # bar chart
    height_month = sorted(month_average)[-1] / days_passed * 1.2
    html_page = html_page.replace('$$HEIGHTMONTH$$', str(height_month))
    html_page = (html_page.replace('$$WORKMONTH$$', str(round(month_average[0] / days_passed, 2)))
                 .replace('$$STUDYMONTH$$', str(round(month_average[1] / days_passed, 2)))
                 .replace('$$SPORTMONTH$$', str(round(month_average[2] / days_passed, 2)))
                 .replace('$$SOCIALMONTH$$', str(round(month_average[3] / days_passed, 2)))
                 .replace('$$SPIRITUALMONTH$$', str(round(month_average[4] / days_passed, 2)))
                 .replace('$$CREATIVEMONTH$$', str(round(month_average[5] / days_passed, 2)))
                 .replace('$$CHILLMONTH$$', str(round(month_average[6] / days_passed, 2)))
                 .replace('$$OTHERMONTH$$', str(round(month_average[7] / days_passed, 2)))
                )  
    return html_page


# The selected date dashboard page
@app.route("/dashboardDateSelected")
def dashboard_date_selected():
    html_page = get_html("dashboard")
    data = get_data()

    # get selected date from input date in form
    date_selected = flask.request.args.get("dateSelected")
    # view selected date in the page
    html_page = html_page.replace("$$DATESELECTED$$", date_selected)

    # Convert the input date string to a datetime object
    input_date = datetime.datetime.strptime(str(date_selected), '%Y-%m-%d')
    # Calculate the start of the week (Monday) by subtracting the day of the week
    start_of_week = input_date - datetime.timedelta(days=input_date.weekday())
    # Calculate the dates of the entire week (Monday to Sunday)
    week_dates = [start_of_week + datetime.timedelta(days=i) for i in range(7)]
    week_dates_str = []
    for date in week_dates:
        week_dates_str.append(date.strftime('%Y-%m-%d'))
        
    # if the file data empty return zeros
    if len(data) == 1 and data[0] == '':
        html_page = (html_page.replace('$$HEIGHT$$', "1")
                     .replace('$$WORK$$', "0")
                     .replace('$$STUDY$$', "0")
                     .replace('$$SPORT$$', "0")
                     .replace('$$SOCIAL$$', "0")
                     .replace('$$SPIRITUAL$$', "0")
                     .replace('$$CREATIVE$$', "0")
                     .replace('$$CHILL$$', "0")
                     .replace('$$OTHER$$', "0")
                    )
        html_page = (html_page.replace('$$COUNT$$', "1")
                     .replace('$$WORKF$$', "0")
                     .replace('$$STUDYF$$', "0")
                     .replace('$$SPORTF$$', "0")
                     .replace('$$SOCIALF$$', "0")
                     .replace('$$SPIRITUALF$$', "0")
                     .replace('$$CREATIVEF$$', "0")
                     .replace('$$CHILLF$$', "0")
                     .replace('$$OTHERF$$', "0")
                    )
        html_page = (html_page.replace('$$HeightLine$$', "0")
                        .replace('$$Monday-Work$$', "0")
                        .replace('$$Monday-Study$$', "0")
                        .replace('$$Monday-Sport$$', "0")
                        .replace('$$Monday-Social$$', "0")
                        .replace('$$Monday-Spiritual$$', "0")
                        .replace('$$Monday-Creative$$', "0")
                        .replace('$$Monday-Chill$$', "0")
                        .replace('$$Monday-Other$$', "0")
                        .replace('$$Tuesday-Work$$', "0")
                        .replace('$$Tuesday-Study$$', "0")
                        .replace('$$Tuesday-Sport$$', "0")
                        .replace('$$Tuesday-Social$$', "0")
                        .replace('$$Tuesday-Spiritual$$', "0")
                        .replace('$$Tuesday-Creative$$', "0")
                        .replace('$$Tuesday-Chill$$', "0")
                        .replace('$$Tuesday-Other$$', "0")
                        .replace('$$Wednesday-Work$$', "0")
                        .replace('$$Wednesday-Study$$', "0")
                        .replace('$$Wednesday-Sport$$', "0")
                        .replace('$$Wednesday-Social$$', "0")
                        .replace('$$Wednesday-Spiritual$$', "0")
                        .replace('$$Wednesday-Creative$$', "0")
                        .replace('$$Wednesday-Chill$$', "0")
                        .replace('$$Wednesday-Other$$', "0")
                        .replace('$$Thursday-Work$$', "0")
                        .replace('$$Thursday-Study$$', "0")
                        .replace('$$Thursday-Sport$$', "0")
                        .replace('$$Thursday-Social$$', "0")
                        .replace('$$Thursday-Spiritual$$', "0")
                        .replace('$$Thursday-Creative$$', "0")
                        .replace('$$Thursday-Chill$$', "0")
                        .replace('$$Thursday-Other$$', "0")
                        .replace('$$Friday-Work$$', "0")
                        .replace('$$Friday-Study$$', "0")
                        .replace('$$Friday-Sport$$', "0")
                        .replace('$$Friday-Social$$', "0")
                        .replace('$$Friday-Spiritual$$', "0")
                        .replace('$$Friday-Creative$$', "0")
                        .replace('$$Friday-Chill$$', "0")
                        .replace('$$Friday-Other$$', "0")
                        .replace('$$Saturday-Work$$', "0")
                        .replace('$$Saturday-Study$$', "0")
                        .replace('$$Saturday-Sport$$', "0")
                        .replace('$$Saturday-Social$$', "0")
                        .replace('$$Saturday-Spiritual$$', "0")
                        .replace('$$Saturday-Creative$$', "0")
                        .replace('$$Saturday-Chill$$', "0")
                        .replace('$$Saturday-Other$$', "0")
                        .replace('$$Sunday-Work$$', "0")
                        .replace('$$Sunday-Study$$', "0")
                        .replace('$$Sunday-Sport$$', "0")
                        .replace('$$Sunday-Social$$', "0")
                        .replace('$$Sunday-Spiritual$$', "0")
                        .replace('$$Sunday-Creative$$', "0")
                        .replace('$$Sunday-Chill$$', "0")
                        .replace('$$Sunday-Other$$', "0")
                        )
        html_page = html_page.replace('$$HEIGHTMONTH$$', "1")
        html_page = (html_page.replace('$$WORKMONTH$$', "0")
                    .replace('$$STUDYMONTH$$', "0")
                    .replace('$$SPORTMONTH$$', "0")
                    .replace('$$SOCIALMONTH$$', "0")
                    .replace('$$SPIRITUALMONTH$$', "0")
                    .replace('$$CREATIVEMONTH$$', "0")
                    .replace('$$CHILLMONTH$$', "0")
                    .replace('$$OTHERMONTH$$', "0")
                    )
        return html_page

    # here the data file not empty 
    # initializing variable used in charts
    activities_duraion = [0, 0, 0, 0, 0, 0, 0, 0]                   # [Work, Study, Sport, Social, Spiritual, Creative, Chill, Other]
    activities_frequency = [0, 0, 0, 0, 0, 0, 0, 0]                 # [Work, Study, Sport, Social, Spiritual, Creative, Chill, Other]
    weekday_dict_duration = {'Monday': [0, 0, 0, 0, 0, 0, 0, 0],    # [Work, Study, Sport, Social, Spiritual, Creative, Chill, Other]
                            'Tuesday': [0, 0, 0, 0, 0, 0, 0, 0],
                            'Wednesday': [0, 0, 0, 0, 0, 0, 0, 0],
                            'Thursday': [0, 0, 0, 0, 0, 0, 0, 0],
                            'Friday': [0, 0, 0, 0, 0, 0, 0, 0],
                            'Saturday': [0, 0, 0, 0, 0, 0, 0, 0],
                            'Sunday': [0, 0, 0, 0, 0, 0, 0, 0]
                            }
    days_passed = 0
    month_average = [0, 0, 0, 0, 0, 0, 0, 0]                            # [Work, Study, Sport, Social, Spiritual, Creative, Chill, Other]
    
    # data file returned as list of lines
    for row in data:
        #spliting the lines to 4 columns
        col = row.split(",")

        # for the column and pie charts checking for the same day 
        if col[2] == str(date_selected):
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
        # using method weekday_activity_duration of class Activity to return the name of day of week
        activity_obj_day = Activity(col[0], col[1], col[2], col[3])
        # for line chart using list of dates of the days in the week of the day selected
        if col[2] in week_dates_str:
            if col[1] == 'Work':
                weekday_dict_duration = weekday_activity_duration(activity_obj_day, weekday_dict_duration, 0, int(col[3]))
            elif col[1] == 'Study':
                weekday_dict_duration = weekday_activity_duration(activity_obj_day, weekday_dict_duration, 1, int(col[3]))
            elif col[1] == 'Sport':
                weekday_dict_duration = weekday_activity_duration(activity_obj_day, weekday_dict_duration, 2, int(col[3]))
            elif col[1] == 'Social':
                weekday_dict_duration = weekday_activity_duration(activity_obj_day, weekday_dict_duration, 3, int(col[3]))
            elif col[1] == 'Spiritual':
                weekday_dict_duration = weekday_activity_duration(activity_obj_day, weekday_dict_duration, 4, int(col[3]))
            elif col[1] == 'Creative':
                weekday_dict_duration = weekday_activity_duration(activity_obj_day, weekday_dict_duration, 5, int(col[3]))
            elif col[1] == 'Chill':
                weekday_dict_duration = weekday_activity_duration(activity_obj_day, weekday_dict_duration, 6, int(col[3]))
            elif col[1] == 'Other':
                weekday_dict_duration = weekday_activity_duration(activity_obj_day, weekday_dict_duration, 7, int(col[3]))

        #for bar chart using average duration of month per day for days passed already for every category
        if int(str(date_selected).split('-')[2]) > days_passed:
            days_passed = int(col[2].split('-')[2])
        if str(col[2]).split('-')[1] == str(date_selected).split('-')[1]:
            if col[1] == 'Work':
                month_average[0] += int(col[3])
            elif col[1] == 'Study':
                month_average[1] += int(col[3])
            elif col[1] == 'Sport':
                month_average[2] += int(col[3])
            elif col[1] == 'Social':
                month_average[3] += int(col[3])
            elif col[1] == 'Spiritual':
                month_average[4] += int(col[3])
            elif col[1] == 'Creative':
                month_average[5] += int(col[3])
            elif col[1] == 'Chill':
                month_average[6] += int(col[3])
            elif col[1] == 'Other':
                month_average[7] += int(col[3])
    
    # column chart height depending on the 1.2* tallest column
    height_chart = sorted(activities_duraion)[-1] * 1.2
    html_page = html_page.replace('$$HEIGHT$$', str(height_chart))
    html_page = (html_page.replace('$$WORK$$', str(activities_duraion[0]))
                 .replace('$$STUDY$$', str(activities_duraion[1]))
                 .replace('$$SPORT$$', str(activities_duraion[2]))
                 .replace('$$SOCIAL$$', str(activities_duraion[3]))
                 .replace('$$SPIRITUAL$$', str(activities_duraion[4]))
                 .replace('$$CREATIVE$$', str(activities_duraion[5]))
                 .replace('$$CHILL$$', str(activities_duraion[6]))
                 .replace('$$OTHER$$', str(activities_duraion[7]))
                )

    # pie chart depending on portion of every category in the data of count of all categories 
    count_activities = sum(activities_frequency)
    html_page = html_page.replace('$$COUNT$$', str(count_activities))
    html_page = (html_page.replace('$$WORKF$$', str(activities_frequency[0]))
                 .replace('$$STUDYF$$', str(activities_frequency[1]))
                 .replace('$$SPORTF$$', str(activities_frequency[2]))
                 .replace('$$SOCIALF$$', str(activities_frequency[3]))
                 .replace('$$SPIRITUALF$$', str(activities_frequency[4]))
                 .replace('$$CREATIVEF$$', str(activities_frequency[5]))
                 .replace('$$CHILLF$$', str(activities_frequency[6]))
                 .replace('$$OTHERF$$', str(activities_frequency[7]))
                )
    
    # height of line chart
    max_height_chart_line = max(max(sublist) for sublist in weekday_dict_duration.values())
    html_page = html_page.replace('$$HeightLine$$', str(max_height_chart_line))
    html_page = (html_page.replace('$$Monday-Work$$', str(weekday_dict_duration['Monday'][0]))
                        .replace('$$Monday-Study$$', str(weekday_dict_duration['Monday'][1]))
                        .replace('$$Monday-Sport$$', str(weekday_dict_duration['Monday'][2]))
                        .replace('$$Monday-Social$$', str(weekday_dict_duration['Monday'][3]))
                        .replace('$$Monday-Spiritual$$', str(weekday_dict_duration['Monday'][4]))
                        .replace('$$Monday-Creative$$', str(weekday_dict_duration['Monday'][5]))
                        .replace('$$Monday-Chill$$', str(weekday_dict_duration['Monday'][6]))
                        .replace('$$Monday-Other$$', str(weekday_dict_duration['Monday'][7]))
                        .replace('$$Tuesday-Work$$', str(weekday_dict_duration['Tuesday'][0]))
                        .replace('$$Tuesday-Study$$', str(weekday_dict_duration['Tuesday'][1]))
                        .replace('$$Tuesday-Sport$$', str(weekday_dict_duration['Tuesday'][2]))
                        .replace('$$Tuesday-Social$$', str(weekday_dict_duration['Tuesday'][3]))
                        .replace('$$Tuesday-Spiritual$$', str(weekday_dict_duration['Tuesday'][4]))
                        .replace('$$Tuesday-Creative$$', str(weekday_dict_duration['Tuesday'][5]))
                        .replace('$$Tuesday-Chill$$', str(weekday_dict_duration['Tuesday'][6]))
                        .replace('$$Tuesday-Other$$', str(weekday_dict_duration['Tuesday'][7]))
                        .replace('$$Wednesday-Work$$', str(weekday_dict_duration['Wednesday'][0]))
                        .replace('$$Wednesday-Study$$', str(weekday_dict_duration['Wednesday'][1]))
                        .replace('$$Wednesday-Sport$$', str(weekday_dict_duration['Wednesday'][2]))
                        .replace('$$Wednesday-Social$$', str(weekday_dict_duration['Wednesday'][3]))
                        .replace('$$Wednesday-Spiritual$$', str(weekday_dict_duration['Wednesday'][4]))
                        .replace('$$Wednesday-Creative$$', str(weekday_dict_duration['Wednesday'][5]))
                        .replace('$$Wednesday-Chill$$', str(weekday_dict_duration['Wednesday'][6]))
                        .replace('$$Wednesday-Other$$', str(weekday_dict_duration['Wednesday'][7]))
                        .replace('$$Thursday-Work$$', str(weekday_dict_duration['Thursday'][0]))
                        .replace('$$Thursday-Study$$', str(weekday_dict_duration['Thursday'][1]))
                        .replace('$$Thursday-Sport$$', str(weekday_dict_duration['Thursday'][2]))
                        .replace('$$Thursday-Social$$', str(weekday_dict_duration['Thursday'][3]))
                        .replace('$$Thursday-Spiritual$$', str(weekday_dict_duration['Thursday'][4]))
                        .replace('$$Thursday-Creative$$', str(weekday_dict_duration['Thursday'][5]))
                        .replace('$$Thursday-Chill$$', str(weekday_dict_duration['Thursday'][6]))
                        .replace('$$Thursday-Other$$', str(weekday_dict_duration['Thursday'][7]))
                        .replace('$$Friday-Work$$', str(weekday_dict_duration['Friday'][0]))
                        .replace('$$Friday-Study$$', str(weekday_dict_duration['Friday'][1]))
                        .replace('$$Friday-Sport$$', str(weekday_dict_duration['Friday'][2]))
                        .replace('$$Friday-Social$$', str(weekday_dict_duration['Friday'][3]))
                        .replace('$$Friday-Spiritual$$', str(weekday_dict_duration['Friday'][4]))
                        .replace('$$Friday-Creative$$', str(weekday_dict_duration['Friday'][5]))
                        .replace('$$Friday-Chill$$', str(weekday_dict_duration['Friday'][6]))
                        .replace('$$Friday-Other$$', str(weekday_dict_duration['Friday'][7]))
                        .replace('$$Saturday-Work$$', str(weekday_dict_duration['Saturday'][0]))
                        .replace('$$Saturday-Study$$', str(weekday_dict_duration['Saturday'][1]))
                        .replace('$$Saturday-Sport$$', str(weekday_dict_duration['Saturday'][2]))
                        .replace('$$Saturday-Social$$', str(weekday_dict_duration['Saturday'][3]))
                        .replace('$$Saturday-Spiritual$$', str(weekday_dict_duration['Saturday'][4]))
                        .replace('$$Saturday-Creative$$', str(weekday_dict_duration['Saturday'][5]))
                        .replace('$$Saturday-Chill$$', str(weekday_dict_duration['Saturday'][6]))
                        .replace('$$Saturday-Other$$', str(weekday_dict_duration['Saturday'][7]))
                        .replace('$$Sunday-Work$$', str(weekday_dict_duration['Sunday'][0]))
                        .replace('$$Sunday-Study$$', str(weekday_dict_duration['Sunday'][1]))
                        .replace('$$Sunday-Sport$$', str(weekday_dict_duration['Sunday'][2]))
                        .replace('$$Sunday-Social$$', str(weekday_dict_duration['Sunday'][3]))
                        .replace('$$Sunday-Spiritual$$', str(weekday_dict_duration['Sunday'][4]))
                        .replace('$$Sunday-Creative$$', str(weekday_dict_duration['Sunday'][5]))
                        .replace('$$Sunday-Chill$$', str(weekday_dict_duration['Sunday'][6]))
                        .replace('$$Sunday-Other$$', str(weekday_dict_duration['Sunday'][7]))
                        )
    
    # bar chart
    height_month = sorted(month_average)[-1] / days_passed * 1.2
    html_page = html_page.replace('$$HEIGHTMONTH$$', str(height_month))
    html_page = (html_page.replace('$$WORKMONTH$$', str(round(month_average[0] / days_passed, 2)))
                 .replace('$$STUDYMONTH$$', str(round(month_average[1] / days_passed, 2)))
                 .replace('$$SPORTMONTH$$', str(round(month_average[2] / days_passed, 2)))
                 .replace('$$SOCIALMONTH$$', str(round(month_average[3] / days_passed, 2)))
                 .replace('$$SPIRITUALMONTH$$', str(round(month_average[4] / days_passed, 2)))
                 .replace('$$CREATIVEMONTH$$', str(round(month_average[5] / days_passed, 2)))
                 .replace('$$CHILLMONTH$$', str(round(month_average[6] / days_passed, 2)))
                 .replace('$$OTHERMONTH$$', str(round(month_average[7] / days_passed, 2)))
                ) 
    return html_page