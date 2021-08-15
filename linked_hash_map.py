from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Generator, Generic, List, Optional, Tuple, TypeVar

from IPython import embed

K = TypeVar("K")
V = TypeVar("V")


@dataclass
class HashNode:
    key: K
    value: V
    prev_node: HashNode = None
    next_node: HashNode = None


class LinkedHashMap(Generic[K, V]):
    __data: List[List[HashNode]]
    __head: Optional[HashNode] = None
    __tail: Optional[HashNode] = None
    __current_node: Optional[HashNode] = None
    __size: int = 0

    def __init__(self, size: int = 25):
        self.__data = [[]] * size

    def __setitem__(self, key: K, value: V) -> None:
        self.put(key, value)

    def put(self, key: K, value: V) -> None:
        if not self._update_value_if_existing(key, value):
            self._add_node(key, value)

    def _update_value_if_existing(self, key: K, value: V) -> bool:
        node = self._find_node(key)
        if node:
            node.value = value
            return True
        return False

    def _add_node(self, key: K, value: V) -> bool:
        self.__size += 1
        new_node = HashNode(key, value, self.__tail)
        self.__data[self._index_from_key(key)].append(new_node)
        if self.__tail:
            self.__tail.next_node = new_node
        self.__tail = new_node
        if not self.__head:
            self.__head = self.__tail

    def __delitem__(self, key: K) -> None:
        self.remove(key)

    def remove(self, key: K) -> None:
        node = self._find_node_with_error(key)
        self.__size -= 1
        self.__data[self._index_from_key(key)].remove(node)
        if node.prev_node:
            node.prev_node.next_node = node.next_node
        if self.__tail == node:
            self.__tail = node.prev_node
        if self.__size == 0:
            self.__head = None

    def __getitem__(self, key: K) -> V:
        return self.get(key)

    def get(self, key: K) -> V:
        node = self._find_node_with_error(key)
        return node.value

    def _find_node_with_error(self, key: K) -> HashNode:
        node = self._find_node(key)
        if not node:
            raise KeyError(key)
        return node

    def _find_node(self, key: K) -> Optional[HashNode]:
        for node in self.__data[self._index_from_key(key)]:
            if node.key == key:
                return node
        return None

    def _index_from_key(self, key: K) -> int:
        return hash(key) % len(self.__data)

    def sort(self, reverse: bool = False, key: Callable[[K], Any] = None) -> None:
        if self.__size == 0:
            return
        sorted_keys = sorted(self.keys(), reverse=reverse, key=key)
        self.__head = self._find_node(sorted_keys[0])
        self.__head.prev_node = None
        self.__tail = self._find_node(sorted_keys[-1])
        self.__tail.next_node = None
        for prev_key, curr_key, next_key in zip(
            [None] + sorted_keys[:-1],
            sorted_keys,
            sorted_keys[1:] + [None],
        ):
            node = self._find_node(curr_key)
            if prev_key is not None:
                node.prev_node = self._find_node(prev_key)
            if next_key is not None:
                node.next_node = self._find_node(next_key)

    def keys(self) -> Generator[K]:
        return (key for key in self)

    def values(self) -> Generator[V]:
        return (self[key] for key in self)

    def items(self) -> Generator[Tuple[K, V]]:
        return ((key, self[key]) for key in self)

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        item_reprs = [f"{repr(key)}: {repr(self[key])}" for key in self]
        full_repr = ", ".join(item_reprs)
        return f"{{{full_repr}}}"

    def __iter__(self) -> LinkedHashMap:
        self.__current_node = self.__head
        return self

    def __next__(self) -> K:
        if not self.__current_node:
            raise StopIteration
        key = self.__current_node.key
        self.__current_node = self.__current_node.next_node
        return key

    def __len__(self) -> int:
        return self.__size


embed()
