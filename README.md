# 🚀 Crypto Currency Price Web App 📈

An interactive web application built with Python and Streamlit to visualize and analyze live and historical cryptocurrency data.

**🔴 Live Demo Link:** [https://crypto-web-app-zc8gfcarbkzljpspgcrhb3.streamlit.app/](https://crypto-web-app-zc8gfcarbkzljpspgcrhb3.streamlit.app/)

---

## 📖 About The Project

* **Objective:** To develop a hands-on data science project creating a functional and user-friendly dashboard.
* **Data Integration:** The app integrates real-time data from a professional API (CoinMarketCap) and historical data from a financial data provider (Yahoo Finance).
* **Core Goal:** To build a complete application from development and debugging to final deployment and documentation, showcasing a full project lifecycle.

---

## 📝 Project Overview

The Crypto Web App provides a feature-rich and intuitive interface for exploring the cryptocurrency market. Upon launching, the user is greeted with an interactive sidebar that serves as the main control panel. From here, users can select their preferred currency (USD or BTC) and choose multiple cryptocurrencies from the top 100 for detailed analysis.

The main dashboard is organized into a clean 2x2 grid of dynamic visualizations:
* **Top-Left Chart:** Bar plots of percentage price change, allowing users to quickly identify the biggest movers over various timeframes (1h, 24h, 7d).
* **Top-Right Chart:** A comparison of the absolute market capitalizations of the selected cryptocurrencies.
* **Bottom-Left Pie Chart:** An illustration of the market dominance of Bitcoin and Ethereum relative to the rest of the top 100 coins.
* **Bottom-Right Line Chart:** A display of the 30-day historical closing price for any single cryptocurrency selected from a dropdown menu.

Below the charts, two detailed data tables provide the raw numbers for price information and percentage changes. A "Download CSV" link allows users to export the selected data for their own offline analysis.

---

## 🛠️ Technologies Used

* **Language:** Python
* **Web Framework:** Streamlit
* **Data & Analysis:** Pandas, Matplotlib
* **APIs & Data:** CoinMarketCap API, yfinance
* **Environment:** python-dotenv

---

## 📂 Project Structure

* `Crypto-Web-app/`
    * `.venv/`: Virtual environment directory.
    * `.env`: File for storing the secret API key (not in git).
    * `.gitignore`: Specifies files for Git to ignore.
    * `crypto_price_app.py`: The main Python script for the Streamlit app.
    * `logo.jpg`: Logo image for the application.
    * `requirements.txt`: Lists the required Python libraries.

---

## ⚙️ How to Run

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Sachin18022006/Crypto-Web-app.git](https://github.com/Sachin18022006/Crypto-Web-app.git)
    cd Crypto-Web-app
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    # On Windows: .venv\Scripts\activate
    ```
3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Create a `.env` file** and add your CoinMarketCap API key:
    ```
    CMC_API_KEY="YOUR_API_KEY_HERE"
    ```
5.  **Run the Streamlit app:**
    ```bash
    streamlit run crypto_price_app.py
    ```

---

## 💡 Insights and Learnings

* **API vs. Web Scraping:** This project provided a crucial, practical lesson on the difference between data acquisition methods. Early attempts using web scraping were fragile and frequently broke. Transitioning to dedicated APIs (CoinMarketCap and yfinance) resulted in a far more stable and reliable application.
* **Environment Management:** Understood the importance of virtual environments (`.venv`) and dependency files (`requirements.txt`) for project reproducibility, ensuring that any developer can set up the exact same environment.
* **Data Handling:** Gained practical experience in fetching, cleaning, and structuring nested JSON data from real-world APIs using the Pandas library.

---

## 🚀 Future Improvements

* **User Authentication:** Add accounts to save favorite cryptocurrencies.
* **Advanced Charting:** Implement technical analysis charts like Moving Averages or RSI.
* **Custom Date Range:** Allow users to select a custom date range for historical data.
* **Alerts System:** Add a feature to set up price alerts and notifications.
