# sharpeVision

A comprehensive stock market dashboard that aggregates data from multiple sources (EDGAR, Polygon, YFinance) to provide fundamental and technical analysis insights. Think of it as a "Roaring Kitty Google Sheet" but as a web application.

## Prerequisites

- Python 3.9+
- pip
- Web browser
- API keys (coming soon):
  - Polygon.io
  - Other data providers

## Setup

1. Clone the repo

   ```bash
   git clone https://github.com/sharpevision/sharpevision.git
   ```

2. Create a virtual environment

   ```bash
   python3 -m venv sharpeVision
   ```

3. Activate the virtual environment

   ```bash
   source sharpeVision/bin/activate
   ```

4. Install the dependencies

   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables

   ```bash
   export FLASK_APP=app.main
   export FLASK_DEBUG=1  # for development mode
   ```

6. Run the app
   ```bash
   python3 -m flask run
   ```

The application will be available at `http://localhost:5000`

## Project Structure
