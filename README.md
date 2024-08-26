# USGS Water Chat

NOTE: THIS IS A WORK IN PROGRESS

I've only completed:
- [knowledgebase_rag](https://github.com/mradassaad/usgs-water-chat/tree/main/knowledgebase_rag), so far, where I push documentation embeddings to Pinecone on a schedule using [Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview?pivots=programming-language-python)

## Introduction

USGS-chat is a project aiming at making USGS water services documentation and data available through a chatbot interface implemented using OpenAI's ChatGPT-3.5. The goal of this project is to make US water services data available through natural language through:

- Retrieving relevant documentation so practitioners can better utilize the USGS water services API
- Constructing URLs allowing practitioners to directly download the data they need

The goals of this project are learning and fun. As an ML Engineer at a Civil Engineering company, this is a fun way of simplifying what I have observed to be a pain point for many employees who'd rather not spend hours on documentation. Personally, I was intrigued by:

- The challenge of incorporating web pages as part of a RAG app
- Designing a compound system able to answer questions and retrieve data on the user's behalf
- Explore evaluation techniques for such compound systems

## Features

- The app allows the user to enter queries and get a response quickly
- The app keeps track of the chat history
- The app is aware of the latest water services documentation on the USGS website
- The evaluation of the full app (from a chatbot perspective) is available to users
- The app generates URLs users can click on the start downloads of the data they need
