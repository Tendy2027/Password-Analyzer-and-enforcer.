from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)


def analyse_password(password):
    feedback = []
    score = 0

    length = len(password)

    if length == 0:
        return {"score": 0, "strength": "Invalid", "passed": False, "feedback": ["Password cannot be empty."]}
    elif length < 8:
        feedback.append("Too short — use at least 8 characters.")
        score += 5
    elif length < 12:
        score += 20
        feedback.append("Good start — 12+ characters would be stronger.")
    elif length < 16:
        score += 30
    else:
        score += 40
        feedback.append("Great length!")

    has_upper   = bool(re.search(r'[A-Z]', password))
    has_lower   = bool(re.search(r'[a-z]', password))
    has_digit   = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>_\-\\/\[\]=+;\'`~]', password))

    if has_upper:   score += 15
    else:           feedback.append("Add uppercase letters (A-Z).")

    if has_lower:   score += 15
    else:           feedback.append("Add lowercase letters (a-z).")

    if has_digit:   score += 15
    else:           feedback.append("Add numbers (0-9).")

    if has_special: score += 15
    else:           feedback.append("Add special characters (!@#$%^&* etc.).")

    common_patterns = [
        r'1234', r'abcd', r'qwerty', r'password',
        r'letmein', r'admin', r'welcome', r'monkey',
        r'(.)\1{2,}'
    ]
    for pattern in common_patterns:
        if re.search(pattern, password, re.IGNORECASE):
            score -= 20
            feedback.append("Avoid common patterns/sequences.")
            break

    score = max(0, min(score, 100))

    if score < 30:      strength = "Weak"
    elif score < 50:    strength = "Moderate"
    elif score < 75:    strength = "Strong"
    else:               strength = "Very Strong"

    passed = (
        length >= 8 and
        has_upper and has_lower and
        has_digit and has_special and
        score >= 50
    )

    return {
        "score": score,
        "strength": strength,
        "passed": passed,
        "feedback": feedback,
        "details": {
            "length": length,
            "has_uppercase": has_upper,
            "has_lowercase": has_lower,
            "has_digit": has_digit,
            "has_special": has_special,
        }
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/analyse", methods=["POST"])
def api_analyse():
    data = request.get_json()
    password = data.get("password", "")
    result = analyse_password(password)
    return jsonify(result)


@app.route("/api/submit", methods=["POST"])
def api_submit():
    data = request.get_json()
    password = data.get("password", "")
    print(f"[SERVER] Submit attempt — length: {len(password)}")
    result = analyse_password(password)
    if result["passed"]:
        return jsonify({"success": True, "message": "Password accepted by server. Account would be created."})
    else:
        return jsonify({
            "success": False,
            "message": "Server rejected this password. Client-side bypass failed.",
            "feedback": result["feedback"],
            "score": result["score"]
        }), 400


if __name__ == "__main__":
    print("\nPassword Enforcer Server running!")
    print("   Open http://127.0.0.1:5000 in your browser\n")
    app.run(debug=True)
    