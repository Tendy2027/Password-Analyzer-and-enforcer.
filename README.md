# Password-Analyzer-and-enforcer.
I just built my first Application Security project from scratch — a Password Strength Analyser &amp; Enforcer.

Password Strength Analyser & Enforcer 
Project 1 of my Application Security learning journey  
> Built to understand the difference between client-side and server-side 
validation — and why that difference is a critical security boundary. 
The Core AppSec Lesson 
Never trust the client!! 
This project was deliberately built in two phases to demonstrate one of 
the most important principles in Application Security: 
| Layer | Role | Trustworthy? | 
|-------|------|-------------| 
| JavaScript (browser) | User experience — instant feedback | ❌ Can be 
disabled by anyone | 
| Python / Flask (server) | Real enforcement | ✅ Attacker cannot bypass 
this | 
If your password policy only lives in JavaScript, a single `curl` command 
defeats it. 
Project Structure 
password-strength-analyser/ 
│ 
├── app.py                  
├── password_analyser.py    
├── requirements.txt        
│ 
└── index.html          
# Flask server + enforcement logic (Phase 2) 
# Standalone CLI analyser (Phase 1) 
# Python dependencies 
# Frontend UI 
The problem: 
I built a password strength analyser, but the goal wasn't really the 
analyser — it was to understand a core security vulnerability that exists 
in most web apps. 
What I discovered: 
Most developers only validate passwords in JavaScript on the frontend. I 
wanted to demonstrate why that's dangerous, so I deliberately built a 
bypass — a button that simulates what an attacker does with a tool like 
Burp Suite or curl. It skips the JavaScript entirely and sends a weak 
password straight to the server. 
This is the 'never trust the client' principle. It applies beyond 
passwords — to any input a user submits. Form data, file uploads, API 
requests — the frontend can always be manipulated, so the backend must 
always validate independently. 
Features 
Phase 1 — Python CLI - Password scoring system (0–100) 
- Regex-based character variety detection (uppercase, lowercase, digits, 
special chars) - Common pattern detection and penalties (`password`, `qwerty`, `1234`, 
repeated chars) - Clear strength labels: Weak / Moderate / Strong / Very Strong - Enforcement gate — pass/fail based on minimum security policy - Never echoes passwords in plaintext (a security habit from day one) 
Phase 2 — Flask Web App - Live strength meter as you type (calls server on every keystroke) - Visual checklist of all password requirements - Colour-coded strength bar - Bypass JS button— simulates an attacker disabling JS and submitting 
directly to the server - Server rejects weak passwords regardless of what the browser did - Demonstrates why server-side validation is the only real security gat 
Tech Stack -Python 3 — core analysis logic - Flask — lightweight web server and REST API - Regex (`re`)— pattern detection - HTML / CSS / JavaScrip — frontend UI (vanilla, no frameworks) 
Getting Started 
1. Clone the repo 
bash 
git clone https://github.com/YOUR_USERNAME/password-strength-analyser.git 
cd password-strength-analyser 
2. Install dependencies 
bash 
pip install -r requirements.txt 
3. Run Phase 1 (CLI) 
```bash 
python password_analyser.py 
``` 
4. Run Phase 2 (Web App) 
```bash 
python app.py 
``` 
Then open your browser at `http://127.0.0.1:5000` 
Demonstrating the Bypass Attack 
This is the most important part of the project. 
What a real attacker does: 
```bash 
Submit a weak password directly to the server, skipping the browser 
entirely 
curl -X POST http://127.0.0.1:5000/api/submit \ -H "Content-Type: application/json" \ -d '{"password": "abc"}' 
``` 
Server response: 
```json 
{ 
"success": false, 
"message": "Server rejected this password. Client-side bypass failed.", 
"score": 20, 
"feedback": ["Too short — use at least 8 characters.", "Add uppercase 
letters (A–Z).", ...] 
} 
``` 
The browser UI's "Submit" button is disabled for weak passwords — but 
that's just UX. The server enforces the real policy every single time. 
Scoring System 
| Criteria | Points | 
|----------|--------| 
| Length 8–11 chars | +20 | 
| Length 12–15 chars | +30 | 
| Length 16+ chars | +40 | 
| Has uppercase (A–Z) | +15 | 
| Has lowercase (a–z) | +15 | 
| Has digits (0–9) | +15 | 
| Has special characters | +15 | 
| Common pattern detected | −20 | 
Enforcement gate (must pass ALL): - Length ≥ 8 - Has uppercase, lowercase, digit, and special character - Score ≥ 50 
AppSec Concepts Covered - Client-side vs server-side validation - Why "never trust the client" is a foundational security principle - Regex-based pattern detection (used in WAFs, IDS, and security tools) - The difference between a password *checker* and a password *enforcer* - Safe terminal practices (never echoing passwords in plaintext) - How attackers use tools like `curl` and Burp Suite to bypass frontend 
controls 
Author 
Built as part of a hands-on Application Security learning journey.   
Follow along as I build more security projects from scratch. 
If this helped you understand client vs server validation, give it a star
