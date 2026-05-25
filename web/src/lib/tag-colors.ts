/**
 * The 8 primary research topics, their human-readable names, colors, and the
 * keyword rules that map a paper's title to a topic.
 *
 * Topic palette: 8 distinct hues, each rendered as a solid pill on cards or
 * an outlined chip in the filter row.
 */
export type TopicColor = { bg: string; fg: string };

export type Topic =
  | "online-harm"
  | "user-behavior"
  | "news-journalism"
  | "beliefs-opinions"
  | "llms-responsible-ai"
  | "bias-fairness"
  | "networks-influence"
  | "digital-health";

export const TOPICS: Topic[] = [
  "online-harm",
  "news-journalism",
  "user-behavior",
  "beliefs-opinions",
  "llms-responsible-ai",
  "bias-fairness",
  "networks-influence",
  "digital-health",
];

export const TOPIC_NAMES: Record<Topic, string> = {
  "online-harm":         "Online harm",
  "news-journalism":     "News & journalism",
  "user-behavior":       "User behavior & engagement",
  "beliefs-opinions":    "Beliefs & opinions",
  "llms-responsible-ai": "LLMs & responsible AI",
  "bias-fairness":       "Bias & fairness",
  "networks-influence":  "Networks & influence",
  "digital-health":      "Digital health",
};

// One-color-per-topic palette. Tailwind 600-level shades — distinct hues that
// work with white text. Picked so adjacent chips never blur into each other.
const COLORS: Record<Topic, TopicColor> = {
  "online-harm":         { bg: "#dc2626", fg: "white" }, // red — warning/danger
  "news-journalism":     { bg: "#57534e", fg: "white" }, // stone — sober/editorial
  "user-behavior":       { bg: "#d97706", fg: "white" }, // amber — warm/human
  "beliefs-opinions":    { bg: "#7c3aed", fg: "white" }, // violet — cognition/mind
  "llms-responsible-ai": { bg: "#4f46e5", fg: "white" }, // indigo — trust/ethics
  "bias-fairness":       { bg: "#0d9488", fg: "white" }, // teal — equity/balance
  "networks-influence":  { bg: "#0284c7", fg: "white" }, // sky — connections
  "digital-health":      { bg: "#db2777", fg: "white" }, // pink — care/wellbeing
};

const FALLBACK: TopicColor = { bg: "#71717a", fg: "white" };

export function topicColor(t: string): TopicColor {
  return (COLORS as Record<string, TopicColor>)[t] ?? FALLBACK;
}

export function topicName(t: string): string {
  return (TOPIC_NAMES as Record<string, string>)[t] ?? t;
}

/** Solid pill — used on cards. */
export function pillStyle(t: string): string {
  const c = topicColor(t);
  return `background-color:${c.bg};color:${c.fg};`;
}

/** Outlined chip — used in the filter row when inactive. */
export function chipStyle(t: string): string {
  const c = topicColor(t);
  return `border-color:${c.bg};color:${c.bg};`;
}

/** Filled chip — used in the filter row when active. */
export function chipActiveStyle(t: string): string {
  const c = topicColor(t);
  return `background-color:${c.bg};color:${c.fg};border-color:${c.bg};`;
}

// ─── Title-rule classification (used for uncurated 2024+ papers) ────────────

type Rule = { re: RegExp; topic: Topic };

const TITLE_RULES: Rule[] = [
  // Health-first so "anti-Asian hate during COVID" type titles route here
  // when health context dominates the framing.
  { re: /\b(mental health|depress|anxiet|suicid|psychiatr|psychological|wellbe|COVID-?19|public health|vaccin)/i,
    topic: "digital-health" },
  { re: /\b(toxic|toxicity|harass|hate|abuse|trolling|cyberbull)/i, topic: "online-harm" },
  { re: /\bmoderat/i,                                                topic: "online-harm" },
  { re: /\b(news|journalis|misinform|disinform|fake news|factualit|propaganda)/i,
    topic: "news-journalism" },
  // Bias / fairness covers media, data, demographic, and AI biases alike.
  { re: /\b(bias|biased|fair|fairness|stereo|stereotype|diversity|gender|racial|race|representation|disparit|equity)/i,
    topic: "bias-fairness" },
  { re: /\b(LLM|ChatGPT|GPT[- ]?\d|FlanT5|DeepSeek|language model|LLMs|alignment|prompt|jailbreak|hallucinat|safety)/i,
    topic: "llms-responsible-ai" },
  { re: /\b(annotator|annotation|judge|simulation|simulat|benchmark)/i,
    topic: "llms-responsible-ai" },
  { re: /\b(belief|opinion|polariz|stance|ideolog|moral|persuas)/i,
    topic: "beliefs-opinions" },
  { re: /\b(network|graph|diffus|centrality|topology|influencer|cascade|propagation)/i,
    topic: "networks-influence" },
  { re: /\b(engagement|attention|retention|click|view|recommend|game|esport|player|gaming|gamer)/i,
    topic: "user-behavior" },
];

/** Classify a paper by its title. Returns null if no rule matches. */
export function classifyTitle(title: string | null | undefined): Topic | null {
  if (!title) return null;
  for (const r of TITLE_RULES) {
    if (r.re.test(title)) return r.topic;
  }
  return null;
}

// ─── Methods (secondary axis: "how") ────────────────────────────────────────
//
// 0..N per paper. Rendered as small outlined chips. Each method gets its own
// muted color so a row of methods stays distinguishable but doesn't fight with
// the primary topic chip for attention.

export type Method =
  | "llm"
  | "nlp"
  | "networks"
  | "crowdsourced"
  | "user-study"
  | "dataset";

export const METHODS: Method[] = ["llm", "nlp", "networks", "crowdsourced", "user-study", "dataset"];

export const METHOD_NAMES: Record<Method, string> = {
  "llm":          "LLMs",
  "nlp":          "NLP",
  "networks":     "Networks",
  "crowdsourced": "Crowdsourced",
  "user-study":   "User study",
  "dataset":      "Dataset",
};

const METHOD_COLORS: Record<Method, string> = {
  "llm":          "#0d9488", // teal — matches AI vibe
  "nlp":          "#475569", // slate — text/NLP
  "networks":     "#0284c7", // sky — networks
  "crowdsourced": "#c2410c", // orange — human labor
  "user-study":   "#65a30d", // lime — empirical
  "dataset":      "#a16207", // mustard — resources
};

export function methodName(m: string): string {
  return (METHOD_NAMES as Record<string, string>)[m] ?? m;
}
export function methodColor(m: string): string {
  return (METHOD_COLORS as Record<string, string>)[m] ?? "#6b7280";
}
export function methodChipStyle(m: string): string {
  const c = methodColor(m);
  return `border-color:${c};color:${c};background-color:white;border-width:1px;border-style:solid;`;
}
export function methodChipActiveStyle(m: string): string {
  const c = methodColor(m);
  return `background-color:${c};color:white;border-color:${c};border-width:1px;border-style:solid;`;
}

// Methods detection rules. Multiple can match per paper.
const METHOD_RULES: { re: RegExp; method: Method }[] = [
  { re: /\b(LLM|LLMs|ChatGPT|GPT[- ]?\d|GPT-?[345]|FlanT5|DeepSeek|large language model|generative AI)/i, method: "llm" },
  { re: /\b(embedding|word2vec|BERT|transformer|tokeniz|sentiment|lexicon|topic model|stance detection|NLP|natural language)/i, method: "nlp" },
  { re: /\b(network|graph|topology|centrality|community detection|diffus|cascade|propagation|homophily|tie strength)/i, method: "networks" },
  { re: /\b(crowdsourc|mechanical turk|MTurk|AMT|annotat)/i, method: "crowdsourced" },
  { re: /\b(survey|focus group|user study|controlled experiment|A\/B test|interview|qualitative|eye-tracking|eye tracking|case study|empirical study)/i, method: "user-study" },
  { re: /\b(dataset|corpus|benchmark|collection)/i, method: "dataset" },
];

export function classifyMethods(text: string | null | undefined): Method[] {
  if (!text) return [];
  const found: Method[] = [];
  for (const r of METHOD_RULES) {
    if (r.re.test(text) && !found.includes(r.method)) found.push(r.method);
  }
  return found;
}

// ─── Platforms (secondary axis: "where") ────────────────────────────────────
//
// 0..N per paper. Rendered as tiny gray text-only pills — least visual weight.

export type Platform =
  | "twitter"
  | "reddit"
  | "youtube"
  | "facebook"
  | "instagram"
  | "tiktok"
  | "gab"
  | "news-media"
  | "multi-platform";

export const PLATFORMS: Platform[] = [
  "twitter", "reddit", "youtube", "facebook", "instagram",
  "tiktok", "gab", "news-media", "multi-platform",
];

export const PLATFORM_NAMES: Record<Platform, string> = {
  "twitter":        "Twitter/X",
  "reddit":         "Reddit",
  "youtube":        "YouTube",
  "facebook":       "Facebook",
  "instagram":      "Instagram",
  "tiktok":         "TikTok",
  "gab":            "Gab",
  "news-media":     "News media",
  "multi-platform": "Multi-platform",
};

export function platformName(p: string): string {
  return (PLATFORM_NAMES as Record<string, string>)[p] ?? p;
}

const PLATFORM_RULES: { re: RegExp; platform: Platform }[] = [
  { re: /\b(Twitter|tweet|hashtag|retweet|#\w+)/i, platform: "twitter" },
  { re: /\b(Reddit|subreddit|r\/\w+)/i,           platform: "reddit" },
  { re: /\bYouTube/i,                              platform: "youtube" },
  { re: /\bFacebook/i,                             platform: "facebook" },
  { re: /\bInstagram/i,                            platform: "instagram" },
  { re: /\bTikTok/i,                               platform: "tiktok" },
  { re: /\bGab\b/,                                 platform: "gab" },
];

export function classifyPlatforms(text: string | null | undefined): Platform[] {
  if (!text) return [];
  const found: Platform[] = [];
  for (const r of PLATFORM_RULES) {
    if (r.re.test(text) && !found.includes(r.platform)) found.push(r.platform);
  }
  // Heuristic: multiple specific platforms → also tag "multi-platform"
  if (found.length >= 2 && !found.includes("multi-platform")) {
    found.push("multi-platform");
  }
  // No specific platform but "social media" mentioned, or "news media"
  if (found.length === 0 && /\b(news media|news organization|news outlet)/i.test(text)) {
    found.push("news-media");
  }
  return found;
}

