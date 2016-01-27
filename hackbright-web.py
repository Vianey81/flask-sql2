from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/")
def get_all_info():
    """Show main page.
    Make a homepage that has two lists – one for all students, and one for all projects. Both should be bulleted lists and both should be made up live links to the full student and project pages.

    """

    students = hackbright.get_students()
    projects = hackbright.get_projects()
    return render_template("home.html",
                           students=students,
                           projects=projects,
                           )


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

@app.route("/project")
def project_info():
    """Show information about a project."""

    title = request.args.get('title', 'Markov')
    title, description, grade = hackbright.get_project_by_title(title)
    name_grade = []
    students = hackbright.get_grades_by_title(title)
    for student in students:
        name, last_name, github = hackbright.get_student_by_github(student[0])
        grade = student[1]
        name_grade.append((name, last_name, grade, github))

    return render_template("project.html",
                            title=title,
                            description=description,
                            max_grade=grade,
                            students=name_grade,
                            )

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
