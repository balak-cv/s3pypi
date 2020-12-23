#!/usr/bin/env python
import argparse
import getpass
import json
import secrets
from dataclasses import asdict

import boto3

from handler import User, hash_password, region


def get_arg_parser():
    p = argparse.ArgumentParser()
    p.add_argument("domain")
    p.add_argument("username")
    p.add_argument("--salt-nbytes", type=int, default=32)
    p.add_argument("--overwrite", action="store_true")
    return p


def main():
    args = get_arg_parser().parse_args()

    password = getpass.getpass()
    salt = secrets.token_urlsafe(args.salt_nbytes)

    user = User(
        username=args.username,
        password_hash=hash_password(password, salt),
        password_salt=salt,
    )
    put_user(args.domain, user, args.overwrite)


def put_user(domain: str, user: User, overwrite: bool = False):
    data = asdict(user)
    username = data.pop("username")
    boto3.client("ssm", region_name=region).put_parameter(
        Name=f"/s3pypi/{domain}/users/{username}",
        Value=json.dumps(data, indent=2),
        Type="SecureString",
        Overwrite=overwrite,
    )


if __name__ == "__main__":
    main()
