"""The RevOps Funnel Equations, version 3 (owner, 2026-10-07).

One metric per stage, per funnel shape. Each metric is a ratio that measures how well that stage works.
Each stage has one equation for that metric, built from short forms, with one line per channel or variant.
Every short form is defined in one line right under the stage. Only + − × ÷.

VARS:  id -> dict(short, name, text, value, rng)
       short: the short form shown in equations (HTML).  text: the one-line definition shown under the stage.
LINES: computed in order. (result, expr, funnels, stage)
STAGES: per funnel, the six stages: metric id, title, the result ids whose lines are shown.
"""
from __future__ import annotations

W, R, K = "webinar", "rsp", "workshop"
FUNNELS = {W: "Webinar", R: "Reverse Squeeze Page", K: "Workshop Series"}

VARS: dict[str, dict] = {}


def sf(id):
    base, _, sub = id.upper().partition("_")
    return f"{base}<sub>{sub.lower()}</sub>" if sub else base


def v(id, text, value=None, rng=None, name=None, short=None):
    VARS[id] = dict(id=id, short=short or sf(id), name=name or text.split(":")[0], text=text, value=value, rng=rng)


# ---------------------------------------------------------------- stage 1: traffic
v("vr", "Visit Rate: page visits ÷ people reached, across every channel")
v("v", "page visits")
v("vr_e", "visit rate of cold email")
v("vr_c", "visit rate of calendar invites")
v("vr_l", "visit rate of LinkedIn")
v("vr_a", "visit rate of ads")
v("vr_o", "visit rate of posts")
v("n_e", "people emailed", 20000)
v("n_c", "calendar invites sent", 100000)
v("n_l", "LinkedIn requests sent: connection requests", 5000)
v("n_a", "ad impressions", 333000)
v("n_o", "post impressions", 300000)
v("dr_e", "email delivered rate: emails delivered ÷ emails sent", 0.98, [0.98, 0.995])
v("or_e", "email open rate: people who opened ÷ people who received it", 0.30, [0.15, 0.35])
v("cr_e", "email click rate: people who clicked ÷ people who opened", 0.04, [0.02, 0.08])
v("lr", "page load rate: page visits ÷ link clicks (set by page speed)", 0.90, [0.75, 0.95])
v("dr_c", "invite delivered rate: invites delivered ÷ invites sent", 0.97, [0.95, 0.99])
v("cl_c", "invite link click rate: clicks on the invite link ÷ invites delivered", 0.002, [0.001, 0.005])
v("ac_l", "acceptance rate: requests accepted ÷ requests sent", 0.22, [0.2075, 0.30])
v("ms_l", "message reach: people messaged ÷ people who accepted", 0.90, [0.85, 0.98])
v("cr_l", "LinkedIn click rate: link clicks ÷ people messaged", 0.04, [0.02, 0.06])
v("ct_a", "ad click-through rate: ad clicks ÷ impressions", 0.012, [0.0045, 0.0259])
v("lv_a", "ad page view rate: page views ÷ ad clicks", 0.80, [0.70, 0.90])
v("ct_o", "post click-through rate: link clicks ÷ post impressions", 0.0008, [0.0005, 0.003])

# ---------------------------------------------------------------- stage 2: landing and sign-up
v("pa", "Page-to-Attendee Rate: attendees who signed up on the page ÷ page visits")
v("hw", "Half-Watch Rate: people who watched more than half of the video on their first visit ÷ page visits")
v("pq", "Page-to-1.5-Day Rate: people who signed up on the page and attended 1.5 days or more ÷ page visits")
v("rr", "registration rate: sign-ups ÷ page visits")
v("st", "stay rate: visits that stayed 10 seconds or more ÷ page visits (100% minus bounce rate)", 0.55, [0.45, 0.70])
v("fs", "form seen rate: people who scrolled to the form ÷ people who stayed", 0.70, [0.60, 0.90])
v("ft", "form start rate: people who started the form ÷ people who saw it", 0.35, [0.25, 0.50])
v("fc", "form finish rate: people who submitted ÷ people who started", 0.70, [0.60, 0.85])
v("su_f", "show-up rate of page sign-ups: page sign-ups who attended ÷ page sign-ups")
v("su_0", "show-up rate of page sign-ups who skipped the thank you page action", 0.30, [0.25, 0.40])
v("su_1", "show-up rate of page sign-ups who did the thank you page action (add to calendar, join WhatsApp)", 0.55, [0.45, 0.70])
v("t1", "thank you page action rate: people who did the action ÷ people who saw the thank you page", 0.40, [0.30, 0.60])
v("ar", "auto-registrants: people registered without the form (calendar Yes or Maybe, interested replies, inbound messages)")
v("ar_c", "registered by a Yes or Maybe on the calendar invite")
v("ar_e", "registered by an interested reply to cold email")
v("ar_l", "registered by an interested reply on LinkedIn")
v("ar_o", "registered from inbound messages after posts")
v("ys", "RSVP Yes rate: Yes ÷ invites delivered", 0.005, [0.003, 0.013])
v("my", "RSVP Maybe rate: Maybe ÷ invites delivered", 0.004, [0.002, 0.01])
v("rp_e", "email reply rate: people who replied ÷ people who received the email", 0.04, [0.034, 0.055])
v("ye", "email interested share: interested replies ÷ all email replies", 0.25, [0.20, 0.40])
v("rp_l", "LinkedIn reply rate: people who replied ÷ people messaged", 0.25, [0.2222, 0.40])
v("yl", "LinkedIn interested share: interested replies ÷ all LinkedIn replies", 0.30, [0.20, 0.40])
v("eg", "post engagement rate: likes, comments and shares ÷ post impressions", 0.023, [0.0229, 0.0765])
v("mg", "inbound message rate: inbound messages ÷ engagements", 0.02, [0.005, 0.03])
v("ir", "inbound registered rate: inbound people registered ÷ inbound messages", 0.50, [0.40, 0.80])
v("r", "registrants: page sign-ups plus auto-registrants")
v("pl", "play rate: people who pressed play ÷ people who stayed", 0.65, [0.60, 0.80])
v("hh", "half-watch rate of plays: people who passed halfway ÷ people who pressed play", 0.30, [0.25, 0.45])
v("h_1", "people who watched more than half on their first visit")
v("os", "early-exit opt-in rate: people who left before halfway and gave their email ÷ people who left before halfway", 0.04, [0.02, 0.08])
v("p", "people you can remind: early leavers who gave their email, plus auto-registrants")

# ---------------------------------------------------------------- stage 3: reminders and nurture
v("su", "Show-Up Rate: attendees ÷ registrants")
v("nh", "Nurtured Half-Watch Rate: people brought past halfway by reminders ÷ people you can remind")
v("qd", "1.5-Day Rate: people who attended 1.5 days or more ÷ registrants")
v("su_d", "Day 1 show-up rate: Day 1 attendees ÷ registrants")
v("dj", "direct join rate: people who joined without clicking any reminder ÷ registrants", 0.08, [0.06, 0.12])
v("j_e", "joins from reminder email: people whose first join came from an email link ÷ registrants")
v("j_w", "joins from WhatsApp: people whose first join came from a WhatsApp link ÷ registrants")
v("j_s", "joins from SMS: people whose first join came from a text link ÷ registrants")
v("j_v", "joins after an AI call: people who joined after confirming on the call ÷ registrants")
v("dr_m", "reminder email delivered rate: delivered ÷ sent", 0.97, [0.95, 0.99])
v("or_m", "reminder email open rate: people who opened a reminder ÷ people who got one", 0.45, [0.35, 0.60])
v("jc_m", "email join click rate: people who joined from an email link ÷ people who opened", 0.15, [0.10, 0.30])
v("wo", "WhatsApp opt-in rate: people who opted in ÷ registrants", 0.45, [0.30, 0.70])
v("dr_w", "WhatsApp delivered rate: delivered ÷ sent", 0.96, [0.92, 0.99])
v("rd_w", "WhatsApp read rate: read ÷ delivered", 0.75, [0.65, 0.80])
v("jc_w", "WhatsApp join click rate: people who joined from a WhatsApp link ÷ people who read", 0.12, [0.05, 0.15])
v("sr_s", "SMS reach: registrants with a phone and text consent ÷ registrants", 0.60, [0.50, 0.90])
v("dr_s", "SMS delivered rate: delivered ÷ sent", 0.95, [0.92, 0.98])
v("jc_s", "SMS join click rate: people who joined from a text link ÷ texts delivered", 0.09, [0.087, 0.20])
v("ph", "phone share: registrants the AI caller can ring ÷ registrants", 0.60, [0.50, 0.90])
v("an", "answer rate: calls answered by a person ÷ people called", 0.35, [0.20, 0.45])
v("cf", "confirm rate: people who said they will come ÷ calls answered", 0.50, [0.40, 0.70])
v("cc", "confirmed-and-came rate: people who joined ÷ people who confirmed", 0.60, [0.50, 0.80])
v("a", "attendees")
v("bb_e", "brought back by email: people who returned to the video from an email ÷ people you can remind")
v("bb_w", "brought back by WhatsApp ÷ people you can remind")
v("bb_s", "brought back by SMS ÷ people you can remind")
v("bb_v", "brought back by an AI call ÷ people you can remind")
v("bc_e", "email return click rate: people who clicked back to the video ÷ people who opened", 0.12, [0.08, 0.25])
v("bc_w", "WhatsApp return click rate: clicked back ÷ read", 0.10, [0.05, 0.15])
v("bc_s", "SMS return click rate: clicked back ÷ delivered", 0.08, [0.05, 0.15])
v("bc_v", "call return rate: people who went back to the video after the call ÷ calls answered", 0.30, [0.20, 0.45])
v("hr", "half-on-return rate: people who passed halfway this time ÷ people who came back", 0.45, [0.30, 0.60])
v("h", "people who watched more than half, first visit plus reminders")
v("sk", "stick rate: people who attended 1.5 days or more ÷ Day 1 attendees", 0.60, [0.50, 0.75])
v("d_1", "Day 1 attendees")
v("d_2", "Day 2 attendees")
v("d_3", "Day 3 attendees")
v("ret_2", "Day 2 return rate: Day 2 attendees ÷ Day 1 attendees", 0.70, [0.60, 0.85])
v("ret_3", "Day 3 return rate: Day 3 attendees ÷ Day 2 attendees", 0.80, [0.70, 0.90])
v("q", "people who attended 1.5 days or more")

# ---------------------------------------------------------------- stage 4: conversion
v("br", "Booking Rate: calls booked ÷ attendees")
v("br_h", "Booking Rate: calls booked ÷ people who watched more than half", short="BR")
v("bq", "Booking Rate: calls booked ÷ people who attended 1.5 days or more")
v("so", "stayed for the offer: people present at the offer minute ÷ attendees", 0.55, [0.45, 0.70])
v("en", "engaged share: people who answered a poll, asked a question or chatted ÷ people at the offer", 0.50, [0.25, 0.90])
v("ce", "engaged click rate: offer clicks ÷ engaged people at the offer", 0.25, [0.15, 0.30])
v("cq", "quiet click rate: offer clicks ÷ quiet people at the offer", 0.05, [0.03, 0.08])
v("ct", "offer click rate: offer clicks ÷ people at the offer")
v("bf", "booking finish rate: calls booked ÷ offer clicks", 0.50, [0.35, 0.60])
v("bl", "live booking rate: calls booked during the event ÷ attendees")
v("fu", "follow-up click rate: booking-link clicks from follow-up messages ÷ people who had not booked", 0.06, [0.03, 0.10])
v("ns", "no-shows per attendee: (registrants − attendees) ÷ attendees")
v("rw", "replay watch rate: replay viewers ÷ no-shows", 0.15, [0.10, 0.25])
v("rc", "replay click rate: offer clicks from the replay ÷ replay viewers", 0.03, [0.02, 0.06])
v("b", "calls booked")
v("rt", "reached the button: people who reached the button's minute ÷ people who watched more than half", 0.75, [0.60, 0.90])
v("ap", "apply click rate: clicks on Apply ÷ people who reached the button", 0.15, [0.05, 0.20])
v("af", "application finish rate: applications sent ÷ application page visits", 0.40, [0.30, 0.60])
v("ab", "application-to-booking rate: calls booked ÷ applications", 0.60, [0.50, 0.80])
v("b_1", "first-time booking rate on Day 1: first-time bookings ÷ Day 1 attendees", 0.03, [0.02, 0.05])
v("b_2", "first-time booking rate on Day 2: first-time bookings ÷ Day 2 attendees", 0.05, [0.03, 0.08])
v("b_3", "first-time booking rate on Day 3: first-time bookings ÷ Day 3 attendees", 0.10, [0.06, 0.15])
v("bd", "calls booked live across the three days")
v("fb", "calls booked from follow-ups")

# ---------------------------------------------------------------- stage 5: pipeline
v("cl", "Close Rate: onboarded customers ÷ calls booked")
v("sh", "call show rate: calls held the first time ÷ calls booked")
v("sh_0", "showed with no reminder click ÷ calls booked", 0.55, [0.50, 0.65])
v("sh_e", "showed after confirming from the email reminder ÷ calls booked")
v("sh_w", "showed after confirming from the WhatsApp reminder ÷ calls booked")
v("sh_s", "showed after confirming from the SMS reminder ÷ calls booked")
v("sh_v", "showed after confirming on the AI call ÷ calls booked")
v("dr_r", "call reminder email delivered rate: delivered ÷ sent", 0.97, [0.95, 0.99])
v("or_r", "call reminder email open rate: opened ÷ delivered", 0.60, [0.45, 0.75])
v("cs_e", "email confirm rate: confirmed and showed ÷ people who opened", 0.15, [0.10, 0.25])
v("wp", "WhatsApp reach for calls: booked contacts with WhatsApp ÷ calls booked", 0.50, [0.30, 0.80])
v("cs_w", "WhatsApp confirm rate: confirmed and showed ÷ read", 0.20, [0.10, 0.30])
v("sp", "SMS reach for calls: booked contacts with a phone and consent ÷ calls booked", 0.70, [0.50, 0.95])
v("cs_s", "SMS confirm rate: confirmed and showed ÷ delivered", 0.10, [0.05, 0.20])
v("pv", "phone share for calls: booked contacts the AI caller can ring ÷ calls booked", 0.70, [0.50, 0.95])
v("av", "confirmation call answer rate: answered ÷ called", 0.40, [0.30, 0.60])
v("cs_v", "call confirm rate: confirmed and showed ÷ answered", 0.30, [0.20, 0.45])
v("rb", "rebook rate: no-shows who rebooked ÷ no-shows (the five follow-ups added)")
v("f_1", "rebooked after no-show follow-up 1 (sent right away) ÷ no-shows", 0.12, [0.06, 0.20])
v("f_2", "rebooked after follow-up 2 (3 days later) ÷ no-shows", 0.06, [0.03, 0.10])
v("f_3", "rebooked after follow-up 3 (3 days after that) ÷ no-shows", 0.04, [0.02, 0.06])
v("f_4", "rebooked after follow-up 4 (3 days after that) ÷ no-shows", 0.03, [0.01, 0.05])
v("f_5", "rebooked after follow-up 5 (a week after that) ÷ no-shows", 0.02, [0.01, 0.04])
v("hd", "held rate: calls held, including rebooked ones ÷ calls booked")
v("qr", "qualified rate: qualified ÷ calls held", 0.75, [0.60, 0.85])
v("pr", "proposal rate: proposals sent ÷ qualified", 0.70, [0.50, 0.80])
v("wn", "win rate: proposals accepted ÷ proposals sent")
v("w_0", "accepted with no chasing ÷ proposals sent", 0.30, [0.15, 0.35])
v("d_1f", "accepted after deal follow-up 1 (day 3) ÷ proposals sent", 0.06, [0.03, 0.10], short="DF<sub>1</sub>")
v("d_2f", "accepted after deal follow-up 2 (day 7) ÷ proposals sent", 0.04, [0.02, 0.06], short="DF<sub>2</sub>")
v("d_3f", "accepted after deal follow-up 3 (day 12) ÷ proposals sent", 0.03, [0.01, 0.05], short="DF<sub>3</sub>")
v("py", "payment rate: payments completed ÷ proposals accepted", 0.90, [0.85, 0.98])
v("ob", "onboarding rate: customers onboarded ÷ customers who paid", 0.95, [0.90, 1.0])
v("c", "onboarded customers")

# ---------------------------------------------------------------- stage 6: the next 52 weeks
v("yb", "Yearly Rebooking Rate: calls booked from the 52-week messages ÷ people on the list")
v("l", "people on the list: everyone known who did not become a customer")
for ch, label, reach, sends, dl, op, ck in (("n", "weekly email", 1.0, 52, 0.97, 0.38, 0.015), ("i", "AI newsletter", 0.6, 52, 0.97, 0.40, 0.015),
                                           ("w", "WhatsApp", 0.4, 26, 0.96, 0.70, 0.05), ("s", "SMS", 0.5, 6, 0.95, None, 0.09)):
    v(f"y_{ch}", f"calls booked from {label} ÷ people on the list (its share of the credit)")
    v(f"rc_{ch}", f"{label} reach: people who can get {label} ÷ people on the list", reach, [0.30, 1.0])
    v(f"sn_{ch}", f"{label} sends per person per year", sends)
    v(f"dl_{ch}", f"{label} delivered rate: delivered ÷ sent", dl, [0.92, 0.99])
    if op is not None:
        v(f"op_{ch}", f"{label} {'read' if ch == 'w' else 'open'} rate: {'read' if ch == 'w' else 'opened'} ÷ delivered", op, [0.65, 0.80] if ch == "w" else [0.30, 0.45])
    v(f"ck_{ch}", f"{label} click rate: clicks ÷ {'messages read' if ch == 'w' else 'messages opened' if op else 'texts delivered'}", ck,
      [0.05, 0.15] if ch in ("w", "s") else [0.0115, 0.0262])
v("y_v", "calls booked from AI check-in calls ÷ people on the list")
v("rc_v", "AI call reach: people the AI caller can ring ÷ people on the list", 0.4, [0.30, 0.80])
v("sn_v", "AI check-in calls per person per year", 4)
v("an_v", "check-in call answer rate: answered ÷ called", 0.20, [0.12, 0.35])
v("bv", "booked on the call: calls booked ÷ check-in calls answered", 0.03, [0.02, 0.06])
v("bk", "book-from-click rate: calls booked ÷ clicks from 52-week messages", 0.02, [0.02, 0.05])
v("b_y", "calls booked from the 52 weeks")
v("c_y", "customers from the 52 weeks")

# ---------------------------------------------------------------- the lines (computed in this order)
LINES: list[tuple] = []


def ln(result, expr, fns=(W, R, K), stage=""):
    LINES.append(dict(result=result, expr=expr, fn=list(fns), stage=stage))


S1 = ["vr_e", "vr_c", "vr_l", "vr_a", "vr_o", "v", "vr"]
ln("vr_e", "dr_e * or_e * cr_e * lr", stage="S1")
ln("vr_c", "dr_c * cl_c * lr", stage="S1")
ln("vr_l", "ac_l * ms_l * cr_l * lr", stage="S1")
ln("vr_a", "ct_a * lv_a", stage="S1")
ln("vr_o", "ct_o * lr", stage="S1")
ln("v", "n_e * vr_e + n_c * vr_c + n_l * vr_l + n_a * vr_a + n_o * vr_o", stage="S1")
ln("vr", "v / (n_e + n_c + n_l + n_a + n_o)", stage="S1")

AR = ["ar_c", "ar_e", "ar_l", "ar_o", "ar"]
ln("ar_c", "n_c * dr_c * (ys + my)", stage="S2")
ln("ar_e", "n_e * dr_e * rp_e * ye", stage="S2")
ln("ar_l", "n_l * ac_l * ms_l * rp_l * yl", stage="S2")
ln("ar_o", "n_o * eg * mg * ir", stage="S2")
ln("ar", "ar_c + ar_e + ar_l + ar_o", stage="S2")

# webinar and workshop: the page
ln("rr", "st * fs * ft * fc", (W, K), "S2")
ln("su_f", "su_0 * (1 - t1) + su_1 * t1", (W,), "S2")
ln("pa", "rr * su_f", (W,), "S2")
ln("r", "v * rr + ar", (W, K), "S2")
# rsp: the video page
ln("hw", "st * pl * hh", (R,), "S2")
ln("h_1", "v * hw", (R,), "S2")
ln("p", "v * st * pl * (1 - hh) * os + ar", (R,), "S2")

# reminders (webinar and workshop Day 1)
JOINS = ["j_e", "j_w", "j_s", "j_v"]
ln("j_e", "dr_m * or_m * jc_m", (W, K), "S3")
ln("j_w", "wo * dr_w * rd_w * jc_w", (W, K), "S3")
ln("j_s", "sr_s * dr_s * jc_s", (W, K), "S3")
ln("j_v", "ph * an * cf * cc", (W, K), "S3")
ln("su", "dj + j_e + j_w + j_s + j_v", (W,), "S3")
ln("a", "r * su", (W,), "S3")
ln("su_d", "dj + j_e + j_w + j_s + j_v", (K,), "S3")
ln("d_1", "r * su_d", (K,), "S3")
ln("d_2", "d_1 * ret_2", (K,), "S3")
ln("d_3", "d_2 * ret_3", (K,), "S3")
ln("qd", "su_d * sk", (K,), "S3")
ln("q", "r * qd", (K,), "S3")
# workshop stage 2 metric needs qd
ln("pq", "rr * qd", (K,), "S2")
# rsp nurture
ln("bb_e", "dr_m * or_m * bc_e", (R,), "S3")
ln("bb_w", "wo * dr_w * rd_w * bc_w", (R,), "S3")
ln("bb_s", "sr_s * dr_s * bc_s", (R,), "S3")
ln("bb_v", "ph * an * bc_v", (R,), "S3")
ln("nh", "(bb_e + bb_w + bb_s + bb_v) * hr", (R,), "S3")
ln("h", "h_1 + p * nh", (R,), "S3")

# conversion
ln("ct", "en * ce + (1 - en) * cq", (W,), "S4")
ln("bl", "so * ct * bf", (W,), "S4")
ln("ns", "(r - a) / a", (W,), "S4")
ln("br", "bl + (1 - bl) * fu * bf + ns * rw * rc * bf", (W,), "S4")
ln("b", "a * br", (W,), "S4")
ln("br_h", "rt * ap * af * ab", (R,), "S4")
ln("b", "h * br_h", (R,), "S4")
ln("bd", "d_1 * b_1 + d_2 * b_2 + d_3 * b_3", (K,), "S4")
ln("fb", "(q - bd) * fu * bf", (K,), "S4")
ln("b", "bd + fb", (K,), "S4")
ln("bq", "b / q", (K,), "S4")

# pipeline
ln("sh_e", "dr_r * or_r * cs_e", stage="S5")
ln("sh_w", "wp * dr_w * rd_w * cs_w", stage="S5")
ln("sh_s", "sp * dr_s * cs_s", stage="S5")
ln("sh_v", "pv * av * cs_v", stage="S5")
ln("sh", "sh_0 + sh_e + sh_w + sh_s + sh_v", stage="S5")
ln("rb", "f_1 + f_2 + f_3 + f_4 + f_5", stage="S5")
ln("hd", "sh + (1 - sh) * rb * sh", stage="S5")
ln("wn", "w_0 + d_1f + d_2f + d_3f", stage="S5")
ln("cl", "hd * qr * pr * wn * py * ob", stage="S5")
ln("c", "b * cl", stage="S5")

# 52 weeks
ln("l", "r - c", (W, K), "S6")
ln("l", "p - c", (R,), "S6")
ln("y_n", "rc_n * sn_n * dl_n * op_n * ck_n * bk", stage="S6")
ln("y_i", "rc_i * sn_i * dl_i * op_i * ck_i * bk", stage="S6")
ln("y_w", "rc_w * sn_w * dl_w * op_w * ck_w * bk", stage="S6")
ln("y_s", "rc_s * sn_s * dl_s * ck_s * bk", stage="S6")
ln("y_v", "rc_v * sn_v * an_v * bv", stage="S6")
ln("yb", "y_n + y_i + y_w + y_s + y_v", stage="S6")
ln("b_y", "l * yb", stage="S6")
ln("c_y", "b_y * cl", stage="S6")

# the stages as shown: metric, title, and the lines shown (by result id, in order)
STAGE_TITLES = {"S1": "Traffic", "S2": "Landing and Sign-Up", "S3": "Reminders and Nurture", "S4": "Booking the Call",
                "S5": "The Sales Pipeline", "S6": "The Next 52 Weeks"}
SHOWN = {
    W: [("S1", "vr", ["vr", "v"] + S1[:5]),
        ("S2", "pa", ["pa", "rr", "su_f", "r", "ar"] + AR[:4]),
        ("S3", "su", ["su", "a"] + JOINS),
        ("S4", "br", ["br", "bl", "ct", "ns", "b"]),
        ("S5", "cl", ["cl", "hd", "sh", "sh_e", "sh_w", "sh_s", "sh_v", "rb", "wn", "c"]),
        ("S6", "yb", ["yb", "y_n", "y_i", "y_w", "y_s", "y_v", "l", "b_y"])],
    R: [("S1", "vr", ["vr", "v"] + S1[:5]),
        ("S2", "hw", ["hw", "h_1", "p", "ar"] + AR[:4]),
        ("S3", "nh", ["nh", "bb_e", "bb_w", "bb_s", "bb_v", "h"]),
        ("S4", "br_h", ["br_h", "b"]),
        ("S5", "cl", ["cl", "hd", "sh", "sh_e", "sh_w", "sh_s", "sh_v", "rb", "wn", "c"]),
        ("S6", "yb", ["yb", "y_n", "y_i", "y_w", "y_s", "y_v", "l", "b_y"])],
    K: [("S1", "vr", ["vr", "v"] + S1[:5]),
        ("S2", "pq", ["pq", "rr", "r", "ar"] + AR[:4]),
        ("S3", "qd", ["qd", "su_d", "d_1", "d_2", "d_3", "q"] + JOINS),
        ("S4", "bq", ["bq", "b", "bd", "fb"]),
        ("S5", "cl", ["cl", "hd", "sh", "sh_e", "sh_w", "sh_s", "sh_v", "rb", "wn", "c"]),
        ("S6", "yb", ["yb", "y_n", "y_i", "y_w", "y_s", "y_v", "l", "b_y"])],
}
WHOLE = {W: "(v * rr + ar) * su * br * cl", R: "(h_1 + p * nh) * br_h * cl", K: "(v * rr + ar) * qd * bq * cl"}

# plain short forms: initials of the full name, no subscripts (owner, 2026-10-07)
from eqnames import NAMES  # noqa: E402
for _k, (_full, _short) in NAMES.items():
    VARS[_k]["short"] = _short
    VARS[_k]["full"] = _full
