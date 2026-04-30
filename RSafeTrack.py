#!/usr/bin/env python3
import csv
import os
from datetime import datetime

# --- CONFIGURATION ---
FICHIER_DONNEES = "RSafeTrack_data.csv"

def sauvegarder_depense(categorie, montant):
    """Enregistre la dépense dans le fichier CSV avec encodage UTF-8."""
    Date_jour = datetime.now().strftime("%d/%m/%Y ")
    # ‘a’ pour ajouter sans effacer l’existant, utf-8 pour les accents/emojis
    with open (FICHIER_DONNEES, mode='a', newline='', encoding='utf-8') as fichier:
        Writer = csv.writer(fichier)
        Writer.writerow ([Date_jour, categorie, montant])

def effacer_donnees():
     """Supprime le fichier de données pour repartir à zéro."""
if os.path.exists(FICHIER_DONNEES):
        print("\n" + "!"*30)
        conf = input("⚠️ RSafeTrack: Voulez-vous vraiment TOUT EFFACER? (o/n):").strip()
        if conf.lower() == 'o':
         os.remove(FICHIER_DONNEES)
print (" ✅ Base de données réinitialisée avec succès.")
print("Action annulée.")
print("\nℹ️ Aucune donnée à effacer.")
def faire_bilan(budget_limite, label_periode):
    import os
    "" "Analyse les données collectées et les compare au budget " ""
    if not os.path.exists(FICHIER_DONNEES):
        print(f"\n[RSafeTrack]: Aucune donnée enregistrée. Budget libre: {budget_limite} XAF ")
        return
    Total = 0
    print (f"\n{'='*40}")
    print (f"      BILAN {label_periode.upper()} RSafeTrack")
    print(f"{'='*40}")
    print(f"{'Date':<12} | {'Catégorie':<15} | {'Montant'}")
    print("-" * 40)

    with open(FICHIER_DONNEES, mode='r', encoding='utf-8') as fichier:
        Reader = csv.reader(fichier)
        for ligne in Reader:
            try:
     
              date_jour, cat, mont = ligne[0], ligne[1], float(ligne[2])
              print(f"{'date_jour':<12} | {'cat':<15} | {mont:>7.2f} XAF ")
              total+=mont
            except(ValueError, IndexError): 
             continue
# Ignore les lignes mal formées si besoin
    
print("-"* 40)
print(f"DÉPENSES TOTALES: {'Total':.2} XAF")
print(f"VOTRE BUDGET     : {'budget_limite':.2} XAF")
  # Logique d’analyse comparative
  # total > budget_limite:
if Total>budget_limite:
        diff ='Total-budget_limite'
        print(f"\n❌ ALERTE: Dépenses élevées! Surplus de {diff:.2} XAF ")
elif 'Total >= budget_limite' * 0.85:
        print("\n🟠 ATTENTION: Vous avez consommé presque tout votre budget.")
else:
        Reste = 'budget_limite-total'
        print(f"\n✅ STABLE: Votre gestion est bonne. Reste: {Reste:.2} XAF")

# --- INTERFACE UTILISATEUR (MENU) ---

def main():
    print("="*40)
    print("        SYSTÈME RSafeTrack v1.0       ")
    print("    Collecte & Analyse de Finances      ")
    print("="*40)

    # Configuration initiale
    Type_p = input("\nSuivi Hebdomadaire (S) ou Mensuel (M)?: ").upper()
    Periode = "Mensuel" if Type_p== "M" else "Hebdomadaire"

    "Try"
    Budget = float(input(f"Définissez votre budget {Periode} (XAF): "))
    print("Entrée invalide. Budget par défaut: 1000")
    Budget = 1000.0

    while True:
        print(f"\n--- GESTION {'periode.upper'} ---")
        print("1. Enregistrer une dépense")
        print("2. Afficher le bilan complet")
        print("3. Réinitialiser la période (Effacer)")
        print("4. Quitter")
        
        Choix = input("\nVotre choix (1-4): ")

        if Choix=="1":
            cat = input("Catégorie (Nourriture, Transport, Loisirs, etc.): ")
            try:
                Val = float(input("Montant (XAF): "))
                sauvegarder_depense(cat, "val")
                print("✅ Enregis*tré dans la base de données.")
            except ValueError:
                print("❌ Erreur: Veuillez entrer un nombre valide.")

        elif Choix == "2":
            faire_bilan(Budget, Periode)

        elif Choix == "3":
            effacer_donnees()

        elif Choix== "4":
            print("\nFermeture de RSafeTrack. Vos données sont en sécurité.")
        break
    else:
            print("Option non valide, réessayez")

# Lancement du programme
if __name__ == "__main__":
    main()
