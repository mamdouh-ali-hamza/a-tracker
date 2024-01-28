A-Tracker : Track your Daily Activities
## MY FINAL PROJECT
Track what activities you do daily and add information like name, category, date, and duration of activities in minutes. Then visulaize your activities in charts to get benifit from the dashboard to track your activities.

- What does it do?  
  This is a web project which tracks my daily activities and make a dashboard of charts to make visulaizations about daily, week and month activities.

- What is the "new feature" which you have implemented that we haven't seen before?  
  Chart drawing library graphs the user data

## Prerequisites
Flask: pip install Flask
Charts.css:
The files needed already included in /static/dis/ . Charts.css latest release can be downloaded from https://github.com/ChartsCSS/charts.css/releases and copy the dist/charts.min.css file to the project then load the CSS file in the HTML documentusing <link> tag and place it inside the document <head>.

## To RUN Project
Run this command: FLASK_APP=tracker.py flask run

## Project Checklist
- [x] It is available on GitHub.
- [x] It uses the Flask web framework.
- [x] It uses at least one module from the Python Standard Library other than the random module.
  Please provide the name of the module you are using in your app.
  - Modules name: os, datetime
- [x] It contains at least one class written by you that has both properties and methods. It uses `__init__()` to let the class initialize the object's attributes (note that  `__init__()` doesn't count as a method). This includes instantiating the class and using the methods in your app. Please provide below the file name and the line number(s) of at least one example of a class definition in your code as well as the names of two properties and two methods.
  - File name for the class definition: tracker.py
  - Line number(s) for the class definition: 12
  - Name of two properties: name, category, date, duration
  - Name of two methods: make_activity(), get_weekday_name()
  - File name and line numbers where the methods are used: tracker.py, 139, 92:104
- [x] It makes use of JavaScript in the front end and uses the localStorage of the web browser.
- [x] It uses modern JavaScript (for example, let and const rather than var).
- [x] It makes use of the reading and writing to the same file feature.
- [x] It contains conditional statements. Please provide below the file name and the line number(s) of at least
  one example of a conditional statement in your code.
  - File name: tracker.py
  - Line number(s): 41, ...
- [x] It contains loops. Please provide below the file name and the line number(s) of at least
  one example of a loop in your code.
  - File name: tracker.py
  - Line number(s): 167, ...
- [x] It lets the user enter a value in a text box at some point.
  This value is received and processed by your back end Python code.
- [x] It doesn't generate any error message even if the user enters a wrong input.
- [x] It is styled using CSS.
- [x] The code follows the code and style conventions as introduced in the course, is fully documented using comments and doesn't contain unused or experimental code. 
  In particular, the code should not use `print()` or `console.log()` for any information the app user should see. Instead, all user feedback needs to be visible in the browser.  
- [x] All exercises have been completed as per the requirements and pushed to the respective GitHub repository.