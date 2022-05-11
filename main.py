import os
import json
from flask import Flask
from flask import jsonify
from odbc import *
from decimal import *
from serialization import *

app = Flask(__name__, instance_relative_config=True)


@app.route('/')
def index():
    html = '<a href="mssql">MSSQLSERVER</a><br><a href="mysql">MYSQL</a>'
    return html

@app.route('/mysql', methods=['GET', 'POST'])
def consult_Mysql():
    mssql = Odbc("MYSQL")
    conn = mssql.connect( auto_commit=False) #auto_comit defaul is false
    cursor = conn.cursor()
    result = cursor.execute("select * from inf_pedido limit 0,5")
    res = toJsonDump(result)
    return jsonify(res)

@app.route('/mssql', methods=['GET', 'POST'])
def consult_MSSQL():
    mssql = Odbc("MSSQLSERVER")
    conn = mssql.connect(char_encode="IBM437", auto_commit=False) #auto_comit defaul is false
    cursor = conn.cursor()
    result = cursor.execute("SELECT top(1) * from QSYSTEMS.dbo.mastinvpos where inv_inventario = ?", 'S19')
    res = toJsonDump(result)
    return jsonify(res)



