import os
import httpx
import requests
from flask import Flask, jsonify, request, render_template
from bookDAO import book_dao
import config
from openai import OpenAI


app = Flask(__name__, static_url_path='', static_folder='static')

os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''

client = OpenAI(
    api_key=config.OPENAI_API_KEY,
http_client=httpx.Client(
        proxy="http://proxy.server:3128",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
# Function to get book description from Google Books API as a fallback
def get_google_books_description(title, author):
    print(f"--- DEBUG FALLBACK ---")
    # Cleaning the title for better search results
    clean_title = title.split(':')[0].split('-')[0].strip()
    print(f"SENDING TO GOOGLE: '{clean_title}'")

    try:
        url = f"https://www.googleapis.com/books/v1/volumes?q={clean_title}"
        response = requests.get(url, timeout=5)
        data = response.json()

        if "items" in data:
            # Looking for a description in the search results
            for item in data["items"]:
                volume_info = item.get("volumeInfo", {})
                desc = volume_info.get("description")
                if desc:
                    return desc[:400] + "..."

        return None
    except Exception as e:
        print(f"Error Google Books: {e}")
        return None

# AI Description Generation Route
@app.route('/books/ai/<int:id>', methods=['POST'])
def generate_ai_description(id):
    print(f"--- DEBUG: Generating AI description for ID: {id} ---")
    book = book_dao.find_by_id(id)
    if not book:
        print(f"Book with ID {id} not found.")
        return jsonify({"error": "Book not found"}), 404

    title = str(book.get('Title') or book.get('title', '')).strip()
    author = str(book.get('Author') or book.get('author', '')).strip()

    description = "No description found."
    source = "None"

    try:
        # Attempt 1: AI
        print(f"Requesting AI description for '{title}' by {author}...")
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": f"Short description for {title} by {author}."}],
            model="gpt-4o-mini",
            max_tokens=100
        )
        description = response.choices[0].message.content
        source = "AI"
        print("AI Description received.")
    except Exception as e:
        # Attempt 2: Fallback (Google Books)
        print(f"!!! AI mistake: {e} !!!")
        print("Trying Google Books...")
        internet_desc = get_google_books_description(title, author)
        if internet_desc:
            description = internet_desc
            source = "Google Books"
            print("Google Books description received.")
        else:
            # Final fallback if both AI and Google fail
            description = "Description unavailable."
            source = "Error/None"
            print("Failed to get description from both AI and Google Books.")

    print(f"Sending description to frontend: {description[:30]}...")
    book_dao.update_description(id, description)

    return jsonify({"id": id,"description": description, "source": source})

# Over routes for CRUD operations

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/books', methods=['GET'])
def get_all():
    results = book_dao.get_all()
    return jsonify(results)

@app.route('/books/<int:id>', methods=['GET'])
def get_one(id):
    book = book_dao.get_by_id(id)
    return jsonify(book)

@app.route('/books', methods=['POST'])
def create():
    if not request.json:
        return jsonify({"error": "No data"}), 400
    book = {
        "Title": request.json.get('Title'),
        "Author": request.json.get('Author'),
        "Year": request.json.get('Year'),
        "Price": request.json.get('Price')
    }
    print(f"DEBUG: Received data: {book}")
    new_id = book_dao.create(book)
    book['id'] = new_id
    return jsonify(book), 201

@app.route('/books/<int:id>', methods=['DELETE'])
def delete(id):
    book_dao.delete(id)
    return jsonify({"done": True})

@app.route('/books/<int:id>', methods=['PUT'])
def update(id):
    if not request.json:
        return jsonify({"error": "No data"}), 400
    book_data = {
        "Title": request.json.get('Title'),
        "Author": request.json.get('Author'),
        "Year": request.json.get('Year'),
        "Price": request.json.get('Price')
    }
    book_dao.update(id, book_data)
    return jsonify({"done": True})


if __name__ == "__main__":
    app.run(debug=True)