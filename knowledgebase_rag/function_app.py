import logging
import azure.functions as func

app = func.FunctionApp()

@app.schedule(schedule="0 0 0 1,8,15,22,29 * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def update_embeddings(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')