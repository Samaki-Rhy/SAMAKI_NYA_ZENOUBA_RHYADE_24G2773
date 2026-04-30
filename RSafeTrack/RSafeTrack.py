from flask import Flask, render_template, request, redirect, url_for
import csv
import os
from datetime import datetime

RSafeTrack = Flask(__name__)
FICHIER_DONNEES = "RSafeTrack_global.csv"

# Configuration par défaut (sera modifiée par l’utilisateur sur le site)
Config_app = {
    "periode": "Mensuel",
    "budget": 5000.0
}

def charger_donnees():
    Lignes = []
    Total_general = 0
    if os.path.exists(FICHIER_DONNEES):
        with open(FICHIER_DONNEES, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    # Structure CSV : Nom, Date, Catégorie, Montant, Statut
                    M = float(row[3])
                    Total_general += M
                    Lignes.append({
                        "nom": row[0],
                        "date": row[1],
                        "categorie": row[2],
                      
                                "montant": M,
                        "statut": row[4]
                    })
                except:

                 continue
    return Lignes, Total_general

@RSafeTrack.route('/')
def index():
    Historique, Total = charger_donnees()
    Budget = Config_app["budget"]
    Reste = Budget - Total
    
    # Message global pour le propriétaire (Toi)
    if Total > Budget:
        Msg = f"Alerte: Budget global dépassé de {abs(Reste)} XAF"
        Style = "danger"
    else:
        Msg = f"Économie globale: {Reste} XAF"
        Style = "success"

    return render_template('RSafeTrack.html',Depenses=Historique, Total=Total, budget=Budget, Periode=Config_app["periode"], message=Msg, style=Style)

@RSafeTrack.route('/ajouter', methods=['POST'])
def ajouter():
    Nom = request.form.get('nom_utilisateur')
    Cat = request.form.get('categorie')
    Mont = float(request.form.get('montant', 0))
    date_j = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # Calcul du statut pour cette dépense précise
    Budget = Config_app["budget"]
    if Mont > (Budget* 0.5): # Si une seule dépense fait plus de 50% du budget
        Statut = "DÉPENSE LOURDE"
    elif Mont > 0:
        Statut = "GESTION OK"
    else:
        Statut = "INVALIDE"

    # Enregistrement dans la base de données csv
    with open(FICHIER_DONNEES, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([Nom, date_j, Cat, Mont, Statut])
        
    return redirect(url_for('index'))

@RSafeTrack.route('/configurer', methods=['POST'])
def configurer():
    Config_app["periode"] = request.form.get('periode')
    Config_app["budget"] = float(request.form.get('budget', 5000))
    return redirect(url_for('index'))

if __name__ == "__main__":
    port= int(os.environ.get("PORT",5000))
    RSafeTrack.run(host='0.0.0.0' , port=5000)
