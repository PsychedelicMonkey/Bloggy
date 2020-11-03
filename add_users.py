from app.models import User, Post
from app import db

import json

users = [{
    "username": "test",
    "display_name": "testuser",
    "first_name": "Test",
    "last_name": "Test",
    "email": "test@test.com"
},
{
    "username": "ryan",
    "display_name": "ryan",
    "first_name": "Ryan",
    "last_name": "Getz",
    "email": "ryan@yahoo.com"
},
{
    "username": "joeschmoe",
    "display_name": "Joe Schmoe from Idaho",
    "first_name": "Joe",
    "last_name": "Schmoe",
    "email": "joe.schmoe@yahoo.com"
},
{
    "username": "hughjanus",
    "display_name": "Hugh Janus",
    "first_name": "Hugh",
    "last_name": "Janus",
    "email": "janus@yahoo.com"
},
{
    "username": "SKeel",
    "display_name": "SKeel",
    "first_name": "Stephan",
    "last_name": "Keeling",
    "email": "stephankeeling@yahoo.com"
},
{
    "username": "Zayne",
    "display_name": "Zayne",
    "first_name": "Zayne",
    "last_name": "Mccarty",
    "email": "zaynemccarty@yahoo.com"
},
{
    "username": "Alexandria",
    "display_name": "Alexandria",
    "first_name": "Alexandria",
    "last_name": "Rodrigues",
    "email": "alexandria.rodrigues@yahoo.com"
},
{
    "username": "Vivek",
    "display_name": "Vivek",
    "first_name": "Vivek",
    "last_name": "Cohen",
    "email": "vivek.cohen@yahoo.com"
},
{
    "username": "Lleyton",
    "display_name": "Lleyton",
    "first_name": "Lleyton",
    "last_name": "Iles",
    "email": "lleyton.iles@yahoo.com"
},
{
    "username": "Kyra",
    "display_name": "Kyra",
    "first_name": "Kyra",
    "last_name": "Plummer",
    "email": "kyra@yahoo.com"
},
{
    "username": "Hancock",
    "display_name": "Hancock",
    "first_name": "Zakary",
    "last_name": "Hancock",
    "email": "zacccccc@yahoo.com"
},
{
    "username": "Hanna",
    "display_name": "Hanna",
    "first_name": "Terrence",
    "last_name": "Hanna",
    "email": "thiccboi@yahoo.com"
},
{
    "username": "Edan",
    "display_name": "Edan",
    "first_name": "Edan",
    "last_name": "Rowland",
    "email": "edan@yahoo.com"
}]

for user in users:
    u = User(username=user['username'], display_name=user['display_name'], first_name=user['first_name'], last_name=user['last_name'], email=user['email'])
    u.set_password('123')
    db.session.add(u)
    print('User {} created.'.format(user['username']))

    for i in range(10):
        post = Post(title='Post {}'.format(str(i)), body="Lorem ipsum dolor, sit amet consectetur adipisicing elit. Nam unde ex ad cum tempora pariatur eaque iure libero! Deleniti aspernatur provident laudantium animi. Fugiat, commodi ea nisi quas aut quam.", author=u)
        db.session.add(post)
    db.session.commit()


all_users = User.query.all()
for user in all_users:
    for i in range(len(all_users)):
        if user == all_users[i]:
            continue
        user.follow(all_users[i])
        print('{} following {}'.format(user.username, all_users[i]))
    db.session.commit()