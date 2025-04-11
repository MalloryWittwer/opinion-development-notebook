from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, HttpUrl, ValidationError
from build import generate_pdf  # Import the generate_pdf function
from fastapi.responses import StreamingResponse

app = FastAPI()

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")


# Route to serve the form
@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


# Pydantic model for validation
class FormData(BaseModel):
    author: str
    topic: str
    image_url: HttpUrl


# Route to handle form submission
@app.post("/submit")
async def submit_form(
    author: str = Form(...), topic: str = Form(...), image_url: str = Form(...)
):
    if len(topic) > 100:
        raise HTTPException(
            status_code=400, detail="Topic must be no longer than 100 characters."
        )

    try:
        form_data = FormData(author=author, topic=topic, image_url=image_url)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Invalid Image URL format.")

    pdf_bytes = generate_pdf(form_data.topic, form_data.author, form_data.image_url, target="bytes")

    return StreamingResponse(
        pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={form_data.topic.lower().replace(' ', '-')}_notebook.pdf"
        },
    )
