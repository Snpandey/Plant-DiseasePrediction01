import streamlit as st
from fpdf import FPDF
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import time

# Set page configuration
st.set_page_config(page_title="UAV-Based Real-Time Plant Disease Detection", layout="wide")
col1, col2, col3 = st.columns([20, 25, 1])
with col2:
    st.image("logo_0.png", width=150)

# Load model
model = tf.keras.models.load_model('trained_model.keras')

# Load classification report data (Replace with your actual data)
classification_report_data = {
    'Apple___Apple_scab': {'precision': 0.91, 'recall': 0.98, 'f1-score': 0.95},
    'Apple___Black_rot': {'precision': 0.96, 'recall': 0.99, 'f1-score': 0.98},
    'Apple___Cedar_apple_rust': {'precision': 0.98, 'recall': 0.96, 'f1-score': 0.97},
    'Apple___healthy': {'precision': 0.97, 'recall': 0.97, 'f1-score': 0.97},
    'Blueberry___healthy': {'precision': 0.95, 'recall': 0.98, 'f1-score': 0.97},
    'Cherry_(including_sour)___Powdery_mildew': {'precision': 1.00, 'recall': 0.98, 'f1-score': 0.99},
    'Cherry_(including_sour)___healthy': {'precision': 0.98, 'recall': 0.99, 'f1-score': 0.99},
    'Corn_(maize)___Cercospora_leaf_spot_Gray_leaf_spot': {'precision': 0.94, 'recall': 0.92, 'f1-score': 0.93},
    'Corn_(maize)___Common_rust': {'precision': 0.99, 'recall': 0.98, 'f1-score': 0.99},
    'Corn_(maize)___Northern_Leaf_Blight': {'precision': 0.95, 'recall': 0.95, 'f1-score': 0.95},
    'Corn_(maize)___healthy': {'precision': 0.99, 'recall': 1.00, 'f1-score': 0.99},
    'Grape___Black_rot': {'precision': 0.95, 'recall': 1.00, 'f1-score': 0.97},
    'Grape___Esca_(Black_Measles)': {'precision': 1.00, 'recall': 0.97, 'f1-score': 0.98},
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': {'precision': 1.00, 'recall': 0.99, 'f1-score': 0.99},
    'Grape___healthy': {'precision': 0.99, 'recall': 1.00, 'f1-score': 1.00},
    'Orange___Haunglongbing_(Citrus_greening)': {'precision': 0.99, 'recall': 0.99, 'f1-score': 0.99},
    'Peach___Bacterial_spot': {'precision': 0.97, 'recall': 0.95, 'f1-score': 0.96},
    'Peach___healthy': {'precision': 0.98, 'recall': 1.00, 'f1-score': 0.99},
    'Pepper,_bell___Bacterial_spot': {'precision': 0.96, 'recall': 0.97, 'f1-score': 0.97},
    'Pepper,_bell___healthy': {'precision': 0.98, 'recall': 0.97, 'f1-score': 0.97},
    'Potato___Early_blight': {'precision': 0.98, 'recall': 0.97, 'f1-score': 0.98},
    'Potato___Late_blight': {'precision': 0.96, 'recall': 0.97, 'f1-score': 0.96},
    'Potato___healthy': {'precision': 0.96, 'recall': 0.97, 'f1-score': 0.97},
    'Tomato___healthy': {'precision': 0.98, 'recall': 1.00, 'f1-score': 0.99},
    'Tomato___Bacterial_spot' : {'precision': 0.99, 'recall': 0.96, 'f1-score': 0.97},     
    'Tomato___Early_blight ' :  {'precision':0.89 , 'recall': 0.91, 'f1-score':0.90},
    'Tomato___Late_blight' :  {'precision':0.98 , 'recall':   0.86 , 'f1-score': 0.92}, 
    'Tomato___Leaf_Mold' :  {'precision':1.00 ,'recall':0.93,'f1-score':0.96},
    'Tomato___Septoria_leaf_spot' :{'precision':0.93,'recall':0.88,'f1-score':0.90},       
    'Tomato___Spider_mites Two-spotted_spider_mite':{'precision':0.97,'recall': 0.95,'f1-score':0.96},      
    'Tomato___Target_Spot' : {'precision':0.91,'recall':0.93,'f1-score':0.92},
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus' : {'precision':0.98,'recall':0.98,'f1-score':0.98},       
    'Tomato___Tomato_mosaic_virus' : {'precision':0.98,'recall':0.99,'f1-score': 0.99},
    'Strawberry___Leaf_scorch' : {'precision':0.94,'recall':0.98,'f1-score':0.96},       
    'Strawberry___healthy' : {'precision':0.98 ,'recall': 0.98, 'f1-score':0.98},
    'Raspberry___healthy' :  {'precision':0.95,'recall': 1.00 ,'f1-score':0.98},
    'Soybean___healthy' :  {'precision':0.97 ,'recall': 0.99 ,'f1-score':0.98},
    'Squash___Powdery_mildew' : {'precision':0.96,'recall':1.00,'f1-score':0.98}        


}

# Set background color and styles
st.markdown("""
<style>
body {
    background-color: #e6f3ff;
}
header, .css-1v3fvcr, footer {
    background-color: #e6f3ff;
}
.css-1d391kg {
    padding-top: 2rem;
}
.css-12oz5g7 {
    font-size: 1.5rem;
    color: #0066FF;
}
.css-1qpc1ke {
    color: #0066FF;
}
.css-1dp5vir, .css-184tjsw {
    text-align: center;
}
.css-1vd0sfs {
    font-weight: bold;
    font-family: Algerian;
    text-decoration: underline;
}
.metrics-box {
    font-size: 3rem;
    font-weight: bold;
    color: #000;
    background-color: #e6f3ff;
    border-radius: 5px;
    padding: 10px;
    margin-top: 10px;
    text-align: center;
}
.metrics-box .precision {
    color: #ff0000;
}
.metrics-box .recall {
    color: #ff9900;
}
.metrics-box .f1-score {
    color: #009900;
}
.disease-box .disease_name {
    color: green;           
}
</style>
""", unsafe_allow_html=True)

# Add logo to the sidebar
st.sidebar.image("logo_0.png", width=120)
# Main header with centered logo and title
st.markdown("<h1 style='text-align: center;color:blue; font-family:algerian'>JAYPEE INSTITUTE OF INFORMATION TECHNOLOGY (JIIT)</h1>", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("Navigation")
st.sidebar.markdown(
    """
    <style>
    .sidebar .radio-label {
        font-size: 30px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
page = st.sidebar.radio("Go to", ["Home", "About", "Disease Recognition", "Train"])

# Class names for the plant diseases
class_names = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy', 'Blueberry___healthy',
               'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot_Gray_leaf_spot',
               'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot',
               'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)',
               'Peach___Bacterial_spot', 'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight',
               'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew',
               'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight',
               'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites_Two-spotted_spider_mite', 'Tomato___Target_Spot',
               'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy']

# Function to display model performance metrics
def display_metrics(disease_name=None):
    if disease_name and disease_name in classification_report_data:
        metrics = classification_report_data[disease_name]
        st.sidebar.subheader(f"Metrics for {disease_name}")
        st.sidebar.markdown("<h2 style='font-size:40px;'>KFCL Project</h2>", unsafe_allow_html=True)
        st.sidebar.markdown("<h3 style='font-size:20px;'>Developer: Saurabh Nirala Pandey</h3>", unsafe_allow_html=True)
        st.sidebar.markdown("<h3 style='font-size:20px;'>Contact: 9155028187</h3>", unsafe_allow_html=True)
        st.sidebar.markdown("<h3 style='font-size:20px;'>Email: pandeysaurabhnirala@gmail.com</h3>", unsafe_allow_html=True)

        st.sidebar.markdown(f"""
        <div class="metrics-box">
            <div class="precision">Precision: {metrics['precision'] * 100:.2f}%</div>
            <div class="recall">Recall: {metrics['recall'] * 100:.2f}%</div>
            <div class="f1-score">F1 Score: {metrics['f1-score'] * 100:.2f}%</div>
            <h2 style='color: #4CAF50;font-size: 45px; font-weight: bold;'> Accuracy: 97%</h2>      
        </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.subheader("Model Performance Metrics")
        st.sidebar.write("Please upload an image and run the prediction to see specific metrics.")
        st.sidebar.text("KFCL")
        st.sidebar.text("Developer:-Saurabh Nirala Pandey")
        st.sidebar.text("Contact:-9155028187")
        st.sidebar.text("Email:-pandeysaurabhnirala@gmail.com")
        

# Tensorflow Model Prediction
def model_prediction(test_image):
    image = load_img(test_image, target_size=(128, 128))
    input_arr = img_to_array(image)
    input_arr = np.array([input_arr])  # Convert Single Image to a batch
    prediction = model.predict(input_arr)
    result_index = np.argmax(prediction)
    return result_index

# Function to create the PDF health card
def create_health_card(result_index):
    disease_name = class_names[result_index]
    metrics = classification_report_data[disease_name]

    # Create instance of FPDF class
   #  pdf = FPDF()
   #  pdf.add_page()
   #  pdf.set_font("Arial", size=12)

   #  # Add content to the PDF
   #  pdf.cell(200, 10, txt="Plant Health Card", ln=True, align='C')
   #  pdf.cell(200, 10, txt=f"Predicted Disease: {disease_name}", ln=True)
   #  pdf.cell(200, 10, txt=f"Precision: {metrics['precision'] * 100:.2f}%", ln=True)
   #  pdf.cell(200, 10, txt=f"Recall: {metrics['recall'] * 100:.2f}%", ln=True)
   #  pdf.cell(200, 10, txt=f"F1 Score: {metrics['f1-score'] * 100:.2f}%", ln=True)
   # Create instance of FPDF class
    pdf = FPDF()

# Add a page
    pdf.add_page()

# Set title font and color for the main heading
    pdf.set_font("Arial", size=20)
    pdf.set_text_color(0, 0, 128)  # Dark blue color for the main heading
    pdf.cell(200, 20, txt="Plant Disease Detection Mechanism", ln=True, align='C')

# Subtitle
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 102, 204)  # Blue color for the subtitle
    pdf.multi_cell(0, 10, txt="Developed By JIIT\nUnder the Guidance of Prof. Richa Gupta And Dr. Gaurav Verma\nJRF - Saurabh Nirala Pandey", align='C')

# Add a border around the entire page
    pdf.set_fill_color(240, 240, 240)  # Light grey background
    pdf.rect(5, 5, 200, 287, 'DF')  # Rectangle around the page (x, y, w, h, style)

# Set content font and color
    pdf.set_font("Arial", size=14)
    pdf.set_text_color(50, 50, 50)  # Dark grey color for the text

# Set fill color for the content background
    pdf.set_fill_color(255, 255, 255)  # White background for content

# Predicted Disease
    pdf.set_text_color(0, 153, 76)  # Green color for disease name
    pdf.cell(0, 10, txt=f"Predicted Disease: {disease_name}", ln=True, align='C', fill=True)

# Precision
    pdf.set_text_color(255, 102, 102)  # Red color for precision
    pdf.cell(0, 10, txt=f"Precision: {metrics['precision'] * 100:.2f}%", ln=True, align='C', fill=True)

# Recall
    pdf.set_text_color(102, 178, 255)  # Light blue color for recall
    pdf.cell(0, 10, txt=f"Recall: {metrics['recall'] * 100:.2f}%", ln=True, align='C', fill=True)

# F1 Score
    pdf.set_text_color(255, 178, 102)  # Orange color for F1 Score
    pdf.cell(0, 10, txt=f"F1 Score: {metrics['f1-score'] * 100:.2f}%", ln=True, align='C', fill=True)

# Add footer section
    pdf.set_y(-30)  # Move to 30 mm from bottom
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0, 0, 128)  # Dark blue color for footer
    pdf.multi_cell(0, 10, txt="Contact us:\nEmail: pandeysaurabhnirala@gmail.com\nMobile: 9155028187\nFeel free to contact", align='C')

# Copyright notice
    pdf.set_y(-15)  # Move to 15 mm from bottom
    pdf.set_font("Arial", size=8)
    pdf.set_text_color(128, 128, 128)  # Grey color for copyright
    pdf.cell(0, 10, txt="© All rights reserved by the developer.", ln=True, align='C')

# Output the PDF
    pdf.output("plant_health_card.pdf")

    # Save the PDF
    pdf_filename = f"health_card_{int(time.time())}.pdf"
    pdf.output(pdf_filename)

    return pdf_filename

# Navigation Pages
if page == "Home":
    st.header("Development Of UAV-Based Real Time Plant Disease Detection Mechanism")
    st.subheader("Developed by JRF Saurabh Nirala Pandey Jaypee Institute of Information Technology (JIIT)")
    st.subheader("Under the guidance of Dr. Gaurav Verma and Prof. Richa Gupta")
    st.image("Drone_img.webp", use_column_width=True)
    st.markdown("""
    Welcome to My UAV-Based Real Time Plant Disease Detection Mechanism Website! 🌿🔍
    
    Our mission is to help in identifying plant diseases efficiently. Upload an image of a plant, and our system will 
    analyze it to detect any signs of diseases. Together, let's protect our crops and ensure a healthier harvest!

    ### How It Works
    1. **Upload Image:** Go to the **Disease Recognition** page and upload an image of a plant with suspected diseases.
    2. **Analysis:** Our system will process the image using advanced algorithms to identify potential diseases.
    3. **Results:** View the results and recommendations for further action.

    ### Why Choose Us?
    - **Accuracy:** Our system utilizes state-of-the-art machine learning techniques for accurate disease detection.
    - **User-Friendly:** Simple and intuitive interface for seamless user experience.
    - **Fast and Efficient:** Receive results in seconds, allowing for quick decision-making.

    ### Get Started
    Click on the **Disease Recognition** page in the sidebar to upload an image and experience the power of our Plant 
    Disease Recognition System!
    ### About Us
    Learn more about the project, our team, and our goals on the **About** page.
    """)


elif page == "About":
    st.header("About")
    st.markdown("""
    ### Project Overview
    The "Development of UAV-Based Real-Time Plant Disease Detection Mechanism" project aims to leverage UAV technology 
    and machine learning to detect diseases in plants in real-time. By capturing high-resolution images of crops and 
    analyzing them using advanced algorithms, the system can identify signs of diseases early, allowing farmers to take 
    timely actions to protect their crops and optimize yields.

    #### Content
    - **Dataset:** The dataset consists of images of various plant diseases and healthy plants across different crop types.
    - **Machine Learning Models:** The system utilizes convolutional neural networks (CNNs) and other deep learning 
      architectures for disease detection.
    - **Applications:** The project has applications in agriculture, enabling farmers to monitor crop health more 
      efficiently and make informed decisions to enhance productivity.
    - **Impact:** By preventing the spread of diseases and minimizing crop losses, the system contributes to food 
      security and sustainable agriculture practices.

    ### Future Scope
    - **Advanced Machine Learning Models:** Implementing more sophisticated models to improve disease detection accuracy.
    - **Integration with Agricultural Practices:** Integrating the system with agricultural practices and management 
      systems for broader adoption.
    - **Real-Time Monitoring:** Enhancing real-time monitoring capabilities using UAVs and IoT devices.

    #### Team
    - **Developers:** JRF Saurabh Nirala Pandey and  Dr. Gaurav Verma & Dr. Richa Gupta from Jaypee Institute of Information Technology (JIIT).
    - **Project Advisors:** Dr. Gaurav Verma and Prof.Richa Gupta.

    #### Acknowledgments
    We acknowledge the support and guidance provided by our mentors and the JIIT community in the development of this 
    innovative project.
    """)

elif page == "Disease Recognition":
    st.title("Disease Recognition")
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=False, width=300)
        st.write("Classifying...")
        result_index = model_prediction(uploaded_file)
        disease_name = class_names[result_index]
        st.success(f'Prediction: {disease_name}')

        # Display metrics for the predicted disease
        display_metrics(disease_name)

        # Create and display health card PDF
        pdf_filename = create_health_card(result_index)
        with open(pdf_filename, "rb") as file:
            btn = st.download_button(
                label="Download Health Card",
                data=file,
                file_name=pdf_filename,
                mime="application/octet-stream"
            )
    else:
        display_metrics()

elif page == "Train":
    st.title("Train")
    st.write("""
    The 'Train' section is where we delve into the machine learning models used for disease detection. Here, we provide insights into the training process, data preprocessing, and model architecture. Currently, this section is under development. Stay tuned for updates!
    """)
