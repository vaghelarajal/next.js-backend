import hashlib
from sqlalchemy.orm import Session
from models.user import UsedToken


def is_token_used(token: str, db: Session) -> bool:
    """Check if reset token has been used"""
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    return db.query(UsedToken).filter(
        UsedToken.token_hash == token_hash
    ).first() is not None


def mark_token_as_used(token: str, user_email: str, db: Session) -> None:
    """Mark reset token as used"""
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    used_token = UsedToken(token_hash=token_hash, user_email=user_email)
    db.add(used_token)
    db.commit()
