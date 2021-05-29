# Helmet Detection from real-time traffic videos 

A system that checks whether workers wear safety helmets through CCTVs at construction sites and reflects them to DB in real time.

# Requirements
python=3.6

```
pip install face_recognition
pip install opencv-python
```

# Face Registering
If you are not registered in database, system will ignore detection of your face.
So, you need to register your face before execute run.py
Be careful, '--id' option value must be unique.
```
python face_register.py your_name --id 1
```
After you execute face_register.py, Check about red box around your face.
If there is red box, press 's' button to register your identity into database.

# Run
```
python run.py
```
Red box means that you did not wear helmet, Blue box means that you wearied a helmet.

# If you want to modify DB
```
python DBmanager.py
```
We give you console to manage DB. Check a helplist.
