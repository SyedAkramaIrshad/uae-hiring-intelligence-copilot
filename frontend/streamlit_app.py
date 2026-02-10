from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title='UAE Hiring Intelligence Copilot', layout='wide')
st.title('🇦🇪 UAE Hiring Intelligence Copilot')

backend_url = st.sidebar.text_input('Backend URL', value='http://localhost:8000')
shortlist_top_n = st.sidebar.slider('Shortlist Top N', min_value=1, max_value=10, value=3)

jd = st.file_uploader('Upload Job Description (TXT/PDF)', type=['txt', 'pdf'])
cvs = st.file_uploader('Upload Candidate CVs (TXT/PDF)', type=['txt', 'pdf'], accept_multiple_files=True)

if st.button('Analyze Candidates', type='primary'):
    if not jd or not cvs:
        st.error('Please upload 1 JD and at least 1 CV.')
    else:
        files = [('jd_file', (jd.name, jd.getvalue(), jd.type or 'application/octet-stream'))]
        for cv in cvs:
            files.append(('cv_files', (cv.name, cv.getvalue(), cv.type or 'application/octet-stream')))

        with st.spinner('Scoring candidates...'):
            resp = requests.post(
                f'{backend_url}/analyze',
                data={'shortlist_top_n': str(shortlist_top_n)},
                files=files,
                timeout=120,
            )

        if resp.status_code != 200:
            st.error(f'Backend error: {resp.status_code} {resp.text}')
        else:
            data = resp.json()
            st.success(f"Mode: {data['mode']}")

            for i, c in enumerate(data['ranked_candidates'], start=1):
                with st.expander(f"#{i} {c['candidate_name']} — {c['score']}"):
                    st.write('**Score breakdown**', c['score_breakdown'])
                    st.write('**Matched skills**', c['matched_skills'])
                    st.write('**Missing skills**', c['missing_skills'])
                    st.write('**Explanation**', c['explanation'])
                    st.write('**Interview questions**')
                    for q in c['interview_questions']:
                        st.write(f'- {q}')
