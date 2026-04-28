# My Library Project
 [https://JMnich.pythonanywhere.com](https://JMnich.pythonanywhere.com)

This project is a RESTful Web Application that demonstrates CRUD operations on a book database, integrated with AI features for generating descriptions.

### Features
* **Full CRUD**: Add, View, Update, and Delete books.
* **AI Descriptions**: Uses OpenAI LLM to generate book descriptions.
* **Smart Fallback**: If no OpenAI API key is provided, the system automatically fetches descriptions from the **Google Books API**.

---

### How to Run the Project

#### 1. Set up the Database
* Open **phpMyAdmin**.
* Create a new database named `library`.
* Import the `books.sql` file (found in this repository) into the `library` database.

#### 2. Install Dependencies
Open your terminal in the project folder and run:
```bash
pip install -r requirements.txt
```
#### 3. Configuration
For security reasons, the `config.py` file containing sensitive API keys is not included in this repository. 

To run the application with AI features:
1. Create a file named `config.py` in the root directory.
2. Add your OpenAI API key to the file in the following format:
   ```python
   OPENAI_API_KEY = "your-actual-api-key-here"
   
#### 4. Technical Note: Database Integrity
The system utilizes the MySQL AUTO_INCREMENT feature for Primary Keys (IDs).
This ensures each book has a unique identifier, which is critical for maintaining consistent data integrity.

Note: In the provided books.sql, IDs may not be perfectly sequential (e.g., gaps after deletions during testing). This is standard database behavior to ensure that a unique ID is never reused for a different record.
