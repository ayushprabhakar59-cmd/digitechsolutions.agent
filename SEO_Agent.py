#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║      SEO & Digital Marketing AI Agent — Powered by Groq          ║
║                     Built for: eLensAI                           ║
╚══════════════════════════════════════════════════════════════════╝

HOW TO SET YOUR GROQ API KEY:
  Option A — Environment variable (recommended):
     export GROQ_API_KEY="gsk_..."          (Mac/Linux)
     set GROQ_API_KEY=gsk_...               (Windows CMD)

  Option B — Paste directly below (replace YOUR_API_KEY_HERE)

  Get / regenerate your key at: https://console.groq.com/keys

INSTALL DEPENDENCIES:
  pip install groq colorama tabulate

RUN:
  python seo_agent.py
"""

import os
import sys
import time
from datetime import datetime

# ─────────────────────── CONFIGURATION ───────────────────────────
GROQ_API_KEY = "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"
GROQ_MODEL   = "openai/gpt-oss-120b"   # Fast, powerful, large context
# ──────────────────────────────────────────────────────────────────

try:
    from groq import Groq
except ImportError:
    print("\n❌  Missing dependency. Run:  pip install groq")
    sys.exit(1)

try:
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
    COLOR = True
except ImportError:
    COLOR = False
    class _Dummy:
        def __getattr__(self, _): return ""
    Fore = Back = Style = _Dummy()

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False


# ─────────────────────────── HELPERS ──────────────────────────────

def banner():
    print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗
║  {Fore.YELLOW}🤖  SEO & Digital Marketing AI Agent  {Fore.CYAN}                         ║
║  {Fore.GREEN}Powered by Groq ({GROQ_MODEL}) · eLensAI{Fore.CYAN}         ║
╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
""")

def section(title: str):
    width = 65
    print(f"\n{Fore.CYAN}{'═' * width}")
    print(f"  {Fore.YELLOW}{title}")
    print(f"{Fore.CYAN}{'═' * width}{Style.RESET_ALL}")

def ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    val = input(f"{Fore.GREEN}  ▶  {prompt}{suffix}: {Style.RESET_ALL}").strip()
    return val if val else default

def print_result(result: str):
    print(f"\n{Fore.WHITE}")
    for line in result.split("\n"):
        if line.startswith("##"):
            print(f"{Fore.YELLOW}{line}{Style.RESET_ALL}")
        elif line.startswith("#"):
            print(f"{Fore.CYAN}{line}{Style.RESET_ALL}")
        elif line.startswith("**") or line.startswith("- **"):
            print(f"{Fore.GREEN}{line}{Style.RESET_ALL}")
        else:
            print(line)
    print(Style.RESET_ALL)

def save_report(title: str, content: str):
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = f"report_{title.lower().replace(' ','_')}_{ts}.txt"
    with open(name, "w", encoding="utf-8") as f:
        f.write(f"SEO & Digital Marketing AI Agent — eLensAI\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Model: {GROQ_MODEL}\n")
        f.write(f"Task: {title}\n")
        f.write("=" * 70 + "\n\n")
        f.write(content)
    print(f"\n{Fore.GREEN}  ✅  Report saved → {name}{Style.RESET_ALL}")
    return name


# ─────────────────────── MAIN AGENT CLASS ─────────────────────────

class SEOAgent:
    """Full-stack SEO & Digital Marketing AI Employee — powered by Groq."""

    def __init__(self, api_key: str):
        if api_key == "YOUR_API_KEY_HERE" or not api_key:
            print(f"\n{Fore.RED}  ❌  No API key detected!")
            print(f"  Get/regenerate yours at: https://console.groq.com/keys")
            print(f"  Set env var:  export GROQ_API_KEY='gsk_...'  {Style.RESET_ALL}\n")
            sys.exit(1)
        self.client = Groq(api_key=api_key)
        self.model  = GROQ_MODEL

    def _call(self, system: str, user: str, max_tokens: int = 8192) -> str:
        """Send a message to Groq and return the text response."""
        resp = self.client.chat.completions.create(
            model      = self.model,
            max_tokens = max_tokens,
            messages   = [
                {"role": "system", "content": system},
                {"role": "user",   "content": user}
            ]
        )
        return resp.choices[0].message.content

    # ── 1. KEYWORD RESEARCH ──────────────────────────────────────
    def keyword_research(self):
        section("🔍  Keyword Research & Analysis")
        topic    = ask("Topic / Product / Service")
        niche    = ask("Niche / Industry")
        audience = ask("Target Audience")
        region   = ask("Target Region / Country", "Global")
        lang     = ask("Language", "English")

        system = (
            "You are a world-class SEO keyword research specialist with 15+ years of experience. "
            "You provide data-driven, actionable keyword strategies used by Fortune 500 brands."
        )
        user = f"""Perform a comprehensive keyword research report for:
- Topic/Product/Service: {topic}
- Niche/Industry: {niche}
- Target Audience: {audience}
- Target Region: {region}
- Language: {lang}
- Date: {datetime.now().strftime('%B %Y')}

Deliver a full professional keyword research report with these sections:

## 1. PRIMARY KEYWORDS (15 keywords)
For each: Keyword | Search Intent | Volume Tier (High/Med/Low) | Difficulty | CPC Estimate | Priority

## 2. LONG-TAIL KEYWORDS (20 keywords)
For each: Keyword | Why it converts | Difficulty

## 3. LSI & SEMANTIC KEYWORDS (15 terms)

## 4. QUESTION-BASED KEYWORDS (10 questions for featured snippets)

## 5. NEGATIVE KEYWORDS TO AVOID

## 6. COMPETITOR KEYWORD GAPS

## 7. KEYWORD CLUSTERS & CONTENT PILLARS

## 8. 90-DAY ACTION PLAN

Be specific, professional, and actionable."""

        print(f"\n{Fore.CYAN}  ⏳  Groq is researching keywords…{Style.RESET_ALL}")
        result = self._call(system, user)
        print_result(result)
        if ask("Save report? (y/n)", "y").lower() == "y":
            save_report("keyword_research", result)
        return result

    # ── 2. CONTENT CREATION ──────────────────────────────────────
    def content_creation(self):
        section("✍️   Content Creation & Optimization")
        print(f"\n{Fore.YELLOW}  Choose content type:{Style.RESET_ALL}")
        types = {
            "1": "SEO Blog Post (1500–2000 words)",
            "2": "Meta Title & Description",
            "3": "Product/Service Page Copy",
            "4": "Landing Page Copy",
            "5": "FAQ Section",
            "6": "Press Release",
            "7": "Email Newsletter",
            "8": "YouTube Video Script",
            "9": "LinkedIn Article"
        }
        for k, v in types.items():
            print(f"  {k}. {v}")
        choice  = ask("Select (1-9)", "1")
        ctype   = types.get(choice, "SEO Blog Post")
        keyword = ask("Primary Target Keyword")
        topic   = ask("Content Topic / Title Idea")
        brand   = ask("Brand/Company Name", "eLensAI")
        tone    = ask("Brand Voice / Tone", "Professional, helpful, trustworthy")
        extras  = ask("Special instructions (optional)", "None")

        system = (
            "You are an elite SEO content strategist and copywriter. "
            "You create content that ranks on page 1 of Google AND converts readers into customers. "
            "Your writing is engaging, E-E-A-T compliant, and search-intent aligned."
        )
        user = f"""Create professional SEO-optimized content:

Content Type: {ctype}
Primary Keyword: {keyword}
Topic: {topic}
Brand: {brand}
Tone: {tone}
Special Instructions: {extras}
Date: {datetime.now().strftime('%B %Y')}

Requirements:
- Naturally integrate the primary keyword (density: 1–2%)
- Include semantic keywords and LSI terms
- Write compelling, human-like prose (not robotic)
- Optimize for featured snippets where applicable
- Include internal linking suggestions [bracketed]
- Add CTA recommendations
- Include a meta title (≤60 chars) and meta description (≤160 chars)
- Provide a Yoast SEO-style checklist at the end

Deliver complete, publish-ready content."""

        print(f"\n{Fore.CYAN}  ⏳  Groq is writing your content…{Style.RESET_ALL}")
        result = self._call(system, user)
        print_result(result)
        if ask("Save report? (y/n)", "y").lower() == "y":
            save_report("content_creation", result)
        return result

    # ── 3. SOCIAL MEDIA ──────────────────────────────────────────
    def social_media(self):
        section("📱  Social Media Marketing")
        print(f"\n{Fore.YELLOW}  Choose task:{Style.RESET_ALL}")
        tasks = {
            "1": "Full Content Calendar (30 days)",
            "2": "Platform-Specific Posts (10 posts)",
            "3": "Hashtag Strategy",
            "4": "Viral Content Ideas (20 ideas)",
            "5": "Bio & Profile Optimization",
            "6": "Paid Social Ad Copy",
            "7": "Influencer Outreach Templates"
        }
        for k, v in tasks.items():
            print(f"  {k}. {v}")
        choice   = ask("Select (1-7)", "1")
        task     = tasks.get(choice, tasks["1"])
        brand    = ask("Brand / Product Name", "eLensAI")
        industry = ask("Industry / Niche")
        audience = ask("Target Audience")
        goals    = ask("Marketing Goals", "Brand awareness, lead generation")
        platforms = ask("Platforms", "Instagram, LinkedIn, Twitter, Facebook")
        tone     = ask("Brand Voice", "Professional yet engaging")

        system = (
            "You are a top-tier social media strategist who has grown brands to millions of followers. "
            "You understand platform algorithms, viral content mechanics, and conversion-focused social marketing."
        )
        user = f"""Create a professional social media marketing plan:

Task: {task}
Brand: {brand}
Industry: {industry}
Target Audience: {audience}
Goals: {goals}
Platforms: {platforms}
Brand Voice: {tone}
Date: {datetime.now().strftime('%B %Y')}

## PLATFORM-BY-PLATFORM STRATEGY
## CONTENT TYPES MIX (% breakdown)
## POSTING SCHEDULE (best times per platform)
## 30-DAY CONTENT CALENDAR (Date | Platform | Type | Caption | Hashtags | CTA | Visual)
## HASHTAG STRATEGY (primary, secondary, niche per platform)
## ENGAGEMENT TACTICS
## KPIs TO TRACK

Make every caption ready to copy-paste."""

        print(f"\n{Fore.CYAN}  ⏳  Groq is building your social strategy…{Style.RESET_ALL}")
        result = self._call(system, user)
        print_result(result)
        if ask("Save report? (y/n)", "y").lower() == "y":
            save_report("social_media", result)
        return result

    # ── 4. SEO AUDIT ─────────────────────────────────────────────
    def seo_audit(self):
        section("🔬  SEO Audit & Technical Analysis")
        website  = ask("Website URL", "https://yourwebsite.com")
        biztype  = ask("Business Type / Industry")
        goals    = ask("SEO Goals", "Increase organic traffic and rankings")
        issues   = ask("Known issues (optional)", "None")

        system = (
            "You are a senior technical SEO consultant who has audited thousands of websites. "
            "You provide precise, prioritized recommendations that drive measurable results."
        )
        user = f"""Perform a comprehensive SEO audit for:

Website: {website}
Business Type: {biztype}
Goals: {goals}
Known Issues: {issues}
Date: {datetime.now().strftime('%B %Y')}

## 1. TECHNICAL SEO CHECKLIST (✅/⚠️/❌ for each item)
Core Web Vitals | Site Speed | Mobile-First | Crawlability | Indexation | HTTPS | XML Sitemap | Robots.txt | Structured Data | Canonical Tags | JavaScript SEO

## 2. ON-PAGE SEO AUDIT
Title Tags | Meta Descriptions | H1-H6 | Keyword Optimization | Content Quality | Image Alt | Internal Linking | URL Structure

## 3. OFF-PAGE SEO AUDIT
Backlink Health | Domain Authority | Link Building Opportunities

## 4. CONTENT AUDIT FRAMEWORK

## 5. PRIORITY ACTION PLAN
🔴 Critical (1 week) | 🟡 Important (1 month) | 🟢 Improvements (3 months)

## 6. 90-DAY SEO ROADMAP

## 7. TRACKING & REPORTING SETUP"""

        print(f"\n{Fore.CYAN}  ⏳  Groq is auditing your SEO…{Style.RESET_ALL}")
        result = self._call(system, user)
        print_result(result)
        if ask("Save report? (y/n)", "y").lower() == "y":
            save_report("seo_audit", result)
        return result

    # ── 5. LATEST TRENDS ─────────────────────────────────────────
    def latest_trends(self):
        section("📈  Latest SEO & Digital Marketing Trends")
        area = ask("Focus area (SEO/PPC/Social/Email/AI/All)", "All")

        system = (
            "You are a leading digital marketing industry analyst who tracks every major update, "
            "algorithm change, and emerging trend. You provide forward-looking strategic intelligence."
        )
        user = f"""Provide a comprehensive {datetime.now().strftime('%B %Y')} industry intelligence report:

Focus Area: {area}

## 1. GOOGLE ALGORITHM UPDATES (Last 6 months)
## 2. TOP SEO TRENDS RIGHT NOW (AI content, SGE, E-E-A-T, Core Web Vitals, etc.)
## 3. DIGITAL MARKETING TRENDS (AI, first-party data, privacy, short-form video)
## 4. PLATFORM UPDATES (Google, Meta, LinkedIn, Instagram, TikTok, YouTube)
## 5. EMERGING OPPORTUNITIES
## 6. WHAT TO STOP DOING (outdated tactics)
## 7. TOOLS & TECHNOLOGIES TO ADOPT
## 8. STRATEGIC RECOMMENDATIONS (30/60/90-day actions)

Be specific and actionable."""

        print(f"\n{Fore.CYAN}  ⏳  Groq is analyzing latest trends…{Style.RESET_ALL}")
        result = self._call(system, user)
        print_result(result)
        if ask("Save report? (y/n)", "y").lower() == "y":
            save_report("latest_trends", result)
        return result

    # ── 6. EMAIL MARKETING ────────────────────────────────────────
    def email_marketing(self):
        section("📧  Email Marketing")
        brand    = ask("Brand / Company Name", "eLensAI")
        goal     = ask("Email Goal", "Nurture leads and drive conversions")
        audience = ask("Audience Segment")
        etype    = ask("Email Type (newsletter/promo/drip/welcome/cart/re-engagement)", "newsletter")
        product  = ask("Product / Service being promoted")
        offer    = ask("Offer / CTA", "Not specified")

        system = (
            "You are a direct-response email marketing expert with a track record of 40%+ open rates. "
            "You write compelling, personalized emails that get opened, read, and acted upon."
        )
        user = f"""Create a complete email marketing campaign:

Brand: {brand}
Email Type: {etype}
Goal: {goal}
Audience: {audience}
Product/Service: {product}
Offer/CTA: {offer}
Date: {datetime.now().strftime('%B %Y')}

## SUBJECT LINE OPTIONS (10 variations with predicted open rate tier)
## PREVIEW TEXT (5 options)
## EMAIL BODY — 3 FULL VERSIONS
  Version A: Short & punchy (150–200 words)
  Version B: Story-driven (300–400 words)
  Version C: Value-packed (500–600 words)
  Each includes: personalization hooks, value prop, social proof, CTA, P.S. line
## A/B TESTING PLAN
## DELIVERABILITY CHECKLIST
## FOLLOW-UP SEQUENCE (3 emails)"""

        print(f"\n{Fore.CYAN}  ⏳  Groq is crafting your email campaign…{Style.RESET_ALL}")
        result = self._call(system, user)
        print_result(result)
        if ask("Save report? (y/n)", "y").lower() == "y":
            save_report("email_marketing", result)
        return result

    # ── 7. COMPETITOR ANALYSIS ────────────────────────────────────
    def competitor_analysis(self):
        section("🕵️   Competitor Analysis")
        your_brand  = ask("Your Brand / Website", "eLensAI")
        competitors = ask("Competitor websites (comma separated)")
        industry    = ask("Industry / Niche")
        focus       = ask("Focus (SEO/Content/Social/PPC/All)", "All")
        usp         = ask("Your USP / Differentiator", "Not specified")

        system = (
            "You are a competitive intelligence expert specializing in digital marketing. "
            "You provide actionable insights that help brands outmaneuver their competition."
        )
        user = f"""Perform a comprehensive competitor analysis:

My Brand: {your_brand}
Competitors: {competitors}
Industry: {industry}
Focus: {focus}
My USP: {usp}
Date: {datetime.now().strftime('%B %Y')}

## 1. SEO COMPARISON FRAMEWORK
## 2. CONTENT STRATEGY ANALYSIS
## 3. SOCIAL MEDIA PRESENCE
## 4. PAID ADVERTISING INTELLIGENCE
## 5. KEYWORD GAP ANALYSIS (ranked by opportunity)
## 6. BACKLINK OPPORTUNITIES
## 7. THEIR WEAKNESSES & GAPS TO EXPLOIT
## 8. DIFFERENTIATION STRATEGY
## 9. BATTLE PLAN (prioritized actions to outrank & outperform)"""

        print(f"\n{Fore.CYAN}  ⏳  Groq is analyzing competitors…{Style.RESET_ALL}")
        result = self._call(system, user)
        print_result(result)
        if ask("Save report? (y/n)", "y").lower() == "y":
            save_report("competitor_analysis", result)
        return result

    # ── 8. LOCAL SEO ──────────────────────────────────────────────
    def local_seo(self):
        section("📍  Local SEO Strategy")
        bizname  = ask("Business Name", "eLensAI")
        location = ask("City / Location")
        category = ask("Business Category")
        radius   = ask("Service Radius", "25 km")
        customers = ask("Target Customers")

        system = (
            "You are a local SEO specialist who helps businesses dominate their local search market. "
            "You know the Google Business Profile algorithm, local pack ranking factors, and local link building."
        )
        user = f"""Create a comprehensive Local SEO strategy:

Business: {bizname}
Location: {location}
Category: {category}
Service Radius: {radius}
Target Customers: {customers}
Date: {datetime.now().strftime('%B %Y')}

## 1. GOOGLE BUSINESS PROFILE OPTIMIZATION (complete checklist)
## 2. LOCAL KEYWORD STRATEGY
## 3. LOCAL CONTENT STRATEGY
## 4. LOCAL LINK BUILDING
## 5. CITATION BUILDING (top 20 directories + NAP guide)
## 6. REVIEW MANAGEMENT (templates included)
## 7. LOCAL SCHEMA MARKUP (exact JSON-LD code)
## 8. LOCAL PACK RANKING FACTORS (prioritized)
## 9. 90-DAY LOCAL SEO PLAN (week by week)"""

        print(f"\n{Fore.CYAN}  ⏳  Groq is building your local SEO plan…{Style.RESET_ALL}")
        result = self._call(system, user)
        print_result(result)
        if ask("Save report? (y/n)", "y").lower() == "y":
            save_report("local_seo", result)
        return result

    # ── 9. PPC STRATEGY ───────────────────────────────────────────
    def ppc_strategy(self):
        section("💰  PPC & Paid Advertising Strategy")
        brand    = ask("Brand / Product", "eLensAI")
        platform = ask("Ad Platform (Google Ads/Meta/LinkedIn/TikTok)", "Google Ads")
        budget   = ask("Monthly Budget (USD)", "$1,000")
        goal     = ask("Campaign Goal", "Lead generation")
        product  = ask("Product / Service")
        audience = ask("Target Audience")

        system = (
            "You are a certified PPC expert who manages $10M+ in annual ad spend. "
            "You deliver campaigns that consistently hit 3–10x ROAS across platforms."
        )
        user = f"""Create a complete PPC campaign strategy:

Brand: {brand}
Platform: {platform}
Budget: {budget}/month
Goal: {goal}
Product/Service: {product}
Target Audience: {audience}
Date: {datetime.now().strftime('%B %Y')}

## 1. CAMPAIGN STRUCTURE (Campaign → Ad Group → Ad hierarchy with budget allocation)
## 2. TARGETING STRATEGY
## 3. KEYWORD STRATEGY (match types, negatives, search terms)
## 4. AD COPY (5 complete ads with all headlines, descriptions, extensions)
## 5. LANDING PAGE RECOMMENDATIONS
## 6. BIDDING STRATEGY
## 7. AUDIENCE SEGMENTS & RETARGETING FUNNEL
## 8. BUDGET ALLOCATION BY FUNNEL STAGE
## 9. KPIs: Target CPC | CTR | CVR | CPA | ROAS
## 10. OPTIMIZATION SCHEDULE (daily/weekly/monthly tasks)"""

        print(f"\n{Fore.CYAN}  ⏳  Groq is building your PPC strategy…{Style.RESET_ALL}")
        result = self._call(system, user)
        print_result(result)
        if ask("Save report? (y/n)", "y").lower() == "y":
            save_report("ppc_strategy", result)
        return result

    # ── 10. MONTHLY REPORT ────────────────────────────────────────
    def marketing_report(self):
        section("📊  Monthly Marketing Report")
        brand    = ask("Brand / Company", "eLensAI")
        month    = ask("Reporting Month", datetime.now().strftime("%B %Y"))
        metrics  = ask("Key metrics achieved (optional)", "Not specified")
        channels = ask("Active marketing channels", "SEO, Social Media, Email")
        goals    = ask("Original monthly goals", "Increase organic traffic and brand awareness")

        system = (
            "You are a digital marketing director who creates board-level marketing reports. "
            "Your reports are data-driven, visually structured, and strategically insightful."
        )
        user = f"""Generate a professional monthly digital marketing report:

Brand: {brand}
Month: {month}
Metrics: {metrics}
Channels: {channels}
Goals: {goals}

## EXECUTIVE SUMMARY
## PERFORMANCE DASHBOARD (Channel | Goal | Result | Status | Action)
## SEO PERFORMANCE
## SOCIAL MEDIA PERFORMANCE
## EMAIL MARKETING PERFORMANCE
## PAID ADVERTISING PERFORMANCE
## WINS THIS MONTH 🏆
## CHALLENGES & SOLUTIONS
## COMPETITOR ACTIVITY
## NEXT MONTH PLAN (Top 5 priorities)
## RECOMMENDATIONS FOR LEADERSHIP"""

        print(f"\n{Fore.CYAN}  ⏳  Groq is generating your report…{Style.RESET_ALL}")
        result = self._call(system, user)
        print_result(result)
        if ask("Save report? (y/n)", "y").lower() == "y":
            save_report("monthly_report", result)
        return result

    # ── 11. CUSTOM TASK ───────────────────────────────────────────
    def custom_task(self):
        section("🛠️   Custom Marketing Task")
        print(f"  {Fore.YELLOW}Describe any SEO or digital marketing task.{Style.RESET_ALL}")
        task = ask("Describe your task in detail")

        system = (
            "You are an expert digital marketing agency with specialists in SEO, content, social media, "
            "PPC, email marketing, analytics, and growth hacking. Deliver professional, actionable output."
        )
        print(f"\n{Fore.CYAN}  ⏳  Groq is working on your task…{Style.RESET_ALL}")
        result = self._call(system, task)
        print_result(result)
        if ask("Save report? (y/n)", "y").lower() == "y":
            save_report("custom_task", result)
        return result


# ────────────────────────── MAIN MENU ─────────────────────────────

MENU = {
    "1":  ("🔍  Keyword Research & Analysis",       "keyword_research"),
    "2":  ("✍️   Content Creation & Optimization",   "content_creation"),
    "3":  ("📱  Social Media Marketing",             "social_media"),
    "4":  ("🔬  SEO Audit & Technical Analysis",     "seo_audit"),
    "5":  ("📈  Latest Trends & Industry Updates",   "latest_trends"),
    "6":  ("📧  Email Marketing",                    "email_marketing"),
    "7":  ("🕵️   Competitor Analysis",               "competitor_analysis"),
    "8":  ("📍  Local SEO Strategy",                 "local_seo"),
    "9":  ("💰  PPC & Paid Advertising",             "ppc_strategy"),
    "10": ("📊  Monthly Marketing Report",           "marketing_report"),
    "11": ("🛠️   Custom Marketing Task",             "custom_task"),
    "0":  ("🚪  Exit",                               None),
}

def main():
    banner()
    agent = SEOAgent(GROQ_API_KEY)
    print(f"  {Fore.GREEN}✅  Connected to Groq ({GROQ_MODEL}){Style.RESET_ALL}")
    print(f"  {Fore.CYAN}Your AI Marketing Employee is ready 24/7.{Style.RESET_ALL}\n")

    while True:
        section("📋  Main Menu — What would you like to do?")
        for key, (label, _) in MENU.items():
            print(f"  {Fore.YELLOW}{key:>2}.{Style.RESET_ALL}  {label}")

        choice = ask("\nSelect a task").strip()

        if choice not in MENU:
            print(f"\n  {Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
            continue

        label, method_name = MENU[choice]

        if choice == "0":
            print(f"\n{Fore.CYAN}  👋  Goodbye! Your AI marketing employee is always here.{Style.RESET_ALL}\n")
            break

        try:
            getattr(agent, method_name)()
        except Exception as e:
            err = str(e)
            if "401" in err or "auth" in err.lower():
                print(f"\n{Fore.RED}  ❌  Invalid API key. Regenerate at: https://console.groq.com/keys{Style.RESET_ALL}")
            elif "429" in err or "rate" in err.lower():
                print(f"\n{Fore.RED}  ⚠️  Rate limit hit. Please wait a moment and try again.{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}  ❌  Error: {err}{Style.RESET_ALL}")

        input(f"\n{Fore.CYAN}  Press Enter to return to the main menu…{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
