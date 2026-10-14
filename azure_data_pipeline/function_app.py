"""Optional: run the pipeline automatically in Azure Functions (timer trigger, every hour).

Deploy with Azure Functions Core Tools:  func azure functionapp publish <APP_NAME>
Set the same environment variables from .env.example as Function App settings.
"""
import logging

import azure.functions as func

import pipeline

app = func.FunctionApp()


@app.timer_trigger(schedule="0 0 * * * *", arg_name="timer", run_on_startup=False)
def scheduled_pipeline(timer: func.TimerRequest) -> None:
    logging.info("Timer fired - running pipeline")
    pipeline.run(file="sales.csv")
