from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import json, os, uuid

app = Flask(__name__)
DATA_FILE = "patients.json"

def load_patients():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_patients(patients):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(patients, f, ensure_ascii=False, indent=2)

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/dashboard")
def index():
    patients = load_patients()
    total = len(patients)
    hospitalises = sum(1 for p in patients if p.get("statut") == "Hospitalisé")
    consultations = sum(1 for p in patients if p.get("statut") == "En consultation")
    sortis = sum(1 for p in patients if p.get("statut") == "Sorti")
    urgences = sum(1 for p in patients if p.get("service") == "Urgences")
    return render_template("index.html", total=total, hospitalises=hospitalises,
                           consultations=consultations, sortis=sortis, urgences=urgences)

@app.route("/patients")
def patients():
    all_patients = load_patients()
    query = request.args.get("q", "").lower()
    service = request.args.get("service", "")
    statut = request.args.get("statut", "")
    if query:
        all_patients = [p for p in all_patients if
                        query in p.get("nom", "").lower() or
                        query in p.get("prenom", "").lower() or
                        query in p.get("id_patient", "").lower()]
    if service:
        all_patients = [p for p in all_patients if p.get("service") == service]
    if statut:
        all_patients = [p for p in all_patients if p.get("statut") == statut]
    return render_template("patients.html", patients=all_patients, query=query,
                           service=service, statut=statut)

@app.route("/nouveau_patient", methods=["GET", "POST"])
def nouveau_patient():
    if request.method == "POST":
        patients = load_patients()
        pid = "PAT-" + str(uuid.uuid4())[:8].upper()
        patient = {
            "id_patient": pid,
            "nom": request.form.get("nom", "").upper(),
            "prenom": request.form.get("prenom", "").capitalize(),
            "date_naissance": request.form.get("date_naissance", ""),
            "sexe": request.form.get("sexe", ""),
            "telephone": request.form.get("telephone", ""),
            "adresse": request.form.get("adresse", ""),
            "groupe_sanguin": request.form.get("groupe_sanguin", ""),
            "service": request.form.get("service", ""),
            "medecin": request.form.get("medecin", ""),
            "salle": request.form.get("salle", ""),
            "motif": request.form.get("motif", ""),
            "antecedents": request.form.get("antecedents", ""),
            "allergies": request.form.get("allergies", ""),
            "symptomes": request.form.getlist("symptomes"),
            "statut": request.form.get("statut", "En consultation"),
            "urgence": request.form.get("urgence", "Non"),
            "date_entree": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "date_sortie": "",
            "diagnostic": "",
            "traitement": "",
            "notes": ""
        }
        patients.append(patient)
        save_patients(patients)
        return redirect(url_for("fiche_patient", pid=pid))
    return render_template("nouveau_patient.html")

@app.route("/patient/<pid>")
def fiche_patient(pid):
    patients = load_patients()
    patient = next((p for p in patients if p["id_patient"] == pid), None)
    if not patient:
        return redirect(url_for("patients"))
    return render_template("fiche_patient.html", patient=patient)

@app.route("/patient/<pid>/modifier", methods=["GET", "POST"])
def modifier_patient(pid):
    patients = load_patients()
    idx = next((i for i, p in enumerate(patients) if p["id_patient"] == pid), None)
    if idx is None:
        return redirect(url_for("patients"))
    if request.method == "POST":
        patients[idx].update({
            "diagnostic": request.form.get("diagnostic", ""),
            "traitement": request.form.get("traitement", ""),
            "notes": request.form.get("notes", ""),
            "statut": request.form.get("statut", ""),
            "salle": request.form.get("salle", ""),
            "medecin": request.form.get("medecin", ""),
            "date_sortie": request.form.get("date_sortie", "")
        })
        save_patients(patients)
        return redirect(url_for("fiche_patient", pid=pid))
    return render_template("modifier_patient.html", patient=patients[idx])

@app.route("/patient/<pid>/supprimer", methods=["POST"])
def supprimer_patient(pid):
    patients = load_patients()
    patients = [p for p in patients if p["id_patient"] != pid]
    save_patients(patients)
    return redirect(url_for("patients"))

@app.route("/statistiques")
def statistiques():
    patients = load_patients()
    services = {}
    statuts = {}
    sexes = {"Masculin": 0, "Féminin": 0}
    groupes = {}
    for p in patients:
        s = p.get("service", "Inconnu")
        services[s] = services.get(s, 0) + 1
        st = p.get("statut", "Inconnu")
        statuts[st] = statuts.get(st, 0) + 1
        sx = p.get("sexe", "")
        if sx in sexes:
            sexes[sx] += 1
        g = p.get("groupe_sanguin", "Inconnu")
        if g:
            groupes[g] = groupes.get(g, 0) + 1
    return render_template("statistiques.html",
                           services=services, statuts=statuts,
                           sexes=sexes, groupes=groupes,
                           total=len(patients), patients=patients)

@app.route("/api/stats")
def api_stats():
    patients = load_patients()
    services = {}
    for p in patients:
        s = p.get("service", "Inconnu")
        services[s] = services.get(s, 0) + 1
    return jsonify(services)

if __name__ == "__main__":
    app.run(debug=True)
