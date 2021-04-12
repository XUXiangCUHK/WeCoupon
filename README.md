# WeCoupon - Project of CSCI3100

## Phase One: Initial Design Report
### Status: completed

## Phase Two: Initial Code of Project
### Running on local machine
We provide app_test.py file for execution on local machine.
You can simply run `python app_test.py` and then open the website.
It is a sample page only used for demonstration with dummy data.

### Login as predefined user
`Login address: http://127.0.0.1:5000/login` or `~/login` 

In order to login, you can use our predefined users.

1. For student:
   ```email: student@gmail.com```
   ```password: 1```
2. For teacher:
   ```email: teacher@gmail.com```
   ```password: 1```

In order to log out, you can click the Log out button.
   
### Functions provided
#### Teacher Version 
##### 1. Add Class
Click the ADD CLASS button and fill in the class info form, and then a new class can be created in the database. When running app.py with our MySQL database, you can see the new one added into the class list. When running app_test.py, you can only submit the form without bugs, but there is nothing changed in the class list because of the dummy data.
##### 2. Enter into a specific class (by clicking course code)
When running app_test.py, the course ESTR4999 is used to show the following functions so you are advised to click this code.
##### 3. View historical question
In the Question page, there is a list of posted questions. You can view their their detailed information and historical answers by clicking the View button.
##### 4. Add question
In the Question page, you can create a new question by clicking the Add question button and filling the form. When running app.py with our MySQL database, you can see the new one added into the question bank. When running app_test.py, you can only submit the form without bugs, but there is nothing changed in the list because of the dummy data.
##### 5. Start a (default) question
In the Question page, you can start a session for students answering a predefined question by clicking the Start button or a default question by clicking the Start default question button. Then you will be redirected to the page showing the constantly updated student answers. After you click the STOP COLLECTING button, the session will be ended and you can see the final sorted answer list and the participation of this question.
##### 6. See Student Participation
After entering into a specific class, you can see the participation in this class in the Participation page. The SID, name, the number of attempts to answer questions, the number of coupons rewarded and the number of coupons used of all students who have registered for this course will be displayed.
##### 7. Reward coupon for student
In the viewing answers page, you can click the Reward button to choose an answer to give a coupon.
##### 8. Use coupon for student
After entering into a specific class, you can click the Use button to use a coupon for a student in the Participation page. When running app.py with our MySQL database, you can see that the coupon data will be changed. When running app_test.py, you can only submit click the button without bugs, but there is nothing changed in the list because of the dummy data.

#### Student Version
##### 1. Register Class
Click the REG CLASS button and fill in the class token, and then you will register a new class if a class with this token is in the database. When running app.py with our MySQL database, you can see the new one added into the class list. When running app_test.py, you can only submit the token without bugs, but there is nothing changed in the class list because of the dummy data.
##### 2. Enter into a specific class
Just click course code.
##### 3. Answer Question
In the Answer page, if there is no question to answer now, you will see a warm reminder. After the instructor start a session for answering, you will see the details of the questiong and get a form to fill in your answer and submit it.
##### 4. View historical attempts
After entering into a specific class, you can see your participation in this class in the Participation page. There is a question list containing the historical questions of this class, your historical answers, the suggested answers and the coupon acquisition status. 

### Models Designed
Totally there are five models: user(account), course, question,
answer, coupon, as defined in `models.py`

### Database Used
We use Mysql as database to store all information.
