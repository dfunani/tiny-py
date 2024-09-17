# Introduction

Tiny-Py is a simple URL shortener application built using Flask. It allows you to shorten long URLs into more manageable and shareable short links.

## Installation

Clone the repository:

```Bash
git clone https://github.com/dfunani/tiny-py.git
```

Install dependencies:

```Bash
pip install -r requirements.txt
```

## Usage

Run the application:

```Bash
python app.py # flask run --reload ALTERNATIVE
```

**Access the web application:** Open your web browser and navigate to *http://localhost:5000*.


## API Endpoints

1. Shorten URL:

 - Method: POST
 - Endpoint: /
 - Data:
   - JSON:

        ```JSON
        {
            "url": "https://www.example.com/long-url"
        }
        ```

    - Form data:

        | Field | Value |
        |---|---|
        | url | https://www.example.com/long-url |

 - Response:
    ```JSON
    {
        "short_url": "https://tiny-py.com/abc"
    }
    ```

Redirect:

Method: GET
Endpoint: /redirect/<short_url>
Example: https://tiny-py.com/abc
Response: Redirects to the original URL.
Caveats
URL Storage: The shortened URLs and their corresponding original URLs are stored in a TinyDB database (urls.json).
Data Format: The data can be submitted either as JSON or form data.
Error Handling: The application should handle errors gracefully, such as invalid URLs or missing data.
Customization
URL Shortening Algorithm: You can customize the algorithm used to generate short URLs.
Database: Consider using a more scalable database like MongoDB or PostgreSQL for larger applications.
Error Handling: Implement more robust error handling and messaging.
Features: Add additional features like custom short codes, analytics, or user accounts.
Contributing
Contributions are welcome! Please feel free to submit pull requests or issues. -->