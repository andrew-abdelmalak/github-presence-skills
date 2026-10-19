# Writing style

The house style for everything these skills write: READMEs, profile text, community files, release notes, and pull request descriptions. It follows the spirit of the [Google developer documentation style guide](https://developers.google.com/style): clear, direct, and written for a reader who is busy and new to the project.

## Contents

- [Principles](#principles)
- [Words to avoid](#words-to-avoid)
- [Structure and formatting](#structure-and-formatting)
- [Accessibility](#accessibility)
- [Self-check](#self-check)

## Principles

1. **Lead with what it is and what it does.** The first sentence a reader sees answers "what is this, and why would I use it?" Put history, motivation, and credits later.
2. **Write for the reader's task.** Address the reader as "you." Use the imperative for steps ("Run", "Set", "Open").
3. **Use the active voice and the present tense.** Write "The CLI reads `config.toml`", not "`config.toml` will be read by the CLI".
4. **Be specific.** A number, a command, or a named file beats an adjective. "Parses 2 GB logs in 40 s on a laptop (see `bench/`)" beats "blazing fast". If you have no number, cut the adjective instead of inventing one.
5. **One idea per sentence. Short paragraphs.** Most sentences should stay under about 25 words.
6. **Define a term the first time you use it,** unless the audience certainly knows it.
7. **Match the existing voice when editing.** When improving a document, keep the author's correct content and tone. Change what is wrong or unclear, not what is merely different.

## Words to avoid

These read as hype or filler, and many are common tells of machine-written text. Replace each with a specific fact or delete it.

| Avoid | Why | Instead |
|---|---|---|
| blazing fast, lightning-fast, high-performance | Unverifiable | A measured number, or nothing |
| simple, easy, just, simply, effortless | Untrue for the reader who is stuck | Show the steps and let the reader judge |
| seamless, robust, powerful, cutting-edge, next-generation, revolutionary, game-changer | Empty praise | Name the property: "retries failed uploads three times" |
| leverage, utilize, harness, unlock, empower, delve, elevate, streamline | Inflated verbs | use, run, help, read, improve |
| "Welcome to X!", "In today's fast-paced world" | Filler openings | Start with what X does |
| "and more!", "and much more" | Hides the real scope | List the real items or stop |

Also avoid:
- More than one exclamation mark in a document.
- Emoji in headings, and emoji as bullet markers, in repository documents. A profile README may use a few when the owner wants them.
- Reflexive groups of three, where a list has three items only because three sounds complete.
- Em dashes as general punctuation. Prefer a comma, a colon, parentheses, or a new sentence.

## Structure and formatting

- **One H1** per document: the project or document name. Use sentence case for headings ("Getting started", not "Getting Started").
- **Order sections by what the reader needs first**: what it is, how to install it, how to use it, then everything else.
- **Code blocks** always name their language (` ```bash `, ` ```python `). Show commands without a leading `$` so readers can copy them. Show output in a separate block, or not at all.
- **Use lists and tables for parallel items,** and prose for reasoning. A table needs at least two columns of real information.
- **Use relative links** for files in the same repository. Write link text that describes the target ("see the configuration reference"), never "click here".
- **Use GitHub alert blocks** (`> [!NOTE]`, `> [!WARNING]`) sparingly, for information a reader must not miss. More than three in a README dilutes them.
- **Keep line content renderable.** Avoid raw HTML except for centered heroes, `<picture>` elements for light and dark images, and `<details>` for long optional content.

## Accessibility

- Every image has alt text that says what the image shows or does. Decorative images get `alt=""`.
- Do not put meaning in color alone. A badge's text must carry the information.
- Do not put essential text inside images. Screen readers and search cannot read it.
- Heading levels go in order: an H3 sits under an H2.
- When the README has animated GIFs, say what they show in text near them.

## Self-check

Before handing over any document, check:

- [ ] The first two sentences say what it is and who it is for.
- [ ] Every command was found in the project's files or verified to run.
- [ ] No word from the "Avoid" table remains without a specific fact behind it.
- [ ] Every link and image path resolves, either relative or absolute.
- [ ] Every `TODO` placeholder is listed in the response.
