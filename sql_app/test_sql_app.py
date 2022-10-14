import sys
import pytest
import sqlalchemy.exc

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append('..')
from main import app, get_db
from sql_app import models

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def test_db():
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_mercenary(test_db):
    client.post('/mercenaries/', json={
        'name': 'my_name1', 'role': 'Protector', 'rarity': 'Rare', 'minion_type': 'Tauren', 'faction': 'Horde'
    })
    client.post('/mercenaries/', json={
        'name': 'my_name2', 'role': 'Caster', 'rarity': 'Epic', 'minion_type': 'Human', 'faction': 'Alliance'
    })
    response = client.get('/mercenaries/')
    assert len(response.json()) == 2
    assert response.json() == [{'faction': 'Horde',
                                'id': 1,
                                'minion_type': 'Tauren',
                                'name': 'my_name1',
                                'rarity': 'Rare',
                                'role': 'Protector'},
                               {'faction': 'Alliance',
                                'id': 2,
                                'minion_type': 'Human',
                                'name': 'my_name2',
                                'rarity': 'Epic',
                                'role': 'Caster'}]


def test_create_duplicate_mercenary(test_db):
    client.post('/mercenaries/', json={
        'name': 'duplicated_name', 'role': 'Protector', 'rarity': 'Rare', 'minion_type': 'Tauren', 'faction': 'Horde'
    })
    response = client.get('/mercenaries/')
    assert len(response.json()) == 1
    assert response.json() == [{'name': 'duplicated_name', 'role': 'Protector', 'rarity': 'Rare', 'minion_type': 'Tauren', 'faction': 'Horde', 'id': 1}]

    with pytest.raises(sqlalchemy.exc.IntegrityError):
        client.post('/mercenaries/', json={
            'name': 'duplicated_name', 'role': 'Caster', 'rarity': 'Epic', 'minion_type': 'Human', 'faction': 'Alliance'
        })
    response = client.get('/mercenaries/')
    assert len(response.json()) == 1
    assert response.json() == [{'name': 'duplicated_name', 'role': 'Protector', 'rarity': 'Rare', 'minion_type': 'Tauren', 'faction': 'Horde', 'id': 1}]
