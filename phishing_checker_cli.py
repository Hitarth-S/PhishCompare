import sys, json, datetime
from phishing_checker import check_phishing

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python phishing_checker_cli.py <real_url> <suspect_url>")
        sys.exit(1)

    real_url, suspect_url = sys.argv[1], sys.argv[2]
    result_json = check_phishing(real_url, suspect_url)

    print(result_json)

    # timestamped result file
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"result_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(result_json)

    print(f"\n JSON result saved as {filename}")
