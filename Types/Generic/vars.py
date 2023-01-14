from typing import TypeVar, Union


T = TypeVar("T")
V = TypeVar("V")
K = TypeVar("K")
U = TypeVar("U")
N = type(None)

Un_TV = Union[T, V]
Un_TVN = Union[T, V, None]
Un_TVK = Union[T, V, K]
Un_TVKN = Union[T, V, K, None]

Beak_Status = Un_TVKN[str, bool, int]

