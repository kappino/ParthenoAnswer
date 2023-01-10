# ParthenoAnswer
This is a project for "web technologies" exam at the Parthenope University of Naples. The authors of this project are Aiello Riccardo, Esposito Crescenzo and the student representative Genovese Aniello.


Features:

-Authentication system using University of Naples "Parthenope" API (base64 encoding), giving access only with the university credentials

-Standard user role (permissions to create posts and add replies)

-Admin user role (same permissions as a standard user with the added possibility to add categories(usually academic year) and inside each category a different subcategory(subject)

-When there is user=1 in Database, this is an admin, elseo if the user is = 0 it will not have the necessary permissions for categories or sub-categories. (IT IS VERY IMPORTANT!) 

-Badge to show if a user has passed the exam for the related post

-User profile page created using "Parthenope" API showing personal info and passed exams



HOW TO RUN: 

To run the web app locally, follow these instructions:

1) Pull the project and link correctly the Python interpreter for the virtual environment.
2)- To do so in PyCharm, go to Settings -> Project: ParthenoAnswer -> Python Interpreter and select your interpreter of choice, then add a configuration and select it; in alternatively you can install the few required modules manually and run it as you please.

2)When, you must install docker, open the terminal and follow these instructions to set it up correctly.

2.1)docker pull mongo;

2.2)docker volume create --name=mongodata

2.3)docker run --name mongodb -v mongodata:/data/db -d -p 27017:27017 mongo

3) Run python app.py (Only in your folder of the project).

4)Open your browser to localhost.

5)Welcome into ParthenoAnswer! 


Link to personal Github repository:
https://github.com/nellogen/ParthenoAnswer


Link to personal presentation: 
https://docs.google.com/presentation/d/1acokhrSv6ViCC0ifGJNpaGh7cAvWs-Lu2_-upTQE1tA/edit#slide=id.p
