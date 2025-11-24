# from __future__ import annotations

import importlib
import re
from pathlib import Path

from typing import Dict, Optional

from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter as StrawberryGraphQLRouter

router: APIRouter = APIRouter(prefix="/api")

_pkg_name = __name__
_pkg_path = Path(__file__).parent
print(f"[api] Auto-discovering endpoints in package: {_pkg_name} ({_pkg_path})")

# Track mounted GraphQL endpoints per version
_graphql_mounted: Dict[str, bool] = {}


###########################################
### Private methods
###########################################


# Infer endpoint version from path parts like src.api.rest.v1.example and src.api.v1.example -> "v1"
def _infer_version(parts: tuple[str, ...]) -> Optional[str]:
    """Infer endpoint version from path parts"""

    for part in parts:
        if re.fullmatch(r"v\d+", part.lower()):
            return part

    return None


###########################################
### Auto discovery of REST and GraphQL modules across the repository
###########################################

# Iterate through all Python files in this package
for file in _pkg_path.rglob("*.py"):
    name = file.name

    # Skip private and non-endpoint modules
    if name.startswith("_") or name == "dependencies.py":
        continue

    # Construct dotted path for import
    rel_path = file.relative_to(Path(__file__).parent).with_suffix("")
    dotted_path = ".".join((_pkg_name, *rel_path.parts))
    parts = file.relative_to(_pkg_path).parts

    # Infer version from path parts
    version = _infer_version(parts)
    ver_key = version or ""

    # Import module
    try:
        mod = importlib.import_module(dotted_path)
    except Exception as ex:
        print(f"Import failed {dotted_path}: {ex}")
        continue

    # REST
    rest_router = getattr(mod, "router", None)
    if rest_router is not None:
        try:
            router.include_router(rest_router, prefix=f"/{version}" if version else "")
        except Exception as ex:
            print(f"[api] Include REST failed {dotted_path}: {ex}")

    # GraphQL with versioning
    if not _graphql_mounted.get(ver_key, False):
        gql_router = getattr(mod, "graphql_router", None)
        if gql_router is not None:
            try:
                router.include_router(
                    gql_router, prefix=f"/{version}/graphql" if version else "/graphql"
                )
                _graphql_mounted[ver_key] = True
                continue
            except Exception as ex:
                print(f"[api] Include GraphQL router failed {dotted_path}: {ex}")

        schema = getattr(mod, "graphql_schema", None) or getattr(mod, "schema", None)
        if schema is not None and not _graphql_mounted.get(ver_key, False):
            try:
                gql = StrawberryGraphQLRouter(schema)
                router.include_router(
                    gql, prefix=f"/{version}/graphql" if version else "/graphql"
                )
                _graphql_mounted[ver_key] = True
            except Exception as ex:
                print(f"[api] Build GraphQL from schema failed {dotted_path}: {ex}")

###########################################
### Debugging
###########################################

# For debug purposes, list all routes
print("================================")
print("Routes generated...")
for route in router.routes:
    if hasattr(route, "methods"):
        print(f"{route.methods}: {route.path}")
    else:
        print(f"{route.name}: {route.path}")
print("================================")
