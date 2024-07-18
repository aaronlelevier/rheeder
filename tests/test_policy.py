#!/usr/bin/env python

"""Tests for `rheeder` package."""

import re

import pytest

import rheeder


### Fixtures ###

@pytest.fixture
def response_01():
    """
    Id: None
    Statement: list
    """
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "ListAndDescribe",
                "Effect": "Allow",
                "Action": [
                    "dynamodb:DescribeTimeToLive"
                ],
                "Resource": "*"
            },

        ]
    }


@pytest.fixture
def response_02():
    """
    Id: None
    Statement: item
    """
    return {
        "Version": "2012-10-17",
        "Statement":
            {
                "Sid": "ListAndDescribe",
                "Effect": "Allow",
                "Action": [
                    "dynamodb:DescribeTimeToLive"
                ],
                "Resource": "*"
            },
    }


@pytest.fixture
def response_03():
    """
    Sid: True
    """
    return {
        "Version": "2012-10-17",
        "Statement":
            {
                "Sid": "1",
                "Effect": "Allow",
                "Action": [
                    "dynamodb:DescribeTimeToLive"
                ],
                "Resource": "*"
            },
    }


@pytest.fixture
def response_04():
    """
    Version: alt
    """
    return {
        "Version": "2008-10-17",
        "Statement":
            {
                "Effect": "Allow",
                "Action": [
                    "dynamodb:DescribeTimeToLive"
                ],
                "Resource": "*"
            },
    }


@pytest.fixture
def response_05():
    """
    Version: None
    """
    return {
        "Statement":
            {
                "Effect": "Allow",
                "Action": [
                    "dynamodb:DescribeTimeToLive"
                ],
                "Resource": "*"
            },
    }


@pytest.fixture
def response_06():
    """
    Id: True
    """
    return {
        "Id": "1",
        "Statement":
            {
                "Effect": "Allow",
                "Action": [
                    "dynamodb:DescribeTimeToLive"
                ],
                "Resource": "*"
            },
    }


@pytest.fixture
def response_07():
    """
    Principal: True
    """
    return {
        "Id": "1",
        "Statement":
            {
                "Effect": "Allow",
                "Action": [
                    "dynamodb:DescribeTimeToLive"
                ],
                "Resource": "*",
                "Principal": {
                    "AWS": [
                        "arn:aws:iam::AWS-account-ID:user/user-name-1",
                    ]
                }
            },
    }


@pytest.fixture
def response_08():
    """
    Effect: Deny
    """
    return {
        "Version": "2008-10-17",
        "Statement":
            {
                "Effect": "Deny",
                "Action": [
                    "dynamodb:DescribeTimeToLive"
                ],
                "Resource": "*"
            },
    }


@pytest.fixture
def response_09():
    """
    Action: *
    """
    return {
        "Version": "2008-10-17",
        "Statement":
            {
                "Effect": "Deny",
                "Action": "*",
                "Resource": "*"
            },
    }


@pytest.fixture
def response_10():
    """
    NotAction: *
    """
    return {
        "Version": "2008-10-17",
        "Statement":
            {
                "Effect": "Deny",
                "NotAction": "*",
                "Resource": "*"
            },
    }


@pytest.fixture
def response_11():
    """
    Action: glob
    """
    return {
        "Version": "2008-10-17",
        "Statement":
            {
                "Effect": "Deny",
                "Action": [
                    "dynamodb:*"
                ],
                "Resource": "*"
            },
    }


@pytest.fixture
def response_12():
    """
    Action: partial glob
    """
    return {
        "Version": "2008-10-17",
        "Statement":
            {
                "Effect": "Deny",
                "Action": [
                    "dynamodb:Describe*"
                ],
                "Resource": "*"
            },
    }

### Tests ###

# <version_block> = "Version" : ("2008-10-17" | "2012-10-17")

def test_stmt_version_true(response_01):
    assert 'Version' in response_01
    assert response_01['Version'] == "2012-10-17"
    assert rheeder.Policy(**response_01)

def test_stmt_version_true_2(response_04):
    assert 'Version' in response_04
    assert response_04['Version'] == "2008-10-17"
    assert rheeder.Policy(**response_04)

def test_stmt_version_false(response_05):
    assert 'Version' not in response_05
    assert rheeder.Policy(**response_05)

# <id_block> = "Id" : <policy_id_string>

def test_stmt_id_true(response_06):
    assert 'Id' in response_06
    assert rheeder.Policy(**response_06)

def test_stmt_id_false(response_03):
    assert 'Id' not in response_03
    assert rheeder.Policy(**response_03)

# <statement_block> = "Statement" : [ <statement>, <statement>, ... ]

def test_stmt_list(response_01):
    assert isinstance(response_01['Statement'], list)
    assert rheeder.Policy(**response_01)

def test_stmt_single(response_02):
    assert isinstance(response_02['Statement'], dict)
    assert rheeder.Policy(**response_02)

# <statement> = {
#     <sid_block?>,
#     <principal_block?>,
#     <effect_block>,
#     <action_block>,
#     <resource_block>,
#     <condition_block?>
# }

#     <sid_block?>,

def test_stmt_sid_true(response_03):
    assert 'Sid' in response_03['Statement']
    assert rheeder.Policy(**response_03)

def test_stmt_sid_false(response_04):
    assert 'Sid' not in response_04['Statement']
    assert rheeder.Policy(**response_04)

#     <principal_block?>,

def test_stmt_principal_true(response_07):
    assert 'Principal' in response_07['Statement']
    assert rheeder.Policy(**response_07)

def test_stmt_principal_false(response_04):
    assert 'Principal' not in response_04['Statement']
    assert rheeder.Policy(**response_04)

#     <effect_block>,

def test_stmt_effect_allow(response_07):
    assert 'Allow' == response_07['Statement']['Effect']
    assert rheeder.Policy(**response_07)

def test_stmt_effect_deny(response_08):
    assert 'Deny' == response_08['Statement']['Effect']
    assert rheeder.Policy(**response_08)

# <statement> = {
#     <action_block>,

        # <action_block> = ("Action" | "NotAction") :
        #     ("*" | [<action_string>, <action_string>, ...])

def test_action_star(response_09):
    assert '*' == response_09['Statement']['Action']
    assert rheeder.Policy(**response_09)

def test_notaction_star(response_10):
    assert '*' == response_10['Statement']['NotAction']
    assert rheeder.Policy(**response_10)

#     ("*" | [<action_string>, <action_string>, ...])

def test_action_string_awsservice_name(response_08):
    assert re.match(r'[a-z]+:[^\*]+[A-Za-z]+[^\*]+', response_08['Statement']['Action'][0])
    assert "dynamodb:DescribeTimeToLive" in  response_08['Statement']['Action'][0]
    assert rheeder.Policy(**response_08)

def test_action_string_awsservice_glob(response_11):
    assert re.match(r'[a-z]+:[A-Za-z\*]+', response_11['Statement']['Action'][0])
    assert 'dynamodb:*' == response_11['Statement']['Action'][0]
    assert rheeder.Policy(**response_11)

def test_action_string_awsservice_partial_glob(response_12):
    assert re.match(r'[a-z]+:[A-Za-z\*]+', response_12['Statement']['Action'][0])
    assert 'dynamodb:Describe*' == response_12['Statement']['Action'][0]
    assert rheeder.Policy(**response_12)

def test_action_string_list_awsservice_name(response_08):
    assert isinstance(response_08['Statement']['Action'], list)
    assert rheeder.Policy(**response_08)

### XOR Tests ###
# Principal
# Action
# Resource

# TODO: tomorrow

