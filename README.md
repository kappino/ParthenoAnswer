# ParthenoAnswer
This is a project for "web technologies" exam at the University of Naples Parthenope. The authors of this project are Aiello Riccardo, Esposito Crescenzo and the student representative Genovese Aniello.

HOW TO RUN: 
To run the web app locally, follow these instructions:
1) Pull the project and link correctly the Python interpreter for the virtual environment.
   - To do so in PyCharm, go to Settings -> Project: ParthenoAnswer -> Python Interpreter and select your interpreter of choice, then add a configuration and select it; in alternatively you can install the few required modules manually and run it as you please.

2)When, you must install docker, open the terminal and follow these instructions to set it up correctly.
2.1)docker pull mongo;
2.2)docker volume create --name=mongodata
2.3)docker run --name mongodb -v mongodata:/data/db -d -p 27017:27017 mongo

3) Run python app.py (Only in your folder of the project).

4)Open your browser to localhost.

5)Welcome into ParthenoAnswer! 

Link to personal Github repository:
https://github.com/nellogen/ParthenoAnswer

