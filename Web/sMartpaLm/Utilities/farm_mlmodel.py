import os
import numpy as np
from datetime import datetime
from keras.preprocessing.image import ImageDataGenerator
from Utilities.comUtilities import get_property
from tensorflow.keras import layers, Model
from tensorflow.keras.models import Model, Sequential, load_model
from Utilities.DBManager import DBman
from PIL import Image

# Preprocessing data.  이미지데이터 preprocessing하고, 수치형 데이터도 만져줘야함.
def preprocessing_data(train_dir):
    train_datagen=ImageDataGenerator(rescale=1./255,
                                       validation_split=0.2)
    img_width, img_height = 256, 256
    img_width,img_height = img_width, img_height #원본 이미지 shape 확인후 입력하던 변수값을 넣던 해야함.
    batch_size = 32

    train_generator =train_datagen.flow_from_directory(train_dir,                        #train_img 전처리
                                                       target_size=(img_width,img_height),
                                                       batch_size=batch_size)
    return train_generator


def predict_disease(image_path, crop_id):
    model_path = get_property('DATA', 'base_dir') + get_property('DATA', 'model') + f"{crop_id}_disease.h5"

    # 모델 로드
    if model_path is not None and os.path.exists(model_path):
        model = SmartFarmModel(window_size=5, image_shape=(256, 256, 3)).get_conv_lstm()
        model.add(layers.Dense(5, activation='softmax'))
        model = model.load_model(model_path)

    # 이미지 불러오기 및 전처리
    x = preprocessing_data(image_path)

    # 예측 수행
    predictions = model.predict(x)
    # class_indices = np.argmax(predictions, axis=1)

    # return class_indices
    return predictions


class SmartFarmModel:
    def __init__(self, window_size=5, image_shape= (720, 480, 3), num_features=4):
        self.window_size = window_size
        self.image_shape = image_shape
        self.num_features = num_features
        self.num_classes = 5  # Number of crop growth states

    def get_convl(self, inp):
        # CNN building.
        # model = Sequential()
        # model.add(layers.Conv2D(32, (3, 3), padding='same', input_shape=input_shape, activation='relu'))
        out_model = layers.MaxPooling2D(pool_size=(2, 2), strides = 2)(inp)
        out_model = layers.Conv2D(32, (3, 3), padding='same', activation='relu')(out_model)
        out_model = layers.MaxPooling2D(pool_size=(2, 2), strides = 2)(out_model)
        out_model = layers.Conv2D(32, (3, 3), padding='same', activation='relu')(out_model)
        out_model = layers.MaxPooling2D(pool_size=(2, 2), strides=2)(out_model)

        out_model = layers.Flatten()(out_model)
        out_model = layers.Dense(256, activation='relu')(out_model)
        out_model = layers.Dropout(0.25)(out_model)
        out_model = layers.Dense(64, activation='relu')(out_model)


        # model.add(layers.MaxPooling2D(pool_size=(2, 2), strides = 2))
        # model.add(layers.Conv2D(32, (3, 3), padding='same', activation='relu'))
        # model.add(layers.MaxPooling2D(pool_size=(2, 2), strides = 2))
        # model.add(layers.Conv2D(32, (3, 3), padding='same', activation='relu'))
        # model.add(layers.MaxPooling2D(pool_size=(2, 2), strides = 2))
        #
        #
        # # 추가적인 컨볼루션 레이어 및 풀링 레이어를 필요에 따라 반복적으로 추가할 수 있음.
        # model.add(layers.Flatten())
        # model.add(layers.Dense(256, activation='relu'))
        # model.add(layers.Dropout(0.25))
        # model.add(layers.Dense(64, activation='relu'))
        # model.add(layers.Dense(5, activation='softmax'))

        # model.summary()

        return out_model

    def get_conv_lstm(self):
        image_input = layers.Input(shape=(self.window_size, self.image_shape))
        cnn_model = self.get_convl(image_input)

        cnn_out = Model(inputs=cnn_model.input, outputs=cnn_model.output)

        rnn_input = layers.Input(shape=(self.window_size, self.num_features))
        rnn_model = layers.LSTM(64)(rnn_input)

        combined = layers.concatenate([cnn_out.output, rnn_model])
        dense = layers.Dense(64, activation='relu')(combined)
        output = layers.Dense(self.num_classes, activation='softmax')(dense)

        model = Model(inputs=[cnn_out.input, rnn_input], outputs=output)
        return model
    
    def train_model(self, epochs, crop_id):
        # 만약 가중치 파일이 있으면 있는데에다 추가로 데이터 학습
        
        # train_gen = preprocessing_data(train_dir)
        df = self.get_data(crop_id)

        # input_shape = train_gen.image_shape  # 거기있는 파일의 shape그대로 or get_model에서 정한 shape 그대로
        # num_class = len(train_gen.class_indices)

        model = self.get_conv_lstm()
        X_train, X_img = self.pre_process(crop_id, df, self.window_size)

        if self.file_path is not None and os.path.exists(self.file_path):
            model.load_weights(self.file_path)

        # opt=keras.optimizers.Adam(lr=0.001)
        model.compile(optimizer='Adam',loss='categorical_crossentropy',metrics=['accuracy'])

        model.fit(
            [X_img, X_train],  # train_generator를 통해 y값은 따로안받아도된다.
            # steps_per_epoch=train_gen.samples // batch_size,
            epochs=epochs
        )

        base_path = get_property('DATA', 'base_dir')
        model_path = get_property('DATA', 'modelpath')

        if os.path.isfile(base_path + model_path + f"{crop_id}_trained.h5"):
            backuppath = model_path = get_property('DATA', 'modelbackup')
            os.rename(base_path + model_path + f"{crop_id}_trained.h5", base_path + backuppath + f"{crop_id}_{datetime.today()}.h5")

        model.save_weights(base_path + model_path + f"{crop_id}_trained.h5")

    def pre_process(self, df, window_size):

        feature_list = []
        img_lst = []
        for i in range(len(df)):
            if i+window_size > len(df):
                break

            if df.iloc[i]['user_id'] == df.iloc[i + window_size]['user_id'] and \
                df.iloc[i]['farm_id'] == df.iloc[i + window_size]['farm_id']:
                feature_list.append(df.iloc[i:i+window_size])

                img_lst.append(Image.open(df.iloc[i + window_size]['status_img']))


        return np.array(feature_list), img_lst

    def get_data(self, crop_id):
        dbm = DBman()
        sql = f"SELECT data.user_id, data.farm_id, co2_density, light_amount, temperature, humidity, nutrition_amt, status_img " \
              "FROM sensored_data data, farm " \
              "WHERE data.user_id = farm.user_id " \
              "AND data.farm_id = farm.farm_id " \
              f"AND farm.crop_id = {crop_id} " \
              "ORDER BY data.user_id, data.farm_id, data.sensor_date DESC"

        df = dbm.excute_alconn('get_data', sql)

        return df




