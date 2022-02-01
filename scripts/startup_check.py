import logging
import os
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

required_environment_variables = [
    '{prefix}{name}'.format(
        prefix='ITUSCHEDULER_',
        name=name,
    )
    for name in [
        # Docker
        'CONTAINER_KIND',
        # Django
        'STAGE',
        'SECRET_KEY',
        # PostgreSQL
        'POSTGRES_HOST',
        'POSTGRES_NAME',
        'POSTGRES_USER',
        'POSTGRES_PASSWORD',
        # Email
        'EMAIL_HOST',
        'EMAIL_HOST_USER',
        'EMAIL_HOST_PASSWORD',
        # Sentry
        'SENTRY_DSN',
        # AWS
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY',
        'AWS_DEFAULT_REGION',
        # Twitter
        'SOCIAL_AUTH_TWITTER_KEY',
        'SOCIAL_AUTH_TWITTER_SECRET',
        # Facebook
        'SOCIAL_AUTH_FACEBOOK_KEY',
        'SOCIAL_AUTH_FACEBOOK_SECRET',
    ]
]

missing_environment_variables = []

for required_environment_variable in required_environment_variables:
    if required_environment_variable not in os.environ:
        missing_environment_variables.append(required_environment_variable)

if len(missing_environment_variables) > 0:
    logging.error(
        "These environment variables are required but not set: {missing_environment_variables}".format(
            missing_environment_variables=', '.join(missing_environment_variables),
        )
    )

if len(missing_environment_variables) > 0:
    sys.exit(1)

logging.info("Startup check is complete.")
