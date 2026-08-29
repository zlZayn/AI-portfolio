"""Content contract tests for projects.yaml / profile.yaml / content/README.md.

Machine guards for the data layer:
- every project carries the required fields and a unique id;
- domains come from the 7-type enumeration;
- github_url is always owned by zlZayn;
- promoted traits never reappear in the project layer;
- any architecture tag with >= 6/9 coverage must be promoted to traits;
- traits match the coverage fact table in content/README.md, and every
  recorded coverage is >= 6/9.
"""

import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"

REQUIRED_FIELDS = [
    "id",
    "name",
    "domain",
    "tagline",
    "quote",
    "description",
    "ai_role",
    "code_role",
    "metric",
    "grid_overview",
    "github_url",
    "tech_stack",
    "highlights",
]

DOMAINS = {
    "数据处理",
    "RAG 检索",
    "Agent 基础设施",
    "内容安全",
    "视觉识别",
    "离线内容生成",
    "AIGC 创作",
}

# Promoted to profile.traits; the project layer must not re-declare them.
PROMOTED = {
    "Prompt Engineering",
    "Atomic Tool",
    "Business / Third-Party API",
    "Permission & Security Control",
}

COVERAGE_THRESHOLD = 6
README_TABLE_ROW = re.compile(r"^\|\s*(.+?)\s*\|\s*(\d+)/9\s*\|\s*≥6/9\s*\|\s*$")


def load_projects() -> list[dict]:
    with open(str(CONTENT / "projects.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)["projects"]


def load_profile() -> dict:
    with open(str(CONTENT / "profile.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


def read_coverage_table() -> dict:
    text = (CONTENT / "README.md").read_text(encoding="utf-8")
    documented = {}
    for line in text.splitlines():
        match = README_TABLE_ROW.match(line)
        if match:
            documented[match.group(1).strip()] = int(match.group(2))
    return documented


class ContentContractTests(unittest.TestCase):
    def setUp(self):
        self.projects = load_projects()
        self.profile = load_profile()

    def test_all_required_fields_present(self):
        for project in self.projects:
            for field in REQUIRED_FIELDS:
                self.assertIn(field, project, f"{project['id']} missing {field}")
                self.assertTrue(project[field], f"{project['id']} has empty {field}")

    def test_ids_are_unique_and_total_nine(self):
        ids = [p["id"] for p in self.projects]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(ids), 9)

    def test_domain_comes_from_enumeration(self):
        for project in self.projects:
            self.assertIn(project["domain"], DOMAINS, project["id"])

    def test_github_url_owned_by_zlzayn(self):
        for project in self.projects:
            self.assertTrue(
                project["github_url"].startswith("https://github.com/zlZayn/")
                or project["github_url"].startswith("https://zlzayn.github.io/"),
                project["id"],
            )

    def test_tag_sections_nonempty(self):
        for project in self.projects:
            stack = project["tech_stack"]
            for section in ("architecture", "technology", "delivery"):
                self.assertTrue(stack.get(section), f"{project['id']} empty {section}")

    def test_promoted_traits_hidden_from_project_layer(self):
        for project in self.projects:
            for tag in project["tech_stack"]["architecture"]:
                self.assertNotIn(tag, PROMOTED, f"{project['id']} re-declares {tag}")

    def test_high_coverage_tags_are_promoted(self):
        traits = {item["name"] for item in self.profile["traits"]}
        counts = {}
        for project in self.projects:
            for tag in project["tech_stack"]["architecture"]:
                counts[tag] = counts.get(tag, 0) + 1
        for tag, count in counts.items():
            if count >= COVERAGE_THRESHOLD:
                self.assertIn(tag, traits, f"{tag} at {count}/9 must be promoted to traits")
        self.assertLessEqual(counts.get("Structured Output Parser", 0), COVERAGE_THRESHOLD - 1)

    def test_trait_entries_are_objects_with_name_and_note(self):
        traits = self.profile["traits"]
        self.assertTrue(traits)
        for item in traits:
            self.assertIn("name", item)
            self.assertIn("note", item)

    def test_traits_match_profile_and_coverage_table(self):
        traits = {item["name"] for item in self.profile["traits"]}
        documented = read_coverage_table()
        self.assertEqual(traits, set(documented), "profile.traits must match content/README.md fact table")
        for trait, covered in documented.items():
            self.assertGreaterEqual(covered, COVERAGE_THRESHOLD, f"{trait} recorded coverage")

    def test_every_project_has_a_registered_diagram(self):
        from src.diagrams import DIAGRAMS

        self.assertEqual({p["id"] for p in self.projects}, set(DIAGRAMS))


if __name__ == "__main__":
    unittest.main()