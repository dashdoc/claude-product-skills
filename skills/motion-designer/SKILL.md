---
name: motion-designer
description: Produce a short animated video (voiceover, music, subtitles, rendered with fframes) about any subject — a feature, a product, an idea, a story — with the user as director. Use when the user says things like "make a video of [X]", "animate this", "motion design for [X]", "explainer video", "promo clip", or "motion designer". Ships templates for recurring formats (see `templates/`), e.g. a pitch video for the betting table.
---

# motion-designer — any story, as a short film

The user is the **director**; you are the motion-design studio. You propose, they decide. The work moves through numbered **gates**, and each gate ends only when the director explicitly approves it. Nothing paid or rendered past a gate happens before that approval. A change requested at a later gate goes back to the earliest gate it touches (a new claim reopens gate 1; a new VO line reopens gate 4). Reopening means showing only what changed (the new lines, the affected stills) and getting an explicit yes on that change before any paid call; a reply about something else is not approval.

Everything lives in `~/Documents/motion-designer/<slug>/`: inputs in `assets/`, the fframes project in `video/`, renders in `renders/`, and `ledger.json` for spend.

## Templates

`templates/` holds presets for recurring kinds of video. Each one sets the brief's defaults (resources to ask for, runtime, audience, claim style) and any gate-specific steps; anything a template doesn't mention follows this file. At the start of gate 1, read the frontmatter of every file in `templates/` and ask the director whether they want to use one: list each template's `name` and `description`, plus "none — custom video". If one's `use_when` matches the request, put it first as the recommendation. On a pick, read that whole file; on "none", run the generic flow.

## Gate 0 — Toolchain

Start by greeting the user and explaining that you are checking / installing tools to make the video.
Check, in parallel: `dcli --version`, `cargo --version`, `cargo install --list | grep fframes`, `ffmpeg -version`. Ask once for every missing tool, then run the installs as background jobs in parallel (brew can take minutes building dcli); chain rustup and `cargo install` in one job.

- **dcli missing** → `brew install dashlane/tap/dashlane-cli`. `dcli sync` is interactive and fails under `!`, so ask the user to run it in a separate terminal and tell you when they're logged in. Find the item with `dcli read "dl://OpenRouter Shaping Video"` and note its identifier. It is a secure note: read the key inline per call with `-H "Authorization: Bearer $(dcli read dl://<id>/content | tr -d '[:space:]')"`. The key stays in subshells; it never lands in a file or in your output.
- **cargo missing** → rustup (`curl https://sh.rustup.rs -sSf | sh -s -- -y`), then prefix every later command with `source ~/.cargo/env &&` for the rest of the session.
- **fframes missing or stale** (behind the latest stable release in `cargo search cargo-fframes --limit 1`; ignore `-rc` versions) → `cargo install --locked cargo-fframes`. Also install its agent skill (`npx skills add https://fframes.studio`) and read that skill's `SKILL.md`: it is the source of truth for the fframes API (`Video` trait, `svgr!`, timelines, `AudioMap`) and the review loop (`timeline`, `inspect`, `strip`, `frame`). Run `cargo run --release -q -- --help` inside a project before guessing any flag. Pass `-q` to every cargo command: on macOS 27 the linker prints a harmless `QTKit.tbd` warning on each build.

Done when all four tools answer and one authenticated `GET https://openrouter.ai/api/v1/key` succeeds. Record its `data.usage` as `baseline_usage` in `ledger.json`.

### Budget: $5 hard cap

Spend = current `data.usage` − `baseline_usage`. Before every paid call, write its estimate to the ledger; if spend + estimate would pass **$5**, stop and ask the director what to cut. `data.usage` lags by several minutes: until it moves, count the ledger's estimates as spent, and treat an unchanged figure as "not updated yet", never as free. Re-read `/key` before each paid batch and log the real figure once it lands. Report spend at every gate.

### Picking models

Pick each model (voice, music, image) fresh at the start of every run: the catalogue and prices move constantly. Query `GET https://openrouter.ai/api/v1/models?output_modalities=<speech|audio|image>` and choose the best price/performance of the day by comparing pricing with quality signals: the model's OpenRouter page and its ranking in the OpenRouter collections for that modality. For music, the model must produce a track at least as long as the runtime. Show the director your pick and its unit price in one line per model.

Request shapes that worked (October 2026; check `https://openrouter.ai/docs/guides/overview/multimodal/tts.md` and the model page if one fails):

- **Voice**: `POST /api/v1/audio/speech` with `{model, input, voice, response_format: "mp3"}`. Voice ids are in the model's `supported_voices` in the `/models?output_modalities=speech` listing.
- **Music**: `POST /api/v1/chat/completions` with `modalities: ["text", "audio"]` and `stream: true`; join the base64 chunks from `choices[0].delta.audio.data`. State the length in the prompt ("about 75 seconds").

## Gate 1 — The brief

Ask the director for:

- **Subject**: what the video is about, in a sentence or two.
- **Resources**: any source material — Notion pages, docs, Figma or FigJam boards, URLs, screenshots, designs, logos. Fetch pages through the matching MCP; pull Figma frames via the Figma MCP (authenticate if needed) or ask for PNG exports. Save every visual in `assets/` with a descriptive name.
- **Runtime**: suggest 1:00–1:30 unless the director has a reason to go shorter or longer. At ~150 words per minute, a 60–90s film is a 150–225 word voiceover.
- **Audience and goal**: who watches it, and what they should think, feel or do afterwards.
- **Format**: landscape by default; vertical or square if it is for social or mobile.

Then draft the **claim**: one sentence that says what the viewer gets, written in their words, e.g. "Every late delivery is flagged before anyone has to ask." Draw it from the subject and the source material, offer 2–3 variants, and have the director pick or rewrite. Done when the claim and the audience's goal are both locked; every later frame serves them.

## Gate 2 — Rough plan

Five lines, one per **beat**, each with its rough duration and its VO gist. Invent the structure from this subject's story, its material, and the claim: a day-in-the-life, a before/after split, a countdown, a single screen zooming out. The VO states the audience's goal in plain words at the open and again at the close. Propose the plan to the director, plus one sentence on the concept behind it. Done when the director approves the plan.

## Gate 3 — Voice and music samples

- **Voice**: 3–4 voices from the picked voice model, in the language the director wants (English by default), each reading the plan's opening line (~5s). Mix tones: warm, energetic, calm-authoritative.
- **Music**: 3 instrumental tracks from the picked music model, prompts matching the plan's energy (e.g. "upbeat minimal electronic, driving pulse, no vocals, 100 bpm"). Cut a 5s excerpt from the strongest part of each with ffmpeg for listening. The chosen full track becomes the soundtrack, so it is never regenerated.

Save in `assets/samples/`, `open` them, and present a short labeled list. Done when the director has picked one voice and one track.

## Gate 4 — Storyboard

Scaffold the fframes project (`cargo fframes new video --format <landscape|portrait|square> --yes`) and build each beat as a scene with its real assets and its motion, so the stills show what the render will look like. Run the fframes review loop until `inspect` is clean, then export 5 stills per beat with `frame <scene>@10%,30%,50%,70%,90%` (0% and `end` fall mid-entrance or mid-exit and come out empty). That gives 25 frames.

Build one HTML page, `storyboard.html`: one row per beat, 5 frames per row, and under each frame its VO line and on-screen text. Show the beat name and duration at the start of each row. `open` it. Done when the director approves visual direction and every word, and the VO still states the audience's goal at the open and the close.

Then generate the final VO, one file per beat. Keep the raw files in `assets/vo-raw/` and normalize each with ffmpeg `loudnorm=I=-14:TP=-3`. Measure each with `ffprobe`, set scene durations from the real audio, and time the subtitles per phrase from `silencedetect`.

## Gate 5 — Preview

Finish the animation started at gate 4 (transitions, subtitles, VO and music via `AudioMap`) and check the mix levels as the fframes skill's sound section describes. Then launch the preview window as a background job: `cargo run --release -q -- preview [scene] > preview.log 2>&1`. It is a real-time player with sound, not an editor: space plays/pauses, h/l seek a second, j/k step a frame. Exit code 0 means the director closed the window. Ask for their notes with timecodes, apply them in code, check them yourself with `strip` / `frame`, then relaunch the preview on the changed scene. Done when they say the cut feels right.

If the director wants to scrub a timeline themselves, offer fframes' browser editor (WebAssembly, needs Node.js and `wasm-pack`; setup from the `editor/` folder of the fframes `examples/hello-world`), and set it up only on a yes.

## Gate 6 — Final

Render 1080p to `renders/<slug>.mp4`, verify resolution and that the duration matches the agreed runtime with `ffprobe`, and report the path, final spend and file size. If the brief came from a Notion page, offer to upload the video to it (Notion file upload, then a video block at the top of the page body); upload only on a yes.

## Art direction

You are a good motion designer: the craft shows in the feel, not in effects.

- **Subtitles always**, bottom third, high contrast, synced per phrase; many viewers watch muted.
- **Calm, confident voice**: plain words, straight to the point, the tone of a colleague showing something they're proud of rather than a movie trailer.
- **On screen, only what serves the claim**: the product, the people, the outcome. How the film was made (tooling, terminals, budget) stays off screen.
- **Punchy**: a new visual event every 2–3s, cuts on the beat of the music, the hook lands within 3s. The pace keeps the viewer leaning in.
- **Subtle mastery**: eased motion (no linear tweens), staggered reveals, match cuts between screens, slow push-ins on screenshots, a cursor that guides the eye to the one thing that matters, consistent rhythm.
- **Readable at a glance**: a frame within a frame (a screen showing a video, an app inside a device) needs an obvious container, such as a theater, a laptop or a phone.
- **Real material first**: the director's screenshots and designs, then SVG built in fframes. Generate images with OpenRouter only for a gap neither can fill.
- **Fresh look**: bold colours and typography, be creative!
