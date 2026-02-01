import pytest
from uuid import uuid4

from be_task_ca.adapters.repositories.user.in_memory_user_repository import InMemoryUserRepository
from be_task_ca.domain.entities.user import User


@pytest.fixture
def user_repository():
    return InMemoryUserRepository()


@pytest.fixture
def sample_user():
    return User(
        email="john@example.com",
        first_name="John",
        last_name="Doe",
        hashed_password="hashed_password_123",
        shipping_address="123 Main St, City, Country"
    )


@pytest.fixture
def another_user():
    return User(
        email="jane@example.com",
        first_name="Jane",
        last_name="Smith",
        hashed_password="hashed_password_456",
        shipping_address="456 Oak Ave, City, Country"
    )


@pytest.mark.asyncio
async def test_save_user(user_repository, sample_user):
    result = await user_repository.save(sample_user)

    assert result == sample_user
    assert result.id == sample_user.id
    assert result.email == "john@example.com"


@pytest.mark.asyncio
async def test_save_multiple_users(user_repository, sample_user, another_user):
    await user_repository.save(sample_user)
    await user_repository.save(another_user)

    assert len(user_repository.users) == 2


@pytest.mark.asyncio
async def test_find_by_email_exact_match(user_repository, sample_user):
    await user_repository.save(sample_user)

    found = await user_repository.find_by_email("john@example.com")

    assert found is not None
    assert found.email == "john@example.com"
    assert found.id == sample_user.id


@pytest.mark.asyncio
async def test_find_by_email_case_insensitive(user_repository, sample_user):
    await user_repository.save(sample_user)

    found = await user_repository.find_by_email("JOHN@EXAMPLE.COM")

    assert found is not None
    assert found.email == "john@example.com"


@pytest.mark.asyncio
async def test_find_by_email_not_found(user_repository):
    found = await user_repository.find_by_email("nonexistent@example.com")

    assert found is None


@pytest.mark.asyncio
async def test_find_by_email_returns_first_match(user_repository, sample_user, another_user):
    await user_repository.save(sample_user)
    await user_repository.save(another_user)

    found = await user_repository.find_by_email("john@example.com")

    assert found == sample_user


@pytest.mark.asyncio
async def test_find_by_id_exact_match(user_repository, sample_user):
    await user_repository.save(sample_user)

    found = await user_repository.find_by_id(sample_user.id)

    assert found is not None
    assert found.id == sample_user.id
    assert found.email == "john@example.com"


@pytest.mark.asyncio
async def test_find_by_id_not_found(user_repository):
    fake_id = uuid4()

    found = await user_repository.find_by_id(fake_id)

    assert found is None


@pytest.mark.asyncio
async def test_find_by_id_returns_correct_user(user_repository, sample_user, another_user):
    await user_repository.save(sample_user)
    await user_repository.save(another_user)

    found = await user_repository.find_by_id(another_user.id)

    assert found == another_user
    assert found.email == "jane@example.com"


@pytest.mark.asyncio
async def test_data_persistence_after_save(user_repository, sample_user):
    await user_repository.save(sample_user)

    assert len(user_repository.users) == 1
    assert user_repository.users[0] == sample_user


@pytest.mark.asyncio
async def test_saved_user_has_id(user_repository):
    user = User(
        email="test@example.com",
        first_name="Test",
        last_name="User",
        hashed_password="hashed",
        shipping_address="Address"
    )

    saved_user = await user_repository.save(user)

    assert saved_user.id is not None


@pytest.mark.asyncio
async def test_find_by_email_with_multiple_users_different_emails(user_repository):
    user1 = User(
        email="alice@example.com",
        first_name="Alice",
        last_name="A",
        hashed_password="hash1",
        shipping_address="Address 1"
    )
    user2 = User(
        email="bob@example.com",
        first_name="Bob",
        last_name="B",
        hashed_password="hash2",
        shipping_address="Address 2"
    )

    await user_repository.save(user1)
    await user_repository.save(user2)

    found_alice = await user_repository.find_by_email("alice@example.com")
    found_bob = await user_repository.find_by_email("bob@example.com")

    assert found_alice.email == "alice@example.com"
    assert found_bob.email == "bob@example.com"
    assert found_alice.id != found_bob.id
