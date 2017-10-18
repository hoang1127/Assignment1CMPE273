import os, uuid
import subprocess
from flask import Flask, request, redirect, url_for, Response, json
from werkzeug.utils import secure_filename

# Save in local server
UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = set(['py'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# For POST
@app.route('/api/v1/scripts', methods=['GET', 'POST'])
def upload_file():
    if not os.path.exists('/api/v1/scripts'):
        os.makedirs('/api/v1/scripts')
    if request.method == 'POST':
        if 'data' not in request.files:
            print('There is No file')
            return redirect(request.url)
        file = request.files['data']
        # Check valid file
        if file.filename == '':
            print('There is no selected file')
            return redirect(request.url)
        if file:
            filename = uuid.uuid4().hex
            file.save('/api/v1/scripts/' + filename + '.py')
        
    # Return file with path
    return Response(json.dumps({"scribe-id": filename }), status=201, mimetype='application/json')

# For GET
@app.route('/api/v1/scripts/<id>')
def execute_func(id):
  return subprocess.check_output("python3 " + "/api/v1/scripts/"  + id + ".py", shell=True)
  
if __name__ == '__main__':
     app.run(port='8000')