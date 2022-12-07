# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import json

import azure.functions as func
import azure.durable_functions as df


def orchestrator_function(context: df.DurableOrchestrationContext):
    context.set_custom_status("Started the proccess")
    result1 = yield context.call_activity("hello_world", "Madrid")
    context.set_custom_status("Madrid done")
    result2 = yield context.call_activity("hello_world", "London")
    context.set_custom_status("London done")
    result3 = yield context.call_activity("hello_world", "Tokyo")
    context.set_custom_status("Tokyo done")
    result4 = yield context.call_activity("hello_world", "Seattle")
    context.set_custom_status("All cities done")
    return [result1, result2, result3, result4]


main = df.Orchestrator.create(orchestrator_function)
