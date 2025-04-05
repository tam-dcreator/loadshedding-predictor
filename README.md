# Load Shedding Classifier

This project aims to estimate load shedding stages based on electricity data and weather data. The project includes data ingestion, preprocessing, model training, and evaluation.

## Key Metrics

- **Accuracy**: Measures the proportion of correctly predicted load shedding stages.
- **Recall**: Measures the proportion of actual load shedding stages that were correctly identified.
- **F1 Score**: Harmonic mean of precision and recall, providing a balance between the two metrics.
- **False Negatives**: Number of actual load shedding stages that were incorrectly predicted as non-load shedding.

## Installation

1. **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd Load Shedding Classifier
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    - Create a `.env` file in the project root directory.
    - Add your Visual Crossing API key:
      ```
      WEATHER_API=<your_api_key>
      ```

## Usage

1. **Fetch Weather Data**:
    - Run the `model.ipynb` notebook to fetch weather data for a specified city.
    - Example:
      ```python
      from fetch_weather_data import get_data
      get_data(city="Cape Town")
      ```

2. **Estimate Load Shedding Schedule**:
    - Run the `estimate_loadshedding_schedule.ipynb` notebook to process raw electricity data and estimate load shedding stages.
    - The output will be saved to `loadshedding_pred.csv`.

3. **Calculate Accuracy**:
    - Run the `calculate_loadshedding_accuracy.ipynb` notebook to calculate the accuracy, recall, and F1 score of the load shedding classifier.

4. **Validate Data**:
    - Run the `validate_data.py` script to validate the load shedding estimation functions and weather data fetching functions.
    - Example:
      ```bash
      pytest validate_data.py
      ```

## Project Structure

- `fetch_weather_data.py`: Fetches historical weather data from the Visual Crossing API.
- `det_loadshedding.py`: Contains functions to determine load shedding based on power demand and supply data.
- `data_ingestion.py`: Provides utility functions to read CSV files.
- `validate_data.py`: Contains test cases to validate the load shedding estimation and weather data fetching functions.
- `estimate_loadshedding_schedule.ipynb`: Notebook to process raw electricity data and estimate load shedding stages.
- `calculate_loadshedding_accuracy.ipynb`: Notebook to calculate the accuracy, recall, and F1 score of the load shedding classifier.
- `model.ipynb`: Notebook to fetch weather data and merge it with load shedding predictions for model training.

## License

This project is licensed under the MIT License.