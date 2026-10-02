import pytest
from app.w365.client import w365
@pytest.mark.asyncio
async def test_fixture_tools():
    x=await w365.list_tools();assert "tools" in x["result"]
@pytest.mark.asyncio
async def test_fixture_screenshot():
    x=await w365.call("take_screenshot",{});assert "result" in x
