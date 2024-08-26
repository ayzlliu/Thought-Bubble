# Thought Bubble
#### Video Demo:  <https://youtu.be/oNE34uasPLQ>
#### Description:

Hello! For my CS50 project I decided to design and implement a Web Application platform using Python, JavaScript, HTML, and SQL that allows users to register for an account on and post their daily blogs.

My project includes a front-end which interfaces with a simple SQL database on the back-end which stores the users' account and blog informations. The database is comprised of two tables: Users and Posts.

Within the Users table are columns that store the users' id, username, password hash, and their blogs count.

Within the Posts table are columns that store the posts' id, the id of the respective user, title, content, and the time the blog was created at.

These two tables allow me to effectively store all information recorded on the web application and be manipulated through SQL queries.

To implement the front-end, I used a series of templates each serving a different functionality:

layout.html: displays the overall layout of the web application, including the logo, copyright tag, and Log In page.

register.html: displays the register page.

error.html: this page is rendered everytime a client-side error occurs, such as incorrect passwords, unmatching passwords when registering, using a previsouly registered username, etc.

post.html: this page allows the user to post a blog.

home.html: displays all of the users' current blogs (if any), as well as the user's current blog count. If the user has no blogs, a message will be displayed guiding the user to post a blog.

To implement the backend functionalities, I created and used a python file (app.py) that contains all the necessary functions, such as logging in, registration, posting, editing, and deleting blogs, etc.

Debated Choices:

Making the Web App interactive between Users:
    I initially planned to have a comments table within my SQL database that stores comments made by other users. I wanted my Web App to perform similarly as Instagram's commenting feature. However, I soon changed my mind to have my Web App to be more user-private, where the user's can post blogs that are only seen by themselves.

Having a streak feature:
    I also wanted to have a streaks feature similar to those of snapchat and duolingo's. But I couldn't figure out a way to implement a streaks feature without using a local storage. I soon changed my mind to displays the user's current blog count instead of their days of consecutively blogging.

Overall Functionality:

When a user launches my Web App, they will be greeted with the message: "Welcome to Thought Bubble!", and "This is a Web Application For You to Post Your Blogs!". If the user is not a returning user, they can register for an account by pressing the register button, and register.html will be rendered.

Within the registration page are inputs that require the user to input a username that is unregistered, a password, and a verification password which must match the password. Should the user try to register with an existing username or fail to match the passwords, error.html will be rendered to display the appropriate error messages. For example, if the user tries to register with the previously registered username "cs50", an error page with the message "Username already exists!" will be displayed to the user.

Once the user successfully registers for an account and signs in, they will see a message saying "No blogs yet, post one!", prompting the user to post their first blog by pressing the Post a New Blog button.

Within the post.html page are two fields: title and content that requires the user to input the blog's title and the content they'd like to post. Once finished, the user may press Post! to post their blog. The blog's title and content will then be stored in the SQL database.

Once the blog is posted, the user is redirect back to home, displaying the new blog, with their blogs count incremented by 1. The blog is displayed as a button that shows the blog's title and time created at. When the blog button is pressed, the blog's content will be displayed in a popup. The user may then be able to choose to edit or delete the blog.

If the user chooses to edit the blog, a popup will appear with editable fields that displays the blog's title and content, allowing the user to make changes. Once done, the user may press the save button to update the SQL database with the changed version. If the user chooses to delete the blog, the blog will be removed from the database with the user's blogs count decremented by 1.


That's about it, I hope you found this useful!
