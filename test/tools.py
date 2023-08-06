import functools
from typing import Iterable, Dict, Any


DESCRIPTION_KEY = "__description__"


def multitest(inputs: Iterable[Dict[str, Any]]):
    def multitest_decorator(f):
        @functools.wraps(f)
        def decorated(self, *existing_args, **existing_kwargs):
            for i, additionnal_kwargs in enumerate(inputs):
                with self.subTest(
                    additionnal_kwargs.get(DESCRIPTION_KEY, f"Subtest {i}")
                ):
                    f(
                        self,
                        *existing_args,
                        **existing_kwargs,
                        **{
                            k: v
                            for k, v in additionnal_kwargs.items()
                            if k != DESCRIPTION_KEY
                        },
                    )

        return decorated

    return multitest_decorator
