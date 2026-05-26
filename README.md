# PTMAP

Path Traversal Mutation Fuzzer

PTMAP is an asynchronous path traversal fuzzing and detection tool written in Python.

## Features

- Traversal mutation payloads
- URL and file targets
- Async scanning
- Payload selection
- Multiple encoding techniques

## Installation

pip install ptmap

## Usage

ptmap TARGET

Example:

ptmap "https://target.com/image?file=FUZZ"