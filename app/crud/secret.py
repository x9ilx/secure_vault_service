from sqlalchemy.orm import Session
from app.models.secret import Secret
from app.schemas.secret import SecretCreate

def create_secret(db: Session, secret: SecretCreate, user_id: int):
    db_secret = Secret(**secret.dict(), creator_id=user_id)
    db.add(db_secret)
    db.commit()
    db.refresh(db_secret)
    return db_secret

def get_secret(db: Session, secret_id: str):
    return db.query(Secret).filter(Secret.id == secret_id).first()
