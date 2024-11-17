from django.shortcuts import render, get_object_or_404, redirect
from .models import ImageData
from .forms import ImageLabelForm

def label_image(request, image_id):
   
    image_data = get_object_or_404(ImageData, pk=image_id)
    print(image_data)
    form = ImageLabelForm(request.POST or None, instance=image_data)

    if request.method == 'POST' and form.is_valid():
        form.save()
        next_image = ImageData.objects.filter(label__isnull=True).exclude(id=image_id).first()
        if next_image:
            return redirect('label_image', image_id=next_image.id)
        else:
            return redirect('done')  # صفحه ای برای اتمام برچسب گذاری

    return render(request, 'image_labeler/label_image.html', {'image_data': image_data, 'form': form})
def done(request):
    return render(request, 'image_labeler/done.html')

def index(request):
    return render(request, 'image_labeler/index.html')