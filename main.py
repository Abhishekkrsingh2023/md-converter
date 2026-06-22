import os
import uuid
import pypandoc

from fastapi.staticfiles import StaticFiles
from fastapi import (
    FastAPI, UploadFile, File, Request,HTTPException,
    BackgroundTasks
)
from fastapi.responses import FileResponse

app = FastAPI()


PANDOC_ARGS = [
    "--pdf-engine=xelatex",
    "-V", "geometry:margin=2.5cm",
    "-V", "fontsize=12pt",
    "--toc",
]

def _get_input_output_paths(output_format: str = "pdf"):
    os.makedirs("tmp", exist_ok=True)
    input_filename = f"{str(uuid.uuid4())[:8]}"
    md_path = os.path.join("tmp", "input_" + input_filename + ".md")
    output_path = os.path.join("tmp", "output_" + input_filename + f".{output_format}")
    return md_path, output_path

# Convert from mardown content to pdf or docx
@app.post("/convert_text")
async def convert(request: Request, type: str = "pdf", background_tasks: BackgroundTasks = None): 
    content = await request.body()
    content = content.decode("utf-8")
    if not content.strip():
        raise HTTPException(status_code=400, detail="No content provided")

    output_format = "pdf" if type == "pdf" else "docx"
    md_path, output_path = _get_input_output_paths(output_format)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(content)

    pypandoc.convert_file(
        md_path,
        output_format,
        outputfile=output_path,
        extra_args=PANDOC_ARGS,
    )
    background_tasks.add_task(os.remove, md_path)
    background_tasks.add_task(os.remove, output_path)

    return FileResponse(
        output_path,
        media_type="application/pdf" if output_format == "pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=f"output.{output_format}",
    )

@app.post("/convert")
async def convert_md_to_pdf(file: UploadFile = File(...), type: str = "pdf", background_tasks: BackgroundTasks = None):
    content = await file.read()
    
    output_format = "pdf" if type == "pdf" else "docx"
    md_path, output_path = _get_input_output_paths(output_format)

    with open(md_path, "wb") as f:
        f.write(content)

    pypandoc.convert_file(
        md_path,
        output_format,
        outputfile=output_path,
        extra_args=PANDOC_ARGS,
    )
    background_tasks.add_task(os.remove, md_path)
    background_tasks.add_task(os.remove, output_path)

    return FileResponse(
        output_path,
        media_type="application/pdf" if output_format == "pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=f"output.{output_format}",
    )

@app.get("/health")
def health():
    return {"status": "ok", "pandoc": pypandoc.get_pandoc_version()}


app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
