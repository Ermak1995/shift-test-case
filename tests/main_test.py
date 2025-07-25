import sys

from src.schemas import UserSchema

sys.path.insert(0, '../src')

import pytest

from httpx import AsyncClient, ASGITransport

from src.main import app, authenticate_user


@pytest.mark.asyncio
async def test_authenticate_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.post('/login', json={
            'username': 'John',
            'password': '1234'
        })
    assert response.status_code == 200
    assert 'token' in response.json()
    assert response.json()['token_type'] == 'Bearer'


@pytest.mark.asyncio
async def test_fail_authenticate_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        res_wrong_data = await ac.post('/login', json={
            'username': 'Tom',
            'password': '1234'
        })
        res_wrongpass = await ac.post('/login', json={
            'username': 'John',
            'password': 'qwerty'
        })

    assert res_wrong_data.status_code == 401
    assert 'token' not in res_wrong_data.json()
    assert res_wrong_data.json()['detail'] == 'Не удалось войти'

    assert res_wrongpass.status_code == 401
    assert 'token' not in res_wrongpass.json()
    assert res_wrongpass.json()['detail'] == 'Неверный пароль'


@pytest.mark.asyncio
async def test_salary_info():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        res_login = await ac.post('/login', json={
            'username': 'Alice',
            'password': 'qwerty'
        })
        token = res_login.json()['token']

        res_salary = await ac.get('/salary_info', headers={'Authorization': f'Bearer {token}'})

    assert res_salary.status_code == 200
    data = res_salary.json()
    assert data['username'] == 'Alice'
    assert data['salary'] == 63500
    assert data['next_raise_date'] == '2026-01-25'
