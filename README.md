<div align="center">

# CORESYNC

**A VERIFICATION ENGINE FOR DECISION-BASED SYSTEMS.**

FEED IT A SET OF ARCHITECTURAL DECISIONS AND CONSTRAINTS. IT TELLS YOU WHERE THEY CONTRADICT EACH OTHER, WHERE THEY'RE INCOMPLETE, AND WHERE THE STRUCTURE DOESN'T HOLD — BEFORE ANY OF IT REACHES PRODUCTION.

![Python](https://img.shields.io/badge/PYTHON-3.12%2B-2ea44f?style=for-the-badge&labelColor=333)
![Status](https://img.shields.io/badge/STATUS-ACTIVE-2ea44f?style=for-the-badge&labelColor=333)
![License](https://img.shields.io/badge/LICENSE-MIT-2ea44f?style=for-the-badge&labelColor=333)
![Version](https://img.shields.io/badge/VERSION-1.0.0-2ea44f?style=for-the-badge&labelColor=333)
![Dependencies](https://img.shields.io/badge/DEPENDENCIES-ZERO-2ea44f?style=for-the-badge&labelColor=333)

</div>

---

## WHY THIS EXISTS

MOST SYSTEM DESIGN REVIEWS ARE MANUAL, INCONSISTENT, AND CAUGHT LATE. CORESYNC RUNS THREE CLASSES OF CHECKS — COMPLETENESS, CONSISTENCY, AND STRUCTURE — AND COMPRESSES THE RESULT INTO A SINGLE SCORE OUT OF 100 WITH A CLEAR VERDICT. NO GUESSWORK ABOUT WHETHER A DESIGN IS READY TO SHIP.

## INSTALL

```bash
git clone https://github.com/cyc3o/CoreSync
cd CoreSync
python main.py
```

ZERO DEPENDENCIES. RUNS ON PURE PYTHON 3.12+, NOTHING ELSE TO SET UP.

OPTIONAL DEV TOOLS: `pip install -r requirements.txt`

## USAGE

```bash
python main.py
# SELECT "1" TO ANALYZE A SYSTEM
# PICK A JSON FILE FROM datasets/
# REVIEW THE HTML REPORT IN logs/
```

---

## LICENSE

MIT — USE IT, MODIFY IT, SHARE IT.

---

**CORESYNC** — CREATED BY VISHAL THAKUR
