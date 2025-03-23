import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import re


# Connexion à la base de données
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="0000",  # Remplace par ton mot de passe MySQL
            database="repertoire"
        )
        return connection
    except mysql.connector.Error as e:
        messagebox.showerror("Erreur", f"Erreur de connexion : {e}")
        return None


# Vérification du numéro de téléphone (10 chiffres)
def verifier_numero(telephone):
    if re.match(r'^\d{10}$', telephone):
        entry_telephone.config(fg="green")  # ✅ Vert si le numéro est correct
        return True
    else:
        entry_telephone.config(fg="red")  # ❌ Rouge si le numéro est incorrect
        return False


# Vérification de l'email (format nom@domaine.xx)
def verifier_email(email):
    if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        entry_email.config(fg="green")  # ✅ Vert si email valide
        return True
    else:
        entry_email.config(fg="red")  # ❌ Rouge si email invalide
        return False


# Fonction pour ajouter un contact
def ajouter_contact():
    nom = entry_nom.get()
    telephone = entry_telephone.get()
    email = entry_email.get()

    if nom == "" or telephone == "" or email == "":
        messagebox.showwarning("Erreur", "Veuillez remplir tous les champs")
        return

    if not verifier_numero(telephone):
        messagebox.showwarning("Erreur", "Numéro de téléphone invalide (10 chiffres)")
        return

    if not verifier_email(email):
        messagebox.showwarning("Erreur", "Adresse email invalide")
        return

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO contacts (nom, telephone, email) VALUES (%s, %s, %s)",
                (nom, telephone, email)
            )
            conn.commit()
            messagebox.showinfo("Succès", "Contact ajouté avec succès !")
            afficher_contacts()
            entry_nom.delete(0, tk.END)
            entry_telephone.delete(0, tk.END)
            entry_email.delete(0, tk.END)
            entry_telephone.config(fg="black")
            entry_email.config(fg="black")
        except mysql.connector.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout : {e}")
        finally:
            cursor.close()
            conn.close()


# Fonction pour afficher les contacts
def afficher_contacts():
    for row in listbox.get_children():
        listbox.delete(row)

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts")
        rows = cursor.fetchall()
        for row in rows:
            listbox.insert("", "end", values=row)
        cursor.close()
        conn.close()


# Fonction pour supprimer un contact
def supprimer_contact():
    selected_item = listbox.selection()
    if not selected_item:
        messagebox.showwarning("Erreur", "Veuillez sélectionner un contact à supprimer")
        return

    contact_id = listbox.item(selected_item[0])['values'][0]

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
            conn.commit()
            messagebox.showinfo("Succès", "Contact supprimé avec succès !")
            afficher_contacts()
        except mysql.connector.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression : {e}")
        finally:
            cursor.close()
            conn.close()


# Fonction pour mettre à jour un contact
def mettre_a_jour_contact():
    selected_item = listbox.selection()
    if not selected_item:
        messagebox.showwarning("Erreur", "Veuillez sélectionner un contact à mettre à jour")
        return

    contact_id = listbox.item(selected_item[0])['values'][0]
    nouveau_nom = entry_nom.get()
    nouveau_telephone = entry_telephone.get()
    nouveau_email = entry_email.get()

    if nouveau_nom == "" or nouveau_telephone == "" or nouveau_email == "":
        messagebox.showwarning("Erreur", "Veuillez remplir tous les champs")
        return

    if not verifier_numero(nouveau_telephone):
        messagebox.showwarning("Erreur", "Numéro de téléphone invalide (10 chiffres)")
        return

    if not verifier_email(nouveau_email):
        messagebox.showwarning("Erreur", "Adresse email invalide")
        return

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE contacts SET nom = %s, telephone = %s, email = %s WHERE id = %s",
                (nouveau_nom, nouveau_telephone, nouveau_email, contact_id)
            )
            conn.commit()
            messagebox.showinfo("Succès", "Contact mis à jour avec succès !")
            afficher_contacts()
            entry_nom.delete(0, tk.END)
            entry_telephone.delete(0, tk.END)
            entry_email.delete(0, tk.END)
            entry_telephone.config(fg="black")
            entry_email.config(fg="black")
        except mysql.connector.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la mise à jour : {e}")
        finally:
            cursor.close()
            conn.close()


# Interface graphique avec Tkinter
root = tk.Tk()
root.title("Répertoire téléphonique")
root.geometry("800x700")  # Taille fixe
root.resizable(False, False)

# 🌈 Style de couleur BLEU
bg_color = "#b3cde0"
table_color = "#6497b1"

root.configure(bg=bg_color)

# 🔤 Champ Nom
tk.Label(root, text="Nom", bg=bg_color, font=("Arial", 16)).pack(pady=5)
entry_nom = tk.Entry(root, font=("Arial", 16), width=40)
entry_nom.pack(pady=5)

# ☎️ Champ Téléphone
tk.Label(root, text="Téléphone", bg=bg_color, font=("Arial", 16)).pack(pady=5)
entry_telephone = tk.Entry(root, font=("Arial", 16), width=40)
entry_telephone.pack(pady=5)

# 📧 Champ Email
tk.Label(root, text="Email", bg=bg_color, font=("Arial", 16)).pack(pady=5)
entry_email = tk.Entry(root, font=("Arial", 16), width=40)
entry_email.pack(pady=5)

# 🎯 Boutons d'action
btn_colors = ["#4caf50", "#f44336", "#ff9800"]
actions = ["Ajouter", "Supprimer", "Modifier"]
commands = [ajouter_contact, supprimer_contact, mettre_a_jour_contact]

frame_buttons = tk.Frame(root, bg=bg_color)
frame_buttons.pack(pady=20)

for i, action in enumerate(actions):
    btn = tk.Button(frame_buttons, text=action, command=commands[i], bg=btn_colors[i], fg="white", width=20, height=2)
    btn.pack(side="left", padx=10)

# 🗂️ Tableau d'affichage des contacts
listbox = ttk.Treeview(root, columns=("ID", "Nom", "Téléphone", "Email"), show="headings", height=25)
listbox.heading("ID", text="ID")
listbox.heading("Nom", text="Nom")
listbox.heading("Téléphone", text="Téléphone")
listbox.heading("Email", text="Email")

listbox.column("ID", width=50)
listbox.column("Nom", width=200)
listbox.column("Téléphone", width=150)
listbox.column("Email", width=250)
listbox.pack(pady=20)

# 🚀 Affichage des contacts
afficher_contacts()

# 🎯 Lancer la boucle principale
root.mainloop()
