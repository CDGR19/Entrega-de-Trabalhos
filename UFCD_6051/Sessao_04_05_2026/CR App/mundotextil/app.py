"""
Banco de Horas - MundoTextil (Demo)
Flask + SQLite — sem login, dados importados automaticamente de dados.json
Porta: 5001
"""

import os, io, json, csv
from datetime import datetime
from flask import Flask, render_template, request, jsonify, abort, Response, send_from_directory
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'demo.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "mundotextil-demo-2024"

db = SQLAlchemy(app)
DIAS_PT = {0:"Segunda",1:"Terca",2:"Quarta",3:"Quinta",4:"Sexta",5:"Sabado",6:"Domingo"}

class Registo(db.Model):
    __tablename__ = "registos"
    id          = db.Column(db.Integer, primary_key=True)
    data        = db.Column(db.String(10), nullable=False)
    dia_semana  = db.Column(db.String(10))
    tipo        = db.Column(db.String(60), nullable=False)
    horas       = db.Column(db.Float, nullable=False)
    descricao   = db.Column(db.String(500), default="")
    def to_dict(self):
        return {"id":self.id,"data":self.data,"dia_semana":self.dia_semana,
                "tipo":self.tipo,"horas":self.horas,"descricao":self.descricao}

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(os.path.join(BASE_DIR, "templates"), filename)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/registos", methods=["GET"])
def listar_registos():
    ano = request.args.get("ano")
    tipo = request.args.get("tipo")
    texto = request.args.get("q","").strip()
    q = Registo.query
    if ano and ano != "todos": q = q.filter(Registo.data.like(f"{ano}-%"))
    if tipo and tipo != "todos": q = q.filter(Registo.tipo == tipo)
    if texto: q = q.filter(db.or_(Registo.descricao.ilike(f"%{texto}%"),Registo.tipo.ilike(f"%{texto}%"),Registo.data.like(f"%{texto}%")))
    registos = q.order_by(Registo.data.asc()).all()
    saldo = db.session.query(db.func.sum(Registo.horas)).scalar() or 0
    return jsonify({"registos":[r.to_dict() for r in registos],"saldo_total":saldo,"count":len(registos)})

@app.route("/api/registos", methods=["POST"])
def criar_registo():
    data = request.get_json()
    if not data: abort(400)
    try: dt = datetime.strptime(data["data"], "%Y-%m-%d")
    except: return jsonify({"erro":"Data invalida"}), 400
    try: horas = float(data["horas"])
    except: return jsonify({"erro":"Horas invalidas"}), 400
    r = Registo(data=data["data"],dia_semana=DIAS_PT[dt.weekday()],tipo=data.get("tipo","Horas Extra"),horas=horas,descricao=data.get("descricao",""))
    db.session.add(r); db.session.commit()
    return jsonify(r.to_dict()), 201

@app.route("/api/registos/<int:rid>", methods=["PUT"])
def atualizar_registo(rid):
    r = Registo.query.get_or_404(rid)
    data = request.get_json()
    if not data: abort(400)
    if "data" in data:
        try:
            dt = datetime.strptime(data["data"],"%Y-%m-%d")
            r.data=data["data"]; r.dia_semana=DIAS_PT[dt.weekday()]
        except: return jsonify({"erro":"Data invalida"}), 400
    if "horas" in data: r.horas=float(data["horas"])
    if "tipo" in data: r.tipo=data["tipo"]
    if "descricao" in data: r.descricao=data["descricao"]
    db.session.commit()
    return jsonify(r.to_dict())

@app.route("/api/registos/<int:rid>", methods=["DELETE"])
def eliminar_registo(rid):
    r = Registo.query.get_or_404(rid)
    db.session.delete(r); db.session.commit()
    return jsonify({"ok":True})

@app.route("/api/saldos_por_ano")
def saldos_por_ano():
    rows = db.session.query(db.func.substr(Registo.data,1,4).label("ano"),db.func.sum(Registo.horas).label("total")).group_by("ano").order_by("ano").all()
    return jsonify([{"ano":r.ano,"total":r.total} for r in rows])

@app.route("/api/exportar/json")
def exportar_json():
    registos = Registo.query.order_by(Registo.data.asc()).all()
    dados = json.dumps([r.to_dict() for r in registos], ensure_ascii=False, indent=2)
    hoje = datetime.now().strftime("%Y-%m-%d")
    return Response(dados, mimetype="application/json", headers={"Content-Disposition":f"attachment; filename=banco_horas_{hoje}.json"})

@app.route("/api/exportar/excel")
def exportar_excel():
    registos = Registo.query.order_by(Registo.data.asc()).all()
    output = io.StringIO(); writer = csv.writer(output, delimiter=";")
    writer.writerow(["Data","Dia da Semana","Tipo","Horas","Descricao"])
    saldo = 0
    for r in registos:
        saldo += r.horas
        writer.writerow([r.data,r.dia_semana,r.tipo,f"{'+' if r.horas>0 else ''}{r.horas}",r.descricao or ""])
    writer.writerow([]); writer.writerow(["","","SALDO",f"{'+' if saldo>=0 else ''}{saldo}",""])
    hoje = datetime.now().strftime("%Y-%m-%d")
    return Response("\ufeff"+output.getvalue(), mimetype="text/csv; charset=utf-8", headers={"Content-Disposition":f"attachment; filename=banco_horas_{hoje}.csv"})

def importar_dados():
    dados_path = os.path.join(BASE_DIR, "dados.json")
    if not os.path.exists(dados_path): return
    if Registo.query.count() > 0: return  # Already imported
    with open(dados_path, encoding="utf-8") as f:
        registos = json.load(f)
    for item in registos:
        try:
            r = Registo(data=item["data"],dia_semana=item.get("dia_semana",""),tipo=item.get("tipo","Horas Extra"),horas=float(item["horas"]),descricao=item.get("descricao",""))
            db.session.add(r)
        except: continue
    db.session.commit()
    print(f"[MT] Importados {Registo.query.count()} registos de dados.json")

with app.app_context():
    db.create_all()
    importar_dados()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
