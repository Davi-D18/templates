from httpx import ASGITransport, AsyncClient

from {{ cookiecutter.project_slug }}.app.main import app


async def test_protected_route_requires_authentication():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.put("/users/1", json={"username": "someone"})

    assert response.status_code == 401
