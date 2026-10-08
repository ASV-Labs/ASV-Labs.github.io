#!/usr/bin/env python3
"""Build design-tools/tools.json and design-tools/index.html from one catalog."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "design-tools"

SOURCE = {
    "name": "designengineer.tools",
    "url": "https://designengineer.tools",
    "retrieved": "2026-09-14",
    "note": (
        "Seeded from the public category listings on designengineer.tools. "
        "Normalized into ASV Labs section headings. No login-gated pages."
    ),
}

SKIPPED = [
    {
        "name": "Arc",
        "url": "https://arc.net/",
        "source_category": "Browser",
        "reason": "No MVP section for browsers.",
    },
    {
        "name": "Brave",
        "url": "https://brave.com/",
        "source_category": "Browser",
        "reason": "No MVP section for browsers.",
    },
    {
        "name": "Firefox",
        "url": "https://www.mozilla.org/firefox/new/",
        "source_category": "Browser",
        "reason": "No MVP section for browsers.",
    },
    {
        "name": "Zen",
        "url": "https://zen-browser.app/",
        "source_category": "Browser",
        "reason": "No MVP section for browsers.",
    },
    {
        "name": "MakeEmoji",
        "url": "https://makeemoji.com/",
        "source_category": "Emoji",
        "reason": "No MVP section for emoji makers.",
    },
]

# (id, heading, kicker, tools[])
# Each tool: name, blurb, url, source_category
SECTIONS = [
    (
        "inspiration",
        "Inspiration",
        "Galleries and reference",
        [
            ("60fps", "Motion-focused website gallery.", "https://60fps.design/", "Inspiration"),
            ("Awwwards", "Awards gallery for web design and development.", "https://www.awwwards.com/", "Inspiration"),
            ("Cosmos", "Visual search and moodboard library.", "https://www.cosmos.so/", "Inspiration"),
            ("Curated Design", "Hand-picked website design gallery.", "https://www.curated.design/", "Inspiration"),
            ("Design Spells", "Collection of clever interface details.", "https://www.designspells.com/", "Inspiration"),
            ("Game UI Database", "Archive of video game interface screenshots.", "https://www.gameuidatabase.com/", "Inspiration"),
            ("Godly", "Gallery of notable websites and interactions.", "https://godly.website/", "Inspiration"),
            ("HUDS+GUIS", "Collection of game HUD and GUI references.", "https://www.hudsandguis.com/", "Inspiration"),
            ("Interface In Game", "Catalog of video game user interfaces.", "https://interfaceingame.com/", "Inspiration"),
            ("Layers", "Community gallery of product and interface design.", "https://layers.to/explore", "Inspiration"),
            ("loadmo.re", "Gallery of web loading animations.", "https://loadmo.re/", "Inspiration"),
            ("Minimal Gallery", "Gallery of minimal websites.", "https://minimal.gallery/", "Inspiration"),
            ("Minimum", "Curated list of stripped-back sites.", "https://mnmm.xyz/", "Inspiration"),
            ("Mobbin", "Mobile and web UI pattern library.", "https://mobbin.com/", "Inspiration"),
            ("Pinterest", "Visual discovery and moodboarding.", "https://pinterest.com/", "Inspiration"),
            ("Rebrand", "Gallery of brand identity redesigns.", "https://www.rebrand.gallery/", "Inspiration"),
            ("Saaspo", "Gallery of SaaS landing pages and product sites.", "https://saaspo.com/", "Inspiration"),
            ("Same Energy", "Visual similarity search.", "https://same.energy/", "Inspiration"),
            ("SearchSystem", "Searchable archive of design references.", "https://searchsystem.co/", "Inspiration"),
            ("SEESAW", "Curated website inspiration gallery.", "https://www.seesaw.website/", "Inspiration"),
            ("SOOT SPIRAL", "Interactive inspiration spiral from SOOT.", "https://spiral.soot.com/spiral", "Inspiration"),
            ("Supahero", "Gallery of website hero sections.", "https://www.supahero.io/", "Inspiration"),
        ],
    ),
    (
        "ai-agents-ides-coding",
        "AI agents / IDEs / coding",
        "From AI Code and Research",
        [
            ("Bolt.new", "In-browser AI app builder.", "https://bolt.new/", "AI Code"),
            ("Claude Code", "Anthropic's agentic coding CLI.", "https://claude.com/product/claude-code", "AI Code"),
            ("Cline", "Open-source coding agent for the editor.", "https://cline.bot/", "AI Code"),
            ("Cursor", "AI-native code editor.", "https://www.cursor.com/", "AI Code"),
            ("OpenAI Codex", "OpenAI's coding agent.", "https://openai.com/codex/", "AI Code"),
            ("Skills", "Directory of agent skill files.", "https://skills.sh/", "AI Code"),
            ("v0 by Vercel", "AI UI generation from Vercel.", "https://v0.dev/", "AI Code"),
            ("Windsurf", "Agentic IDE from Windsurf.", "https://codeium.com/windsurf", "AI Code"),
            ("Zed", "High-performance editor with agentic features.", "https://zed.dev/agentic", "AI Code"),
            ("ChatGPT", "OpenAI conversational assistant.", "https://chatgpt.com/", "Research"),
            ("Google Gemini", "Google conversational assistant.", "https://gemini.google.com/", "Research"),
            ("NotebookLM", "Google research notebook with source-grounded AI.", "https://notebooklm.google/", "Research"),
        ],
    ),
    (
        "components",
        "Components",
        "UI kits and primitives",
        [
            ("21st.dev", "Marketplace of UI components.", "https://21st.dev/", "Components"),
            ("Component Gallery", "Directory of design-system components.", "https://component.gallery/", "Components"),
            ("Cursify", "Cursor and pointer effect components.", "https://cursify.vercel.app/", "Components"),
            ("Fancy Components", "Animated React component library.", "https://www.fancycomponents.dev/", "Components"),
            ("Framer University Resources", "Framer component and resource library.", "https://framer.university/resources", "Components"),
            ("Motion Primitives", "Animated component primitives.", "https://motion-primitives.com/", "Components"),
            ("NumberFlow", "Animated number component.", "https://number-flow.barvian.me/", "Components"),
            ("React Bits", "Collection of animated React components.", "https://www.reactbits.dev/", "Components"),
            ("shadcn/ui", "Copy-paste React component system.", "https://ui.shadcn.com/", "Components"),
        ],
    ),
    (
        "color-easing",
        "Color & easing",
        "From Web Utility",
        [
            ("Color.review", "Color pair contrast reviewer.", "https://color.review/", "Web Utility"),
            ("Easing Editor", "Interactive easing-curve editor.", "https://animejs.com/easing-editor", "Web Utility"),
            ("Easing Functions", "Visual cheat sheet of CSS easing curves.", "https://easings.net/", "Web Utility"),
            ("Easing Gradients", "Tool for perceptually eased color gradients.", "https://larsenwork.com/easing-gradients/", "Web Utility"),
            ("OKLCH Color Picker", "OKLCH color picker and converter.", "https://oklch.com/", "Web Utility"),
        ],
    ),
    (
        "productivity",
        "Productivity",
        "Desktop, organization, and web utilities",
        [
            ("Claude Cowork", "Claude desktop agent for local files and tasks.", "https://claude.com/product/cowork", "Desktop Utility"),
            ("Deskflow", "Share a keyboard and mouse across computers.", "https://deskflow.org", "Desktop Utility"),
            ("Granola", "AI meeting notes for the desktop.", "https://www.granola.ai/", "Desktop Utility"),
            ("LocalSend", "Local-network file sharing.", "https://localsend.org/", "Desktop Utility"),
            ("Raycast", "Keyboard launcher for macOS.", "https://www.raycast.com/", "Desktop Utility"),
            ("Warp", "AI-assisted terminal.", "https://www.warp.dev/", "Desktop Utility"),
            ("Wispr Flow", "Voice-to-text dictation.", "https://wisprflow.ai/", "Desktop Utility"),
            ("Linear", "Issue tracking for product teams.", "https://linear.app/", "Organization"),
            ("Trello", "Kanban boards for tasks.", "https://trello.com/", "Organization"),
            ("Ray.so", "Code screenshot maker.", "https://ray.so/", "Web Utility"),
            ("RegExr", "Browser regular-expression tester.", "https://regexr.com/", "Web Utility"),
        ],
    ),
    (
        "video-capture",
        "Video & Capture",
        "Record, cut, and share",
        [
            ("DaVinci Resolve", "Professional video edit and color suite.", "https://www.blackmagicdesign.com/products/davinciresolve", "Video & Capture"),
            ("LosslessCut", "Lossless video and audio cutter.", "https://mifi.no/losslesscut/", "Video & Capture"),
            ("NVIDIA ShadowPlay", "GPU game and desktop capture.", "https://www.nvidia.com/en-us/software/nvidia-app/#shadowplay", "Video & Capture"),
            ("OBS Studio", "Open-source streaming and recording.", "https://obsproject.com/", "Video & Capture"),
            ("OpenCut", "Open-source video editor.", "https://opencut.app/", "Video & Capture"),
            ("Parsec", "Low-latency remote desktop.", "https://parsec.app/", "Video & Capture"),
            ("Recordly", "Browser-based screen recorder.", "https://recordly.dev/", "Video & Capture"),
            ("Screen Studio", "Mac screen recording for product videos.", "https://screen.studio/", "Video & Capture"),
            ("ShareX", "Windows screen capture and sharing.", "https://getsharex.com/", "Video & Capture"),
            ("ui.camera", "UI screenshot and capture tool.", "https://ui.camera/", "Web Utility"),
        ],
    ),
    (
        "whiteboard-knowledge",
        "Whiteboard / knowledge",
        "From Whiteboard and Organization",
        [
            ("Excalidraw", "Hand-drawn style whiteboard.", "https://excalidraw.com/", "Whiteboard"),
            ("FigJam", "Figma collaborative whiteboard.", "https://www.figma.com/figjam/", "Whiteboard"),
            ("Miro", "Online collaborative whiteboard.", "https://miro.com/", "Whiteboard"),
            ("Muse", "Spatial canvas for thinking.", "https://museapp.com/", "Whiteboard"),
            ("tldraw", "Infinite canvas SDK and whiteboard.", "https://www.tldraw.com/", "Whiteboard"),
            ("AFFiNE", "Local-first notes and whiteboard workspace.", "https://affine.pro/", "Organization"),
            ("Are.na", "Visual research and collection tool.", "https://www.are.na/", "Organization"),
            ("Eagle", "Local design-asset organizer.", "https://en.eagle.cool/", "Organization"),
            ("Obsidian", "Local markdown knowledge base.", "https://obsidian.md/", "Organization"),
        ],
    ),
    (
        "design-tools",
        "Design tools",
        "Interface, type, visual, and SVG",
        [
            ("Figma", "Collaborative interface design.", "https://figma.com", "Interface"),
            ("Framer", "Design-to-site tool for interactive websites.", "https://www.framer.com/", "Interface"),
            ("Paper", "Interface design canvas.", "https://paper.design/", "Interface"),
            ("Penpot", "Open-source design and prototype tool.", "https://penpot.app/", "Interface"),
            ("Rive", "Interactive motion graphics for products.", "https://rive.app", "Interface"),
            ("Stitch by Google Labs", "AI UI design from Google Labs.", "https://stitch.withgoogle.com/", "Interface"),
            ("Best Free Fonts", "Directory of free typefaces.", "https://bestfreefonts.com/", "Fonts"),
            ("Fonts In Use", "Archive of typography in the wild.", "https://fontsinuse.com/", "Fonts"),
            ("Fontshare", "Free font family library.", "https://www.fontshare.com/", "Fonts"),
            ("Free Faces", "Gallery of free fonts.", "https://www.freefaces.gallery/", "Fonts"),
            ("UNCUT", "Independent type foundry and font catalog.", "https://uncut.wtf/", "Fonts"),
            ("Bitspace", "Node-based visual programming.", "https://bitspace.sh/", "Visual"),
            ("cables", "Browser visual programming for graphics.", "https://cables.gl/", "Visual"),
            ("Nodes", "Visual programming environment.", "https://nodes.io/", "Visual"),
            ("NodeToy", "Node-based shader editor.", "https://nodetoy.co/", "Visual"),
            ("ShaderToy", "Community shader playground.", "https://www.shadertoy.com/", "Visual"),
            ("TouchDesigner", "Node-based realtime visual tool.", "https://derivative.ca/", "Visual"),
            ("Unicorn.studio", "Web visual-effects design tool.", "https://www.unicorn.studio/", "Visual"),
            ("SVGOMG", "SVG optimizer with an SVGO GUI.", "https://jakearchibald.github.io/svgomg/", "Web Utility"),
        ],
    ),
    (
        "motion-lottie",
        "Motion / Lottie",
        "From Motion",
        [
            ("Cavalry", "Procedural motion design app.", "https://cavalry.scenegroup.co/", "Motion"),
            ("Jitter", "Web motion design for product UI.", "https://jitter.video/", "Motion"),
            ("Lottie Creator", "Official Lottie animation editor.", "https://lottiefiles.com/lottie-creator", "Motion"),
            ("Lottielab", "Lottie editor and collaboration.", "https://www.lottielab.com/", "Motion"),
            ("Theatre.js", "Animation toolkit for the web.", "https://www.theatrejs.com/", "Motion"),
        ],
    ),
    (
        "audio",
        "Audio",
        "Voice, middleware, and samples",
        [
            ("ElevenLabs", "AI voice generation.", "https://elevenlabs.io/", "Audio"),
            ("FMOD", "Interactive audio middleware.", "https://www.fmod.com/", "Audio"),
            ("Splice", "Sample and sound library.", "https://splice.com/features/sounds", "Audio"),
        ],
    ),
    (
        "three-d",
        "3D",
        "From 3D, Volumetric, glTF, and Digital Fashion",
        [
            ("Bezi", "Collaborative 3D design.", "https://www.bezi.com/", "3D"),
            ("Blender", "Open-source 3D suite.", "https://www.blender.org/", "3D"),
            ("Houdini", "Procedural 3D and VFX.", "https://www.sidefx.com/", "3D"),
            ("Spline", "Browser 3D design.", "https://spline.design/", "3D"),
            ("Womp", "Browser 3D modeling.", "https://womp.com/", "3D"),
            ("Depthkit", "Volumetric video capture.", "https://www.depthkit.tv/", "Volumetric"),
            ("KIRI Engine", "Photogrammetry and 3D scanning.", "https://www.kiriengine.app/", "Volumetric"),
            ("Luma AI", "AI 3D capture and scenes.", "https://lumalabs.ai/interactive-scenes", "Volumetric"),
            ("Polycam", "LiDAR and photogrammetry 3D capture.", "https://poly.cam/", "Volumetric"),
            ("RealityScan", "Photogrammetry from Epic Games.", "https://www.unrealengine.com/en-US/realityscan", "Volumetric"),
            ("SuperSplat Editor", "Gaussian splat editor.", "https://superspl.at/editor", "Volumetric"),
            ("gltfjsx", "Convert glTF models to React JSX.", "https://github.com/pmndrs/gltfjsx", "glTF"),
            ("gltfpack", "glTF compression and optimization.", "https://github.com/zeux/meshoptimizer/blob/master/gltf/README.md", "glTF"),
            ("Needle Viewer", "glTF and 3D scene viewer.", "https://viewer.needle.tools/", "glTF"),
            ("CLO", "3D fashion design software.", "https://www.clo3d.com/", "Digital Fashion"),
            ("Marvelous Designer", "3D garment simulation.", "https://www.marvelousdesigner.com/", "Digital Fashion"),
            ("Style3D", "3D fashion design platform.", "https://www.linctex.com/", "Digital Fashion"),
        ],
    ),
]


def tool_dict(name: str, blurb: str, url: str, source_category: str) -> dict:
    return {
        "name": name,
        "blurb": blurb,
        "url": url,
        "source_category": source_category,
    }


def catalog() -> dict:
    sections = []
    for section_id, heading, kicker, tools in SECTIONS:
        sections.append(
            {
                "id": section_id,
                "heading": heading,
                "kicker": kicker,
                "tools": [tool_dict(*tool) for tool in tools],
            }
        )
    return {
        "title": "ASV Labs Design Engineer Tools",
        "source": SOURCE,
        "curated_by": "ASV Labs",
        "skipped": SKIPPED,
        "sections": sections,
    }


def pad(index: int) -> str:
    return f"{index:02d}"


def render_tool_row(tool: dict, index: int) -> str:
    name = html.escape(tool["name"])
    blurb = html.escape(tool["blurb"])
    url = html.escape(tool["url"], quote=True)
    source = html.escape(tool["source_category"])
    aria = html.escape(f"Open {tool['name']}")
    return f"""            <li class="tool-row">
              <span class="tool-row__index">{pad(index)}</span>
              <div class="tool-row__identity">
                <h3><a href="{url}">{name}</a></h3>
                <p>{blurb}</p>
              </div>
              <dl class="tool-row__meta">
                <div>
                  <dt>Source group</dt>
                  <dd>{source}</dd>
                </div>
              </dl>
              <a class="tool-row__open" href="{url}" aria-label="{aria}">
                <span aria-hidden="true">↗</span>
              </a>
            </li>"""


def render_html(data: dict) -> str:
    tool_count = sum(len(section["tools"]) for section in data["sections"])
    skipped_count = len(data["skipped"])
    jump_links = "\n".join(
        f'            <a href="#{html.escape(section["id"])}">{html.escape(section["heading"])} <span>{pad(len(section["tools"]))}</span></a>'
        for section in data["sections"]
    )
    section_blocks = []
    for index, section in enumerate(data["sections"], start=1):
        rows = "\n".join(
            render_tool_row(tool, tool_index)
            for tool_index, tool in enumerate(section["tools"], start=1)
        )
        heading = html.escape(section["heading"])
        kicker = html.escape(section["kicker"])
        section_id = html.escape(section["id"])
        count = pad(len(section["tools"]))
        section_blocks.append(
            f"""      <section class="ledger tools-section" id="{section_id}" aria-labelledby="{section_id}-title">
        <div class="section-rail">
          <span>{heading}</span>
          <span>{kicker}</span>
          <span>{count} tools</span>
        </div>
        <div class="tools-section__heading">
          <h2 id="{section_id}-title"><span>{pad(index)}</span>{heading}</h2>
        </div>
        <ol class="tool-list">
{rows}
        </ol>
      </section>"""
        )

    sections_html = "\n\n".join(section_blocks)
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta
      name="description"
      content="ASV Labs Design Engineer Tools — a curated map of public tools for design engineers, seeded from designengineer.tools."
    />
    <meta name="theme-color" content="#071411" />
    <meta property="og:title" content="ASV Labs — Design Engineer Tools" />
    <meta
      property="og:description"
      content="A curated tools map for design engineers. Seeded from designengineer.tools; curated by ASV Labs."
    />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://asv-labs.github.io/design-tools/" />
    <meta name="twitter:card" content="summary" />
    <title>Design Engineer Tools — ASV Labs</title>
    <link rel="canonical" href="https://asv-labs.github.io/design-tools/" />
    <link rel="icon" href="../assets/mark.svg" type="image/svg+xml" />
    <link rel="stylesheet" href="../assets/styles.css" />
    <link rel="stylesheet" href="../assets/design-tools.css" />
    <script src="../assets/app.js" defer></script>
    <script src="catalog.js" defer></script>
  </head>
  <body class="tools-page">
    <a class="skip-link" href="#main">Skip to content</a>
    <div class="pointer-field" aria-hidden="true">
      <span class="pointer-field__x"></span>
      <span class="pointer-field__y"></span>
      <span class="pointer-field__dot"></span>
    </div>

    <header class="site-header" data-on-dark>
      <a class="wordmark" href="/" aria-label="ASV Labs home">
        <span>ASV</span><b>/</b><span>LABS</span>
      </a>
      <nav aria-label="Primary navigation">
        <a href="/">Public work</a>
        <a href="/design-tools/" aria-current="page">Design tools</a>
        <a href="#index">Index</a>
      </nav>
      <div class="header-actions">
        <a class="header-page" href="/">Public work</a>
        <a class="header-github" href="https://github.com/ASV-Labs">
          GitHub
          <span aria-hidden="true">↗</span>
        </a>
      </div>
    </header>

    <main id="main">
      <section class="hero tools-hero" id="top" aria-labelledby="hero-title">
        <div class="hero__copy">
          <p class="eyebrow"><span>Design engineer tools</span><span>Public index / 2026</span></p>
          <h1 id="hero-title">
            Tools map
            <em>for design engineers.</em>
          </h1>
          <p class="hero__dek">
            A curated index of public tools: name, what it is, and the outbound URL.
            Seeded from the public listings on
            <a href="https://designengineer.tools">designengineer.tools</a>
            and grouped into ASV Labs sections.
          </p>
          <a class="text-action" href="#index">
            Browse the index
            <span aria-hidden="true">↓</span>
          </a>
        </div>

        <aside class="field-note" id="field" aria-label="About this index">
          <div class="field-note__index">FIELD / 02</div>
          <div class="field-note__body">
            <p class="field-note__label">About this index</p>
            <p>
              Public links only. Categories from the source site are normalized into
              the headings below. {skipped_count} browser and emoji listings were
              skipped as ambiguous fits.
            </p>
          </div>
          <div class="field-note__status">
            <span class="status-dot" aria-hidden="true"></span>
            <span id="catalog-summary">{tool_count} public tools / 11 sections</span>
          </div>
        </aside>
      </section>

      <section class="tools-index" id="index" aria-labelledby="index-title">
        <div class="section-rail">
          <span>Index</span>
          <span>Jump to a section</span>
          <span id="tool-count">{pad(tool_count)} entries</span>
        </div>
        <div class="tools-index__heading">
          <h2 id="index-title">Eleven sections.<br />No private-roadmap theater.</h2>
          <p>
            One-line descriptions are ASV Labs editorial notes for each public listing.
            Original source groups stay visible on every row.
          </p>
        </div>
        <nav class="tools-jump" aria-label="Section index">
{jump_links}
        </nav>
      </section>

{sections_html}

      <section class="closing" aria-labelledby="closing-title">
        <p class="eyebrow"><span>Source</span><span>Public listings only</span></p>
        <h2 id="closing-title">Seeded from the public field.<br />Kept as a ledger.</h2>
        <a href="https://designengineer.tools">
          Visit designengineer.tools
          <span aria-hidden="true">↗</span>
        </a>
      </section>
    </main>

    <footer class="site-footer">
      <a class="wordmark" href="/"><span>ASV</span><b>/</b><span>LABS</span></a>
      <p>Seeded from <a href="https://designengineer.tools">designengineer.tools</a>; curated by ASV Labs.</p>
      <p>© <span id="year">2026</span> ASV Labs</p>
    </footer>
  </body>
</html>
"""


def main() -> None:
    data = catalog()
    names = [tool["name"] for section in data["sections"] for tool in section["tools"]]
    if len(names) != len(set(names)):
        raise SystemExit("Duplicate tool names in catalog")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUT_DIR / "tools.json"
    html_path = OUT_DIR / "index.html"
    json_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    html_path.write_text(render_html(data), encoding="utf-8")
    tool_count = sum(len(section["tools"]) for section in data["sections"])
    print(f"Wrote {json_path.relative_to(ROOT)} and {html_path.relative_to(ROOT)}")
    print(f"{len(data['sections'])} sections / {tool_count} tools / {len(data['skipped'])} skipped")
    for section in data["sections"]:
        print(f"  {section['heading']}: {len(section['tools'])}")


if __name__ == "__main__":
    main()
