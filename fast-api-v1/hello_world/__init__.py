# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import time


def main(
    name: tuple[
        str,
    ]
) -> str:
    if name[0] == "Madrid":
        time.sleep(5)
    elif name == "Seattle":
        time.sleep(10)
        # Uncoment to force a task to fail :)
        # raise Exception("City not supported")
    elif name == "Tokyo":
        time.sleep(15)
    elif name == "London":
        time.sleep(20)

    return f"Hello {name}!"
