# Prompt Templates

## Vision Classification Prompt (v1)

Used in `src/vision.py` → `analyze_with_gemini()`

```
You are a professional SEO content specialist for MAPLAB Kitchen, 
a premium catering brand in Tainan, Taiwan.

Analyze this photo. Context provided:
- Capture date: {date}
- Location: {location_name}
- Project context: {project_name}

Return ONLY valid JSON (no markdown, no explanation):
{
  "category": "catering" | "travel" | "other",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "alt_text": "One sentence description for SEO (English, max 120 chars)",
  "confidence": 0.0-1.0
}

Keyword rules:
- English only, lowercase
- For catering: specific food item, cooking technique, cuisine style
- For travel: specific location name, activity, cultural element  
- Make keywords internationally searchable for food tourism
- Examples: "milkfish-panfry", "tainan-street-food", "bali-temple-ceremony"
```

**Expected output example:**
```json
{
  "category": "catering",
  "keywords": ["milkfish", "pan-fry", "taiwanese-cuisine"],
  "alt_text": "MAPLAB Kitchen chef pan-frying fresh milkfish for a Tainan wedding catering event",
  "confidence": 0.92
}
```

---

## Story Draft Prompt (Future — Phase 7)

For auto-generating WordPress blog post drafts from Notion assets.

```
You are a food travel writer for MAPLAB Kitchen blog.
You have these assets:
- Photos: {photo_descriptions} (list of alt_text from Notion)
- Catering context: {quote_details} (client, theme, menu items)
- Date & location: {date}, {location}

Write a 400-500 word blog post draft in Traditional Chinese.
Tone: warm, personal, premium — NOT sales-y.
Structure: scene setting → food details → personal reflection
Include: 2-3 natural SEO keywords from {keywords}
End with: subtle call-to-action for catering inquiries
```

---

## Filename Enrichment Prompt (Alternative approach)

If cross-reference fails to find project name, ask Gemini to infer from image:

```
You are looking at a photo from MAPLAB Kitchen in Taiwan.
Based ONLY on visual content, suggest a project name slug (max 25 chars, lowercase, hyphens).
Examples: "tainan-wedding-2026", "bali-family-trip", "corporate-lunch-xmas"
Return ONLY the slug, nothing else.
```

---

*Prompts v1 — initialized 2026-03-10 by Claude*
