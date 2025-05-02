from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "truckinglist.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


@app.route('/')
def index():
    return '''
        <html>
        <head><title>Trucking Company API</title></head>
        <body>
            <h1>Welcome to the Trucking Company REST API</h1>
            <p>This API manages a list of trucking companies stored in a nested JSON structure.</p>
            
            <h2>Available Endpoints</h2>
            <ul>
                <li><strong>GET /companies</strong> – Returns a list of all companies</li>
                <li><strong>GET /companies/&lt;name&gt;</strong> – Returns details for a single company</li>
                <li><strong>POST /companies</strong> – Adds a new company (send JSON in body)</li>
                <li><strong>PUT /companies/&lt;name&gt;</strong> – Updates a company (send JSON in body)</li>
                <li><strong>DELETE /companies/&lt;name&gt;</strong> – Deletes the specified company</li>
            </ul>

            <h2>Sample curl Commands</h2>
            <pre>
curl http://&lt;your-ec2-ip&gt;:8000/companies

curl http://&lt;your-ec2-ip&gt;:8000/companies/UPS

curl -X POST http://&lt;your-ec2-ip&gt;:8000/companies \\
     -H "Content-Type: application/json" \\
     -d '{"Company": "New Truck Co", "Services": "New services", "Hubs": {"Hub": []}, "Revenue": "$100", "HomePage": "http://example.com", "Logo": "logo.png"}'

curl -X PUT http://&lt;your-ec2-ip&gt;:8000/companies/UPS \\
     -H "Content-Type: application/json" \\
     -d '{"Revenue": "$99,999"}'

curl -X DELETE http://&lt;your-ec2-ip&gt;:8000/companies/FedEx
            </pre>

            <p>Data is read from and written to <code>truckinglist.json</code> on the server.</p>
        </body>
        </html>
    '''

@app.route('/companies', methods=['GET'])
def get_all_companies():
    try:
        data = load_data()
        companies = data["Mainline"]["Table"]["Row"]
        return jsonify(companies)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/companies/<string:name>', methods=['GET'])
def get_company(name):
    try:
        data = load_data()
        companies = data["Mainline"]["Table"]["Row"]
        for company in companies:
            if company["Company"].lower() == name.lower():
                return jsonify(company)
        return jsonify({'error': 'Company not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/companies', methods=['POST'])
def add_company():
    required_fields = ["Company", "HomePage", "Revenue"]
    new_company = request.get_json()

    if not new_company:
        return jsonify({'error': 'Request body must be JSON'}), 400

    missing = [field for field in required_fields if field not in new_company]
    if missing:
        return jsonify({'error': f'Missing required fields: {", ".join(missing)}'}), 400

    data = load_data()
    companies = data["Mainline"]["Table"]["Row"]

    for company in companies:
        if company["Company"].lower() == new_company["Company"].lower():
            return jsonify({'error': 'Company already exists'}), 400

    companies.append(new_company)
    save_data(data)
    return jsonify(new_company), 201

@app.route('/companies/<string:name>', methods=['PUT'])
def update_company(name):
    update_data = request.get_json()
    data = load_data()
    companies = data["Mainline"]["Table"]["Row"]

    for company in companies:
        if company["Company"].lower() == name.lower():
            company.update(update_data)
            save_data(data)
            return jsonify(company)

    return jsonify({'error': 'Company not found'}), 404

@app.route('/companies/<string:name>', methods=['DELETE'])
def delete_company(name):
    data = load_data()
    companies = data["Mainline"]["Table"]["Row"]
    new_list = [c for c in companies if c["Company"].lower() != name.lower()]

    if len(new_list) == len(companies):
        return jsonify({'error': 'Company not found'}), 404

    data["Mainline"]["Table"]["Row"] = new_list
    save_data(data)
    return jsonify({'message': f'Company "{name}" deleted.'})


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True)
