# Multilingual architecture guardrail

Experimental Newsroom uses separate public URLs for separately published language versions.

- Keep language and geography separate.
- Use one canonical URL per published language page.
- Every language version lists itself and every sibling with reciprocal hreflang metadata.
- Keep an explicit, visible language switcher.
- Do not force visitors away from a language page based on inferred country or browser language.
- A future language hint may only be a dismissible suggestion after its destination exists.
- Use the registry language tag on the root html element.
- Predominantly right-to-left pages, including Hebrew, use semantic root direction with dir="rtl".
- Adding a language is a version-bound content change and still needs the normal review gate.

The architecture should tolerate nb, en, fr, de, ja, ko, hi, he and Chinese language tags such as zh-Hans or zh-Hant without implying that a translation already exists or has independent native-language review.
