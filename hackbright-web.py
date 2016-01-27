from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'sdevelops')
    first, last, github = hackbright.get_student_by_github(github)
    title_grades = hackbright.get_grades_by_github(github)
    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           projects=title_grades)
    return html


@app.route("/student_search")
def get_student_form():
    """Show form for searching for a student."""
    
    return render_template("student_search.html")


@app.route("/student-add", methods=['GET'])
def student_add_render():
    """Add a student."""
    return render_template("student-add.html")


@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student."""

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    github = request.form.get('github')

    hackbright.make_new_student(fname, lname, github)

    return "Student added! <br><a href='student?github=%s'>Student Info</a>" % github


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
