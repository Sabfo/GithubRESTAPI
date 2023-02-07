from flask import Blueprint, jsonify, request
import requests
import json
from datetime import timedelta, datetime as dt, timezone as tz
import os

repo = Blueprint('blueprint', __name__, url_prefix='/api/repos')
API_URL = 'https://api.github.com/repos'
TOKEN = os.getenv('TOKEN_GITHUB_RESTAPI', 'anything')
headers_default = {'Authorization': f'{TOKEN}', 'X-GitHub-Api-Version': '2022-11-28'}


def template_request(owner: str, repo_name: str, path_param='', params=None, headers_=None) -> requests.Response:
    if params is None:
        params = {}
    headers = headers_default
    if headers_ is not None:
        for k, v in headers_.items():
            headers[k] = v

    response = requests.get(f'{API_URL}/{owner}/{repo_name}{path_param}', params=params, headers=headers)
    return response


@repo.route('/<owner>/<repo_name>', methods=['GET'])
def get_repo(owner: str, repo_name: str):
    """Get repo details."""
    response = template_request(owner, repo_name)
    return json.loads(response.content)


@repo.route('/<owner>/<repo_name>/issues', methods=['GET'])
def get_repo_issues(owner: str, repo_name: str):
    """Get a list of all pull issues."""
    response = template_request(owner, repo_name, path_param='/issues', params=request.args.to_dict())
    return json.loads(response.content)


@repo.route('/<owner>/<repo_name>/forks', methods=['GET'])
def get_repo_forks(owner: str, repo_name: str):
    """Get a list of all pull forks."""
    response = template_request(owner, repo_name, path_param='/forks', params=request.args.to_dict())
    return json.loads(response.content)


@repo.route('/<owner>/<repo_name>/pulls', methods=['GET'])
def get_repo_pulls(owner: str, repo_name: str):
    """Get a list of all pull requests."""
    response = template_request(owner, repo_name, path_param='/pulls', params=request.args.to_dict())
    return json.loads(response.content)


def str2datetime_utc(datetime_str: str) -> dt:
    return dt.fromisoformat(datetime_str[:-1] + '+00:00')


def is_not_merged_and_open_at_least_2weeks(pull_body: dict) -> bool:
    return pull_body['merged_at'] is None and \
           str2datetime_utc(pull_body['created_at']) + timedelta(weeks=2) <= dt.now(tz=tz.utc)


@repo.route('/<owner>/<repo_name>/old_open_pulls', methods=['GET'])
def get_repo_old_open_pulls(owner: str, repo_name: str):
    """Get a list of all pull requests which have not been merged for two weeks or more."""
    per_page = 100
    counter = 0
    has_old_open_pulls = True
    old_open_pulls = []
    while has_old_open_pulls and counter < 10:
        response = template_request(owner, repo_name, path_param='/pulls',
                                    params={'state': 'open', 'per_page': per_page})
        response_json = json.loads(response.content)
        if response.status_code not in (200, 304):
            return response_json
        if len(response_json) < per_page:
            has_old_open_pulls = False

        old_open_pulls.extend(filter(is_not_merged_and_open_at_least_2weeks, response_json))
        counter += 1
    return old_open_pulls
