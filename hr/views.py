from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import base64
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import numpy as np
import tensorflow as tf
import os


# Create your views here.
def index(request):
    return HttpResponse("<h2>Hi</h2>")


def home(request):
    return render(request, "hr/home.html")


@csrf_exempt
def process_url_from_client(request):
    image = request.POST.get('url')
    # print(image)
    with open('hr/static/hr/img/sample.png', 'wb') as f:
        f.write(base64.decodebytes(image.split(',')[1].encode()))
    size = 28, 28
    image = Image.open('hr/static/hr/img/sample.png').convert('LA')
    image.thumbnail(size, Image.ANTIALIAS)
    arr = np.array(image)
    outer = []
    for a in arr:
        inner = []
        for b in a:
            inner.append(b[1] / 255.0)
        outer.append(inner)

    test = [outer]
    test = np.array(test)

    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(512, activation=tf.nn.relu6),
        tf.keras.layers.Dense(10, activation=tf.nn.softmax)
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.load_weights('hr/static/hr/img/cp.ckpt')
    prediction = qwerty = model.predict(test)
    _, pred = np.where(prediction == np.max(qwerty))
    # print(pred)

    return JsonResponse({"data": str(pred[0])})
