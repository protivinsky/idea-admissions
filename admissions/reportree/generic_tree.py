from __future__ import annotations
from collections import defaultdict
from typing import List, Tuple, Union, Any

# TODO:
#   - is it better to have leafs as dicts with _value? or as just values?
#   - I can just handle in getitem and setitem, is is sane?
#   - should I enforce some ordering on the dict?


class GenericTree(defaultdict):
    _LEAF_KEY = "_value"

    def __init__(self, *args, **kwargs):
        super().__init__(self.__class__, *args, **kwargs)

    def __getitem__(self, key):
        if self.is_leaf():
            if key == self._LEAF_KEY:
                return super().__getitem__(key)
            else:
                raise KeyError(f"Leaf {self} has no key {key}.")
        else:
            child = super().__getitem__(key)
            if child.is_leaf():
                return child.get_value()
            else:
                return child

    def __setitem__(self, key, value):
        if self.is_leaf():
            if key == self._LEAF_KEY:
                super().__setitem__(key, value)
            else:
                raise KeyError(f"Leaf {self} cannot contain values.")
        else:
            if key == self._LEAF_KEY:
                if not self.keys():
                    super().__setitem__(key, value)
                else:
                    raise KeyError(f"Node {self} cannot contain leaf value.")
            else:
                if isinstance(value, GenericTree):
                    super().__setitem__(key, value)
                else:
                    super().__setitem__(key, self.__class__.leaf(value))

    def add(self, path: Tuple[str], value: Any):
        if self.is_leaf():
            raise ValueError(f"Cannot add to leaf {self}.")
        tree = self
        for part in path:
            tree = tree[part]
        tree.set_value(value)

    def lookup(self, path: Tuple[str]) -> Union[GenericTree, Any]:
        tree = self
        for part in path:
            tree = tree[part]
        return tree.get_value() if tree.is_leaf() else tree

    def filter(self, path_filters):
        if self.is_leaf():
            return self.copy()
        elif not path_filters:
            return self.copy()

        keys = path_filters[0]
        if keys is None:
            keys = self.keys()
        new_tree = self.__class__()
        for key in keys:
            if not key in self:
                raise ValueError(f"Key {key} not found in {self}.")
            new_tree[key] = self[key].filter(path_filters[1:])
        return new_tree

    def prune(self):
        """Remove levels just with a single key:"""
        if self.is_leaf():
            return self.copy()

        new_tree = self.__class__()
        for key, value in self.items():
            new_value = value.prune()
            if len(new_value) == 1 and not new_value.is_leaf():
                new_tree[key] = next(iter(new_value.values()))
            else:
                new_tree[key] = new_value

        # If after simplifying all the children, the new_tree only has one key
        # and it is not '_value', replace the tree with its single child.
        if len(new_tree) == 1 and not new_tree.is_leaf():
            new_tree = next(iter(new_tree.values()))

        return new_tree

    def map(self, f):
        if self.is_leaf():
            return self.__class__.leaf(f(self.get_value()))
        new_tree = self.__class__()
        for key, value in self.items():
            new_tree[key] = value.map(f)
        return new_tree

    def pretty_print(self, level=0):
        if not level:
            print(f"{self.__class__.__name__}[", end="")
        if self.is_leaf():
            print(" = " + str(self.get_value()), end="")
        else:
            for k, v in self.items():
                print("\n" + "    " * (level + 1) + k, end="")
                v.pretty_print(level=level + 1)
        if not level:
            print("\n]")

    def is_leaf(self):
        return GenericTree._LEAF_KEY in self

    def num_children(self):
        return len(self) - 1 if self.is_leaf() else len(self)

    def get_value(self):
        return self[self._LEAF_KEY]

    def set_value(self, value: Any):
        if self.keys() and not self.is_leaf():
            raise ValueError(f"Cannot set value of non-leaf {self}.")
        self[self._LEAF_KEY] = value

    @classmethod
    def leaf(cls, value: Any):
        leaf = cls()
        leaf.set_value(value)
        return leaf

    def __eq__(self, other: GenericTree) -> bool:
        if self.is_leaf() != other.is_leaf():
            return False
        if self.is_leaf():
            return self.get_value() == other.get_value()
        if set(self.keys()) != set(other.keys()):
            return False
        for k in self.keys():
            if self[k] != other[k]:
                return False
        return True

    def __copy__(self):
        if self.is_leaf():
            return self.leaf(self.get_value())
        new_tree = self.__class__()
        for k, v in self.items():
            new_tree[k] = v.__copy__()
        return new_tree

    copy = __copy__

    def __str__(self):
        if self.is_leaf():
            inner = f'"{self._LEAF_KEY}" = {self.get_value()}'
        else:
            inner = '"' + '", "'.join(self.keys()) + '"' if self.keys() else ""
        return f"{self.__class__.__name__}[{inner}]"

    __repr__ = __str__
