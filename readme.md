###Тестовое задание для STL
Implement a proxy REST API for obtaining information about a certain GitHub repo.

Requirements:
1.  Get repo details.  `/repos/{owner}/{repo_name}`
2.  Get a list of all pull requests.  `/repos/{owner}/{repo_name}/pulls`
3.  Get a list of all pull requests which have not been merged for two weeks or more. `/repos/{owner}/{repo_name}/old_open_pulls`
4.  Get a list of all issues.  `/repos/{owner}/{repo_name}/issues`
5.  Get a list of all forks.  `/repos/{owner}/{repo_name}/forks`
---
Сделана MVP-версия. Стоит переработать метод `repo/get_repo_old_open_pulls` через paginate, но 
сходу не придумал, как быстро это реализовать, не храня состояние на сервере.
---
####Installation and Run
`pip install -r requirements.txt`  
`python3 app.py`  
В переменную окружения `TOKEN_GITHUB_RESTAPI` или файл .env можно добавить свой токен