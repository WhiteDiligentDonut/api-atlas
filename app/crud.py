from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import API
from .schemas import APICreate


def create_api(db: Session, api_data: APICreate) -> API:
    api = API(
        name=api_data.name,
        description=api_data.description,
        version=api_data.version,
        specification=api_data.specification,
    )

    db.add(api)
    db.commit()
    db.refresh(api)

    return api


def get_api(db: Session, api_id):
    return db.get(API, api_id)


def search_apis(db: Session, search: str | None = None):
    statement = select(API).order_by(API.created_at.desc())

    if search:
        search_pattern = f"%{search}%"

        statement = statement.where(
            API.name.ilike(search_pattern)
            | API.description.ilike(search_pattern)
        )

    return db.scalars(statement).all()


def delete_api(db: Session, api_id):
    api = db.get(API, api_id)

    if api is None:
        return False

    db.delete(api)
    db.commit()

    return True