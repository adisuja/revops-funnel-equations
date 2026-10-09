# The RevOps Funnel Equations: Context for Whoever Edits Next

Read this file in full before changing anything. It holds every decision and rule from the owner (Adi) so far.

## What This Is

A one-page reference, "The RevOps Funnel Equations", for the 3-Day AI RevOps Workshop. It also works as a free lead magnet.
For three funnel shapes (webinar, reverse squeeze page, workshop series), it gives:

- **one metric per stage**, six stages per funnel, each a ratio that shows how well that stage works;
- **one equation per stage** showing what that metric is made of, with one line per channel or variant;
- **a one-line definition** of every short form, right under the stage that uses it.

The one live copy: https://revops-funnel-equations.growthcluborg.workers.dev (Cloudflare, published by Adi's integrator).

There used to be a second copy on GitHub Pages, added because Pages was down on launch night. It was switched off on 2026-10-09. Do not turn GitHub Pages back on, and never link to a github.io address for this page.

## The Sign-Up Gate

The page is a lead magnet, so the equations sit behind a short form (decided 2026-10-09).

- The form asks for name, email and WhatsApp number. Nothing else.
- On submit the equations open on the same page, and the browser remembers it (localStorage key `rfe_unlocked`), so a returning reader never sees the form again.
- The sign-up is posted to the workshop's form receiver and lands in the team's tracker, in its own Funnel Equations tab. It is sent as a registration row with `source` set to `funnel-equations`, because the receiver only accepts its existing form names. Keep that `source` value: the tracker uses it to tell lead magnet sign-ups from workshop registrations.
- Once open, the page carries one link: the free workshop. Do not add a second call to action.
- The form, its script and the link live in `src/equations.py` (`GATE_FORM`, `GATE_JS`, `GATE_CSS`, `WORKSHOP_URL`). Rule 4 still holds around the form: no cards, tips, examples or ranges.
- To see the form again while testing, open the page in a private window, or run `localStorage.removeItem("rfe_unlocked")` in the console.

## The 18 Metrics

| Stage | Webinar | Reverse Squeeze Page | Workshop Series |
|---|---|---|---|
| 1 Traffic | VR Visit Rate = page visits ÷ people reached | VR | VR |
| 2 Landing and Sign-Up | PAR Page-to-Attendee Rate = attendees who signed up on the page ÷ page visits | HWR Half-Watch Rate = watched more than half on first visit ÷ page visits | PDHR Page-to-Day-and-a-Half Rate = page sign-ups who attended 1.5+ days ÷ page visits |
| 3 Reminders and Nurture | SUR Show-Up Rate = attendees ÷ registrants | NHWR Nurtured Half-Watch Rate = people brought past halfway by reminders ÷ remindable people | DHR Day-and-a-Half Rate = attended 1.5+ days ÷ registrants |
| 4 Booking the Call | BR Booking Rate = calls booked ÷ attendees | BR = calls booked ÷ total half-watchers | BR = calls booked ÷ day-and-a-half attendees |
| 5 The Sales Pipeline | CR Close Rate = onboarded customers ÷ calls booked | CR | CR |
| 6 The Next 52 Weeks | YRR Yearly Rebooking Rate = calls booked from 52-week messages ÷ list size | YRR | YRR |

The whole-funnel line for each shape multiplies its stage metrics. The build checks that it equals the stage-by-stage chain. For example, for the webinar: OC = (PV × RR + AR) × SUR × BR × CR.

## Where the Requirements Came From

Adi's original brief, condensed:
- **Stage 1, traffic.** The goal per channel is landing page visits, built from that channel's own numbers:
  - cold email: delivery, open and click rates;
  - calendar invites and LinkedIn: their response and click rates;
  - ads: click-through, page views and lead form completion;
  - organic content: visits, plus inbound messages as their own count.
- **Stage 2, landing and sign-up.** The outcome differs by shape:
  - webinar: attendees, driven by the page's numbers (speed, form steps, thank you pages);
  - reverse squeeze page: people who watch more than 50% of the video;
  - workshop series: people who attend more than 1.5 of the 3 days.
- **Stage 3, multi-channel nurture.** The same outcomes as Stage 2, connected to each reminder channel's delivery, open or read, and click rates. The channels are email, WhatsApp, SMS and AI voice calls (answer, confirm, came).
- **Stage 4, conversion.** The north star is calls booked, connected to everything above.
- **Stage 5, the pipeline.** Every stage gets its own conversion. They come from the GHL pipeline doc and are the same for all three shapes:
  - form filled, evaluation call, qualified, call held, proposal, accepted, paid, onboarding;
  - five no-show follow-ups (sent immediately, then +3, +3, +3 days, then +1 week);
  - three deal follow-ups (day 3, 7 and 12);
  - reminder channels for calls.
- **Stage 6, the 52 weeks.** Per channel: weekly email, AI newsletter, WhatsApp, SMS and AI check-in calls. Each needs delivery, open and click rates, and each channel's bookings give source attribution.

## Owner Rules (Non-Negotiable)

1. **Simple maths only:** + − × ÷ and brackets. Every rate is one count divided by another count. No powers, no probability unions, no Greek letters.
2. **Short forms are the capital initials of a full, readable name**, with no subscripts. For example: AI = Ad Impressions, PI = Post Impressions, VRCE = Visit Rate, Cold Email. If two clash, rename the full name; don't invent notation.
3. **Define every short form right under the stage that uses it**, as "SHORT Full Name: what it means". No jump links or "see #19". A reader must never leave the stage to understand it.
4. **No AI slop.** No cards, pictures, worked examples, tips, typical ranges, tables of advice or filler paragraphs on the page. Compact and to the point.
5. **One metric per stage per funnel**, a ratio that shows that stage's efficiency. No generic totals (cost per customer, total customers, cost per booked call and so on); Adi called those "dumb metrics".
6. **No em dashes or en dashes**, anywhere. Use a colon, a comma, brackets, or "to" for ranges.
7. **No client names or client numbers** in anything public.
8. **Never invent or borrow a benchmark** as if it were someone's own number. The example values in the source only make the build's maths checks run. They are not shown on the page.
9. **After any update, give Adi the clickable, cache-busted link** (for example `https://revops-funnel-equations.growthcluborg.workers.dev/?v=<something>`), near the top of the reply, even if the URL did not change. Missing this is a "complete no-no".
10. **Verify visually before handing over**, at desktop (about 1280px) and phone (390px) widths. An HTTP 200 is not proof.

## What Was Already Rejected (Do Not Repeat)

- **v1:** probability unions, exponents, Greek symbols and a 252-KPI catalog. Rejected as not simple enough, with variables not explained.
- **v2:** 91 big "cards" with coloured blocks, worked examples, pictures, ranges and sources. Rejected as AI slop.
- **v2 compact:** a list of 91 equations with "from #19" links. Rejected because of the jump links, and because it had no one-metric-per-stage structure.
- **v3:** one metric per stage, but short forms with subscripts (Nₐ, VRₑ). Rejected: use plain initials.
- **Current v4:** one metric per stage, plain initials, definitions under each stage. This is the base to edit.

## Files

| File | What it holds | Edit it? |
|---|---|---|
| `src/eqstages.py` | Every variable: `v(id, "definition", example value)`. Every equation line: `ln(result, "expr", funnels, stage)`, in calculation order. `SHOWN`: which lines each stage displays, and its metric. `WHOLE`: the whole-funnel line per shape. | Yes, for maths and definitions |
| `src/eqnames.py` | `id -> (Full Name, SHORT)` for every variable | Yes, for names and short forms |
| `src/equations.py` | The renderer. `render_standalone()` builds the page, including the sign-up form; `stage_block()`, `whole_block()`, `key_line()` and `meaning()` lay out each stage and key. It also renders the private repo's playbook, centres and agent pack, which is why it has more than this page needs. | Only for layout |
| `src/base-style.html` | The page stylesheet (copied from the workshop playbook) | Rarely |
| `build.py` | Checks every rule it can (operators, short forms, uniqueness, six stages, whole-funnel equals chain, no dashes, no jump links, no client names), then writes `index.html` | No |
| `index.html` | Generated output | Never by hand |

Ids in `expr` are lowercase internal ids (for example `dr_e`). Readers only ever see the short forms from `eqnames.py`.

## How to Make a Change

1. Edit `src/eqstages.py` and/or `src/eqnames.py`.
2. Run `python3 build.py`. Fix anything it reports as `FAIL`.
3. Preview with `python3 -m http.server 8000`, then open `http://localhost:8000/?v=1` at desktop and phone widths. Read every stage you touched.
4. Fork the repo, push your branch to your fork and open a pull request against `main`. The repo is public, so anyone can do this; nobody needs to be added as a collaborator.
5. Tell Adi's integrator the pull request is ready. They merge it, then:
   - redeploy the Cloudflare page (a static Worker deployed from its own isolated folder holding only `index.html`, never from the monorepo's `cloud/` folder);
   - port the change into the private monorepo.
   Merging alone publishes nothing: the live page changes only when the integrator redeploys.
6. Once it is live, confirm the page shows the change (`curl` the URL and grep for your new text), then send Adi the link with a fresh `?v=` and a two-line summary of what changed.

## The Private Monorepo (For the Integrator)

The same three source files also live in the private repo `adisuja/3-day-tantra-ai-revops-workshop`, under `workshop-plan/build/` on branch `r5/EQ`. That copy drives:
- the playbook's "The Funnel Equations" chapter and "The One Equation to Memorize" section;
- the Day 2 "Metric for This Stage" boxes;
- the Day 3 interactive model;
- both onboarding centres;
- the agent pack's `equations/run.mjs`.

To port a change:
1. Copy `src/eqstages.py`, `src/eqnames.py` and `src/equations.py` into `workshop-plan/build/`.
2. From the repo root, run:
   - `python3 workshop-plan/build/equations.py`
   - `python3 workshop-plan/build/test_equations.py`
   - `python3 workshop-plan/build/titlecase.py`
   - `python3 workshop-plan/build/embed.py`
   - `cp workshop-plan/playbook.html app/public/materials/playbook.html`
3. Then run the playbook probe.

`r5/EQ` is not yet merged into `onboarding-v2`.

## Open Items

- Merge `r5/EQ` into `onboarding-v2` and deploy the centre: integrator.
- The receiver could take the lead magnet as its own form name instead of a tagged registration row. That needs a new version of the receiver, published from Adi's Google account.
