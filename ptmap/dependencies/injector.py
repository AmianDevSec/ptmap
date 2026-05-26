from urllib.parse import (
    urlparse,
    parse_qsl,
    urlencode,
    urlunparse
)


def generate_injection_points(
    url: str,
    payload: str
) -> list[str]:

    parsed = urlparse(url)

    #
    # Query parameter mode
    #

    if parsed.query:

        params = parse_qsl(
            parsed.query,
            keep_blank_values=True
        )

        injected_urls = []

        for index, (key, _) in enumerate(params):

            cloned_params = params.copy()

            cloned_params[index] = (
                key,
                payload
            )

            rebuilt_query = urlencode(
                cloned_params,
                doseq=True
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

    stripped_path = parsed.path.rstrip("/")

    splitted_path = stripped_path.split("/")

    if splitted_path and splitted_path[-1]:

        splitted_path[-1] = payload

    rebuilt_path = "/".join(splitted_path)

    return [
        urlunparse(
            parsed._replace(
                path=rebuilt_path
            )
        )
    ]


if __name__ == "__main__":

    urls = [
        "https://site.com/page?a=1&b=fuzz",
        "https://site.com/page?a=1&b=2&c=3",
        "https://site.com/path/file.txt",
        "https://site.com/path/"
    ]

    for url in urls:

        for injected in generate_injection_points(
            url,
            "PAYLOAD"
        ):

            print(injected)