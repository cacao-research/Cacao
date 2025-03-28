import pytest
import time
from cacao.core.session import SessionManager

@pytest.fixture
def session_manager():
    return SessionManager(storage_type="memory")

def test_session_creation(session_manager):
    session_id = session_manager.create_session()
    assert session_id is not None
    session = session_manager.get_session(session_id)
    assert session["state"] == {}

def test_session_data_persistence(session_manager):
    session_id = session_manager.create_session()
    assert session_manager.update_session_state(session_id, {"user": "test_user"})
    
    loaded_session = session_manager.get_session(session_id)
    assert loaded_session["state"]["user"] == "test_user"

def test_session_deletion(session_manager):
    session_id = session_manager.create_session()
    assert session_manager.delete_session(session_id)
    assert session_manager.get_session(session_id) is None

def test_session_expiry_check():
    # Create a session manager with a very short expiry time
    manager = SessionManager(storage_type="memory", session_expiry=0.1)
    session_id = manager.create_session()
    
    # Make sure the session exists initially
    assert manager.get_session(session_id) is not None
    
    # Wait for the session to expire
    time.sleep(0.2)
    
    # Now cleanup should work
    removed = manager.cleanup_expired_sessions()
    assert removed > 0