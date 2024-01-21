# GPT-Explainer

GPT-Explainer is a Python-based application designed to enhance the understanding of PowerPoint presentations by automatically generating explanations for each slide using the GPT-3.5 AI model. 

## Project Structure

### 1. API Module - Flask-based Interface
It consists of two routes: 
1. File Upload Route - allows users to submit PPTX files for processing. The file is stored in the `uploads` directory and the upload details are recorded in a database.
2. Status Request Route - enables users to request the status of a previously submitted upload.

### 2. Client Module
Enables users to upload files and check their status.

### 3. Database Module

Uses SQLAlchemy as an ORM. Defines two tables:
1. `Users`: Represents individuals uploading files.
2. `Uploads`: Represents uploaded files and associated metadata.

### 4. Explainer Module
Connects parsing of the presentation with asynchronous calls to the OpenAI API to receive explanations for each slide.

### 5. OpenAI Module
Connects to the OpenAI API, sending prompts to summarize slides.

### 6. PPTX Parser Module
Parses a pptx file, yielding text and index numbers for each slide using the `pptx` library.

### 7. Tests Module
Tests the app functionality using `pytest`.

## Dependencies
* Flask
* pptx
* requests
* SQLAlchemy
* Pytest  
