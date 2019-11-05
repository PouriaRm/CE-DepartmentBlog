import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
from flask_login import login_user, current_user, login_required, logout_user
from flask_user import roles_required
from pip._vendor.requests import auth
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from website import app, login_manager, ALLOWED_EXTENSIONS
from website.models import Post, User, Tags, Category, db, Course, Syllabes, Resources, Assignments, SharedFile, \
    NewsCourse


@app.route('/')
@app.route('/index')
def index():
    posts = Post.query.all()

    tag_name = []
    for p in posts:
     post = p.tags
     print(p.tags)
     for tag in p.tags:
         print(tag.tagname)
         tag_name.append(tag.tagname)

    print("start")
    print(tag_name)
    print(" end")
    return render_template("index.html", post = posts, tag_name = tag_name)

@app.route('/index_admin_edit/<postid>')
@login_required
@roles_required('Admin')
def index_admin_edit(postid):

    post = Post.query.all()
    posts = Post.query.filter_by(post_id=postid).first()
    if request.method == 'POST':

        auth = User.query.filter_by(user_name=current_user.user_id).first_or_404()
      #  print(post)

        cats= Category.query.filter_by(posts=request.form['cat']).first_or_404()
        print(cats.cat_id)

        post.post_title=  request.form['name']
        post.post_content=request.form['comment']
        post.post_date="2017",
        post.author= auth,
        post.cat= cats
        if Tags.query.filter_by(tagname=request.form['tag']).first():
            t = Tags.query.filter_by(tagname=request.form['tag']).first()
        else:
             t = Tags(tagname = request.form['tag'])

        db.session.commit()

    return render_template("index_admin.html", post = posts, tag_name = t.tagname, useredit=True)


@app.route('/course/hwlist/<coursetime>')
@login_required
@roles_required('Teacher')
def hw_list(coursetime):

    auther = User.query.filter(User.course_auth.any(course_id=coursetime)).filter(User.roles.any(id=2)).first()
    print(auther)
    sharedfile = SharedFile.query.filter_by(author=auther.user_id).all()
    course = Course.query.filter_by(course_id=coursetime).first()

    return render_template("hwlist.html", sharedfile=sharedfile, author=auther.user_name, course=course.course_title)

@app.route('/index_admin_del/<postid>')
@login_required
@roles_required('Admin')
def index_admin_del(postid):

    p =Post.query.filter_by(post_id=postid).first()
    db.session.delete(p)
    db.session.commit()

    return redirect(url_for('index_admin_edit', postid=postid))

@app.route('/webservice')
def webservice():
    posts = Post.query.all()

    data = [post.to_json() for post in posts]
    print(data)

    return jsonify(data)
@app.route('/testwebservice')
def test_webservice():
    return render_template("webservice.html")

@app.route('/login', methods = ('GET' , 'POST'))
def login():
    if request.method == "POST":
        if request.form['username'] == '' or request.form['username'] == None:
            print('Not exists')
            redirect(url_for(login))
        if request.form['password'] == '' or request.form['password'] == None:
             print('Not exists')
             redirect(url_for(login))
        user = db.session.query(User).filter_by(user_name=request.form['username']).first()
        if user is not None and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(request.args.get('next') or url_for('index'))
    print(current_user)
    return render_template("login.html")

@app.route('/register', methods = ('GET' , 'POST'))
def register():
    if request.method == "POST":
        print("ented to register")
        u = User(user_name=request.form['username'], password = generate_password_hash(request.form['password']))
        db.session.add(u)
        db.session.commit()
        print("hashpassword: " + generate_password_hash(request.form['password']))
        #redirect(url_for(index))
    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('index')

@app.route('/aboutus')
def aboutus():
    return render_template("aboutus.html")

@app.route('/coursetimeline')
def coursetimeline():
    return render_template("coursetimeline.html")

@app.route('/courselist/<coursetime>')
def courselist(coursetime):
    courses = Course.query.filter_by(course_date=coursetime).all()

    authers = []
    for c in courses:
     print(c.course_title)
     auther = User.query.filter(User.course_auth.any(course_id=c.course_id)).filter(User.roles.any(id=2)).first()
     authers.append(auther.user_name)
     print(auther.user_name)
    return render_template("courselist.html", course = courses, author=authers)

@app.route('/course/<coursetime>')
@login_required
def course(coursetime):
    item = Course.query.filter_by(course_id=coursetime).first()
    news = NewsCourse.query.filter_by(course=coursetime).all()

    auther = User.query.filter(User.course_auth.any(course_id=item.course_id)).filter(User.roles.any(id=2)).first()

    if current_user.user_id == auther.user_id:
        return redirect(url_for('course_teacher', coursetime=coursetime))
    #for c in courses:
    # print(c.course_title)

    return render_template("course.html", news=news, author= auther.user_name, item=item)

@app.route('/course_teacher/<coursetime>', methods = ('GET' , 'POST'))
@roles_required('Teacher')
@login_required
def course_teacher(coursetime):
    item = Course.query.filter_by(course_id=coursetime).first()
    news = NewsCourse.query.filter_by(course=coursetime).all()

    auther = User.query.filter(User.course_auth.any(course_id=item.course_id)).filter(User.roles.any(id=2)).first()

    if request.method == 'POST':
        a = NewsCourse(news_title=request.form['name'],
                 news_description=request.form['comment'],
                 course=item.course_id)
        db.session.add(a)
        db.session.commit()

    return render_template("course_teacher.html", news = news, author= auther.user_name, item = item )

@app.route('/course_teacher_del/<coursetime>/<coursenews>', methods = ('GET' , 'POST'))
@roles_required('Teacher')
@login_required
def course_teacher_del(coursetime,coursenews):

    a = NewsCourse.query.filter_by(news_id=coursenews).first()
    db.session.delete(a)
    db.session.commit()

    return redirect(url_for('course_teacher', coursetime=coursetime, coursenews=coursenews))


@app.route('/course_teacher_edit/<coursetime>/<coursenews>', methods = ('GET' , 'POST'))
@roles_required('Teacher')
@login_required
def course_teacher_edit(coursetime,coursenews):
    item = Course.query.filter_by(course_id=coursetime).first()
    news = NewsCourse.query.filter_by(course=coursetime).all()

    auther = User.query.filter(User.course_auth.any(course_id=item.course_id)).filter(User.roles.any(id=2)).first()

    if request.method == 'POST':
        a = NewsCourse.query.filter_by(news_id=coursenews).first()
        a.news_title=request.form['name']
        a.news_description=request.form['comment']
        a.course=item.course_id
        db.session.commit()

    return render_template("course_teacher.html", news = news, author= auther.user_name, item = item, useredit=True )



@app.route('/course/syllabes/<coursetime>')
@login_required
def syllabes(coursetime):
    item = Course.query.filter_by(course_id=coursetime).first()
    courses = Syllabes.query.filter_by(course_syllabes=item).first()

    print(courses)
    #for c in courses:
    # print(c.course_title)

    return render_template("syllabes.html", course = courses)

@app.route('/course/resources/<coursetime>')
@login_required
def resources(coursetime):
    item = Course.query.filter_by(course_id=coursetime).first()
    courses = Resources.query.filter_by(course_resources=item).first()

    print(courses)
    #for c in courses:
    # print(c.course_title)

    return render_template("resource.html", course = courses)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/course/assignment/<coursetime>/',  methods = ('GET' , 'POST'))
@login_required
def assignment(coursetime):
    item = Course.query.filter_by(course_id=coursetime).first()
    courses = Assignments.query.filter_by(course_assignments=item).first()
    auther = User.query.filter(User.course_auth.any(course_id=coursetime)).filter(User.roles.any(id=2)).first()

    if current_user.user_id == auther.user_id:
        return redirect(url_for('assignment_teacher', coursetime=coursetime,username=current_user.user_id))

    #check before presents.
    #check_file = SharedFile.query.filter_by(course=item.course_id).filter_by(author=username).filter_by(assignment=courses.assignments_id).all()

   # for check in check_file:

      #  print(check.shared_file_title)
    if request.method == 'POST':
        file = request.files['inputfile']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #assign = Assignments.query.filter_by(course=coursetime).filter_by(auther=auther).first()
        newFile = SharedFile(shared_file_title=filename, shared_file_path=file.read(), author=current_user.user_id,
                             course=coursetime,assignment=courses.assignments_id)
        db.session.add(newFile)
        db.session.commit()
        return redirect(url_for('uploaded_file',filename=filename))

    print(courses)
    #for c in courses:
    # print(c.course_title)

    return render_template("assignment.html", course = courses, item=item)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/course/assignment_teacher/<coursetime>/<username>' , methods = ('GET' , 'POST'))
@login_required
@roles_required('Teacher')
def assignment_teacher(coursetime,username):
    item = Course.query.filter_by(course_id=coursetime).first()
    courses = Assignments.query.filter_by(course_assignments=item).all()

    if request.method == 'POST':
        a = Assignments(assignments_title=request.form['name'],
                 assignments_description=request.form['comment'],
                 assignments_course=item.course_id)
        db.session.add(a)
        db.session.commit()
        return redirect(url_for('assignment_teacher', coursetime=coursetime, username=current_user.user_id))

    print(courses)
    #for c in courses:
    # print(c.course_title)

    return render_template("assignment_teacher.html", courses = courses, item=item, username=username)

@app.route('/course/assignment_teacher_del/<coursetime>/<assignid>' , methods = ('GET' , 'POST'))
@login_required
@roles_required('Teacher')
def assignment_teacher_del(coursetime,assignid):

    item = Course.query.filter_by(course_id=coursetime).first()
    courses = Assignments.query.filter_by(course_assignments=item).all()

    assign = Assignments.query.filter_by(assignments_id=assignid).first()
    db.session.delete(assign)
    db.session.commit()

    return redirect(url_for('assignment_teacher', coursetime=coursetime, username=current_user.user_id))
@app.route('/course/assignment_teacher_edit/<coursetime>/<assignid>' , methods = ('GET' , 'POST'))
@login_required
@roles_required('Teacher')
def assignment_teacher_edit(coursetime,assignid):

    item = Course.query.filter_by(course_id=coursetime).first()
    courses = Assignments.query.filter_by(course_assignments=item).all()



    if request.method == 'POST':
        assign = Assignments.query.filter_by(assignments_id=assignid).first()
        assign.assignments_title=request.form['name']
        assign.assignments_description=request.form['comment']
        assign.assignments_course=item.course_id
        db.session.commit()


    return render_template("assignment_teacher.html", courses=courses, item=item, username=current_user.user_id, useredit=True)

@app.route('/profile/<userid>')
@login_required
def profile(userid):
    item = User.query.filter_by(user_id=userid).first()
    courses = Course.query.filter_by(author=item).first()

    print(courses)
    #for c in courses:
    # print(c.course_title)

    return render_template("profile.html", user=item ,course = courses)


@app.route('/post/<postid>')
def showPost(postid):
    #post = Post.query.get(postid)
    post = Post.query.filter(Post.post_id == postid).first()
#    querytage =User.query.filter_by(tagname=post.tags).all()

    for tag in post.tags:
        print(tag.tagname)
        tag_name = tag.tagname + " "
    #User.query.all()
    #tak
    #db.session.query(Post).all()
    #db.session.query(User).all()


    obj = {'title': "mypost",
           'date': "2017",
           'id': 2,
           'content': "<p>This is <strong>Blogging</strong>, a free, fully standards-compliant CSS template designed by Free CSS Templates</a>, released for free under the Creative Commons Attribution 2.5 license. The photos in this design are from . You're free to use this template for anything as long as you link back to . Enjoy :)</p><p>Sed lacus. Donec lectus. Nullam pretium nibh ut turpis. Nam bibendum. In nulla tortor, elementum ipsum. Proin imperdiet est. Phasellus dapibus semper urna. Pellentesque ornare, orci in felis. Donec ut ante. In id eros. Suspendisse lacus turpis, cursus egestas at sem.Sed lacus. Donec lectus. </p>"}

    return render_template('post.html', post=post, tag_name=tag_name )


@app.route('/contact', methods = ('GET' , 'POST'))
@login_required
def contact():
    if request.method == 'POST':

        auth = User.query.filter_by(user_name=current_user.user_id).first_or_404()
      #  print(post)

        cats= Category.query.filter_by(cat_name=request.form['cat']).first_or_404()
        print(cats.cat_id)

        p = Post(post_title=  request.form['name'],
                 post_content=request.form['comment'],
                 post_date="2017",
                 author= auth,
                 cat= cats)
        if Tags.query.filter_by(tagname=request.form['tag']).first():
            t = Tags.query.filter_by(tagname=request.form['tag']).first()
        else:
             t = Tags(tagname = request.form['tag'])

        db.session.add(t)
        db.session.add(p)
        t.tags.append(p)

        db.session.commit()

    for a in request.form.keys():
        print(a, request.form[a])
        return render_template("contact.html", title ='form sent!', usercomment = p)
    else:
        title = 'contact form'
        return render_template("contact.html", title = title)

def initdb():

    """ Create database """
    db.create_all()
   # posts = buildPosts()
    print('Successful')

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


if __name__ == '__main__':
    app.run(port=8080)
