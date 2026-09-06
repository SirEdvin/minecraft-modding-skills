import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


MODULE_PATH = Path(__file__).with_name("validate-skills.py")
SPEC = importlib.util.spec_from_file_location("validate_skills", MODULE_PATH)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        (self.root / "skills" / "example-skill").mkdir(parents=True)
        (self.root / "schemas").mkdir()
        schema = json.loads(
            (MODULE_PATH.parents[1] / "schemas" / "skills.sh.schema.json").read_text()
        )
        (self.root / "schemas" / "skills.sh.schema.json").write_text(json.dumps(schema))
        self.write_skill()
        self.write_manifest(["example-skill"])
        self.write_readme(["example-skill"])

    def tearDown(self):
        self.tempdir.cleanup()

    def write_skill(self, metadata="version: 1.0.0", description="Useful example skill.", body=""):
        text = (
            "---\n"
            "name: example-skill\n"
            f"description: {description}\n"
            "license: MIT\n"
            "metadata:\n"
            f"  {metadata}\n"
            "---\n"
            f"# Example\n{body}"
        )
        (self.root / "skills" / "example-skill" / "SKILL.md").write_text(text)

    def write_manifest(self, skills):
        manifest = {"groupings": [{"title": "Tests", "skills": skills}]}
        (self.root / "skills.sh.json").write_text(json.dumps(manifest))

    def write_readme(self, skills):
        entries = "\n".join(f"- `{name}` — Description." for name in skills)
        (self.root / "README.md").write_text(f"# Test\n\n## Skills\n\n{entries}\n\n## Install\n")

    def errors(self):
        return validator.validate_repository(self.root)

    def assert_error(self, text):
        self.assertTrue(any(text in error for error in self.errors()), self.errors())

    def test_valid_repository(self):
        self.assertEqual([], self.errors())

    def test_metadata_requires_string_keys_and_values(self):
        for metadata in (
            "nested: {key: value}",
            "items: [one, two]",
            "version: 1.0",
            "1: value",
        ):
            with self.subTest(metadata=metadata):
                self.write_skill(metadata=metadata)
                self.assert_error("metadata must map string keys to string values")

    def test_description_routing_policy(self):
        for description in ("x" * 61 + ".", "Missing period", '"Two\\nlines."'):
            with self.subTest(description=description):
                self.write_skill(description=description)
                self.assert_error("description must be one line, at most 60 characters, and end with a period")

    def test_duplicate_yaml_key_is_rejected_without_traceback(self):
        self.write_skill(metadata="version: 1.0.0\n  version: 2.0.0")
        errors = self.errors()
        self.assertTrue(any("duplicate YAML key 'version'" in error for error in errors), errors)
        self.assertFalse(any("Traceback" in error for error in errors), errors)

    def test_invalid_yaml_timestamp_is_rejected_without_traceback(self):
        for timestamp in ("2026-99-99", "2026-09-06T25:00:00Z"):
            with self.subTest(timestamp=timestamp):
                self.write_skill(metadata=f"version: 1.0.0\n  reviewed: {timestamp}")
                errors = self.errors()
                self.assertTrue(any("invalid YAML" in error for error in errors), errors)
                self.assertFalse(any("Traceback" in error for error in errors), errors)

    def test_non_string_top_level_frontmatter_key_is_rejected_without_traceback(self):
        path = self.root / "skills" / "example-skill" / "SKILL.md"
        path.write_text(path.read_text().replace("license: MIT\n", "license: MIT\n1: invalid\n"))
        errors = self.errors()
        self.assertTrue(
            any("frontmatter keys must be strings: 1" in error for error in errors),
            errors,
        )
        self.assertFalse(any("Traceback" in error for error in errors), errors)

    def test_missing_and_escaping_support_links(self):
        self.write_skill(body="See `references/missing.md`.\n")
        self.assert_error("missing local reference references/missing.md")
        outside = self.root / "outside.md"
        outside.write_text("outside")
        self.write_skill(body="[escape](../../outside.md)\n")
        self.assert_error("local reference escapes skill package")

    def test_symlink_cannot_escape_package(self):
        outside = self.root / "outside.md"
        outside.write_text("outside")
        (self.root / "skills" / "example-skill" / "references").mkdir()
        (self.root / "skills" / "example-skill" / "references" / "escape.md").symlink_to(outside)
        self.write_skill(body="See `references/escape.md`.\n")
        self.assert_error("local reference escapes skill package")

    def test_urls_anchors_placeholders_and_code_examples_are_exempt(self):
        self.write_skill(
            body=(
                "[web](https://example.com/file.md) [mail](mailto:test@example.com) "
                "[section](#section) [template](<path/<modid>/file.md>)\n"
                "Use `https://example.com/file.md` and `src/main/resources/fabric.mod.json`.\n"
            )
        )
        self.assertEqual([], self.errors())

    def test_fenced_markdown_links_and_backticks_are_exempt(self):
        skill = self.root / "skills" / "example-skill"
        (skill / "templates").mkdir()
        for fence in ("```", "~~~"):
            with self.subTest(fence=fence):
                (skill / "templates" / "README.md").write_text(
                    f"{fence}markdown\n"
                    "[Contributing](CONTRIBUTING.md)\n"
                    "Use `references/missing.md`.\n"
                    f"{fence}\n"
                )
                self.write_skill(body="Use `templates/README.md`.\n")
                self.assertEqual([], self.errors())

    def test_standard_markdown_relative_link_and_multihop_support(self):
        skill = self.root / "skills" / "example-skill"
        (skill / "references").mkdir()
        (skill / "references" / "first.md").write_text("Continue to [second](second.md).\n")
        (skill / "references" / "second.md").write_text("Done.\n")
        self.write_skill(body="Read [the first reference](references/first.md).\n")
        self.assertEqual([], self.errors())

    def test_support_reachability_can_traverse_root_and_assets_markdown(self):
        skill = self.root / "skills" / "example-skill"
        (skill / "assets").mkdir()
        (skill / "references").mkdir()
        (skill / "index.md").write_text("Continue to [assets](assets/index.md).\n")
        (skill / "assets" / "index.md").write_text(
            "Continue to [guide](../references/guide.md).\n"
        )
        (skill / "references" / "guide.md").write_text("Done.\n")
        self.write_skill(body="Read [the index](index.md).\n")
        self.assertEqual([], self.errors())

    def test_unreachable_support_file_is_rejected(self):
        skill = self.root / "skills" / "example-skill"
        (skill / "templates").mkdir()
        (skill / "templates" / "unused.md").write_text("Unused.\n")
        self.assert_error("support file is not reachable from SKILL.md: templates/unused.md")

    def test_manifest_must_exactly_cover_skills_without_duplicates(self):
        self.write_manifest([])
        self.assert_error("missing skill entry 'example-skill'")
        manifest = {
            "groupings": [
                {"title": "One", "skills": ["example-skill"]},
                {"title": "Two", "skills": ["example-skill"]},
            ]
        }
        (self.root / "skills.sh.json").write_text(json.dumps(manifest))
        self.assert_error("duplicate skill entry 'example-skill'")

    def test_readme_catalog_must_exactly_cover_skills_without_duplicates(self):
        self.write_readme([])
        self.assert_error("README Skills catalog missing entry 'example-skill'")
        self.write_readme(["example-skill", "example-skill"])
        self.assert_error("README Skills catalog has duplicate entry 'example-skill'")

    def test_readme_catalog_rejects_malformed_bullet(self):
        (self.root / "README.md").write_text(
            "# Test\n\n## Skills\n\n- `example-skill`: Description.\n\n## Install\n"
        )
        self.assert_error("invalid Skills catalog entry")

    def test_unicode_format_control_reports_file_and_line(self):
        readme = self.root / "README.md"
        readme.write_text(readme.read_text() + "Hidden \u202e text.\n")
        self.assert_error("README.md:8: Unicode format control U+202E")

    def test_unicode_check_ignores_dependencies_but_checks_docs_and_skills(self):
        dependency = self.root / "node_modules" / "dependency"
        dependency.mkdir(parents=True)
        (dependency / "README.md").write_text("Ignored \u202e text.\n")
        docs = self.root / "docs"
        docs.mkdir()
        (docs / "guide.md").write_text("Hidden \u202e text.\n")
        skill = self.root / "skills" / "example-skill" / "SKILL.md"
        skill.write_text(skill.read_text() + "Hidden \u202e text.\n")

        errors = self.errors()
        self.assertTrue(any("docs/guide.md:1: Unicode format control" in error for error in errors), errors)
        self.assertTrue(any("skills/example-skill/SKILL.md:9: Unicode format control" in error for error in errors), errors)
        self.assertFalse(any("node_modules" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
