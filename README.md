# PhonePe-Pulse-Data-Visualization-and-Exploration

Domain: Fintech

Approach
1. Data Extraction:
In this phase, the project initiates with a scripted process to clone the GitHub repository containing PhonePe Pulse data. Utilizing scripting ensures a seamless and automated extraction process. The extracted data is then stored in a structured format, either CSV or JSON, facilitating ease of use in subsequent steps.

2. Data Transformation:
Python, along with the Pandas library, is employed for data manipulation and transformation. This step involves comprehensive data cleaning, addressing missing values, and structuring the dataset to meet the requirements of analysis and visualization. By leveraging Python's powerful data processing capabilities, the dataset is refined and prepared for the next stages.

3. Database Insertion:
Connecting to a MySQL database using the "mysql-connector-python" library, the transformed data is efficiently inserted into the database. Utilizing SQL commands, the data is stored securely, ensuring a streamlined approach for storage and retrieval. This step enhances data management capabilities and supports the scalability of the solution.

4. Dashboard Creation:
The visualization aspect is crafted using Streamlit and Plotly libraries in Python. Plotly's geo-map functions are integrated to provide geographical insights visually. The user interface is designed to be intuitive and user-friendly, featuring dropdown options for users to select different metrics and figures. This ensures an interactive and engaging experience for users exploring the PhonePe Pulse data.

5. Data Retrieval:
Connecting back to the MySQL database with the "mysql-connector-python" library, the project retrieves the stored data into a Pandas dataframe. This dynamic retrieval ensures that the dashboard is consistently updated with the latest information, maintaining its relevance and usefulness over time.

6. Deployment:
Prior to public deployment, the solution undergoes rigorous testing to ensure security, efficiency, and user-friendliness. Thorough testing protocols are implemented to identify and rectify any potential issues. Once validated, the dashboard is deployed for public access, offering a reliable tool for users to explore and gain insights from the PhonePe Pulse data.

# Dataset
- Data Link: [PhonePe Pulse GitHub API](https://api.github.com/repos/PhonePe/pulse)
- Inspired From: [PhonePe Pulse](https://www.phonepe.com/pulse)

This project aims to provide a comprehensive and user-friendly solution for extracting, transforming, and visualizing data from the PhonePe Pulse GitHub repository, offering valuable insights for analysis and decision-making.
# Technologies  covered:
- GitHub Cloning
- Python
- Pandas
- MySQL
- mysql-connector-python
- Streamlit
- Plotly
