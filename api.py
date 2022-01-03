from operator import attrgetter
import flask
from flask import request, jsonify
from impresora import Principal
from flask_cors import CORS, cross_origin
import time

app = flask.Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/api/factura', methods=['POST'])
@cross_origin()
def api_all():
    """Función para facturar.
        :return: Número de factura
        :rtype: json
        """
    estados = {'e': ' ', 'g': '!', 'r': '"', 'a': '#'}
    codigos = []
    data = request.get_json(force= True)
    items = data.get("invoice").get("items")
    data_cliente = data.get("invoice").get("client")
    nombre_cliente = f"{data_cliente.get('name')} {data_cliente.get('surname')}"
    direccion = data_cliente.get("address")
    documento_cliente = data_cliente.get("document").get("document")
    tipo_doc = data_cliente.get("document").get("documentType")
    telefono_cliente = data_cliente.get("phone")
    pagos = data.get("invoice").get("payments")
    data_cajero = data.get("invoice").get("cashier")
    for x in items:
        excento = x.get("exempt")
        precio = str(x.get('price'))
        p_entero, p_decimal = precio.split('.')
        cantidad = str(float(x.get('amount')))
        c_entera, c_decimal = cantidad.split('.')
        producto = x.get('name')
        codigos.append(f"{estados.get('e') if excento == True else estados.get('g')}{(('0') * (8 - len(p_entero))) + p_entero}{p_decimal + (('0') * (2 - len(p_decimal)))}\
{(('0') * (5 - len(c_entera))) + c_entera}{c_decimal + (('0') * (3 - len(c_decimal)))}{producto}")
    try:
        principal = Principal()
        principal.reconocer_puerto()
        principal.abrir_puerto()
        factura_anterior = principal.printer.n_factura()
        principal.factura(lista_productos = codigos, cliente = nombre_cliente, \
            direccion = direccion, documento = "-".join([tipo_doc, documento_cliente]), telefono = telefono_cliente,\
                pago = pagos, cajero = data_cajero)
        principal.cerrar_puerto()
        principal.abrir_puerto()
        factura_n = principal.printer.n_factura()
        principal.cerrar_puerto()
        if factura_anterior != factura_n:
            return jsonify({'invoice_number': factura_n})
        else:
            return jsonify({'Error': 'Error de máquina fiscal'}), 418
    except AttributeError as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Impresora no conectada"}), 503
@app.route("/api/imprimirx", methods =['POST', 'GET'])
def imprimir_x():
    try:
        principal = Principal()
        principal.reconocer_puerto()
        principal.abrir_puerto()
        principal.imprimir_ReporteX()
        principal.cerrar_puerto()
        return jsonify({'report_x': True})
    except AttributeError as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Impresora no conectada"}), 503
@app.route("/api/obtenerx", methods =['POST', 'GET'])
def obtener_x():
    try:
        principal = Principal()
        principal.reconocer_puerto()
        principal.abrir_puerto()
        principal.obtener_reporteX()
        principal.cerrar_puerto()
        return jsonify({'report_x': True})
    except AttributeError as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Impresora no conectada"}), 503
@app.route("/api/imprimirz", methods =['POST', 'GET'])
def imprimir_z():
    try:
        principal = Principal()
        principal.reconocer_puerto()
        principal.abrir_puerto()
        principal.imprimir_ReporteZ()
        principal.cerrar_puerto()
        return jsonify({"report_z":True})
    except AttributeError as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Impresora no conectada"}), 503
# @app.route("/api/devolucion", methods =['POST'])
# def devolucion():
#     data = request.get_json(force= True)
#     principal = Principal()
@app.route("/api/reimprimir", methods = ['POST'])
def reimprimir():
    """Función para reimprimir una factura."""
    data = request.get_json(force=True)
    n_factura = data.get("invoice_number")
    try:
        principal = Principal()
        principal.reconocer_puerto()
        principal.abrir_puerto()
        principal.ReimprimirFacturas(n_factura)
        principal.cerrar_puerto()
        return jsonify({"Executed": True})
    except AttributeError as e:
        print(f"Error: {e}")
        return jsonify({"Error": 'No se'})

@app.route('/api/devolucion', methods=['POST'])
@cross_origin()
def devolucion():
    """Función para devolucion.
        :return: Número de devolucion
        :rtype: json
        """
    estados = {'e': '0', 'g': '1', 'r': '2', 'a': '3'}
    codigos = []
    data = request.get_json(force= True)
    items = data.get("invoice").get("items")
    data_cliente = data.get("invoice").get("client")
    nombre_cliente = f"{data_cliente.get('name')} {data_cliente.get('surname')}"
    direccion = data_cliente.get("address")
    documento_cliente = data_cliente.get("document").get("document")
    tipo_doc = data_cliente.get("document").get("documentType")
    telefono_cliente = data_cliente.get("phone")
    pagos = data.get("invoice").get("payments")
    data_cajero = data.get("invoice").get("cashier")
    n_factura = data.get('invoice').get('invoiceNumber')
    serial = data.get('invoice').get('cashier').get('serial')
    for x in items:
        excento = x.get("exempt")
        precio = str(x.get('price'))
        p_entero, p_decimal = precio.split('.')
        cantidad = str(float(x.get('amount')))
        c_entera, c_decimal = cantidad.split('.')
        producto = x.get('name')
        codigos.append(f"d{estados.get('e') if excento == True else estados.get('g')}{(('0') * (8 - len(p_entero))) + p_entero}{p_decimal + (('0') * (2 - len(p_decimal)))}\
{(('0') * (5 - len(c_entera))) + c_entera}{c_decimal + (('0') * (3 - len(c_decimal)))}{producto}")
    try:
        principal = Principal()
        principal.reconocer_puerto()
        principal.abrir_puerto()
        nota_anterior = principal.printer.n_nota_credito()
        principal.notaCredito(lista_productos = codigos, cliente = nombre_cliente, \
            direccion = direccion, documento = "-".join([tipo_doc, documento_cliente]), telefono = telefono_cliente,\
                pago = pagos, cajero = data_cajero, n_factura = n_factura, serial = serial)
        principal.cerrar_puerto()
        principal.abrir_puerto()
        nota_n = principal.printer.n_nota_credito()
        principal.cerrar_puerto()
        print(nota_n)
        if nota_anterior != nota_n:
            return jsonify({'invoice_number': nota_n})
        else:
            return jsonify({'Error': 'Error de máquina fiscal'}), 418
    except AttributeError as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Impresora no conectada"}), 503

if __name__ == '__main__':
    app.run(host = "127.0.0.1",port=5000)