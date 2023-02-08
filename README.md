# Cloud Computing : Term Paper

Code implementation on research paper - [Unified Cloud Access Control Model for Cloud Storage Broker](https://ieeexplore.ieee.org/document/8717982)

<br/><br/>
<br/><br/>

## Run App

```sh
# create and activate venv
python3 -m venv env
source env/bin/activate

# install packages
pip3 install -r requirements.txt

# run app
cd app
uvicorn main:app --reload --host 0.0.0.0

```

open docs on [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
