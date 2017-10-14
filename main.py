from flask import Flask, Response, make_response, request
from routine import get_csv_document
import io
import csv

app = Flask(__name__)


@app.route("/")
def hello():
    return app.send_static_file("index.html")


@app.route("/extract", methods=['POST'])

def extract():
    content = [line.decode("utf-8","strict") for line in io.BytesIO(request.data).readlines()]
    values = get_csv_document(content)
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerows(values)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output 

if __name__ == "__main__":
    app.debug=True
    app.run()
