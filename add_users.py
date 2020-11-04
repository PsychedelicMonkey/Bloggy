from app.models import User, Post
from app import db

import os
import json
import random
import string


people = 'app/static/images/people'
background = 'app/static/images/background'

first_names = json.loads(open('first_names.json').read())
last_names = json.loads(open('last_names.json').read())

for name in last_names:
    first_name = random.choice(first_names)
    display_name = first_name + name
    username = display_name.lower()
    email = ''.join(first_name.lower() + '.' + name.lower() + '@yahoo.com')

    user = User(
        username=username,
        display_name=display_name,
        first_name=first_name,
        last_name=name,
        email=email
    )
    user.set_password('123')
    user.avatar = random.choice(os.listdir(people))
    user.background_image = random.choice(os.listdir(background))
    print ('Creating Username={}'.format(user.username))

    for i in range(5):
        post = Post(
            title='Post {}'.format(str(i)),
            body='Lorem ipsum dolor, sit amet consectetur adipisicing elit. Nam unde ex ad cum tempora pariatur eaque iure libero! Deleniti aspernatur provident laudantium animi. Fugiat, commodi ea nisi quas aut quam.',
            author=user
        )
        db.session.add(post)
    db.session.commit()

# Add followers
all_users = User.query.all()
for user in all_users:
    for i in range(len(all_users)):
        if user == all_users[i]:
            continue
        user.follow(all_users[i])
        print('{} following {}'.format(user.username, all_users[i]))
    db.session.commit()