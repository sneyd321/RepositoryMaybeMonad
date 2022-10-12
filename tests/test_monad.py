from monad import RepositoryMaybeMonad
import pytest, sqlalchemy


async def raise_operational_error():
    raise sqlalchemy.exc.OperationalError(None, None, None)

async def raise_integrity_error():
    raise sqlalchemy.exc.IntegrityError(None, None, None)

async def void_function(value):
    data = 1 + 1

async def no_param_void_function():
    data = 1 + 1

async def two_param_void_function(value1, value2):
    data = 1 + 1

async def return_function(value):
    return 1 + 1

async def no_param_return_function():
    return 1 + 1

async def two_param_return_function(value1, value2):
    return 1 + 1

@pytest.mark.asyncio
async def test_MaybeMonad_bind_returns_error_on_operational_error():
    monad = RepositoryMaybeMonad()
    monad = await monad.bind(raise_operational_error)
    assert monad.error_status == {"status": 502, "reason": "Failed to connect to database"}

@pytest.mark.asyncio
async def test_MaybeMonad_bind_data_returns_error_on_operational_error():
    monad = RepositoryMaybeMonad()
    monad = await monad.bind_data(raise_operational_error)
    assert monad.error_status == {"status": 502, "reason": "Failed to connect to database"}


@pytest.mark.asyncio
async def test_MaybeMonad_bind_returns_error_on_integrity_error():
    monad = RepositoryMaybeMonad()
    monad = await monad.bind(raise_integrity_error)
    assert monad.error_status == {"status": 409, "reason": "Failed to insert data into database"}


@pytest.mark.asyncio
async def test_MaybeMonad_bind_data_returns_error_on_integrity_error():
    monad = RepositoryMaybeMonad()
    monad = await monad.bind_data(raise_integrity_error)
    assert monad.error_status == {"status": 409, "reason": "Failed to insert data into database"}

@pytest.mark.asyncio
async def test_MaybeMonad_bind_returns_error_on_None_with_empty_error():
    monad = RepositoryMaybeMonad(None)
    monad = await monad.bind(void_function)
    assert monad.error_status == {"status": 404, "reason": "No data in repository monad"}


@pytest.mark.asyncio
async def test_MaybeMonad_bind_data_returns_error_on_None_with_empty_error():
    monad = RepositoryMaybeMonad(None)
    monad = await monad.bind_data(return_function)
    assert monad.error_status == {"status": 404, "reason": "No data in repository monad"}

@pytest.mark.asyncio
async def test_MaybeMonad_bind_returns_error_on_None_with_existing_error():
    monad = RepositoryMaybeMonad(None, error_status={"status": 100, "reason": "data"})
    monad = await monad.bind(void_function)
    assert monad.error_status == {"status": 100, "reason": "data"}

@pytest.mark.asyncio
async def test_MaybeMonad_bind_data_returns_error_on_None_with_existing_error():
    monad = RepositoryMaybeMonad(None, error_status={"status": 100, "reason": "data"})
    monad = await monad.bind(return_function)
    assert monad.error_status == {"status": 100, "reason": "data"}

@pytest.mark.asyncio
async def test_MaybeMonad_bind_returns_successfully_with_no_parameters():
    monad = RepositoryMaybeMonad()
    monad = await monad.bind(no_param_void_function)
    assert monad.error_status == None

@pytest.mark.asyncio
async def test_MaybeMonad_bind_returns_successfully_with_two_parameters():
    monad = RepositoryMaybeMonad("dsad", "Sdasd")
    monad = await monad.bind(two_param_void_function)
    assert monad.error_status == None


@pytest.mark.asyncio
async def test_MaybeMonad_bind_data_returns_successfully_with_no_parameters():
    monad = RepositoryMaybeMonad()
    monad = await monad.bind(no_param_return_function)
    assert monad.error_status == None

@pytest.mark.asyncio
async def test_MaybeMonad_bind_data_returns_successfully_with_two_parameters():
    monad = RepositoryMaybeMonad(123, 321)
    monad = await monad.bind(two_param_return_function)
    assert monad.error_status == None