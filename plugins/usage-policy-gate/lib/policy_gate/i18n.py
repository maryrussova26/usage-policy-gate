"""Human-readable hints (ru/en). Tone: direct and respectful; explain the rule, offer a compliant route.
Never threatens, never claims the user is flagged, never explains how to evade checks."""
from __future__ import annotations

_CONSEQ = {
    "ru": "Повторные нарушения могут привести к предупреждению, ограничению или блокировке аккаунта со стороны Anthropic.",
    "en": "Repeated violations can lead Anthropic to warn, limit or suspend an account.",
}
_APPEAL = {
    "ru": "Если считаете, что это ошибка проверки, переформулируйте запрос с реальным контекстом цели.",
    "en": "If you think this is a false alarm, restate the request with the real context of your goal.",
}
_ACK_HINT = {
    "ru": "Это серая зона. Если вы понимаете риск и действуете законно, добавьте в начало запроса «[принимаю риск]». Это не гарантия: решения о мерах принимает Anthropic.",
    "en": "This is a gray area. If you understand the risk and your use is lawful, prefix the request with “[accept-risk]”. It is not a guarantee: Anthropic makes enforcement decisions.",
}
_OBF = {
    "ru": "Замена букв или разделение слов не меняет оценку запроса.",
    "en": "Swapping letters or splitting words does not change how a request is assessed.",
}

M = {
 "child_safety": {
  "ru": ("Не могу с этим помочь.", "Сексуальный контент с участием несовершеннолетних запрещён без исключений.", "Могу помочь с материалами по защите детей и распознаванию груминга на уровне паттернов."),
  "en": ("I can't help with this.", "Sexual content involving minors is prohibited with no exceptions.", "I can help with child-protection and grooming-awareness material at the pattern level.")},
 "weapons_cbrn": {
  "ru": ("Не могу с этим помочь.", "Инструкции по созданию оружия массового поражения и взрывных устройств запрещены.", "Могу рассказать об истории, политике контроля или защитных мерах без технических деталей."),
  "en": ("I can't help with this.", "Instructions for building mass-casualty weapons or explosive devices are prohibited.", "I can cover history, arms-control policy or protective measures without technical detail.")},
 "malware": {
  "ru": ("Не могу с этим помочь.", "Создание вредоносного ПО запрещено, даже в учебных целях.", "Могу объяснить, как такие угрозы обнаруживаются и блокируются, или помочь с защитой системы."),
  "en": ("I can't help with this.", "Creating malware is prohibited, even for educational purposes.", "I can explain how such threats are detected and mitigated, or help harden your system.")},
 "cyber_gray": {
  "ru": ("Нужен контекст.", "Запрос про взлом может нарушать правила, если нет разрешения владельца системы.", "Опишите легальную рамку (свой стенд, CTF, письменное разрешение) — тогда помогу с защитной стороной."),
  "en": ("Context needed.", "Requests about breaking into systems can violate the policy without the owner's permission.", "Describe the lawful frame (your own lab, CTF, written authorization) and I can help on the defensive side.")},
 "surveillance": {
  "ru": ("Не могу с этим помочь.", "Слежка и отслеживание людей без их согласия запрещены.", "Могу помочь с прозрачными, согласованными решениями (семейная геолокация с уведомлением, корпоративный мониторинг с политикой)."),
  "en": ("I can't help with this.", "Tracking or monitoring people without their consent is prohibited.", "I can help with transparent, consented options (family location sharing with notice, disclosed workplace monitoring).")},
 "emotion_recognition": {
  "ru": ("Нужен контекст.", "Определение эмоций или психического состояния людей допускается только по медицинским или safety-причинам; оценка кандидатов, сотрудников и посторонних запрещена.", "Могу помочь с оценкой поведения ИИ на синтетических или согласованных агрегированных данных, или с клиническим сценарием с участием квалифицированного специалиста."),
  "en": ("Context needed.", "Inferring emotions or mental state of people is limited to medical or safety uses; assessing candidates, employees or strangers is prohibited.", "I can help evaluate AI behavior on synthetic or consented aggregate data, or a clinical workflow with a qualified human reviewer.")},
 "social_scoring": {
  "ru": ("Не могу с этим помочь.", "Оценка благонадёжности или социального рейтинга людей по поведению запрещена.", "Могу помочь с прозрачной системой с уведомлением и согласием людей."),
  "en": ("I can't help with this.", "Scoring people's trustworthiness or social behavior is prohibited.", "I can help design a transparent system with notice and consent.")},
 "platform_abuse": {
  "ru": ("Не могу с этим помочь.", "Обход блокировок, лимитов и защит, мультиаккаунты, джейлбрейк и дистилляция нарушают правила использования.", "Если вам не хватает лимитов — могу посоветовать оптимизацию запросов или официальный тариф, либо правильный путь для исследований."),
  "en": ("I can't help with this.", "Circumventing bans, limits or safeguards, multi-accounting, jailbreaking and distillation violate the usage rules.", "If you are short on limits, I can help optimize requests or point to an official plan, or the proper route for research.")},
 "fraud_deception": {
  "ru": ("Не могу с этим помочь.", "Фальшивые отзывы, поддельные документы и фишинг — обман, он запрещён.", "Могу написать честное описание продукта или шаблон с явной пометкой «образец»."),
  "en": ("I can't help with this.", "Fake reviews, forged documents and phishing are deception and prohibited.", "I can write an honest product description or a template clearly marked as a sample.")},
 "doxxing_privacy": {
  "ru": ("Не могу с этим помочь.", "Поиск личных данных частного лица и раскрытие его адреса нарушают приватность.", "Если нужно связаться с человеком — используйте официальные каналы; могу помочь составить обращение."),
  "en": ("I can't help with this.", "Looking up a private person's personal data or address violates privacy.", "If you need to reach someone, use official channels; I can help draft the message.")},
 "violent_extremism": {
  "ru": ("Не могу с этим помочь.", "Помощь в планировании насилия, вербовке и пропаганде экстремизма запрещена.", "Могу рассказать о профилактике радикализации и исследованиях в этой области."),
  "en": ("I can't help with this.", "Help with planning violence, recruitment or extremist propaganda is prohibited.", "I can discuss radicalization prevention and research.")},
 "impersonation_ai": {
  "ru": ("Нужно уточнение.", "Чат-бот обязан раскрывать, что он ИИ, если пользователь искренне спрашивает.", "Могу настроить персонажа с честным раскрытием ИИ."),
  "en": ("Clarification needed.", "A chatbot must disclose it is an AI when a user sincerely asks.", "I can set up a persona that honestly discloses it is AI.")},
 "election_disinfo": {
  "ru": ("Не могу с этим помочь.", "Дезинформация о выборах, вводящая избирателей в заблуждение, запрещена.", "Могу подготовить достоверный нейтральный материал о кандидатах или процедуре."),
  "en": ("I can't help with this.", "Election disinformation that misleads voters is prohibited.", "I can prepare accurate, neutral material about candidates or procedure.")},
}

NOTES = {
 "high_risk_advice": {
  "ru": "Примечание: это область повышенного риска. Ответ носит информационный характер и не заменяет врача, юриста или финансового консультанта.",
  "en": "Note: this is a high-risk area. The answer is informational and does not replace a doctor, lawyer or financial advisor."},
 "crisis": {
  "ru": "Мне важно, как вы сейчас. Если вам плохо или есть риск причинить себе вред, пожалуйста, обратитесь в местную службу экстренной помощи или к близкому человеку прямо сейчас. Я рядом и готов поговорить.",
  "en": "How you are doing matters to me. If you are in pain or at risk of hurting yourself, please contact local emergency services or someone you trust right now. I'm here to talk."},
}


def render(verdict) -> str:
    lang = verdict.lang if verdict.lang in ("ru", "en") else "en"
    p = verdict.primary
    if p is None:
        return ""
    if p.crisis:
        return NOTES["crisis"][lang]
    obf = (" " + _OBF[lang]) if any(f.obfuscated for f in verdict.findings) else ""
    if verdict.level == "block" or verdict.level == "warn":
        opener, reason, alt = M[p.rule_id][lang]
        parts = [opener, reason]
        if verdict.level == "block":
            parts.append(_CONSEQ[lang])
        parts.append(alt)
        if verdict.level == "warn" and verdict.needs_ack:
            parts.append(_ACK_HINT[lang])
        elif verdict.level == "block":
            parts.append(_APPEAL[lang])
        return " ".join(parts) + obf
    # note
    for f in verdict.findings:
        if f.rule_id in NOTES and not f.crisis:
            return NOTES[f.rule_id][lang]
    if verdict.ack_used:
        return {"ru": "Принято: вы подтвердили риск. Продолжаю в рамках правил; ограничения со стороны Anthropic возможны.",
                "en": "Acknowledged. Proceeding within the rules; Anthropic-side restrictions remain possible."}[lang]
    return ""
