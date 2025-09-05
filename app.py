
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
import pandas as pd
from openpyxl import load_workbook

APP_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.environ.get("EXCEL_PATH", os.path.join(APP_DIR, "..", "animal_shelter.xlsx"))
if not os.path.exists(EXCEL_PATH):
    EXCEL_PATH = os.path.join(APP_DIR, "..", "animal_shelter.xlsx")
    if not os.path.exists(EXCEL_PATH):
        EXCEL_PATH = os.path.join(APP_DIR, "animal_shelter.xlsx")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "123456")

def read_all():
    xls = pd.ExcelFile(EXCEL_PATH)
    animals = pd.read_excel(xls, "animals")
    shelters = pd.read_excel(xls, "shelters")
    employees = pd.read_excel(xls, "employees")
    vets = pd.read_excel(xls, "vets")
    examinations = pd.read_excel(xls, "examinations")
    return animals, shelters, employees, vets, examinations

def write_all(animals=None, shelters=None, employees=None, vets=None, examinations=None):
    a, s, e, v, ex = read_all()
    animals = animals if animals is not None else a
    shelters = shelters if shelters is not None else s
    employees = employees if employees is not None else e
    vets = vets if vets is not None else v
    examinations = examinations if examinations is not None else ex

    with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl", mode="w") as writer:
        animals.to_excel(writer, sheet_name="animals", index=False)
        shelters.to_excel(writer, sheet_name="shelters", index=False)
        employees.to_excel(writer, sheet_name="employees", index=False)
        vets.to_excel(writer, sheet_name="vets", index=False)
        examinations.to_excel(writer, sheet_name="examinations", index=False)

def get_logged_shelter_id():
    return session.get("shelter_id")

def require_owner():
    if "shelter_id" not in session:
        flash("Lütfen giriş yapın.", "warning")
        return False
    return True

@app.template_filter("datefmt")
def datefmt(value, fmt="%Y-%m-%d"):
    try:
        if pd.isna(value):
            return ""
        if isinstance(value, str):
            return value[:10]
        return pd.to_datetime(value).strftime(fmt)
    except Exception:
        return str(value)

@app.route("/")
def index():
    animals, shelters, employees, vets, examinations = read_all()
    q = request.args.get("q", "").strip().lower()
    animal_type = request.args.get("animal_type", "").strip()
    shelter_id = request.args.get("shelter_id", "").strip()
    health = request.args.get("health_condition", "").strip()

    filtered = animals.copy()

    if q:
        mask = (
            filtered["name"].astype(str).str.lower().str.contains(q)
            | filtered["breed"].astype(str).str.lower().str.contains(q)
            | filtered["animal_type"].astype(str).str.lower().str.contains(q)
        )
        filtered = filtered[mask]

    if animal_type:
        filtered = filtered[filtered["animal_type"].astype(str) == animal_type]
    
    if shelter_id:
        try:
            sid = int(shelter_id)
            filtered = filtered[filtered["shelter_id"] == sid]
        except ValueError:
            pass

    if health:
        filtered = filtered[filtered["health_condition"].astype(str) == health]


    animal_types = sorted(animals["animal_type"].dropna().astype(str).unique().tolist())
    health_options = sorted(animals["health_condition"].dropna().astype(str).unique().tolist())


    filtered_merged = filtered.merge(
        shelters, left_on='shelter_id', right_on='shelter_id', how='left'
    )

    return render_template(
        "index.html",
        shelters=shelters,
        animals=filtered,  
        merged=filtered_merged,
        animal_types=animal_types,
        health_options=health_options,
        current_filters={
            "q": q,
            "animal_type": animal_type,
            "shelter_id": shelter_id,
            "health_condition": health,
        },
    )

@app.route("/shelter/<int:shelter_id>")
def view_shelter(shelter_id):
    animals, shelters, employees, vets, examinations = read_all()
    shelter = shelters[shelters["shelter_id"] == shelter_id]
    if shelter.empty:
        flash("Barınak bulunamadı.", "danger")
        return redirect(url_for("index"))
    shelter = shelter.iloc[0]

    a = animals[animals["shelter_id"] == shelter_id]
    e = employees[employees["shelter_id"] == shelter_id]

    return render_template("shelter.html", shelter=shelter, animals=a, employees=e)

@app.route("/login", methods=["GET", "POST"])
def login():
    animals, shelters, employees, vets, examinations = read_all()
    error = None
    if request.method == "POST":
        try:
            shelter_id = int(request.form.get("shelter_id"))
        except (TypeError, ValueError):
            shelter_id = None
        password = (request.form.get("password") or "").strip()

        rec = shelters[shelters["shelter_id"] == shelter_id]
        if rec.empty:
            error = "Barınak seçimi geçersiz."
        else:
            rec = rec.iloc[0]
            sheet_pwd_col = None
            for cand in ["password", "pass", "sifre", "şifre"]:
                if cand in shelters.columns:
                    sheet_pwd_col = cand
                    break
            if sheet_pwd_col is None:
                error = "Şifre kolonu 'shelters' sayfasında bulunamadı."
            else:
                real_pw = str(rec[sheet_pwd_col])
                if password == real_pw:
                    session["shelter_id"] = int(rec["shelter_id"])
                    session["shelter_name"] = str(rec["shelter_name"])
                    flash("Giriş başarılı.", "success")
                    return redirect(url_for("dashboard"))
                else:
                    error = "Şifre hatalı."
    return render_template("login.html", shelters=shelters, error=error)

@app.route("/logout")
def logout():
    session.clear()
    flash("Çıkış yapıldı.", "info")
    return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    if not require_owner():
        return redirect(url_for("login"))
    sid = get_logged_shelter_id()
    animals, shelters, employees, vets, examinations = read_all()
    shelter = shelters[shelters["shelter_id"] == sid].iloc[0]
    a = animals[animals["shelter_id"] == sid]
    e = employees[employees["shelter_id"] == sid]
    return render_template("dashboard.html", shelter=shelter, animals=a, employees=e)

# ---------- Manage Animals ----------
@app.route("/animals/add", methods=["GET", "POST"])
def add_animal():
    if not require_owner():
        return redirect(url_for("login"))
    sid = get_logged_shelter_id()
    animals, shelters, employees, vets, examinations = read_all()
    if request.method == "POST":
        form = request.form
        try:
            new_id = int(animals["animal_id"].max()) + 1 if len(animals) else 1
        except Exception:
            new_id = 1
        row = {
            "animal_id": new_id,
            "name": form.get("name"),
            "animal_type": form.get("animal_type"),
            "breed": form.get("breed"),
            "gender": form.get("gender"),
            "age": int(form.get("age") or 0),
            "weight": float(form.get("weight") or 0),
            "neutering_status": form.get("neutering_status"),
            "health_condition": form.get("health_condition"),
            "arrival_date": form.get("arrival_date") or datetime.now().strftime("%Y-%m-%d"),
            "shelter_id": sid,
        }
        animals = pd.concat([animals, pd.DataFrame([row])], ignore_index=True)
        write_all(animals=animals)
        flash("Hayvan eklendi.", "success")
        return redirect(url_for("dashboard"))
    return render_template("animal_form.html", action="add")

@app.route("/animals/<int:animal_id>/delete", methods=["POST"])
def delete_animal(animal_id):
    if not require_owner():
        return redirect(url_for("login"))
    sid = get_logged_shelter_id()
    animals, shelters, employees, vets, examinations = read_all()
    before = len(animals)
    animals = animals[~((animals["animal_id"] == animal_id) & (animals["shelter_id"] == sid))]
    after = len(animals)
    if after < before:
        write_all(animals=animals)
        flash("Hayvan silindi.", "info")
    else:
        flash("Hayvan bulunamadı veya yetkiniz yok.", "warning")
    return redirect(url_for("dashboard"))

@app.route("/animals/<int:animal_id>/edit", methods=["GET", "POST"])
def edit_animal(animal_id):
    if not require_owner():
        return redirect(url_for("login"))
    sid = get_logged_shelter_id()
    animals, shelters, employees, vets, examinations = read_all()
    rec = animals[(animals["animal_id"] == animal_id) & (animals["shelter_id"] == sid)]
    if rec.empty:
        flash("Kayıt bulunamadı.", "danger")
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        form = request.form
        for col in ["name","animal_type","breed","gender","neutering_status","health_condition"]:
            animals.loc[(animals["animal_id"] == animal_id), col] = form.get(col)
        for col in ["age","weight"]:
            val = form.get(col)
            try:
                if col == "age":
                    animals.loc[(animals["animal_id"] == animal_id), col] = int(val) if val else 0
                else:
                    animals.loc[(animals["animal_id"] == animal_id), col] = float(val) if val else 0.0
            except Exception:
                pass
        arrival = form.get("arrival_date")
        if arrival:
            animals.loc[(animals["animal_id"] == animal_id), "arrival_date"] = arrival
        write_all(animals=animals)
        flash("Güncellendi.", "success")
        return redirect(url_for("dashboard"))
    rec = rec.iloc[0].to_dict()
    return render_template("animal_form.html", action="edit", animal=rec)

# ---------- Manage Employees ----------
@app.route("/employees/add", methods=["GET", "POST"])
def add_employee():
    if not require_owner():
        return redirect(url_for("login"))
    sid = get_logged_shelter_id()
    animals, shelters, employees, vets, examinations = read_all()
    if request.method == "POST":
        form = request.form
        try:
            new_id = int(employees["employee_id"].max()) + 1 if len(employees) else 1
        except Exception:
            new_id = 1
        row = {
            "employee_id": new_id,
            "name": form.get("name"),
            "role": form.get("role"),
            "start_date": form.get("start_date") or datetime.now().strftime("%Y-%m-%d"),
            "shelter_id": sid,
        }
        employees = pd.concat([employees, pd.DataFrame([row])], ignore_index=True)
        write_all(employees=employees)
        flash("Çalışan eklendi.", "success")
        return redirect(url_for("dashboard"))
    return render_template("employee_form.html", action="add")

@app.route("/employees/<int:employee_id>/delete", methods=["POST"])
def delete_employee(employee_id):
    if not require_owner():
        return redirect(url_for("login"))
    sid = get_logged_shelter_id()
    animals, shelters, employees, vets, examinations = read_all()
    before = len(employees)
    employees = employees[~((employees["employee_id"] == employee_id) & (employees["shelter_id"] == sid))]
    after = len(employees)
    if after < before:
        write_all(employees=employees)
        flash("Çalışan silindi.", "info")
    else:
        flash("Çalışan bulunamadı veya yetkiniz yok.", "warning")
    return redirect(url_for("dashboard"))

@app.route("/employees/<int:employee_id>/edit", methods=["GET", "POST"])
def edit_employee(employee_id):
    if not require_owner():
        return redirect(url_for("login"))
    sid = get_logged_shelter_id()
    animals, shelters, employees, vets, examinations = read_all()
    rec = employees[(employees["employee_id"] == employee_id) & (employees["shelter_id"] == sid)]
    if rec.empty:
        flash("Kayıt bulunamadı.", "danger")
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        form = request.form
        for col in ["name","role"]:
            employees.loc[(employees["employee_id"] == employee_id), col] = form.get(col)
        start_date = form.get("start_date")
        if start_date:
            employees.loc[(employees["employee_id"] == employee_id), "start_date"] = start_date
        write_all(employees=employees)
        flash("Güncellendi.", "success")
        return redirect(url_for("dashboard"))
    rec = rec.iloc[0].to_dict()
    return render_template("employee_form.html", action="edit", employee=rec)

# -------- Static file helper (for CSS) --------
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(os.path.join(APP_DIR, "static"), filename)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
