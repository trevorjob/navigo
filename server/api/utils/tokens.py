from sqlalchemy.orm import Session
from api.v1.models.black_list import BlacklistedToken


def blacklist_token(token: str, db: Session):
    """
    Add a token to the blacklist.
    """
    blacklisted_token = BlacklistedToken(token=token)
    db.add(blacklisted_token)
    db.commit()


def is_token_blacklisted(token: str, db: Session) -> bool:
    """
    Check if a token is blacklisted.
    """
    return db.query(BlacklistedToken).filter_by(token=token).first() is not None
