#!/usr/bin/env python3
import os
import sys

def main():
    print("Google Search Console Sitemap Submission Script")
    print("==============================================")
    
    print("\n[Notice] Google officially disabled the public anonymous ping endpoint (google.com/ping?sitemap=...) in late 2023.")
    print("Sitemaps must now be submitted either passively via robots.txt (which is already configured) or programmatically via the Google Search Console (GSC) API.")
    
    try:
        from googleapiclient.discovery import build
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        import pickle
    except ImportError:
        print("\n[Dependency Missing] To run this script, please install the Google API client:")
        print("  pip install google-api-python-client google-auth-oauthlib google-auth-httplib2")
        print("\nAlternatively, you can manually upload the sitemap.xml in the Google Search Console UI:")
        print("  https://search.google.com/search-console/sitemaps")
        sys.exit(1)

    creds_path = 'credentials.json'
    token_path = 'token.pickle'
    
    if not os.path.exists(creds_path) and not os.path.exists(token_path):
        print(f"\n[Configuration Required] To authenticate with the GSC API:")
        print("  1. Go to Google Cloud Console: https://console.cloud.google.com/")
        print("  2. Create a new project and enable the 'Google Search Console API'.")
        print("  3. Go to Credentials -> Create Credentials -> OAuth Client ID (Desktop Application).")
        print("  4. Download the client secrets JSON, rename it to 'credentials.json', and place it in this directory.")
        sys.exit(0)
        
    creds = None
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
            
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, ['https://www.googleapis.com/auth/webmasters'])
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
            
    try:
        service = build('webmasters', 'v3', credentials=creds)
        site_url = 'https://jimiejosh.github.io/'
        sitemap_url = 'https://jimiejosh.github.io/sitemap.xml'
        
        print(f"\nSubmitting sitemap '{sitemap_url}' for property '{site_url}'...")
        service.sitemaps().submit(siteUrl=site_url, feedpath=sitemap_url).execute()
        print("[Success] Sitemap submitted successfully to Google Search Console!")
    except Exception as e:
        print(f"\n[Error] Failed to submit sitemap: {e}")

if __name__ == '__main__':
    main()
