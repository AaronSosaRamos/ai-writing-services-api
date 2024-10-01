# AI Writing Services API

**AI Writing Services API** is a powerful API designed to provide advanced writing services in JSON format. It offers five core writing services: **Spelling Check**, **Writing Enhancement**, **Addition of Connectors**, **Textual Tone Shifts**, and **Plagiarism Check**. The API uses state-of-the-art AI technologies to emulate complex writing processes, ensuring that users receive high-quality suggestions and corrections for their written content.

Developed by **Wilfredo Aaron Sosa Ramos**, this API leverages a combination of **Google Generative AI**, **GPT-4o-mini**, and other AI models through **LangChain** and **LangGraph** frameworks. It is optimized for complex writing tasks, employing a **few-shot learning approach** for better results in JSON format responses.

## Table of Contents

- [1. Features](#1-features)
- [2. Writing Services](#2-writing-services)
- [3. Technologies Used](#3-technologies-used)
- [4. Few-shot Approach](#4-few-shot-approach)
- [5. API Endpoints](#5-api-endpoints)

---

## 1. Features

**AI Writing Services API** offers comprehensive features that support a variety of writing services designed to enhance and correct text input. The main features include:

- **Spelling Check**: Detects and corrects spelling errors in the provided text.
- **Writing Enhancement**: Improves sentence structure, grammar, and overall flow.
- **Addition of Connectors**: Adds logical connectors to improve the flow and coherence of paragraphs.
- **Textual Tone Shifts**: Adjusts the tone of the text, such as changing from formal to informal or vice versa.
- **Plagiarism Check**: Checks for duplicate content across a vast database to ensure originality.

The API is designed to handle complex language processing tasks and produce refined responses in JSON format that can easily be integrated into different applications.

---

## 2. Writing Services

The **AI Writing Services API** provides five key writing services, each aimed at improving the quality and coherence of written content:

- **Spelling Check**: The API analyzes the input text for spelling errors and provides corrections in the JSON response. This feature ensures that all words are spelled correctly, offering alternative suggestions when needed.
  
- **Writing Enhancement**: This service focuses on improving the overall quality of writing by suggesting better sentence structures, grammar corrections, and stylistic improvements. It is particularly useful for refining essays, reports, or any professional writing.

- **Addition of Connectors**: Enhances the logical flow of a document by adding appropriate connectors (such as "however", "moreover", "in addition"). This service makes it easier for the reader to follow the argument or narrative.

- **Textual Tone Shifts**: This feature allows the user to modify the tone of the text. For instance, the API can transform an informal tone into a formal one or adjust the language for a specific audience (e.g., making it more persuasive or neutral).

- **Plagiarism Check**: The API checks the input text against a wide array of sources to detect any copied or duplicated content, ensuring the originality of the writing. This feature is especially valuable for academic work and professional publications.

---

## 3. Technologies Used

The **AI Writing Services API** leverages a robust technology stack to deliver high-quality writing services. The main technologies used include:

- **Python**: The primary language for building the API, offering extensive libraries for machine learning, natural language processing, and API development.
- **FastAPI**: A modern, fast web framework for building APIs with Python, known for its performance and simplicity.
- **LangChain**: A framework that integrates with language models such as **GPT-4o-mini** and **Google Generative AI** to enable advanced natural language processing tasks.
- **LangGraph**: A powerful tool used to manage and process complex workflows involving multiple AI models, ensuring seamless coordination between different language models.
- **Google Generative AI**: A language model that provides the backbone for tasks such as writing enhancement and tone shifting.
- **GPT-4o-mini**: An optimized version of GPT-4 that provides strong support for natural language understanding and generation, ensuring high accuracy and relevance in the responses.

This stack ensures the API is capable of handling complex language tasks with precision and efficiency, providing users with reliable, high-quality responses.

---

## 4. Few-shot Approach

The **AI Writing Services API** employs a **few-shot learning approach** to enhance the accuracy of its responses. Few-shot learning involves training the AI model with a limited number of examples, allowing it to better understand and generalize various writing tasks. This approach is particularly effective in generating high-quality results for services such as:

- **Textual Tone Shifts**: The model can understand subtle shifts in tone based on a few examples, adjusting the text as per user requirements.
- **Writing Enhancement**: The API refines sentences and paragraphs with minimal input by using prior knowledge to recognize optimal improvements.
- **Addition of Connectors**: The API effectively inserts logical connectors in text based on few-shot learning, ensuring coherence and fluidity.

By leveraging few-shot learning, the API can deliver precise, contextually appropriate responses with minimal user input, making it a versatile tool for a variety of writing services.

---

## 5. API Endpoints

The **AI Writing Services API** offers several endpoints to handle different writing services. Below are the key endpoints and their functionality:

- **POST /check-spelling**: This endpoint accepts text input and returns JSON responses with spelling corrections and suggestions.

- **POST /writing-enhancement**: Submits text for enhancement, and the API responds with suggested improvements to grammar, sentence structure, and flow.

- **POST /addition-of-connectors**: This endpoint processes the input text and adds appropriate connectors to improve the logical flow.

- **POST /textual-tone-shifts**: Accepts text and adjusts its tone based on user preferences (e.g., formal, informal).

- **POST /plagiarism-check**: Users can submit text to check for plagiarism, and the API will return a JSON response indicating whether the content is original or contains duplicate material from other sources.

These endpoints allow developers to integrate the API into various applications, automating writing tasks for enhanced productivity and quality.

---

This README provides an overview of the **AI Writing Services API**, highlighting its features, services, and underlying technologies, ensuring that users can integrate and leverage advanced writing tools into their applications with ease.
