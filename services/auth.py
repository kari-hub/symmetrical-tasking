from datetime import datetime, timedelta
from jose import jwt, JWTError
from core.security import settings
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models.users import User
from passlib.context import CryptContext
from db import get_db

# password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# oauth scheme for fastapi
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(db: Session, email: str, password: str):
    """
    authenticates created users in db

    Args:
        db (Session): current database session
        email (str): user email
        password (str): user password

    Returns:
        user(User): if sign in is successful
        None: if failed
    """
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(
        password, user.hashed_password
    ):  # use hashed_password from verify_password
        return None
    return user


def create_access_token(
    data: dict, expires_delta: timedelta | None = None
):  # expires delta should have a default of None, hence `= None`
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY_MINUTES)
    )
    to_encode.update(
        {
            "exp": expire,
            "sub": data.get("email"),  # gets email from data dict.
        }
    )
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )  # algorithm takes exact algo for signing in jwt.encode
    return encoded_jwt


# def verify_token(token: str):
#     try:
#         payload = jwt.decode(
#             token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
#         )
#         return payload
#     except JWTError as e:
#         if "expired" in str(e):
#             raise HTTPException(status_code=401, detail="Token expired")
#         raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )  # algorithms used in jwt.decode takes list args  for allowed algorithms
        email: str = payload.get("sub")  # using email/username for user signin
        if email is None:
            raise credentials_exception
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception
