from distutils.command.build import build
import json
import requests
import streamlit as st
import pandas as pd


headers = {'Authorization': 'token ' + st.secrets['TOKEN']}

@st.cache(ttl = 3600*12) 
def getStats(repo, headers = headers):    
    # define base url
    url = 'https://api.github.com/repos/statgarten/' + repo    
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
    s = requests.get(url + '/issues?state=all', headers = headers).json()
    allissue = len(s)

    # pull requests
    s = requests.get(url + '/pulls?state=closed', headers = headers).json()
    pr = len(s)
    allissue = allissue - pr

    # open issue
    s = requests.get(url + '/issues?state=open', headers = headers).json()
    openissue = len(s)

    closeissue = allissue - openissue

    active = openissue +  (closeissue) * 2
    df = pd.DataFrame(
        data = [[repo, commits, contributors, star, active, openissue, closeissue]], 
        columns = ["Repo",'Commits', 'Contributors', 'Stars', 'Active Score', 'Opened Issue', 'Closed Issue']
    )
    return(df)


def buildMetrics(metrics):         
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.metric(label = '🛠️ 커밋', value = int(metrics['Commits']), delta = int(metrics[0])-300)

    with col2:
        st.metric(label = '🧑‍🤝‍🧑 기여자', value = int(metrics['Contributors']), delta = int(metrics[1])-10)

    with col3:
        st.metric(label = '⭐ 스타', value = int(metrics['Stars']), delta = int(metrics[2])-50)

    with col4:
        st.metric(label = '💯 커뮤니티 활성도', value = int(metrics['Active Score']), delta = int(metrics[3])-120)

    with col5:
        st.metric(label = '❗ 오픈 이슈', value = int(metrics['Opened Issue']))

    with col6:
        st.metric(label = '✅ 클로즈 이슈', value = int(metrics['Closed Issue']))

df = pd.concat([
    getStats('door'), 
    getStats('datatoys'),
    getStats('dockerImage'),
#    getStats('goophi'), # changed repository name.
    getStats('stove'),
    getStats('exRep'),
    getStats('scissor'),
    getStats('plotGen'),
    getStats('board'),
    getStats('SGDS')
])

df = df.set_index('Repo')

Metrics = df.sum()
st.markdown("### Statgarten: Total Metrics")
buildMetrics(Metrics)

st.markdown("### Metrics for each repo")
st.table(df)
