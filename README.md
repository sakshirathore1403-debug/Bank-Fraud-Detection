This project implements a Machine Learning based Fraud Detection System that predicts whether a financial transaction is fraudulent or legitimate. The model analyzes transaction patterns from historical data and identifies suspicious activities that may indicate fraud. This type of system is commanly used in banking, online payments, and financial security platforms.
<br>
<ul><h4>Features of this model</h4>
  <li>Data preprocessing and cleaning</li><br>
  <li>Feature encoding using LabelEncoder</li><br>
  <li>Train-test dataset splitting</li><br>
  <li>Fraud prediction using Random Forest Classifier</li><br>
  <li>Model evaluation using accuracy metrics</li><br>
  <li>Interactive interface using Streamlit</li><br>
  <li>Integration with SQL database</li>
</ul>
<br>
<ul><h4>Tools and Technologies</h4>
  <l>Python</l><br>
  <l>Pandas</l><br>
  <l>Scikit-learn</l><br>
  <l>Streamlit</l><br>
  <l>MySQL</l><br>
</ul>

The project uses Random Forest Classifier for fraud detection. This algorithm is chosen beacause it works well with structured datasets,it reduces overfitting by combining multiple decision trees.it provides better prediction accuracy.
<br>
<ul><h4> Model accuracy : 87%</h4>
<br>
<ul><h4>Installation</h4></ul>
git clone : https://github.com/sakshirathore1403-debug/Bank-Fraud-Detection.git
<br>
cd fraud-detection-model
<br>
pip install -r requirements.txt
<ul><h4>Run the Project</h4></ul>
streamlit run fraud.py
<br>
The application will open in your browser where you can test fraud predictions.
