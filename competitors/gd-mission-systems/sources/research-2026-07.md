# Research notes — General Dynamics Mission Systems (gd-mission-systems)

Drafted: 2026-07-17. Collection method: public web search plus page fetches
through the sandbox proxy. All access dates are 2026-07-17.

## Collection constraints (record of what could not be verified directly)

- Direct fetches of gdmissionsystems.com, gd.com, wikipedia.org, gao.gov,
  sec.gov, stocktitan.net, and investing.com returned HTTP 403 through the
  session proxy. Facts from those domains were taken from search-result
  summaries and titles actually seen in this session, and every URL below was
  seen in those results. Flag for the human reviewer: spot-check S3, S4, S13,
  S16, S25 against the live pages.
- api.usaspending.gov was blocked by the egress policy (CONNECT 403), so no
  FPDS/USAspending obligation totals or top-customer breakdown was pulled.
  Gap: quantify GDMS prime obligations by agency before promoting the card.
- SAM.gov presence (UEIs, registrations) not checked this session.
- GAO docket search: only one GDMS-named decision surfaced (B-416181, 2018,
  denied). Full protest docket review not performed.

## Sources (mirrors the card's Sources section)

1. GDMS official site (homepage/company description; TACLANE and comms
   product references) — https://gdmissionsystems.com/ — accessed 2026-07-17
   (via search results; direct fetch 403).
2. Wikipedia, "General Dynamics Mission Systems" — formed January 2015 from
   GD C4 Systems + GD Advanced Information Systems —
   https://en.wikipedia.org/wiki/General_Dynamics_Mission_Systems — accessed
   2026-07-17 (via search results).
3. GD FY2025 Form 10-K — Technologies segment: revenue $13.47B, operating
   earnings $1.28B, margin 9.5%, ~40,000 employees; two units (GDIT, Mission
   Systems); GDIT grew faster than Mission Systems (mix/margin note); units
   share customer base and go to market together when appropriate —
   https://www.sec.gov/Archives/edgar/data/40533/000004053326000006/gd-20251231.htm
   — accessed 2026-07-17 (via search results).
4. GD Q4/FY2025 results release (2026-01-28) — FY2025 company revenue $52.6B;
   Technologies Q4 revenue $3.24B; FY backlog $16.7B; 1.2x book-to-bill at
   both GDIT and Mission Systems —
   https://www.gd.com/Articles/2026/01/28/general-dynamics-reports-fourth-quarter-and-full-year-2025-financial-results
   — accessed 2026-07-17 (via search results).
5. GD Q1 2026 earnings transcript (Motley Fool, 2026-04-29) and StockTitan
   8-K summary — Technologies $3.6B (+4.2%); Mission Systems +11.7%; C5ISR
   +$125M driven by space portfolio and international; margin 9.5%; backlog
   $17.7B (+23% YoY); book-to-bill 1.3x —
   https://www.fool.com/earnings/call-transcripts/2026/04/29/general-dynamics-gd-q1-2026-earnings-transcript/
   and
   https://www.stocktitan.net/sec-filings/GD/8-k-general-dynamics-corp-reports-material-event-8f0af9542188.html
   — accessed 2026-07-17 (via search results).
6. PRNewswire — GDMS awarded $491.6M SDA Ground, Management and Integration
   (GMI) design and development contract (announced September 2024) —
   https://www.prnewswire.com/news-releases/general-dynamics-mission-systems-awarded-491-6-million-design-and-development-contract-for-space-development-agencys-ground-management-and-integration-program-302238594.html
   — accessed 2026-07-17.
7. SDA.mil — Tranche 1 Operations & Integration award announcement,
   $324,516,613; ops centers at Grand Forks AFB; base period May 2022 to
   January 2025 with options to September 2029 —
   https://www.sda.mil/sda-announces-award-for-tranche-1-operations-integration/
   — accessed 2026-07-17.
8. GD release (2022-05-26) — GDMS and Iridium awarded SDA ground control and
   operations contract —
   https://www.gd.com/Articles/2022/05/26/general-dynamics-mission-systems-and-iridium-awarded-ground-control-and-operations-contract
   — accessed 2026-07-17 (via search results).
9. GDMS news release (2025-10-06) and Army.mil article — initial CMFF
   (CMOSS Mounted Form Factor) prototype award; PEO C3N PM Mission Command
   via C5 Consortium OTA; two-year effort; chassis, CMOSS management
   software, modeling, integration services —
   https://gdmissionsystems.com/articles/2025/10/06/news-release-us-army-awards-general-dynamics-contract-to-deliver-initial-cmff-prototype-systems
   and
   https://www.army.mil/article/288717/cmoss_mounted_form_factor_award_initiates_rapid_prototype_development
   — accessed 2026-07-17 (via search results).
10. CMFF award value $28.3M — GDMS post on X (2025-10-06, dateline
    Chantilly, Va.) and Aeromag Asia coverage —
    https://x.com/GDMS/status/1975204678527828252 and
    https://www.aeromagasia.com/news/land-systems/general-dynamics-secures-283-mn-us-army-contract-for-cmoss-cmff-prototypes
    — accessed 2026-07-17 (via search results).
11. PRNewswire (2022-02-07) — NGLD-M: $229M Army contract, NSA-certified key
    loader, 10-year PoP, planned 265,000 units —
    https://www.prnewswire.com/news-releases/general-dynamics-mission-systems-awarded-229-million-us-army-contract-to-build-next-generation-cryptographic-key-loader-301476911.html
    — accessed 2026-07-17.
12. GD release (2019-11-27) and C4ISRNET (2019-12-02) — MUOS ground system
    sustainment, $731.8M, 10-year, sole-source IDIQ —
    https://www.gd.com/Articles/2019/11/27/gd-receives-10-year-sustainment-contract-for-next-generation-satellite-communications-system
    and
    https://www.c4isrnet.com/battlefield-tech/c2-comms/2019/12/02/navy-awards-732m-contract-for-satellite-ground-systems/
    — accessed 2026-07-17 (via search results).
13. GD FY2024 Form 10-K — MUOS sustainment for US Space Force, maximum
    potential value $2.2B —
    https://www.sec.gov/Archives/edgar/data/40533/000004053325000008/gd-20241231.htm
    — accessed 2026-07-17 (via search results).
14. GovCon Wire — GDMS $106M MUOS ground segment sustainment task order from
    Space Systems Command; base and options $294.9M; work possibly through
    May 2031; obligations cited FY2025 procurement and FY2026 O&M funds
    (award therefore late 2025/early 2026) —
    https://www.govconwire.com/articles/gdms-muos-sustainment-task-order —
    accessed 2026-07-17 (via search results).
15. GDIT press release — SACSS, $988M, Navy C5ISR systems support; awarded
    December 2025, announced 2026-01-12; one-year base, four one-year
    options, six-month option; integration, engineering, procurement,
    logistics, installation across surface combatants, carriers, Coast Guard
    vessels, aircraft, shore stations —
    https://www.gdit.com/about-gdit/press-releases/gdit-awarded-usd988-million-contract-to-modernize-navy-c5isr-systems/
    — accessed 2026-07-17 (via search results).
16. GAO decision page B-416181 — GDMS protest of Army DCGS-A Capability Drop
    1 awards to Raytheon and Palantir (awards 2018-03-08); protest denied —
    https://www.gao.gov/products/b-416181 — accessed 2026-07-17 (via search
    results; gao.gov direct fetch 403 this session).
17. GDMS leadership page (Chris Brady, president since 2019-01-01) and
    Wash100 2026 coverage (sixth Wash100 award) —
    https://gdmissionsystems.com/about-us/leadership-team/chris-brady and
    https://www.wash100.com/blog/chris-brady-gdms-accepts-2026-wash100/ —
    accessed 2026-07-17 (via search results).
18. WashingtonExec (Jan 2026) — Chris Jaeger appointed VP of cross business
    and strategic initiatives, effective 2026-01-05; 30+ years CIA/State/Army
    — https://washingtonexec.com/2026/01/general-dynamics-mission-systems-appoints-chris-jaeger-as-vp-of-cross-business-strategic-initiatives/
    — accessed 2026-07-17 (via search results).
19. GovCon Wire — Ron Moore named GDMS VP of IT and CIO (effective January
    2026; GDMS featured story dated 2026-02-02); same executive-move search
    coverage reported Brendan Grant named VP of space systems (October 2025,
    16-year company veteran) —
    https://www.govconwire.com/articles/ron-moore-gdms-cio-it-vp and
    https://gdmissionsystems.com/articles/2026/02/02/featured-story-general-dynamics-mission-systems-announces-ron-moore-as-cio
    — accessed 2026-07-17 (via search results).
20. ExecutiveBiz — GDMS/Progeny Systems $66M Navy DARTS contract —
    https://www.executivebiz.com/articles/gdms-progeny-systems-navy-darts —
    accessed 2026-07-17 (via search results).
21. GovCon Wire — Progeny Systems (GDMS business, Manassas, VA) $121M Navy
    submarine software development services contract —
    https://www.govconwire.com/articles/gdms-business-progeny-systems-secures-121m-navy-contract-for-submarine-software-development-services
    — accessed 2026-07-17 (via search results).
22. Defence Industry Europe and GDMS release (2025-10-08) — $18.2M AUKUS
    contract, submarine weapon launch and weapon simulation systems (US, UK,
    Australia) —
    https://defence-industry.eu/general-dynamics-mission-systems-wins-18-2-million-aukus-contract-for-submarine-weapon-and-simulation-systems/
    and
    https://gdmissionsystems.com/articles/2025/10/08/news-release-general-dynamics-to-provide-submarine-weapon-launch-weapon-simulation-capabilities
    — accessed 2026-07-17 (via search results).
23. WashingtonExec (Sept 2025) — $15.3M Navy contract, security toolkit
    shipsets for submarines and carriers; cumulative $91M with options to
    August 2030 —
    https://washingtonexec.com/2025/09/general-dynamics-mission-systems-wins-15-3m-navy-contract-to-support-submarines-aircraft-carriers/
    — accessed 2026-07-17 (via search results).
24. Defense Daily contract-award notice and DoD contracts list (2025-12-23)
    — GDMS (Scottsdale, AZ) $39,307,155 modification, PWSA ground
    management, SDA contracting activity —
    https://www.defensedaily.com/contract-awards/contract-award-general-dynamics-mission-systems-inc-scottsdale-arizona-39307155/
    and https://www.war.gov/News/Contracts/Contract/Article/4367503/ —
    accessed 2026-07-17 (via search results).
25. GD Q4/FY2024 results (2025-01-29) and 2024 Annual Report PDF — slight
    revenue decline at Mission Systems amid transition from legacy work to
    new growth lines; Technologies FY2024 revenue $12.9B (+3.4%), operating
    earnings down ~2% —
    https://www.gd.com/Articles/2025/01/29/general-dynamics-reports-fourth-quarter-and-full-year-2024-financial-results
    and
    https://s22.q4cdn.com/891946778/files/doc_financials/2024/ar/2024-Annual-Report-General-Dynamics-Corporation.pdf
    — accessed 2026-07-17 (via search results).
26. Cummings Research Park tenant listing (GDMS, 6000 Technology Drive NW,
    Huntsville, AL) and Manta directory listing (est. 100-249 employees at
    that location; directory estimates are low-confidence) —
    https://cummingsresearchpark.com/tenant/general-dynamics-mission-systems/
    and https://www.manta.com/c/mmf5hzs/general-dynamics-mission-systems-inc
    — accessed 2026-07-17 (via search results).
27. GDMS Strategic Weapon Deterrence page — 70-year heritage, ICBM/SLBM
    guidance, weapon command and control, communications —
    https://gdmissionsystems.com/en/command-and-control/strategic-weapon-deterrence
    — accessed 2026-07-17 (via search results).
28. Potomac Officers Club profile (Chris Brady/GDMS) and ZoomInfo company
    profile — ~12,000 employees, 80+ facilities; HQ listed at 12450 Fair
    Lakes Cir, Fairfax, VA (recent GDMS releases dateline Chantilly, Va.) —
    https://www.potomacofficersclub.com/chris-brady-president-of-general-dynamics-mission-systems/
    and https://www.zoominfo.com/c/general-dynamics-mission-systems-inc/80431222
    — accessed 2026-07-17 (via search results).
29. GD release (2018-12-17) — Navy awards General Dynamics SeaPort-NxG
    contract (held via GDIT) —
    https://www.gd.com/en/Articles/2018/12/17/navy-awards-general-dynamics-seaport-nxg-contract
    — accessed 2026-07-17 (via search results).

## Taxonomy notes

- Needed but missing from config/taxonomy.yaml (not added per instructions):
  an agency value for the Space Development Agency ("sda"), an agency value
  for Army PEO C3N/C3T, and a vehicle value for OTA consortium awards
  (CMFF ran through the C5 Consortium OTA).
- vehicles tag "seaport-nxg" reflects the GD family holding via GDIT (S29);
  GDMS's typical capture route is directed/agency IDIQs and OTAs.
