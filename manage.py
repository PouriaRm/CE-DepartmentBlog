from flask_script import Manager
from werkzeug.security import generate_password_hash

from website import db
from website.models import Post, Category, Tags, Course, Syllabes, Assignments, Resources, SharedFile, User, Role
from website.untitled1 import app

manager = Manager(app)


def buildPosts():
    posts = []
    con = """
    The new ComposerLinter subclass has been created, if you maintain or use a linter that uses Composer to install the dependency. Consider having that linter use ComposerLinter to get added
  benifits!

  JRuby <http://jruby.org/> support has been added! Any linter that uses the RubyLinter subclass will have search for jruby if no other ruby executable is found.

  You may have also noted SublimeLinter run a little faster lately. That's because in the last update we switched to the new usage of the async eventlisteners. You shouldn't see any negative effects but if you do please reach out to use in our Issue Tracker <https://github.com/SublimeLinter/SublimeLinter3/issues>

  Thank you for the continued support of SublimeLinter! We are extremely appreciative of your usage, support, and contributions.


    """
    for i in range(1, 6):
        u = User( user_name = "ahmad " + str(i), password="tt")

        db.session.add(u)


        p = Post(post_title="title" + str(i),
                 post_content = con + "",
                 post_date= "2017",
                 author_id= i,
                 category_id =i)


        db.session.add(p)
        c = Category(cat_name = "catgo " + str(i))
        db.session.add(c)
        admin = User('admin', 'admin@example.com')
        # posts.append(p)

    db.session.commit()
    return posts

def buildnewpost():
    u = User(user_name="اضعر فرهادی")
    db.session.add(u)
    c1 = Category(cat_name = "فرم ها")
    db.session.add(c1)
    c2 = Category(cat_name="وضعیت کلاس ها")
    db.session.add(c2)
    c3 = Category(cat_name="سرفصل دروس")
    db.session.add(c3)
    c4 = Category(cat_name="رشته های موجود")
    db.session.add(c4)
    c5 = Category(cat_name="آرشیو اخبار")
    db.session.add(c5)


    p = Post(post_title="همایش",
             post_content= "همایش بزرگ مهندسین کامپیوتر در سرزمین دنیای کامپیوتر",
             post_date="2017/6/12",
             author = u,
             cat = c2)
    db.session.add(p)

    t= Tags(tagname = "کامپیوتر")
    db.session.add(t)
    t.tags.append(p)
    db.session.commit()

def buildtags():
    t1 = Tags(tagname="الصاق")
    db.session.add(t1)
    t1 = Tags(tagname="درس")
    db.session.add(t1)
    t1 = Tags(tagname="وضعیت")
    db.session.add(t1)
    t1 = Tags(tagname="آرشیو")
    db.session.add(t1)
    db.session.commit()

def buildCourse():

    u1 = User(user_name="اضعر فرهادی")
    cour1 = Course(course_title = "برنامه سازی پیشرفته",
                   course_description="جاوا",
                   author=u1,
                   course_date="پاییز-96"
                   )
    db.session.add(cour1)
    file1 = SharedFile(shared_file_title="book",
                       shared_file_path="book.pdf")
    db.session.add(file1)
    syllab = Syllabes(syllabes_title="10 نمره پروژه",
                      course_syllabes=cour1)
    db.session.add(syllab)
    assign = Assignments(assignments_title="سوال هفته",
                         assignments_description="برنامه ایی بنویسید که لیست صورت حساب ها را نشان بدهد.",
                         course_assignments=cour1)
    db.session.add(assign)
    reourse = Resources(resources_title="کتاب",
                        sharedfile=file1,
                        course_resources=cour1
                        )
    db.session.add(reourse)
    db.session.commit()

def userdefine():
    u = User(user_name="Mammad",
             user_type=1)
    db.session.add(u)
    db.session.commit()
def usercourse():

    u = User.query.filter_by(user_name="alireza").first()
    cour1 = Course(course_title="ساختمان داده",
                   course_description="ساختمان داده ارائه شده در این ترم",
                   course_date="پاییز-96"
                   )


    u.course_auth.append(cour1)
    db.session.add(cour1)
    db.session.commit()

def definerole():
    u1 = User(user_name="Ebrahimi",password=generate_password_hash("123456"),user_mail="Ebrahimi@gmail.com")
    u1.roles.append(Role(name='Teacher'))
    db.session.add(u1)

    u2 = User(user_name="Nahvi", password=generate_password_hash("123456"), user_mail="Nahvi@gmail.com")
    u2.roles.append(Role(name='Student'))
    db.session.add(u2)

    u3 = User(user_name="Malekzade", password=generate_password_hash("123456"), user_mail="Malekzade@gmail.com")
    r2 = Role.query.filter_by(name="Teacher").first()
    u3.roles.append(r2)
    db.session.add(u3)

    u4 = User(user_name="Azimi", password=generate_password_hash("123456"), user_mail="Azimi@gmail.com")
    r3 = Role.query.filter_by(name="Student").first()
    u4.roles.append(r3)
    db.session.add(u4)

    db.session.commit()

@manager.command
def initdb():

    """ Create database """
    db.create_all()
    #usercourse()
    #userdefine()
    #buildtags()
    #buildnewpost()
   # posts = buildPosts()
   # buildCourse()
    print('Successful')

@manager.command
def dropall():
    """ Drop database """
    db.drop_all()
    print('Successful')

def getquery(Post):
   posts =  Post.query.all()
   print(posts)
   return posts

if __name__ == '__main__':
    initdb()
    #definerole()
    #getquery(User)
    #manager.run()
