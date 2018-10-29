# wdrforyou-cms
CMS for the WDRforyou bot

## Django on AWS using Zappa
Our CMS is based on [Django](https://www.djangoproject.com/) and hosted on AWS Lambda using [Zappa](https://zappa.io).
It provides a REST-API for [wdrforyou-bot](https://github.com/wdr-data/wdrforyou-bot).


## Local development
We don't advise you to deploy to AWS for local development, as it is quite time consuming to set up.

Copy `.env.sample` to `.env` and make adjustments if necessary.

Enable pipenv shell:
```bash
$ pipenv shell
```

### Initial setup
```bash
$ app/manage.py migrate
$ app/manage.py createsuperuser
```

### Development
To run local development server:
```bash
$ app/manage.py runserver
```
For database migrations use:

```bash
$ app/manage.py makemigrations
$ app/manage.py migrate
```

Alternatively you can run commands without enabling pipenv shell, for example:
```bash
$ pipenv run app/manage.py runserver
```

## AWS Deployment
- Set up an S3 bucket for static files and an IAM user with access to that bucket
- Create Zappa deployment bucket and update the `s3_bucket` key in `zappa_settings.json`
- Follow [this guide](https://edgarroman.github.io/zappa-django-guide/walk_database/) to set up an SQL database (Postgres)
- Follow [this guide](https://aws.amazon.com/premiumsupport/knowledge-center/internet-access-lambda-function/) to give your Lambda functions general internet access
- Optional: Create an S3 endpoint in your VPC to specifically set up S3 connectivity for your Lambda functions
- Run `zappa deploy <stage>` for initial deployment and `zappa update <stage>` for updating

### Environment Configuration
You can use the `s3-env-config` npm package to configure the environment variables in an S3 bucket.

The following environment variables are required:

```json
{
    "DEBUG": "",  // Can be True or False
    "SECRET_KEY": "",  // If DEBUG=False
    "S3_BUCKET_NAME": "",  // S3 bucket for static files
    "AWS_ACCESS_KEY_ID": "",  // Credentials for the bucket
    "AWS_SECRET_ACCESS_KEY": "",
    "DB_NAME": "",
    "DB_USER": "",
    "DB_PASSWORD": "",
    "DB_HOST": "",
    "BOT_SERVICE_ENDPOINT": ""  // With trailing slash
}
```
