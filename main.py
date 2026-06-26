import os
import uuid
import pypandoc
import aiofiles

from fastapi import FastAPI, UploadFile, File, Request, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

PANDOC_ARGS = [
    "--standalone",
    "--pdf-engine=xelatex",
    "--toc",
    "-V", "geometry:margin=2.5cm",
    "-V", "fontsize=12pt",
    "--lua-filter=fix_math.lua",
    "--from=markdown+tex_math_dollars+tex_math_single_backslash",
]


def _get_paths(output_format: str = "pdf"):
    os.makedirs("tmp", exist_ok=True)
    name = str(uuid.uuid4())[:8]
    return f"tmp/input_{name}.md", f"tmp/output_{name}.{output_format}"


def _file_response(output_path: str, output_format: str, background_tasks: BackgroundTasks) -> FileResponse:
    media_type = (
        "application/pdf"
        if output_format == "pdf"
        else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    background_tasks.add_task(os.remove, output_path)
    return FileResponse(output_path, media_type=media_type, filename=f"output.{output_format}")


@app.post("/convert_text")
async def convert_text(request: Request, type: str = "pdf", background_tasks: BackgroundTasks = None):
    content = (await request.body()).decode("utf-8")
    if not content.strip():
        raise HTTPException(status_code=400, detail="No content provided")

    output_format = "pdf" if type == "pdf" else "docx"
    md_path, output_path = _get_paths(output_format)

    async with aiofiles.open(md_path, "w", encoding="utf-8") as f:
        await f.write(content)

    try:
        pypandoc.convert_file(md_path, output_format, outputfile=output_path, extra_args=PANDOC_ARGS)
    except RuntimeError as e:
        print(f"Conversion failed: {e}")
        raise HTTPException(status_code=500, detail=f"Conversion failed: {e}")
    finally:
        if os.path.exists(md_path):
            os.remove(md_path)  # input cleaned up immediately

    return _file_response(output_path, output_format, background_tasks)


@app.post("/convert")
async def convert(file: UploadFile = File(...), type: str = "pdf", background_tasks: BackgroundTasks = None):
    content = await file.read()

    output_format = "pdf" if type == "pdf" else "docx"
    md_path, output_path = _get_paths(output_format)

    async with aiofiles.open(md_path, "wb") as f:
        await f.write(content)

    try:
        pypandoc.convert_file(md_path, output_format, outputfile=output_path, extra_args=PANDOC_ARGS)
    except RuntimeError as e:
        print(f"Conversion failed: {e}")
        raise HTTPException(status_code=500, detail=f"Conversion failed: {e}")
    finally:
        if os.path.exists(md_path):
            os.remove(md_path)

    return _file_response(output_path, output_format, background_tasks)


@app.get("/health")
def health():
    return {"status": "ok", "pandoc": pypandoc.get_pandoc_version()}


app.mount("/", StaticFiles(directory="frontend", html=True), name="static")