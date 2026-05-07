"""
Registo de Horas - BP (Demo)
Flask + SQLite — sem login, dados importados automaticamente de dados.json
Taxa configuravel. Porta: 5002
"""

import os, io, json, csv
from datetime import datetime
from flask import Flask, render_template, request, jsonify, abort, Response, send_from_directory
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'demo.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "bp-demo-2024"

db = SQLAlchemy(app)
DIAS_PT = {"Monday":"seg","Tuesday":"ter","Wednesday":"qua","Thursday":"qui","Friday":"sex","Saturday":"sab","Sunday":"dom"}

class Configuracao(db.Model):
    __tablename__ = "configuracao"
    id    = db.Column(db.Integer, primary_key=True)
    chave = db.Column(db.String(50), unique=True, nullable=False)
    valor = db.Column(db.String(200), nullable=False)

class Registo(db.Model):
    __tablename__ = "registos"
    id            = db.Column(db.Integer, primary_key=True)
    data          = db.Column(db.String(10), nullable=False)
    dia_semana    = db.Column(db.String(10))
    entrada_manha = db.Column(db.String(5))
    saida_manha   = db.Column(db.String(5))
    entrada_tarde = db.Column(db.String(5))
    saida_tarde   = db.Column(db.String(5))
    horas_total   = db.Column(db.Float, default=0.0)
    ganhos        = db.Column(db.Float, default=0.0)
    notas         = db.Column(db.String(300), default="")

    def calcular(self, taxa):
        total_min = 0; fmt = "%H:%M"
        try:
            if self.entrada_manha and self.saida_manha:
                e=datetime.strptime(self.entrada_manha,fmt); s=datetime.strptime(self.saida_manha,fmt)
                if s>e: total_min+=(s-e).seconds//60
        except: pass
        try:
            if self.entrada_tarde and self.saida_tarde:
                e=datetime.strptime(self.entrada_tarde,fmt); s=datetime.strptime(self.saida_tarde,fmt)
                if s>e: total_min+=(s-e).seconds//60
        except: pass
        self.horas_total=round(total_min/60,4); self.ganhos=round(self.horas_total*taxa,4)

    def to_dict(self):
        return {"id":self.id,"data":self.data,"dia_semana":self.dia_semana,
                "entrada_manha":self.entrada_manha or "","saida_manha":self.saida_manha or "",
                "entrada_tarde":self.entrada_tarde or "","saida_tarde":self.saida_tarde or "",
                "horas_total":self.horas_total,"ganhos":self.ganhos,"notas":self.notas or ""}

def get_taxa():
    cfg=Configuracao.query.filter_by(chave="taxa_hora").first()
    return float(cfg.valor) if cfg else 5.0

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(os.path.join(BASE_DIR,"templates"),filename)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/configuracao/taxa", methods=["GET"])
def obter_taxa():
    return jsonify({"taxa":get_taxa()})

@app.route("/api/configuracao/taxa", methods=["PUT"])
def atualizar_taxa():
    data=request.get_json()
    try: nova_taxa=float(data["taxa"]); assert nova_taxa>0
    except: return jsonify({"erro":"Taxa invalida"}),400
    cfg=Configuracao.query.filter_by(chave="taxa_hora").first()
    if cfg: cfg.valor=str(nova_taxa)
    else: cfg=Configuracao(chave="taxa_hora",valor=str(nova_taxa)); db.session.add(cfg)
    for r in Registo.query.all(): r.calcular(nova_taxa)
    db.session.commit()
    return jsonify({"taxa":nova_taxa,"ok":True})

@app.route("/api/registos", methods=["GET"])
def listar():
    ano=request.args.get("ano"); mes=request.args.get("mes"); q=Registo.query
    if ano and ano!="todos": q=q.filter(Registo.data.like(f"{ano}-%"))
    if mes and mes!="todos":
        if ano and ano!="todos": q=q.filter(Registo.data.like(f"{ano}-{mes.zfill(2)}-%"))
        else: q=q.filter(db.func.substr(Registo.data,6,2)==mes.zfill(2))
    registos=q.order_by(Registo.data.asc()).all()
    th=sum(r.horas_total for r in registos); tg=sum(r.ganhos for r in registos)
    anos_rows=db.session.query(db.func.substr(Registo.data,1,4).label("ano"),db.func.sum(Registo.horas_total).label("horas"),db.func.sum(Registo.ganhos).label("ganhos")).group_by("ano").order_by("ano").all()
    return jsonify({"registos":[r.to_dict() for r in registos],"total_horas":round(th,2),"total_ganhos":round(tg,2),"count":len(registos),"taxa":get_taxa(),"saldos_ano":[{"ano":r.ano,"horas":round(r.horas,2),"ganhos":round(r.ganhos,2)} for r in anos_rows]})

@app.route("/api/registos", methods=["POST"])
def criar():
    data=request.get_json()
    if not data: abort(400)
    try: dt=datetime.strptime(data["data"],"%Y-%m-%d")
    except: return jsonify({"erro":"Data invalida"}),400
    r=Registo(data=data["data"],dia_semana=DIAS_PT.get(dt.strftime("%A"),""),entrada_manha=data.get("entrada_manha","") or None,saida_manha=data.get("saida_manha","") or None,entrada_tarde=data.get("entrada_tarde","") or None,saida_tarde=data.get("saida_tarde","") or None,notas=data.get("notas",""))
    r.calcular(get_taxa()); db.session.add(r); db.session.commit()
    return jsonify(r.to_dict()), 201

@app.route("/api/registos/<int:rid>", methods=["PUT"])
def atualizar(rid):
    r=Registo.query.get_or_404(rid); data=request.get_json()
    if not data: abort(400)
    if "data" in data:
        try: dt=datetime.strptime(data["data"],"%Y-%m-%d"); r.data=data["data"]; r.dia_semana=DIAS_PT.get(dt.strftime("%A"),"")
        except: return jsonify({"erro":"Data invalida"}),400
    for c in ("entrada_manha","saida_manha","entrada_tarde","saida_tarde"):
        if c in data: setattr(r,c,data[c] or None)
    if "notas" in data: r.notas=data["notas"]
    r.calcular(get_taxa()); db.session.commit()
    return jsonify(r.to_dict())

@app.route("/api/registos/<int:rid>", methods=["DELETE"])
def eliminar(rid):
    r=Registo.query.get_or_404(rid); db.session.delete(r); db.session.commit()
    return jsonify({"ok":True})

@app.route("/api/exportar/json")
def exportar_json():
    registos=Registo.query.order_by(Registo.data.asc()).all()
    dados=json.dumps([r.to_dict() for r in registos],ensure_ascii=False,indent=2)
    hoje=datetime.now().strftime("%Y-%m-%d")
    return Response(dados,mimetype="application/json",headers={"Content-Disposition":f"attachment; filename=bp_horas_{hoje}.json"})

@app.route("/api/exportar/excel")
def exportar_excel():
    registos=Registo.query.order_by(Registo.data.asc()).all()
    output=io.StringIO(); writer=csv.writer(output,delimiter=";")
    writer.writerow(["Data","Dia","Entrada Manha","Saida Manha","Entrada Tarde","Saida Tarde","Horas","Ganhos EUR","Notas"])
    for r in registos:
        writer.writerow([r.data,r.dia_semana,r.entrada_manha or "",r.saida_manha or "",r.entrada_tarde or "",r.saida_tarde or "",f"{r.horas_total:.2f}",f"{r.ganhos:.2f}",r.notas or ""])
    writer.writerow([]); th=sum(r.horas_total for r in registos); tg=sum(r.ganhos for r in registos)
    writer.writerow(["","","","","","TOTAL",f"{th:.2f}",f"{tg:.2f}",""])
    hoje=datetime.now().strftime("%Y-%m-%d")
    return Response("\ufeff"+output.getvalue(),mimetype="text/csv; charset=utf-8",headers={"Content-Disposition":f"attachment; filename=bp_horas_{hoje}.csv"})

def importar_dados():
    dados_path=os.path.join(BASE_DIR,"dados.json")
    if not os.path.exists(dados_path): return
    if Registo.query.count()>0: return
    taxa=get_taxa()
    with open(dados_path,encoding="utf-8") as f: registos=json.load(f)
    for item in registos:
        try:
            dt=datetime.strptime(item["data"],"%Y-%m-%d")
            r=Registo(data=item["data"],dia_semana=DIAS_PT.get(dt.strftime("%A"),item.get("dia_semana","")),entrada_manha=item.get("entrada_manha") or None,saida_manha=item.get("saida_manha") or None,entrada_tarde=item.get("entrada_tarde") or None,saida_tarde=item.get("saida_tarde") or None,notas=item.get("notas",""))
            r.calcular(taxa); db.session.add(r)
        except: continue
    db.session.commit()
    print(f"[BP] Importados {Registo.query.count()} registos de dados.json")

with app.app_context():
    db.create_all(); importar_dados()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)
