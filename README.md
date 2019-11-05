# CE Department Blog
A blogging engine based on Flask. For an [Flask](https://palletsprojects.com/p/flask/) Core version. Perfect for academic Department to self-host a blog.


## Features
•	Three-level of permission access consists of the admin user, professor and student<br>
•	Adding, updating and deleting posts as an admin user and professor<br>
•	Uploading Assignments with a specific deadline for each course<br>
•	Separating each course and post with specific tags and categories<br>
•	Session Management<br>
• Simple Templates<br>
• MySQL Database<br>
• User Logins and Registeration<br>
• Profile Page and Course Page<br>
• Error Handling<br>
• Class Followers<br>
• Pagination<br>
• Setting easy dates and times for deadlines<br>
• Using Ajax<br>
• Full-Text Search<br>
• Some JavaScript Magic<br>
• User Notifications for assignments in their panel<br>
• Application Programming Interfaces (APIs)<br>

## How to run it on your host?
If you don't know how to run flask project or even have no idea about pip please check [this article](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).

After you make sure about doing everything correctly, follow the diagram of the project structure:
```
CE DepartmentBlog/
  website/
   untitled1.py
```
In this path, Please run below instructions in the console:
```
flask run
```
## MySQL Setting
This project is usuing SQLALCHEMY as a python connector to mysql.
To change setting, please change the config file to your destination config.
```
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://MySQLUserName:MySqlPassword@Yourhost'
```
