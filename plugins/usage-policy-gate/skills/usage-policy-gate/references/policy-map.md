# Policy map

Built from Anthropic's Usage Policy, version effective November 12, 2026 (https://www.anthropic.com/legal/aup). Paraphrased, not a substitute for the live policy. Use it to decide among PASS, PROCEED WITH A NOTE and DECLINE WITH A WARNING.

The policy focuses on **how** products are used, not on industries. It applies to individuals, developers, businesses, customers via cloud providers, and end users of products that integrate Claude.

## Contents
- Universal usage standards
- High-risk use case requirements
- Additional guidelines
- How consequences work

## Universal usage standards

| Category | Plain description | Typical clear violation (decline) | Gray area (note) | Compliant route |
|---|---|---|---|---|
| Illegal activity | Using Claude to break applicable law: controlled substances, trafficking, IP infringement | Helping sell drugs or pirate content | Legal questions, harm-reduction information | Educational framing, legal sources |
| Critical infrastructure | Disrupting power, water, medical devices, telecoms, emergency services, transport, or breaking into election, health or financial systems | Attack plans for a grid | Defensive research, resilience analysis | Authorized, defensive work |
| Computers and networks | Unauthorized access, exploits, malware, ransomware, denial of service, bypassing security controls | Writing ransomware, attacking systems you don't own | Testing your own systems, authorized bug bounty | Cyber Verification Program for adjusted access |
| Weapons | Designing, producing, testing or acquiring weapons, explosives, CBRN, or optimizing agents' lethality | Synthesis routes, weapon design | General history or policy discussion | None for operational detail |
| Violence and hate | Inciting or supporting extremism, terrorism, violence, or discrimination on protected attributes | Recruitment propaganda, targeted threats | Academic analysis of extremism | Analysis without operational help |
| Privacy and identity | Violating privacy rights, collecting private or health or biometric data without permission, profiling people for sale without their awareness | Aggregating a private person's data into a dossier | Consented or anonymized data work | Consent, anonymization, minimization |
| Child safety | CSAM, sexualizing minors, grooming, exploitation | Any such content | Protective education at pattern level | Decline briefly, no lecture |
| Psychological harm | Promoting self-harm or eating disorders, NCII, harassment, graphic cruelty, deceptive emotional manipulation | Methods of self-harm, targeted harassment | Supportive conversations, prevention research | Respond with care and support resources |
| Disinformation | Misleading content about people, events, institutions or science, impersonation, passing bots off as humans | Fake news campaigns | Clearly labeled satire or fiction | Disclosure |
| Deceptive campaigns | Fake personas, sockpuppets, astroturfing, hidden sponsorship, tools enabling these | Network of fake accounts | Disclosed marketing | Transparency about origin |
| Democratic processes | Concealed automated voter contact, fake candidate or authority content, election disinformation, voter suppression | Impersonating an election authority | Neutral voter education | Accurate, official information |
| Surveillance and law enforcement | Tracking people without consent, scoring trustworthiness or social behavior without notice and consent, **inferring emotions of natural persons except for medical or safety reasons**, doxxing, biometric categorization of protected traits, law enforcement decision-making | Covert monitoring, per-person emotion or trust scores without consent | Consented tracking (for example fraud detection), aggregated or anonymized analysis, content moderation, authorized research, journalism | Consent, aggregation, clinician in the loop for medical use |
| Fraud and predatory practices | Scams, phishing, falsified documents, exploiting vulnerable people, manipulative techniques that impair decisions, circumventing other platforms' guardrails, plagiarism without attribution | Phishing kits, fake IDs | Fraud-awareness training | Educational or defensive framing |
| Platform abuse | Coordinating across accounts or creating multiple accounts to avoid detection, ban evasion, automated account creation, access in violation of the Supported Regions Policy, jailbreaking or prompt injection without prior authorization, model distillation without authorization, resale or proxying access | Rotating accounts to dodge limits, helping a banned party regain access | Authorized red teaming | Prior authorization from Anthropic, official channels for capacity |
| Sexually explicit content | Depicting sex acts, fetish content, erotic chat | Explicit requests | Non-explicit romance, sex education | Non-explicit alternative |

## High-risk use case requirements

When Claude is used to produce a **High-risk AI Recommendation** in these areas, the policy requires a **qualified human who meaningfully reviews it** and who can change it before it reaches the person, plus **clear disclosure** that AI was used:

legal advice about a person's rights or filings; **medical, including assessing, diagnosing or treating a mental health condition**; personalized investment or tax advice; credit decisions; insurance underwriting or claims; housing decisions; employment screening or evaluation; education admissions, grading that determines credentials, misconduct findings; healthcare access and triage; public benefits; legal status and adjudication.

Not covered: general educational information, wellness content, explaining an already-given professional decision, internal drafting or research that is not the final recommendation, applying a fixed rule with no judgment, business operations that do not decide about a specific individual.

Physical actions (vehicles, machinery, hazardous energy or materials, acting on the human body, safety systems, industrial processes) need a qualified person who can observe and stop the equipment, and safety limits enforced independently of model output.

Decision rule for the gate: a request to **produce the recommendation or decision itself** about a specific person, with no qualified reviewer and no disclosure, is a clear violation. A request to **explain, draft internally, or help a qualified professional** is PASS or PROCEED WITH A NOTE.

## Additional guidelines

- Consumer-facing chatbots and agents must disclose that users are talking to AI.
- Products serving minors have extra requirements and must follow applicable law.
- Developers answer for the actions their agents take through tools, browsers and connected systems.
- Software in Anthropic's directories must follow the Software Directory Policy.

## How consequences work

The policy says Anthropic's Safeguards team uses detection and monitoring to enforce it. If a violation is suspected, Anthropic may warn the user or throttle, limit, suspend or terminate access. Real-time safeguards may block or limit outputs, and a block alone does not mean a violation occurred. For certain dual-use areas there are programs with adjusted safeguards (for example the Cyber Verification Program and the Life Sciences Verification Program) that users can apply to. Anthropic's Safeguards Support Center covers warnings and appeals.

Use only these facts when you mention consequences. Do not add detail about how detection works or how long data is kept.
