import os
import requests
from dotenv import load_dotenv

load_dotenv()

def export_jira_to_md():
    domain = os.getenv("JIRA_DOMAIN").replace("https://", "").replace("http://", "").strip("/")
    token = os.getenv("JIRA_BEARER_TOKEN")
    project = os.getenv("JIRA_PROJECT_KEY")
    version = os.getenv("JIRA_VERSION_NAME")

    # Change to v2 - Jira Data Center/Server standard
    url = f"https://{domain}/rest/api/2/search"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Atlassian-Token": "no-check" # Often helps bypass some proxy filters
    }
    
    params = {
        'jql': f'project = "{project}" AND fixVersion = "{version}"',
        'fields': 'summary,description',
        'maxResults': 50
    }

    print(f"Connecting to: {url}...")
    response = requests.get(url, headers=headers, params=params)

    # If you see <p> or <html> in this print, the token is still being rejected
    if "text/html" in response.headers.get("Content-Type", ""):
        print("CRITICAL: Still receiving HTML instead of JSON.")
        print("Your Bearer Token is likely invalid or the SSO is blocking it.")
        return

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return

    data = response.json()
    issues = data.get('issues', [])
    
    with open("./output/jira-content.txt", "w", encoding="utf-8") as f:
        f.write(f"# Release Notes: {version}\n\n")
        for issue in issues:
            key = issue['key']
            summary = issue['fields'].get('summary', 'N/A')
            # v2 uses plain text for description, much simpler than v3!
            description = issue['fields'].get('description', 'No description')
            
            f.write(f"### {key}: {summary}\n")
            f.write(f"{description}\n\n---\n\n")

    print(f"Done! Created notes for {len(issues)} issues.")

if __name__ == "__main__":
    export_jira_to_md()