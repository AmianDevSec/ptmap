import typer

def build_option(
    default: str,
    *names,
    help: str = "...",
    prompt: bool = False, 
    show_default: bool = True
    ):
    
    return typer.Option(
        default,
        *names,
        help=help,
        prompt=prompt,
        show_default=show_default
    )

def build_argument(
    default: str =...,
    help: str = "...",
):
    return typer.Argument(
        default,
        help=help,
    )
    
payload_size_option = build_option(
    None,
    "--size", "-s",
    help=(
        "Request payload size."
    )
)

platform_option = build_option(
    "linux",
    "--platform", "-pf",
    help=(
        "Target operating system "
        "(linux or windows)"
    )
)

threading_option = build_option(
    10,
    "--threads", "-t",
    help=(
        "Number of concurrent worker threads."
    )
)

target_option = build_argument(
    None,
    help=(
    "Target URL or file containing newline-separated target URLs. "
    "(e.g. : https://example.com:8080 or targets.txt)"
    )
)

payloads_option = build_option(
    "traverse,urlencode",
    "--payloads", "-p",
    help=(
        "Comma-separated list of payload mutators to enable. "
        "Available options: traverse, urlencode, "
        "double_urlencode, overlong_utf8, nested_slashes, "
        "encode_dots, nullbyte, direct_path, all. \n\n"
        "Use 'all' to enable every available payload mutator"
    )
)

max_depth_option = build_option(
    10,
    "--max-depth", "-md",
    help=(
        "Maximum traversal depth for payload generation"
    )
)

custom_payloads_option = build_option(
    None,
    "--custom-payloads", "-cp",
    help=(
        "Path to a custom payload file. "
        "If omitted, built-in payload generation is used"
    )
)
