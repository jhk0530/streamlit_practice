from distutils.command.build import build
import json
import requests
import streamlit as st
import pandas as pd

headers = {'Authorization': 'token ' + st.secrets['TOKEN']}

@st.cache(ttl = 3600*2) # if updated before 1 hour, not update again
def getStats(repo, org = 'statgarten', headers = headers):    
    # define base url
    url = 'https://api.github.com/repos/'+ org + '/' + repo
    # star
    s = requests.get(url, headers = headers).json()
    star = s['stargazers_count']

    # commits

    i = 1
    commits = 0
    while True:
        s = requests.get(url + '/commits?per_page=30&page=' + str(i), headers = headers).json()
        commits += len(s)
        i += 1
        if len(s) == 0: break

    # contributors
    s = requests.get(url + '/contributors', headers = headers).json()
    contributors = len(s)

    # all issue
    # s = requests.get(url + '/issues?state=all', headers = headers).json()
    
    # fix; 30 per page
    i = 1
    allissue = 0
    while True:
        s = requests.get(url + '/issues?state=all&page=' + str(i), headers = headers).json()
        allissue += len(s)
        i += 1
        if len(s) == 0: break

    # pull requests
    s = requests.get(url + '/pulls?state=closed', headers = headers).json()
    pr = len(s)
    allissue = allissue - pr

    # open issue

    # s = requests.get(url + '/issues?state=open', headers = headers).json()

    i = 1
    openissue = 0
    while True:
        s = requests.get(url + '/issues?state=open&page=' + str(i), headers = headers).json()
        openissue += len(s)
        i += 1
        if len(s) == 0: break    
    
    closeissue = allissue - openissue

    active = openissue +  (closeissue) * 2
    df = pd.DataFrame(
        data = [[repo, commits, contributors, star, active, openissue, closeissue]], 
        columns = ["Repo",'Commits', 'Contributors', 'Stars', 'Active Score', 'Opened Issue', 'Closed Issue']
    )
    return(df)

def get_contributors(owner, repo):
    github_api_url = "https://api.github.com"
    endpoint = f"{github_api_url}/repos/{owner}/{repo}/contributors"
    
    try:
        response = requests.get(endpoint)
        response.raise_for_status()  # HTTP 오류가 발생하면 예외를 발생시킵니다.
        contributors = response.json()
        logins = [contributor["login"] for contributor in contributors]  # 'login' 필드만 추출
        return logins
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve contributors' logins: {e}")
        return []

def find_contributors(v, owner, repo):
    data = get_contributors(owner, repo)
    logins = [item['login'] for item in data]

    v = v + logins
    return(v)

def buildMetrics(metrics, i):
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.metric(label = '🛠️ 커밋', value = int(metrics['Commits']), delta = int(metrics[0])-1000) # 커밋 1000

    with col2:
        # st.metric(label = '🧑‍🤝‍🧑 기여자', value = int(metrics['Contributors']), delta = int(metrics[1])-30) # 기여자 30
        st.metric(label = '🧑‍🤝‍🧑 기여자', value = i, delta = i-30) # 기여자 30

    with col3:
        st.metric(label = '⭐ 스타', value = int(metrics['Stars']), delta = int(metrics[2])-200) # 스타 200

    with col4:
        st.metric(label = '💯 커뮤니티 활성도', value = int(metrics['Active Score']), delta = int(metrics[3])-360) # 활성도 360 

    with col5:
        st.metric(label = '❗ 오픈 이슈', value = int(metrics['Opened Issue']))

    with col6:
        st.metric(label = '✅ 클로즈 이슈', value = int(metrics['Closed Issue']))

df = pd.concat([
    getStats('board', org = 'statgarten'),
    getStats('colorpen', org = 'statgarten'),
    getStats('datatoys', org = 'statgarten'),
    getStats('datatoys-python', org = 'statgarten'),
    getStats('datatoys-raw', org = 'statgarten'),
    getStats('dockerImage', org = 'statgarten'),
    getStats('door', org = 'statgarten'),
    # getStats('exRep', org = 'statgarten'),
    getStats('maps', org = 'statgarten'),
    getStats('playdoh', org = 'statgarten'),
    getStats('publicdata101', org = 'statgarten'),
    getStats('scissor', org = 'statgarten'),
    getStats('SGDS', org = 'statgarten'),
    getStats('sgthemes', org = 'statgarten'),
    getStats('soroban', org = 'statgarten'),
    getStats('statgarten', org = 'statgarten'),
    getStats('stove', org = 'statgarten'),
    getStats('jstable', org = 'jinseob2kim'),
    getStats('jskm', org = 'jinseob2kim'),
    getStats('jsmodule', org = 'jinseob2kim'),
    getStats('shiny.likert', org = 'zarathucorp')      
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
v = find_contributors(v, 'statgarten', 'board')
v = find_contributors(v, 'statgarten', 'colorpen')
v = find_contributors(v, 'statgarten', 'datatoys')
v = find_contributors(v, 'statgarten', 'datatoys-python')
v = find_contributors(v, 'statgarten', 'datatoys-raw')
v = find_contributors(v, 'statgarten', 'dockerImage')
v = find_contributors(v, 'statgarten', 'door')
v = find_contributors(v, 'statgarten', 'maps')
v = find_contributors(v, 'statgarten', 'playdoh')
v = find_contributors(v, 'statgarten', 'publicdata101')
v = find_contributors(v, 'statgarten', 'scissor')
v = find_contributors(v, 'statgarten', 'SGDS')
v = find_contributors(v, 'statgarten', 'sgthemes')
v = find_contributors(v, 'statgarten', 'soroban')
v = find_contributors(v, 'statgarten', 'statgarten')
v = find_contributors(v, 'statgarten', 'stove')
v = find_contributors(v, 'jinseob2kim', 'jstable')
v = find_contributors(v, 'jinseob2kim', 'jskm')
v = find_contributors(v, 'jinseob2kim', 'jsmodule')
v = find_contributors(v, 'zarathucorp', 'shiny.likert')

# unique
v = list(set(v))
v = [item for item in v if item != 'github-actions[bot]']

buildMetrics(Metrics, i = len(v))

st.markdown("### Metrics for each repo")
st.table(df)

