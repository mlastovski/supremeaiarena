from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exists
from emails import commit_to_text_file

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletter.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class MailingGroup(db.Model):
    __tablename__ = "mailing_group"

    mail = db.Column(db.String(100), nullable=False, primary_key=True)
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return "<MailingGroup mail='%s'>" % self.mail


@app.route('/', methods=["POST", "GET"])
@app.route('/home', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        # emails_list = MailingGroup.query.all()
        #
        # # print all existing emails and id's in console
        # print('All existing emails and ids:')
        # for single_email in emails_list:
        #     print("Email: ", single_email.mail, ", Id: ", single_email.id)
        #     # print(single_email)
        #

        # Getting email from click
        email = request.form['mail']
        # print(email)
        if email == '':
            print('empty field')
            # resp = jsonify('<span style=\'color:red;\'>Username is required field.</span>')
            # resp.status_code = 200
            # return resp
            return redirect('/fail')

        # Checking if email already exists
        email_exists = db.session.query(exists().where(MailingGroup.mail == email)).scalar()

        # If yes - return an error
        if email_exists:

            print('We already have this email, returning error page to the user')
            print(email, ' already exists')
            # resp = jsonify('<span style=\'color:red;\'>Username unavailable</span>')
            # resp.status_code = 200
            # return resp
            return redirect('/fail')

        # if no - commit do database
        elif not email_exists:
            print('New email, commiting to the database')
            print(email, ' does not exist')

            mailing_group = MailingGroup(mail=email)
            db.session.add(mailing_group)
            db.session.commit()
            commit_to_text_file()
            return redirect('/success')

        # Debug for mistakes, redirects to main page
        else:
            print('sho')
            return redirect('/')


    else:
        return render_template('index.html')


@app.route('/presskit')
def presskit():
    return render_template('presskit.html')


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/fail')
def fail():
    return render_template('fail.html')


if __name__ == '__main__':
    app.run(debug=True)
