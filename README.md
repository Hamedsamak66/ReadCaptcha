CAPTCHA Recognition in Persian using CNN
Welcome to the CAPTCHA Recognition project repository. This project focuses on developing a Convolutional Neural Network (CNN) to identify Persian numerals in CAPTCHA images, even with complex backgrounds and distortions.

Overview
This algorithm attempts to accurately read Persian numerals from CAPTCHA images with varying colors, patterns, and overlays such as random lines and the addition operator (+).

Features
Process Persian CAPTCHA images
Recognize digits from 0 to 9
Utilize a CNN model for image classification
Achieved an accuracy rate of 82%
Dataset
Contains 6,000 images of Persian numerals extracted from CAPTCHA images.
The dataset was divided into training and testing sets.
Usage
Clone the Repository:

bash
git clone https://github.com/Hamedsamak66/ReadCaptcha
Install Requirements:

bash
pip install -r requirements.txt
Train the Model: Use your preferred training script or tool to start training the model with the dataset provided.

Run the Algorithm: You can test the trained model on new CAPTCHA samples using the provided predict.py script.

File Structure
dataset/: Contains the CAPTCHA images used for training and testing.
models/: Pre-trained models and saved checkpoints.
scripts/: Python scripts for training, testing, and data preprocessing.
README.md: Project overview and instructions.
Getting Started
The README provides details on setting up and using the project. For further details on implementation, refer to the scripts and comments in the code.

Contributions
Contributions are welcome! Please create an issue to discuss your ideas or open a pull request with improvements.

License
This project is licensed under the MIT License. See the LICENSE file for more details.

Contact
For any questions or suggestions, feel free to contact me at samak.h@outlook.com.