import re
import hmac
from pprint import pprint

import requests
from decouple import config
from flask import Flask, request, abort


DEBUG = config('DEBUG', False, cast=bool)
GITHUB_WEBHOOK_SECRET = config('GITHUB_WEBHOOK_SECRET', 'secret')
BUGZILLA_BASE_URL = config('BUGZILLA_BASE_URL', 'https://bugzilla.mozilla.org')

app = Flask(__name__)


class ConfigurationError(ValueError):
    """when there's something wrong with the current config values"""


@app.route('/postreceive', methods=['POST', 'GET'])
def postreceive():
    if request.method == 'GET':
        return "Yeah, it works but use POST\n"

    if GITHUB_WEBHOOK_SECRET == 'secret' and not DEBUG:
        raise ConfigurationError(
            'GITHUB_WEBHOOK_SECRET not set'
        )

    # Need do a SHA check on the payload
    header_signature = request.headers.get('X-Hub-Signature')
    if header_signature is None:
        abort(403)

    sha_name, signature = header_signature.split('=')
    if sha_name != 'sha1':
        abort(501)

    print('request.data:')
    print(type(request.get_data()))
    print(repr(request.get_data()))
    # print('request.body:')
    # print(type(request.body))
    # print(repr(request.body))

    # HMAC requires the key to be bytes, but data is string
    mac = hmac.new(
        GITHUB_WEBHOOK_SECRET.encode('utf-8'),
        msg=request.data,
        digestmod='sha1'
    )

    print("MAC", repr(mac.hexdigest()), 'SIGNATURE', repr(signature))
    if mac.hexdigest() != signature:
        abort(403)

    posted = request.form
    pprint(dict(posted))

    if (
        posted.get('pull_request') and  # sanity check the payload
        posted.get('action') == 'opened' and  # only *created* PRs
        posted.get('state') == 'open' and  # not sure this is needed
        find_bug_id(posted.get('title'))  # only bother if it can be found
    ):
        url = posted['_links']['html']['href']
        bug_id = find_bug_id(posted['title'])
        # can we find the bug at all?!
        bug_comments = find_bug_comments(bug_id)
        if bug_comments is None:
            # Oh no! Bug can't be found
            abort(400, f'Bug {bug_id!r} can not be found')

        print("BUG_COMMENTS")
        print(repr(bug_comments))

        # loop over the current comments to see if there's already on
        for comment in bug_comments:
            print("COMMENT:")
            pprint(comment)
            print('\n')

    return "OK"


def find_bug_comments(id):
    """Return true if the bug can be found"""
    # XXX should this use secure credentials??
    # bug_url = f'{BASE_URL}/rest/bug/{bug_id}/comment'
    # XXX Idea; it could
    bug_url = f'{BUGZILLA_BASE_URL}/rest/bug/{id}'
    response = requests.get(bug_url)
    if response.status_code == 200:
        return response.json()


def find_bug_id(text):
    """give a piece of text, that is presumed to be the pull request title,
    return the bug ID out of it, if found."""

    # XXX Is this right?
    # How does the bugcloser do it?
    regex = re.compile('bug (\d+)', re.I)
    for match in regex.findall(text):
        return match


@app.route('/')
def homepage():
    return "See README\n"


if __name__ == '__main__':
    app.run(debug=DEBUG, use_reloader=DEBUG)
