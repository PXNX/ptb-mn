import config
from dataclasses import dataclass


@dataclass
class Language:
    lang_key: str
    channel_id: int
    #  chat_id: int
    footer: str
    breaking: str
    announce: str


# captcha:str

languages: [Language] = [
    Language(
        "en-us",  # English
        config.CHANNEL_EN,  # https://t.me/MilitaryNewsEN
        "🔰 Subscribe to @MilitaryNewsEN\n🔰 Join us @MilitaryChatEN",
        "BREAKING",
        "ANNOUNCEMENT"),
    Language(
        "tr",  # Turkish
        -1001712502236,  # https://t.me/MilitaryNewsTR
        "🔰@MilitaryNewsTR'e abone olun\n🔰Bize katılın @MNChatTR",
        "SON_DAKİKA",
        "DUYURU"),
    Language(
        "fa",  # Persian
        -1001568841775,  # https://t.me/MilitaryNewsFA
        "\nعضو شوید:\n🔰 @MilitaryNewsFA\nبه چت ملحق بشید:\n🔰 @MNChatFA",
        "خبرفوری",
        "اعلامیه"),
    Language(
        "ru",  # Russian
        -1001330302325,  # https://t.me/MilitaryNewsRU
        "🔰 Подписывайтесь на @MilitaryNewsRU",
        "СРОЧНЫЕ_НОВОСТИ",
        "ОБЪЯВЛЕНИЕ"),
    Language(
        "pt-br",  # Portugese
        -1001614849485,  # https://t.me/MilitaryNewsBR
        "🔰 Se inscreva no @militaryNewsBR",
        "NOTÍCIAS_URGENTES",
        "MENSAGEM"),
    Language(
        "es",  # Spanish
        -1001715032604,  # https://t.me/MilitaryNewsES
        "🔰 Suscríbete a @MilitaryNewsES",
        "ÚLTIMA_HORA",
        "ANUNCIO"),
    Language(
        "fr",
     -1001337262241 ,  # French
        "🔰 Abonnez-vous à @MilitaryNewsFR\n🔰 Rejoignez notre tchat anglophone: @MilitaryChatEN",
        "BREAKING_NEWS",
        "ANNONCE"),
     Language("it",
                -1001632091535, # Italian
              "🔰 iscriviti a @MilitaryNewsITA",
                  "ULTIME_NOTIZIE",
              "ANNUNCIO"
              )
]