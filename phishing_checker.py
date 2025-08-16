import os, re, difflib, cv2, requests, json, tldextract, undetected_chromedriver as uc, datetime
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from skimage.metrics import structural_similarity as ssim

# ---------- Utils ----------
def normalize_url(url):
    return url if url.startswith(("http://", "https://")) else "https://" + url

def extract_domain(url):
    ext = tldextract.extract(url)
    return f"{ext.domain}.{ext.suffix}"

def text_similarity(url1, url2, limit=50000):
    def fetch_text(url):
        try:
            r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(r.text, "html.parser")
            [t.decompose() for t in soup(["script","style","noscript"])]
            return " ".join(soup.stripped_strings)[:limit]
        except:
            return ""
    return difflib.SequenceMatcher(None, fetch_text(url1), fetch_text(url2)).ratio()

def screenshot(url, path):
    try:
        opts = uc.ChromeOptions()
        opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1366,768")
        driver = uc.Chrome(options=opts, headless=True)
        driver.get(url)
        driver.save_screenshot(path)
        driver.quit()
        return True
    except:
        return False

def visual_similarity(img1_path, img2_path, diff_path):
    img1, img2 = cv2.imread(img1_path), cv2.imread(img2_path)
    if img1 is None or img2 is None:
        return 0.0
    h, w = min(img1.shape[0], img2.shape[0]), min(img1.shape[1], img2.shape[1])
    img1, img2 = cv2.resize(img1,(w,h)), cv2.resize(img2,(w,h))
    g1, g2 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY), cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    score, diff = ssim(g1,g2,full=True)
    diff=(diff*255).astype("uint8")

    _,th=cv2.threshold(diff,200,255,cv2.THRESH_BINARY_INV)
    for c in cv2.findContours(th,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]:
        if cv2.contourArea(c)>100:
            x,y,w,h=cv2.boundingRect(c)
            cv2.rectangle(img2,(x,y),(x+w,y+h),(0,0,255),2)
    cv2.imwrite(diff_path,img2)
    return round(score,3)

# ---------- Main ----------
def check_phishing(real_url, suspect_url, threshold=0.7):
    real_url, suspect_url = normalize_url(real_url), normalize_url(suspect_url)
    real_dom, sus_dom = extract_domain(real_url), extract_domain(suspect_url)
    dom_sim = difflib.SequenceMatcher(None, real_dom, sus_dom).ratio()

    findings=[]
    if real_dom!=sus_dom: findings.append("Domain mismatch")
    if dom_sim>0.7 and real_dom!=sus_dom: findings.append("Lookalike domain")
    if real_dom in suspect_url and real_dom!=sus_dom: findings.append("Deceptive subdomain")
    if "xn--" in suspect_url: findings.append("Punycode detected")

    txt_sim = round(text_similarity(real_url,suspect_url),3)

    # Screenshots with timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder = f"screenshots/{timestamp}"
    os.makedirs(folder, exist_ok=True)
    real_img, sus_img, diff_img = f"{folder}/real.png", f"{folder}/suspect.png", f"{folder}/diff.png"
    ok1,ok2 = screenshot(real_url,real_img), screenshot(suspect_url,sus_img)
    vis_sim = visual_similarity(real_img,sus_img,diff_img) if ok1 and ok2 else 0.0

    phishing_flag = (
        "Domain mismatch" in findings and 
        (vis_sim > threshold or txt_sim > threshold)
    )

    return json.dumps({
        "real_domain": real_dom,
        "suspect_domain": sus_dom,
        "domain_similarity": round(dom_sim,3),
        "url_findings": findings or ["No major URL issues"],
        "text_similarity": txt_sim,
        "visual_similarity": vis_sim,
        "real_screenshot": real_img if ok1 else None,
        "suspect_screenshot": sus_img if ok2 else None,
        "diff_image": diff_img if ok1 and ok2 else None,
        "phishing_likely": phishing_flag
    }, indent=4)

# ---------- Example ----------
if __name__=="__main__":
    real="https://www.paypal.com/login"
    suspect="https://paypal.secure-login-support.com"
    print(check_phishing(real,suspect))
