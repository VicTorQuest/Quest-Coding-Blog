from django.urls import path
from newsletter.views import subscribe, subscription_confirmed, send_news_letter, edit_preference, unsubscribe, unsubscribe_successful



urlpatterns = [
    path('subscribe/', subscribe, name='subscribe'),
    path('subscription-confirmed/', subscription_confirmed, name='subscription_confirmed'),
    path('subscription-confirmed/<slug:slug>/', edit_preference, name='edit_preference'),
    path('unsubscribe/<slug:slug>/', unsubscribe, name='unsubscribe'),
    path('unsubscription-successful/', unsubscribe_successful, name='unsubscribe_successful'),
    path('send-news-letter/', send_news_letter, name='send_news_letter'),
]
