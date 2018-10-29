# wdrforyou-cms
CMS for the WDRforyou bot

## Django on AWS using Zappa
Our CMS is based on [Django](https://www.djangoproject.com/) and hosted on AWS Lambda using [Zappa](https://zappa.io).
It provides a REST-API for [wdrforyou-bot](https://github.com/wdr-data/wdrforyou-bot).


## Local development
We don't advise to deploy to AWS for local development, as it is quite time consuming to set up. Test locally using:

Enable pipenv shell:
```
$ pipenv shell
```

To run local development server:
```
$ app/manage.py runserver
```
For database migrations use:

```
$ app/manage.py makemigrations
$ app/manage.py migrate
```

Alternatively you can run commands without enabling pipenv shell, for example:
```$ pipenv run app/manage.py runserver```

## Deployment
TBD
