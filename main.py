from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, HttpUrl, ValidationError
from typing import Optional

from build import generate_pdf


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


class FormData(BaseModel):
    author: str
    topic: str
    image_url: Optional[HttpUrl]
    facts: str
    trust: str
    missing: str
    interpretations: str
    difficult: str
    assumptions: str
    emotions: str
    experiences: str
    yourself: str
    others: str
    positive: str
    negative: str
    summary: str


@app.post("/submit")
async def submit_form(
    author: str = Form(...),
    topic: str = Form(...),
    image_url: str = Form(
        # default="https://raw.githubusercontent.com/MalloryWittwer/opinion-development-notebook/refs/heads/main/assets/self_reflection.png"
        default=None
    ),
    facts: str = Form(default=""),
    trust: str = Form(default=""),
    missing: str = Form(default=""),
    interpretations: str = Form(default=""),
    difficult: str = Form(default=""),
    assumptions: str = Form(default=""),
    emotions: str = Form(default=""),
    experiences: str = Form(default=""),
    yourself: str = Form(default=""),
    others: str = Form(default=""),
    positive: str = Form(default=""),
    negative: str = Form(default=""),
    summary: str = Form(default=""),
):
    if len(topic) > 100:
        raise HTTPException(
            status_code=400, detail="Topic must be no longer than 100 characters."
        )
    
    # Ensure image_url is None if empty
    image_url = image_url if image_url else None

    try:
        form_data = FormData(
            author=author,
            topic=topic,
            image_url=image_url,
            facts=facts,
            trust=trust,
            missing=missing,
            interpretations=interpretations,
            difficult=difficult,
            assumptions=assumptions,
            emotions=emotions,
            experiences=experiences,
            yourself=yourself,
            others=others,
            positive=positive,
            negative=negative,
            summary=summary,
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Invalid Image URL format.")

    pdf_bytes = generate_pdf(
        form_data.topic,
        form_data.author,
        form_data.image_url,
        form_data.facts,
        form_data.trust,
        form_data.missing,
        form_data.interpretations,
        form_data.difficult,
        form_data.assumptions,
        form_data.emotions,
        form_data.experiences,
        form_data.yourself,
        form_data.others,
        form_data.positive,
        form_data.negative,
        form_data.summary,
        target="bytes",
    )

    return StreamingResponse(
        pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={form_data.topic.lower().replace(' ', '-')}_notebook.pdf"
        },
    )


@app.post("/edit", response_class=HTMLResponse)
async def edit_notebook(
    request: Request,
    author: str = Form(...),
    topic: str = Form(...),
    image_url: str = Form(
        default=None,
        # default="https://raw.githubusercontent.com/MalloryWittwer/opinion-development-notebook/refs/heads/main/assets/self_reflection.png"
    ),
):
    return templates.TemplateResponse(
        "edit.html",
        {
            "request": request,
            "author": author,
            "topic": topic,
            "image_url": image_url,
        },
    )
