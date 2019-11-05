from flask_user import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from website import db, app

post_tags = db.Table('post_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.post_id'))
)


class Tags(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.String(100))



course_author = db.Table('course_author',
    db.Column('course_id', db.Integer, db.ForeignKey('course.course_id')),
    db.Column('author_id', db.Integer, db.ForeignKey('user.user_id'))
)

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    user_id = db.Column(db.INTEGER, primary_key=True)
    user_name = db.Column(db.String(120), nullable=False)
    user_qq = db.Column(db.String(120))
    user_mail = db.Column(db.String(120))
    password = db.Column(db.String(120))
    post = db.relationship('Post', backref='author', lazy='dynamic' )
    roles = db.relationship('Role', secondary='user_roles')
    course_auth = db.relationship('Course', secondary=course_author, backref=db.backref('course'))
    sharedfile = db.relationship('SharedFile', backref='author_shared', lazy='dynamic')




   # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id

    def __unicode__(self):
        return self.user_name



# Define the Role data-model
class Role(db.Model):
        __tablename__ = 'roles'
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
        __tablename__ = 'user_roles'
        id = db.Column(db.Integer(), primary_key=True)
        user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id', ondelete='CASCADE'))
        role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))





class Post(db.Model):

    __tablename__ = 'post'

    post_id = db.Column(db.INTEGER, primary_key=True)
    author_id = db.Column(db.INTEGER, db.ForeignKey('user.user_id'))
    post_date = db.Column(db.DateTime)
    post_content = db.Column(db.Text)
    post_title = db.Column(db.String(120), nullable=False)
    category_id = db.Column(db.INTEGER, db.ForeignKey('category.cat_id'))
    post_modified_date = db.Column(db.DateTime)
    tags = db.relationship(
        'Tags',
        secondary=post_tags,
        backref=db.backref('tags', lazy = 'dynamic'))





    def __unicode__(self):
        return self.user_name

    def to_json(self):
        return {
            'post_id': self.post_id,
            'author': self.author.user_name,
            'post_date': self.post_date,
            'post_content': self.post_content,
            'post_title': self.post_title,
            'category_id': self.cat.cat_name,
            'post_modified_date': self.post_modified_date,
        }



class Course(db.Model):

    __tablename__ = 'course'

    course_id = db.Column(db.INTEGER, primary_key=True)
    course_title = db.Column(db.String(120))
    course_description = db.Column(db.String(120))
    course_date = db.Column(db.String(120))
    syllabes = db.relationship('Syllabes', backref='course_syllabes', lazy='dynamic')
    assignment = db.relationship('Assignments', backref='course_assignments', lazy='dynamic')
    resources = db.relationship('Resources', backref='course_resources', lazy='dynamic')
    sharedfile = db.relationship('SharedFile', backref='course_file', lazy='dynamic')
    news = db.relationship('NewsCourse', backref='course_news', lazy='dynamic')
class Syllabes(db.Model):

    __tablename__ = 'syllabes'

    syllabes_id = db.Column(db.INTEGER, primary_key=True)
    syllabes_title =  db.Column(db.String(120))
    syllabes_description = db.Column(db.String(120))
    course = db.Column(db.INTEGER, db.ForeignKey('course.course_id'))

class NewsCourse(db.Model):

    __tablename__ = 'newscourse'

    news_id = db.Column(db.INTEGER, primary_key=True)
    news_title =  db.Column(db.String(120))
    news_description = db.Column(db.String(120))
    course = db.Column(db.INTEGER, db.ForeignKey('course.course_id'))

class Assignments(db.Model):

    __tablename__ = 'assignments'

    assignments_id = db.Column(db.INTEGER, primary_key=True)
    assignments_title = db.Column(db.String(120))
    assignments_description = db.Column(db.String(120))
    assignments_course= db.Column(db.INTEGER, db.ForeignKey('course.course_id'))
    sharedfile = db.relationship('SharedFile', backref='sharedfile_assign', lazy='dynamic')


class Resources(db.Model):

    __tablename__ = 'resources'

    resources_id = db.Column(db.INTEGER, primary_key=True)
    resources_title = db.Column(db.String(120))
    resources_description = db.Column(db.String(120))
    resources_shared_file = db.Column(db.INTEGER, db.ForeignKey('sharedfile.shared_file_id'))
    resources_course = db.Column(db.INTEGER, db.ForeignKey('course.course_id'))

class Test(db.Model):

    __tablename__ = 'test'

    test_id = db.Column(db.INTEGER, primary_key=True)

class SharedFile(db.Model):

    __tablename__ = 'sharedfile'

    shared_file_id = db.Column(db.INTEGER, primary_key=True)
    shared_file_title = db.Column(db.String(120))
    shared_file_path = db.Column(db.LargeBinary)
    resources = db.relationship('Resources', backref='sharedfile_res', lazy='dynamic')
    author = db.Column(db.INTEGER, db.ForeignKey('user.user_id'))
    course = db.Column(db.INTEGER, db.ForeignKey('course.course_id'))
    assignment = db.Column(db.INTEGER, db.ForeignKey('assignments.assignments_id'))

class Category(db.Model):

    __tablename__ = 'category'

    cat_id = db.Column(db.INTEGER, primary_key=True)
    cat_name = db.Column(db.String(120))
    cat_description = db.Column(db.String(120))
    post = db.relationship('Post', backref='cat', lazy='dynamic')

    def __unicode__(self):
        return self.cat_name

    @staticmethod
    def list_category():
        categories = Category.query.all()
        return [c.to_json() for c in categories]

    def to_json(self):
        return {
            'cat_id': self.cat_id,
            'cat_name': self.cat_name,
            'cat_description': self.cat_description
        }

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
