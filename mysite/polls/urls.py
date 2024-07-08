from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IndexView, DetailView, ResultsView, detail, results, vote, QuestionViewSet, ChoiceViewSet

app_name = 'polls'  # This sets the namespace for the app

router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'choices', ChoiceViewSet)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('questions/<int:pk>/', DetailView.as_view(), name='detail'),
    path('questions/<int:pk>/results/', ResultsView.as_view(), name='results'),
    path('questions/<int:question_id>/vote/', vote, name='vote'),
    path('api/', include(router.urls)),
]
