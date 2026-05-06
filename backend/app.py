from flask import Flask, render_template, request, redirect, url_for, session, flash
from PWDWizard.MasterPassword import get_key_from_password
from PWDWizard.MySQL import create_db, create_user, get_user, get_connection
from PWDWizard.SavingAndRetrieving import save_password, save_generated_password
from PWDWizard.EncryptAndDecrypt import decrypt_password
import hashlib
import os
import traceback

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-in-prod"


def hash_password(password, salt):
    """Hash a password with a salt for storing in the users table."""
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000).hex()


def get_key():
    """Retrieve the encryption key from session."""
    key = session.get("key")
    if isinstance(key, list):
        key = bytes(key)
    return key


def get_user_id():
    """Retrieve the logged-in user's ID from session."""
    return session.get("user_id")


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        master_pw = request.form.get("master_password", "")

        if not username or not master_pw:
            flash("Username and master password are required.", "error")
            return render_template("login.html")

        try:
            user = get_user(username)
            if not user:
                flash("Invalid username or password.", "error")
                return render_template("login.html")

            user_id, stored_hash, salt = user

            # Verify password
            if hash_password(master_pw, salt) != stored_hash:
                flash("Invalid username or password.", "error")
                return render_template("login.html")

            # Generate encryption key from master password + user's salt
            key = get_key_from_password(master_pw, salt)
            session["key"] = list(key)
            session["user_id"] = user_id
            session["username"] = username
            return redirect(url_for("dashboard"))
        except Exception as e:
            traceback.print_exc()
            flash(f"Error logging in: {str(e)}", "error")

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        master_pw = request.form.get("master_password", "")
        confirm_pw = request.form.get("confirm_password", "")

        if not username or not master_pw:
            flash("Username and master password are required.", "error")
            return render_template("signup.html")

        if master_pw != confirm_pw:
            flash("Passwords do not match.", "error")
            return render_template("signup.html")

        if len(master_pw) < 8:
            flash("Master password must be at least 8 characters.", "error")
            return render_template("signup.html")

        try:
            # Generate a unique salt for this user
            salt = os.urandom(16)
            password_hash = hash_password(master_pw, salt)

            user_id = create_user(username, password_hash, salt)
            if user_id is None:
                flash("Username already taken. Please choose another.", "error")
                return render_template("signup.html")

            # Auto-login after signup
            key = get_key_from_password(master_pw, salt)
            session["key"] = list(key)
            session["user_id"] = user_id
            session["username"] = username
            flash(f"Welcome, {username}! Your vault is ready.", "success")
            return redirect(url_for("dashboard"))
        except Exception as e:
            traceback.print_exc()
            flash(f"Error creating account: {str(e)}", "error")

    return render_template("signup.html")


@app.route("/dashboard")
def dashboard():
    key = get_key()
    user_id = get_user_id()
    if not key or not user_id:
        return redirect(url_for("login"))
    try:
        passwords = _get_passwords_list(key, user_id)
    except Exception:
        traceback.print_exc()
        passwords = []
    return render_template("dashboard.html", passwords=passwords, username=session.get("username"))


@app.route("/add", methods=["GET", "POST"])
def add_password():
    key = get_key()
    user_id = get_user_id()
    if not key or not user_id:
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
                generated = save_generated_password(website, username, key, user_id)
                flash(f"Generated password saved: {generated}", "success")
            else:
                if not password:
                    flash("Password is required.", "error")
                    return render_template("add_password.html")
                save_password(website, username, password, key, user_id)
                flash("Password saved successfully.", "success")
            return redirect(url_for("dashboard"))
        except Exception as e:
            traceback.print_exc()
            flash(f"Error saving password: {str(e)}", "error")

    return render_template("add_password.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


def _get_passwords_list(key, user_id):
    """Return passwords for a specific user as a list of dicts."""
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT website, username, password FROM passwords WHERE user_id = %s",
        (user_id,)
    )
    rows = c.fetchall()
    c.close()
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