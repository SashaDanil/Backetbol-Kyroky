from flask import Flask, render_template, request

app = Flask(__name__)

# Данные о персонажах
CHARACTERS = [
    {
        'id': 1,
        'name': 'Тацуя Куроко',
        'japanese_name': '黒子 テツヤ',
        'position': 'Призрачный шестой игрок',
        'team': 'Сейрин',
        'height': '168 см',
        'weight': '57 кг',
        'birthday': '31 января',
        'special_ability': 'Незаметность, Игно-пасс',
        'description': 'Бывший член Поколения Чудес, известный своей почти невидимой игрой. Обладает исключительными навыками паса и видением площадки.',
        'abilities': ['Игно-пасс', 'Циклический пас', 'Незаметность', 'Куэйкер Степ'],
        'voice_actor': 'Кэнси Оно',
        'image': 'kuroko.png'
    },
    {
        'id': 2,
        'name': 'Тайга Кагами',
        'japanese_name': '火神 大我',
        'position': 'Силовой форвард',
        'team': 'Сейрин',
        'height': '190 см',
        'weight': '82 кг',
        'birthday': '2 августа',
        'special_ability': 'Звериный инстинкт, Прыгучесть',
        'description': 'Талантливый игрок, вернувшийся из Америки. Обладает невероятной прыгучестью и стремлением побеждать.',
        'abilities': ['Звериный инстинкт', 'Метка Зоны', 'Потрясающая прыгучесть'],
        'voice_actor': 'Юки Кадзи',
        'image': 'kagami.png'
    },
    {
        'id': 3,
        'name': 'Дайки Аоминэ',
        'japanese_name': '青峰 大輝',
        'position': 'Атакующий защитник',
        'team': 'Тоо',
        'height': '192 см',
        'weight': '85 кг',
        'birthday': '31 августа',
        'special_ability': 'Формальный бросок, Неправильная форма',
        'description': 'Член Поколения Чудес, известный как самый быстрый и непредсказуемый нападающий.',
        'abilities': ['Формальный бросок', 'Неправильная форма', 'Сверхскорость'],
        'voice_actor': 'Субуру Кимицуки',
        'image': 'aomine.png'
    },
    {
        'id': 4,
        'name': 'Ацуси Мурокасаки',
        'japanese_name': '紫原 敦',
        'position': 'Центровой',
        'team': 'Ясен',
        'height': '208 см',
        'weight': '95 кг',
        'birthday': '9 октября',
        'special_ability': 'Громовой данк, Защита всей площадки',
        'description': 'Член Поколения Чудес, обладающий огромным ростом и силой. Может защищать всю площадку.',
        'abilities': ['Громовой данк', 'Защита всей площадки', 'Силовое превосходство'],
        'voice_actor': 'Кэнъити Судзумура',
        'image': 'murasakibara.png'
    },
    {
        'id': 5,
        'name': 'Сюнсукэ Кисе',
        'japanese_name': '黄瀬 涼太',
        'position': 'Атакующий защитник',
        'team': 'Каё',
        'height': '189 см',
        'weight': '77 кг',
        'birthday': '18 июня',
        'special_ability': 'Идеальное подражание',
        'description': 'Член Поколения Чудес, способный копировать движения других игроков после однократного просмотра.',
        'abilities': ['Идеальное подражание', 'Атлетичность', 'Быстрое обучение'],
        'voice_actor': 'Коки Мията',
        'image': 'kise.png'
    },
    {
        'id': 6,
        'name': 'Сейджуро Акаси',
        'japanese_name': '赤司 征十郎',
        'position': 'Разыгрывающий защитник',
        'team': 'Ракудзан',
        'height': '173 см',
        'weight': '64 кг',
        'birthday': '20 декабря',
        'special_ability': 'Императорский глаз',
        'description': 'Капитан Поколения Чудес и лидер команды. Обладает Императорским глазом, позволяющим видеть будущее противника.',
        'abilities': ['Императорский глаз', 'Совершенный пас', 'Абсолютное лидерство'],
        'voice_actor': 'Хироки Ясумото',
        'image': 'akashi.png'
    },
    {
        'id': 7,
        'name': 'Синтаро Мидорима',
        'japanese_name': '緑間 真太郎',
        'position': 'Атакующий защитник',
        'team': 'Сюто',
        'height': '195 см',
        'weight': '79 кг',
        'birthday': '7 июля',
        'special_ability': 'Бросок из любой точки площадки',
        'description': 'Член Поколения Чудес, известный своими невероятными трехочковыми бросками с любой точки площадки. Всегда следует своим приметам.',
        'abilities': ['Полноплощадочный бросок', 'Высокая точность', 'Тактическое мышление'],
        'voice_actor': 'Дайсукэ Намикава',
        'image': 'midorima.png'
    }
]

# Данные об эпизодах (исправлены пропущенные запятые)
EPISODES = [
    {
        'id': 1,
        'season': 1,
        'episode_number': 1,
        'title': 'Я - Куроко',
        'description': 'Тацуя Куроко знакомится с Тайгой Кагами и предлагает ему стать партнерами по баскетболу.',
        'key_moments': ['Первая встреча Куроко и Кагами', 'Демонстрация Игно-пасса', 'Решение играть вместе'],
        'importance': 'high',
        'rutub_url': 'https://rutube.ru/video/35cbc4fb51ce32377959008ae4bf9d50/',
        'duration': '24 мин'
    },
    {
        'id': 2,
        'season': 1,
        'episode_number': 2,
        'title': 'Поколение Чудес',
        'description': 'Кагами узнает о Поколении Чудес и встречает первого из них - Кисэ.',
        'key_moments': ['Рассказ о Поколении Чудес', 'Встреча с Кисэ', 'Первая игра против Каё'],
        'importance': 'high',
        'rutub_url': 'https://rutube.ru/video/8d683f51a5b13aa42b7f63c47541a90e/',
        'duration': '24 мин'
    },
    {
        'id': 3,
        'season': 1,
        'episode_number': 25,
        'title': 'Победа или поражение',
        'description': 'Финальная игра против Тоо и Аоминэ. Решающий момент в развитии команды Сейрин.',
        'key_moments': ['Пробуждение Кагами', 'Финальная дуэль с Аоминэ', 'Развитие команды'],
        'importance': 'critical',
        'rutub_url': 'https://rutube.ru/video/d368810ac81c1f6bff113f6406e86a52/?playlist=386250',
        'duration': '24 мин'
    },
    {
        'id': 4,
        'season': 2,
        'episode_number': 1,
        'title': 'Новый вызов',
        'description': 'Начало Зимнего Кубка и встреча с новой угрозой - командой Ясен.',
        'key_moments': ['Начало нового турнира', 'Встреча с Мурокасаки', 'Новые цели'],
        'importance': 'high',
        'rutub_url': 'https://rutube.ru/video/a769e0ddf9eedb25e8a5080ff3eab5be/?playlist=386250',
        'duration': '24 мин'
    },
    {
        'id': 5,
        'season': 2,
        'episode_number': 25,
        'title': 'Сильнейший противник',
        'description': 'Финальная битва против Акаси и команды Ракудзан.',
        'key_moments': ['Императорский глаз Акаси', 'Объединение усилий Куроко и Кагами', 'Финальный результат'],
        'importance': 'critical',
        'rutub_url': 'https://rutube.ru/video/2f4ff8308d7314fea95d60bb7b92008e/?playlist=386250',
        'duration': '24 мин'
    },
    {
        'id': 6,
        'season': 3,
        'episode_number': 1,
        'title': 'Последняя игра',
        'description': 'Финальный сезон и противостояние с объединенной командой Поколения Чудес.',
        'key_moments': ['Формирование команды противников', 'Новые уровни способностей', 'Начало финальной битвы'],
        'importance': 'critical',
        'rutub_url': 'https://rutube.ru/video/1f96391e398815e96d1fd4a648e92030/?playlist=386250',
        'duration': '24 мин'
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/characters')
def characters():
    return render_template('characters.html', characters=CHARACTERS)

@app.route('/character/<int:character_id>')
def character_detail(character_id):
    character = next((c for c in CHARACTERS if c['id'] == character_id), None)
    if character:
        return render_template('character_detail.html', character=character)
    return "Персонаж не найден", 404

@app.route('/episodes')
def episodes():
    season = request.args.get('season', 'all')
    
    if season != 'all':
        filtered_episodes = [ep for ep in EPISODES if ep['season'] == int(season)]
    else:
        filtered_episodes = EPISODES
    
    return render_template('episodes.html', episodes=filtered_episodes, season=season)

@app.route('/episode/<int:episode_id>')
def episode_detail(episode_id):
    episode = next((ep for ep in EPISODES if ep['id'] == episode_id), None)
    if episode:
        return render_template('episode_detail.html', episode=episode)
    return "Эпизод не найден", 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)