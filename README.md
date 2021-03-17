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
   
### Functions provided
#### Teacher Version
1. Edit Profile
2. Add Class
3. Enter into a specific class (by clicking course code)
4. View historical question
5. Add question
6. Start a (default) question
7. See Student Participation
8. Reward coupon for student
9. Use coupon for student

#### Student Version
1. Register Class
2. Enter into a specific class (by clicking course code)
3. Answer Question
4. View historical attempts

### Models Designed
Totally there are five models: user(account), course, question,
answer, coupon, as defined in `models.py`

### Database Used
We use Mysql as database to store all information.



