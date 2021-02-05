# **Official Little Sissy Domor membership site public version**

## **What is this?**
- A secure custom website designed for my fan club members 
- Uses PGSQL as database 
- Main language is python and html 

## **What will happen in the future**
- More social media options
- More options for chastity time 
- Please email [me](mailto:domor8123@gmail.com) if you have any sugguestions for the website or content that I should add 

## **File/Folder Information**
- [timer.py](timer.py)
    - Custom countdown time that updates database every seciond with a new value
- [requirements.txt](requirements.txt)
    - Text file that tells you all modules I used to make this project
- [Procfile](Procfile)
    - File that tells Heroku what I need to run every single time
- [information.json](information.json)
    - File that has all credentials to make it easier to edit and implement everywhere
- [frontend.py](frontend.py)
    - Python file that allows all dynamic content like username change and coundown timer change
- [backend.py](backend.py)
    - Python file that hosts all things hidden like the data being uploaded to the database 
- [app.py](app.py)
    - Python file that shows all routes and what can be ran through the web server
- [static](/static)
    - All files that won't change and can be kept 