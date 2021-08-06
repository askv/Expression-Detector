import matplotlib.pyplot as plt
import os
import cv2
import glob
import pandas
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Dense, Dropout, Flatten, Conv2D, BatchNormalization, Activation, MaxPooling2D
from keras.models import Sequential
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint

dir="C:/Users/Deeksha/Datasets/Expressions"  #path to the folder
categories=["Angry", "Fear", "Happy", "Neutral", "Sad"]

#Reading angry images
path=os.path.join(dir,categories[0])
angry=glob.glob(path+"/*")
print("No. of images in angry="+str(len(angry)))
print(angry[0])
k=os.path.join(str(angry[0].split("\\")[0]),str(angry[0].split("\\")[1]))
print(k)
k=str(angry[0].split("\\")[2])
print(k)

angry_folder=[str(os.path.join(str(i.split("\\")[0]),str(i.split("\\")[1]))) for i in angry]
angry_image=[str(i.split("\\")[2]) for i in angry]
angry_emotion="Angry"
angry_label=[1]*len(angry)

df_angry=pandas.DataFrame()
df_angry["Folder"]=angry_folder
df_angry["Image"]=angry_image
df_angry["Emotion"]=angry_emotion
df_angry["Label"]=angry_label
print(df_angry)


#Reading fear images
path=os.path.join(dir,categories[1])
fear=glob.glob(path+"/*")
print("No. of images in fear="+str(len(fear)))
print(fear[0])
k=os.path.join(str(fear[0].split("\\")[0]),str(fear[0].split("\\")[1]))
print(k)
k=str(fear[0].split("\\")[2])
print(k)

fear_folder=[str(os.path.join(str(i.split("\\")[0]),str(i.split("\\")[1]))) for i in fear]
fear_image=[str(i.split("\\")[2]) for i in fear]
fear_emotion="Fear"
fear_label=[2]*len(fear)

df_fear=pandas.DataFrame()
df_fear["Folder"]=fear_folder
df_fear["Image"]=fear_image
df_fear["Emotion"]=fear_emotion
df_fear["Label"]=fear_label
print(df_fear)

#Reading happy images
path = os.path.join(dir,categories[2])
happy = glob.glob(path+"/*")
print("No. of images in happy="+str(len(happy)))
print(happy[0])
k = os.path.join(str(happy[0].split("\\")[0]),str(happy[0].split("\\")[1]))
print(k)
k = str(happy[0].split("\\")[2])
print(k)

happy_folder = [str(os.path.join(str(i.split("\\")[0]),str(i.split("\\")[1]))) for i in happy]
happy_image = [str(i.split("\\")[2]) for i in happy]
happy_emotion = "Happy"
happy_label = [3]*len(happy)

df_happy = pandas.DataFrame()
df_happy["Folder"] = happy_folder
df_happy["Image"] = happy_image
df_happy["Emotion"] = happy_emotion
df_happy["Label"] = happy_label
print(df_happy)

#Reading neutral images
path = os.path.join(dir,categories[3])
neutral = glob.glob(path+"/*")
print("No. of images in neutral="+str(len(neutral)))
print(neutral[0])
k = os.path.join(str(neutral[0].split("\\")[0]),str(neutral[0].split("\\")[1]))
print(k)
k = str(neutral[0].split("\\")[2])
print(k)

neutral_folder = [str(os.path.join(str(i.split("\\")[0]),str(i.split("\\")[1]))) for i in neutral]
neutral_image = [str(i.split("\\")[2]) for i in neutral]
neutral_emotion = "Neutral"
neutral_label = [4]*len(neutral)

df_neutral = pandas.DataFrame()
df_neutral["Folder"] = neutral_folder
df_neutral["Image"] = neutral_image
df_neutral["Emotion"] = neutral_emotion
df_neutral["Label"] = neutral_label
print(df_neutral)

#Reading sad images
path = os.path.join(dir, categories[4])
sad = glob.glob(path+"/*")
print("No. of images in sad="+str(len(sad)))
print(sad[0])
k = os.path.join(str(sad[0].split("\\")[0]),str(sad[0].split("\\")[1]))
print(k)
k = str(sad[0].split("\\")[2])
print(k)

sad_folder = [str(os.path.join(str(i.split("\\")[0]),str(i.split("\\")[1]))) for i in sad]
sad_image = [str(i.split("\\")[2]) for i in sad]
sad_emotion = "Sad"
sad_label = [5]*len(sad)

df_sad = pandas.DataFrame()
df_sad["Folder"] = sad_folder
df_sad["Image"] = sad_image
df_sad["Emotion"] = sad_emotion
df_sad["Label"] = sad_label
print(df_sad)

#Splitting the data into train, cv and test

frames = [df_angry, df_fear, df_happy, df_neutral, df_sad] #list of all the dataframes
df_all = pandas.concat(frames)    #concatenate all data frames
#print(df_all.shape)

df_train, df_test = train_test_split(df_all, stratify=df_all["Label"], test_size=0.195) #split df_all by Label
df_train, df_cv = train_test_split(df_train, stratify=df_train["Label"], test_size=0.1) #split df_train by Label

df_train.reset_index(inplace=True, drop=True)

df_cv.reset_index(inplace=True, drop=True)

df_test.reset_index(inplace=True, drop=True)


df_train["Label"].value_counts().plot(kind='bar')
plt.title("Distribution of emotions in Training data,(1=Angry, 2=Fear, 3=Happy, 4=Neutral, 5=Sad)")
plt.show()

df_cv["Label"].value_counts().plot(kind='bar')
plt.title("Distribution of emotions in Validation data,(1=Angry, 2=Fear, 3=Happy, 4=Neutral, 5=Sad)")
plt.show()

df_test["Label"].value_counts().plot(kind='bar')
plt.title("Distribution of emotions in Testing data,(1=Angry, 2=Fear, 3=Happy, 4=Neutral, 5=Sad)")
plt.show()


def convt_to_gray(df):
    count = 0
    for i in range(len(df)):

        path1=df["Folder"][i]
        path2 = df["Image"][i]
        img = os.path.join(path1, path2)

        # noinspection PyUnresolvedReferences
        gray = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
        faceCascade = cv2.CascadeClassifier("C:/Users/Deeksha/PycharmProjects/test2/venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
        # noinspection PyUnresolvedReferences
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=3,
            minSize=(75, 75)        #can detect smallest face size of 75x75
        )
        face_resize=gray
        for (x, y, w, h) in faces:
            cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2) #drawing rectangle around face
            img_face = gray[y:y + h, x:x + w]            #extracting face
            # noinspection PyUnresolvedReferences
            face_resize=cv2.resize(img_face,(48,48))     #resize image

        cv2.imwrite(os.path.join(path1,path2), face_resize)
        count+=1
    print("Total number of images converted, cropped, resized and saved= "+str(count))


convt_to_gray(df_train)

convt_to_gray(df_cv)

convt_to_gray(df_test)


def make_folder(df,k):
    for i in range(len(df)):
        path1 = df["Folder"][i]
        path2 = df["Image"][i]
        img = os.path.join(path1, path2)
        # noinspection PyUnresolvedReferences
        gray = cv2.imread(img, cv2.IMREAD_GRAYSCALE)

        if(k==0):
            cv2.imwrite(os.path.join(dir,"train",df["Emotion"][i],path2), gray)
        elif(k==1):
            cv2.imwrite(os.path.join(dir, "validation",df["Emotion"][i],path2), gray)
        else:
            cv2.imwrite(os.path.join(dir, "test",df["Emotion"][i],path2), gray)

make_folder(df_train,0)
make_folder(df_cv,1)
make_folder(df_test,2)

batch_size = 128


datagen_train = ImageDataGenerator() #Generate batches of tensor image data with real-time data augmentation. The data will be looped over (in batches)
datagen_validation = ImageDataGenerator()

train_generator = datagen_train.flow_from_directory("C:/Users/Deeksha/Datasets/Expressions/train",  #reads images from the folder
                                                    target_size=(48,48),
                                                    color_mode="grayscale",
                                                    batch_size=batch_size,
                                                    class_mode='categorical',   #since there are more than 2 classes(not binary)
                                                    shuffle=True)       #shuffle the order of images

validation_generator = datagen_validation.flow_from_directory("C:/Users/Deeksha/Datasets/Expressions/validation",
                                                    target_size=(48,48),
                                                    color_mode="grayscale",
                                                    batch_size=batch_size,
                                                    class_mode='categorical',
                                                    shuffle=False)

# number of possible label values
nb_classes = 5

# Initialising the CNN
model = Sequential()

# 1 - Convolution
model.add(Conv2D(64,(3,3), padding='same', input_shape=(48, 48,1)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

# 2nd Convolution layer
model.add(Conv2D(128,(5,5), padding='same'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

# 3rd Convolution layer
model.add(Conv2D(512,(3,3), padding='same'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

# 4th Convolution layer
model.add(Conv2D(512,(3,3), padding='same'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

# Flattening
model.add(Flatten())

# Fully connected layer 1st layer
model.add(Dense(256))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dropout(0.25))

# Fully connected layer 2nd layer
model.add(Dense(512))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dropout(0.25))

model.add(Dense(nb_classes, activation='softmax'))

opt = Adam(lr=0.0001)
model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=["binary_accuracy"])


print(model.summary())


# number of epochs to train the NN
epochs = 50

checkpoint = ModelCheckpoint("model_weights.h5", monitor='val_binary_accuracy', verbose=1, save_best_only=True, mode='max') #saves the model
                                                                                                                        #after every epoch
callbacks_list = [checkpoint]

history = model.fit_generator(generator=train_generator,
                                steps_per_epoch=train_generator.n//train_generator.batch_size,
                                epochs=epochs,
                                validation_data = validation_generator,
                                validation_steps = validation_generator.n//validation_generator.batch_size,
                                callbacks=callbacks_list
                                )

# serialize model structure to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)

plt.figure(figsize=(20,10))
plt.subplot(1, 2, 1)
plt.suptitle('Optimizer : Adam', fontsize=10)           #Adam optimizer
plt.ylabel('Loss', fontsize=16)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend(loc='upper right')

plt.subplot(1, 2, 2)
plt.ylabel('Accuracy', fontsize=16)
plt.plot(history.history['binary_accuracy'], label='Training Accuracy')
plt.plot(history.history['val_binary_accuracy'], label='Validation Accuracy')
plt.legend(loc='lower right')
plt.show()



