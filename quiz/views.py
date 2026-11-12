
from django.shortcuts import render, redirect

PERSONALITIES = {
    "sleepy": {
        "name": "The Sleepy Student",
        "emoji": "😴",
        "description": "Your favorite subject is Sleeping! Even the teacher's voice makes you sleepy.",
        "message": "Coffee is your best friend!"
    },
    "backbencher": {
        "name": "The Backbencher",
        "emoji": "😎",
        "description": "You are the entertainment department of your classroom!",
        "message": "Last bench, unlimited fun!"
    },
    "topper": {
        "name": "The Class Topper",
        "emoji": "🏆",
        "description": "You are always prepared, organized and ready for every exam.",
        "message": "Keep shining, superstar!"
    },
    "warrior": {
        "name": "The Last-Minute Warrior",
        "emoji": "🔥",
        "description": "You believe that anything can be studied the night before an exam!",
        "message": "Deadline is your motivation!"
    }
}

QUESTIONS = [
    {
        "text": "1. When do you start studying for exams?",
        "options": [
            ("One month before exams", "topper"),
            ("One week before exams", "backbencher"),
            ("One night before exams", "warrior"),
            ("I prefer sleeping", "sleepy"),
        ]
    },
    {
        "text": "2. What do you do during boring lectures?",
        "options": [
            ("Take detailed notes", "topper"),
            ("Sleep peacefully", "sleepy"),
            ("Chat with friends", "backbencher"),
            ("Study only when exams arrive", "warrior"),
        ]
    },
    {
        "text": "3. When the teacher asks a question, what do you do?",
        "options": [
            ("Raise my hand immediately", "topper"),
            ("Pretend to search my bag", "backbencher"),
            ("Look at my friends", "sleepy"),
            ("Hope the teacher forgets me", "warrior"),
        ]
    },
    {
        "text": "4. When do you complete assignments?",
        "options": [
            ("Before the deadline", "topper"),
            ("At the last minute", "warrior"),
            ("After copying from a friend", "backbencher"),
            ("When I wake up from my nap", "sleepy"),
        ]
    },
    {
        "text": "5. What is your favorite classroom activity?",
        "options": [
            ("Learning new things", "topper"),
            ("Sleeping", "sleepy"),
            ("Making everyone laugh", "backbencher"),
            ("Waiting for lunch break", "warrior"),
        ]
    },
    {
        "text": "6. What is your reaction when exams are announced?",
        "options": [
            ("I am fully prepared", "topper"),
            ("Let me sleep first", "sleepy"),
            ("Let's enjoy until the last day", "backbencher"),
            ("Time to activate emergency mode!", "warrior"),
        ]
    },
    {
        "text": "7. What is always inside your college bag?",
        "options": [
            ("Books and organized notes", "topper"),
            ("Snacks and random items", "backbencher"),
            ("A pillow would be useful", "sleepy"),
            ("One notebook for all subjects", "warrior"),
        ]
    },
    {
        "text": "8. What happens when you hear the word homework?",
        "options": [
            ("I will complete it now", "topper"),
            ("Maybe tomorrow", "sleepy"),
            ("Let's ask a friend", "backbencher"),
            ("Deadline? Challenge accepted!", "warrior"),
        ]
    },
    {
        "text": "9. Where do you prefer sitting in class?",
        "options": [
            ("First bench", "topper"),
            ("Last bench", "backbencher"),
            ("Near the window for sleeping", "sleepy"),
            ("Anywhere, as long as I can survive", "warrior"),
        ]
    },
    {
        "text": "10. What is your biggest college talent?",
        "options": [
            ("Getting excellent marks", "topper"),
            ("Making friends everywhere", "backbencher"),
            ("Sleeping anywhere", "sleepy"),
            ("Passing exams with one-night preparation", "warrior"),
        ]
    },
]


def home(request):
    return render(request, 'quiz/home.html')


def quiz_page(request):
    if request.method == 'POST':
        name = request.POST.get('student_name', '').strip()

        if not name or len(name) > 50:
            return redirect('home')

        context = {
            'name': name,
            'questions': QUESTIONS,
        }

        return render(request, 'quiz/questions.html', context)

    return redirect('home')


def result(request):
    if request.method != 'POST':
        return redirect('home')

    name = request.POST.get('student_name', '').strip()

    if not name or len(name) > 50:
        return redirect('home')

    scores = {
        'sleepy': 0,
        'backbencher': 0,
        'topper': 0,
        'warrior': 0,
    }

    for index, question in enumerate(QUESTIONS, start=1):
        selected = request.POST.get(f'q{index}')

        valid_answers = [
            category for _, category in question['options']
        ]

        if selected in valid_answers:
            scores[selected] += 1

    highest_score = max(scores.values())

    # In case of a tie, select the first matching category.
    winner = next(
        category
        for category in scores
        if scores[category] == highest_score
    )

    personality = PERSONALITIES[winner]

    context = {
        'name': name,
        'personality': personality,
        'score': highest_score,
        'scores': scores,
    }

    return render(request, 'quiz/result.html', context)
