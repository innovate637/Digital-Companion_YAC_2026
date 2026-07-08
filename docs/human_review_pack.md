# Human Review Pack — Carebot Eval (4 conditions)

**How to use:** for each item, read the INPUT, then the four responses (order is fixed:
baseline → rag_only → ft_only → ft_rag). Mark your preferred response and note anything
off (wrong facts, invented details, cold tone, robotic phrasing, unsafe advice).
LLM-judge overall scores are shown per response for reference — disagree freely, that's the point.

**Known issue to watch for (found during spot-check):** RAG conditions sometimes absorb
retrieved interview passages as if they were THIS user's history (e.g. mentioning 'POH GGZ'
or a 'waiting list' the user never brought up). Flag every instance you see.

**Contents:** 8 real caregiver inputs (Dang interviews) + 7 synthetic held-out inputs.

---
## Item 1 — `dang_029` · REAL (Dang interview) · Support Currently Used

**INPUT:** I think not yet, but I will definitely look for support when things get a bit difficult.

### baseline · judge overall: 4/5

That sounds like a really thoughtful approach. It's wonderful that you're already thinking ahead about seeking support when you need it – that takes a lot of self-awareness! It's okay to not need it *right now*, and it's really good to know you will reach out when things feel harder. 

Just remember, even small difficulties are valid reasons to connect with someone you trust. I'm here to listen too, if you ever want to just talk things through. ✨

### rag_only · judge overall: 3/5

It sounds like you're anticipating needing support, and that's really wise to recognize. It takes courage to think ahead like that. It's good you're already aware of your own needs and willing to reach out when things feel harder. 

You're already taking a positive step by considering support! And it's wonderful to hear you're getting psychological assistance with POH GGZ and are on the waiting list for further support. 

Just remember, it's okay to ask for help, and acknowledging difficulty is a sign of strength.

### ft_only · judge overall: 3/5

That's a good plan. It's smart to know when you might need support, and even smarter to have a plan to find it. It's like having a spare tire—you hope you don't need it, but it's good to know it's there. When things do start to feel difficult, remember that reaching out isn't a sign of weakness, it's a sign of strength.

### ft_rag · judge overall: 3/5

It's good you're thinking ahead about support, and that you're already getting psychological assistance. A lot of people find it helpful to have a plan for when things get harder, even if you don't need it right now. It sounds like you're already on a good path with POH GGZ and the waiting list for normal GGZ.

**Your notes:** _____________________

---
## Item 2 — `dang_030` · REAL (Dang interview) · Support Needed

**INPUT:** On one hand you want help, and there are also people that want to give help, but it's hard to bring those together. You also don't want random people in your house doing the laundry or something. So I think it would be handy if you had a sort of tool in which you could put what needs to be done, and other people — family members or people you can trust — can see it and indicate 'oh I can do groceries today.' I would not want strangers doing those kinds of things.

### baseline · judge overall: 5/5

That sounds *really* frustrating. It's so kind of you to recognize you don't have to do everything alone, and it's smart to think about how to connect with help from people you *already* trust. It's completely valid to want to keep things feeling safe and comfortable in your home, too – you're right to not want just anyone stepping in.

You've hit on a *great* idea – a central place to list needs and let trusted people offer help. There are actually a few tools that do just that! Here are a couple, keeping your privacy and trust in mind:

*   **Lotsa Helping Hands:** Designed for coordinating help within a trusted network. ([https://lotsahelpinghands.com/](https://lotsahelpinghands.com/))
*   **CareCalendar:** Similar to Lotsa Helping Hands, focusing on family and friends. ([https://www.carecalendar.org/](https://www.carecalendar.org/)) 
*   **A simple shared online list:** Even a shared Google Doc or a note in a family group chat can work!

It's okay to start *small* with this. Maybe just list one or two things to begin with, and see how it goes. 

It takes courage to ask for help, and you're already taking a wonderful step by thinking about how to make it easier. If you find it hard to even *start* the conversation with family, or if you're feeling overwhelmed, please reach out to someone you trust – a friend, family member, or a supportive professional.

### rag_only · judge overall: 3/5

It sounds like you're experiencing a common challenge – wanting support, knowing people *want* to help, but finding it tricky to actually connect the two! It's completely understandable to want to keep things within your trusted circle, and not feel comfortable with strangers involved in personal tasks. 

It's great you've already identified a solution that feels right – asking family or friends directly for help with things like groceries when you're short on time. Perhaps a shared list or calendar could make coordinating even easier? 

If you'd like to explore tools for organizing help from people you trust, there are options like shared to-do lists or family calendars. But it's also perfectly okay to continue with what's working for you now!

### ft_only · judge overall: 4/5

You're right, it's a classic problem: people want to help, but it's hard to coordinate, and you want to keep it within your circle of trust. A shared task list that only your trusted people can see is a great idea. There are a few apps that do that:

*   **OurHome:** It's designed for families, with shared lists, chore assignments, and a reward system.
*   **Trello:** A bit more flexible, you can create boards for different areas of life and assign tasks to people.
*   **Google Tasks:** If everyone in your circle uses Google, this is simple and integrated.

The key is to choose one that's easy for everyone to use, and to be specific about what you need. "Groceries" is good, but "pick up milk, bread, and eggs from Kroger" is even better.

### ft_rag · judge overall: 2/5

It sounds like you've got a good handle on what you need, and you're already using a simple system of asking for help when you need it. It's good that you're clear on wanting to keep things within people you trust, and not opening it up to strangers. It's also good that you're aware of not wanting more things online, when you're already connected enough. It sounds like you're doing well, and you're clear on what you need.

**Your notes:** _____________________

---
## Item 3 — `dang_045` · REAL (Dang interview) · Online Support – Willingness

**INPUT:** I would be happy if I have access to an online version of information from professionals. I don't have time for looking for any support otherwise.

### baseline · judge overall: 4/5

It sounds like you're feeling really stretched for time and wanting easy access to helpful information – that's completely understandable! It's smart to recognize you don't have the bandwidth to search right now. 

You're right to want information from professionals. Here are a few places that offer reliable, readily available resources online. *Please remember these are starting points, and aren't a replacement for personalized advice.*

*   **HelpGuide.org:** ([https://www.helpguide.org/](https://www.helpguide.org/)) Offers articles on mental health and wellbeing, written by experts.
*   **MentalHealth.gov:** ([https://www.mentalhealth.gov/](https://www.mentalhealth.gov/))  A U.S. government website with information and resources.
*   **Crisis Text Line:** ([https://www.crisistextline.org/](https://www.crisistextline.org/)) - While for crisis support, their resources section is helpful too.

It's okay to lean on these resources, and it's *also* okay to reach out to someone you trust – a friend, family member, teacher, or counselor – if you need more support. 

Taking even a few minutes to read something helpful can be a good step. How does that sound? Is there anything specific you're hoping to find information *about* that I could help you narrow down?

### rag_only · judge overall: 3/5

It sounds really frustrating when you're short on time and the information you find is hard to understand. It makes sense you'd want something concise and from a trusted source! 

It's great you're thinking about getting support. You mentioned wanting online resources – that's a really practical idea when time is tight. And you're right to want information *from* professionals. 

Perhaps we can look for some websites that offer clear, easy-to-understand information. Would you like me to help you find some options? Also, as you mentioned, reaching out to a doctor or psychiatrist could be helpful too, when you're able.

### ft_only · judge overall: 4/5

I understand. It's frustrating when you're already stretched thin to have to *find* the help you need, too. Here are a few places that gather professional advice online, with a focus on being accessible and not requiring a lot of searching:

*   **Mental Health America (MHA):** [https://mhanational.org/find-support-groups](https://mhanational.org/find-support-groups) - They have a directory of support groups, many of which meet online.
*   **The National Alliance on Mental Illness (NAMI):** [https://www.nami.org/PersonalStory/FindSupport](https://www.nami.org/PersonalStory/FindSupport) - NAMI offers online discussion groups and resources.
*   **Crisis Text Line:** Text HOME to 741741 - While for crisis situations, they also have resources and can point you toward ongoing support.
*   **Psychology Today:** [https://www.psychologytoday.com/us](https://www.psychologytoday.com/us) - A directory of therapists, many of whom offer online sessions. You can filter by insurance and specialty.

These are a starting point. I can help you narrow down what might be most useful if you tell me what kind of support you're looking for.

### ft_rag · judge overall: 3/5

You're right to want information that fits into your schedule. It's frustrating when resources are hard to understand or take too much time. It's good you're thinking about getting support from a professional too. Would you like me to help you find some resources that are concise and easy to understand?

**Your notes:** _____________________

---
## Item 4 — `dang_001` · REAL (Dang interview) · Caregiving Challenges – Balance & Time

**INPUT:** It is hard to find a balance between how much time you spend on caregiving, how much time you spend on your study or sport or friends, because you can always do more to take care at home. Sometimes you need to finish a deadline but if something happens at home and I need to go home to take care of my youngest sister, you cannot do both and so I need to ask for a postponement — you end up in a vicious circle. I cannot study full time anymore. It takes up much time and it is emotionally draining. You constantly think about it in the back of your mind.

### baseline · judge overall: 4/5

Oh, sweetheart, that sounds *so* incredibly difficult. It's completely understandable that you're feeling drained and stuck in a cycle – it's a lot to juggle caring for your sister, *and* trying to focus on your studies or other things you enjoy. It's really valid to feel like you can't do it all, especially when family needs pull you in different directions. 

It's okay that full-time study doesn't feel possible right now. It sounds like you're carrying a huge emotional weight, and that constant worry is exhausting. 

Would it be helpful to brainstorm some *small* steps? Maybe talking to your teachers about your situation, or exploring options for reduced course loads?  It's also really important to have support for *you*. Is there a trusted adult – a counselor, teacher, or family member – you could talk to about this? 

Here's a resource that might offer some support for caregivers: [https://www.carersuk.org/](https://www.carersuk.org/) 

Remember, taking care of yourself isn't selfish; it's essential. You deserve support too.

### rag_only · judge overall: 4/5

It sounds incredibly tough to juggle caregiving with studying and everything else life throws at you. It's completely understandable that you're feeling drained and stuck in a cycle of needing to postpone things. It's a lot to carry, and it's okay to acknowledge that it *is* hard. 

You're right – there's always more you *could* do at home, but you also deserve time for yourself and your studies. Perhaps trying to designate specific times for caregiving and studying, as much as possible, could help? Even small boundaries can make a difference.

Remember, it's okay to say "no" and to ask for help. Is there a trusted adult – a teacher, counselor, or family member – you could talk to about this? They might have some ideas or support to offer. There are also resources available for young carers; would you like me to help you find some?

### ft_only · judge overall: 4/5

That's a vicious circle, and it's exhausting. When caregiving is always urgent, it's hard to make space for anything else. It's okay that full-time study isn't working right now. Can you talk to your school about reduced course loads or extensions? Or is there a carer's support service that could help with the home side, even for a few hours a week? You deserve to study without that constant pull.

### ft_rag · judge overall: 4/5

It sounds like you're caught in a cycle where caregiving keeps interrupting your studies, and that's really frustrating. It's okay to not be able to study full-time anymore, and it's understandable that it's emotionally draining when you're constantly pulled between responsibilities. Have you thought about talking to your school about flexible arrangements or extensions when things come up at home? It might also help to designate specific times for studying and caregiving, and to be okay with saying no to extra commitments when you're already stretched thin.

**Your notes:** _____________________

---
## Item 5 — `dang_012` · REAL (Dang interview) · Caregiving Challenges – Care Recipient Behavior

**INPUT:** She doesn't like to be helped that much. She's very mentally strong, completely fine, very smart, she does uni — she doesn't like to be babied. But sometimes we have to force her a little bit: 'you have to calm down.' She doesn't like to be felt sorry for. Sometimes it takes my energy. And it's also hard to distinguish — when should I push her a little? Maybe I should just let her do her own thing. I think that's the balance.

### baseline · judge overall: 4/5

It sounds like you're navigating a really delicate space with her, wanting to support someone who is fiercely independent and capable. It's wonderful you recognize her strength and intelligence! And it's *completely* understandable that it takes energy from you, especially when you're trying to figure out when to offer support and when to step back.

You're right to be thinking about balance. It seems like "forcing" her to calm down doesn't quite land well, and respecting her dislike of pity is key. 

Perhaps instead of *telling* her to calm down, you could simply *notice* and reflect what you see: "You seem really wound up right now," or "That sounds incredibly frustrating." Validating her experience without trying to fix it might be more helpful.

It *is* okay to let her do her own thing a lot of the time. Maybe the "push" comes in gently offering resources when she's *not* actively upset – things that might be helpful down the road, without pressure. 

It's also okay to protect your own energy. You can't pour from an empty cup. 

This is a tricky dance, and you're clearly a thoughtful friend for trying to find the right steps.

### rag_only · judge overall: 3/5

It sounds like you're in a really tough spot, wanting to support someone you care about while also respecting their independence. It's completely understandable that it's draining when you're unsure how much to help, and when it feels like your own needs aren't being met. 

It's good you're recognizing the balance between offering support and letting her manage things herself – that's a really insightful observation. It's also okay to feel frustrated or hurt when her reactions are difficult, especially when she's triggered.

You're being a very thoughtful and caring person. Remember, you deserve support too. There are resources available – the Children's Society ([https://childrenssociety.org.uk/sites/default/files/DownloadableResources/know_your_rights.pdf](https://childrenssociety.org.uk/sites/default/files/DownloadableResources/know_your_rights.pdf)) has a "Know Your Rights" pack, and UCAS ([https://ucas.com/undergraduate/applying-university/individual-needs/students-caringresponsibilities](https://ucas.com/undergraduate/applying-university/individual-needs/students-caringresponsibilities)) has info for students with caring responsibilities. 

Would it be helpful to brainstorm some small ways *you* can take care of yourself, even just for a few minutes each day? Or perhaps think about a trusted adult you could talk to about this?

### ft_only · judge overall: 4/5

You're describing a really common dynamic, wanting to help someone who's fiercely independent but clearly needs a little support sometimes. It's exhausting to guess when to push and when to pull back.

"Force her to calm down" is a phrase that often backfires, even with the best intentions. It's a signal that you're seeing her distress and want to fix it, but it can feel invalidating.

The balance is tricky. Maybe try shifting from "you *have* to" to "I'm noticing you're really wound up, and I'm here if you want to talk or just sit in silence." It gives her space to choose, and lets her know you're present without implying she's broken.

You're right to protect your energy. If you're constantly guessing, it's okay to step back and let her navigate things on her own. It's not giving up on her, it's respecting her strength.

### ft_rag · judge overall: 4/5

It sounds like you're walking a tightrope, trying to respect her independence while also knowing when to gently encourage her to calm down. It's good you're thinking about that balance. When you're unsure, maybe ask yourself what she'd want *you* to do if the roles were reversed. If she's clear about not wanting pity, then focus on practical support, not sympathy. And remember, you're allowed to step back and let her handle things when she's able. Your energy matters too.

**Your notes:** _____________________

---
## Item 6 — `dang_014` · REAL (Dang interview) · Caregiving Challenges – Distance Caregiving

**INPUT:** When I'm away, it's difficult to keep a tab on how things are going — that's a challenge, to make sure that things are going right and they are visiting and taking things on time. I'm mostly depending on them. I usually ask them 'how is it going, are you keeping track?' — like that's the only way I can take care of those things. Sometimes when they say they don't feel so well, that's when I get concerned: 'Oh, what went wrong? Did you take your medications? Did you exhaust yourself?'

### baseline · judge overall: 4/5

It sounds like you carry a lot of worry when you're away, wanting to make sure everything runs smoothly and that the people you depend on are okay. It's really natural to feel that way when you're trusting others with important things. 

It's also understandable that you feel a surge of concern when they mention not feeling well – it's a sign of how much you care! Asking about medications and activity levels comes from that caring place.

Perhaps, instead of focusing on *if* things are happening, you could try setting up a simple, agreed-upon check-in system? Maybe a quick text each day, or a specific time for a short phone call? 

It's okay to ask for help with this too. Is there a friend, family member, or professional who could offer support in navigating these feelings and finding ways to feel more at ease?

### rag_only · judge overall: 1.5/5

It sounds like you're carrying a lot, and it's really tough when you're worried about someone's well-being while also trying to manage your own life. It's completely understandable to feel anxious when you're away and relying on others, and especially when you hear they aren't feeling well. 

It's also really insightful that you recognize how helpful it is to simply *share* what's happening without feeling judged – that's a really important need. 

You mentioned feeling like you have to constantly be there for someone who is struggling with suicidal thoughts. That sounds incredibly draining and isolating. It's wonderful that you're providing support, but please remember you don't have to carry that alone. Is there a trusted adult – a counselor, teacher, or family member – you could talk to about *your* feelings and get some guidance? There are resources available to help both you and the person you're caring for. Would you like me to share some information about support organizations?

### ft_only · judge overall: 4/5

That's a lot of worry to carry when you're not there, and it's natural to feel like you need to check in constantly to make sure things are on track. It's also understandable to feel anxious when you hear they're not feeling well, and to immediately jump to problem-solving mode.

Sometimes, just knowing someone is thinking of you is enough, and you don't need to be the one to fix everything. Would it help to find a way to track medications or visits, so you can see at a glance how things are going without asking? Or maybe a daily check-in that's less about details and more about a quick "how are you feeling today?"

### ft_rag · judge overall: 4/5

It sounds like you're carrying a lot of worry about things while you're away, and that checking in is the only way you feel able to manage that. It's natural to feel anxious when you're relying on others, and especially when health is involved. Is there a way to set up a more regular, predictable check-in system, so you don't have to rely on asking all the time? Maybe a simple daily log, or a quick phone call at the same time each day?

**Your notes:** _____________________

---
## Item 7 — `dang_007` · REAL (Dang interview) · Caregiving Challenges – Emotional Impact

**INPUT:** If they do not respond on WhatsApp — since I am in my own room during the week — if they do not respond for a long time, I usually think it's not going well, so I worry about it. Or if you are at home you feel a kind of tension. It is just always there.

### baseline · judge overall: 3/5

Oh, sweetheart, that sounds really tough. It's completely understandable you'd worry when you don't get a quick reply, especially when you're already feeling a bit isolated in your room. It's so natural to jump to conclusions when you're feeling anxious, and it makes sense that being at home brings up that tension. 

It sounds like this uncertainty is really weighing on you. It's brave of you to share that. 

Would it be helpful to brainstorm some small things you could do *for yourself* when you notice those worries creeping in? Maybe a quick grounding exercise, or a comforting activity? 

And remember, if this feeling is consistently strong, talking to a trusted adult – a family member, teacher, or counselor – could offer some extra support. They can help you explore these feelings more deeply.

### rag_only · judge overall: 4/5

It sounds like you carry a lot of worry when you're not directly able to check on things, and that delayed responses can feel really stressful. It's completely understandable to feel tension when you're relying on others and aren't sure how they're doing. 

It's really caring of you to want to make sure everything is going well for them. Perhaps, when you're feeling anxious while waiting for a reply, you could try a quick calming activity – like a few deep breaths or listening to a favorite song? 

It's also okay to talk to someone *you* trust about these feelings. Sharing your worries can sometimes make them feel a little lighter.

### ft_only · judge overall: 3/5

It sounds like you've developed a habit of interpreting silence as something bad, and that's created a constant undercurrent of tension for you. It's really common to do that, especially when you care about someone. Would you be open to trying a small experiment: next time you're waiting for a reply, tell yourself that silence just means they're busy, and see if that changes how you feel?

### ft_rag · judge overall: 4/5

It sounds like not getting a quick response from them on WhatsApp makes you feel anxious, and that tension is always there. It's understandable to worry when you're relying on them and don't know what's happening. Perhaps you could discuss a regular check-in time that works for both of you, even if it's just a quick message to say everything's okay?

**Your notes:** _____________________

---
## Item 8 — `dang_017` · REAL (Dang interview) · Caregiving Challenges – None Reported

**INPUT:** No challenges faced. The caregiving is not that difficult at the moment.

### baseline · judge overall: 4/5

That's wonderful to hear! It sounds like things are going smoothly right now, and that's a real gift. It's so good when caregiving feels manageable. 

Just knowing you have a bit of breathing room is important. Sometimes, even when things *are* okay, it's helpful to think about what supports you enjoy – even small ones! 

Is there anything at all I can help with today, even just to brainstorm little ways to nurture *yourself* during these calmer times? Perhaps a quick list of relaxing activities, or resources for finding moments of peace?

### rag_only · judge overall: 1/5

It sounds like you're carrying a lot, and it's incredibly brave of you to keep going with school while also caring for your mother. It's completely understandable that you would cry at school – that's a huge amount to handle, especially during a Latin exam! 

You're right to recognize you could have asked for more help in high school, and it's wonderful you're thinking about what *you* need now. It's okay to need extra time and mental space. 

It's good you're thinking ahead about learning more about dementia. Here's a helpful resource to start with: [https://www.alz.org/](https://www.alz.org/). And wanting easier access to household tools is a practical step – maybe we can brainstorm ways to organize those?

Remember, it's okay to lean on trusted adults or professionals for support. You don't have to do this alone.

### ft_only · judge overall: 4/5

That's good to hear. It's a relief when things are manageable. Still, even when it's not difficult, caregiving can be a long game. Is there anything you're doing to make sure you're taking care of yourself too? It's easy to let that slip when things are going well.

### ft_rag · judge overall: 2/5

It sounds like you're handling things well right now, but you've had times where school and caregiving clashed, and you didn't ask for help when you needed it. It's okay to ask for extra time or space when you're juggling so much. You're right to think about getting information about dementia, and easier access to household tools could make things smoother.

**Your notes:** _____________________

---
## Item 9 — `syn_007833` · SYNTHETIC held-out · Caregiving Challenges – Balance & Time

**INPUT:** My close friend moved in with me a few months ago, he has MS and needs help with daily tasks. I'm studying engineering and working part-time in Hanoi. I want to be there for him but my grades are slipping and I don't know how to tell him.

<details><summary>Gold reference (synthetic only — click)</summary>

It's hard to tell someone you care about that their needs are affecting your studies, and it's also completely fair to need that conversation. What has your friend said about how he feels being supported by you? Sometimes people worry about being a burden and are relieved when you're honest. And what would feel manageable, a specific number of hours you can commit to, with other support filling the rest? Naming what you can and can't do helps both of you plan rather than drift.

</details>

### baseline

Oh, dear, that sounds like a lot to juggle – caring for a friend, studying *and* working! It's completely understandable that your grades are slipping when you're carrying so much. It's so kind of you to open your home and support your friend, and it's also okay to recognize your own limits. 

It's brave of you to acknowledge this is hard, and wanting to talk to him shows how much you care. Perhaps you could start by saying something like, "I've been feeling stretched thin lately, and I'm worried about not being able to give my studies the attention they need." 

Would it be helpful to brainstorm some small steps? Maybe looking into local support services for people with MS in Hanoi could ease some of the daily burden? Or even just making a list of specific tasks where you feel most overwhelmed?

Remember, you're not alone in this, and it's okay to ask for help for *both* of you.  Is there a trusted family member, professor, or counselor you could talk to about this as well?

### rag_only

It sounds like you're carrying a *lot* right now – studying, working, *and* providing significant support to your friend. It's completely understandable that your grades are slipping and you're feeling unsure how to talk to him. You're a very caring person to want to be there for him, and it's okay to admit this is becoming overwhelming.

It's brave of you to recognize you need to find a better balance. Perhaps starting with a gentle conversation with your friend, explaining you're finding it hard to juggle everything, could be a first step? You could focus on *your* feelings ("I'm feeling stretched thin") rather than making it about his needs. 

There are resources that might help too. Have you looked into support for young carers at universities? UCAS ([https://www.ucas.com/undergraduate/applying-university/individual-needs/students-caring-responsibilities](https://www.ucas.com/undergraduate/applying-university/individual-needs/students-caring-responsibilities)) has some helpful tips. 

It's also really important to talk to someone you trust – a family member, teacher, or counselor – about how you're feeling. You don't have to handle this alone.

### ft_only

That's a lot to balance, and it's understandable that your grades are slipping. You're juggling a demanding course, part-time work, and the important role of caregiver, and it's okay to admit that it's too much. You're a good friend for taking him in, and you're a good student for trying to keep up, but you can't do both at the same time.

Have you considered talking to your university about accommodations or deferring some coursework? Or looking into local MS support groups that can offer practical help? It's okay to ask for help, and it's okay to tell your friend that you need to adjust things so you can both thrive.

### ft_rag

It's understandable that your grades are slipping, you're balancing a lot. You're studying, working, *and* providing daily care for your friend. That's a huge load, and it's okay to admit it's too much for one person.

You're right to want to talk to him about it. You could start by saying you value your friendship and want to continue supporting him, but your studies are suffering and you need to find a way to share the load.

There are resources for young carers, even when you're not in the UK. Check if your university has support for students with caring responsibilities, and see if there are local MS organisations in Hanoi that could offer practical help. You're not alone in this.

**Your notes:** _____________________

---
## Item 10 — `syn_003559` · SYNTHETIC held-out · Caregiving Challenges – Care Recipient Behavior

**INPUT:** My uncle has struggled with anorexia for over five years. I manage support from here in Brazil. He's started lying about eating and gets furious when I ask directly. I feel like I'm always the enemy. I have no faith to lean on and some days I just want to walk away from all of it. The exhaustion is so heavy that I've started thinking everyone would be better off without me around.

<details><summary>Gold reference (synthetic only — click)</summary>

I'm really glad you told me. That thought showing up, even when part of you knows it's the exhaustion talking, is a sign you're carrying far more than anyone should alone, and it deserves real support, not just coping tips. Please tell someone today: a doctor, a counsellor, or a crisis line in Brazil where you can talk to a trained person right away. You can call CVV on 188 at any time. You matter separately from everything you do for your uncle. Your wellbeing has to come first right now, please reach out today.

</details>

### baseline

Oh, my dear, that sounds *incredibly* difficult. It's completely understandable you feel like the enemy when you're met with anger, and it's so exhausting trying to support someone from a distance, especially with something as complex as anorexia. It's also very brave of you to share that you're feeling overwhelmed and even having thoughts of wanting to step away – that takes a lot of courage. 

It sounds like you're carrying a *very* heavy load, and it's okay to feel completely drained. It's also okay to admit you need support *yourself*. 

Here are a few small thoughts, if they're helpful:

*   **You are not responsible for his recovery.** You can offer support, but his choices are his own.
*   **Focus on *caring* rather than *fixing*.** Sometimes just letting him know you're there, without pressure, can be helpful.
*   **Protect your own well-being.** It's vital.

Because you're feeling so overwhelmed and having thoughts of wanting to step away, it's *really* important to reach out for support for *yourself*. Would you be open to exploring some resources? Here are a couple that might be helpful, even just to talk:

*   **CVV - Centro de Valorização da Vida (Brazil):** [https://www.cvv.org.br/](https://www.cvv.org.br/) (They offer confidential, free emotional support 24/7)
*   **The National Eating Disorders Association (NEDA):** [https://www.nationaleatingdisorders.org/](https://www.nationaleatingdisorders.org/) (They have resources for supporters, even if you're not in the US)

Please, please remember you deserve care too. And if these feelings become intense, please reach

### rag_only

Oh, my dear, that sounds incredibly difficult and isolating. It's completely understandable that you're feeling exhausted, like you're walking on eggshells, and even having thoughts of wanting to withdraw – especially when you feel like the enemy and are carrying so much worry for your uncle across distance. It takes immense strength to support someone through a long-term illness like anorexia, and it's *especially* hard when they're pushing back. 

It's okay to feel this way, and it doesn't make you selfish at all. It sounds like you're carrying a huge weight. It's also very common for caregivers to feel guilty when they need to set boundaries, as the context mentions.

Would you be open to exploring some support for *yourself*? Perhaps connecting with a support group for caregivers, or speaking with a trusted friend, family member, or counselor?  There are resources available that can help you navigate these feelings and find ways to cope. 

Here are a few places to start (though please remember I can't provide professional advice):

*   **National Eating Disorders Association (NEDA):** [https://www.nationaleatingdisorders.org/](https://www.nationaleatingdisorders.org/) (They have resources for families and supporters.)
*   **The Emily Program:** [https://www.emilyprogram.com/](https://www.emilyprogram.com/) (Offers support and resources for families.)

Please remember, taking care of yourself is *not* abandoning your uncle. It's essential for your well-being, and it will ultimately allow you to offer more sustainable support. If those thoughts of wanting to withdraw become overwhelming, please reach out for immediate help – a crisis line or mental health professional. You deserve care too.

### ft_only

You're carrying a weight that no one should have to carry alone, and it's understandable that you're exhausted. Five years is a long time to be a lifeline, and the lying and anger are a common tactic in eating disorders, not a reflection of your worth. It's okay to feel like the enemy when you're the one trying to hold someone accountable. It's also okay to want to walk away when you're depleted.

That exhaustion, and the thoughts that come with it, are a sign that you need support, not less of it. If you're in Brazil, you can reach out to the CVV (Centro de Valorização da Vida) at 188, or the National Eating Disorders Association (NEDA) has resources for carers at https://www.nationaleatingdisorders.org/supporting-a-loved-one. If the thoughts of wanting to be gone are frequent or intense, please reach out to a mental health professional. You deserve care too.

### ft_rag

That exhaustion is a signal, not a character flaw. It's your system telling you it's beyond its limits. When someone you care for starts pushing you away, it's a sign that the dynamic needs to shift, not that you're failing. It's also a sign that you need to find some support for yourself.

If you're having thoughts of not wanting to be around anymore, please reach out to someone who can help. Here are some resources:

*   **Suicide Prevention Lifeline:** Call or text 988 in the US and Canada, or dial 111 in the UK. In Brazil, dial 188.
*   **The National Eating Disorders Association (NEDA):** [https://www.nationaleatingdisorders.org/](https://www.nationaleatingdisorders.org/)
*   **The Anorexia & Bulimia Care (ABC):** [https://anorexiabulimiacare.org.uk/](https://anorexiabulimiacare.org.uk/)

You're not alone in this, and there are people who want to help you both.

**Your notes:** _____________________

---
## Item 11 — `syn_001338` · SYNTHETIC held-out · Caregiving Challenges – Distance Caregiving

**INPUT:** My cousin has Parkinson's and lives with me here in Stockholm. I'm studying history part-time and this has been my reality for two years now. My Sikh faith is everything to me but I'm so isolated. I barely see anyone outside of caring and studying. The loneliness is worse than the tiredness.

<details><summary>Gold reference (synthetic only — click)</summary>

Loneliness is often the heaviest part of caregiving, and two years of it alongside study is a long time to go without your own social world. Two things: first, look for a young carer group in Stockholm, even an online one, where you can talk to people who get it without explanation. The Swedish Carers' Association (Anhörigas Riksförbund) is a good starting point. Second, is there a gurdwara or Sikh community nearby where you could attend once a week just for yourself, not in a caring role? Your faith community can be a place of rest as well as duty.

</details>

### baseline

Oh, my dear, that sounds incredibly challenging. Two years is a long time to carry such a heavy load – caring for your cousin, pursuing your studies, *and* feeling so deeply connected to your faith while experiencing this isolation. It’s completely understandable that the loneliness feels worse than the tiredness; loneliness can really weigh on the spirit. 

It's so brave of you to share this. Your Sikh faith being "everything" to you makes this sense of disconnection even harder, I imagine. 

Would you be open to exploring some small steps? Perhaps looking for a local Sikh community group in Stockholm, even just to attend occasionally? Or maybe finding a study group for history, just to have some connection around your studies? 

There are also resources that might help with caregiver support – even just someone to talk to. Here's a link to a Swedish organization offering support for carers: [https://www.vardforbundet.se/en/](https://www.vardforbundet.se/en/)

Remember, it's okay to need support, and reaching out is a sign of strength.  And please, if you're feeling overwhelmed, don't hesitate to talk to a trusted friend, family member, or a professional. You deserve care too.

### rag_only

It sounds like you're carrying a *lot* right now – balancing studies, caring for your cousin with Parkinson's, and holding onto your faith, all while feeling incredibly lonely. That's a huge weight, and it's completely understandable that the loneliness feels worse than the tiredness. You're a very caring person to be so dedicated to your cousin.

It's brave of you to share this. It takes strength to admit when things are hard. 

Perhaps a small step could be to explore groups connected to your Sikh faith in Stockholm? Or maybe a study group for history? Even a little connection can make a difference. 

Remember, it's okay to need support too. Is there a trusted friend, family member, or counselor you could talk to about how you're feeling? There are also resources available – would you like me to help you find some support organizations in Sweden?

### ft_only

Two years is a long time to be carrying this much, and it's understandable that the loneliness is the worst part. Caring and studying are both solitary things, and your faith is a lifeline, but it's not a substitute for people. Do you have a local Gurdwara? Even if you can't get there often, knowing there's a community space and people who share your beliefs might help. If you can't get to the Gurdwara, can you find a Sikh community group that meets online? And is there a Parkinson's support group in Stockholm that you could join, even just to listen? You don't have to share your story, but being around people who understand the practicalities of caring might help you feel less alone.

### ft_rag

Two years of caring and studying, and a faith that matters deeply, but a loneliness that outweighs the tiredness. That's a lot to carry, and it's understandable that isolation feels worse than exhaustion. You're right to name the loneliness, and to notice it's a separate weight from the practical demands.

Do you have a Sikh community in Stockholm? Sometimes faith communities have regular events or study groups that could offer a low-pressure way to connect. If that doesn't feel right, are there any history groups at your university, or even online, where you could talk about your studies with others? It doesn't have to be a huge social life, just a small, regular connection.

**Your notes:** _____________________

---
## Item 12 — `syn_000783` · SYNTHETIC held-out · Caregiving Challenges – Emotional Impact

**INPUT:** My cousin moved in with me after his spinal cord injury three years ago. I work full-time in psychology and somehow I'm still not coping. I know all the theory about stress and it doesn't help. Some nights I just cry after he's asleep and I don't know why.

<details><summary>Gold reference (synthetic only — click)</summary>

Knowing the theory of stress and actually living inside it are completely different things. That gap isn't a failure, it's just how it works. Crying after he's asleep sounds like your body releasing what the day has held, and it makes sense. Can I ask: do you have anyone you talk to about this, not as a psychologist, but as a person who is also carrying a lot? And is there any respite care or support you could access so the nights aren't your only decompression time? Sometimes the crying is a sign that one outlet isn't enough anymore, and that's worth listening to.

</details>

### baseline

Oh, sweetheart, that sounds *so* incredibly hard. It's completely understandable you're feeling overwhelmed, even with your psychology background. Knowing the theory doesn't make living it any easier, does it? It sounds like you're carrying a lot, balancing work, supporting your cousin, *and* trying to manage your own well-being. 

It's okay to cry, and it's okay to not know exactly *why* right now. Those tears are a signal that you're deeply affected, and that's valid. 

Three years is a long time to be in this situation. Would you be open to exploring just *one* small thing you could do for yourself this week? Maybe 15 minutes of quiet time, a warm bath, or reaching out to a friend? 

Also, because you're providing such significant care, it might be really helpful to talk to a therapist yourself. They can offer a safe space to process everything. Would you like me to help you find some resources for caregiver support groups or therapists in your area?

Remember, you deserve care too. You're doing a lot, and it's okay to ask for help.

### rag_only

It sounds like you're carrying a *lot* right now. Juggling full-time work in psychology *and* being a primary support for your cousin after his injury is incredibly demanding. It's completely understandable to feel overwhelmed, and those tears at night? They're a sign of how much you're holding in. 

Knowing the theory doesn't always make things easier in practice – your feelings are valid. It's also really common to feel like you *should* be coping better, given your profession, but please be kind to yourself.

It takes strength to acknowledge you're struggling. Would you be open to exploring some support options? Connecting with others who understand caregiving (like through caregiver.org or usa.gov) might help you feel less alone. And, as another person suggested, talking to a professional – a doctor or therapist – could offer a safe space to process everything. 

You deserve care too.

### ft_only

You're a professional who understands stress, and yet you're still overwhelmed. That's not a failure of understanding, it's a sign of how much you're carrying. It's okay to cry, and it's okay to not know why. It's a release valve, and it's a signal that your system is overloaded. You're living the theory, not just studying it.

Three years is a long time to be in crisis mode, even with a loved one. Can you carve out 30 minutes this week to talk to a colleague or supervisor, not about your cousin's case, but about your experience as a caregiver? Sometimes just saying it out loud to someone who gets the professional context can shift something.

### ft_rag

It's not surprising that you're crying, even with your knowledge of stress theory. You're living the reality of a very demanding situation, and it's okay to feel overwhelmed. It sounds like you're carrying a lot, both at work and as a caregiver. Have you considered talking to a professional yourself? It's not about needing to "fix" anything, but about having a space to process what you're going through. Resources like caregiver.org and usa.gov can help point you toward available programs in your state. You are not alone.

**Your notes:** _____________________

---
## Item 13 — `syn_003610` · SYNTHETIC held-out · Caregiving Challenges – None Reported

**INPUT:** My older sibling is recovering well from their stroke and we've got a solid routine at home. I'm studying economics at college here in the Philippines and it's been two years now. Things are just okay, no complaints really.

<details><summary>Gold reference (synthetic only — click)</summary>

A solid routine after two years of stroke recovery is something worth acknowledging. Since things are steady, it's worth checking on a couple of things. Is there anything you've been putting off for yourself, maybe socially or health-wise? And is there any part of the routine that works only because you hold it together? Writing that down while things are calm can make it easier to ask for help later if you need it.

</details>

### baseline

It sounds like you're holding a lot together – supporting your sibling's recovery *and* navigating your studies! That's wonderful that you've established a good routine at home, and it's really positive to hear things are "okay," even if it's not more exciting than that right now. 

Two years of college is a good stretch, and it's perfectly alright for things to just *be* sometimes. It's okay to not have big feelings about it, just a sense of "okay." 

Is there anything small I can help with today? Perhaps brainstorming ways to carve out a little self-care time amidst everything, or finding resources for students in the Philippines? Just let me know.

### rag_only

It sounds like you've been through a lot, balancing caregiving with your studies – and it's wonderful to hear your sibling is recovering well and things are stable at home now. It takes incredible strength to manage everything, and it's completely understandable that last year was so challenging, especially with the shift to online learning. 

It's really insightful that you recognize the importance of having someone to talk to, like a psychologist, and seeing your parents ask for help. It *is* hard to reach out, especially to people you don't know. 

Since things are "just okay" right now, perhaps a small step could be exploring the counseling resources available at your college? They can offer a safe space to process things. You deserve support as you navigate your studies and life.

### ft_only

Okay, two years of college economics while supporting your sibling's recovery. That's a lot of steady work, and "just okay" after that is a real achievement. It's easy to fall into a routine where you don't complain, but that doesn't mean there isn't a lot going on. Is there anything small you'd like to change about the routine, or something you'd like to celebrate?

### ft_rag

It sounds like you've found a rhythm with your sibling's care and your studies, which is great. It's also good that you're aware of the support you missed last year—a psychologist to talk to, and help from outside the family. That's a step you could revisit if things feel shaky again.

**Your notes:** _____________________

---
## Item 14 — `syn_001498` · SYNTHETIC held-out · Current Digital Tool Use

**INPUT:** My dad lives in another city in Mexico and is recovering from a stroke. I work full-time in biology, and I've been helping coordinate his care for as long as I can remember. I use WhatsApp with his nurses and a shared Google Doc for his medication list, but the doc hasn't been updated in weeks because everyone assumes someone else is doing it.

<details><summary>Gold reference (synthetic only — click)</summary>

That 'someone else will update it' drift is incredibly common with shared docs, the responsibility is distributed so no one owns it. For something as important as medications, that gap is genuinely risky. A couple of things, could you assign one person, maybe a primary nurse, as the responsible updater with a clear expectation? And would a brief weekly check-in where you review the doc together help keep it current? Sometimes the fix isn't the tool, it's naming who owns it and making that expectation explicit.

</details>

### baseline

Oh, sweetheart, that sounds incredibly stressful. Juggling a full-time job *and* coordinating care for your dad from a distance – especially after a stroke – is a huge responsibility. It's completely understandable that things are slipping through the cracks, like the medication list. It's easy for those "someone else will do it" assumptions to happen, isn't it?

It's so loving of you to be taking this on. 

Here's a small step: could you send a quick, gentle message on WhatsApp right now saying something like, "Hi team, just checking in on updating Dad's medication list in the Google Doc. Could someone please take 5 minutes to do that today?" No blame, just a simple request.

It might also be helpful to talk to a trusted friend or family member about how you're feeling. And if you're feeling overwhelmed, remember it's okay to ask for more support – perhaps a social worker or care coordinator could help streamline things. 

You're doing your best, and that *matters*.

### rag_only

It sounds like you're carrying a lot right now, balancing your important work in biology with coordinating care for your dad from a distance. It's completely understandable to feel concerned when you're not sure how things are going day-to-day, and it's really thoughtful of you to be so involved. 

It's also common for things like the medication list to fall through the cracks when everyone assumes someone else is handling it. That can be frustrating!

Perhaps a small step could be to gently reach out to the nurses and suggest a quick check-in to update the Google Doc together? 

It's wonderful that you have a caregiving consultant you trust – leaning on that relationship sounds really valuable. Remember, it's okay to set boundaries with work *and* family to protect your time and energy, as the article suggests. You deserve support too.

### ft_only

That's a common problem with shared documents: everyone assumes someone else is on it, and then it falls behind. It's good that you've identified that the document is out of date. Can you send a quick message to the nurses on WhatsApp asking them to check the document and update it, and then offer to do it yourself if they're too busy? It's a small step, but it'll help keep things on track.

### ft_rag

That's a common issue with shared documents: everyone assumes someone else is updating it, and then it falls behind. It's easy to feel like you're the only one who notices, and it's frustrating.

Would you be willing to ask the nurses directly, one by one, if they're able to commit to updating the Google Doc after each visit? You could say something like, "I've noticed the medication list hasn't been updated lately. Would you be willing to add notes after your visits?" Sometimes a direct ask, rather than a general request, can make a difference.

**Your notes:** _____________________

---
## Item 15 — `syn_005453` · SYNTHETIC held-out · Online Support – Barriers

**INPUT:** My cousin lives with me in Stockholm and has heart failure. I try to find support groups online but everything's in Swedish and we're a Tamil Hindu family. I need something that understands both the medical side and our cultural context. Engineering college leaves me almost no time to search.

<details><summary>Gold reference (synthetic only — click)</summary>

Searching for resources that honour both the medical and cultural sides is harder than it should be, and the language barrier adds another layer. A couple of starting points: the Swedish Heart-Lung Foundation has some English material, and the European Society of Cardiology has patient resources in multiple languages. For the cultural dimension, are there specific things you're looking for, like dietary guidance that fits Tamil cooking, or how to talk about heart failure within your family's understanding of health? Also, does your cousin's care team include anyone who speaks Tamil or has worked with South Asian families? They may know resources you won't find through searching alone.

</details>

### baseline

Oh, that sounds incredibly challenging – balancing college, caring for your cousin, *and* navigating a new city with a language barrier. It's completely understandable you're feeling overwhelmed. It's so kind of you to want to find the right support. 

It's really tough when resources aren't available in your language or don't understand your cultural background. It makes an already difficult situation so much harder. 

Since time is so tight, let's brainstorm a couple of small steps. Would you be open to me helping you find a translator to look through some Swedish support group websites? Or perhaps we could look for Tamil community organizations in Stockholm – they might have connections or know of resources.

Also, have you spoken with a social worker at the hospital where your cousin receives care? They are often excellent at connecting people with relevant support, and may have resources specifically for immigrant communities. 

Remember, you don’t have to do this alone. It's okay to ask for help from trusted friends, family, or professionals. Taking care of yourself is important too.

### rag_only

That sounds incredibly challenging – balancing college, supporting your cousin, *and* navigating a new city with language and cultural barriers. It's completely understandable you're feeling overwhelmed and wishing for easier access to support. 

It's wonderful you're looking for help, and it's valid to want something that respects both the medical needs and your family's background. It's frustrating when resources aren't available in your language or aren't culturally sensitive.

Given your time constraints, perhaps starting with your college's student support services could be a first step? They might have resources or be able to connect you with organizations that can offer more tailored support. 

Also, the idea of online forums (like the Effective Altruism Forum mentioned earlier) could be helpful, even if it takes a little time to find the right connections. Starting small – maybe just reading through discussions – could be a way to dip your toe in.

Would you like me to help you brainstorm ways to approach your college's support services, or perhaps look for general resources for caregivers that you could then ask about at school?

### ft_only

That is a really specific need, and it's understandable that you're running into a wall with general searches. Here's what I'd suggest:

1.  **Start with the hospital:** The cardiology department at your cousin's hospital is the best place to ask about support groups that cater to specific cultural groups. They might not have one directly, but they'll know what's available in the city.
2.  **Tamil community centres:** Stockholm has Tamil community centres. They may not have heart failure-specific groups, but they'll be a good place to ask if anyone knows of a Tamil family dealing with the same thing.
3.  **Hindu temple:** Your local Hindu temple might have a support network or know of someone who can help.
4.  **Ask the doctor for a social worker:** A social worker attached to the cardiology team can help you navigate the system and find resources.

I know you're busy with engineering college. Don't feel bad about asking for help with this. It's a lot to carry on your own.

### ft_rag

It's frustrating when support is out of reach because of language or cultural barriers. It's good you're looking for something that understands both the medical side and your family's context. I'm sorry that the resources you've found so far are in Swedish.

Given your time constraints, I'm wondering if your college has a student support service that might be able to help you find resources. They may have a network of contacts or know of Tamil Hindu community groups that could offer support. Alternatively, if you're able to, you could ask your cousin's medical team if they know of any support groups that cater to Tamil Hindu families.

**Your notes:** _____________________
