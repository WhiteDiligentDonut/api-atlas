import uuid
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import crud
from .database import Base, engine, get_db
from .schemas import APICreate, APIResponse


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Atlas",
    description="A simple API documentation catalog.",
    version="1.0.0",
)

templates = Jinja2Templates(
    directory=str(Path(__file__).parent / "templates")
)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/apis", response_model=APIResponse)
def create_api(
    api_data: APICreate,
    db: Session = Depends(get_db),
):
    return crud.create_api(db, api_data)


@app.get("/api/apis", response_model=list[APIResponse])
def list_apis(
    search: str | None = None,
    db: Session = Depends(get_db),
):
    return crud.search_apis(db, search)


@app.get("/api/apis/{api_id}", response_model=APIResponse)
def get_api(
    api_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    api = crud.get_api(db, api_id)

    if api is None:
        raise HTTPException(
            status_code=404,
            detail="API not found",
        )

    return api


@app.delete("/api/apis/{api_id}")
def delete_api(
    api_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    deleted = crud.delete_api(db, api_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="API not found",
        )

    return {"message": "API deleted"}