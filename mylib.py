import pymysql

def check_photo(email):
    cn = pymysql.connect(host='localhost',port=3306,user='root',passwd="",db="student_fee",autocommit=True)
    cur = cn.cursor()
    cur.execute("select * from photodata where user_email='"+email+"'")
    n = cur.rowcount
    photo = 'no'
    if(n>0):
        row = cur.fetchone()
        photo = row[1]
    return photo
def make_connection():
    cn = pymysql.connect(host="localhost",port=3306,db="student_fee",user="root",autocommit=True,passwd="")
    cur = cn.cursor()
    return cur

def get_admin_name(email):
    cur = make_connection()
    cur.execute("select * from admin_data where email='"+email+"'")
    n = cur.rowcount
    name = "no"
    if(n>0):
        row = cur.fetchone()
        name = row[0]
    return name

def get_accountant_name(email):
    cur = make_connection()
    cur.execute("select * from accountant where email='"+email+"'")
    n = cur.rowcount
    name = "no"
    if(n>0):
        row = cur.fetchone()
        name = row[1]
    return name
def get_course_paid(stid,cid):
    cur = make_connection()
    cur.execute("select * from st_fee where reg_no="+str(stid)+" and course_id="+str(cid))
    n = cur.rowcount
    t=0
    if(n>0):
        data=cur.fetchall()
        for d in data:
            t=t+ d[3]
    return t

