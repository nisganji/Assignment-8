from flask import Flask, render_template, request, redirect, url_for, flash
import os
import DAL
import contact_DAL

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a random secret key
DAL.init_db()
contact_DAL.init_contact_db()

@app.route('/')
def home():
    return render_template('index.html', active_page='home')

@app.route('/about')
def about():
    return render_template('about.html', active_page='about')

@app.route('/resume')
def resume():
    return render_template('resume.html', active_page='resume')

@app.route('/projects')
def projects():
    projects_list = DAL.list_projects()
    return render_template('projects.html', active_page='projects', projects=projects_list)


@app.route('/projects/new', methods=['GET', 'POST'])
def new_project():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        image_file_name = request.form.get('image_file_name', '').strip()

        if not title or not description or not image_file_name:
            flash('All fields are required: Title, Description, and Image File Name.', 'error')
            return redirect(url_for('new_project'))

        try:
            DAL.insert_project(title, description, image_file_name)
        except Exception as e:
            flash(f'Failed to add project: {e}', 'error')
            return redirect(url_for('new_project'))

        flash('Project added successfully.', 'success')
        return redirect(url_for('projects'))

    return render_template('project_form.html', active_page='projects')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        
        # Basic validation (frontend handles detailed validation)
        if not all([first_name, last_name, email, password, confirm_password]):
            flash('All fields are required.', 'error')
            return redirect(url_for('contact'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('contact'))
        
        if len(password) < 8:
            flash('Password must be at least 8 characters.', 'error')
            return redirect(url_for('contact'))
        
        # Save contact form data to the contacts database
        try:
            contact_DAL.insert_contact(first_name, last_name, email, password)
            flash('Thank you for your message! Your information has been saved.', 'success')
        except Exception as e:
            flash(f'Failed to save your information: {e}', 'error')
            return redirect(url_for('contact'))
        
        return redirect(url_for('thank_you'))
    
    return render_template('contact.html', active_page='contact')

@app.route('/thank-you')
def thank_you():
    return render_template('thankyou.html', active_page='contact')

if __name__ == '__main__':
    # Allow configuring host/port/debug via environment (useful for Docker)
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', '5000'))
    debug = os.getenv('FLASK_DEBUG', '0') == '1'
    app.run(host=host, port=port, debug=debug)
