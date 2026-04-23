from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from email_validator import validate_email, EmailNotValidError

app = Flask(__name__)
app.secret_key = 'secret123'

# DATABASE CONFIG

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/contact_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODEL
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    address = db.Column(db.String(200))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(15), unique=True)

# HOME
@app.route('/')
def home():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)

# ADD CONTACT
@app.route('/add', methods=['POST'])
def add_contact():
    first = request.form['first_name']
    last = request.form['last_name']
    address = request.form['address']
    email = request.form['email']
    phone = request.form['phone']

    # Name validation
    if not first.isalpha():
        flash("First name must contain only letters", "danger")
        return redirect('/')

    if last and not last.isalpha():
        flash("Last name must contain only letters", "danger")
        return redirect('/')

    # Email validation
    try:
        valid = validate_email(email)
        email = valid.email

        if not email.endswith("@gmail.com"):
            flash("Email must be a Gmail address", "danger")
            return redirect('/')

    except EmailNotValidError:
        flash("Invalid Email format", "danger")
        return redirect('/')

    # Phone validation
    if not phone.isdigit() or len(phone) != 10:
        flash("Phone must be exactly 10 digits and numeric", "danger")
        return redirect('/')

    # Duplicate check
    if Contact.query.filter_by(email=email).first():
        flash("Email already exists", "danger")
        return redirect('/')

    if Contact.query.filter_by(phone=phone).first():
        flash("Phone already exists", "danger")
        return redirect('/')

    new_contact = Contact(
        first_name=first,
        last_name=last,
        address=address,
        email=email,
        phone=phone
    )

    db.session.add(new_contact)
    db.session.commit()

    flash("Contact added successfully!", "success")
    return redirect('/')

# DELETE
@app.route('/delete/<int:id>')
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    return redirect('/')

# EDIT PAGE
@app.route('/edit/<int:id>')
def edit_contact(id):
    contact = Contact.query.get_or_404(id)
    return render_template('edit.html', contact=contact)

# UPDATE CONTACT
@app.route('/update/<int:id>', methods=['POST'])
def update_contact(id):
    contact = Contact.query.get_or_404(id)

    first = request.form['first_name']
    last = request.form['last_name']
    address = request.form['address']
    email = request.form['email']
    phone = request.form['phone']

    # Name validation
    if not first.isalpha():
        flash("First name must contain only letters", "danger")
        return redirect(f'/edit/{id}')

    if last and not last.isalpha():
        flash("Last name must contain only letters", "danger")
        return redirect(f'/edit/{id}')

    # Email validation
    try:
        valid = validate_email(email)
        email = valid.email

        if not email.endswith("@gmail.com"):
            flash("Email must be a Gmail address", "danger")
            return redirect(f'/edit/{id}')

    except EmailNotValidError:
        flash("Invalid Email format", "danger")
        return redirect(f'/edit/{id}')

    # Phone validation
    if not phone.isdigit() or len(phone) != 10:
        flash("Phone must be exactly 10 digits and numeric", "danger")
        return redirect(f'/edit/{id}')

    # Duplicate check (exclude current record)
    existing_email = Contact.query.filter(
        Contact.email == email,
        Contact.id != id
    ).first()

    if existing_email:
        flash("Email already exists", "danger")
        return redirect(f'/edit/{id}')

    existing_phone = Contact.query.filter(
        Contact.phone == phone,
        Contact.id != id
    ).first()

    if existing_phone:
        flash("Phone already exists", "danger")
        return redirect(f'/edit/{id}')

    # Update values
    contact.first_name = first
    contact.last_name = last
    contact.address = address
    contact.email = email
    contact.phone = phone

    db.session.commit()

    flash("Contact updated successfully!", "success")
    return redirect('/')

# MAIN RUN
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
