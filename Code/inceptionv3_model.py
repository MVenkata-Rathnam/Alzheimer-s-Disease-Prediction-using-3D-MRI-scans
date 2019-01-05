import keras
import numpy as np
from keras.models import Sequential, Model
from keras.layers import Dense, Flatten
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras.optimizers import Adam

train_data_dir = 'AlzheimerDataset/train/'
validation_data_dir = 'AlzheimerDataset/test/'

batch_size = 32
img_height = 208
img_width = 176
numClasses=4
epoch=10

train_datagen= ImageDataGenerator(
        rescale= 1./255, 
        shear_range= 0.2,
        zoom_range= 0.2, 
        horizontal_flip= True)

validation_datagen= ImageDataGenerator(
        rescale= 1./255)

train_generator= train_datagen.flow_from_directory(
        train_data_dir, target_size= (img_height, img_width),
        batch_size= batch_size,
        class_mode='categorical')

validation_generator= validation_datagen.flow_from_directory(
        validation_data_dir, target_size= (img_height, img_width),
        batch_size= batch_size,
        class_mode= 'categorical')


base_model= keras.applications.inception_v3.InceptionV3(weights= 'imagenet', include_top= False, input_shape=(img_height, img_width, 3))

add_model= Sequential()
add_model.add(Flatten(input_shape=base_model.output_shape[1:]))
add_model.add(Dense(4, activation='softmax'))

model= Model(inputs= base_model.input, outputs=add_model(base_model.output))
model.compile(loss='categorical_crossentropy', optimizer=optimizers.SGD(lr=1e-4, momentum=0.9),
              metrics=['accuracy'])

model.summary()

steps_per_epoch = train_generator.n // batch_size
validation_steps = validation_generator.n // batch_size

model.fit_generator(train_generator,
        epochs=epoch,
        validation_data=validation_generator,
        verbose=1,
	steps_per_epoch=steps_per_epoch,
	validation_steps=validation_steps
        )        
