from django.shortcuts import render, redirect
from .models import *


def index(request):
    metadata = MetaData.objects.filter(is_active=True).first()
    hero = Hero.objects.filter(is_active=True).first()
    about = About.objects.filter(is_active=True).first()
    skillgroups = SlkillGroup.objects.filter(is_active=True)
    projects = Project.objects.filter(is_active=True)
    get_in_touch = GetInTouch.objects.filter(is_active=True).first()
    sections = Sections.objects.all().first()

    education_list = Education.objects.all()
    featured_achievements = Achievement.objects.filter(featured=True)
    achievement_categories = AchievementCategory.objects.prefetch_related("achievements")
    uncategorized_achievements = Achievement.objects.filter(category__isnull=True)
    experience_list = Experience.objects.all()

    context = {
        'metadata': metadata,
        'hero': hero,
        'about': about,
        'skillgroups': skillgroups,
        'projects': projects,
        'get_in_touch': get_in_touch,
        'sections': sections,
        'education_list': education_list,
        'featured_achievements': featured_achievements,
        'achievement_categories': achievement_categories,
        'uncategorized_achievements': uncategorized_achievements,
        'experience_list': experience_list,

    }

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        Message.objects.create(name=name, email=email, message=message)
        return redirect('index')
        # return render(request, 'index.html', context=context)

    return render(request, 'index.html', context=context)


def robots(request):
    return render(request, 'robots.txt', content_type='text/plain')


def sitemap(request):
    return render(request, 'sitemap.xml', content_type='text/xml')




###########chatbot
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .chatbot import get_bot_response


@csrf_exempt
@require_POST
def chatbot_api(request):
    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()
        if not user_message:
            return JsonResponse({"error": "Empty message"}, status=400)

        chat_history = request.session.get("chat_history", [])

        bot_reply = get_bot_response(user_message, chat_history)

        chat_history.append({"role": "human", "content": user_message})
        chat_history.append({"role": "ai", "content": bot_reply})
        request.session["chat_history"] = chat_history[-20:]  # keep last 10 exchanges

        return JsonResponse({"reply": bot_reply})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)