Skip to content
mustafalperkan
ozetlehaber-bot
Repository navigation
Code
Issues
Pull requests
Actions
Projects
Wiki
Security
Insights
Settings
Haber Botu Calistir
Haber Botu Calistir #17
All jobs
Run details
build
succeeded now in 18s
Search logs
1s
Current runner version: '2.331.0'
Runner Image Provisioner
Operating System
Runner Image
GITHUB_TOKEN Permissions
Secret source: Actions
Prepare workflow directory
Prepare all required actions
Getting action download info
Download action repository 'actions/checkout@v3' (SHA:f43a0e5ff2bd294095638e18286ca9a3d1956744)
Download action repository 'actions/setup-python@v4' (SHA:7f4fc3e22c37d6ff65e88745f38bd3157c663f7c)
Complete job name: build
1s
Run actions/checkout@v3
Syncing repository: mustafalperkan/ozetlehaber-bot
Getting Git version info
Temporarily overriding HOME='/home/runner/work/_temp/73ed2133-245b-4fbe-a296-34a8bb27f96f' before making global git config changes
Adding repository directory to the temporary git global config as a safe directory
/usr/bin/git config --global --add safe.directory /home/runner/work/ozetlehaber-bot/ozetlehaber-bot
Deleting the contents of '/home/runner/work/ozetlehaber-bot/ozetlehaber-bot'
Initializing the repository
Disabling automatic garbage collection
Setting up auth
Fetching the repository
Determining the checkout info
Checking out the ref
/usr/bin/git log -1 --format='%H'
'a2e75b33658d2e04e415ea2a3a415af9e550f092'
0s
Run actions/setup-python@v4
Installed versions
11s
Run pip install google-generativeai google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client feedparser
Collecting google-generativeai
  Downloading google_generativeai-0.8.6-py3-none-any.whl.metadata (3.9 kB)
Collecting google-auth
  Downloading google_auth-2.48.0-py3-none-any.whl.metadata (6.2 kB)
Collecting google-auth-oauthlib
  Downloading google_auth_oauthlib-1.2.4-py3-none-any.whl.metadata (3.1 kB)
Collecting google-auth-httplib2
  Downloading google_auth_httplib2-0.3.0-py3-none-any.whl.metadata (3.1 kB)
Collecting google-api-python-client
  Downloading google_api_python_client-2.190.0-py3-none-any.whl.metadata (7.0 kB)
Collecting feedparser
  Downloading feedparser-6.0.12-py3-none-any.whl.metadata (2.7 kB)
Collecting google-ai-generativelanguage==0.6.15 (from google-generativeai)
  Downloading google_ai_generativelanguage-0.6.15-py3-none-any.whl.metadata (5.7 kB)
Collecting google-api-core (from google-generativeai)
  Downloading google_api_core-2.29.0-py3-none-any.whl.metadata (3.3 kB)
Collecting protobuf (from google-generativeai)
  Downloading protobuf-6.33.5-cp39-abi3-manylinux2014_x86_64.whl.metadata (593 bytes)
Collecting pydantic (from google-generativeai)
  Downloading pydantic-2.12.5-py3-none-any.whl.metadata (90 kB)
Collecting tqdm (from google-generativeai)
  Downloading tqdm-4.67.3-py3-none-any.whl.metadata (57 kB)
Collecting typing-extensions (from google-generativeai)
  Downloading typing_extensions-4.15.0-py3-none-any.whl.metadata (3.3 kB)
Collecting google-auth
  Downloading google_auth-2.49.0.dev0-py3-none-any.whl.metadata (6.0 kB)
Collecting proto-plus<2.0.0dev,>=1.22.3 (from google-ai-generativelanguage==0.6.15->google-generativeai)
  Downloading proto_plus-1.27.1-py3-none-any.whl.metadata (2.2 kB)
Collecting protobuf (from google-generativeai)
  Downloading protobuf-5.29.6-cp38-abi3-manylinux2014_x86_64.whl.metadata (592 bytes)
Collecting pyasn1-modules>=0.2.1 (from google-auth)
  Downloading pyasn1_modules-0.4.2-py3-none-any.whl.metadata (3.5 kB)
Collecting cryptography>=38.0.3 (from google-auth)
  Downloading cryptography-46.0.5-cp311-abi3-manylinux_2_34_x86_64.whl.metadata (5.7 kB)
Collecting googleapis-common-protos<2.0.0,>=1.56.2 (from google-api-core->google-generativeai)
  Downloading googleapis_common_protos-1.72.0-py3-none-any.whl.metadata (9.4 kB)
Collecting requests<3.0.0,>=2.18.0 (from google-api-core->google-generativeai)
  Downloading requests-2.32.5-py3-none-any.whl.metadata (4.9 kB)
Collecting grpcio<2.0.0,>=1.33.2 (from google-api-core[grpc]!=2.0.*,!=2.1.*,!=2.10.*,!=2.2.*,!=2.3.*,!=2.4.*,!=2.5.*,!=2.6.*,!=2.7.*,!=2.8.*,!=2.9.*,<3.0.0dev,>=1.34.1->google-ai-generativelanguage==0.6.15->google-generativeai)
  Downloading grpcio-1.78.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (3.8 kB)
Collecting grpcio-status<2.0.0,>=1.33.2 (from google-api-core[grpc]!=2.0.*,!=2.1.*,!=2.10.*,!=2.2.*,!=2.3.*,!=2.4.*,!=2.5.*,!=2.6.*,!=2.7.*,!=2.8.*,!=2.9.*,<3.0.0dev,>=1.34.1->google-ai-generativelanguage==0.6.15->google-generativeai)
  Downloading grpcio_status-1.78.0-py3-none-any.whl.metadata (1.3 kB)
INFO: pip is looking at multiple versions of grpcio-status to determine which version is compatible with other requirements. This could take a while.
  Downloading grpcio_status-1.76.0-py3-none-any.whl.metadata (1.1 kB)
  Downloading grpcio_status-1.75.1-py3-none-any.whl.metadata (1.1 kB)
  Downloading grpcio_status-1.75.0-py3-none-any.whl.metadata (1.1 kB)
  Downloading grpcio_status-1.74.0-py3-none-any.whl.metadata (1.1 kB)
  Downloading grpcio_status-1.73.1-py3-none-any.whl.metadata (1.1 kB)
  Downloading grpcio_status-1.73.0-py3-none-any.whl.metadata (1.1 kB)
  Downloading grpcio_status-1.72.2-py3-none-any.whl.metadata (1.1 kB)
INFO: pip is still looking at multiple versions of grpcio-status to determine which version is compatible with other requirements. This could take a while.
  Downloading grpcio_status-1.72.1-py3-none-any.whl.metadata (1.1 kB)
  Downloading grpcio_status-1.71.2-py3-none-any.whl.metadata (1.1 kB)
Collecting charset_normalizer<4,>=2 (from requests<3.0.0,>=2.18.0->google-api-core->google-generativeai)
  Downloading charset_normalizer-3.4.4-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (37 kB)
Collecting idna<4,>=2.5 (from requests<3.0.0,>=2.18.0->google-api-core->google-generativeai)
  Downloading idna-3.11-py3-none-any.whl.metadata (8.4 kB)
Collecting urllib3<3,>=1.21.1 (from requests<3.0.0,>=2.18.0->google-api-core->google-generativeai)
  Downloading urllib3-2.6.3-py3-none-any.whl.metadata (6.9 kB)
Collecting certifi>=2017.4.17 (from requests<3.0.0,>=2.18.0->google-api-core->google-generativeai)
  Downloading certifi-2026.1.4-py3-none-any.whl.metadata (2.5 kB)
Collecting requests-oauthlib>=0.7.0 (from google-auth-oauthlib)
  Downloading requests_oauthlib-2.0.0-py2.py3-none-any.whl.metadata (11 kB)
Collecting httplib2<1.0.0,>=0.19.0 (from google-auth-httplib2)
  Downloading httplib2-0.31.2-py3-none-any.whl.metadata (2.2 kB)
Collecting pyparsing<4,>=3.1 (from httplib2<1.0.0,>=0.19.0->google-auth-httplib2)
  Downloading pyparsing-3.3.2-py3-none-any.whl.metadata (5.8 kB)
Collecting uritemplate<5,>=3.0.1 (from google-api-python-client)
  Downloading uritemplate-4.2.0-py3-none-any.whl.metadata (2.6 kB)
Collecting sgmllib3k (from feedparser)
  Downloading sgmllib3k-1.0.0.tar.gz (5.8 kB)
  Installing build dependencies: started
  Installing build dependencies: finished with status 'done'
  Getting requirements to build wheel: started
  Getting requirements to build wheel: finished with status 'done'
  Preparing metadata (pyproject.toml): started
  Preparing metadata (pyproject.toml): finished with status 'done'
Collecting cffi>=2.0.0 (from cryptography>=38.0.3->google-auth)
  Downloading cffi-2.0.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (2.6 kB)
Collecting pycparser (from cffi>=2.0.0->cryptography>=38.0.3->google-auth)
  Downloading pycparser-3.0-py3-none-any.whl.metadata (8.2 kB)
Collecting pyasn1<0.7.0,>=0.6.1 (from pyasn1-modules>=0.2.1->google-auth)
  Downloading pyasn1-0.6.2-py3-none-any.whl.metadata (8.4 kB)
Collecting oauthlib>=3.0.0 (from requests-oauthlib>=0.7.0->google-auth-oauthlib)
  Downloading oauthlib-3.3.1-py3-none-any.whl.metadata (7.9 kB)
Collecting annotated-types>=0.6.0 (from pydantic->google-generativeai)
  Downloading annotated_types-0.7.0-py3-none-any.whl.metadata (15 kB)
Collecting pydantic-core==2.41.5 (from pydantic->google-generativeai)
  Downloading pydantic_core-2.41.5-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (7.3 kB)
Collecting typing-inspection>=0.4.2 (from pydantic->google-generativeai)
  Downloading typing_inspection-0.4.2-py3-none-any.whl.metadata (2.6 kB)
Downloading google_generativeai-0.8.6-py3-none-any.whl (155 kB)
Downloading google_ai_generativelanguage-0.6.15-py3-none-any.whl (1.3 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.3/1.3 MB 145.0 MB/s  0:00:00
Downloading google_auth-2.49.0.dev0-py3-none-any.whl (236 kB)
Downloading google_api_core-2.29.0-py3-none-any.whl (173 kB)
Downloading googleapis_common_protos-1.72.0-py3-none-any.whl (297 kB)
Downloading grpcio-1.78.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (6.7 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.7/6.7 MB 234.0 MB/s  0:00:00
Downloading grpcio_status-1.71.2-py3-none-any.whl (14 kB)
Downloading proto_plus-1.27.1-py3-none-any.whl (50 kB)
Downloading protobuf-5.29.6-cp38-abi3-manylinux2014_x86_64.whl (320 kB)
Downloading requests-2.32.5-py3-none-any.whl (64 kB)
Downloading charset_normalizer-3.4.4-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (151 kB)
Downloading idna-3.11-py3-none-any.whl (71 kB)
Downloading typing_extensions-4.15.0-py3-none-any.whl (44 kB)
Downloading urllib3-2.6.3-py3-none-any.whl (131 kB)
Downloading google_auth_oauthlib-1.2.4-py3-none-any.whl (19 kB)
Downloading google_auth_httplib2-0.3.0-py3-none-any.whl (9.5 kB)
Downloading httplib2-0.31.2-py3-none-any.whl (91 kB)
Downloading pyparsing-3.3.2-py3-none-any.whl (122 kB)
Downloading google_api_python_client-2.190.0-py3-none-any.whl (14.7 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 14.7/14.7 MB 240.6 MB/s  0:00:00
Downloading uritemplate-4.2.0-py3-none-any.whl (11 kB)
Downloading feedparser-6.0.12-py3-none-any.whl (81 kB)
Downloading certifi-2026.1.4-py3-none-any.whl (152 kB)
Downloading cryptography-46.0.5-cp311-abi3-manylinux_2_34_x86_64.whl (4.5 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.5/4.5 MB 210.0 MB/s  0:00:00
Downloading cffi-2.0.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (215 kB)
Downloading pyasn1_modules-0.4.2-py3-none-any.whl (181 kB)
Downloading pyasn1-0.6.2-py3-none-any.whl (83 kB)
Downloading requests_oauthlib-2.0.0-py2.py3-none-any.whl (24 kB)
Downloading oauthlib-3.3.1-py3-none-any.whl (160 kB)
Downloading pycparser-3.0-py3-none-any.whl (48 kB)
Downloading pydantic-2.12.5-py3-none-any.whl (463 kB)
Downloading pydantic_core-2.41.5-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 182.1 MB/s  0:00:00
Downloading annotated_types-0.7.0-py3-none-any.whl (13 kB)
Downloading typing_inspection-0.4.2-py3-none-any.whl (14 kB)
Downloading tqdm-4.67.3-py3-none-any.whl (78 kB)
Building wheels for collected packages: sgmllib3k
  Building wheel for sgmllib3k (pyproject.toml): started
  Building wheel for sgmllib3k (pyproject.toml): finished with status 'done'
  Created wheel for sgmllib3k: filename=sgmllib3k-1.0.0-py3-none-any.whl size=6091 sha256=8f10e7b1d7683bf4d7af4fbf07346dde0d1a488baa751dd5a0b4008a516fcde8
  Stored in directory: /home/runner/.cache/pip/wheels/3b/25/2a/105d6a15df6914f4d15047691c6c28f9052cc1173e40285d03
Successfully built sgmllib3k
Installing collected packages: sgmllib3k, urllib3, uritemplate, typing-extensions, tqdm, pyparsing, pycparser, pyasn1, protobuf, oauthlib, idna, feedparser, charset_normalizer, certifi, annotated-types, typing-inspection, requests, pydantic-core, pyasn1-modules, proto-plus, httplib2, grpcio, googleapis-common-protos, cffi, requests-oauthlib, pydantic, grpcio-status, cryptography, google-auth, google-auth-oauthlib, google-auth-httplib2, google-api-core, google-api-python-client, google-ai-generativelanguage, google-generativeai

Successfully installed annotated-types-0.7.0 certifi-2026.1.4 cffi-2.0.0 charset_normalizer-3.4.4 cryptography-46.0.5 feedparser-6.0.12 google-ai-generativelanguage-0.6.15 google-api-core-2.29.0 google-api-python-client-2.190.0 google-auth-2.49.0.dev0 google-auth-httplib2-0.3.0 google-auth-oauthlib-1.2.4 google-generativeai-0.8.6 googleapis-common-protos-1.72.0 grpcio-1.78.0 grpcio-status-1.71.2 httplib2-0.31.2 idna-3.11 oauthlib-3.3.1 proto-plus-1.27.1 protobuf-5.29.6 pyasn1-0.6.2 pyasn1-modules-0.4.2 pycparser-3.0 pydantic-2.12.5 pydantic-core-2.41.5 pyparsing-3.3.2 requests-2.32.5 requests-oauthlib-2.0.0 sgmllib3k-1.0.0 tqdm-4.67.3 typing-extensions-4.15.0 typing-inspection-0.4.2 uritemplate-4.2.0 urllib3-2.6.3
3s
Run python bot.py
/home/runner/work/ozetlehaber-bot/ozetlehaber-bot/bot.py:3: FutureWarning: 

All support for the `google.generativeai` package has ended. It will no longer be receiving 
updates or bug fixes. Please switch to the `google.genai` package as soon as possible.
See README for more details:

https://github.com/google-gemini/deprecated-generative-ai-python/blob/main/README.md

  import google.generativeai as genai
HATA OLUŞTU: 404 models/gemini-1.5-flash is not found for API version v1beta, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.
0s
Post job cleanup.
1s
Post job cleanup.
/usr/bin/git version
git version 2.52.0
Temporarily overriding HOME='/home/runner/work/_temp/0e48c653-fddf-423b-b0cd-561e77530122' before making global git config changes
Adding repository directory to the temporary git global config as a safe directory
/usr/bin/git config --global --add safe.directory /home/runner/work/ozetlehaber-bot/ozetlehaber-bot
/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
http.https://github.com/.extraheader
/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :"
0s
Cleaning up orphan processes
import os
import feedparser
import google.generativeai as genai
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# GitHub Secrets'tan verileri al
GEMINI_KEY = os.getenv('GEMINI_API_KEY')
BLOG_ID = os.getenv('BLOGGER_BLOG_ID')
CLIENT_ID = os.getenv('BLOGGER_CLIENT_ID')
CLIENT_SECRET = os.getenv('BLOGGER_CLIENT_SECRET')
REFRESH_TOKEN = os.getenv('BLOGGER_REFRESH_TOKEN')

# ANAHTAR KONTROLÜ (Hata buradaysa bizi uyaracak)
if not all([GEMINI_KEY, BLOG_ID, CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN]):
    print("HATA: GitHub Secrets eksik veya okunamıyor!")
    print(f"Client ID mevcut mu?: {bool(CLIENT_ID)}")
    exit(1)

# Gemini Yapılandırması
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

def get_blogger_service():
    creds = Credentials(
        token=None,
        refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )
    if not creds.valid:
        creds.refresh(Request())
    return build('blogger', 'v3', credentials=creds)

def summarize(title, link):
    prompt = f"Haber Başlığı: {title}. Link: {link}. Bu haberi 3 maddede özetle ve HTML formatında ver."
    response = model.generate_content(prompt)
    return response.text

try:
    feed = feedparser.parse("https://news.google.com/rss?hl=tr&gl=TR&ceid=TR:tr")
    service = get_blogger_service()
    item = feed.entries[0]
    summary_html = summarize(item.title, item.link)

    body = {
        "kind": "blogger#post",
        "title": item.title,
        "content": summary_html + f"<br><br><a href='{item.link}'>Kaynağa git</a>"
    }

    service.posts().insert(blogId=BLOG_ID, body=body).execute()
    print(f"BAŞARILI: {item.title} paylaşıldı!")
except Exception as e:
    print(f"HATA OLUŞTU: {e}")
