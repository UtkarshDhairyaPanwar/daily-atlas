#!/usr/bin/env python3
"""Build data/days/0868.json: Profiling and its scientific problems (Crime, tier B)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from t0868_sources import SOURCES
from t0868_content_a import SECTIONS_A
from t0868_content_b import SECTIONS_B

ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
IMAGES = json.load(open(os.path.join(HERE, "t0868_images.json")))
V = "2026-10-25"
YT = "Standard YouTube licence. Embed only, do not download."

def yt(id, vid, title, publisher, dur, start=0, end=None):
    end = end if end is not None else min(dur, 90)
    return {"id": id, "kind": "video", "provider": "youtube", "url": f"https://www.youtube.com/watch?v={vid}",
            "embed_url": f"https://www.youtube-nocookie.com/embed/{vid}?start={start}&end={end}", "start": start, "end": end,
            "title": title, "publisher": publisher, "license": YT, "duration_s": dur, "verified_on": V,
            "verified_by": "youtube oembed returned 200 with this channel name"}

MEDIA = [
    yt("vid_wired_clemente", "LHqbfJ3tq4Y", "Former FBI Agent Explains Criminal Profiling (Jim Clemente, Tradecraft)", "WIRED", 972, 0, 90),
    yt("vid_mastermind", "BbZF_WluzPI", "Mastermind: To Think Like a Killer, official trailer (Ann Burgess)", "Hulu", 162, 0, 90),
    yt("vid_nickell_doc", "Vj5uaeZTKRM", "The Murder of Rachel Nickell, official trailer", "Netflix", 97, 0, 90),
    yt("vid_witness_trailer", "3iKFLt9gjAU", "The Witness, official trailer", "Netflix", 99, 0, 90),
    yt("vid_jewell_trailer", "gSMxBLlA8qY", "Richard Jewell, official trailer", "Warner Bros.", 140, 0, 90),
    yt("vid_canter_first_profile", "6zzO2tTARBY", "The First Scientific Offender Profile", "David Canter", 350, 0, 90),
    yt("vid_canter_huddersfield", "a0hQXRG5EBo", "Professor David Canter, the creator of Investigative Psychology", "University of Huddersfield", 86, 0, 86),
    yt("vid_rossmo_ideacity", "YeClmHJIwgU", "Kim Rossmo: criminology explained and new technology used to catch a suspect", "ideacity", 1299, 0, 90),
    yt("vid_budhan_tedx", "Qm-jXEba0mA", "Theatre activism and rehabilitation, Dakxin Chhara, TEDxNUV", "TEDx Talks", 1123, 0, 90),
    yt("vid_mindhunter_trailer", "evdxH50J3rs", "Mindhunter, trailer 2", "Netflix", 66, 0, 66),
]

SECTIONS = SECTIONS_A + SECTIONS_B

def q(id, type, prompt, answer, expl, srcs, section=None, spot=None, diff=2, **kw):
    d = {"id": id, "type": type, "prompt": prompt, "answer": answer, "explanation": expl, "source_ids": srcs,
         "section_id": section, "spotlight_id": spot, "difficulty": diff}
    d.update(kw)
    return d

# ---------- section checks ----------
QUIZ_BANK = [
    q("qb_kelly", "mcq", "Who actually found George Metesky's name in January 1957?", 2,
      "Con Edison clerk Alice Kelly found his compensation file, marked 'injustice' and 'permanent disability'.",
      ["wiki_metesky"], "hook", "alice_kelly", 1, options=["Psychiatrist James Brussel", "An FBI profiler", "Con Edison clerk Alice Kelly", "A handwriting expert"]),
    q("qb_brussel_germany", "true_false", "According to later research by Donald Foster, Brussel told police the bomber was probably born and educated in Germany.", True,
      "True. Metesky was born in Waterbury, Connecticut, to Lithuanian parents. Brussel's 1968 memoir left that miss out.",
      ["wiki_op"], "hook", "brussel_profile", 2),
    q("qb_homology_def", "mcq", "What is the 'homology assumption' in profiling?", 1,
      "Homology: offenders who commit crimes in similar ways have similar backgrounds. Consistency is the separate idea that one offender behaves similarly across his own crimes.",
      ["wiki_op"], "what_it_is", None, 2, options=["An offender behaves the same way in all his crimes", "Similar crimes are committed by similar kinds of people", "Offenders strike close to home", "Crime scenes reflect the victim's personality"]),
    q("qb_no_profiler", "true_false", "The FBI has an official job title called 'Profiler'.", False,
      "False. The FBI's FAQ says it has no job called profiler; supervisory special agents at the NCAVC do the work.",
      ["milcom_fbi"], "what_it_is", "quantico", 1),
    q("qb_bertillon", "mcq", "What did Alphonse Bertillon standardise in 1888?", 0,
      "The mug shot: a face-on and a profile photograph, alongside his body measurements.",
      ["wiki_bertillon"], "roots", "bertillon", 1, options=["The police mug shot", "Fingerprint classification", "The lie detector", "The criminal profile"]),
    q("qb_order_roots", "order", "Put these in order, earliest first.", ["Lombroso's Criminal Man", "Thomas Bond's Ripper report", "Langer's report on Hitler", "Brussel's Mad Bomber profile", "FBI Behavioral Science Unit formed"],
      "1876, 1888, 1943, 1956, 1972.", ["wiki_op", "wiki_lombroso", "wiki_bond", "wiki_langer"], "roots", None, 2,
      items=[{"label": "Lombroso's Criminal Man", "year": 1876}, {"label": "Thomas Bond's Ripper report", "year": 1888}, {"label": "Langer's report on Hitler", "year": 1943}, {"label": "Brussel's Mad Bomber profile", "year": 1956}, {"label": "FBI Behavioral Science Unit formed", "year": 1972}]),
    q("qb_meirhofer", "true_false", "In the 1973 Montana case, a truth-serum interview and polygraph exposed David Meirhofer.", False,
      "False. The polygraph was inconclusive and he was released. A recorded phone call identified his voice.",
      ["wiki_meirhofer"], "quantico_years", "teten_meirhofer", 2),
    q("qb_vicap", "mcq", "ViCAP, launched in 1985 with Robert Ressler's help, is best described as:", 3,
      "A central database for linking unsolved violent crimes across police forces, set up with LAPD's Pierce Brooks.",
      ["wiki_ressler", "wiki_op"], "quantico_years", "ressler", 2, options=["A personality test for offenders", "A prison interview programme", "A training film", "A database for linking violent crimes"]),
    q("qb_canter2004", "mcq", "When Canter's team analysed 100 US serial killings in 2004, what did they find?", 2,
      "Organized features were common to most killings and disorganized ones were rare; no distinct two-type split appeared.",
      ["canter2004"], "typology", "canter_test", 2, options=["A clean split into organized and disorganized", "Three types: organized, disorganized and mixed", "No distinct types; 'organized' features were common to most", "Disorganized killers were the majority"]),
    q("qb_orgdis_tf", "true_false", "The organized/disorganized typology was first published after being tested on a large random sample of killers.", False,
      "False. It came from informal interviews with 36 convicted offenders and was tested statistically only later.",
      ["wiki_op", "canter2004"], "typology", "org_dis", 2),
    q("qb_pinizzotto", "mcq", "In Pinizzotto and Finkel's 1990 test, where did FBI profilers clearly beat the other groups?", 1,
      "On the rape case. On the murder case they were no better on average.",
      ["apa2004"], "tests", "pinizzotto", 2, options=["On the murder case", "On the rape case", "On both cases", "On neither"]),
    q("qb_snook_hl", "higher_lower", "Snook's 2007 meta-analysis: was the profilers' advantage higher or lower for offence behaviours than for the overall description?", "lower",
      "Overall description r = .24; offence behaviours r = .00.", ["snook2008"], "tests", "snook_meta", 2,
      options=[{"label": "Overall description", "value": 0.24, "unit": "r"}, {"label": "Offence behaviours", "value": 0.0, "unit": "r"}]),
    q("qb_forer", "mcq", "In Forer's 1948 test, where did the 'personal' description each student received come from?", 3,
      "Every student got the same text, assembled from a newsstand astrology book. They rated it 4.30 out of 5.",
      ["wiki_barnum"], "illusion", "barnum", 1, options=["Each student's test answers", "A psychiatrist's interview", "Their teachers' reports", "A newsstand astrology book"]),
    q("qb_alison", "true_false", "When officers compared one profile with a fabricated offender, they rated it as accurate as officers who saw the real offender.", True,
      "True. Both groups averaged about 5.3 out of 7.", ["snook2008", "alison2003"], "illusion", "alison_two_offenders", 2),
    q("qb_mischel", "mcq", "Walter Mischel's 1968 book challenged which assumption?", 0,
      "That people behave consistently across different situations, the trait assumption profiling relies on.",
      ["wiki_mischel"], "person_situation", "mischel", 2, options=["That behaviour is consistent across situations", "That offenders strike near home", "That DNA can identify relatives", "That memory can be read from EEG"]),
    q("qb_homology_tf", "true_false", "Mokros and Alison (2002) found that rapists with similar crime-scene behaviour were similar in age, job and record.", False,
      "False. There was no significant relationship, a direct blow to homology.", ["mokros2002"], "person_situation", "homology", 2),
    q("qb_stagg", "mcq", "Why did the judge throw out the case against Colin Stagg in 1994?", 1,
      "Mr Justice Ognall called the undercover 'honeytrap' operation 'deceptive conduct of the grossest kind'.",
      ["wiki_nickell"], "failures", "nickell_stagg", 2, options=["DNA cleared him", "The undercover honeytrap was deceptive", "The profiler withdrew", "A witness recanted"]),
    q("qb_sniper_car", "image_id", "The D.C. snipers fired from this car while police hunted a white van. What was it?", 2,
      "A 1990 Chevrolet Caprice with a firing port cut into the trunk.", ["wiki_dcsniper"], "failures", "dc_sniper", 1,
      image_id="img_caprice_trunk", options=["A white box truck", "A Ford Econoline van", "A 1990 Chevrolet Caprice", "A Jeep Cherokee"]),
    q("qb_btk", "mcq", "What finally identified BTK in 2005?", 3,
      "Metadata in a deleted Word file on a floppy disk: 'Christ Lutheran Church' and 'Dennis'.", ["wiki_rader"], "what_caught_them", "btk_floppy", 1,
      options=["A psychological profile", "A fingerprint on a letter", "A tip from his wife", "Metadata on a floppy disk"]),
    q("qb_unabomber", "true_false", "The FBI's 1983 replacement profile of the Unabomber, an airline mechanic, led to his arrest.", False,
      "False. His brother David recognised the manifesto's phrasing.", ["wiki_kaczynski"], "what_caught_them", "unabomber", 2),
    q("qb_buffer", "mcq", "In geographic profiling, what is the 'buffer zone'?", 0,
      "An area right around the offender's home where he tends to avoid offending, in case he is recognised.",
      ["wiki_geoprof"], "better_methods", "distance_decay", 2, options=["A ring around home where offenders avoid striking", "The area police search first", "The distance a commuter offender travels", "A zone of high police patrols"]),
    q("qb_rossmo", "true_false", "Kim Rossmo's 1998 conclusion that a serial killer was targeting women in Vancouver was accepted at once.", False,
      "False. Senior officers rejected it; Robert Pickton was arrested in 2002.", ["wiki_rossmo"], "better_methods", "rossmo", 2),
    q("qb_cta_year", "mcq", "When were India's 'criminal tribes' denotified?", 2,
      "On 31 August 1952, after the 1924 Act was repealed in 1949. The Habitual Offenders Acts followed.",
      ["wiki_cta"], "india", "criminal_tribes_act", 2, options=["1871", "1924", "1952", "1971"]),
    q("qb_selvi", "mcq", "What did the Supreme Court decide in Selvi v. State of Karnataka (2010)?", 1,
      "Forced narcoanalysis, polygraph and brain-mapping tests violate Article 20(3) and Article 21.",
      ["selvi"], "india", "selvi", 2, options=["BEOS is reliable evidence", "Forced narco, polygraph and brain tests are unconstitutional", "Profiles are admissible in court", "Denotified tribes must register with police"]),
    q("qb_silence", "mcq", "How many of the five main Academy Awards did The Silence of the Lambs win?", 3,
      "All five: picture, director, actor, actress and adapted screenplay.", ["wiki_silence"], "on_screen", "silence", 1,
      options=["Two", "Three", "Four", "All five"]),
    q("qb_myth_loner", "true_false", "The FBI's 2008 serial murder report treats 'serial killers are dysfunctional loners' as a myth.", True,
      "True. Many hold jobs and have families; Dennis Rader was president of his church council.", ["fbi_serial2008", "wiki_rader"], "myths", None, 1),
    q("qb_aiact", "mcq", "The EU AI Act bans AI systems that predict crime based solely on what?", 0,
      "Profiling or the assessment of personality traits (Article 5(1)(d)), from 2 February 2025.", ["fpf_aiact"], "now", "eu_ai_act", 2,
      options=["Profiling or personality traits", "Fingerprints", "CCTV footage", "Previous convictions"]),
    q("qb_kohberger", "true_false", "Bryan Kohberger was identified mainly through a behavioural profile.", False,
      "False. DNA on a knife sheath, sightings of his car and phone data identified him.", ["npr_kohberger"], "now", "kohberger", 1),
    q("qb_base_rate", "true_false", "A profile saying 'the offender is male and probably has previous convictions' is strong evidence of profiling skill for a serial sex offence.", False,
      "False. That is true of most such offenders; it restates the base rate.", ["snook2008"], "how_to_judge", None, 2),
]

# ---------- end-of-day quiz ----------
QUIZ = [
    q("q_suit", "guess_clues", "Guess the case from the clues.", "The Mad Bomber, George Metesky",
      "Metesky's 1940 to 1956 campaign; Brussel's profile; Alice Kelly's file search.", ["wiki_metesky"], "hook", "metesky", 1,
      clues=["Pipe bombs carried in wool socks.", "Grand Central Terminal was hit five times.", "Letters were signed F.P.", "A psychiatrist's profile predicted a buttoned double-breasted suit."],
      options=["The Unabomber", "The Mad Bomber, George Metesky", "Wearside Jack", "The Railway Rapist"]),
    q("q_order_cases", "order", "Put these profiling moments in order, earliest first.", ["First FBI profile, Montana", "USS Iowa equivocal death analysis", "Colin Stagg trial collapses", "Richard Jewell named as suspect", "Beltway sniper shootings"],
      "1973, 1989, 1994, 1996, 2002.", ["wiki_meirhofer", "wiki_iowa", "wiki_nickell", "wiki_jewell", "wiki_dcsniper"], "failures", None, 2,
      items=[{"label": "First FBI profile, Montana", "year": 1973}, {"label": "USS Iowa equivocal death analysis", "year": 1989}, {"label": "Colin Stagg trial collapses", "year": 1994}, {"label": "Richard Jewell named as suspect", "year": 1996}, {"label": "Beltway sniper shootings", "year": 2002}]),
    q("q_match_caught", "match", "Match each offender to what actually identified him.", [["George Metesky", "A clerk's file search"], ["Ted Kaczynski", "His brother recognised the writing"], ["Dennis Rader", "Floppy disk metadata"], ["Joseph DeAngelo", "Genetic genealogy"], ["Gary Ridgway", "DNA from 1987 samples"]],
      "None was identified by a personality profile.", ["wiki_metesky", "wiki_kaczynski", "wiki_rader", "wiki_deangelo", "wiki_ridgway"], "what_caught_them", None, 2,
      pairs=[["George Metesky", "A clerk's file search"], ["Ted Kaczynski", "His brother recognised the writing"], ["Dennis Rader", "Floppy disk metadata"], ["Joseph DeAngelo", "Genetic genealogy"], ["Gary Ridgway", "DNA from 1987 samples"]]),
    q("q_pin_quantico", "map_pin", "Tap the FBI Academy at Quantico.", {"lat": 38.5225, "lon": -77.4535},
      "Quantico, Virginia, about 60 km south of Washington, D.C.", ["wiki_bau"], "what_it_is", "quantico", 2,
      target={"lat": 38.5225, "lon": -77.4535, "tolerance_km": 150, "label": "FBI Academy, Quantico"}),
    q("q_pin_wimbledon", "map_pin", "Tap Wimbledon Common, scene of the 1992 Rachel Nickell murder.", {"lat": 51.4338, "lon": -0.2335},
      "South-west London.", ["wiki_nickell"], "failures", "nickell_stagg", 2,
      target={"lat": 51.4338, "lon": -0.2335, "tolerance_km": 40, "label": "Wimbledon Common"}),
    q("q_img_bertillon", "image_id", "What is this card?", 1,
      "Alphonse Bertillon's own anthropometric record: mug shots plus body measurements.", ["wiki_bertillon"], "roots", "bertillon", 2,
      image_id="img_bertillon_card", options=["A Criminal Tribes Act pass", "A Bertillon anthropometric card", "An FBI profile", "A BEOS report"]),
    q("q_img_kemper", "image_id", "This man was one of the FBI's most talkative interviewees. Who is he?", 0,
      "Edmund Kemper, photographed on 28 April 1973.", ["wiki_kemper"], "quantico_years", "kemper", 2,
      image_id="img_kemper", options=["Edmund Kemper", "Gary Ridgway", "George Metesky", "Dennis Rader"]),
    q("q_hl_copson", "higher_lower", "UK officers, 1995: was the share saying they would seek profiling advice again higher or lower than the share calling it operationally useful?", "higher",
      "92.4% would seek it again; 82.6% called it useful.", ["snook2008", "copson1995"], "illusion", None, 2,
      options=[{"label": "Would seek advice again", "value": 92.4, "unit": "%"}, {"label": "Called it operationally useful", "value": 82.6, "unit": "%"}]),
    q("q_hl_accuracy", "higher_lower", "The 1986 FBI case-study profile: were its correct predictions higher or lower than its wrong ones?", "lower",
      "11 correct, 18 wrong: 38% accurate.", ["snook2008"], "illusion", "counting_hits", 2,
      options=[{"label": "Correct predictions", "value": 11, "unit": ""}, {"label": "Wrong predictions", "value": 18, "unit": ""}]),
    q("q_odd_methods", "odd_one_out", "Which of these makes the narrowest, most testable prediction?", 2,
      "Geographic profiling predicts a likely home area, which can be scored. The others are judgements about personality or state of mind.",
      ["wiki_geoprof"], "better_methods", None, 2, options=["Organized/disorganized typing", "Clinical psychoanalytic profile", "Geographic profiling", "Equivocal death analysis"]),
    q("q_odd_india", "odd_one_out", "Which of these was NOT barred from compulsory use by the Selvi judgment?", 3,
      "Selvi covered narcoanalysis, polygraph and brain-mapping (BEAP). Fingerprinting is ordinary identification evidence.",
      ["selvi"], "india", "selvi", 2, options=["Narcoanalysis", "Polygraph", "Brain Electrical Activation Profile", "Fingerprinting"]),
    q("q_mcq_barnum", "mcq", "Why do vague profiles feel accurate after an arrest?", 1,
      "The Barnum effect: general statements seem specific once you know who they are 'about'.", ["wiki_barnum", "snook2008"], "illusion", "barnum", 1,
      options=["Because profilers see the suspect first", "The Barnum effect", "Because DNA confirms them", "Because juries are told to believe them"]),
    q("q_mcq_wearside", "mcq", "How did the Wearside Jack hoax damage the Yorkshire Ripper inquiry?", 0,
      "Police treated the hoaxer's north-east accent as a trait of the killer and looked away from Bradford.", ["wiki_wearside", "wiki_yorkshire"], "failures", "wearside_jack", 2,
      options=["It pointed police to the wrong region and accent", "It made police arrest the hoaxer as the Ripper", "It contained a false DNA sample", "It named the wrong victim"]),
    q("q_tf_duffy", "true_false", "John Duffy matched most of the 17 points in David Canter's profile.", True,
      "True: 13 of 17 by the usual count (some accounts say 12). The Railway Rapist case of 1986 was Britain's first major use of a psychologist's profile.", ["wiki_duffy"], "what_caught_them", "duffy_canter", 1),
    q("q_tf_beos", "true_false", "A June 2025 investigation found BEOS used in at least 700 Indian police cases.", True,
      "True, reported by Science and ThePrint, despite a 2008 expert panel calling its basis 'suboptimal'.", ["theprint_beos"], "india", "beos", 2),
    q("q_compare_canter_rossmo", "compare", "Which picture shows the founder of investigative psychology?", 0,
      "Left: David Canter. Right: Walter Mischel, the personality psychologist.", ["wiki_canter", "wiki_mischel"], "better_methods", "canter_ip", 2,
      image_ids=["img_canter", "img_mischel"], options=["Left", "Right"]),
    q("q_mcq_iowa", "mcq", "What did Sandia National Laboratories conclude about the 1989 USS Iowa explosion?", 2,
      "Probably an accidental overram of powder bags, contradicting the FBI-backed suicide theory.", ["wiki_iowa"], "failures", "iowa", 2,
      options=["Sabotage by Clayton Hartwig", "A Soviet mine", "An accidental overram of powder bags", "A lightning strike"]),
    q("q_match_people", "match", "Match each person to their contribution.", [["Thomas Bond", "Profiled Jack the Ripper, 1888"], ["Walter Langer", "OSS report on Hitler, 1943"], ["Ann Burgess", "Turned FBI interviews into data"], ["Kim Rossmo", "Geographic profiling"], ["Walter Mischel", "Questioned personality consistency"]],
      "Bond 1888, Langer 1943, Burgess from the late 1970s, Rossmo 1990s, Mischel 1968.", ["wiki_bond", "wiki_langer", "wiki_burgess", "wiki_rossmo", "wiki_mischel"], None, None, 2,
      pairs=[["Thomas Bond", "Profiled Jack the Ripper, 1888"], ["Walter Langer", "OSS report on Hitler, 1943"], ["Ann Burgess", "Turned FBI interviews into data"], ["Kim Rossmo", "Geographic profiling"], ["Walter Mischel", "Questioned personality consistency"]]),
    q("q_mcq_cta", "mcq", "By the most widely cited estimate, roughly how many people were subject to the Criminal Tribes Act at independence in 1947?", 1,
      "About 13 million people in 127 communities. Some historians give much lower figures for those still actively covered.", ["wiki_cta"], "india", "criminal_tribes_act", 2,
      options=["1.3 million", "13 million", "130 million", "130,000"]),
    q("q_clues_jewell", "guess_clues", "Guess the person.", "Richard Jewell",
      "The security guard at Atlanta's 1996 Olympics, suspected for 88 days because he fitted a 'lone bomber' profile.", ["wiki_jewell"], "failures", "jewell", 1,
      clues=["He found a green backpack under a bench.", "He helped clear the area before it exploded.", "A newspaper reported he fitted a 'lone bomber' profile.", "Clint Eastwood made a film about him in 2019."],
      options=["Richard Jewell", "Eric Rudolph", "Colin Stagg", "Clayton Hartwig"]),
]

PREQUESTIONS = [
    q("pq_brussel", "true_false", "Guess: the psychiatrist's profile is what led police to the Mad Bomber in 1957.", False,
      "No. A Con Edison clerk found his file. You will see why the profile got the credit.", ["wiki_metesky"], "hook", "alice_kelly", 1),
    q("pq_accuracy", "mcq", "Guess: in controlled tests, how do professional profilers compare with other groups?", 1,
      "Usually only slightly better, and inconsistently; science students sometimes matched them.", ["apa2004", "snook2007"], "tests", None, 2,
      options=["Far more accurate than everyone", "Slightly and inconsistently better at best", "Much worse than students", "Exactly as accurate as psychics"]),
    q("pq_typology", "true_false", "Guess: the famous FBI split of killers into 'organized' and 'disorganized' has strong statistical support.", False,
      "No. A 2004 test of 100 serial killings found no such split.", ["canter2004"], "typology", "canter_test", 2),
    q("pq_india", "mcq", "Guess: which Indian law labelled whole communities as born criminals?", 0,
      "The Criminal Tribes Act of 1871.", ["wiki_cta"], "india", "criminal_tribes_act", 1,
      options=["Criminal Tribes Act, 1871", "Indian Penal Code, 1860", "Arms Act, 1878", "Police Act, 1861"]),
    q("pq_where", "mcq", "Guess: which of these makes the most reliable prediction about an unknown serial offender?", 2,
      "Where he lives: offenders tend to strike near home, the basis of geographic profiling.", ["wiki_geoprof"], "better_methods", None, 2,
      options=["His relationship with his mother", "His IQ", "Roughly where he lives", "His favourite films"]),
]

def c(id, type, front, back, sec, spot=None, img=None, core=False, srcs=None, imgs=None):
    d = {"id": id, "type": type, "front": front, "back": back, "image_id": img, "spotlight_id": spot, "section_id": sec, "core": core, "source_ids": srcs or []}
    if imgs: d["image_ids"] = imgs
    return d

CARDS = [
    c("c01", "image", "Who is this man, and what was his nickname?", "George Metesky, the Mad Bomber of New York (bombs 1940 to 1956).", "hook", "metesky", "img_metesky", True, ["wiki_metesky"]),
    c("c02", "fact", "Who actually found the Mad Bomber's name in 1957?", "Con Edison clerk Alice Kelly, searching workers' compensation files.", "hook", "alice_kelly", None, True, ["wiki_metesky"]),
    c("c03", "why", "Why is Brussel's Mad Bomber profile a weak proof of profiling?", "It was published before the arrest (the bomber read papers), his memoir dropped wrong guesses (Germany, White Plains), and a file search found him.", "hook", "brussel_profile", None, True, ["snook2008", "wiki_op"]),
    c("c04", "cloze", "The two core assumptions of profiling are behavioural ____ and ____.", "Consistency and homology.", "what_it_is", None, None, False, ["wiki_op"]),
    c("c05", "fact", "What does 'homology' mean in profiling?", "Offenders who commit crimes in similar ways have similar backgrounds.", "what_it_is", None, None, False, ["wiki_op"]),
    c("c06", "image", "Name this place and the unit formed there in 1972.", "The FBI Academy, Quantico; the Behavioral Science Unit.", "what_it_is", "quantico", "img_fbi_academy", True, ["wiki_bau"]),
    c("c07", "fact", "Does the FBI have a job called 'Profiler'?", "No. Supervisory special agents at the NCAVC do the work, with no 'psychic flashes'.", "what_it_is", "quantico", None, False, ["milcom_fbi"]),
    c("c08", "why", "How does racial profiling differ from offender profiling?", "Offender profiling works backwards from a crime; racial profiling targets people by group before any crime.", "what_it_is", "racial_profiling", None, False, ["wiki_floyd"]),
    c("c09", "image", "Whose theory said criminals could be recognised by their bodies?", "Cesare Lombroso, L'uomo delinquente, 1876.", "roots", "lombroso", "img_lombroso", False, ["wiki_lombroso"]),
    c("c10", "image", "What is this card, and who invented the system?", "An anthropometric record with mug shots, by Alphonse Bertillon (mug shot standardised 1888).", "roots", "bertillon", "img_bertillon_card", True, ["wiki_bertillon"]),
    c("c11", "fact", "Who wrote a profile of Jack the Ripper in 1888?", "Police surgeon Thomas Bond, report of 10 November 1888.", "roots", "bond_ripper", None, True, ["wiki_bond"]),
    c("c12", "fact", "Who used the word Serienmorder in 1930?", "Ernst Gennat, head of the Berlin murder squad.", "roots", "gennat", None, False, ["wiki_gennat"]),
    c("c13", "fact", "What did Walter Langer's 1943 OSS report predict about Hitler?", "Suicide as the most plausible outcome of defeat.", "roots", "langer_hitler", None, False, ["wiki_langer"]),
    c("c14", "fact", "What was the FBI's first active-case profile?", "Montana, 1973: the Susan Jaeger kidnapping; David Meirhofer was caught after an anniversary phone call.", "quantico_years", "teten_meirhofer", None, True, ["wiki_meirhofer", "wiki_teten"]),
    c("c15", "image", "Who is this FBI agent, co-founder of ViCAP?", "Robert Ressler.", "quantico_years", "ressler", "img_ressler", False, ["wiki_ressler"]),
    c("c16", "image", "Whose 1995 memoir became the Netflix series Mindhunter?", "John E. Douglas.", "quantico_years", "douglas", "img_douglas", True, ["wiki_douglas"]),
    c("c17", "image", "This nurse researcher helped turn FBI prison interviews into data. Who is she?", "Ann Wolbert Burgess.", "quantico_years", "burgess", "img_burgess", False, ["wiki_burgess"]),
    c("c18", "fact", "How many offenders did the FBI interview for its 1970s to 80s study?", "36.", "quantico_years", None, None, False, ["wiki_op"]),
    c("c19", "image", "Which talkative killer taught the FBI agents in Mindhunter?", "Edmund Kemper.", "quantico_years", "kemper", "img_kemper", False, ["wiki_kemper"]),
    c("c20", "fact", "Who developed the organized/disorganized split, and when?", "Roy Hazelwood, FBI, 1980.", "typology", "org_dis", None, False, ["wiki_hazelwood"]),
    c("c21", "fact", "What did Canter's 2004 test of 100 serial killings find?", "No distinct organized/disorganized types: organized features were common to most killings.", "typology", "canter_test", None, True, ["canter2004"]),
    c("c22", "fact", "Pinizzotto and Finkel (1990): where did profilers beat the others?", "On the rape case only; no better on the murder.", "tests", "pinizzotto", None, False, ["apa2004"]),
    c("c23", "fact", "In Kocsis's tests, which non-expert group did surprisingly well?", "Science students, who in some tests beat experienced police. Logic seemed to matter more than experience.", "tests", "kocsis", None, False, ["apa2004"]),
    c("c24", "cloze", "Snook 2007: profilers' advantage on offence behaviours was r = ____.", ".00 (overall description .24).", "tests", "snook_meta", None, False, ["snook2008"]),
    c("c25", "image", "Whose 1948 classroom test showed the Barnum effect?", "Bertram Forer; students rated an astrology text 4.30 out of 5.", "illusion", "barnum", "img_forer", True, ["wiki_barnum"]),
    c("c26", "fact", "Alison's two-offender study: what did officers rate the same profile?", "About 5.3 out of 7, whether matched to the real or a fake offender.", "illusion", "alison_two_offenders", None, True, ["snook2008"]),
    c("c27", "cloze", "Of 880 predictions in 21 profiles, ____% were unsubstantiated.", "82%.", "illusion", "alison_two_offenders", None, False, ["snook2008"]),
    c("c28", "fact", "How accurate was the 1986 FBI case-study profile once all predictions were counted?", "38%: 11 right, 18 wrong.", "illusion", "counting_hits", None, False, ["snook2008"]),
    c("c29", "image", "Which psychologist questioned personality consistency in 1968?", "Walter Mischel, Personality and Assessment.", "person_situation", "mischel", "img_mischel", False, ["wiki_mischel"]),
    c("c30", "why", "Why does Mokros and Alison's 2002 finding matter?", "Similar crimes did not mean similar offenders, so the homology inference behind profiling failed.", "person_situation", "homology", None, True, ["mokros2002"]),
    c("c31", "image", "Which case does this place recall, and who was wrongly charged?", "Wimbledon Common, Rachel Nickell (1992); Colin Stagg.", "failures", "nickell_stagg", "img_wimbledon", True, ["wiki_nickell"]),
    c("c32", "fact", "Why was Robert Napper ruled out of the Green Chain rapes?", "He was over six feet tall, a guessed trait used as a filter.", "failures", "nickell_stagg", None, False, ["wiki_nickell"]),
    c("c33", "image", "These scars are from which 1996 bomb, and who was wrongly suspected?", "Centennial Olympic Park, Atlanta; Richard Jewell, for 88 days.", "failures", "jewell", "img_olympic_shrapnel", False, ["wiki_jewell"]),
    c("c34", "image", "What does this car show about the 2002 sniper hunt?", "The Caprice the snipers used; police had focused on a white van and a lone white man.", "failures", "dc_sniper", "img_caprice_trunk", True, ["wiki_dcsniper"]),
    c("c35", "image", "This explosion was blamed on a dead sailor by an FBI analysis. Which ship?", "USS Iowa, 19 April 1989; Sandia later found an accidental overram.", "failures", "iowa", "img_iowa_blast", False, ["wiki_iowa"]),
    c("c36", "fact", "Who was Wearside Jack?", "John Humble, a hoaxer whose 1979 tape steered the Ripper hunt to Sunderland; jailed 2006.", "failures", "wearside_jack", None, False, ["wiki_wearside"]),
    c("c37", "fact", "Railway Rapist, 1986: how many of Canter's 17 points did John Duffy fit?", "13, by the usual count (some accounts say 12).", "what_caught_them", "duffy_canter", None, True, ["wiki_duffy"]),
    c("c38", "fact", "What identified the Unabomber?", "His brother David recognised the manifesto's phrasing.", "what_caught_them", "unabomber", None, False, ["wiki_kaczynski"]),
    c("c39", "fact", "What identified BTK in 2005?", "Metadata on a floppy disk: 'Christ Lutheran Church' and 'Dennis'.", "what_caught_them", "btk_floppy", None, True, ["wiki_rader"]),
    c("c40", "image", "Who is this, and what technique caught him in 2018?", "Joseph James DeAngelo, the Golden State Killer; genetic genealogy.", "what_caught_them", "gsk_genealogy", "img_deangelo", False, ["wiki_deangelo"]),
    c("c41", "fact", "What is distance decay?", "Offenders commit fewer crimes the further they are from their base, except a buffer zone right around home.", "better_methods", "distance_decay", None, True, ["wiki_geoprof"]),
    c("c42", "image", "Who founded investigative psychology?", "David Canter, Liverpool.", "better_methods", "canter_ip", "img_canter", False, ["wiki_canter"]),
    c("c43", "fact", "Who developed geographic profiling and the Rigel software?", "Kim Rossmo, Vancouver police, PhD 1995.", "better_methods", "rossmo", None, False, ["wiki_rossmo"]),
    c("c44", "image", "What law is this 1942 pamphlet issued under?", "The Criminal Tribes Act (1871; 1924 version), which branded whole communities criminal.", "india", "criminal_tribes_act", "img_cta_pamphlet", True, ["wiki_cta"]),
    c("c45", "fact", "What is BEOS?", "Brain Electrical Oscillation Signature profiling, an Indian EEG test claiming to detect 'experiential knowledge'; used in 700+ cases.", "india", "beos", None, True, ["theprint_beos"]),
    c("c46", "image", "What did this court rule in Selvi (2010)?", "Forced narco, polygraph and brain tests violate Articles 20(3) and 21.", "india", "selvi", "img_sci", False, ["selvi"]),
    c("c47", "image", "Which theatre did this writer help found, and with which community?", "Mahasweta Devi; Budhan Theatre, with the Chhara of Ahmedabad (1998).", "india", "budhan", "img_mahasweta", False, ["wiki_budhan"]),
    c("c48", "fact", "What did Sukanya Shantha v. Union of India (2024) strike down?", "Prison-manual rules that assigned work by caste and treated denotified tribes as habitual offenders.", "india", "sukanya", None, False, ["barbench_sukanya"]),
    c("c49", "fact", "What does Article 5(1)(d) of the EU AI Act ban?", "AI predicting crime risk based solely on profiling or personality traits, from 2 February 2025.", "now", "eu_ai_act", None, True, ["fpf_aiact"]),
    c("c50", "fact", "What identified Bryan Kohberger?", "DNA on a knife sheath, his car on camera and phone data, not a profile. Sentenced 23 July 2025.", "now", "kohberger", None, False, ["npr_kohberger"]),
    c("c51", "image", "Whose map is this, and what did it find?", "John Snow's 1854 cholera map; deaths clustered around the Broad Street pump.", "better_methods", None, "img_snow_map", False, ["lecomber2011"]),
    c("c52", "fact", "Where did geographic profiling rank the Broad Street pump among 13 pumps?", "First, in the top 0.2% of the geoprofile (Le Comber and colleagues, 2011).", "better_methods", None, None, False, ["lecomber2011"]),
]

BEST_FACTS = [
    {"fact": "The Mad Bomber was not found by the famous profile. A Con Edison clerk, Alice Kelly, found his file because it used the word 'injustice', the same word as his letters to a newspaper.", "why_surprising": "Profiling's founding legend was really a records search.", "score": 10, "spotlight_id": "alice_kelly", "source_ids": ["wiki_metesky", "snook2008"]},
    {"fact": "The FBI's own FAQ says it has no job called 'Profiler', and that its analysts do not get 'vibes' or 'psychic flashes' at crime scenes.", "why_surprising": "The most famous job in crime fiction does not officially exist.", "score": 9, "spotlight_id": "quantico", "source_ids": ["milcom_fbi"]},
    {"fact": "Police ruled the real killer of Rachel Nickell, Robert Napper, out of an earlier rape series because he was over six feet tall.", "why_surprising": "A guessed physical trait let a serial attacker walk free.", "score": 9, "spotlight_id": "nickell_stagg", "source_ids": ["wiki_nickell"]},
    {"fact": "When officers were shown one profile alongside two completely different 'offenders', both groups rated it equally accurate, about 5.3 out of 7.", "why_surprising": "A profile can seem to fit whoever is arrested.", "score": 9, "spotlight_id": "alison_two_offenders", "source_ids": ["snook2008"]},
    {"fact": "A celebrated 1986 FBI profile made 29 predictions; only 11 were right, a 38% hit rate, yet it was published as a success.", "why_surprising": "Success stories hide the misses.", "score": 9, "spotlight_id": "counting_hits", "source_ids": ["snook2008"]},
    {"fact": "The organized/disorganized typology, still taught worldwide, failed when tested on 100 US serial killings in 2004: no two types appeared.", "why_surprising": "The most famous profiling idea was never validated before it spread.", "score": 9, "spotlight_id": "canter_test", "source_ids": ["canter2004"]},
    {"fact": "BTK asked police whether a floppy disk could be traced. They replied in a newspaper ad, 'Rex, it will be ok', and the disk's metadata named his church and 'Dennis'.", "why_surprising": "A 30-year hunt ended because a killer trusted the police's tech advice.", "score": 9, "spotlight_id": "btk_floppy", "source_ids": ["wiki_rader"]},
    {"fact": "By the most cited estimate, India's Criminal Tribes Act covered about 13 million people in 127 communities at independence, presumed criminal by birth.", "why_surprising": "Profiling by birth was the law for 78 years.", "score": 9, "spotlight_id": "criminal_tribes_act", "source_ids": ["wiki_cta"]},
    {"fact": "In some of Kocsis's profiling tests, science students picked for their logical reasoning outscored experienced police officers.", "why_surprising": "Logic beat years on the job.", "score": 8, "spotlight_id": "kocsis", "source_ids": ["apa2004"]},
    {"fact": "Ten of 14 American Psychological Association experts rejected the FBI analysis that blamed sailor Clayton Hartwig for the USS Iowa blast; engineers later pointed to an accident.", "why_surprising": "A psychological autopsy convicted a dead man in public.", "score": 8, "spotlight_id": "iowa", "source_ids": ["wiki_iowa"]},
    {"fact": "Geographic profiling, built to find serial killers, ranked the Broad Street pump first of 13 pumps in John Snow's 1854 cholera data.", "why_surprising": "A crime tool solves an epidemic retroactively.", "score": 8, "spotlight_id": "distance_decay", "source_ids": ["lecomber2011"]},
    {"fact": "Students in Forer's 1948 class rated a 'personal' description 4.30 out of 5. All had the same text, copied from an astrology book.", "why_surprising": "Vague words feel tailor-made.", "score": 8, "spotlight_id": "barnum", "source_ids": ["wiki_barnum"]},
    {"fact": "Berlin's Ernst Gennat used the word Serienmorder in 1930, decades before 'serial killer' became an FBI term.", "why_surprising": "A famous American coinage has a German ancestor.", "score": 7, "spotlight_id": "gennat", "source_ids": ["wiki_gennat", "wiki_ressler"]},
    {"fact": "India's BEOS brain test has been used in at least 700 cases, though its main validation study, of 110 people, was never peer reviewed.", "why_surprising": "Unvalidated neuroscience is steering real investigations.", "score": 8, "spotlight_id": "beos", "source_ids": ["theprint_beos"]},
    {"fact": "By the 2020s only two full-time behavioural investigative advisers were supporting all of Britain's police forces.", "why_surprising": "The 'profiler' profession is tiny outside fiction.", "score": 7, "spotlight_id": "uk_bia", "source_ids": ["npcc_bia"]},
    {"fact": "The Wearside Jack hoax tape may have delayed the Yorkshire Ripper's arrest by 18 months; police had interviewed Sutcliffe nine times.", "why_surprising": "One fake clue outweighed nine real interviews.", "score": 8, "spotlight_id": "wearside_jack", "source_ids": ["wiki_wearside", "wiki_yorkshire"]},
]
BEST_FACTS.sort(key=lambda f: -f["score"])

VERIFICATION = [
    {"claim": "Copson (1995): profiling advice led directly to identifying the offender in about 3% of cases", "status": "unverified", "note": "The 82.6% 'useful' and 92.4% 'would use again' figures come from Snook et al. (2008). The roughly 3% identification figure appears only in secondary study notes; the original Police Research Group report was not available. The day says 'rarely' rather than giving a number."},
    {"claim": "Profilers predicted a lone white male in the 2002 D.C. sniper case", "status": "unverified", "note": "Widely reported in secondary accounts (Britannica, AP-derived pieces); no single published FBI profile was found. Wikipedia confirms the white van focus and repeated plate checks of the Caprice."},
    {"claim": "Attribution of the 1871 'tribes whose ancestors were criminals from time immemorial' speech", "status": "disputed", "note": "Wikipedia attributes near-identical wording both to T. V. Stephens and to James Fitzjames Stephen. The day says 'the official usually named as T. V. Stephens'."},
    {"claim": "Number of offenders interviewed by the FBI (36) and the period", "status": "range", "note": "Sources agree on 36; start dates are given as 1976 (Ressler article) and early 1978 (offender profiling article)."},
    {"claim": "Kocsis studies: ranking of groups", "status": "disputed", "note": "Kocsis reports profilers first and science students second; Bennell, Jones, Taylor and Snook (2006) argued the scoring method favoured profilers. Original papers not read in full."},
    {"claim": "Mokros and Alison (2002) sample details", "status": "unverified", "note": "Abstract-level summary only (via Wikipedia); sample size not checked against the paper."},
    {"claim": "Budhan Sabar's date of death", "status": "range", "note": "CBI puts the death on 16 February 1998; ETV Bharat says his wife learned of it on 17 February. Reports also differ on the 2023 sentence (13 years per ETV Bharat; another report says five)."},
    {"claim": "Burari deaths date and count hanging", "status": "unverified", "note": "The Quint confirms 11 deaths in July 2018 and the CBI report of 12 September 2018; 1 July date and 'ten hanging' are from widely reported coverage, not the report itself."},
    {"claim": "MARVEL crime-location prediction modules", "status": "unverified", "note": "Described in government and press material (NITI Aayog frontier tech page); no independent evaluation found."},
    {"claim": "About 13 million people in 127 communities under the Criminal Tribes Act in 1947", "status": "range", "note": "The 13 million / 127 communities figure is the most cited (Wikipedia, TISS report). Other historians, such as Sarah Gandee, estimate about 3.5 million people were still actively within the Act's scope by independence."},
    {"claim": "John Duffy fitted 13 of Canter's 17 points", "status": "range", "note": "Most accounts say 13 of 17; Crime and Investigation says at least 12."},
    {"claim": "Pinizzotto and Finkel (1990): profilers most accurate on the rape case", "status": "disputed", "note": "The APA Monitor (2004) summary says profilers beat the other groups on the rape case. Saks and colleagues (APA Monitor letters, October 2004) noted that as a share of statements, students scored 91% on the rape case against profilers' 82%."},
    {"claim": "Brussel's prediction of the double-breasted suit", "status": "disputed", "note": "Known mainly from Brussel's own 1968 memoir; Snook et al. note the profile was published before the arrest and Metesky followed the press."},
]
for sid in ["brussel_profile", "pinizzotto", "kocsis", "snook_meta", "alison_two_offenders", "homology", "rossmo", "uk_bia", "burari", "kohberger", "mahacrimeos"]:
    VERIFICATION.append({"claim": f"Image for spotlight {sid}", "status": "no_image", "note": "No openly licensed photo of this study, person or event was found on Wikimedia Commons; left without an image rather than using a generic one.", "spotlight_id": sid})

SIDE_DISH = {
    "area": "Epidemiology",
    "title": "The killer-hunting algorithm that found a cholera pump",
    "body_md": "On 31 August 1854 cholera broke out in Soho, London. Physician **John Snow** marked each death on a street map and saw them clustered around a water pump on Broad Street. The parish removed the pump's handle on 8 September, though the outbreak may already have been in decline. His map became a founding image of epidemiology.\n\nMore than 150 years later, biologist **Steven Le Comber** at Queen Mary University of London teamed up with **Kim Rossmo**, the policeman who invented geographic profiling. They asked a simple question: if cholera deaths are treated like a serial offender's crimes, can the algorithm find the 'home base'? Using 321 disease sites and 13 neighbourhood pumps, it ranked the Broad Street pump first, in the top 0.2% of the map.\n\nThey then tried a live problem: malaria in Cairo. From 139 case locations the model ranked 59 possible water sources. Seven actually held the mosquito Anopheles sergentii, and the model placed six of them in its top six. Field teams had searched almost 300 square kilometres to find those sites.\n\nThe same team later fed in the locations of 140 Banksy artworks in London and Bristol. The heat map pointed to places linked to Robin Gunningham, a name first printed in 2008. In March 2026 a Reuters investigation also named Gunningham, which Banksy's lawyer disputed.\n\nThe lesson for today's topic: the part of profiling that travels to other sciences is the narrow, testable one, the map, not the mind-reading.",
    "image_ids": ["img_snow_map", "img_snow_pump", "img_banksy_irpin"],
    "card_ids": ["c51", "c52"],
    "source_ids": ["lecomber2011", "qmul_banksy", "rs_banksy", "wiki_rossmo", "wiki_broadstreet"],
}

OFFLINE_TASK = {
    "kind": "try",
    "title": "Write a Barnum profile and test it on a friend",
    "body_md": "**Takes 15 minutes, needs one or two people.**\n\n1. Without telling anyone why, write a 'personality profile' of six sentences that could fit almost anyone. Use Forer's tricks: two-sided statements ('At times you are outgoing, at other times you prefer your own company'), flattering ones ('You have a lot of unused potential'), and vague worries ('You sometimes doubt whether you made the right decision').\n2. Tell a friend you have been reading about profiling and wrote this about them from how they text or what they wear. Ask them to rate its accuracy from 0 to 5.\n3. Now give the same text to a second person and ask the same question.\n4. Reveal the trick and talk about it: which sentences felt most 'personal'? Which could actually be proved wrong?\n\n**Then try the opposite.** Write three statements about your friend that *could* be wrong, such as 'You were born in a month ending in -ber' or 'You have never been to Kolkata'. Notice how much harder it is to sound impressive when you can be checked. That gap is the whole scientific problem with personality profiling.",
    "source_ids": ["wiki_barnum", "snook2008"],
}

HERO = {"image_id": "img_metesky", "kicker": "Day 868 · Crime", "headline": "Profiling: the Mad Bomber's suit, the FBI's mindhunters, and why the evidence keeps disappointing"}

STATS = [
    {"key": "fbi_requests_1971_81", "label": "FBI profiling requests, 1971 to 1981", "value": 192, "year": "1971-1981", "source_ids": ["snook2008"]},
    {"key": "uk_useful", "label": "UK officers calling profiles operationally useful", "value": 82.6, "unit": "%", "year": "1995", "source_ids": ["snook2008"]},
    {"key": "snook_r_overall", "label": "Profiler advantage, overall description (r)", "value": 0.24, "year": "2007", "source_ids": ["snook2008"]},
    {"key": "unsubstantiated", "label": "Profile predictions with no reasoning", "value": 82, "unit": "%", "year": "2003", "source_ids": ["snook2008"]},
    {"key": "cta_people_1947", "label": "People under India's Criminal Tribes Act at independence", "value": 13000000, "year": "1947", "source_ids": ["wiki_cta"]},
    {"key": "beos_cases", "label": "Indian cases using BEOS brain tests", "value": 700, "year": "2025", "source_ids": ["theprint_beos"]},
]

def collect_image_refs(obj, acc):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("image_id",) and isinstance(v, str): acc.add(v)
            elif k == "image_ids" and isinstance(v, list): acc.update(v)
            else: collect_image_refs(v, acc)
    elif isinstance(obj, list):
        for x in obj: collect_image_refs(x, acc)

day = {
    "schema_version": 2, "id": "t0868", "day": 868, "area": "Crime", "title": "Profiling and its scientific problems",
    "native_name": None, "as_of": "2026-10-25", "reading_minutes": 55,
    "hero": HERO, "geo": None, "stats": STATS,
    "prequestions": PREQUESTIONS, "sections": SECTIONS, "cards": CARDS, "quiz": QUIZ, "quiz_bank": QUIZ_BANK,
    "images": [], "media": MEDIA, "sources": SOURCES, "verification": VERIFICATION,
    "side_dish": SIDE_DISH, "offline_task": OFFLINE_TASK, "best_facts": BEST_FACTS,
}
refs = set(); collect_image_refs(day, refs)
day["images"] = [i for i in IMAGES if i["id"] in refs]
missing = refs - {i["id"] for i in IMAGES}
if missing: raise SystemExit(f"unknown image ids: {missing}")
used_src = set()
def collect_src(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "source_ids": used_src.update(v)
            else: collect_src(v)
    elif isinstance(o, list):
        for x in o: collect_src(x)
collect_src(day)
out = os.path.join(ROOT, "data", "days", "0868.json")
json.dump(day, open(out, "w"), ensure_ascii=False, indent=1)
print("wrote", out, "images", len(day["images"]), "unused sources", sorted({s["id"] for s in SOURCES} - used_src))
