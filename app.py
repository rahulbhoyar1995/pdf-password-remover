from flask import Flask, render_template, request, flash, redirect, url_for
import pikepdf
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'supersecretkey'  # Change this to a more secure key in production

def remove_password(pdf_loc, pdf_pass, save_location, save_file):
    try:
        pdf = pikepdf.open(pdf_loc, password=pdf_pass)
        pdf.save(os.path.join(save_location, save_file))
        return True
    except pikepdf.PasswordError:
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pdf_pass = request.form['pdf_password']
        pdf_file = request.files['pdf_file']

        if pdf_file and pdf_pass:
            try:
                pdf_filename = pdf_file.filename
                pdf_location = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
                pdf_file.save(pdf_location)

                save_location = app.config['UPLOAD_FOLDER']
                save_file = f"unlocked_{pdf_filename}"

                if remove_password(pdf_location, pdf_pass, save_location, save_file):
                    flash('Password successfully removed from the PDF.', 'success')
                    result_location = os.path.join(save_location, save_file)
                    flash('Result PDF location: ' + result_location, 'success')
                else:
                    flash('Incorrect password. Please try again.', 'error')

                return redirect(url_for('index'))
            except Exception as e:
                flash(f'An error occurred: {str(e)}', 'error')
                return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
