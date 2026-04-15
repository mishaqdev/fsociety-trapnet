# FSociety TrapNet - Cybersecurity Project


## Overview

This project is a web-based honeypot system designed to simulate vulnerable endpoints and capture malicious activities in a controlled environment.

The goal is to:
- Monitor attacker behavior
- Log intrusion attempts
- Analyze real-world attack patterns
- Improve defensive security skills

## Features

- Fake vulnerable web endpoints
- Dashboard for monitoring attacks
- Logging of attacker payloads, IPs, and requests
- Separate user authentication system
- Structured database for attack & user data

## How It Works

1. The honeypot exposes intentionally vulnerable-looking endpoints (e.g., login form).
2. The authentication system is deliberately non-functional:
   - Every login attempt returns an "Invalid Credentials" response
   - No real authentication or session is created
3. This design encourages attackers to:
   - Attempt brute-force attacks
   - Inject payloads (SQLi, XSS, etc.)
4. All incoming requests and payloads are:
   - Logged in detail
   - Stored in the attack database
5. The admin dashboard provides visibility into:
   - Login attempts
   - Payloads used
   - Request patterns
  
## Installation & Setup

1. ### Clone the repository

```bash
git clone https://github.com/mishaqdev/honeypot-website.git
cd fsociety-trapnet
```

2. ### Install dependencies

```bash
pip install -r requirements.txt
```

4. ### Run the vulnerable website

```bash
python -m honeypot.app
```

5. ### Attack the localhost website using the script (Optional)

```bash
python run attackScript.py
```

6. ### Run dashboard for analysis

```bash
python -m dashboard.app
```

## Use Cases

- Cybersecurity learning & practice
- Ethical hacking labs
- Attack pattern analysis
- Logging & monitoring research

## 📬 Contact

<p align="center">
  <a href="https://github.com/mishaqdev">
    <img src="https://img.shields.io/badge/GitHub-mishaqdev-181717?style=for-the-badge&logo=github" />
  </a>
  
  <a href="https://www.linkedin.com/in/mishaqdev">
    <img src="https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin" style="margin-left:10px;" />
  </a>
  
  <a href="mailto:muhammadishaq.dev@example.com">
    <img src="https://img.shields.io/badge/Email-Contact-red?style=for-the-badge&logo=gmail" style="margin-left:10px;" />
  </a>
</p>
