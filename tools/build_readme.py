#!/usr/bin/env python3
"""Build README.md for the profile from one place, so layout and palette stay consistent.

Author: Sebastian R.O. Marshall

  python3 tools/build_readme.py        writes README.md with an empty STATS marker
  python3 sync_profile.py --from <site repo>   then fills the markers from the portfolio's data

One palette runs through every badge: deep teal, teal, cyan, blue, sea green, with amber as the
single accent. The page is curated for a technical audience: skills, research code and activity. The CV lives on the portfolio site.
"""
import os
import urllib.parse as U

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEEP, TEAL, CYAN, SKY, BLUE, SEA, GREEN, AMBER = "0a3a4a", "0e7490", "0891b2", "0284c7", "1d6fa5", "0f766e", "059669", "d97706"


def q(s):
    return U.quote(s.replace("-", "--").replace("_", "__").replace(" ", "_"), safe="_")


def badge(text, color, logo=None, label=None, alt=None, style="flat-square"):
    core = (q(label) + "-" if label else "") + q(text) + "-" + color
    u = f"https://img.shields.io/badge/{core}?style={style}"
    if logo:
        u += f"&amp;logo={logo}&amp;logoColor=white"
    return f'<img src="{u}" alt="{alt or text}"/>'


def two(left, right):
    return ('<table width="100%">\n<tr>\n<td width="50%" valign="top">\n\n' + left + '\n\n</td>\n<td width="50%" valign="top">\n\n'
            + right + "\n\n</td>\n</tr>\n</table>")


SKILLS = [
    ("Programming Languages", TEAL, [("Python", "python"), ("R", "r"), ("SQL", "postgresql"), ("MATLAB", None), ("JavaScript", "javascript"), ("C#", None)]),
    ("Machine Learning &amp; Data Science", CYAN, [("TensorFlow", "tensorflow"), ("PyTorch", "pytorch"), ("scikit-learn", "scikitlearn"), ("XGBoost", None), ("Pandas", "pandas"), ("NumPy", "numpy"), ("xarray", None)]),
    ("GIS &amp; Remote Sensing", SKY, [("Earth Engine", "googleearthengine"), ("SMAP", None), ("SWOT", None), ("QGIS", "qgis"), ("ArcGIS", "arcgis"), ("GDAL", None), ("Rasterio", None)]),
    ("Hydrological &amp; Coastal Modeling", SEA, [("SWAT / SWAT+", None), ("HEC-RAS", None), ("HEC-HMS", None), ("NASA LISF", "nasa"), ("HAND-FIM", None), ("Delft3D", None), ("MIKE Suite", None)]),
    ("Cloud &amp; DevOps", BLUE, [("AWS", "amazonwebservices"), ("Docker", "docker"), ("GitHub Actions", "githubactions"), ("Git", "git"), ("Linux", "linux")]),
    ("Databases", GREEN, [("PostgreSQL", "postgresql"), ("MySQL", "mysql"), ("SQL Server", None)]),
]
DOMAINS = [("Climate Extremes", DEEP), ("Climate & Food Systems", TEAL), ("Climate & Health", CYAN), ("Water Cycle from Space", SKY),
           ("Data Assimilation", BLUE), ("Floods & Rivers", SEA), ("AI & Statistics", GREEN), ("Coasts & Water Systems", TEAL)]
TYPING = ["Climate extremes · water · food · health", "From orbit to field: satellites, models and statistics",
          "Water Prediction Innovators Fellow · CUAHSI 2026", "Erasmus Mundus Scholar · CHEC Scholar", "Licensed Professional Engineer"]


def link(href, inner):
    return f'<a href="{href}">{inner}</a>'


def skill_cell(g):
    name, color, tools = g
    return f"<b>{name}</b><br>\n" + " ".join(badge(t, color, logo) for t, logo in tools)


def build():
    typing = ("https://readme-typing-svg.demolab.com?font=JetBrains+Mono&amp;weight=400&amp;size=13&amp;duration=3000&amp;pause=1200"
              "&amp;color=22B8CF&amp;center=true&amp;vCenter=true&amp;width=640&amp;height=28&amp;lines=" + ";".join(U.quote_plus(l) for l in TYPING))
    skills = "\n".join(two(skill_cell(SKILLS[i]), skill_cell(SKILLS[i + 1])) for i in (0, 2, 4))
    return f'''<p align="center">
  <a href="https://rushmarshall.github.io"><img src="assets/header.svg" width="100%" alt="Sebastian R.O. Marshall, Climate Scientist and Ph.D. Researcher, Johns Hopkins University"/></a>
</p>

<p align="center">
<a href="https://git.io/typing-svg"><img src="{typing}" alt="Typing SVG"/></a>
</p>

<p align="center">
{link("https://rushmarshall.github.io", badge("rushmarshall.github.io", TEAL, "googlechrome", label="Portfolio", alt="Portfolio"))}&nbsp;
{link("https://scholar.google.com/citations?user=uck5WJAAAAAJ&amp;hl=en", badge("Google Scholar", CYAN, "googlescholar"))}&nbsp;
{link("https://orcid.org/0009-0001-0853-6200", badge("ORCID", SEA, "orcid"))}&nbsp;
{link("https://www.linkedin.com/in/marshallsebastian/", badge("LinkedIn", SKY, "linkedin"))}&nbsp;
{link("https://www.researchgate.net/profile/Sebastian-Marshall", badge("ResearchGate", GREEN, "researchgate"))}
</p>

### About me

I work at the intersection of climate science, hydrology, remote sensing, and environmental data science, with a focus on understanding how climate and environmental hazards affect water resources, agricultural systems, and human health.

As a Ph.D. researcher at **Johns Hopkins University**, my work integrates satellite Earth observations, hydrological and Earth system modeling, statistical methods, and machine learning to investigate climate and environmental risks across interconnected natural and human systems. I am particularly interested in how environmental variability and extremes translate into broader impacts on food security, population health, and societal resilience.

My current research explores drought dynamics and their implications for agricultural production, the vulnerability of national crop portfolios to concurrent climate extremes, and connections between soil moisture conditions and population health. I also investigate satellite-informed hydrology, flood inundation modeling, and data assimilation, with an emphasis on improving the reliability and practical value of environmental predictions. I welcome opportunities for research collaborations, fellowships, and interdisciplinary projects across academia, industry, and government.

<p align="center">
<!-- STATS:START --><!-- STATS:END -->
</p>

### Technical skills

{skills}

### What I work on

<p align="center">
{chr(10).join(badge(t, c) for t, c in DOMAINS)}
</p>

Most of my code is research code: reproducible Python pipelines that join satellite soil moisture, reanalysis and gauge records, hydrological models (SWAT, HAND flood mapping), and ensemble data assimilation. The code behind my 2026 *Journal of Hydrology* paper on SMAP soil-moisture assimilation over the Mekong is public: [mekong-swat-smap-enkf](https://github.com/rushmarshall/mekong-swat-smap-enkf).

### GitHub activity

<p align="center">
<img src="https://github-readme-streak-stats.herokuapp.com/?user=rushmarshall&amp;hide_border=true&amp;background=00000000&amp;ring=0e7490&amp;fire=d97706&amp;currStreakLabel=0e7490&amp;sideLabels=7d8590&amp;dates=7d8590&amp;currStreakNum=0891b2&amp;sideNums=7d8590" alt="Contribution streak" width="58%"/>
</p>

<p align="center">
{badge("CUAHSI", TEAL, label="Innovators Fellow", alt="CUAHSI")}
{badge("European Union", SKY, label="Erasmus Mundus", alt="Erasmus Mundus")}
{badge("China Harbour Engineering", SEA, label="CHEC Scholar", alt="CHEC")}
{badge("Jamaica", AMBER, label="P.E.", alt="P.E.")}
<br><sub>ASCE · EWRI · AGU · AWWA · COPRI · JIE Jamaica</sub>
</p>

<p align="center">
Open to collaborations on climate extremes, water, food and health.
<br><br>
<a href="https://www.linkedin.com/in/marshallsebastian/"><img src="https://img.shields.io/badge/Let's_Connect-{TEAL}?style=for-the-badge&amp;logo=linkedin&amp;logoColor=white" alt="Connect"/></a>
</p>

<p align="center">
  <a href="https://rushmarshall.github.io"><img src="assets/footer.svg" width="100%" alt="rushmarshall.github.io"/></a>
</p>
'''


if __name__ == "__main__":
    with open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8") as f:
        f.write(build())
    print("README.md written; now run sync_profile.py --from <site repo> to fill the Scholar numbers")
