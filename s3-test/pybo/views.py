from django.core.serializers import serialize
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from rest_framework.decorators import api_view
from django.utils import timezone
from django.http import HttpResponseNotAllowed, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pybo.models import Question, Answer

from .forms import QuestionForm, AnswerForm
from .serializer import PresignedURLSerializer
from .utils import s3_file_upload_by_file_date
import logging

logger = logging.getLogger(__name__)


class DetailView(generic.DetailView):
    model = Question


class IndexView(generic.ListView):
    def get_queryset(self):
        return Question.objects.order_by('-create_date')


def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', pk=question.id)
    else:
        return HttpResponseNotAllowed('Only POST is Possible')
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


def question_create(request):
    print('question_create')
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    print(f'context : {context}')
    return render(request, 'pybo/question_form.html', context)


@api_view(['POST'])
def upload_to_s3(request):
    print(f'@@@@@@@@@@@@ request.FILES : {request.FILES}')
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file part'}, status=400)

    upload_file = request.FILES['file']
    bucket_path = 'uploads'

    try:
        uploaded_file_url = s3_file_upload_by_file_date(
            upload_file=upload_file,
            bucket_path=bucket_path,
            content_type=upload_file.content_type
        )
        if uploaded_file_url:
            return JsonResponse({'file_url': uploaded_file_url}, status=201)
        return JsonResponse({'error': 'Failed to upload file'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


class PresignedURLView(APIView):
    def post(self, request):
        print("Request Data:", request.data)

        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@ 이거 뭐냐 PresignedURLView")
        serializer = PresignedURLSerializer(data=request.data)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@ 이거 뭐냐 PresignedURLView22")
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)