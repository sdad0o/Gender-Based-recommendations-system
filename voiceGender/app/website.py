from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import os
import time
from . import test  

def index(request):
    return render(request, 'index.html')

def upload(request):
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']
        if file.name == '':
            return JsonResponse({'error': 'No selected file'})
        filename = file.name
        file_path = os.path.join(settings.MEDIA_ROOT, filename + ".wav")  # Add .wav extension
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        time.sleep(1)  # Wait for 1 second to ensure the file is fully saved

        # Extract features and predict gender
        features = test.extract_feature(file_path, mel=True).reshape(1, -1)
        model = test.create_model()
        model.load_weights("results/model.h5")
        male_prob = model.predict(features)[0][0]
        female_prob = 1 - male_prob
        gender = "male" if male_prob > female_prob else "female"

        # Convert NumPy float32 to Python float
        male_prob = float(male_prob)
        female_prob = float(female_prob)

        return JsonResponse({'result': gender, 'male_prob': male_prob, 'female_prob': female_prob})
    else:
        return JsonResponse({'error': 'No file part'})