# Easy Ferry

Easy Ferry is a web application that helps you manage your ferry business. It allows you to manage your sales, customers, and reports.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them:

```
- Python 3.11
- pip
- virtualenv
```

### Installing

A step by step series of examples that tell you how to get a development env running:

1. **Clone the repo:**
   ```sh
   git clone https://github.com/your_username/easy-ferry.git
   ```
2. **Create a virtual environment:**
   ```sh
   python -m venv venv
   ```
3. **Activate the virtual environment:**
   - On Windows:
     ```sh
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```sh
     source venv/bin/activate
     ```
4. **Install the dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
5. **Run the development server:**
   ```sh
   python manage.py runserver
   ```

The application will be available at `http://127.0.0.1:8000/`.

## Project Structure

The project is divided into the following apps:

- **account**: Handles user accounts and notifications.
- **authentication**: Handles user authentication, including login, registration, and token management.
- **registration**: Handles the registration process, including token generation and validation.
- **reports**: Handles the generation of reports, including sales reports and marine reports.
- **tracking**: Handles the tracking of ferries.

## API Documentation

### Account App

- **`business_notifications(request)`**:
  - **Description**: Retrieves all notifications for a given business.
  - **Method**: `GET`
  - **URL**: `/account/notifications/`
  - **Parameters**: `business`
  - **Returns**: A JSON object containing a list of notifications.

- **`mark_read_notification(request)`**:
  - **Description**: Marks a notification as read.
  - **Method**: `POST`
  - **URL**: `/account/notifications/mark-read/`
  - **Body**: `{"notification_id": 1}`
  - **Returns**: A JSON object with a success message.

### Authentication App

- **`login(request)`**:
  - **Description**: Authenticates a user and returns a token.
  - **Method**: `POST`
  - **URL**: `/auth/login/`
  - **Body**: `{"email": "user@example.com", "password": "password"}`
  - **Returns**: A JSON object with the user's data and a token.

- **`register_user(request)`**:
  - **Description**: Registers a new user.
  - **Method**: `POST`
  - **URL**: `/auth/register/`
  - **Body**: `{"first_name": "John", "last_name": "Doe", "email": "user@example.com", "password": "password", "business_id": 1}`
  - **Returns**: A JSON object with a success message and the new user's ID.

- **`refresh_token(request)`**:
  - **Description**: Refreshes a user's token.
  - **Method**: `POST`
  - **URL**: `/auth/refresh-token/`
  - **Body**: `{"token": "your_token"}`
  - **Returns**: A JSON object with a new refresh token.

### Registration App

- **`request_registration_token(request)`**:
  - **Description**: Requests a registration token for a given email.
  - **Method**: `POST`
  - **URL**: `/registration/request-token/`
  - **Body**: `{"email": "user@example.com"}`
  - **Returns**: A JSON object with a success message.

- **`validate_registration_token(request)`**:
  - **Description**: Validates a registration token.
  - **Method**: `GET`
  - **URL**: `/registration/validate-token/`
  - **Parameters**: `token`
  - **Returns**: A JSON object with a boolean indicating if the token is valid and the email associated with the token.

- **`use_token(request)`**:
  - **Description**: Marks a registration token as used.
  - **Method**: `POST`
  - **URL**: `/registration/use-token/`
  - **Body**: `{"token": "your_token"}`
  - **Returns**: A JSON object with a success message.

- **`get_token_mail(request)`**:
  - **Description**: Retrieves the email associated with a registration token.
  - **Method**: `GET`
  - **URL**: `/registration/get-email/`
  - **Parameters**: `token`
  - **Returns**: A JSON object with the email associated with the token.

### Reports App

- **`save_data(request)`**:
  - **Description**: Saves or updates a sale.
  - **Method**: `POST` or `PUT`
  - **URL**: `/reports/save-data/`
  - **Body**: A JSON object with the sale data.
  - **Returns**: A JSON object with the ID of the created sale or a success message.

- **`save_multiple_data(request)`**:
  - **Description**: Saves multiple sales.
  - **Method**: `POST`
  - **URL**: `/reports/save-multiple-data/`
  - **Body**: A list of JSON objects with the sale data.
  - **Returns**: A JSON object with the IDs of the created sales.

- **`generate_marine_report(request)`**:
  - **Description**: Generates a marine report.
  - **Method**: `POST`
  - **URL**: `/reports/generate-marine-report/`
  - **Body**: `{"business": "business_name", "time": "10:00", "date": "2023-01-01"}`
  - **Returns**: An Excel file with the marine report.

- **`get_sells_data(request)`**:
  - **Description**: Retrieves sales data for a given business and date range.
  - **Method**: `GET`
  - **URL**: `/reports/get-sells-data/`
  - **Parameters**: `business`, `start_date`, `end_date`
  - **Returns**: A JSON object with the sales data.

- **`get_sells_ferry(request)`**:
  - **Description**: Retrieves sales data for a given business, date range, and ferry.
  - **Method**: `GET`
  - **URL**: `/reports/get-sells-ferry/`
  - **Parameters**: `business`, `start_date`, `end_date`
  - **Returns**: A JSON object with the sales data.

- **`delete_sales(request)`**:
  - **Description**: Deletes multiple sales.
  - **Method**: `POST`
  - **URL**: `/reports/delete-sales/`
  - **Body**: `{"ids": [1, 2, 3]}`
  - **Returns**: A JSON object with the number of deleted sales.

- **`update_sale(request)`**:
  - **Description**: Updates a sale.
  - **Method**: `POST`
  - **URL**: `/reports/update-sale/`
  - **Body**: A JSON object with the sale data to update.
  - **Returns**: A JSON object with a success message.

- **`get_owner(request)`**:
  - **Description**: Retrieves the owner of a business.
  - **Method**: `GET`
  - **URL**: `/reports/get-owner/`
  - **Parameters**: `business`
  - **Returns**: A JSON object with the owner's data.

- **`update_owner(request)`**:
  - **Description**: Updates the owner of a business.
  - **Method**: `POST`
  - **URL**: `/reports/update-owner/`
  - **Body**: A JSON object with the owner's data to update.
  - **Returns**: A JSON object with the updated owner's data.

- **`get_crew(request)`**:
  - **Description**: Retrieves the crew of a business.
  - **Method**: `GET`
  - **URL**: `/reports/get-crew/`
  - **Parameters**: `business`
  - **Returns**: A JSON object with the crew's data.

- **`update_crew(request)`**:
  - **Description**: Updates the crew of a business.
  - **Method**: `POST`
  - **URL**: `/reports/update-crew/`
  - **Body**: A JSON object with the crew's data to update.
  - **Returns**: A JSON object with the updated crew's data.

- **`get_sales_by_business(request)`**:
  - **Description**: Retrieves all sales for a given business.
  - **Method**: `GET`
  - **URL**: `/reports/get-sales-by-business/`
  - **Parameters**: `business`, `format` (optional, can be `xlsx`, `csv`, or `json`)
  - **Returns**: A file in the specified format or a JSON object with the sales data.

- **`mark_as_paid(request)`**:
  - **Description**: Marks multiple sales as paid.
  - **Method**: `POST`
  - **URL**: `/reports/mark-as-paid/`
  - **Body**: `{"ids": [1, 2, 3]}`
  - **Returns**: A JSON object with the number of updated sales.

- **`get_ferry(request)`**:
  - **Description**: Retrieves all ferries for a given business.
  - **Method**: `GET`
  - **URL**: `/reports/get-ferry/`
  - **Parameters**: `business`
  - **Returns**: A JSON object with a list of ferries.

### Tracking App

- **`get_coordinates(request)`**:
  - **Description**: Retrieves the coordinates of a ferry for a given business.
  - **Method**: `GET`
  - **URL**: `/tracking/get-coordinates/`
  - **Parameters**: `business`
  - **Returns**: A JSON object with a list of coordinates.

- **`save_coordinates(request)`**:
  - **Description**: Saves the coordinates of a ferry.
  - **Method**: `GET`
  - **URL**: `/tracking/save-coordinates/`
  - **Parameters**: `lat`, `long`, `business`
  - **Returns**: A JSON object with a success message.
