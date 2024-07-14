## USGS Knowledge Base Q&A RAG Chain

To build a retrieval augmented generation chain for our USGS knowledge base Q&A, we automate these steps:
1. Scrape the [USGS water services documentation](https://waterservices.usgs.gov/docs) along with child pages
2. Run the retrieved HTML pages through a local Docker instance of the [nlm-ingestor](https://github.com/nlmatics/nlm-ingestor)

