# Human Review Pack v2 — Carebot Eval (post RAG-leak fix)

**What changed since pack v1:** the two RAG conditions were re-run with labeled retrieved
context (blocks marked as 'another caregiver's experience' or 'guide: <source>') plus an
explicit instruction never to attribute retrieved content to the current user.
The old leak (e.g. 'your POH GGZ support') is eliminated in spot checks.

**Your job this round — two questions per item:**
1. Which response would you want to receive? (pick one)
2. For ft_only vs ft_rag_v2 specifically: did retrieval ADD anything (a useful resource,
   grounded insight) or did it make the reply vaguer? Mark ADD / NEUTRAL / HURT.

**Also flag:** any remaining false attribution ('you mentioned/you're getting X' the user
never said), fabricated-looking URLs, meta-slips (model referring to its own instructions),
and geographic mismatches (e.g. US chains suggested to Dutch users).

**Contents:** 12 real (Dang) + 3 synthetic inputs. Judge overall shown per response.

---
## Item 1 — `dang_029` · REAL (Dang) · Support Currently Used

**INPUT:** I think not yet, but I will definitely look for support when things get a bit difficult.

### baseline · judge: 4/5

That sounds like a really thoughtful approach. It's wonderful that you're already thinking ahead about seeking support when you need it – that takes a lot of self-awareness! It's okay to not need it *right now*, and it's really good to know you will reach out when things feel harder. 

Just remember, even small difficulties are valid reasons to connect with someone you trust. I'm here to listen too, if you ever want to just talk things through. ✨

### ft_only · judge: 3/5

That's a good plan. It's smart to know when you might need support, and even smarter to have a plan to find it. It's like having a spare tire—you hope you don't need it, but it's good to know it's there. When things do start to feel difficult, remember that reaching out isn't a sign of weakness, it's a sign of strength.

### rag_only_v2 · judge: 4/5

It sounds like you're aware that things might get challenging, and you're already thinking ahead about seeking support – that's really proactive of you. It's okay to anticipate needing help, and it's wonderful that you're planning to reach out when the time comes. 

Just remember, acknowledging things are hard is a really important first step. When you *do* feel ready, leaning on others can make a big difference. Is there anyone you feel you could talk to now, even just to share how you're feeling?

### ft_rag_v2 · judge: 4/5

That's a good plan. It's very common to feel like you don't *need* support until things feel harder, and it's smart to get ahead of that. It's also okay to wait until you're ready, and to start small. What kind of support feels most appealing right now?

**Preferred response:** ______   **RAG effect (ADD/NEUTRAL/HURT):** ______

**Notes:** _____________________

---
## Item 2 — `dang_030` · REAL (Dang) · Support Needed

**INPUT:** On one hand you want help, and there are also people that want to give help, but it's hard to bring those together. You also don't want random people in your house doing the laundry or something. So I think it would be handy if you had a sort of tool in which you could put what needs to be done, and other people — family members or people you can trust — can see it and indicate 'oh I can do groceries today.' I would not want strangers doing those kinds of things.

### baseline · judge: 5/5

That sounds *really* frustrating. It's so kind of you to recognize you don't have to do everything alone, and it's smart to think about how to connect with help from people you *already* trust. It's completely valid to want to keep things feeling safe and comfortable in your home, too – you're right to not want just anyone stepping in.

You've hit on a *great* idea – a central place to list needs and let trusted people offer help. There are actually a few tools that do just that! Here are a couple, keeping your privacy and trust in mind:

*   **Lotsa Helping Hands:** Designed for coordinating help within a trusted network. ([https://lotsahelpinghands.com/](https://lotsahelpinghands.com/))
*   **CareCalendar:** Similar to Lotsa Helping Hands, focusing on family and friends. ([https://www.carecalendar.org/](https://www.carecalendar.org/)) 
*   **A simple shared online list:** Even a shared Google Doc or a note in a family group chat can work!

It's okay to start *small* with this. Maybe just list one or two things to begin with, and see how it goes. 

It takes courage to ask for help, and you're already taking a wonderful step by thinking about how to make it easier. If you find it hard to even *start* the conversation with family, or if you're feeling overwhelmed, please reach out to someone you trust – a friend, family member, or a supportive professional.

### ft_only · judge: 4/5

You're right, it's a classic problem: people want to help, but it's hard to coordinate, and you want to keep it within your circle of trust. A shared task list that only your trusted people can see is a great idea. There are a few apps that do that:

*   **OurHome:** It's designed for families, with shared lists, chore assignments, and a reward system.
*   **Trello:** A bit more flexible, you can create boards for different areas of life and assign tasks to people.
*   **Google Tasks:** If everyone in your circle uses Google, this is simple and integrated.

The key is to choose one that's easy for everyone to use, and to be specific about what you need. "Groceries" is good, but "pick up milk, bread, and eggs from Kroger" is even better.

### rag_only_v2 · judge: 4/5

It sounds like you're experiencing that tricky balance – wanting support, knowing people *want* to help, but finding it hard to actually connect the two. And it's completely understandable to want to keep things to people you trust! 

It's a good idea to think about a way to clearly list what needs doing, so those close to you can easily offer help with specific tasks, like groceries. 

Would it be helpful to brainstorm some simple ways to do that? Maybe a shared online list, or even just a quick text message outlining a few things? Just small steps, whatever feels comfortable for *you*.

### ft_rag_v2 · judge: 4/5

It sounds like you're wanting to make it easier for people you *already* trust to help, rather than opening things up to strangers. A shared list or calendar where family can sign up for tasks could be a good way to do that. It's a small step, but it could make a big difference in feeling less alone with everything.

**Preferred response:** ______   **RAG effect (ADD/NEUTRAL/HURT):** ______

**Notes:** _____________________

---
## Item 3 — `dang_045` · REAL (Dang) · Online Support – Willingness

**INPUT:** I would be happy if I have access to an online version of information from professionals. I don't have time for looking for any support otherwise.

### baseline · judge: 4/5

It sounds like you're feeling really stretched for time and wanting easy access to helpful information – that's completely understandable! It's smart to recognize you don't have the bandwidth to search right now. 

You're right to want information from professionals. Here are a few places that offer reliable, readily available resources online. *Please remember these are starting points, and aren't a replacement for personalized advice.*

*   **HelpGuide.org:** ([https://www.helpguide.org/](https://www.helpguide.org/)) Offers articles on mental health and wellbeing, written by experts.
*   **MentalHealth.gov:** ([https://www.mentalhealth.gov/](https://www.mentalhealth.gov/))  A U.S. government website with information and resources.
*   **Crisis Text Line:** ([https://www.crisistextline.org/](https://www.crisistextline.org/)) - While for crisis support, their resources section is helpful too.

It's okay to lean on these resources, and it's *also* okay to reach out to someone you trust – a friend, family member, teacher, or counselor – if you need more support. 

Taking even a few minutes to read something helpful can be a good step. How does that sound? Is there anything specific you're hoping to find information *about* that I could help you narrow down?

### ft_only · judge: 4/5

I understand. It's frustrating when you're already stretched thin to have to *find* the help you need, too. Here are a few places that gather professional advice online, with a focus on being accessible and not requiring a lot of searching:

*   **Mental Health America (MHA):** [https://mhanational.org/find-support-groups](https://mhanational.org/find-support-groups) - They have a directory of support groups, many of which meet online.
*   **The National Alliance on Mental Illness (NAMI):** [https://www.nami.org/PersonalStory/FindSupport](https://www.nami.org/PersonalStory/FindSupport) - NAMI offers online discussion groups and resources.
*   **Crisis Text Line:** Text HOME to 741741 - While for crisis situations, they also have resources and can point you toward ongoing support.
*   **Psychology Today:** [https://www.psychologytoday.com/us](https://www.psychologytoday.com/us) - A directory of therapists, many of whom offer online sessions. You can filter by insurance and specialty.

These are a starting point. I can help you narrow down what might be most useful if you tell me what kind of support you're looking for.

### rag_only_v2 · judge: 3/5

It sounds like you're really stretched for time and looking for support that's easy to access. That's completely understandable – caregiving is demanding, and it's hard to find extra moments. 

It's great you're thinking about getting information from professionals! Many people find it helpful to have expert insights. Knowing others have wished for easily accessible, clear information (like you do!) can be validating.

Would you like me to help you brainstorm some places to *start* looking for online resources? We can focus on finding things that are concise and avoid complicated medical terms. Or, if you'd prefer, I can share some ideas for connecting with a professional directly – even a quick phone call could be a good first step.

### ft_rag_v2 · judge: 4/5

That makes total sense. It's hard to carve out time for extra research when you're already stretched thin. I'll keep that in mind as I respond. Is there anything specific you're looking for information on right now? If you tell me the topic, I can try to find a concise, reliable source.

**Preferred response:** ______   **RAG effect (ADD/NEUTRAL/HURT):** ______

**Notes:** _____________________

---
## Item 4 — `dang_012` · REAL (Dang) · Caregiving Challenges – Care Recipient Behavior

**INPUT:** She doesn't like to be helped that much. She's very mentally strong, completely fine, very smart, she does uni — she doesn't like to be babied. But sometimes we have to force her a little bit: 'you have to calm down.' She doesn't like to be felt sorry for. Sometimes it takes my energy. And it's also hard to distinguish — when should I push her a little? Maybe I should just let her do her own thing. I think that's the balance.

### baseline · judge: 4/5

It sounds like you're navigating a really delicate space with her, wanting to support someone who is fiercely independent and capable. It's wonderful you recognize her strength and intelligence! And it's *completely* understandable that it takes energy from you, especially when you're trying to figure out when to offer support and when to step back.

You're right to be thinking about balance. It seems like "forcing" her to calm down doesn't quite land well, and respecting her dislike of pity is key. 

Perhaps instead of *telling* her to calm down, you could simply *notice* and reflect what you see: "You seem really wound up right now," or "That sounds incredibly frustrating." Validating her experience without trying to fix it might be more helpful.

It *is* okay to let her do her own thing a lot of the time. Maybe the "push" comes in gently offering resources when she's *not* actively upset – things that might be helpful down the road, without pressure. 

It's also okay to protect your own energy. You can't pour from an empty cup. 

This is a tricky dance, and you're clearly a thoughtful friend for trying to find the right steps.

### ft_only · judge: 4/5

You're describing a really common dynamic, wanting to help someone who's fiercely independent but clearly needs a little support sometimes. It's exhausting to guess when to push and when to pull back.

"Force her to calm down" is a phrase that often backfires, even with the best intentions. It's a signal that you're seeing her distress and want to fix it, but it can feel invalidating.

The balance is tricky. Maybe try shifting from "you *have* to" to "I'm noticing you're really wound up, and I'm here if you want to talk or just sit in silence." It gives her space to choose, and lets her know you're present without implying she's broken.

You're right to protect your energy. If you're constantly guessing, it's okay to step back and let her navigate things on her own. It's not giving up on her, it's respecting her strength.

### rag_only_v2 · judge: 4/5

It sounds really tricky to find the right balance between supporting her and respecting her independence. It's wonderful that she's so capable and determined, and it's completely understandable that it's draining when you're unsure how much help to offer. It's also really insightful of you to recognize that "forcing" her to calm down isn't ideal, and you're wondering about letting her navigate things on her own. 

That's a very thoughtful approach. It's okay to feel unsure – it's a tough spot to be in. Perhaps focusing on *asking* what she needs, rather than *telling* her what to do, could be a small step? Even just, "Is there anything I can do to help right now?" 

Remember, taking care of yourself is important too. If you're feeling depleted, it's okay to step back a little and recharge. 

If you'd like to explore resources for young carers, The Children's Society has a helpful guide with information about your rights and support options: [https://childrenssociety.org.uk/sites/default/files/DownloadableResources/know_your_rights.pdf](https://childrenssociety.org.uk/sites/default/files/DownloadableResources/know_your_rights.pdf). There's also support available at universities: [https://www.ucas.com/undergraduate/applying-university/individual-needs/students-caring-responsibilities](https://www.ucas.com/undergraduate/applying-university/individual-needs/students-caring-responsibilities).

### ft_rag_v2 · judge: 4/5

It sounds like you're walking a really delicate line between supporting her and respecting her independence, and it's exhausting to constantly second-guess when to step in. It's good you're thinking about that balance. Sometimes, "letting her do her own thing" can be the most supportive thing, even if it feels counterintuitive. If you're finding it hard to know when to push and when to pull back, it might be worth talking to a professional, just to get an outside perspective. The Children's Society has a 'Know Your Rights' pack that might help you understand what support is available.

**Preferred response:** ______   **RAG effect (ADD/NEUTRAL/HURT):** ______

**Notes:** _____________________

---
## Item 5 — `dang_038` · REAL (Dang) · Support Needed

**INPUT:** I feel like I already have it. I'm not her only friend — there are also other friends. We sometimes talk to each other about it. And I can also talk to my boyfriend.

### baseline · judge: 3/5

It sounds like you're navigating a tricky situation with a friend, and it's good you're already reaching out to others for support – both friends *and* your boyfriend. That takes strength! It's really validating that you have people you can talk to about this. 

Since you're already doing some things to cope, maybe just continuing to lean on those connections is a good first step? If it feels overwhelming at any point, remember it's okay to talk to a trusted adult too, like a family member or counselor. They can offer another perspective.

### ft_only · judge: 3/5

That's good. It's a relief to know you're not alone in this, and you have people you can talk to. It's a good sign that you're already using your support network. If you want to talk more about how you're feeling, I'm here.

### rag_only_v2 · judge: 3/5

It sounds like you're already taking some really good steps to manage things – leaning on friends and your boyfriend for support is wonderful. It's really positive that you have people you can talk to. 

It's completely understandable to feel… well, *something* when you're supporting someone, even when you have a network. It's good you recognize you're not alone in this.

Just checking in – how are *you* doing today, beyond the support you're offering? Even small moments for yourself can make a difference.

### ft_rag_v2 · judge: 3/5

It's good you have a network of friends and a partner you can talk to. That's a solid base for navigating the ups and downs of caregiving. It's also normal to feel like you're already "getting it," but remember that caregiving is a long game, and needs change. Check in with your friends and partner regularly, and don't hesitate to ask for specific support when you need it.

**Preferred response:** ______   **RAG effect (ADD/NEUTRAL/HURT):** ______

**Notes:** _____________________

---
## Item 6 — `dang_001` · REAL (Dang) · Caregiving Challenges – Balance & Time

**INPUT:** It is hard to find a balance between how much time you spend on caregiving, how much time you spend on your study or sport or friends, because you can always do more to take care at home. Sometimes you need to finish a deadline but if something happens at home and I need to go home to take care of my youngest sister, you cannot do both and so I need to ask for a postponement — you end up in a vicious circle. I cannot study full time anymore. It takes up much time and it is emotionally draining. You constantly think about it in the back of your mind.

### baseline · judge: 4/5

Oh, sweetheart, that sounds *so* incredibly difficult. It's completely understandable that you're feeling drained and stuck in a cycle – it's a lot to juggle caring for your sister, *and* trying to focus on your studies or other things you enjoy. It's really valid to feel like you can't do it all, especially when family needs pull you in different directions. 

It's okay that full-time study doesn't feel possible right now. It sounds like you're carrying a huge emotional weight, and that constant worry is exhausting. 

Would it be helpful to brainstorm some *small* steps? Maybe talking to your teachers about your situation, or exploring options for reduced course loads?  It's also really important to have support for *you*. Is there a trusted adult – a counselor, teacher, or family member – you could talk to about this? 

Here's a resource that might offer some support for caregivers: [https://www.carersuk.org/](https://www.carersuk.org/) 

Remember, taking care of yourself isn't selfish; it's essential. You deserve support too.

### ft_only · judge: 4/5

That's a vicious circle, and it's exhausting. When caregiving is always urgent, it's hard to make space for anything else. It's okay that full-time study isn't working right now. Can you talk to your school about reduced course loads or extensions? Or is there a carer's support service that could help with the home side, even for a few hours a week? You deserve to study without that constant pull.

### rag_only_v2 · judge: 4/5

It sounds incredibly challenging to juggle caregiving with everything else in your life – studies, friends, and just having time for yourself. It's completely understandable that you're feeling drained and stuck in a cycle of needing to choose between responsibilities. It's a lot to carry, and it's okay to feel overwhelmed.

It's really smart to recognize that you can't do *everything* at once. Perhaps starting with small steps could help? Maybe identifying one small thing you can do for *yourself* this week, or talking to someone at school about needing a little flexibility? 

Remember, it's okay to ask for help and to set boundaries. There are resources available, and talking to a trusted adult – a teacher, counselor, or family member – could offer some support. The Children's Society guide suggests thinking about what helps *you* cope when you're stressed, and who else you can lean on. Would exploring that be helpful?

### ft_rag_v2 · judge: 4/5

That feeling of being pulled in too many directions, and the guilt of not being able to do everything, is really common for caregivers. It sounds like you're caught in a cycle where caregiving keeps interrupting your studies, and that's exhausting. One small step might be to talk to your school about flexible deadlines or arrangements, even if it feels awkward. You're not alone in this, and it's okay to ask for help.

**Preferred response:** ______   **RAG effect (ADD/NEUTRAL/HURT):** ______

**Notes:** _____________________

---
## Item 7 — `dang_013` · REAL (Dang) · Caregiving Challenges – Care Recipient Behavior

**INPUT:** He can't clean very well anymore because he can't see very well, so certain things — when something falls, or reading things — you have to read that out loud and speak loudly so that he understands everything. It's more about the way others talk to him, because he's half deaf.

### baseline · judge: 3/5

It sounds like things are shifting, and you're stepping up to help your loved one navigate some challenges with vision and hearing. That's really kind of you. It's understandable that it feels like more work when you need to adapt *how* you communicate – reading things aloud and speaking clearly takes extra effort. 

It's wonderful you've already identified those key adjustments! It shows you're really tuned in to what he needs. 

Just remember to be patient with both of you as you adjust. Small things, like consistently speaking a little louder and reading things out, can make a big difference. 

If you're feeling overwhelmed, or if you'd like to explore resources for supporting someone with vision or hearing loss, the Family Caregiver Alliance ([https://www.caregiver.org/](https://www.caregiver.org/)) is a good place to start. And please, don't hesitate to reach out to other family members or trusted friends for support *for yourself* too. You deserve it.

### ft_only · judge: 3/5

It sounds like you're adapting to a new way of communicating with him, and that's a lot of extra effort. It's good that you're reading things out loud and speaking more loudly, and that you're aware that his vision and hearing are changing. It's also good that you're aware that it's not just about what you do, but how others talk to him too. Is there a way to let others know about his needs, so they can communicate with him more effectively?

### rag_only_v2 · judge: 3/5

It sounds like you're navigating some changes in how you connect and help someone you care for. It's completely understandable that adjusting to these new needs – like needing things read aloud or spoken more clearly – can feel like a shift. 

It's really thoughtful of you to be aware of how communication impacts things. Small things, like making sure you're speaking clearly and reading things aloud, can make a big difference. 

Remember to be kind to yourself through this. It’s okay to feel a little overwhelmed as you learn what works best. If you're finding it hard to cope with these changes, talking to a trusted adult or someone like a counselor could be really helpful. They can offer support and strategies.

### ft_rag_v2 · judge: 2/5

It sounds like communication is becoming a bigger part of your caregiving role. Reading things aloud and speaking clearly can be tiring, but it's a way of keeping him connected to what's happening around him. It's good to be aware of his needs, and to adjust how you communicate to make sure he understands.

**Preferred response:** ______   **RAG effect (ADD/NEUTRAL/HURT):** ______

**Notes:** _____________________

---
## Item 8 — `dang_014` · REAL (Dang) · Caregiving Challenges – Distance Caregiving

**INPUT:** When I'm away, it's difficult to keep a tab on how things are going — that's a challenge, to make sure that things are going right and they are visiting and taking things on time. I'm mostly depending on them. I usually ask them 'how is it going, are you keeping track?' — like that's the only way I can take care of those things. Sometimes when they say they don't feel so well, that's when I get concerned: 'Oh, what went wrong? Did you take your medications? Did you exhaust yourself?'

### baseline · judge: 4/5

It sounds like you carry a lot of worry when you're away, wanting to make sure everything runs smoothly and that the people you depend on are okay. It's really natural to feel that way when you're trusting others with important things. 

It's also understandable that you feel a surge of concern when they mention not feeling well – it's a sign of how much you care! Asking about medications and activity levels comes from that caring place.

Perhaps, instead of focusing on *if* things are happening, you could try setting up a simple, agreed-upon check-in system? Maybe a quick text each day, or a specific time for a short phone call? 

It's okay to ask for help with this too. Is there a friend, family member, or professional who could offer support in navigating these feelings and finding ways to feel more at ease?

### ft_only · judge: 4/5

That's a lot of worry to carry when you're not there, and it's natural to feel like you need to check in constantly to make sure things are on track. It's also understandable to feel anxious when you hear they're not feeling well, and to immediately jump to problem-solving mode.

Sometimes, just knowing someone is thinking of you is enough, and you don't need to be the one to fix everything. Would it help to find a way to track medications or visits, so you can see at a glance how things are going without asking? Or maybe a daily check-in that's less about details and more about a quick "how are you feeling today?"

### rag_only_v2 · judge: 4/5

It sounds like you're carrying a lot of worry when you're not able to be directly present, and it's natural to feel that concern when you depend on others for important care. It's also really thoughtful of you to check in and ask how things are going. 

It's okay to feel anxious when you hear they aren't feeling well – that shows how much you care. Perhaps, alongside asking what happened, you could gently explore if there's a way to make checking in feel less stressful for *you*? 

Would it be helpful to brainstorm some simple ways to get a little more reassurance while you're away? Even small things can sometimes make a difference.

### ft_rag_v2 · judge: 4/5

It sounds like you're carrying a lot of responsibility, even when you're not physically present. It's natural to feel concerned when you hear someone isn't feeling well, and to want to know the details. It's also common to feel like you're the only one keeping track.

When you're away, could you ask the person providing care to send a short daily summary, rather than waiting for a problem to arise? Something like "Medication taken, lunch eaten, no new concerns" can be reassuring without requiring a long conversation.

**Preferred response:** ______   **RAG effect (ADD/NEUTRAL/HURT):** ______

**Notes:** _____________________

---
## Item 9 — `dang_006` · REAL (Dang) · Caregiving Challenges – Emotional Impact

**INPUT:** The caretaking itself is not that big of a challenge, because you do it bit by bit. The worrying — I struggled with that a lot, and I notice it's getting worse during corona times. I had intensive support for it. I am part of a caregiving organisation since I was 10, so in there we had a companion group, and from there I got referred because I just worry very intensely. Now, in corona times, I contacted the caregiving fulcrum — sometimes it's nice to tell your story without people judging or without people being in the same situation.

### baseline · judge: 4/5

It sounds like you're incredibly dedicated to caregiving, having been involved since you were so young! And it's *completely* understandable that worrying would be a big part of that, and that it's even *more* challenging now with everything happening. 

It's really good you recognized the worrying was increasing and reached out for support. It takes courage to do that, and it's smart to lean on resources like the caregiving fulcrum – having a safe space to share without judgment is so valuable. 

You've already done so much to build a support system over the years. Perhaps, when you have a moment, you could jot down a few things that *specifically* helped in the past, so you can revisit those strategies when the worry feels overwhelming? 

Remember, it's okay to not be okay, and it's a sign of strength to ask for help.

### ft_only · judge: 2/5

It's good you're in touch with the caregiving fulcrum. It's a relief to have a space to tell your story without having to explain the context or worry about judgment. It's also good you've had support for worrying since you were 10. That's a long time to be aware of it, and it's good you're able to reach out when it gets worse. It's also good you're part of a caregiving organisation. That can be a good source of support and information.

### rag_only_v2 · judge: 4/5

It sounds like you're carrying a lot, and it's completely understandable to feel overwhelmed. It's really common for caregivers to find the *worrying* part especially tough, and it makes sense that would be heightened right now. 

It's great you're reaching out. Just acknowledging how you feel is a really important first step. It also sounds like breaking things down into smaller steps, "bit by bit," can be helpful with the caretaking itself.

Would you like to talk a little more about what's worrying you most right now? Or perhaps we could brainstorm some small things you could do to feel a little more supported? Remember, there are people who want to listen without judgment, and seeking support is a sign of strength.

### ft_rag_v2 · judge: 2/5

It sounds like you're carrying a lot of worry alongside the practical tasks of caregiving. One caregiver found it helpful to have a space to share their story without judgment, like through a caregiving organisation or a "fulcrum" support service. Would you be open to exploring options like that, where you could talk things through with someone who understands?

**Preferred response:** ______   **RAG effect (ADD/NEUTRAL/HURT):** ______

**Notes:** _____________________

---
## Item 10 — `dang_017` · REAL (Dang) · Caregiving Challenges – None Reported

**INPUT:** No challenges faced. The caregiving is not that difficult at the moment.

### baseline · judge: 4/5

That's wonderful to hear! It sounds like things are going smoothly right now, and that's a real gift. It's so good when caregiving feels manageable. 

Just knowing you have a bit of breathing room is important. Sometimes, even when things *are* okay, it's helpful to think about what supports you enjoy – even small ones! 

Is there anything at all I can help with today, even just to brainstorm little ways to nurture *yourself* during these calmer times? Perhaps a quick list of relaxing activities, or resources for finding moments of peace?

### ft_only · judge: 4/5

That's good to hear. It's a relief when things are manageable. Still, even when it's not difficult, caregiving can be a long game. Is there anything you're doing to make sure you're taking care of yourself too? It's easy to let that slip when things are going well.

### rag_only_v2 · judge: 3/5

It sounds like you're managing well right now, and that's wonderful to hear. It's really positive that things aren't *too* difficult at the moment. 

Even when things are going okay, caregiving can still bring up a lot of feelings. It's okay to acknowledge those, even if they're small. Sometimes just noticing how you *feel* can be helpful.

I also noticed some other caregivers have found it hard to balance responsibilities, or wished they'd asked for more support. It's good to remember you don't have to do everything alone, and reaching out is a sign of strength. 

Is there anything small I can help with today? Perhaps finding some general information about resources, or just a space to share how you're doing?

### ft_rag_v2 · judge: 3/5

That's good to hear. It's helpful to know that things are manageable right now. Even when things are going well, it's worth thinking about what resources or information might be useful down the road, like what the other caregivers mentioned about dementia or household tools. Is there anything I can help you think through today?

**Preferred response:** ______   **RAG effect (ADD/NEUTRAL/HURT):** ______

**Notes:** _____________________

---
## Item 11 — `dang_054` · REAL (Dang) · Current Digital Tool Use

**INPUT:** I read articles about emotional parenthood — how to emotionally support someone — because that's what I'm dealing with right now. Some parental tricks actually work. I just Google things and read things on Reddit and Quora — firsthand human experience, rather than just textbook, although I do read articles too. It's just that I never really find or look for specific things.

### baseline · judge: 3/5

It sounds like you're really taking the initiative to learn how to best support someone you care about, and that's wonderful. It's also smart to draw from a variety of sources – articles *and* the experiences of others. It makes sense you'd gravitate towards firsthand accounts; sometimes those feel more real and relatable. 

It's okay to not have a specific plan right away. Just *seeking* understanding is a great first step. It sounds like you're already doing that! 

If you ever feel overwhelmed, or like you need to talk through what you're learning, please remember it's okay to reach out to a trusted friend, family member, or professional for support too. You deserve care as you care for others.

### ft_only · judge: 3/5

That's a really good way to approach it, to gather from both formal sources and direct experience. It's also smart to not look for specific things, but to just absorb the general principles. Sometimes the right thing to do isn't something you can find in a list, but something you feel your way into.

### rag_only_v2 · judge: 3/5

It sounds like you're putting a lot of effort into learning how to best support someone, and that you're finding helpful insights from a variety of sources – that's wonderful! It's also understandable to feel a bit overwhelmed when you're searching and not finding *exactly* what you need. 

It's really kind of you to be taking this on. Sometimes, just knowing you're trying your best is a big step. 

If you're feeling stressed or anxious while navigating this, remember there are resources available. The 80,000 Hours guide mentions some helpful apps like Mind Ease ([mindease.io](https://mindease.io)) and resources for things like perfectionism and imposter syndrome. 

And please, remember to take care of yourself too. Talking to someone you trust about how *you're* feeling can make a big difference. The Children's Society ([childrenssociety.org.uk/youngcarer/advice-for-young-people/well-beingand-mental-health](https://childrenssociety.org.uk/youngcarer/advice-for-young-people/well-beingand-mental-health)) has some helpful information as well.

### ft_rag_v2 · judge: 3/5

It makes sense to look for help that feels real, from people who've been there. It's good you're finding things on Reddit and Quora, and also reading articles. If you're looking for something more specific, the 80,000 Hours guide has resources for anxiety, ADHD, perfectionism, and imposter syndrome, and suggests that finding a therapist who's a good match is key. The Children's Society also has resources for young carers, and stresses the importance of talking to someone you trust.

**Preferred response:** ______   **RAG effect (ADD/NEUTRAL/HURT):** ______

**Notes:** _____________________

---
## Item 12 — `dang_048` · REAL (Dang) · Online Support – Barriers

**INPUT:** Only issue I could see would be internet connectivity — there are certain places where you can't get internet or maybe you've exhausted your data. In those situations you can't get access. Apart from that, maybe compatibility with the device could also be a possible issue. But apart from that, I don't see any other issue.

### baseline · judge: 3/5

It sounds like you've given this some really thoughtful consideration! You're right to point out those potential hurdles – internet access and device compatibility are definitely things to keep in mind. It's good you're anticipating those challenges. 

It's helpful to be prepared, and recognizing those limitations upfront is a smart move. If you find yourself in a spot with no internet, perhaps having a backup plan like a downloaded resource or a trusted person to reach out to could be useful. 

You're doing great thinking through this! Is there anything I can help you brainstorm about those potential issues, or anything else on your mind?

### ft_only · judge: 3/5

That's a really practical assessment. Internet access and device compatibility are the two big hurdles for anything digital, and you've pinpointed them right away. It's good to be aware of those limits, so you can plan around them if you need to.

### rag_only_v2 · judge: 3/5

It sounds like you're thoughtfully considering the practical side of things – like making sure there's a reliable internet connection and that the technology will actually work with your devices. That's really smart to think ahead about those potential hurdles! 

It's also understandable to wonder about relying on something digital for support. Some people find it hard to trust opening up online, and that's perfectly okay. It's good to be aware of what *you* need to feel comfortable and safe. 

If you're feeling any worry about how this might all work, or just need to talk through your thoughts, please know that's completely valid. Is there someone you trust you could chat with about this?

### ft_rag_v2 · judge: 3/5

It's good to think through practical things like internet access and device compatibility before relying on online support. Those are real barriers. It's also valid to feel unsure about opening up to someone you don't know online, or to worry when a message goes unanswered. It's a tension many caregivers feel. If you're trying out online support, maybe have a backup plan for when tech fails or you need a more personal connection.

**Preferred response:** ______   **RAG effect (ADD/NEUTRAL/HURT):** ______

**Notes:** _____________________

---
## Item 13 — `syn_006098` · SYNTHETIC · Caregiving Challenges – Care Recipient Behavior

**INPUT:** My younger brother has epilepsy and he's started refusing to tell me when he's had a seizure. I'm in another city doing an apprenticeship and I only find out from our mum weeks later. I need to know what's happening but he says I'm overreacting.

### baseline

Oh, that sounds really tough. It's completely understandable you're feeling worried and a little hurt that he's not sharing this with you, especially while you're away. It's natural to want to know how he's doing and be there for him. 

It sounds like he might feel like you're too concerned, and maybe that feels controlling to him? It's brave of him to set a boundary, even if it's making things harder for you.

Perhaps you could try telling him you understand he wants independence, but that knowing helps *you* feel connected and able to support him. Maybe suggest a check-in system that feels comfortable for *him* – a quick text, maybe, instead of a detailed explanation right away?

It might also be helpful to talk to Mum about this, and see if she has any ideas. And if you're feeling really distressed, reaching out to a trusted friend or mentor could offer some support for *you*. 

Remember, you're a good sibling for caring so much.

### ft_only

It's understandable that you're worried, and it's a really difficult position to be in when you're not getting information directly from him. It's also common for people to want to downplay things, especially when they feel like they're being monitored.

Could you try saying something like, "I'm not trying to check up on you, I just want to know what's happening so I can be there for you, and I need to know what's happening so I can be there for Mum too"?

If he's still reluctant, maybe ask if he'd be open to talking to a trusted professional about this, like a nurse or counsellor. They might be able to help him understand why you need to know, and help you both find a way to communicate that works.

### rag_only_v2

That sounds really worrying, and it's completely understandable you'd want to know what's happening with your brother. It's tough being an apprentice in another city and feeling disconnected from things at home, especially when it comes to a brother you care about. 

It's also really hard when someone you love dismisses your concerns – it sounds frustrating that he thinks you're overreacting. It's valid to feel anxious when you're learning about seizures weeks after they happen.

Perhaps you could gently share with him *why* knowing is important to you – not to control him, but because you care and want to be supportive. Maybe framing it as wanting to understand how *he's* feeling after a seizure might help?

It might also be helpful to talk to a trusted adult – perhaps someone at your apprenticeship, or a counselor – about how you're managing this worry. And, if you feel comfortable, maybe you and your mum could talk about how to best support your brother *together*.

### ft_rag_v2

That's a tricky spot, being a distance away and relying on someone else to tell you what's happening. It's understandable you'd want to know straight away, and it's also understandable he'd push back if he thinks you're getting anxious.

Does he have a neurologist? If so, maybe you could ask to be included in a quick check-in call, so you can hear directly from the doctor about how things are going. That might take some of the pressure off him to be the messenger, and give you a bit more reassurance.

**Preferred response:** ______   **RAG effect (ADD/NEUTRAL/HURT):** ______

**Notes:** _____________________

---
## Item 14 — `syn_001726` · SYNTHETIC · Current Digital Tool Use

**INPUT:** I'm a psychology apprentice in Poland and I live with my grandfather, who has early-onset Alzheimer's. Right now I track his daily routine and meds using a Google Sheet and a phone alarm for myself. It's been about a year and it works, but I worry everything falls apart if I forget to update it for a day.

### baseline

Oh, my dear, that sounds like a lot to carry, and it's so wonderful that you're taking such dedicated care of your grandfather. A year is a long time to maintain that system – you've been doing a really good job! It's completely understandable to worry about things slipping if *you* have a busy day, or just need a break. It's natural to feel that pressure.

It sounds like you're recognizing a potential weak point in the system, which is very insightful. Perhaps exploring a slightly more automated approach could offer some peace of mind? 

Have you considered apps specifically designed for medication reminders and routine tracking? There are some that allow for shared access, too, in case another family member or friend could help. (I can share some links to articles listing options if you'd like, but remember I can't *recommend* any specifically.)

Even just brainstorming one small change – like setting a recurring calendar event for yourself to double-check the sheet – might help lessen that worry. 

You're doing important work, and remember to be kind to yourself in the process. It's okay to ask for support, too. Is there a trusted friend, family member, or perhaps a supervisor at your apprenticeship you could talk to about this?

### ft_only

That's a really valid worry. A year is a long time to keep something going on willpower alone, and a single missed update can be a big deal. Have you considered a dedicated care calendar app? They're designed to handle meds and routines, and most have built-in reminders that don't rely on *you* remembering to set them. Some even let family members share access, so someone else can step in if you're unwell. It's a small change, but it could give you a lot of peace of mind.

### rag_only_v2

It sounds like you're doing a wonderful job caring for your grandfather, and it's completely understandable to feel anxious about things slipping if your system gets disrupted – a year is a long time to maintain that level of detail! It's really thoughtful of you to be proactive about finding ways to make things more sustainable.

It's great you've already found something that *mostly* works. It's common for caregivers to tweak things over time. I noticed another caregiver found a phone app, Minimalist, helpful for task lists – perhaps something similar could offer a bit more peace of mind than a Google Sheet, since it's always right there on your phone? 

It's okay if it feels overwhelming to switch things up. Maybe start by just exploring a couple of apps to see if any feel like a good fit? 

And please remember, you're also studying psychology – you're equipped to understand this is a challenging situation, and it's okay to ask for support from trusted friends, family, or professionals in Poland as you navigate this.

### ft_rag_v2

That's a very real worry. A single missed update on a system like that can easily throw things off. It's good you've identified that as a risk. One caregiver I spoke with found a simple task-list app on their phone was easier to keep up with than a journal or website. It meant they had the list with them, and could tick things off as they went. It's not a huge change, but it might be worth looking into if you think that would reduce the risk of things slipping.

**Preferred response:** ______   **RAG effect (ADD/NEUTRAL/HURT):** ______

**Notes:** _____________________

---
## Item 15 — `syn_003125` · SYNTHETIC · Caregiving Challenges – None Reported

**INPUT:** Things are okay with my grandmother. Her Parkinson's has been stable and from Cape Town I've got a good call routine going. Over five years of this and my computer science degree is going well. Just wanted to touch base.

### baseline

That's wonderful to hear! It sounds like you've really found a good rhythm with caring for your grandmother from a distance, and that's a *huge* accomplishment – especially alongside your studies. Five years is a long time to maintain that, and it shows real dedication. 

It's lovely that things are stable right now. It's good you're checking in, and I'm glad you wanted to share the good news. It's okay to just *be* doing well, you deserve that! 

Keep up the great work with both your grandmother and your degree. You're clearly capable and caring. ✨

### ft_only

That's a lot to hold, and it's good to hear that things are stable. Five years is a long time to be doing this, and it's good to have a routine. It's okay to just touch base and check in, and it's okay to be proud of what you've built.

### rag_only_v2

That's wonderful to hear! It sounds like you've found a really good rhythm supporting your grandmother from Cape Town, and that's a huge accomplishment alongside your studies. Five years is a long time – you've built a strong routine and shown a lot of dedication. 

It's great her Parkinson's is stable, and that you feel connected through your calls. It's okay to just *check in* and acknowledge things are going well. Sometimes simply recognizing the good is enough. 

Keep up the great work with both caring for your grandmother and your computer science degree. You're building a really solid foundation for a fulfilling future – perhaps even one where you can use your skills to do good, as this article suggests: [link to 80,000 Hours guide].

### ft_rag_v2

That's good to hear about your grandmother, and that a stable routine is working from Cape Town. Five years is a long time to hold that together, and a computer science degree on top of it is a lot. It's okay to just touch base and acknowledge that things are okay, and to let that be enough.

**Preferred response:** ______   **RAG effect (ADD/NEUTRAL/HURT):** ______

**Notes:** _____________________
