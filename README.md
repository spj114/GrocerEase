# GrocerEase: Grocery Store Management System

GrocerEase: Simplifying grocery store management with a Python/Flask API. Features product, order, and UOM handling, backed by MySQL, and includes a basic HTML/JS frontend for easy demonstration.

This project was developed as a learning exercise to understand backend development principles, API creation, database interaction with Python, and basic frontend integration.

## ✨ Features

*   **Product Management:**
    *   View all products with details (name, UOM, price).
    *   Add new products to the inventory.
    *   Delete existing products.
*   **Unit of Measure (UOM) Management:**
    *   View all available units of measure.
*   **Order Management:**
    *   Create new customer orders with multiple items.
    *   View a list of all past orders.
*   **RESTful API:** Well-defined API endpoints for all functionalities.
*   **Basic Web UI:** A single-page HTML interface for demonstrating API interactions.

## 🛠️ Technologies & Stack

*   **Backend:**
    *   **Python 3.x**
    *   **Flask:** Micro web framework for building the API.
    *   **MySQL:** Relational database for data storage.
    *   **mysql-connector-python:** Official MySQL driver for Python.
*   **Frontend (Basic Demo UI):**
    *   HTML5
    *   CSS3 (Embedded)
    *   JavaScript (Vanilla JS, Embedded)
*   **Database Interaction:**
    *   DAO (Data Access Object) pattern for modular database logic.
*   **Environment Management:**
    *   Virtual Environments (recommended).
    *   Environment variables for database configuration.

## 📂 Project Structure
```
GrocerEase/
├── .gitignore              # Git ignore rules
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
├── database_schema.sql     # Database schema SQL
├── orders_dao.py           # DAO for orders
├── products_dao.py         # DAO for products
├── server.py               # Main Flask server
├── sql_connection.py       # DB connection module
├── uom_dao.py              # DAO for units of measurement
├── static/
│   ├── style.css           # CSS styles
│   └── script.js           # JS scripts
└── templates/
    └── index.html          # Main HTML template
```


## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   **Python 3.7+:** Download from [python.org](https://www.python.org/downloads/)
*   **MySQL Server:** Download from [mysql.com](https://dev.mysql.com/downloads/mysql/) or use a service like Docker. Ensure the server is running.
*   **Git:** For cloning the repository. Download from [git-scm.com](https://git-scm.com/downloads)
*   **pip:** Python package installer (usually comes with Python).

### Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/spj114/GrocerEase.git
    cd GrocerEase
    ```
    *(Replace `your-username/GrocerEase.git` with your actual repository URL after you create it on GitHub and name it `GrocerEase`.)*

2.  **Create and Activate a Virtual Environment:**
    (Recommended to keep dependencies isolated)
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up the MySQL Database:**
    *   Connect to your MySQL server (e.g., using MySQL Workbench, `mysql` command-line client).
    *   Create a new database. The default expected by the application is `grocery_store`:
        ```sql
        CREATE DATABASE IF NOT EXISTS grocery_store;
        ```
    *   Use the newly created database:
        ```sql
        USE grocery_store;
        ```
    *   Execute the `database_schema.sql` script provided in the project to create tables and seed initial data:
        *   Using MySQL command line: `mysql -u your_mysql_user -p grocery_store < database_schema.sql`
        *   Or, copy-paste the content of `database_schema.sql` into your MySQL client and run it.

5.  **Configure Environment Variables:**
    The application requires environment variables for database connection. Create these in your current terminal session before running the server:

    *   **For Linux/macOS:**
        ```bash
        export DB_USER="your_mysql_username"
        export DB_PASSWORD="your_mysql_password"
        export DB_HOST="127.0.0.1"  # Or your MySQL host if different
        export DB_NAME="grocery_store" # Or your database name if different
        ```
    *   **For Windows (Command Prompt):**
        ```cmd
        set DB_USER="your_mysql_username"
        set DB_PASSWORD="your_mysql_password"
        set DB_HOST="127.0.0.1"
        set DB_NAME="grocery_store"
        ```
    *   **For Windows (PowerShell):**
        ```powershell
        $env:DB_USER="your_mysql_username"
        $env:DB_PASSWORD="your_mysql_password"
        $env:DB_HOST="127.0.0.1"
        $env:DB_NAME="grocery_store"
        ```
    *(Replace `"your_mysql_username"` and `"your_mysql_password"` with your actual MySQL credentials.)*

### Running the Application

1.  **Start the Backend Flask Server:**
    Ensure your virtual environment is activated and environment variables are set.
    ```bash
    python server.py
    ```
    The server will start, typically on `http://localhost:5000` (or `http://0.0.0.0:5000/`). You should see console output indicating it's running.

2.  **Access the Frontend UI:**
    Open the `index.html` file in your web browser. You can usually do this by double-clicking the file in your project directory or using your browser's "File > Open" menu.

## 🔌 API Endpoints

The backend server exposes the following RESTful API endpoints:

| Method | Endpoint         | Description                                   | Request Body (Form Data)                                                                                                | Success Response (JSON)                                  |
| :----- | :--------------- | :-------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------- |
| `GET`  | `/getProducts`   | Retrieve all products                         | -                                                                                                                       | `[{product_id, name, uom_id, price_per_unit, uom_name}, ...]` |
| `GET`  | `/getUOM`        | Retrieve all units of measure                 | -                                                                                                                       | `[{uom_id, uom_name}, ...]`                              |
| `POST` | `/insertProduct` | Add a new product                             | `data` field containing JSON string: `{"name": "str", "uom_id": "int", "price_per_unit": "float"}`                       | `{"product_id": int}` (201 Created)                       |
| `POST` | `/deleteProduct` | Delete a product by its ID                    | `product_id` field: `int`                                                                                               | `{"message": "str", "product_id": "int", "rows_affected": int}` (200 or 404) |
| `GET`  | `/getAllOrders`  | Retrieve all orders                           | -                                                                                                                       | `[{order_id, customer_name, total_cost, datetime}, ...]` |
| `POST` | `/insertOrder`   | Create a new order                            | `data` field containing JSON string: `{"customer_name": "str", "grand_total": "float", "datetime": "YYYY-MM-DD HH:MM:SS", "order_details": [{"product_id": int, "quantity": float, "total_price": float}, ...]}` | `{"order_id": int}` (201 Created)                         |

*Error responses typically include `{"error": "Error type", "message": "Detailed message"}` with appropriate HTTP status codes (400, 404, 500, 503).*

## 💡 Potential Future Enhancements

*   User authentication and authorization.
*   More sophisticated frontend UI (e.g., using a JavaScript framework like React, Vue, or Angular).
*   Dynamic order detail creation in the UI.
*   Endpoint to fetch a single order with its details.
*   Endpoint to update existing products or orders.
*   Inventory stock management.
*   Unit testing and integration testing.
*   Dockerization for easier deployment.

## 🤝 Contributing

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 🙏 Acknowledgements

*   The course/tutorial that inspired this project [CodeBasics](https://codebasics.io/courses/python-project-grocery-store-application/lecture/459).
*   Flask and MySQL communities for excellent documentation and resources.

---
