
# 🛡️ Phishing URL Detection Pipeline

This project compares a **legitimate (real) URL** against a **suspect URL** to detect possible phishing.
It checks for:

* 🔗 **Domain & URL similarity** (lookalike domains, subdomains, punycode)
* 📄 **Page text similarity**
* 📸 **Visual similarity using full-page screenshots**
* 📝 **JSON report with results & screenshot paths**

---

## 📦 Installation

1. **Clone this repo / download the code**

```bash
git clone https://github.com/yourusername/phishing-checker.git
cd phishing-checker
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

**requirements.txt** should contain:

```
beautifulsoup4
tldextract
requests
opencv-python
scikit-image
undetected-chromedriver
selenium
```

---

## 🚀 Usage

### 1. Run with CLI script

```bash
python phishing_checker_cli.py <real_url> <suspect_url>
```

Example:

```bash
python phishing_checker_cli.py https://www.paypal.com/login https://paypal.secure-login-support.com
```

### 2. Output

* A **JSON report** will be saved in the current folder:

  ```
  result_2025-08-16_18-05-40.json
  ```

* Screenshots will be saved in a timestamped folder:

  ```
  screenshots/2025-08-16_18-05-40/
      ├── real.png        # Legitimate page
      ├── suspect.png     # Suspect page
      └── diff.png        # Highlighted visual differences
  ```

* Example JSON output:

```json
{
    "real_domain": "paypal.com",
    "suspect_domain": "secure-login-support.com",
    "domain_similarity": 0.61,
    "url_findings": [
        "Domain mismatch",
        "Lookalike domain"
    ],
    "text_similarity": 0.42,
    "visual_similarity": 0.75,
    "real_screenshot": "screenshots/2025-08-16_18-05-40/real.png",
    "suspect_screenshot": "screenshots/2025-08-16_18-05-40/suspect.png",
    "diff_image": "screenshots/2025-08-16_18-05-40/diff.png",
    "phishing_likely": true
}
```

---

## ⚙️ Files

* **`phishing_checker.py`** → main pipeline (logic + screenshot + comparison)
* **`phishing_checker_cli.py`** → command line wrapper for easy usage
* **`screenshots/`** → auto-generated timestamped screenshot folders
* **`result_*.json`** → JSON reports per run

---

## 🛠 Notes

* Runs in **headless mode** using `undetected-chromedriver` (Chrome required).
* Works on Linux / macOS / Windows.
* Needs internet connection to fetch pages.
* For heavy use, increase timeout in requests / Selenium.

---
