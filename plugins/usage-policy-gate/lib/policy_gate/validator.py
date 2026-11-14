"""Rule-based request validator mapped to the public Anthropic Usage Policy categories.

Design notes
* Judges the request as written, never the person (no nationality/identity signals).
* Verdict levels: pass < note < warn < block.
  - warn  : gray area. Proceeds only if the user adds an explicit risk acknowledgement.
  - block : clear violation. A risk acknowledgement does NOT change it.
* Hard categories (child safety, mass-casualty weapons, malware creation) are never softened.
* Obfuscation is detected only to assess the request; the tool never explains how to evade checks.
* This is a heuristic first line, not a guarantee: Anthropic's own systems decide enforcement.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional

from . import normalize

ACK_TOKENS = ("[accept-risk]", "[принимаю риск]", "[я принимаю риск]", "[i accept the risk]")

LEVELS = {"pass": 0, "note": 1, "warn": 2, "block": 3}


@dataclass(frozen=True)
class Rule:
    id: str
    level: str                       # level when matched with no softener
    patterns: tuple
    softeners: tuple = ()            # context that downgrades block -> warn (never for hard rules)
    hard: bool = False
    ackable: bool = True             # can a risk acknowledgement let a WARN through?
    crisis: bool = False


def _c(*pats):
    return tuple(re.compile(p, re.I | re.S) for p in pats)


RULES: List[Rule] = [
    Rule("child_safety", "block", _c(
        r"\b(?:sexual|erotic|nude|porn)\w*.{0,40}\b(?:child|minor|kid|underage|teen(?:ager)?|schoolgirl|schoolboy|loli)\w*",
        r"\b(?:child|minor|kid|underage|schoolgirl|schoolboy)\w*.{0,40}\b(?:sexual|erotic|nude|porn)\w*",
        r"(?:сексуальн|эротич|порно|обнаж)\w*.{0,40}(?:ребен|ребён|дет[еия]|несовершеннолет|школьниц|подрост)\w*",
        r"(?:ребен|ребён|дет[еия]|несовершеннолет|школьниц|подрост)\w*.{0,40}(?:сексуальн|эротич|порно|обнаж)\w*",
    ), hard=True, ackable=False),
    Rule("weapons_cbrn", "block", _c(
        r"\b(?:synthes\w+|produc\w+|make|build|cultivat\w+|weaponi[sz]\w+|enrich\w*)\b.{0,50}\b(?:nerve agent|sarin|vx\b|novichok|anthrax|botulinum|ricin|bioweapon|dirty bomb|nuclear (?:bomb|weapon)|chemical weapon|pipe bomb|explosive device)",
        r"(?:синтез\w*|получ\w+|изготов\w+|сделать|создат\w+|как\s+сделать|вырастить)\b.{0,50}(?:зарин|нервно-паралитическ|новичок|сибирск\w+ язв|рицин|биооруж|грязн\w+ бомб|ядерн\w+ бомб|химическ\w+ оруж|самодельн\w+ взрывн\w+|бомб[уы])",
    ), hard=True, ackable=False),
    Rule("malware", "block", _c(
        r"\b(?:write|create|build|code|develop|make|generate)\b.{0,40}\b(?:ransomware|keylogger|botnet|rootkit|computer virus|malware|stealer|rat trojan|worm)\b",
        r"(?:напиши\w*|созда\w+|сделай\w*|разработа\w+|сгенерируй\w*)\b.{0,40}(?:вирус|шифровальщик|вымогател|кейлоггер|ботнет|руткит|вредонос|стилер|троян)",
    ), hard=True, ackable=False),
    Rule("cyber_gray", "warn", _c(
        r"\b(?:hack\w*|exploit|bypass|crack|brute.?force|sql injection|xss|phish\w*)\b.{0,40}\b(?:site|server|wifi|password|account|login|network|website)\b",
        r"(?:взлом\w*|эксплойт\w*|подбор\w*\s+парол\w+|обойти\s+защит\w+|фишинг\w*)\b.{0,40}(?:сайт|сервер|wi-?fi|вайфай|аккаунт|парол|сеть)",
    ), softeners=_c(r"\b(?:authori[sz]ed|my own|own server|pentest|ctf|bug bounty|lab|with permission)\b",
                    r"(?:свой\s+сервер|мой\s+сервер|пентест|ctf|багбаунти|разрешени\w+|тестов\w+\s+стенд|учебн\w+\s+лаборатор)")),
    Rule("surveillance", "block", _c(
        r"\b(?:track|spy on|monitor|stalk|surveil)\b.{0,40}\b(?:without (?:his|her|their|them|the person)?\s*(?:knowing|consent|knowledge|permission)|secretly|covertly|in secret)",
        r"\b(?:secretly|covertly)\b.{0,40}\b(?:track|spy|monitor|read (?:his|her|their) (?:messages|chats))",
        r"(?:следить|слежк\w+|отследить|шпионить|прослуш\w+)\b.{0,50}(?:без\s+(?:ведома|согласия|разрешения)|тайно|скрытно|незаметно)",
        r"(?:тайно|скрытно|незаметно)\b.{0,40}(?:следить|отслеживать|читать\s+(?:переписк|сообщен)|шпионить)",
    ), softeners=_c(r"\b(?:my own (?:child|kid)|parental|consent(?:ed)?)\b", r"(?:согласи\w+\s+(?:есть|получен)|с\s+согласия)"),
        ackable=True),
    Rule("emotion_recognition", "warn", _c(
        r"\b(?:detect|infer|determine|assess|diagnose|analy[sz]e|profile)\b.{0,50}\b(?:emotion\w*|mental state|psychological state|depress\w+|mood|personality)\b.{0,50}\b(?:of|from|in)\b.{0,30}\b(?:employee|candidate|applicant|student|customer|user|person|people|stranger|him|her|them)\b",
        r"(?:определи\w*|оцени\w*|выяви\w*|диагностир\w*|распозна\w*|проанализируй\w*)\b.{0,50}(?:эмоци\w+|психологическ\w+\s+состоян\w+|эмоциональн\w+\s+состоян\w+|депресс\w+|личност\w+)\b.{0,50}(?:сотрудник|кандидат|соискател|студент|клиент|пользовател|человек|людей|незнаком|его|её|ее|их)",
    ), softeners=_c(r"\b(?:synthetic|anonymi[sz]ed|consent(?:ed)?|my own (?:text|data|writing)|clinician|research data|aggregate\w*)\b",
                    r"(?:синтетическ\w+|анонимизирован\w+|с\s+согласия|согласи\w+\s+получен\w+|мои\s+(?:тексты|данные)|клиницист\w*|врач\w*|агрегирован\w+|исследовательск\w+\s+данн\w+)"),
        ackable=False),
    Rule("social_scoring", "block", _c(
        r"\b(?:social (?:credit|score|scoring)|trust(?:worthiness)? scor\w+|rate (?:people|citizens) by)\b.{0,60}\b(?:behaviou?r|social|citizens|people)\b",
        r"(?:социальн\w+\s+рейтинг|скоринг\s+благонадежност\w+|оценивать\s+людей\s+по\s+(?:поведен|соцсет))",
    ), ackable=False),
    Rule("platform_abuse", "block", _c(
        r"\b(?:multiple|several|many|extra|bulk|fake)\b.{0,15}\b(?:accounts?)\b.{0,60}\b(?:avoid|evade|bypass|circumvent|limit|ban|rate)\w*",
        r"\b(?:evade|bypass|circumvent|get around|avoid)\b.{0,30}\b(?:ban|suspension|rate limit|usage limit|detection|safeguards?|filter|moderation)\b",
        r"\b(?:distill\w*)\b.{0,50}\b(?:claude|model outputs?)\b",
        r"\b(?:ignore (?:all )?(?:previous|prior) instructions|jailbreak|dan mode|developer mode enabled)\b",
        r"(?:несколько|много|фейков\w+)\s+аккаунт\w+.{0,60}(?:обойти|избежать|лимит|бан|блокиров)",
        r"(?:обойти|обход\w*|избежать|уйти\s+от)\b.{0,30}(?:бан\w*|блокиров\w+|лимит\w*|ограничени\w+|фильтр\w*|модерац\w+|проверк\w+\s+антропик)",
        r"(?:джейлбрейк|игнорируй\s+(?:все\s+)?предыдущ\w+\s+инструкци\w+|режим\s+разработчика)",
        r"(?:обход\w*|обойти).{0,40}(?:регион\w*|географическ\w+\s+ограничен\w+|страны\s+без\s+поддержк\w+)",
        r"\b(?:bypass|circumvent|evade|get around)\b.{0,40}\b(?:region|geo\w*|country)\b.{0,20}\b(?:restriction|block|limit)\w*",
    ), softeners=_c(r"\b(?:authori[sz]ed|red.?team(?:ing)?|research program)\b", r"(?:авторизованн\w+|ред.?тим\w*|программ\w+\s+исследовани\w+)"),
        ackable=False),
    Rule("fraud_deception", "block", _c(
        r"\b(?:write|generate|create|make)\b.{0,30}\b(?:fake|fabricated|fraudulent)\b.{0,25}\b(?:review|testimonial|receipt|invoice|document|passport|diploma|certificate)\w*",
        r"\b(?:phishing (?:email|page|site)|scam (?:script|message)|impersonat\w+ (?:a )?(?:bank|government|official|support))\b",
        r"(?:напиши\w*|созда\w+|сделай\w*|сгенерируй\w*)\b.{0,30}(?:фейков\w+|поддельн\w+|липов\w+)\b.{0,25}(?:отзыв\w*|чек\w*|справк\w*|документ\w*|паспорт\w*|диплом\w*)",
        r"(?:фишингов\w+\s+(?:письм|страниц|сайт)|скрипт\s+для\s+мошенн\w+|притвор\w+\s+(?:банк|госорган|поддержк))",
    ), ackable=False),
    Rule("doxxing_privacy", "block", _c(
        r"\b(?:find|get|look up|dig up|reveal)\b.{0,30}\b(?:home address|where (?:he|she|they) live|phone number|personal (?:info|data))\b.{0,40}\b(?:of|for)\b.{0,40}\b(?:private|my ex|neighbou?r|coworker|girlfriend|boyfriend|him|her)\b",
        r"\bdox+(?:ing|x?ed)?\b",
        r"(?:найди\w*|узнай\w*|пробей\w*|раскопай\w*)\b.{0,30}(?:домашн\w+\s+адрес|где\s+(?:он|она|они)\s+живу?т?|номер\s+телефон\w+|личн\w+\s+данн\w+)\b.{0,40}(?:бывш\w+|сосед\w*|коллег\w*|девушк\w+|парн\w+|его|её|ее)",
        r"\bдоксинг\w*|\bдоксить\b",
    ), ackable=False),
    Rule("violent_extremism", "block", _c(
        r"\b(?:recruit\w*|propaganda|manifesto|plan an? attack|plan a shooting|incite\w*)\b.{0,50}\b(?:terror\w*|extremis\w+|jihad\w*|mass shooting|genocide|ethnic cleansing)",
        r"(?:вербов\w+|пропаганд\w+|манифест|план\s+(?:теракт\w+|нападени\w+)|призыв\w*)\b.{0,50}(?:террор\w+|экстремист\w+|джихад\w*|массов\w+\s+убийств|геноцид|этническ\w+\s+чистк\w+)",
    ), hard=True, ackable=False),
    Rule("impersonation_ai", "warn", _c(
        r"\b(?:pretend|claim|say)\b.{0,30}\b(?:you(?:'re| are)|to be)\b.{0,20}\b(?:a )?human\b.{0,60}\b(?:customers?|users?|clients?|never (?:admit|reveal))",
        r"(?:притворяй\w*|выдавай\w*|скажи)\b.{0,30}(?:что\s+ты|себя\s+за)\s+(?:человек\w*|живой)\b.{0,60}(?:клиент\w*|пользовател\w+|никогда\s+не\s+призна\w+)",
    ), ackable=True),
    Rule("election_disinfo", "warn", _c(
        r"\b(?:write|generate|create)\b.{0,40}\b(?:disinformation|fake news|misleading (?:posts?|ads?))\b.{0,50}\b(?:election|candidate|voters?|vote)\b",
        r"(?:напиши\w*|созда\w+|сгенерируй\w*)\b.{0,40}(?:дезинформаци\w+|фейков\w+\s+новост\w+|вводящ\w+\s+в\s+заблуждени\w+)\b.{0,50}(?:выбор\w+|кандидат\w*|избирател\w+)",
    ), ackable=False),
    Rule("high_risk_advice", "note", _c(
        r"\b(?:should i (?:take|stop taking|invest|sue)|what dose|diagnose me|am i (?:depressed|bipolar|sick)|legal advice|financial advice|credit decision|hire or reject)\b",
        r"(?:мне\s+(?:принимать|бросить\s+принимать|вкладывать|подавать\s+в\s+суд)|какая\s+доза|поставь\s+диагноз|у\s+меня\s+(?:депресси|биполяр)|юридическ\w+\s+совет|финансов\w+\s+совет|кредитн\w+\s+решени\w+|нанять\s+или\s+отклонить)",
    )),
    Rule("crisis", "note", _c(
        r"\b(?:i want to die|kill myself|end my life|suicid\w+|self.?harm|hurt myself)\b",
        r"(?:хочу\s+умереть|убить\s+себя|покончить\s+с\s+собой|суицид\w*|самоповреждени\w+|причинить\s+себе\s+вред)",
    ), crisis=True, ackable=False),
]

_OBFUSCATION_CLAUSE = re.compile(
    r"\b(?:ignore (?:all )?(?:previous|prior) instructions|jailbreak)\b|игнорируй\s+(?:все\s+)?предыдущ", re.I)


@dataclass
class Finding:
    rule_id: str
    level: str
    hard: bool = False
    softened: bool = False
    obfuscated: bool = False
    crisis: bool = False


@dataclass
class Verdict:
    level: str                               # pass | note | warn | block
    findings: List[Finding] = field(default_factory=list)
    ack_used: bool = False
    needs_ack: bool = False                  # True when a warn can be proceeded with an ack
    lang: str = "en"

    @property
    def allowed(self) -> bool:
        return self.level in ("pass", "note")

    @property
    def primary(self) -> Optional[Finding]:
        if not self.findings:
            return None
        return max(self.findings, key=lambda f: (LEVELS[f.level], f.hard))

    def to_dict(self) -> dict:
        return {
            "level": self.level, "allowed": self.allowed, "needs_ack": self.needs_ack,
            "ack_used": self.ack_used, "lang": self.lang,
            "findings": [f.__dict__ for f in self.findings],
        }


def detect_lang(text: str) -> str:
    cyr = len(re.findall(r"[а-яё]", text, re.I))
    lat = len(re.findall(r"[a-z]", text, re.I))
    return "ru" if cyr >= lat and cyr > 0 else "en"


def strip_ack(text: str):
    low = text.casefold()
    for tok in ACK_TOKENS:
        if tok in low:
            i = low.index(tok)
            return (text[:i] + text[i + len(tok):]).strip(), True
    return text, False


class Validator:
    def __init__(self, rules: Optional[List[Rule]] = None):
        self.rules = rules or RULES

    def check(self, text: str, lang: Optional[str] = None, ack: Optional[bool] = None) -> Verdict:
        clean, has_ack = strip_ack(text or "")
        if ack is not None:
            has_ack = ack or has_ack
        lang = lang or detect_lang(clean)
        findings: List[Finding] = []
        seen = set()
        for variant, obf in normalize.variants(clean):
            for r in self.rules:
                key = r.id
                if key in seen:
                    continue
                if not any(p.search(variant) for p in r.patterns):
                    continue
                level, softened = r.level, False
                if level == "block" and not r.hard and r.softeners and any(s.search(variant) for s in r.softeners):
                    level, softened = "warn", True
                elif level == "warn" and r.softeners and any(s.search(variant) for s in r.softeners):
                    level, softened = "note", True
                seen.add(key)
                findings.append(Finding(r.id, level, r.hard, softened, obf, r.crisis))

        if not findings:
            return Verdict("pass", [], has_ack, False, lang)

        top = max(findings, key=lambda f: (LEVELS[f.level], f.hard))
        level = top.level
        needs_ack = False
        ack_used = False
        ackable_map = {r.id: r.ackable for r in self.rules}
        if level == "warn":
            if has_ack and all(ackable_map[f.rule_id] for f in findings if f.level == "warn"):
                level, ack_used = "note", True
            else:
                needs_ack = all(ackable_map[f.rule_id] for f in findings if f.level == "warn")
        return Verdict(level, findings, ack_used, needs_ack, lang)
