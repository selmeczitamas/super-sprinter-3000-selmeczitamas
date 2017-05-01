from flask import Flask, render_template, request, url_for, redirect
import csv
app = Flask(__name__)


@app.route('/story', methods=['POST'])
def add_new_story():
    title = "Add new Story"
    button = "Create"
    story = ["", "", "", "", "100", "1.0", ""]
    return render_template('form.html', title=title, button=button, story=story)


@app.route("/", methods=["GET", "POST"])
def index():
    title = 'Super Sprinter 3000'
    header = 'User Story Manager'
    stories = read_csv_file()
    return render_template("list.html", header="header", title="title", stories=stories)


@app.route("/list", methods=["POST"])
def print_list():
    title = 'Super Sprinter 3000'
    stories = read_csv_file()
    new_data = []
    id_number = 0
    if request.form["button"] == "Create":
        id_number = str(int(stories[-1][0]) + 1)
        new_data.append(id_number)
        new_data.append(request.form["story_title"])
        new_data.append(request.form["story"])
        new_data.append(request.form["criteria"])
        new_data.append(request.form["value"])
        new_data.append(request.form["estimation"])
        new_data.append(request.form["status"])
        stories.append(new_data)
        write_database(stories, file_name='database.csv')
        return render_template("list.html", title="title", stories=stories)
    elif request.form["button"] == "Update":
        id_number = request.form["story_id"]
        updated_data = []
        updated_data.append(request.form["story_id"])
        updated_data.append(request.form["story_title"])
        updated_data.append(request.form["story"])
        updated_data.append(request.form["criteria"])
        updated_data.append(request.form["value"])
        updated_data.append(request.form["estimation"])
        updated_data.append(request.form["status"])
        new_data = []
        for item in stories:
            if item[0] != id_number:
                new_data.append(item)
            else:
                new_data.append(updated_data)
        write_database(new_data, file_name='database.csv')
        return redirect("/")


@app.route("/edit/<id>", methods=["GET", "POST"])
def edit_story(id):
    title = "Edit Story"
    button = "Update"
    stories = read_csv_file()
    for item in stories:
        if item[0] == id:
            story = item
    write_database(stories, file_name='database.csv')
    return render_template('form.html', title=title, button=button, story=story, id=id)


@app.route("/delete/<id>", methods=["GET", "POST"])
def delete(id):
    stories = read_csv_file()
    new_stories = []
    for item in stories:
        if item[0] != id:
            new_stories.append(item)
    write_database(new_stories, file_name='database.csv')
    return redirect("/")


def read_csv_file(filename="database.csv"):
    content = []
    with open(filename, "r") as myfile:
        reader = csv.reader(myfile)
        for line in reader:
            content.append(line)
    return content


def add_to_database(new_info, filename="database.csv",):
    with open(filename, 'a') as database:
        writer = csv.writer(database)
        writer.writerow(new_info)
    stories = read_csv_file(filename="database.csv")
    return stories


def write_database(new_data, file_name='database.csv'):
    with open(file_name, 'w', newline='') as csvfile:
        datawriter = csv.writer(csvfile, delimiter=',')
        datawriter.writerows(new_data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=None)
