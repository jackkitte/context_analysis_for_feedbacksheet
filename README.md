# Development environment for Context analysis with Jumann++ and KNP

## Requirement
- Docker
- pipenv

## Usage
```
$ git clone git@github.com:jackkitte/context_analysis_for_feedbacksheet.git
$ docker pull jackkitte/python_for_jumanpp_knp
$ docker run -it --name pipenv_knp --network elastic_docker_default -v /Users/tamash/work/feedbacksheet:/home/tamash/work -p 3000:3000 jackkitte/python_for_jumanpp_knp
$ pipenv install
$ pipenv run python knp_test.py
```