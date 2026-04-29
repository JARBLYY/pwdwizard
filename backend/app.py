from flask import Flask, render_template, request, redirect, url_for, session, flash
from PWDWizard.MasterPassword import get_key_from_password
from PWDWizard.MySQL import create_db, load_or_create_salt
from PWDWizard.SavingAndRetrieving import save_password, save_generated_password, get_passwords
import mysql.connector
import traceback

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-in-prod"


def get_key():
    """Retrieve the encryption key from session."""
    key = session.get("key")
    if isinstance(key, list):
        key = bytes(key)
    return key


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        master_pw = request.form.get("master_password", "")
        if not master_pw:
            flash("Master password is required.", "error")
            return render_template("login.html")
        try:
            salt = load_or_create_salt()
            key = get_key_from_password(master_pw, salt)
            session["key"] = list(key)  # store bytes as list for JSON serialization
            return redirect(url_for("dashboard"))
        except Exception as e:
            import traceback
            traceback.print_exc()
            flash(f"Error processing master password: {str(e)}", "error")
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    key = get_key()
    if not key:
        return redirect(url_for("login"))
    try:
        passwords = _get_passwords_list(key)
    except Exception:
        passwords = []
    return render_template("dashboard.html", passwords=passwords)


@app.route("/add", methods=["GET", "POST"])
def add_password():
    key = get_key()
    if not key:
        return redirect(url_for("login"))

    if request.method == "POST":
        website = request.form.get("website", "").strip()
        username = request.form.get("username", "").strip()
        mode = request.form.get("mode", "manual")
        password = request.form.get("password", "").strip()

        if not website or not username:
            flash("Website and username are required.", "error")
            return render_template("add_password.html")

        try:
            if mode == "generate":
                generated = save_generated_password(website, username, key)
                flash(f"Generated password saved: {generated}", "success")
            else:
                if not password:
                    flash("Password is required.", "error")
                    return render_template("add_password.html")
                save_password(website, username, password, key)
                flash("Password saved successfully.", "success")
            return redirect(url_for("dashboard"))
        except Exception as e:
            flash(f"Error saving password: {str(e)}", "error")

    return render_template("add_password.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


def _get_passwords_list(key):
    """Return passwords as a list of dicts instead of printing them."""
    from PWDWizard.MySQL import get_connection
    from PWDWizard.EncryptAndDecrypt import decrypt_password

    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT website, username, password FROM passwords")
    rows = c.fetchall()
    conn.close()

    results = []
    for website, username, encrypted_pw in rows:
        try:
            decrypted = decrypt_password(key, encrypted_pw)
        except Exception:
            decrypted = "[decryption failed]"
        results.append({"website": website, "username": username, "password": decrypted})
    return results


create_db()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
