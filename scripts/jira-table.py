import os
import requests
import re
from dotenv import load_dotenv

load_dotenv()

def export_jira_to_md():
    # Configuration
    domain = "jira.ictu-sd.nl"
    project = os.getenv("JIRA_PROJECT_KEY")
    version = os.getenv("JIRA_VERSION_NAME")
    token = os.getenv("JIRA_BEARER_TOKEN")

    # API v2 for Jira Data Center
    url = f"https://{domain}/rest/api/2/search"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Common custom field ID for Sprints. 
    # Adjust 'customfield_10020' if your instance uses a different ID.
    params = {
        'jql': f'project = "{project}" AND fixVersion = "{version}"',
        'fields': 'summary,customfield_10207', 
        'maxResults': 50
    }

    try:
        response = requests.get(url, headers=headers, params=params)

        if "text/html" in response.headers.get("Content-Type", ""):
            print("Error: Received HTML. The Bearer Token is being rejected by the SSO gateway.")
            return

        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            return

        data = response.json()
        issues = data.get('issues', [])

        with open("./output/jira-table.txt", "w", encoding="utf-8") as f:
            # Table Header
            f.write("| Jira issue | Beschrijving | Sprint\n")
            
            for issue in issues:
                key = issue['key']
                fields = issue.get('fields', {})
                
                # Get summary and remove leading/trailing whitespace
                raw_summary = fields.get('summary', 'Geen beschrijving')
                summary = raw_summary.strip()
                
                # Sprint extraction logic
                sprint_field = fields.get('customfield_10207')
                sprint_name = "-"
                
                if sprint_field and isinstance(sprint_field, list) and len(sprint_field) > 0:
                    # Sprints in Data Center are often returned as string objects
                    sprint_str = str(sprint_field[-1]) # Use the most recent sprint
                    match = re.search(r"name=([^,\]]+)", sprint_str)
                    if match:
                        sprint_name = match.group(1).strip('Sprint ')

                # Format the row
                jira_link = f"https://{domain}/browse/{key}[{key}]"
                f.write(f"| {jira_link} | {summary} | {sprint_name}\n")

        print(f"Finished. Processed {len(issues)} issues.")

    except Exception as e:
        print(f"Script error: {e}")

if __name__ == "__main__":
    export_jira_to_md()