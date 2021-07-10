#!/usr/bin/python3
import os

from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
##postgress
engine = create_engine("mysql+pymysql://root:free@localhost:3306/uob")


db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")
@app.route("/insert", methods=['GET'])
def insert():
    return render_template("insert.html")

@app.route("/view", methods=['POST', 'GET'])
def view():
    if request.method == "POST":

        fname = request.form.get("fname")
        lname = request.form.get("lname")
        session = request.form.get("session")
        sub_fee = request.form.get("sub_fee")
        due_fee = request.form.get("due_fee")
        tot_fee = request.form.get("tot_fee")
        db.execute("INSERT into fee_record(firstname, lastname, session, submittedfee, duefee, totalfee) VALUES (:firstname, :lastname, :session, :submittedfee, :duefee, :totalfee)",
                {"firstname": fname, "lastname": lname, "session": session, "submittedfee": sub_fee, "duefee": due_fee, "totalfee": tot_fee})
        db.commit()

        # Get all records again
        students = db.execute("SELECT * FROM fee_record").fetchall()
        return render_template("view.html", students=students)
    else:
        students = db.execute("SELECT * FROM fee_record").fetchall()
        return render_template("view.html", students=students)


# @app.route("/update/<int:id>/", methods=['POST','GET'])
# def update(id):
#     if request.method=="POST":
#         fname = request.form.get("fname")
#         lname = request.form.get("lname")
#         session = request.form.get("session")
#         subfee = request.form.get("subfee")
#         duefee = request.form.get("duefee")
#         totfee = request.form.get("totfee")
#         db.execute("Update fee SET firstname=:fname, lastname=:lname, Session=:session, submitted_fee=: subfee, due_fee=: duefee, total_fee=:totfee where id = :id",)
#                 {"firstname": fname, "lastname": lname, "Session":session, "submitted_fee": subfee, "due_fee": duefee, "total_fee":totfee})
#         db.commit()
#         return redirect(url_for('intro'))
#     else:
#         stud = db.execute("SELECT * FROM fee WHERE id = :id", {"id": id}).fetchone()
#         return render_template("update.html", stud=stud, id=id)
#
#
# @app.route("/update_now/<int:id>/", methods=['POST', 'GET'])
# def update_now(id):
#     stud = db.execute("SELECT * FROM fee WHERE id = :id", {"id": id}).fetchone()
#     if stud is None:
#         return "No record found by ID = " + str(id) +". Kindly go back to <a href='/intro'> Intro </a>"
#     else:
#         stud = db.execute("delete FROM students WHERE id = " + str(id))
#         db.commit()
#         return redirect(url_for('intro'))
# # @app.route("/delete/<int:id>/")
# # def delete(id):
# #     stud = db.execute("SELECT * FROM students WHERE id = :id", {"id": id}).fetchone()
# #     if stud is None:
# #         return "No record found by ID = " + str(id) +". Kindly go back to <a href='/intro'> Intro </a>"
# #     else:
# #         stud = db.execute("delete FROM students WHERE id = " + str(id))
# #         db.commit()
# #         return redirect(url_for('intro'))
#

if __name__ == "__main__":
    app.run(debug=True)
