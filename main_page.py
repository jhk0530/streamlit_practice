from distutils.command.build import build
import json
import requests
import streamlit as st
import pandas as pd

headers = {'Authorization': 'token ' + st.secrets['TOKEN']}

@st.cache_data(ttl = 3600*2) # if updated before 1 hour, not update again
def getStats(repo, org = 'statgarten', headers = headers):    
    # define base url
    url = 'https://api.github.com/repos/'+ org + '/' + repo
    
    s = requests.get(url, headers = headers).json()
    
    # star
    star = s['stargazers_count']

    # watchers
    watchers = s['subscribers_count']

    # commits
    i = 1
    commits = 0
    while True:
        s = requests.get(url + '/commits?per_page=100&page=' + str(i), headers = headers).json() # change to 100. 30 costs api over
        commits += len(s)
        i += 1
        if len(s) == 0: break

    # contributors
    s = requests.get(url + '/contributors', headers = headers).json()
    contributors = len(s)
    
    # issues
    i = 1
    allissue = 0
    while True:
        s = requests.get(url + '/issues?state=all&per_page=100&page=' + str(i), headers = headers).json()
        allissue += len(s)
        i += 1
        if len(s) == 0: break

    # pull requests - all
    i = 1
    allprs = 0    
    while True:
        s = requests.get(url + '/pulls?state=all&per_page=100&page=' + str(i), headers = headers).json()
        allprs += len(s)
        i += 1
        if len(s) == 0: break

    ## pull requests - open
    i = 1
    openprs = 0
    while True:
        s = requests.get(url + '/pulls?state=open&per_page=100&page=' + str(i), headers = headers).json()
        openprs += len(s)
        i +=1
        if len(s) == 0: break
    
    allissue = allissue - allprs

    # active score
    i = 1
    openissue = 0
    while True:
        s = requests.get(url + '/issues?state=open&page=' + str(i), headers = headers).json()
        openissue += len(s)
        i += 1
        if len(s) == 0: break    
    openissue = openissue - openprs
    
    closeissue = allissue - openissue

    active = openissue + (closeissue) * 2
            
    # release
    releases = int(len(requests.get(f'{url}/releases', headers=headers).json()))

    # Forks
    forks = int(len(requests.get(f'{url}/forks', headers=headers).json()))

    return pd.DataFrame(
        data=[[repo, commits, contributors, star, watchers, active, openissue, closeissue, allprs, releases, forks]],
        columns=["Repo", 'Commits', 'Contributors', 'Stars', 'Watchers', 'Active Score', 'Opened Issue', 'Closed Issue', 'Pull Requests', 'Releases', 'Forks']
    )

def get_contributors(owner, repo, headers):
    github_api_url = "https://api.github.com"
    endpoint = f"{github_api_url}/repos/{owner}/{repo}/contributors"
    
    try:
        response = requests.get(endpoint, headers = headers)
        response.raise_for_status()  # HTTP 오류가 발생하면 예외를 발생시킵니다.
        contributors = response.json()
        logins = [contributor["login"] for contributor in contributors]  # 'login' 필드만 추출
        return logins
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve contributors' logins: {e}")
        return []

def find_contributors(v, owner, repo, headers):
    data = get_contributors(owner, repo, headers)    
    v = v + data
    return(v)

def buildMetrics(metrics, i):
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.metric(label = '🛠️ 커밋', value = int(metrics['Commits']), delta = int(metrics['Commits']) - 1000) # 커밋 1000
        st.metric(label = '📢 릴리즈', value = int(metrics['Releases']))

    with col2:        
        st.metric(label = '🧑‍🤝‍🧑 기여자', value = i, delta = i - 30) # 기여자 30
        st.metric(label = '👀 와쳐', value = int(metrics['Watchers']))

    with col3:
        st.metric(label = '⭐ 스타', value = int(metrics['Stars']), delta = int(metrics['Stars']) - 200) # 스타 200

    with col4:
        st.metric(label = '💯 커뮤니티 활성도', value = int(metrics['Active Score']), delta = int(metrics['Active Score']) - 360) # 활성도 360 

    with col5:
        st.metric(label = '❗ 오픈 이슈', value = int(metrics['Opened Issue']))
        st.metric(label = '✅ 클로즈 이슈', value = int(metrics['Closed Issue']))
    with col6:
        st.metric(label = '➡️ 풀 리퀘스트', value = int(metrics['Pull Requests']))
        st.metric(label = '🍴 포크', value = int(metrics['Forks']))    

df = pd.concat([
    #getStats('board', org = 'statgarten'),
    #getStats('colorpen', org = 'statgarten'),
    #getStats('datatoys', org = 'statgarten'),
    #getStats('datatoys-python', org = 'statgarten'),
    #getStats('datatoys-raw', org = 'statgarten'),
    #getStats('dockerImage', org = 'statgarten'),
    #getStats('door', org = 'statgarten'),
    # getStats('exRep', org = 'statgarten'),
    #getStats('maps', org = 'statgarten'),
    getStats('playdoh', org = 'statgarten'),
    #getStats('publicdata101', org = 'statgarten'),
    #getStats('scissor', org = 'statgarten'),
    #getStats('SGDS', org = 'statgarten'),
    #getStats('sgthemes', org = 'statgarten'),
    #getStats('soroban', org = 'statgarten'),
    #getStats('statgarten', org = 'statgarten'),
    getStats('stove', org = 'statgarten'),
    #getStats('jstable', org = 'jinseob2kim'),
    #getStats('jskm', org = 'jinseob2kim'),
    #getStats('jsmodule', org = 'jinseob2kim'),
    #getStats('docker-rshiny', org = 'jinseob2kim'),
    #getStats('shiny.likert', org = 'zarathucorp')      
    # kindergarten
    # statgarten.github.io
    # dispatch_test
    # CLATest    
])

df = df.set_index('Repo')

Metrics = df.sum()
st.markdown("### Statgarten: Total Metrics")

# contributors 
v = []
#v = find_contributors(v, 'statgarten', 'board', headers = headers)
#v = find_contributors(v, 'statgarten', 'colorpen', headers = headers)
#v = find_contributors(v, 'statgarten', 'datatoys', headers = headers)
#v = find_contributors(v, 'statgarten', 'datatoys-python', headers = headers)
#v = find_contributors(v, 'statgarten', 'datatoys-raw', headers = headers)
#v = find_contributors(v, 'statgarten', 'dockerImage', headers = headers)
#v = find_contributors(v, 'statgarten', 'door', headers = headers)
#v = find_contributors(v, 'statgarten', 'maps', headers = headers)
v = find_contributors(v, 'statgarten', 'playdoh', headers = headers)
#v = find_contributors(v, 'statgarten', 'publicdata101', headers = headers)
#v = find_contributors(v, 'statgarten', 'scissor', headers = headers)
#v = find_contributors(v, 'statgarten', 'SGDS', headers = headers)
#v = find_contributors(v, 'statgarten', 'sgthemes', headers = headers)
#v = find_contributors(v, 'statgarten', 'soroban', headers = headers)
#v = find_contributors(v, 'statgarten', 'statgarten', headers = headers)
v = find_contributors(v, 'statgarten', 'stove', headers = headers)
#v = find_contributors(v, 'jinseob2kim', 'jstable', headers = headers)
#v = find_contributors(v, 'jinseob2kim', 'jskm', headers = headers)
#v = find_contributors(v, 'jinseob2kim', 'jsmodule', headers = headers)
#v = find_contributors(v, 'jinseob2kim', 'docker-rshiny', headers = headers)
# v = find_contributors(v, 'zarathucorp', 'shiny.likert', headers = headers)
### 

# unique
v = list(set(v))
v = [item for item in v if item != 'github-actions[bot]']

print(v)

buildMetrics(Metrics, i = len(v))

st.markdown("### Metrics for each repo")
st.table(df)

