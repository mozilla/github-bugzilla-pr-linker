import json

import requests


PAYLOAD = json.load(open("sample-push-payload.json"))


r = requests.post(
    "http://localhost:5000/postreceive",
    # "https://www.peterbe.com/postreceive",
    headers={
        "X-Hub-Signature": "sha1=0e2c18e2af623759cec3bbd31c2a791e8045ccdd",
        "X-GitHub-Event": "push",
        "content-type": "application/x-www-form-urlencoded",
    },
    # json=PAYLOAD,
    data={"payload": json.dumps(PAYLOAD)},
    # data={"payload": PAYLOAD},
)

print(r)
print(r.status_code)
print(repr(r.content))
