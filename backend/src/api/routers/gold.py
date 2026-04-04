from ..dependencies import gold_dep
from .layer import create_layer_router

gold_router = create_layer_router(gold_dep, multi_source=True)
