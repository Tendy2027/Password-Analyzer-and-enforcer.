import re
import sys

# ─────────────────────────────────────────────
#  PASSWORD STRENGTH ANALYSER & ENFORCER
#  Project 1 — Application Security Learning
# ─────────────────────────────────────────────

def analyse_password(password):
    """
    Analyses a password and returns a detailed report.
    Returns a dictionary with score, strength label, and feedback.
    """

    feedback = []  # List of improvement suggestions
    score = 0      # We'll build up a score out of 100

    # ── 1. LENGTH CHECKS ──────────────────────────────────────────
    length = len(password)

    if length == 0:
        return {
            "score": 0,
            "strength": "Invalid",
            "passed": False,
            "feedback": ["Password cannot be empty."]
        }
    elif length < 8:
        feedback.append("Too short — use at least 8 characters.")
        score += 5   # tiny credit for trying
    elif length < 12:
        score += 20
        feedback.append("Good start — 12+ characters would be stronger.")
    elif length < 16:
        score += 30
    else:
        score += 40  # long passwords are the best defence
        feedback.append("Great length! 💪")

    # ── 2. CHARACTER VARIETY CHECKS ───────────────────────────────

    has_upper   = bool(re.search(r'[A-Z]', password))
    has_lower   = bool(re.search(r'[a-z]', password))
    has_digit   = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>_\-\\/\[\]=+;\'`~]', password))

    if has_upper:
        score += 15
    else:
        feedback.append("Add uppercase letters (A–Z).")

    if has_lower:
        score += 15
    else:
        feedback.append("Add lowercase letters (a–z).")

    if has_digit:
        score += 15
    else:
        feedback.append("Add numbers (0–9).")

    if has_special:
        score += 15
    else:
        feedback.append("Add special characters (!@#$%^&* etc.).")

    # ── 3. COMMON PATTERN PENALTIES ───────────────────────────────
    
    common_patterns = [
        r'1234', r'abcd', r'qwerty', r'password',
        r'letmein', r'admin', r'welcome', r'monkey',
        r'(.)\1{2,}'  # same character repeated 3+ times (e.g. "aaa")
    ]

    for pattern in common_patterns:
        if re.search(pattern, password, re.IGNORECASE):
            score -= 20
            feedback.append("⚠️  Avoid common patterns/sequences (e.g. '1234', 'qwerty', 'password').")
            break  # only penalise once

    # Clamp score between 0 and 100
    score = max(0, min(score, 100))

    # ── 4. STRENGTH LABEL ─────────────────────────────────────────
    if score < 30:
        strength = "🔴 Weak"
    elif score < 50:
        strength = "🟠 Moderate"
    elif score < 75:
        strength = "🟡 Strong"
    else:
        strength = "🟢 Very Strong"

    # ── 5. ENFORCEMENT GATE ───────────────────────────────────────
    # A password PASSES enforcement only if it meets minimum standards:
    # length >= 8, has upper, lower, digit, and special char, score >= 50
    passed = (
        length >= 8 and
        has_upper and
        has_lower and
        has_digit and
        has_special and
        score >= 50
    )

    if not passed and not feedback:
        feedback.append("Password does not meet the minimum security requirements.")

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


def print_report(password, result):
    """Prints a formatted security report to the terminal."""

    print("\n" + "═" * 45)
    print("   🔐 PASSWORD STRENGTH REPORT")
    print("═" * 45)
    print(f"  Password : {'*' * len(password)}")   # never echo passwords in plaintext!
    print(f"  Score    : {result['score']} / 100")
    print(f"  Strength : {result['strength']}")
    print(f"  Status   : {'✅ PASSED' if result['passed'] else '❌ FAILED — does not meet policy'}")

    print("\n  📋 Details:")
    d = result["details"]
    print(f"     Length          : {d['length']} chars")
    print(f"     Uppercase (A-Z) : {'✔' if d['has_uppercase'] else '✘'}")
    print(f"     Lowercase (a-z) : {'✔' if d['has_lowercase'] else '✘'}")
    print(f"     Digits (0-9)    : {'✔' if d['has_digit'] else '✘'}")
    print(f"     Special chars   : {'✔' if d['has_special'] else '✘'}")

    if result["feedback"]:
        print("\n  💡 Suggestions:")
        for tip in result["feedback"]:
            print(f"     • {tip}")

    print("═" * 45 + "\n")


# ─────────────────────────────────────────────
#  MAIN — Interactive loop
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🔐 Welcome to the Password Strength Analyser")
    print("   Type 'quit' to exit.\n")

    while True:
        try:
            pwd = input("  Enter a password to analyse: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n  Goodbye! Stay secure. 👋")
            sys.exit(0)

        if pwd.lower() == "quit":
            print("  Goodbye! Stay secure. 👋\n")
            break

        result = analyse_password(pwd)
        print_report(pwd, result)