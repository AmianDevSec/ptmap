import asyncio
import aiohttp
import typer
from typing import Literal
from ptmap.cli_setup.logger import logger
from ptmap.cli_setup.banner import hero
from ptmap.utils.path import resolve_path
from ptmap.utils.file import load_file
from ptmap.utils.handle_pipe import piped_input
from ptmap.dependencies.check import is_vulnerable

from ptmap.utils.utils import (
    truncate_msg,
    is_url
)

from ptmap.payloads.handler import (
    format_payload,
    load_payloads
)

from ptmap.cli_setup.config import (
    payload_size_option,
    platform_option,
    threading_option,
    payloads_option,
    target_option,
    max_depth_option,
    custom_payloads_option
)

app = typer.Typer()

async def worker(session, sem, payload, idx, stop_event, url):
    
    if stop_event.is_set():
        return

    async with sem:

        if stop_event.is_set():
            return

        formatted_payloads = format_payload(url, payload.strip())

        for f_payload in formatted_payloads: 
            
            try:
                async with session.get(f_payload) as r:
                    
                    if stop_event.is_set():
                        return
                
                    body = await r.text()
                    status = r.status

                    truncated_payload = truncate_msg(payload)

                    logger(f"{status = } | { truncated_payload = } | {idx = }")

                    if is_vulnerable(status=status, body=body):
                        logger(
                            f"Traversal vulnerability detected\n\n"
                            f"           Target : {url}\n"
                            f"           Payload: {payload}",
                            "success"
                        )
                        stop_event.set()
                        
                    return body, status, payload
            
            except aiohttp.ClientConnectorError:
                logger(
                    "Connection failed: target unreachable",
                    "error"
                )

            except aiohttp.ServerDisconnectedError:
                logger(
                    "Server disconnected unexpectedly",
                    "warning"
                )

            except asyncio.TimeoutError:
                logger(
                    "Request timed out",
                    "warning"
                )

            except aiohttp.InvalidURL:
                logger(
                    f"Invalid target URL: {url}",
                    "error"
                )

            except aiohttp.ClientConnectionError as e:
                logger(
                    f"Connection error: {e}",
                    "error"
                )

            except Exception as e:
                logger(str(e), "error")
            
async def async_main(
    targets: str,
    custom_payloads: str,
    payloads: str,
    payloads_size: int,
    max_depth: int,
    platform: str,
    threading: int,
    ):
    
    loaded_payload = load_payloads(
        target_os=platform, 
        payloads=payloads,
        custom_payloads=custom_payloads,
        max_depth=max_depth
    )
    
    payloads_length = len(loaded_payload)
    logger(f"Loaded {payloads_length} payloads")
    
    payloads_size = payloads_size or payloads_length
    payloads = None
    
    if payloads_size and payloads_size < 1:
        logger("Payloads size should be a positive integer", "error")
        return
    elif payloads_size > len(loaded_payload):
        logger(f"Payloads size should be less than {len(loaded_payload)}", "error")
        return
    
    payloads = loaded_payload[:payloads_size]
    
    logger(f"Processing payloads {len(payloads)}")
    
    stop_event = asyncio.Event()
    sem = asyncio.Semaphore(threading)

    connector = aiohttp.TCPConnector(limit=0, ssl=False)
    timeout = aiohttp.ClientTimeout(total=35)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:

        tasks = [
            asyncio.create_task(worker(session, sem, p, i, stop_event, target))
            for target in targets
            for i, p in enumerate(payloads)
        ]

        await asyncio.gather(*tasks, return_exceptions=True)

        # cancel everything still running
        for t in tasks:
            t.cancel()

@app.command()
def main(
    target: str = target_option,
    custom_payloads: str  = custom_payloads_option,
    payloads_size: int = payload_size_option,
    threading: int = threading_option,
    max_depth: int = max_depth_option,
    platform: Literal["linux", "windows"] = platform_option,
    payloads: str = payloads_option
    ) -> None:
    
    hero()
    
    targets = resolve_path(target) and load_file(target)
    target_is_url = is_url(target)
    pip_input = piped_input()
    
    if target_is_url:
        targets = [target]
    elif pip_input:
        targets = pip_input
    elif targets:
        pass
    else:
        logger(
            "Use 'ptmap --help' to view available options and usage examples",
            "info"
        )
        
        raise typer.Exit(1)

    asyncio.run(async_main(
        targets=list(dict.fromkeys(targets)),
        custom_payloads=custom_payloads,
        payloads=payloads,
        payloads_size=payloads_size,
        max_depth=max_depth,
        platform=platform,
        threading=threading
    ))

def run():
    typer.run(main)
    
if __name__ == "__main__":
    run()
