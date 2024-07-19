import logging
import azure.functions as func
import utils as utils

app = func.FunctionApp()

@app.schedule(schedule="0 0 0 1,8,15,22,29 * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def update_embeddings(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    # Scrape the USGS water services documentation
    url = "https://waterservices.usgs.gov/docs/"
    links = utils.find_pages_from_base(url)
    logging.info(f"Found {len(links)} pages to process.")

    # Process the pages
    embeddings = []
    for link in links:
        embeddings.extend(utils.unstructured_page_processing(link))
        logging.info(f"Processed page: {link} with {len(embeddings)} embeddings.")

    logging.info(f"Total chunks processed: {len(embeddings)}.")

    # Upsert the embeddings to Pinecone database
    utils.update_embeddings_in_pinecone(embeddings)

    logging.info('Python timer trigger function executed.')