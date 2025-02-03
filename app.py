import csv
from flask import Flask, render_template, request

app = Flask(__name__)

# Function to fetch mobile details from CSV
def get_phone_details(brand, model):
    with open("mobiles_cleaned.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        reader.fieldnames = [field.strip() for field in reader.fieldnames]  # Strip spaces from headers

        for row in reader:
            if row is None:
                continue

            row = {key.strip(): (value.strip() if value else "N/A") for key, value in row.items()}
            
            if row.get("Brand", "").lower() == brand.lower() and row.get("Model Name", "").lower() == model.lower():
                return row
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    brand = request.form['brand']
    model = request.form['model']
    phone = get_phone_details(brand, model)

    if phone:
        return render_template('search.html', phone=phone)
    else:
        return render_template('index.html', error="Mobile Not Found!", brand=brand, model=model)

@app.route('/compare', methods=['POST'])
def compare():
    brand1 = request.form['brand1']
    model1 = request.form['model1']
    brand2 = request.form['brand2']
    model2 = request.form['model2']

    phone1 = get_phone_details(brand1, model1)
    phone2 = get_phone_details(brand2, model2)

    if phone1 and phone2:
        return render_template('compare.html', phone1=phone1, phone2=phone2)
    else:
        return render_template('index.html', error="One or both mobiles not found!")

if __name__ == '__main__':
    app.run(debug=True)
