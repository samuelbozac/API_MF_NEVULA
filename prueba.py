from operator import attrgetter
import flask
from flask import request, jsonify
from impresora import Principal
from flask_cors import CORS
app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/api/v1/factura', methods=['POST'])
def api_all():
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
        principal.factura(lista_productos = codigos, cliente = nombre_cliente, \
            direccion = direccion, documento = "-".join([tipo_doc, documento_cliente]), telefono = telefono_cliente,\
                pago = pagos)
        principal.cerrar_puerto()
        principal.abrir_puerto()
        factura_n = principal.printer.N_Factura()
        principal.cerrar_puerto()
        return jsonify({'invoice_number': factura_n})
    except AttributeError:
        return jsonify({"Error": "Impresora no conectada"})
@app.route("/api/prueba", methods =['POST'])
def return_string():
    return jsonify("Prueba superada")
if __name__ == '__main__':
    app.run(host = "127.0.0.1",port=5000)