import pytest
from unittest.mock import AsyncMock

from app.services.sessions_service import SessionService


@pytest.mark.asyncio
async def test_get_all_sessions_service():
    # GIVEN - mock du repository
    mock_repo = AsyncMock()
    mock_repo.get_all.return_value = [
        {"id": 1, "name": "Session A"},
        {"id": 2, "name": "Session B"}
    ]

    # Service
    service = SessionService(mock_repo)

    # WHEN
    result = await service.get_all_sessions()

    # THEN
    assert len(result) == 2
    assert result[0]["name"] == "Session A"
    mock_repo.get_all.assert_called_once()