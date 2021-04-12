import pytest

from app import app as flask_app


@pytest.fixture
def app():
    # flask_app.config['LOGIN_DISABLED'] = True
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


test_case_for_login = [
    {
        'input_data': {
            'first_name': 'Steven',
            'last_name': 'Yu',
            'SID': '1155101234',
            'email': 'xuxiangcuhk@qq.com',
            'user_name': 'XiaoYU',
            'password': '1234',
            'confirmed_password': '1234'
        },
        'expected_outcome': 'successful'
    },
    {
        'input_data': {
            'first_name': 'Steven',
            'last_name': 'Yu',
            'SID': '1155101234',
            'email': 'xuxiangcuhk@qq.com',
            'user_name': 'XiaoYU',
            'password': '1234',
            'confirmed_password': '1234',
            'is_instructor': True
        },
        'expected_outcome': 'successful'
    },
    {
        'input_data': {
            'first_name': 'Steven',
            'last_name': 'Yu',
            'SID': '115510',
            'email': 'xuxiangcuhk@qq.com',
            'user_name': 'XiaoYU',
            'password': '1234',
            'confirmed_password': '1234'
        },
        'expected_outcome': 'SID requires 10 numbers'
    },
    {
        'input_data': {
            'first_name': 'Steven',
            'last_name': 'Yu',
            'SID': '1155101234',
            'email': 'xuxiangcuhk',
            'user_name': 'XiaoYU',
            'password': '1234',
            'confirmed_password': '1234'
        },
        'expected_outcome': 'The email address is not valid.'
    },
    {
        'input_data': {
            'first_name': 'Steven',
            'last_name': 'Yu',
            'SID': '1155101234',
            'email': 'xuxiangcuhk@qq.com',
            'user_name': 'XiaoYU^^',
            'password': '1234',
            'confirmed_password': '1234'
        },
        'expected_outcome': 'Usernames must have only letters, numbers, dots or underscores'
    },
    {
        'input_data': {
            'first_name': 'Steven',
            'last_name': 'Yu',
            'SID': '1155101234',
            'email': 'xuxiangcuhk@qq.com',
            'user_name': 'XiaoYU',
            'password': '1234',
            'confirmed_password': '12'
        },
        'expected_outcome': 'Passwords must match.'
    },
    {
        'input_data': {
            'first_name': 'Steven',
            'last_name': 'Yu',
            'SID': '1155101234',
            'email': '1155107785@link.cuhk.edu.hk',
            'user_name': 'XiaoYU',
            'password': '1234',
            'confirmed_password': '1234'
        },
        'expected_outcome': 'The email has already been registered.'
    },
]

test_case_for_add_class = [
    {
        'input_data': {
            'course_code': 'ESTR1003',
            'course_title': 'Java',
            'course_instructor': 'Prof. Michael R. Lyu',
            'course_token': 'question'
        },
        'expected_outcome': 'successful'
    },
    {
        'input_data': {
            'course_code': 'ESTR1003',
            'course_title': 'Java',
            'course_instructor': 'Prof. Michael R. Lyu',
            'course_token': 'software'
        },
        'expected_outcome': 'The token is occupied by others.'
    }
]

test_case_for_reg_class = [
    {
        'input_data': {
            'course_token': 'ESTR1002'
        },
        'expected_outcome': 'successful'
    },
    {
        'input_data': {
            'course_token': 'CSCI3100'
        },
        'expected_outcome': 'successful'
    },
    {
        'input_data': {
            'course_token': 'wabcdefg'
        },
        'expected_outcome': 'The token is not available!'
    }
]

test_case_for_add_question = [
    {
        'input_data': {
            'question_title': 'Demo Question',
            'question_content': 'What is the name of this course?',
            'suggested_answer': 'CSCI3100',
        },
        'expected_outcome': 'successful'
    },
    {
        'input_data': {
            'question_title': 'Demo Question',
            'question_content': 'What is the name of this course?',
            'suggested_answer': '',
        },
        'expected_outcome': 'successful'
    },
]

test_case_for_submit_answer = [
    {
        'input_data': {
            'question_id': 1,
            'answer': 'Demo Answer',
        },
        'expected_outcome': 'successful'
    },
    {
        'input_data': {
            'question_id': 100,
            'answer': 'Demo Answer',
        },
        'expected_outcome': 'unsuccessful'
    },
]


def test_email_check(app, client):
    res = client.get('/email_check')
    assert res.status_code == 200


def test_login(app, client):
    res = client.get('/login')
    assert res.status_code == 200


# def test_confirm(app, client):
#     token = '6ac7e9240dad2617ea655c529343ec3b'
#     url = '/confirm' + token
#     response = client.get(url)
#     assert response.status_code == 200
#
#
# def test_unconfirmed(app, client):
#     res = client.get('/unconfirmed')
#     assert res.status_code == 200
#
#
# def test_logout(app, client):
#     res = client.get('/logout')
#     assert res.status_code == 200
