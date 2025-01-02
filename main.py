import pymysql.err
from flask import Flask, render_template, request,url_for,redirect,session
from mylib import *
from werkzeug.utils import secure_filename
import time
import os
app = Flask(__name__)
app.secret_key="super secret key"
app.config['UPLOAD_FOLDER']='./static/photos'

@app.route('/')
def hello():
    return render_template('login.html')
#login
@app.route("/login",methods=["GET","POST"])
def login():
    if(request.method=="POST"):
        email = request.form["T1"]
        password = request.form["T2"]
        cur = make_connection()
        s1 = "select * from login_data where email='"+email+"' and password='"+password+"'"
        cur.execute(s1)
        n = cur.rowcount
        if( n>0 ):
            data = cur.fetchone()
            ut = data[3]
            session["email"]=email
            session["usertype"]=ut
            if(ut=="admin"):
                return redirect(url_for("admin_home"))
            elif(ut=="accountant"):
                return redirect(url_for("accountant_home"))
            else:
                return render_template("login.html",msg="usertype doesnot exist")
        else:
            return render_template("login.html",msg="Enter email and password is incorrect")
    else:
        return render_template("login.html")
#Logout
@app.route("/logout",methods=['GET','POST'])
def logout():
    if("usertype" in session):
        session.pop("usertype", None)
        session.pop("email",None)
        return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))

# auth_error
@app.route("/auth_error")
def auth_error():
    return render_template("auth_error.html")


# admin reg
@app.route('/admin_reg',methods=["GET","POST"])
def admin_reg():
    if(request.method=="POST"):
        name = request.form["T1"]
        address = request.form["T2"]
        contact = request.form["T3"]
        email = request.form["T4"]
        password = request.form["T5"]
        con_pass = request.form["T6"]
        usertype = "admin"
        msg = ""
        if(password!=con_pass):
            msg = "Data saved and login created"
        else:
            cur = make_connection()
            s1 = "insert into admin_data values ('"+name+"','"+address+"','"+contact+"','"+email+"')"
            s2 = "insert into login_data values ('"+email+"','"+password+"','"+con_pass+"','"+usertype+"')"
            cur.execute(s1)
            n = cur.rowcount

            cur.execute(s2)
            m = cur.rowcount
            if(m==1 and n==1):
                msg = "Data is saved and login created"
            elif(n==1):
                msg = "only data is saved"
            elif(m==1):
                msg = "only login created"
            else:
                msg = "No data saved and no login created"
            return render_template("admin_reg.html",vgt=msg)
    else:
        return render_template("admin_reg.html")

# show_admin
@app.route('/show_admin',methods=["GET","POST"])
def show_admin():
    cur = make_connection()
    s1 = "select * from admin_data"
    cur.execute(s1)
    n = cur.rowcount
    if(n>0):
        data = cur.fetchall()
        return render_template("show_admin.html",vgt=data)
    else:
        return render_template("show_admin.html",msg="No Data found")
# admin_photo
@app.route('/admin_photo')
def admin_photo():
    if 'usertype' in session:
        usertype=session['usertype']
        if usertype == 'admin':
            return render_template('photoupload_admin.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

# admin_photo1
@app.route('/admin_photo1',methods=['GET','POST'])
def admin_photo1():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            if request.method == 'POST' :
                file = request.files['F1']
                if(file):
                    path = os.path.basename(file.filename)
                    file_ext = os.path.splitext(path)[1][1:]
                    filename = str(int(time.time())) + '.' + file_ext
                    filename = secure_filename(filename)
                    cn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='student_fee',autocommit=True)
                    cur = cn.cursor()
                    sql = "insert into photodata values('"+email+"','" + filename + "')"

                    try:
                        cur.execute(sql)
                        n = cur.rowcount
                        if(n == 1):
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                            return render_template('photoupload_admin1.html', result="success")
                        else:
                            return render_template('photoupload_admin1.html', result="failure")
                    except:
                        return render_template('photoupload_admin1.html', result="duplicate")
            else:
                return render_template('photoupload_admin1.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

#Admin profile
@app.route("/admin_pro")
def admin_pro():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="admin"):
            cur=make_connection()
            e1=session["email"]
            photo=check_photo(e1)
            sql="select * from admin_data where email='"+e1+"'"
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                data=cur.fetchone()
                return render_template("admin_pro.html",kota=data,photo=photo)
            else:
                return render_template("admin_pro.html",msg="No Data Found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Admin Profile1
@app.route("/admin_pro1",methods=['GET','POST'])
def admin_pro1():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="admin"):
            if(request.method=="POST"):
                cur=make_connection()
                e1=session["email"]
                sql="select * from admin_data where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    data=cur.fetchone()
                    return  render_template("admin_pro1.html",kota=data,msg="Data Saved")
                else:
                    return render_template("admin_pro1.html",msg="Data Not Saved")
            else:
                return redirect(url_for("admin_pro"))
        else:
            return  redirect(url_for("auth_error"))
    else:
        return  redirect(url_for("auth_error"))

#Admin Profile2
@app.route("/admin_pro2",methods=['GET','POST'])
def admin_pro2():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="admin"):
            if(request.method=="POST"):
                nm=request.form["T1"]
                ad=request.form["T2"]
                co=request.form["T3"]
                email=session["email"]
                cur=make_connection()
                sql="update admin_data set name='"+nm+"',address='"+ad+"',contact='"+co+"'where email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    return render_template("admin_pro2.html",msg="Data Updated")
                else:
                    return  render_template("admin_pro2.html",msg="Data Is Not  Updated")
            else:
                return redirect(url_for("admin_pro"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Admin Change Photo
@app.route("/admin_change_photo")
def admin_change_photo():
    if("usertype" in session):
        ut=session["usertype"]
        email=session["email"]
        if(ut=="admin"):
            photo=check_photo(email)
            cur=make_connection()
            sql="delete from photodata where user_email='"+email+"'"
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                os.remove("./static/photos/" + photo)
                return render_template("admin_change_photo.html",data="success")
            else:
                return render_template("admin_change_photo.html",data="Failure")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Admin Change Password
@app.route("/admin_change_password",methods=['GET','POST'])
def admin_change_password():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="admin"):
            if(request.method=="POST"):
                e1=session["email"]
                oldpass=request.form["T1"]
                newpass=request.form["T2"]
                conpass=request.form["T3"]
                cur=make_connection()
                sql="update login_data set password='"+newpass+"'where email='"+e1+"' AND password='"+oldpass+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    return  render_template("admin_change_password.html",msg="Password Changed Successfully")
                else:
                    return render_template("admin_change_password.html",msg="Password Not Changed")
            else:
                return render_template("admin_change_password.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


# admin_home
@app.route("/admin_home",methods=["GET","POST"])
def admin_home():
    if("usertype" in session):
        ut = session["usertype"]
        email = session["email"]
        if(ut=="admin"):
            cur = make_connection()
            cur.execute("SELECT * FROM admin_with_photo")
            n = cur.rowcount
            if (n > 0):
                kota = cur.fetchall()
                return render_template("admin_home.html",email=email,kota=kota)
            else:
                return render_template("admin_home.html",msg="No data found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

# accountant_home
@app.route("/accountant_home",methods=["GET","POST"])
def accountant_home():
    if("usertype" in session):
        ut = session["usertype"]
        email = session["email"]
        if(ut=="accountant"):
            cur = make_connection()
            cur.execute("SELECT * FROM accountant_with_photo")
            n = cur.rowcount
            if (n > 0):
                kota = cur.fetchall()
                return render_template("accountant_home.html",email=email,kota=kota)
            else:
                return render_template("accountant_home.html",msg="No data found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))



# Accountant Change Photo
@app.route("/accountant_change_photo")
def accountant_change_photo():
    if("usertype" in session):
        ut=session["usertype"]
        email=session["email"]
        if(ut=="accountant"):
            photo=check_photo(email)
            cur=make_connection()
            sql="delete from photodata where user_email='"+email+"'"
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                os.remove("../static/photos/" + photo)
                return render_template("accountant_change_photo.html",data="success")
            else:
                return render_template("accountant_change_photo.html",data="Failure")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))
#Accountant Change Password
@app.route("/accountant_change_pass",methods=['GET','POST'])
def accountant_change_pass():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="accountant"):
            if(request.method=="POST"):
                e1=session["email"]
                oldpass=request.form["T1"]
                newpass=request.form["T2"]
                conpass=request.form["T3"]
                cur=make_connection()
                sql="update login_data set password='"+newpass+"'where email='"+e1+"' AND password='"+oldpass+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    return  render_template("accountant_change_pass.html",msg="Password Changed Successfully")
                else:
                    return render_template("accountant_change_pass.html",msg="Password Not Changed")
            else:
                return render_template("accountant_change_pass.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


# accountant_photo
@app.route('/accountant_photo')
def accountant_photo():
    if 'usertype' in session:
        usertype=session['usertype']
        email = session["email"]
        if usertype == 'accountant':
            return render_template('photoupload_accountant.html',email=email)
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


# accountant upload photo
@app.route("/accountant_photo1",methods=["GET","POST"])
def accountant_photo1():
    if("usertype" in session):
        ut = session["usertype"]
        email = session["email"]
        if(ut=="accountant"):
            name = get_accountant_name(email)
            if(request.method=="POST"):
                file = request.files["F1"]
                if(file):
                    path = os.path.basename(file.filename)
                    file_ext = os.path.splitext(path)[1][1:]
                    filename = str(int(time.time()))+'.'+file_ext
                    filename = secure_filename(filename)
                    cur = make_connection()
                    s1 = "insert into photodata values('"+email+"','"+filename+"')"
                    try:
                        cur.execute(s1)
                        n = cur.rowcount
                        if(n==1):
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                            return render_template("accountant_home.html",e1=email,photo=filename,name=name)
                        else:
                            return render_template("accountant_home.html",result="Failure",phot="no")
                    except:
                        return render_template("accountant_home.html",result="Duplicate",photo="no")
            else:
                return render_template("accountant_home.html",e1=email,name=name)
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


#accountant reg
@app.route("/accountant_reg",methods=['GET','POST'])
def accountant_reg():
    if(request.method=="POST"):
        emp=request.form["T1"]
        nm=request.form["T2"]
        des=request.form["T3"]
        co=request.form["T4"]
        email=request.form["T5"]
        pas=request.form["T6"]
        con_pass=request.form["T7"]
        usertype="accountant"
        msg = ""
        if (pas != con_pass):
            msg = "Data saved and login created"
        else:
            cur = make_connection()
            sql = "insert into accountant values('" + emp + "','" + nm + "','" + des + "','" + co + "','" + email + "')"
            sql1 = "insert into login_data values('" + email + "','" + pas + "','" + con_pass + "','" + usertype + "')"

            cur.execute(sql)
            n = cur.rowcount

            cur.execute(sql1)
            m = cur.rowcount
            if (m == 1 and n == 1):
                msg = "Data is saved and login created"
            elif (n == 1):
                msg = "only data is saved"
            elif (m == 1):
                msg = "only login created"
            else:
                msg = "No data saved and no login created"
            return render_template("accountant_reg.html", msg=msg)
    else:
        return render_template("accountant_reg.html")

#Show Accountant
@app.route("/show_accountant")
def show_accountant():
        cur=make_connection()
        sql="select * from accountant"
        cur.execute(sql)
        n=cur.rowcount
        if(n>0):
            data=cur.fetchall()
            return render_template("show_accountant.html",kota=data)
        else:
            return render_template("show_accountant.html",msg="No Data Found")



#Edit_Accountant
@app.route("/edit_accountant",methods=["GET","POST"])
def edit_accountant():
    if(request.method=="POST"):
        email=request.form["H1"]
        cur=make_connection()
        sql="Select * from accountant where email='"+email+"'"
        cur.execute(sql)
        n=cur.rowcount
        if(n==1):
            data=cur.fetchone()
            return render_template("edit_accountant.html",kota=data)
        else:
            return render_template("edit_accountant.html",msg="Data Not Found")
    else:
        return redirect(url_for("show_accountant.html"))


#Edit_Accountant1
@app.route("/edit_accountant1",methods=["GET","POST"])
def edit_accountant1():
    if(request.method=="POST"):
        emp = request.form["T1"]
        nm = request.form["T2"]
        des = request.form["T3"]
        con = request.form["T4"]
        email = request.form["T5"]
        cur = make_connection()
        sql = "update accountant set name='" + nm + "',designation='" + des + "',contact='" + con + "',email='" + email + "'where emp_no='" + emp + "' "
        cur.execute(sql)
        n = cur.rowcount
        if (n == 1):
            return render_template("edit_accountant1.html", msg="Data Saved")
        else:
            return render_template("edit_accountant1.html", msg="Data Not Saved")
    else:
        return redirect(url_for("show_accountant.html"))

#Delete_Accountant
@app.route("/delete_accountant",methods=["GET","POST"])
def delete_accountant():
    if (request.method == "POST"):
        email = request.form["H1"]
        cur = make_connection()
        sql = "Select * from accountant where email='" + email + "'"
        cur.execute(sql)
        n = cur.rowcount
        if (n == 1):
            data = cur.fetchone()
            return render_template("delete_accountant.html", kota=data)
        else:
            return render_template("delete_accountant.html", msg="Data Not Found")
    else:
        return redirect(url_for("show_accountant.html"))

#Delete_Accountant1
@app.route("/delete_accountant1",methods=["GET","POST"])
def delete_accountant1():
    if (request.method == "POST"):
        emp = request.form["T1"]
        nm = request.form["T2"]
        des = request.form["T3"]
        con = request.form["T4"]
        email = request.form["T5"]
        cur = make_connection()
        sql = "delete from accountant where emp_no='" + emp + "'"
        cur.execute(sql)
        n = cur.rowcount
        if (n == 1):
            return render_template("delete_accountant1.html", msg="Data Saved")
        else:
            return render_template("delete_accountant1.html", msg="Data Not Saved")
    else:
        return redirect(url_for("show_accountant.html"))


# student reg
@app.route("/student_reg",methods=["GET","POST"])
def student_reg():
    if(request.method=="POST"):
        Ragistration_no = request.form["T1"]
        Name = request.form["T2"]
        Address = request.form["T3"]
        contact = request.form["T4"]
        Email = request.form["T5"]
        usertype = "accountant"
        msg = ""
        cur = make_connection()
        s1 = "insert into st_data values('"+Ragistration_no+"','"+Name+"','"+Address+"','"+contact+"','"+Email+"')"
        cur.execute(s1)
        n = cur.rowcount
        if(n>0):
            msg = "Data is saved"
        else:
            msg = "Data id not saved"
        return render_template("student_reg.html",msg=msg)
    else:
        return render_template("student_reg.html")

#Show Student
@app.route("/show_student")
def show_student():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="accountant"):
            cur=make_connection()
            sql="select * from st_data"
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                data=cur.fetchall()
                return render_template("show_student.html",kota=data)
            else:
                return render_template("show_student.html",msg="No Data Found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return  redirect(url_for("auth_error"))
#Edit Student
@app.route("/edit_student",methods=['GET','POST'])
def edit_student():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="accountant"):
            if(request.method=="POST"):
                reg=request.form["H1"]
                cur=make_connection()
                sql="select * from st_data where reg_no='"+reg+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    data=cur.fetchone()
                    return render_template("edit_student.html",kota=data)
                else:
                    return render_template("edit_student.html",msg="No data found")
            else:
                return redirect(url_for("show_student"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))
#Edit Student1
@app.route("/edit_student1",methods=['GET','POST'])
def edit_student1():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="accountant"):
            if(request.method=="POST"):
                reg=request.form["T1"]
                nm=request.form["T2"]
                ad=request.form["T3"]
                co=request.form["T4"]
                email=request.form["T5"]

                cur=make_connection()
                sql="update st_data set name='"+nm+"',address='"+ad+"',contact='"+co+"',email='"+email+"' where reg_no='"+reg+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    return render_template("edit_student1.html",msg="Changes saved")
                else:
                    return render_template("edit_student1.html",msg="Error")
            else:
                return redirect(url_for("show_student"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

# student_course
@app.route("/student_course",methods=["GET","POST"])
def student_course():
    if("usertype" in session):
        ut = session["usertype"]
        if(ut=="accountant"):
            if(request.method=="POST"):
                course_id = request.form["T1"]
                reg_no = request.form["T2"]
                course = request.form["T3"]
                fee = request.form["T4"]
                discount = request.form["T5"]
                join_date = request.form["T6"]
                remarks = request.form["T7"]
                cur = make_connection()
                s1 = "insert into st_course values('"+course_id+"','"+reg_no+"','"+course+"','"+fee+"','"+discount+"','"+join_date+"','"+remarks+"')"

                try:
                    cur.execute(s1)
                    n = cur.rowcount

                    if(n>0):
                        msg = "Data is saved"
                    else:
                        msg = "Data not saved"
                except pymysql.err.InternalError:
                    msg = "Data is already Registered"
                return  render_template("student_course.html",msg=msg)
            else:
                return render_template("student_course.html")
        else:
            return redirect(url_for("auth_error.html"))
    else:
        return redirect(url_for("auth_error.html"))

# show course
@app.route("/show_course")
def show_course():
    if("usertype" in session):
        ut = session["usertype"]
        if(ut=="accountant"):
            cur = make_connection()
            s1 = "select * from st_course"
            cur.execute(s1)
            n = cur.rowcount
            if(n>0):
                data = cur.fetchall()
                return render_template("show_course.html",kota=data)
            else:
                return render_template("show_course.html",msg="No data found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

# edit_course
@app.route("/edit_course",methods=["GET","POST"])
def edit_course():
    if("usertype" in session):
        ut = session["usertype"]
        if(ut=="accountant"):
            if(request.method=="POST"):
                course_id = request.form["H1"]
                cur = make_connection()
                s1 = "select * from st_course where course_id='"+course_id+"'"
                cur.execute(s1)
                n = cur.rowcount
                if(n==1):
                    data = cur.fetchone()
                    return render_template("edit_course.html",kota=data)
                else:
                    return render_template("edit_course.html",msg="No data found")

            else:
                return redirect(url_for("show_course"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

# edit_course1
@app.route("/edit_course1",methods=["GET","POST"])
def edit_course1():
    if("usertype" in session):
        ut = session["usertype"]
        if(ut=="accountant"):
            if (request.method == "POST"):
                course_id = request.form["T1"]
                reg_no = request.form["T2"]
                course = request.form["T3"]
                fee = request.form["T4"]
                discount = request.form["T5"]
                join_date = request.form["T6"]
                remarks = request.form["T7"]
                cur = make_connection()
                s1 = "update st_course set reg_no='" + reg_no + "',course='" + course + "',fee='" + fee + "',discount='" + discount + "',join_date='" + join_date + "',remarks='" + remarks + "' where course_id='" + course_id + "'"
                cur.execute(s1)
                n = cur.rowcount
                if (n == 1):
                    return render_template("edit_course1.html", msg="Data is updated successfully")
                else:
                    return render_template("edit_course1.html", msg="Data is not uodated")
            else:
                return redirect(url_for("show_course"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


# Course Details
@app.route("/course_master",methods=["GET","POST"])
def course_master():
    if("usertype" in session):
        ut = session["usertype"]
        if(ut=="admin"):
            if(request.method=="POST"):
                course= request.form["T1"]
                fee = request.form["T2"]
                duration = request.form["T3"]
                remark = request.form["T4"]
                cur = make_connection()
                s1 = "insert into course_master values('"+course+"','"+fee+"','"+duration+"','"+remark+"')"

                try:
                    cur.execute(s1)
                    n = cur.rowcount

                    if(n>0):
                        msg = "Data is saved"
                    else:
                        msg = "Data not saved"
                except pymysql.err.InternalError:
                    msg = "Data is already Registered"
                return  render_template("course_master.html",msg=msg)
            else:
                return render_template("course_master.html")
        else:
            return redirect(url_for("auth_error.html"))
    else:
        return redirect(url_for("auth_error.html"))

# show course master
@app.route("/show_course_master")
def show_course_master():
    if("usertype" in session):
        ut = session["usertype"]
        if(ut=="admin"):
            cur = make_connection()
            s1 = "select * from course_master"
            cur.execute(s1)
            n = cur.rowcount
            if(n>0):
                data = cur.fetchall()
                return render_template("show_course_master.html",kota=data)
            else:
                return render_template("show_course_master.html",msg="No data found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))
# edit_course_master
@app.route("/edit_course_master",methods=["GET","POST"])
def edit_course_master():
    if("usertype" in session):
        ut = session["usertype"]
        if(ut=="admin"):
            if(request.method=="POST"):
                course = request.form["H1"]
                cur = make_connection()
                s1 = "select * from course_master where course='"+course+"'"
                cur.execute(s1)
                n = cur.rowcount
                if(n==1):
                    data = cur.fetchone()
                    return render_template("edit_course_master.html",kota=data)
                else:
                    return render_template("edit_course_master.html",msg="No data found")

            else:
                return redirect(url_for("show_course_master"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

# edit_course1
@app.route("/edit_course_master1",methods=["GET","POST"])
def edit_course_master1():
    if("usertype" in session):
        ut = session["usertype"]
        if(ut=="admin"):
            if (request.method == "POST"):
                course = request.form["T1"]
                fee = request.form["T2"]
                duration = request.form["T3"]
                remark = request.form["T4"]

                cur = make_connection()
                s1 = "update course_master set fee='" + fee + "',duration='" + duration + "',remarks='" + remark + "' where course='" + course+ "'"
                cur.execute(s1)
                n = cur.rowcount
                if (n == 1):
                    return render_template("edit_course_master1.html", msg="Data is updated successfully")
                else:
                    return render_template("edit_course_master1.html", msg="Data is not uodated")
            else:
                return redirect(url_for("show_course_master"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Student fee
@app.route("/student_fee",methods=['GET','POST'])
def student_fee():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="accountant"):
            if(request.method=="POST"):
                reg = request.form["T1"]
                couid=request.form["T2"]
                amt=request.form["T3"]
                dep=request.form["T4"]
                rm=request.form["T5"]
                cur=make_connection()
                sql="insert into st_fee values(0,'"+reg+"','"+couid+"',"+amt+",'"+dep+"','"+rm+"')"
                print(sql)

                try:
                    cur.execute(sql)
                    n=cur.rowcount

                    if(n==1):
                        msg="Data Saved"
                    else:
                        msg="Data Not Saved "
                except pymysql.err.IntegrityError:
                    msg="Data is already registered"
                return render_template("student_fee.html",msg=msg)
            else:
                return render_template("student_fee.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Show Fee
@app.route("/show_fee")
def show_fee():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="accountant"):
            cur=make_connection()
            sql="select * from st_fee"
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                data=cur.fetchall()
                return render_template("show_fee.html",kota=data)
            else:
                return render_template("show_fee.html",msg="No Data Found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return  redirect(url_for("auth_error"))


#Edit fee
@app.route("/edit_fee",methods=['GET','POST'])
def edit_fee():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="accountant"):
            if(request.method=="POST"):
                t_no=request.form["H1"]
                cur=make_connection()
                sql="select * from st_fee where tno='"+t_no+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    data=cur.fetchone()
                    return render_template("edit_fee.html",vgt=data)
                else:
                    return render_template("edit_fee.html",msg="No data found")
            else:
                return redirect(url_for("show_student"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Edit fee1
@app.route("/edit_fee1",methods=["GET","POST"])
def edit_fee1():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="accountant"):
            if(request.method=="POST"):
                t_no = request.form["T1"]
                reg=request.form["T2"]
                couid=request.form["T3"]
                amt=request.form["T4"]
                dep=request.form["T5"]
                re=request.form["T6"]

                cur = make_connection()
                sql="update st_fee set reg_no="+reg+",course_id="+couid+",amount="+amt+",deposit_date='"+dep+"',remarks='"+re+"' where tno= '"+t_no+"' "
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    return render_template("edit_fee1.html",msg="Changes saved")
                else:
                    return render_template("edit_fee1.html",msg="Error")
            else:
                return redirect(url_for("student_home"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


#student home
@app.route("/student_home",methods=["GET","POST"])
def student_home():
    if("usertype" in session):
        email = session["usertype"]
        ut=session["usertype"]
        if(ut=="accountant"):
            if(request.method=="POST"):
                reg_no = request.form["H1"]
                photo = check_photo(email)
                cur = make_connection()
                sql = "select * from st_data where reg_no='" + reg_no + "'"
                print(sql)
                cur.execute(sql)
                n = cur.rowcount
                if (n==1):
                    data = cur.fetchall()
                    s2 = "select * from st_course where reg_no=" + reg_no
                    print(s2)
                    cur.execute(s2)
                    m = cur.rowcount
                    if (m>0):
                        data1 = cur.fetchall()
                        #create list for student courses
                        stcourses=[]
                        total_fee=0
                        total_paid=0
                        total_discount=0

                        for d in data1:
                            paid=get_course_paid(d[1],d[0])
                            total_fee=total_fee+d[3]
                            total_discount=total_discount+d[4]
                            total_paid=total_paid+paid

                            due=d[3]-d[4]-paid
                            aa=[d[0],d[1],d[2],d[3],d[4],d[5],d[6],paid,due]
                            stcourses.append(aa)
                        final_total=total_fee-total_discount-total_paid
                        fee_list=[total_fee,total_discount,total_paid,final_total]

                        s3 = "select * from st_fee where reg_no=" + reg_no
                        cur.execute(s3)
                        a = cur.rowcount
                        if(a>0):
                            data2 = cur.fetchall()
                            return render_template("student_home.html",photo=photo, kota=data, vgt=stcourses,punit=data2,fees=fee_list)
                        else:
                            return render_template("student_home.html", photo=photo, kota=data, vgt=data1)
                    else:
                        return render_template("student_home.html",photo=photo, kota=data, msg="No data found")
                else:
                    return render_template("student_home.html", msg="No Data Found")
            else:
                return render_template("student_home.html",msg="NO Data Found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return  redirect(url_for("auth_error"))



if __name__=="__main__":
    app.run(debug=True)
