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
    for x in data:
        precio = str(x.get('precio'))
        p_entero, p_decimal = precio.split('.')
        cantidad = str(x.get('cantidad'))
        c_entera, c_decimal = cantidad.split('.')
        producto = x.get('producto')
        codigos.append(f"{estados.get(x.get('estado'))}{(('0') * (8 - len(p_entero))) + p_entero}{p_decimal + (('0') * (2 - len(p_decimal)))}\
{(('0') * (5 - len(c_entera))) + c_entera}{c_decimal + (('0') * (3 - len(c_decimal)))}{producto}")
    principal = Principal()
    principal.reconocer_puerto()
    factura_n = principal.printer.GetXReport()._numberOfLastInvoice
    principal.abrir_puerto()
    principal.factura(codigos)
    return jsonify({'factura_n':factura_n})
@app.route("/api/prueba", methods =['POST'])
def return_string():
    return jsonify("Prueba superada")
if __name__ == '__main__':
    app.run(port=3000)