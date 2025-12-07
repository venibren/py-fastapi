import importlib
import re
import types
from pathlib import Path
from typing import List, Optional, Sequence, Tuple, TypeAlias

from fastapi import APIRouter
from strawberry import Schema
from strawberry.fastapi import GraphQLRouter as StrawberryGraphQLRouter
from strawberry.tools import merge_types

from src.app.core.logger import get_logger

_logger = get_logger(__name__)

###########################################
# Type aliases
###########################################
GraphQLRootClass: TypeAlias = type
GraphQLRootList: TypeAlias = List[GraphQLRootClass]
TripleOptionalRootClasses: TypeAlias = Tuple[
    Optional[GraphQLRootClass], Optional[GraphQLRootClass], Optional[GraphQLRootClass]
]


###########################################
# Discovery setup
###########################################
_package_name: str = __name__
_package_path: Path = Path(__file__).parent
_logger.debug("Auto-discovering endpoints in package: %s", _package_name)


###########################################
# API router to collect discovered endpoints
###########################################
api_router: APIRouter = APIRouter()


###########################################
# Collected GraphQL root types
###########################################
_graphql_query_root_types: GraphQLRootList = []
_graphql_mutation_root_types: GraphQLRootList = []
_graphql_subscription_root_types: GraphQLRootList = []


###########################################
# Private helpers
###########################################


# Infer version from path parts
def _infer_version(parts: Sequence[str]) -> Optional[str]:
    """
    Infer 'vN' wgeb present in a path sequence.
    Examples:
    - 'src.api.v1.module' -> 'v1'
    - 'src.api.v2.module' -> 'v2'
    - 'src.api.rest.v1.module' -> 'v1'
    - 'src.api.rest.v2.module' -> 'v2'
    - 'src.api.module' -> None
    - 'src.api.legacy.module' -> None
    - 'src.api.graphql.module' -> None

    REST versioning only; GraphQL has no versioning.
    """

    for part in parts:
        if re.fullmatch(r"v\d+", part.lower()):
            return part
    return None


def _collect_graphql_roots_from_schema(schema: Schema) -> TripleOptionalRootClasses:
    """
    Extraction of Strawberry root types from a Schema.
    Backward compatibility when modules export 'schema' instead of root classes.
    """

    # Prefer direct attributes if available across Strawberry versions
    query_candidate: object = getattr(schema, "_query_type", None)
    mutation_candidate: object = getattr(schema, "_mutation_type", None)
    subscription_candidate: object = getattr(schema, "_subscription_type", None)

    # Fallback to public helper if present, wrappers vary by Strawberry version
    try:
        if query_candidate is None and hasattr(schema, "get_root_type"):
            query_wrapper: object = schema.get_root_type("query")
            query_candidate = (
                getattr(query_wrapper, "python_name", None)
                or getattr(query_wrapper, "origin", None)
                or getattr(query_wrapper, "wrapper", None)
                or getattr(query_wrapper, "annotation", None)
            )
        if mutation_candidate is None and hasattr(schema, "get_root_type"):
            mutation_wrapper: object = schema.get_root_type("mutation")
            mutation_candidate = (
                getattr(mutation_wrapper, "python_name", None)
                or getattr(mutation_wrapper, "origin", None)
                or getattr(mutation_wrapper, "wrapper", None)
                or getattr(mutation_wrapper, "annotation", None)
            )
        if subscription_candidate is None and hasattr(schema, "get_root_type"):
            subscription_wrapper: object = schema.get_root_type("subscription")
            subscription_candidate = (
                getattr(subscription_wrapper, "python_name", None)
                or getattr(subscription_wrapper, "origin", None)
                or getattr(subscription_wrapper, "wrapper", None)
                or getattr(subscription_wrapper, "annotation", None)
            )
    except Exception:
        # Schema internals differ across versions, failing softly preserves discovery
        pass

    def ensure_class_or_none(candidate: object) -> Optional[GraphQLRootClass]:
        return candidate if isinstance(candidate, type) else None

    return (
        ensure_class_or_none(query_candidate),
        ensure_class_or_none(mutation_candidate),
        ensure_class_or_none(subscription_candidate),
    )


def _merge_graphql_types(
    label: str, type_list: GraphQLRootList
) -> Optional[GraphQLRootClass]:
    """
    Avoid crash when merging 0/1 types.
    Strawberry expects >=2 for merge.
    """

    if not type_list:
        return None
    if len(type_list) == 1:
        return type_list[0]
    return merge_types(label, tuple(type_list))


###########################################
# Auto discovery of REST and GraphQL modules
###########################################
for source_file in _package_path.rglob("*.py"):
    filename: str = source_file.name

    # Skip private modules and common non-endpoint helpers
    if filename.startswith("_") or filename == "dependencies.py":
        continue

    # Build dotted import path: <package>.<relative.parts.without.suffix>
    relative_path: Path = source_file.relative_to(Path(__file__).parent).with_suffix("")
    module_dotted_path: str = ".".join((_package_name, *relative_path.parts))
    _logger.silly("Discovered module: %s", module_dotted_path)

    # Determine REST version from path (GraphQL remains global)
    relative_parts: Tuple[str, ...] = source_file.relative_to(_package_path).parts

    # Import module
    try:
        imported_module: types.ModuleType = importlib.import_module(module_dotted_path)
    except Exception as ex:
        _logger.exception("Import failed %s: %s", module_dotted_path, ex)
        continue

    # REST: include module router when present
    module_rest_router: Optional[APIRouter] = getattr(imported_module, "router", None)
    if module_rest_router is not None:
        rest_version: Optional[str] = _infer_version(relative_parts)
        try:
            api_router.include_router(
                module_rest_router,
                prefix=f"/{rest_version}" if rest_version else "",
            )
        except Exception as ex:
            _logger.exception("Include REST failed %s: %s", module_dotted_path, ex)

    # GraphQL: collect global root classes (no versioning)
    try:
        query_root: object = getattr(imported_module, "Query", None)
        mutation_root: object = getattr(imported_module, "Mutation", None)
        subscription_root: object = getattr(imported_module, "Subscription", None)

        if isinstance(query_root, type):
            _graphql_query_root_types.append(query_root)
        if isinstance(mutation_root, type):
            _graphql_mutation_root_types.append(mutation_root)
        if isinstance(subscription_root, type):
            _graphql_subscription_root_types.append(subscription_root)

        # Derive from exported 'schema' when root classes were not explicitly provided
        if not any(
            isinstance(x, type) for x in (query_root, mutation_root, subscription_root)
        ):
            module_schema_attr: object = getattr(imported_module, "schema", None)
            if isinstance(module_schema_attr, Schema):
                derived_query_root, derived_mutation_root, derived_subscription_root = (
                    _collect_graphql_roots_from_schema(module_schema_attr)
                )
                if derived_query_root is not None:
                    _graphql_query_root_types.append(derived_query_root)
                if derived_mutation_root is not None:
                    _graphql_mutation_root_types.append(derived_mutation_root)
                if derived_subscription_root is not None:
                    _graphql_subscription_root_types.append(derived_subscription_root)
            elif module_schema_attr is not None:
                # If a 'schema' symbol exists but is not Strawberry Schema; warn and continue.
                _logger.silly(
                    "Ignored non-Schema 'schema' in %s (type=%s)",
                    imported_module.__name__,
                    type(module_schema_attr),
                )
    except Exception as ex:
        _logger.exception("Collect GraphQL types failed %s: %s", module_dotted_path, ex)

###########################################
# Build & mount a GraphQL endpoint
###########################################
if _graphql_query_root_types:
    try:
        merged_query_root: Optional[GraphQLRootClass] = _merge_graphql_types(
            "Query", _graphql_query_root_types
        )
        merged_mutation_root: Optional[GraphQLRootClass] = _merge_graphql_types(
            "Mutation", _graphql_mutation_root_types
        )
        merged_subscription_root: Optional[GraphQLRootClass] = _merge_graphql_types(
            "Subscription", _graphql_subscription_root_types
        )

        graphql_schema: Schema = Schema(
            query=merged_query_root,
            mutation=merged_mutation_root,
            subscription=merged_subscription_root,
        )
        graphql_router: StrawberryGraphQLRouter = StrawberryGraphQLRouter(
            schema=graphql_schema,
            tags=["GraphQL"],
        )
        api_router.include_router(graphql_router, prefix="/graphql")
    except Exception as ex:
        _logger.exception("GraphQL setup failed: %s", ex)
else:
    _logger.silly("No GraphQL Query types discovered; GraphQL not mounted.")


###########################################
# Debugging
###########################################
if __debug__:
    _logger.debug("Routes generated:")
    for route in api_router.routes:
        if hasattr(route, "methods"):
            _logger.verbose("%s: %s", route.methods, route.path)
        else:
            _logger.verbose("%s: %s", route.name, route.path)
    _logger.debug("Mounted GraphQL with:")
    _logger.verbose("{%s} Query", len(_graphql_query_root_types))
    _logger.verbose("{%s} Mutation", len(_graphql_mutation_root_types))
    _logger.verbose("{%s} Subscription", len(_graphql_subscription_root_types))


# Exported symbols
__all__ = ["api_router"]
