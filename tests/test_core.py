from api.models import db


def test_unknown_exception_handler(client, new_user):
    """
    Check unknown exception handling
    """
    # Create unknown exception by dropping all tables
    db.drop_all()

    response = client.post("/users", json=new_user, follow_redirects=True)
    assert response.status_code == 500
    assert (
        b"Unknown Error. Sorry, that error is on us, please contact support if this wasn't an accident"
        in response.data
    )
