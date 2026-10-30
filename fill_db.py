import os
import django

# Настройка Django для работы вне manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User
from myblog.models import Category, Post, Comment

def run():
    print("Начинаем заполнение базы...")

    # 1. Создаем пользователя-автора (если его нет)
    author, created = User.objects.get_or_create(username='Лесных Юлия')
    if created:
        author.set_password('password123')
        author.save()
        print("Создан автор: Лесных Юлия")

    # 2. Создаем категории
    cat_sad, _ = Category.objects.get_or_create(title='Садовые', slug='sadovye')
    cat_mnog, _ = Category.objects.get_or_create(title='Многолетники', slug='mnogoletniki')
    cat_luk, _ = Category.objects.get_or_create(title='Луковичные', slug='lukovichnye')
    cat_osen, _ = Category.objects.get_or_create(title='Осенние', slug='osennie')

    # 3. Данные для постов
    posts_data = [
        {
            'title': 'Гербера',
            'slug': 'gerbera',
            'content': 'Гербера — это яркий многолетник из семейства астровых. Крупные соцветия-корзинки бывают жёлтыми, оранжевыми, розовыми и красными.\n\nРодом гербера из Южной Африки. В Европу её завезли в XVIII веке, и с тех пор она стала одним из самых популярных садовых и комнатных растений.\n\nЦветёт гербера долго — с ранней весны до поздней осени. Любит солнце, регулярный полив и хорошо дренированную почву. Отлично стоит в срезке — до двух недель.',
            'image': 'posts/gerbera.jpg',
            'category': cat_sad
        },
        {
            'title': 'Роза',
            'slug': 'roza',
            'content': 'Роза — символ любви и красоты. Существуют сотни сортов — от миниатюрных кустовых до плетистых, которые украшают арки и стены.\n\nРодиной розы считается Персия. В Европу её завезли ещё в античные времена, и с тех пор она остаётся самым популярным цветком.\n\nРоза требует солнца, регулярной обрезки и укрытия на зиму. Взамен она цветёт всё лето и радует глаз пышными бутонами.',
            'image': 'posts/roza.jpg',
            'category': cat_sad
        },
        {
            'title': 'Тюльпан',
            'slug': 'tyulpan',
            'content': 'Тюльпан — весенний луковичный цветок родом из Средней Азии. Расцветает одним из первых — в апреле-мае.\n\nВ Голландии в XVII веке тюльпаны стоили дороже золота. За одну луковицу редкого сорта отдавали целый дом.\n\nТюльпаны бывают почти всех цветов, кроме синего. Любят солнечные участки и хорошо дренированную почву.',
            'image': 'posts/tyulpan.jpg',
            'category': cat_luk
        },
        {
            'title': 'Пион',
            'slug': 'pion',
            'content': 'Пион — пышный многолетник с крупными махровыми цветками. Цветёт в конце весны, живёт на одном месте десятки лет.\n\nРодина пиона — Китай, где он считается национальным цветком и символом богатства. В Европу попал в XVIII веке.\n\nПионы неприхотливы, но не любят пересадку. Один раз посадив куст, можно забыть о нём на 20–30 лет.',
            'image': 'posts/pion.jpg',
            'category': cat_mnog
        },
        {
            'title': 'Лилия',
            'slug': 'liliya',
            'content': 'Лилия — элегантный луковичный цветок с сильным ароматом. Высокие стебли, крупные воронковидные цветки.\n\nВ древности лилию считали символом чистоты. Её изображения встречаются на гербах и в храмовой росписи.\n\nЛилии бывают белые, жёлтые, розовые, оранжевые и даже тёмно-красные. Цветут в середине лета.',
            'image': 'posts/liliya.jpg',
            'category': cat_luk
        },
        {
            'title': 'Хризантема',
            'slug': 'hrizantema',
            'content': 'Хризантема — осенний цветок, символ долголетия. Бывает шаровидной, игольчатой и помпонной формы.\n\nРодина хризантемы — Китай и Япония. В Японии она считается императорским цветком, её изображение — на печати императора.\n\nХризантемы цветут до самых заморозков. Устойчивы к холоду, любят солнце и регулярный полив.',
            'image': 'posts/hrizantema.jpg',
            'category': cat_osen
        }
    ]

    # 4. Создаем посты
    for data in posts_data:
        post, created = Post.objects.get_or_create(
            slug=data['slug'],
            defaults={
                'title': data['title'],
                'content': data['content'],
                'image': data['image'],
                'category': data['category'],
                'author': author,
                'is_published': True
            }
        )
        if created:
            print(f"Добавлен пост: {post.title}")
            
            # Добавляем по комментарию от каждого
            Comment.objects.create(post=post, name='Богаева Ксения', text='Отличный блог! Очень нравится, как вы описываете цветы — читается легко и с удовольствием.')
            Comment.objects.create(post=post, name='Орлов Вадим', text='Очень красиво и познавательно!')

    print("Готово! Все посты добавлены.")

if __name__ == '__main__':
    run()