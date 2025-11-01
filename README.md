# Pettry Admin Dashboard

This is a complete frontend application for the **Pettry Admin** dashboard, designed to manage all aspects of a pet products e-commerce shop. It provides a clean, modern, and dark-mode interface for store owners to track sales, manage products, handle customers, and analyze performance.

This project was built using **Vue.js**.

## Getting Started

To get this project running locally on your machine, follow these simple steps.

### Prerequisites

Make sure you have [Node.js](https://nodejs.org/) and `npm` (or `yarn`) installed on your system.

### Installation & Running

1.  **Go to the repository:**
    ```bash
    cd Admin-Frontend
    ```

2.  **Remove node and then Reinstall dependencies:**
    This command will install all the necessary packages and libraries defined in your `package.json` file.
    ```bash
    rm -rf node_modules package-lock.json
    npm install
    ```

3.  **Run the development server:**
    This command will start the local development server (usually at `http://localhost:5173` or a similar port). The app will automatically reload if you change any of the source files.
    ```bash
    npm run dev
    ```

4.  **Open in your browser:**
    Visit `http://localhost:5173` (or the port shown in your terminal) to see the application live.

## Features

This admin panel is divided into several key modules:

* **Authentication**
    * **Login Page:** A secure sign-in page to access the admin panel.

* **Product & Inventory Management**
    * **Products Page:** View a comprehensive table of all products, including their image, name, SKU, price, and stock.
    * **Add New Product:** A dedicated form to add new items with fields for name, SKU, price, stock, description, tags, and image upload.
    * **Filtering:** Easily search and filter the product list by category, pet type, or stock status.
    * **Inventory Page:** Get a quick overview of stock with summary cards for **Total Inventory Value**, **Low Stock Items**, and **Out of Stock** items.

* **Sales & Promotions**
    * **Orders Page:** Shows a table for all orders sorted by date, with options to edit and delete. An **‘Export CSV’ button** allows for easy data export.
    * **Promo Codes Page:** Create, view, edit, and delete promotional codes.
    * **Add New Promo Code:** A form to create new codes with different types, such as 'Percentage' or 'Fixed' discounts.

* **Customer Management**
    * **Customers Page:** Manage customer relationships and view key metrics like **Total Customers**, **Active Customers**, **Total Revenue**, and **Average Order Value**.
    * **Customer Actions:** Block or delete customers from the system.
    * **Export Data:** Includes an **‘Export Customers’** button to download customer data.

* **Analytics**
    * **Product Analysis Page:** A visual dashboard to analyze business performance.
    * **Key Charts:** Includes graphs for **Total Sales**, **Product-wise Sales**, **Number of Orders**, and **Monthly Growth**.

* **Help & Support**
    * **FAQ Page:** A full CRUD (Create, Read,Update, Delete) interface to manage the store's Frequently Asked Questions.
    * **Add New Question:** A form to add new questions and answers to the help center.

