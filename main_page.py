import json
import requests
import streamlit as st

secrets = st.secrets['TOKEN']

token = 'token ' + secrets
headers = {'Authorization': token}

s = requests.get('https://api.github.com/repos/statgarten/door', headers = headers).json()

star = s['stargazers_count']

i = 1
commits = 0
while True:
    url = 'https://api.github.com/repos/statgarten/door/commits?per_page=30&page=' + str(i)
    s = requests.get(url, headers = headers).json()
    commits += len(s)
    i += 1
    if len(s) == 0: break

s = requests.get('https://api.github.com/repos/statgarten/door/contributors', headers = headers).json()

contributors = len(s)

# all issue
s = requests.get('https://api.github.com/repos/statgarten/door/issues?state=all', headers = headers).json()
allissue = len(s)

# pull requests
s = requests.get('https://api.github.com/repos/statgarten/door/pulls?state=closed', headers = headers).json()
pr = len(s)
allissue = allissue - pr

# open issue
s = requests.get('https://api.github.com/repos/statgarten/door/issues?state=open', headers = headers).json()
openissue = len(s)

closeissue = allissue - openissue

active = openissue +  (closeissue) * 2




st.markdown("# Statgarten: door Metrics 🎈")
# st.sidebar.markdown("# Main page 🎈") # no need to sidebar
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric(label = '커밋', value = commits, delta = commits-300)

with col2:
    st.metric(label = '기여자', value = contributors, delta = contributors-10)

with col3:
    st.metric(label = '스타', value = star, delta = star-50)

with col4:
    st.metric(label = '커뮤니티 활성도', value = active, delta = active-120)

with col5:
    st.metric(label = '오픈 이슈', value = openissue)

with col6:
    st.metric(label = '클로즈 이슈', value = closeissue)
