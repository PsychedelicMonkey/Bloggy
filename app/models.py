from flask_login import UserMixin
from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash

like = db.Table('like',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

share = db.Table('share',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('created', db.DateTime, default=datetime.utcnow)
)

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('timestamp', db.DateTime, default=datetime.utcnow)
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)            # used for the login manager
    display_name = db.Column(db.String(64), index=True, unique=True)        # used for displaying the username on pages
    first_name = db.Column(db.String(64), nullable=False)
    middle_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(164), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    about_me = db.Column(db.String(280), nullable=True)
    last_seen = db.Column(db.DateTime)

    avatar = db.Column(db.String(64), nullable=True)
    background_image = db.Column(db.String(64), nullable=True)

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    files = db.relationship('File', backref='user', lazy='dynamic')

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    shared_posts = db.relationship('Post', secondary='share', lazy='dynamic',
        backref=db.backref('shares', lazy='dynamic'))

    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy='dynamic')
    received_messages = db.relationship('Message', foreign_keys='Message.recipient_id', backref='recipient', lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.created_at.desc())

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(Message.created_at > last_read_time).count()

    def share_post(self, post):
        if not self.is_sharing(post):
            self.shared_posts.append(post)

    def unshare_post(self, post):
        if self.is_sharing(post):
            self.shared_posts.remove(post)

    def is_sharing(self, post):
        return self.shared_posts.filter(share.c.post_id == post.id).count() > 0


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    likes = db.relationship('User', secondary=like, lazy='dynamic',
        backref=db.backref('likes', lazy='dynamic'))

    def __repr__(self):
        return '<Post {}>'.format(self.title)

    def is_liked(self, user):
        return self.likes.filter(like.c.user_id == user.id).count() > 0


class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    url = db.Column(db.String(120), nullable=True)
    file_author = db.Column(db.String(120), nullable=True)
    file_author_url = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return '<File {}>'.format(self.name)


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)