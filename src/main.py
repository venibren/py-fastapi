from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path
import importlib

app = FastAPI(
    title="Experimental FastAPI App",
    description="Just a basic application to learn and experiment with FastAPI",
    version="0.0.1",
    root_path="/api",
)

# Import the routers package to find all router modules
pkg = importlib.import_module("src.routers")
pkg_path = Path(pkg.__file__).parent

# Dynamically import and include all routers from the src.routers package
for module_path in pkg_path.glob("*.py"):
    # Skip dunder and private files
    if module_path.name.startswith("_"):
        continue

    # Derive the full module name
    module_name = module_path.stem
    full_module_name = f"src.routers.{module_name}"

    # Import the module
    try:
        module = importlib.import_module(full_module_name)
    except Exception as exc:
        # Log and continue instead of crashing the whole app
        print(f"Failed to import {full_module_name}: {exc}")
        continue

    # Get the router attribute
    router = getattr(module, "router", None)
    if router is None:
        # No "router" attribute, skip quietly
        continue

    # Include the router in the main app
    app.include_router(router)
    print(f"Included router from {full_module_name}")


# Define root and favicon endpoints
@app.get("/")
async def root():
    return {"message": "There's nothing here... yet!"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(str("./src/assets/favicon.ico"))
