import flask
from flask import request, jsonify
from impresora import Principal
app = flask.Flask(__name__)
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
    documento = data_cliente.get("document").get("document")
    tipo_doc = data_cliente.get("document").get("documentType")
    for x in items:
        excento = x.get("exempt")
        print(excento)
        precio = str(x.get('price'))
        p_entero, p_decimal = precio.split('.')
        cantidad = str(float(x.get('amount')))
        print(cantidad)
        c_entera, c_decimal = cantidad.split('.')
        producto = x.get('name')
        codigos.append(f"{estados.get('e') if excento == True else estados.get('g')}{(('0') * (8 - len(p_entero))) + p_entero}{p_decimal + (('0') * (2 - len(p_decimal)))}\
{(('0') * (5 - len(c_entera))) + c_entera}{c_decimal + (('0') * (3 - len(c_decimal)))}{producto}")
    principal = Principal()
    principal.reconocer_puerto()
    principal.abrir_puerto()
    # factura_n = principal.printer.GetXReport()._numberOfLastInvoice
    principal.factura(codigos, nombre_cliente, direccion, "-".join([tipo_doc, documento]))
    return jsonify({'factura_n':True})
@app.route("/api/prueba", methods =['POST'])
def return_string():
    return jsonify("Prueba superada")
if __name__ == '__main__':
    app.run(port=3000)