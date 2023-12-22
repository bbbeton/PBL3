from flask import Flask, jsonify, request

app = Flask(__name__)

data = 25

@app.route('/temperature/s1', methods=['GET'])
def get_temperature():
	return jsonify({'temperature': data})

@app.route('/temperature/s1', methods=['PUT'])
def set_temperature():
	global data
	new_data = request.json.get('temperature', None)
	if new_data is not None:
		data = new_data
		return jsonify({'message': f'Temperature set to {data}'})
	else:
		return jsonify({'error': 'No valid number provided in the request body'})
	
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
