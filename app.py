from jira import JIRA
from flask import Flask, make_response, render_template, jsonify, flash, redirect, url_for
import forms
import settings

jira = JIRA(settings.globaloptions, basic_auth=settings.authcredentials)
app = Flask('JIRA')
app.config.from_object('config')


@app.errorhandler(404)
def not_found(error):  # handles any 404 requests to the instance
    return make_response(jsonify({'Error': '404 Not Found'}), 404)

@app.route("/", methods=['GET', 'POST'])
def homepage():
    form = forms.LoginForm()
    if form.validate_on_submit():
        flash('Login requested for access key="%s", remember_me=%s' %
              (form.accesskey.data, str(form.remember_me.data)))
        return redirect('/dashboard')
    try:
        return render_template("home.html", settings=settings.home, form=form)
    except Exception, e:
        return str(e)

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    current_issues = jira.search_issues('reporter = currentUser()')
    CreateIssueForm = forms.CreateIssue()
    if CreateIssueForm.validate_on_submit():
        new_issue = jira.create_issue(project=settings.project, summary=CreateIssueForm.title.data, description=CreateIssueForm.description.data, issuetype={'name': 'Task'})
        flash('New issue created: %s, Title=%s, Description=%s' %
              (new_issue.key, CreateIssueForm.title.data, str(CreateIssueForm.description.data)))
        return redirect('/dashboard')
    try:
        return render_template("dashboard.html", settings=settings.dashboard, issues=current_issues, form=CreateIssueForm)
    except Exception, e:
        return str(e)

if __name__ == '__main__':
    #app.debug = True
    app.run(host='127.0.0.1', port=5000)


