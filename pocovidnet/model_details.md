
COVID from POCUS predictor:
- Model can differentiate 3 classes: Pneunomia, Healthy & COVID
- Total number of samples: 300 (220 train, 80 test)
    - COVID: 117 / 55
    - Healthy: 49 / 14
    - Pneunomia: 54 / 11
- Split: @Marion Disdier maybe you can give some details here
- Data sources: @Marion Disdier maybe you can give some details here
- Model: 
    - A deep convolutional neural network
    - Our model is based on VGG16 [K Simonyan, 2014], (>35k citations), a model for object recognition in images 
    - VGG16 is quite big (14M parameters) and wasp retrained on millions of natural images
    - For our task VGG16 is fixed and we only add a few more layers with only 33k trainable parameters for COVID detection
- The model is trained for ~30 min on one single CPU (standard laptop)
- All images are downsampled to RGB images of size  224x224
- We exploit data augmentation strategies to compensate for the small size of the dataset. This was found to significantly improve generalisation capabilities. In particular, we perform rotations of up to 15 degrees as well as horizontal and vertical flips of all images.
- The model performs stochastic gradient descent and optimises cross entropy loss
- Current the model has a high precision as well as recall on COVID 19 samples


```
[INFO] evaluating network...
              precision    recall  f1-score   support
       covid       0.96      0.93      0.94        55
   pneunomia       0.59      0.91      0.71        11
     regular       0.70      0.50      0.58        14
    accuracy                           0.85        80
   macro avg       0.75      0.78      0.75        80
weighted avg       0.86      0.85      0.85        80

```