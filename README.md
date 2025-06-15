# ✨ Glitter-App: Stock Options Filter for Small Portfolios

<p align="center">
  <img src="https://github.com/user-attachments/assets/7d1fb682-aa80-4f81-99a5-dd83e8205279" alt="Glitter App Banner" width="600"/>
</p>

<p align="center">
  <a href="https://twitter.com/glitteroptions?s=21&t=K2xvwYUI22wW4v2q4JbvMQ"><img src="https://img.shields.io/badge/Twitter-@glitteroptions-1DA1F2?style=flat&logo=twitter"/></a>
  <a href="https://discord.gg/7Xs3CTpH"><img src="https://img.shields.io/badge/Discord-Join%20Community-5865F2?style=flat&logo=discord"/></a>
  <img src="https://img.shields.io/badge/License-MIT-green.svg"/>
  <img src="https://img.shields.io/badge/PRs-Welcome-brightgreen.svg?style=flat-square"/>
</p>

---

## 🚀 Project Pitch

**Glitter-App** is a web application designed for retail investors with portfolios under $1000, making options trading accessible, simple, and data-driven. By leveraging the [Tradier API](https://developer.tradier.com/), users can filter and discover stock options for specific companies, using intuitive filters for price, expiration, and more. Glitter empowers new and budget-conscious traders to make informed decisions without information overload.

---

## ✨ Features

- 🔍 **Options Filtering**: Search by ticker, expiration date, and price range (less than, greater than, or between values).
- 📈 **Real-Time Data**: Fetches live options chains and company info from Tradier API.
- 💸 **Tailored for Small Portfolios**: Focuses on trades suitable for accounts under $1000.
- 🏆 **User-Friendly UI**: Modern, responsive design with clear navigation and helpful tooltips.
- 📊 **Volume & Liquidity Filters**: Only shows options with sufficient open interest and volume.
- 🗂️ **Paginated Results**: Easily browse through filtered options.
- 🤝 **Community & Support**: Join our Discord or follow us on Twitter for updates and help.

---

## 🖼️ Screenshots

<p align="center">
  <img src="https://github.com/user-attachments/assets/7d1fb682-aa80-4f81-99a5-dd83e8205279" alt="Glitter App Screenshot" width="600"/>
</p>

---

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS3, JavaScript, [FontAwesome](https://fontawesome.com/)
- **Database**: SQLite
- **API**: [Tradier API](https://developer.tradier.com/)

---

## ⚡ Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Glitter-App.git
   cd Glitter-App
   ```
2. **Create a virtual environment & activate it:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install django requests
   ```
4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```
6. **Visit:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## 📝 Usage Guide

1. **Home Page**: Learn about the app and its mission.
2. **Start Filtering**: Click the "Start Filtering" button to access the options filter.
3. **Enter Ticker**: Type a stock symbol (e.g., AAPL) and select from suggestions.
4. **Set Filters**: Choose price range and expiration date.
5. **View Results**: Browse the filtered options, sorted by volume and liquidity.
6. **Pagination**: Use navigation to view more results.

---

## 🔗 API Reference

- **Tradier API**: Used for fetching real-time options chains and company data. [API Docs](https://developer.tradier.com/documentation/options/get_option_chains)
- **Endpoints Used**:
  - `/v1/markets/options/chains` (options data)
  - `/v1/markets/lookup` (company info)

---

## 🤝 Contributing

We welcome contributions! To get started:

- Fork this repo
- Create a new branch (`git checkout -b feature/your-feature`)
- Commit your changes (`git commit -am 'Add new feature'`)
- Push to the branch (`git push origin feature/your-feature`)
- Open a Pull Request

For major changes, please open an issue first to discuss what you would like to change.

---

## 🙏 Credits

- **Glitter Team**: [hi@glitterfund.xyz](mailto:hi@glitterfund.xyz)
- **Tradier API** for market data
- [FontAwesome](https://fontawesome.com/) for icons
- Community feedback and support

---

## ⚠️ Disclaimer

> This tool is provided for filtering price to liquidity and in no way provides investment recommendations. Your data is protected with 256-bit SSL encryption and never stored. We take your privacy seriously.

---

<p align="center">
  <b>© 2023 glitter, Inc. All rights reserved.</b>
</p>
