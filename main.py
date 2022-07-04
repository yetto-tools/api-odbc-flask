from flask import send_from_directory
from flask import Flask, request, render_template, send_file
from flask import jsonify
from odbc import *
from serialization import *
from flask_cors import CORS
from datetime import datetime
from SQLQueries import *
from io import BytesIO
from commons import *
import base64
from os import urandom, path
import qrcode


app = Flask(__name__, instance_relative_config=True, static_url_path='/static')
app.secret_key = urandom(24)
app.config["JSON_SORT_KEYS"] = False
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

cors = CORS(app, resources={
            r"/api/*": {"origins": "*"}}, methods=['GET', 'POST'])


def to_qcode(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color="white")
    bufferImage = BytesIO()
    img.save(bufferImage, format="PNG")
    img_tobase64 = base64.b64encode(bufferImage.getbuffer().tobytes())

    return img_tobase64.decode("utf-8")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    html = '<a href="/api/v1/mssql">MSSQLSERVER</a><br><a href="/api/v1/mysql">MYSQL</a>'
    return html


@app.route('/report')
def report():
    mssql = Odbc("MSSQLSERVER")
    conn = mssql.connect()
    cursor = conn.cursor()
    result = cursor.execute(
        "select COD_Reporte, RPT_Nombre, RPT_SQLQuery, RPT_FechaUpdate from SysReports..MFT_Reporte ORDER BY RPT_FechaUpdate DESC;")

    text = toStringAll(result)

    # with  open("REPORTES_SQL.json", 'w') as f:
    #     f.write(result[0])
    #     f.close()
    return jsonify(text)


@app.route('/api/v1/mysql', methods=['GET', 'POST'])
def consult_Mysql():
    mysql = Odbc("MYSQL")
    conn = mysql.connect(auto_commit=False)  # auto_comit defaul is false
    cursor = conn.cursor()
    result = cursor.execute(
        "select * FROM inf_factura where empresa=01 and serie =?  and factura = ?;", 'IFF2', 1571)
    res = toStringAll(result)  # All values return of consult convert to string
    return jsonify(res)


@app.route('/api/v1/mysql_jsondump', methods=['GET', 'POST'])
def consult_jsondump():
    mysql = Odbc("MYSQL")
    conn = mysql.connect(auto_commit=False)  # auto_comit defaul is false
    cursor = conn.cursor()
    result = cursor.execute(
        "select * FROM inf_factura where empresa=01 and serie =?  and factura = ?;", 'IFF2', 1571)
    res = toJsonDump(result)  # All values return of consult convert to string
    return jsonify(res)


# http://localhost:5000/api/v1/especiales2?initial=2020-08-21&final=2020-08-21
@app.route('/api/v1/especiales2', methods=['GET', 'POST'])
def especiales2():

    date_init = request.args.get('init')
    dete_final = request.args.get('final')

    if date_init:
        mysql = Odbc("MYSQL")
        conn = mysql.connect(auto_commit=False)  # auto_comit defaul is false
        cursor = conn.cursor()
        result = cursor.execute(ESPECIALES_2_DEFAULT_CROM, date_init, dete_final)
        res = toStringAll(
            result)  # All values return of consult convert to string
        return jsonify(res)
    else:
        return jsonify("bad args")


@app.route('/api/v1/mssql', methods=['GET', 'POST'])
def consult_MSSQL():
    mssql = Odbc("MSSQLSERVER")
    # auto_comit defaul is false
    conn = mssql.connect(char_encode="IBM437", auto_commit=False)
    cursor = conn.cursor()
    result = cursor.execute(
        "SELECT Top(1) * FROM dbo.DIST_INVDEVOLCLIH WHERE DINDCH_VENDEDOR = ?", 405)
    res = toJsonDump(result)
    return jsonify(res)


@app.route('/api/v1/float', methods=['GET', 'POST'])
def consult_MSSQL_float():
    mssql = Odbc("MSSQLSERVER")
    # auto_comit defaul is false
    conn = mssql.connect(char_encode="IBM437", auto_commit=False)
    cursor = conn.cursor()
    result = cursor.execute("SELECT * FROM sysreports..MFT_Reporte")
    res = toJsonDump(result)
    return jsonify(res)


@app.route('/api/v1/form', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        for item in request.form:
            print(request.form.get(item))
    return render_template('form.html')


@app.route('/api/v1/facturas_pagos', methods=['GET', 'POST'])
def facturas_pagos():

    no_fac = request.args.get('nofac')

    if no_fac:
        mysql = Odbc("MYSQL")
        conn = mysql.connect(auto_commit=False)  # auto_comit defaul is false
        cursor = conn.cursor()
        result = cursor.execute(PAGOS_FACTURAS, no_fac, str(datetime.now().year)+"-01-01")

        res = toStringAll(result)
        print(res)
        qcode = to_qcode(res)

        return jsonify({'invoice': res, 'qcode': qcode})
    else:
        return jsonify("bad args")


@app.route('/recibo_pagos', methods=['GET', 'POST'])
def imprimir_recibo_pago():
    if request.method == 'GET':
        # with open("test.html", "w") as f:
        #     f.write (render_template('recibo.html'))
        return render_template('recibo.html')


@app.route('/especiales2', methods=['GET', 'POST'])
def test_especiales():
    date_init = request.args.get('init')
    dete_final = request.args.get('final')
    credito = 0
    if date_init:
        mysql = Odbc("MYSQL")
        conn = mysql.connect(auto_commit=False)  # auto_comit defaul is false
        cursor = conn.cursor()
        cursor.execute("SET @@lc_time_names = 'es_GT'; ")
        result = cursor.execute(FILTRO_ESPECIALES2, date_init, dete_final, credito, date_init, dete_final)
        consult = result
        buffer = send_to_xlsx_fix(consult)
        mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

        return send_file(buffer, mimetype=mimetype)
    else:
        return jsonify("bad args")


@app.route('/api/v1/export', methods=['GET', 'POST'])
def api_export_to_xlsx():
    date_init = request.args.get('init')
    dete_final = request.args.get('final')
    credito = 0
    file = None
    if date_init:
        mysql = Odbc("MYSQL")
        conn = mysql.connect(auto_commit=False)  # auto_comit defaul is false
        cursor = conn.cursor()
        cursor.execute("SET @@lc_time_names = 'es_GT'; ")
        result = cursor.execute(ESPECIALES_2_TO_EXCEL, date_init, dete_final, credito)
        file = ResposeFileExcel(result.fetchall())
    return file


@app.route('/export', methods=['GET', 'POST'])
def export_to_xlsx():
    return render_template('export_to_xlsx.html')

@app.route('/excel', methods=['GET', 'POST'])
def test_send_to_execl():
    date_init = request.args.get('init')
    dete_final = request.args.get('final')
    credito = 0
    file = None
    if date_init:
        mysql = Odbc("MYSQL")
        conn = mysql.connect(auto_commit=False)  # auto_comit defaul is false
        cursor = conn.cursor()
        cursor.execute("SET @@lc_time_names = 'es_GT';")
        if dete_final >= date_init:
            result = cursor.execute(ESPECIALES_2_DEFAULT_CROM, date_init, dete_final)
        elif date_init >= dete_final:
            result = cursor.execute(ESPECIALES_2_DEFAULT_CROM, dete_final, date_init)
    send_to_xlsx(result)
    return "ok"

def ResposeFileExcel(data):
    buffer = send_to_simple_xlsx_fix(data, headers=['fecha', 'dia', 'cliente', 'nombre', 'monto', 'forma']) # data_to_xlsx_and_table(data) # fix_data_to_xlsx_and_table(data)
    mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    return send_file(buffer, mimetype=mimetype)


@app.route('/<int:codigo>', methods=['DELETE'])
def testing(codigo):
    return jsonify(codigo)

# es cierto que sentarse para hablas
# las cosas, no siempres resuelve todo
# pero si no lo hacemos nunca nos 
# entenderemos