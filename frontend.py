import backend
import re

def home(time, username="Guest"):
    if username is not "Guest":
        link = "/profile/" + str(re.sub('[^A-Za-z0-9]+','',str(backend.encryptedtext(username))))
    else:
        link = "/"
    return '''<!DOCTYPE html> 
<html>
    <head>
        <title>Little Sissy Domor</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script>
        <link rel="stylesheet" href="/static/index.css">
        <link rel="shortcut icon" href="/static/Logo.png">
    </head>
    <body>
        <nav class="navbar navbar-expand-md navbar-custom fixed-top">
            <li class="navbar-brand"><a href="https://domor8123.github.io/little_sissy_domor"><img src="/static/navbarlogo.png" alt="Little Sissy Domor Logo"></a></li>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#collapsenavbar">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="collapsenavbar">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href= >''' + username + '''</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="https://domor8123.github.io/little_sissy_domor/index.html#about">About Me</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="https://www.pornhub.com/model/little_sissy_domor">Ponrhub Porfile</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="https://domor8123.github.io/little_sissy_domor/Update.html">Additional plans/update-log</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="https://domor8123.github.io/little_sissy_domor/Contact.html">Contact/Tip Information</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/amazonWishlist">Amazon Wish List</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/chast">Lock Me</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/member-signup">Sign up</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/member-login">Log in</a>
                    </li>
                </ul>
            </div>
        </nav>
        <h2 class="gap"></h2>
        <div class="show-picture">
            <div class="row">
                <div class="col-md-12">
                    <div align="center">
                        <img src="/static/Banner.png">
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <div align="center">
                    <h1>'''+ time + '''</h1>
                </div>
            </div>
        </div>
    </body>
    <footer>
        <div class="row">
            <div class="col-md-4">
                <div align="center">
                    <img src="/static/Logo.png">
                </div>
            </div>
            <div class="col-md-4">
                <div align="center">
                    <h4><strong>Navigation</strong></h4>
                    <p><a href="https://domor8123.github.io/little_sissy_domor/index.html#about">About Me</a></p>
                    <p><a href="https://www.pornhub.com/model/little_sissy_domor">Pornhub Profile</a></p>
                    <p><a href="https://domor8123.github.io/little_sissy_domor/Update.html">Additional Plans/Change-log</a></p>
                    <p><a href="https://domor8123.github.io/little_sissy_domor/Contact.html">Contact/Tip Information</a></p>
                    <p><a href="/amazonwishlist">Amazon Wishlist</a></p>
                    <p><a href="/member-signup">Sign up</a></p>
                    <p><a href="/member-login">Login</a></p>
                </div>
            </div>
            <div class="col-md-4">
                <h4 align="center"><strong>Contact Information</strong></h4>
                <p align="center"><a href="mailto:domor8123@gmail.com">Email Me</a></p>
                <p align="center"><a href="https://www.pornhub.com/model/little_sissy_domor">Pornhub Profile</a></p>
            </div>
        </div>
    </footer>
</html>'''

def profile(username):
    if username is not "Guest":
        link = "/profile/" + str(re.sub('[^A-Za-z0-9]+','',str(backend.encryptedtext(username))))
    else:
        link = "/"
    return '''<!DOCTYPE html> 
<html>
    <head>
        <title>Little Sissy Domor</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script>
        <link rel="stylesheet" href="/static/index.css">
        <link rel="shortcut icon" href="/static/Logo.png">
    </head>
    <body>
        <nav class="navbar navbar-expand-md navbar-custom fixed-top">
            <li class="navbar-brand"><a href="https://domor8123.github.io/little_sissy_domor"><img src="/static/navbarlogo.png" alt="Little Sissy Domor Logo"></a></li>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#collapsenavbar">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="collapsenavbar">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href=>''' + username + '''</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="https://domor8123.github.io/little_sissy_domor/index.html#about">About Me</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="https://www.pornhub.com/model/little_sissy_domor">Ponrhub Porfile</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="https://domor8123.github.io/little_sissy_domor/Update.html">Additional plans/update-log</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="https://domor8123.github.io/little_sissy_domor/Contact.html">Contact/Tip Information</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/amazonWishlist">Amazon Wish List</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/chast">Lock Me</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/member-signup">Sign up</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/member-login">Log in</a>
                    </li>
                </ul>
            </div>
        </nav>
        <h2 class="gap"></h2>
        <div class="show-picture">
            <div class="row">
                <div class="col-md-12">
                    <div align="center">
                        <img src="/static/Banner.png">
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <div align="center">
                    <h1> Hello '''+ username + '''</h1>
                </div>
            </div>
        </div>
        <form method="POST" action="/profile-updated">
            <div class="row">
                <div class="col-md-12">
                    <h1 align="center"><strong>Account Settings</strong></h1>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <div align="center">
                        <input type="text" name="previousUsername" id="previousUsername" class="form-control" placeholder="Previous/Current username" required><br>
                        <input type="text" name="changeUsername" id="changeUsername" class="form-control" placeholder="new username"><br>
                        <input type="password" name="changePassword" id="changePassword" class="form-control" placeholder="new password"><br>
                        <input type="password" name="changecheckPassword" id="changecheckPassword" class="form-control" placeholder=" confirm new password"><br>
                        <input type="email" name="changeEmail" id="changeEmail" class="form-control" placeholder="new email"><br>
                        <input type="email" name="changecheckEmail" id="changecheckEmail" class="form-control" placeholder="confirm new email"><br>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <div align="center">
                        <button id="Save" class="button" type="submit" value="Save">Save</button>
                        <p> Might not be able to handle multiple changes, so I recommend to change one thing at a time </p>
                    </div>
                </div>
            </div>
        </form> 
    </body>
    <footer>
        <div class="row">
            <div class="col-md-4">
                <div align="center">
                    <img src="/static/Logo.png">
                </div>
            </div>
            <div class="col-md-4">
                <div align="center">
                    <h4><strong>Navigation</strong></h4>
                    <p><a href="https://domor8123.github.io/little_sissy_domor/index.html#about">About Me</a></p>
                    <p><a href="https://www.pornhub.com/model/little_sissy_domor">Pornhub Profile</a></p>
                    <p><a href="https://domor8123.github.io/little_sissy_domor/Update.html">Additional Plans/Change-log</a></p>
                    <p><a href="https://domor8123.github.io/little_sissy_domor/Contact.html">Contact/Tip Information</a></p>
                    <p><a href="/amazonwishlist">Amazon Wishlist</a></p>
                    <p><a href="/member-signup">Sign up</a></p>
                    <p><a href="/member-login">Login</a></p>
                </div>
            </div>
            <div class="col-md-4">
                <h4 align="center"><strong>Contact Information</strong></h4>
                <p align="center"><a href="mailto:domor8123@gmail.com">Email Me</a></p>
                <p align="center"><a href="https://www.pornhub.com/model/little_sissy_domor">Pornhub Profile</a></p>
            </div>
        </div>
    </footer>
</html>
    '''