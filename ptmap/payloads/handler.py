from ptmap.utils.file import load_file
from ptmap.payloads.generator import payload_gen
from ptmap.dependencies.injector import generate_injection_points

def format_payload(url: str, payload: str) -> str:
    return generate_injection_points(url=url, payload=payload)

def load_payloads(
    target_os: str,  
    payloads: str = "traverse", 
    custom_payloads: str = None,
    max_depth: int = 10
    )-> list[str]:
    
    loaded_payloads = []
    
    def get_payloads(payloads_: dict[str, list], key: str) -> list[str]:
        normalized_key = [ks for k in key.split(',') if (ks:=k.strip())]

        get_payload = lambda x: payloads_.get(x, None)
        extend_payloads = lambda x: loaded_payloads.extend(x)
        
        for nk in normalized_key:
            payloads_got = get_payload(nk)
            
            if nk == "all":
                
                payloads_values = [
                    value for values in payloads_.values()
                    for value in values
                ]
                
                extend_payloads(payloads_values)
                return
            
            elif payloads_got:
                extend_payloads(payloads_got)
            
        additional_payloads = ["legacy_bypasses", "direct_path"]
        
        for add_payload in additional_payloads:
            payload_got_ = get_payload(add_payload)
            extend_payloads(payload_got_)

    if custom_payloads:
        loaded_payloads = load_file(custom_payloads)
    else:
        generated_payloads = payload_gen(
            target_os=target_os, 
            max_depth=max_depth
            )
        get_payloads(payloads_=generated_payloads, key=payloads)
        
    return loaded_payloads

