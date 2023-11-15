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

def get_stats(repo, org='statgarten', headers=headers, per_page=30, max_pages=10):
    # define base url
    url = f'https://api.github.com/repos/{org}/{repo}'

    # star
    star = requests.get(url, headers=headers).json()['stargazers_count']

    # commits
    commits = sum(len(requests.get(f'{url}/commits?per_page={per_page}&page={i}', headers=headers).json()) for i in range(1, max_pages + 1))

    # contributors
    contributors = len(requests.get(f'{url}/contributors', headers=headers).json())

    # all issue
    all_issues = sum(len(requests.get(f'{url}/issues?state=all&page={i}', headers=headers).json()) for i in range(1, max_pages + 1))

    # pull requests
    pr = int(len(requests.get(f'{url}/pulls?state=all', headers=headers).json()))

    # open issue
    open_issue = sum(len(requests.get(f'{url}/issues?state=open&page={i}', headers=headers).json()) for i in range(1, max_pages + 1))

    close_issue = all_issues - open_issue

    # release
    releases = int(len(requests.get(f'{url}/releases', headers=headers).json()))

    # Forks
    forks = int(len(requests.get(f'{url}/forks', headers=headers).json()))

    active = open_issue + close_issue * 2

    return pd.DataFrame(
        data=[[repo, commits, contributors, star, active, open_issue, close_issue, pr, releases, forks]],
        columns=["Repo", 'Commits', 'Contributors', 'Stars', 'Active Score', 'Opened Issue', 'Closed Issue', 'Pull Requests', 'Releases', 'Forks']
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
    get_stats('board', org = 'statgarten'),
    get_stats('colorpen', org = 'statgarten'),
    get_stats('datatoys', org = 'statgarten'),
    get_stats('datatoys-python', org = 'statgarten'),
    get_stats('datatoys-raw', org = 'statgarten'),
    get_stats('dockerImage', org = 'statgarten'),
    get_stats('door', org = 'statgarten'),
    # getStats('exRep', org = 'statgarten'),
    get_stats('maps', org = 'statgarten'),
    get_stats('playdoh', org = 'statgarten'),
    get_stats('publicdata101', org = 'statgarten'),
    get_stats('scissor', org = 'statgarten'),
    get_stats('SGDS', org = 'statgarten'),
    get_stats('sgthemes', org = 'statgarten'),
    get_stats('soroban', org = 'statgarten'),
    get_stats('statgarten', org = 'statgarten'),
    get_stats('stove', org = 'statgarten'),
    get_stats('jstable', org = 'jinseob2kim'),
    get_stats('jskm', org = 'jinseob2kim'),
    get_stats('jsmodule', org = 'jinseob2kim'),
    get_stats('shiny.likert', org = 'zarathucorp')      
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
v = find_contributors(v, 'statgarten', 'board', headers = headers)
v = find_contributors(v, 'statgarten', 'colorpen', headers = headers)
v = find_contributors(v, 'statgarten', 'datatoys', headers = headers)
v = find_contributors(v, 'statgarten', 'datatoys-python', headers = headers)
v = find_contributors(v, 'statgarten', 'datatoys-raw', headers = headers)
v = find_contributors(v, 'statgarten', 'dockerImage', headers = headers)
v = find_contributors(v, 'statgarten', 'door', headers = headers)
v = find_contributors(v, 'statgarten', 'maps', headers = headers)
v = find_contributors(v, 'statgarten', 'playdoh', headers = headers)
v = find_contributors(v, 'statgarten', 'publicdata101', headers = headers)
v = find_contributors(v, 'statgarten', 'scissor', headers = headers)
v = find_contributors(v, 'statgarten', 'SGDS', headers = headers)
v = find_contributors(v, 'statgarten', 'sgthemes', headers = headers)
v = find_contributors(v, 'statgarten', 'soroban', headers = headers)
v = find_contributors(v, 'statgarten', 'statgarten', headers = headers)
v = find_contributors(v, 'statgarten', 'stove', headers = headers)
v = find_contributors(v, 'jinseob2kim', 'jstable', headers = headers)
v = find_contributors(v, 'jinseob2kim', 'jskm', headers = headers)
v = find_contributors(v, 'jinseob2kim', 'jsmodule', headers = headers)
v = find_contributors(v, 'zarathucorp', 'shiny.likert', headers = headers)

# unique
v = list(set(v))
v = [item for item in v if item != 'github-actions[bot]']

buildMetrics(Metrics, i = len(v))

st.markdown("### Metrics for each repo")
st.table(df)

