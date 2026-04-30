from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Connexion base de données
def get_db():
    Conn = sqlite3.connect("database.db")
    Conn.row_factory = sqlite3.Row
    return Conn

# Création table
def init_db():
    Conn = get_db()
    Conn.execute("""
        CREATE TABLE IF NOT EXISTS depenses (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Montant REAL,
            Categorie TEXT,
            Date TEXT,
            Description TEXT
        )
    """)
    Conn.execute ("""
                  CREATE TABLE IF NOT EXISTS configuration
                  (solde_initial REAL)
                  """)
    Conn.commit
    Conn.close()
    

init_db()
# Page principale (formulaire)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        Montant = request.form["montant"]
        Categorie = request.form["categorie"]
        Date = request.form["date"]
        Description = request.form["description"]

        if not Montant:
            return "Erreur: montant obligatoire"

        Conn = get_db()
        Conn.execute(
            "insert INTO depenses (montant, categorie, date, description) VALUES (?,?,?,?)",
            (Montant, Categorie, Date, Description)
        )
        Conn.commit()
        Conn.close()

        return redirect("/dashboard")

    return render_template("RSafeTrack.html")
@app.route('/set_budget', methods=['POST'])
def set_budget():
    Budget = request.form.get('budget')
    Conn = get_db()
    # On efface l’ancien budget pour ne garder que le nouveau
    Conn.execute("DELETE FROM configuration") 
    Conn.execute("INSERT INTO configuration (solde_initial) VALUES (?)", (Budget,))
    Conn.commit()
    Conn.close()
    return redirect('/dashboard')


# Dashboard (analyse)
@app.route("/dashboard")
def dashboard():
    Conn = get_db()

    res_Total= Conn.execute("SELECT SUM(montant) FROM depenses").fetchone()
    Total=res_Total[0] if res_Total[0] else 0

    res_Moyenne = Conn.execute("SELECT AVG(montant) FROM depenses").fetchone()
    Moyenne=res_Moyenne[0] if res_Moyenne and res_Moyenne[0] is not None else 0
    
    cat_rows= Conn.execute("""
        SELECT categorie, SUM(montant) as Total
        FROM depenses
        GROUP BY categorie
    """).fetchall()
    Categories=[[r[0],r[1]] for r in cat_rows]


    date_rows = Conn.execute("""
        SELECT date, SUM(montant) as Total
        FROM depenses
        GROUP BY date
    """).fetchall()
    Dates=[[r[0],r[1]] for r in date_rows]

    Conn.close()

    return render_template(
        "dashboard.html",
        Total=Total,
        Moyenne=Moyenne,
        Categories=Categories,
        Dates=Dates
    )

if __name__ == "__main__":
    app.run(debug=True)
